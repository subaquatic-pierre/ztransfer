import json
from time import time
import requests
import os
from requests_toolbelt.multipart.encoder import MultipartEncoder
from server.zero_sdk.network import ConnectionBase
from server.zero_sdk.utils import get_home_path, hash_string, pprint
from random import randint
from reedsolo import RSCodec


class Allocation(ConnectionBase):
    def __init__(self, id, wallet, storage_address) -> None:
        self.id = id
        self.wallet = wallet
        self.storage_address = storage_address
        self.blobbers = self.get_allocation_info()["blobbers"]
        self.num_parity_shards = 2
        self.num_data_shards = 2

    def get_allocation_info(self):
        url = f"{self.wallet.network.sharders[0]}/v1/screst/{self.storage_address}/allocation?allocation={self.id}"
        res = requests.get(url)
        error_message = f"There was an error getting blobber info"
        valid_res = self._validate_response(res, error_message)
        return valid_res

    def get_blobbers(self):
        return self.blobbers

    def get_file_path(self, blobber, remote_path, headers):
        url = (
            f'{blobber["url"]}/v1/file/referencepath/{self.id}?paths=["{remote_path}"]'
        )
        res = requests.get(url, headers=headers)
        return res.json()

    def download_file(self, filepath):
        headers = {
            "X-App-Client-Id": self.wallet.client_id,
            "X-App-Client-Key": self.wallet.public_key,
        }

        results = []

        for blobber in self.blobbers:
            url = f"{blobber['url']}/v1/file/meta/{self.id}"
            res = requests.post(url, data={"path": filepath}, headers=headers)
            file_info = res.json()

            if res.status_code == 200:

                # Get latest read marker
                for sharder in self.wallet.network.sharders:
                    url = f"{sharder}/v1/screst/6dba10422e368813802877a85039d3985d96760ed844092319743fb3a76712d7/latestreadmarker?client={self.wallet.client_id}&blobber={blobber['id']}"
                    read_marker_res = requests.get(url)

                old_marker = read_marker_res.json()
                signature_payload = hash_string(
                    f"{old_marker['allocation_id']}:{old_marker['blobber_id']}:{old_marker['client_id']}:{old_marker['client_public_key']}:{old_marker['owner_id']}:{old_marker['counter']}:{old_marker['timestamp']}"
                )
                signature = self.wallet.sign(signature_payload)
                num_blocks = (
                    file_info.get("num_of_blocks")
                    if file_info.get("num_of_blocks")
                    else 1
                )

                counter = (
                    old_marker["counter"] + num_blocks
                    if old_marker.get("counter")
                    else num_blocks
                )
                path_hash = (
                    file_info.get("path_hash") if file_info.get("path_hash") else ""
                )

                read_marker = {
                    "client_id": self.wallet.client_id,
                    "client_public_key": self.wallet.public_key,
                    "blobber_id": blobber["id"],
                    "allocation_id": self.id,
                    "owner_id": self.wallet.client_id,
                    "timestamp": str(int(time())),
                    "counter": str(counter),
                    "signature": signature,
                }

                # Download the file
                url = f"{blobber['url']}/v1/file/download/{self.id}"
                data = MultipartEncoder(
                    fields={
                        "path_hash": path_hash,
                        "block_num": "1",
                        "num_blocks": str(num_blocks),
                        "read_marker": json.dumps(read_marker),
                    }
                )
                headers["Content-Type"] = data.content_type

                res = requests.post(url, data=data, headers=headers)
                results.append(res)

        return results

    def _hash_file(self, filename):
        hashed_file = None
        with open(filename, "r") as file:
            hashed_file = hash_string(file.read())

        return hashed_file

    def _shard_file(self, filename):
        rsc = RSCodec(2)
        with open(filename) as file:
            shard = rsc.encode(file.read().encode("utf-8"))
            return shard

    def upload_file(self, filepath):
        blobber = self.blobbers[0]

        split = filepath.split("/")
        filename = split.pop()

        file_size = os.path.getsize(filepath)
        hashed_file = self._hash_file(filepath)
        file_shards = self._shard_file(filepath)
        # file_shards = open(f'{get_home_path()}/.zcn/uploads/TOPS.txt')

        hashed_allocation_id = hash_string(self.id)
        signature = self.wallet.sign(hashed_allocation_id)

        upload_headers = {
            "X-App-Client-Id": self.wallet.client_id,
            "X-App-Client-Signature": signature,
            "X-App-Client-Key": self.wallet.public_key,
        }

        connection_id = str(randint(100000000, 999999999))

        upload_result = self._upload_shards(
            file_shards,
            filename,
            file_size,
            hashed_file,
            upload_headers,
            connection_id,
        )

        file_meta = self._build_file_meta(
            upload_result[0].json(), hashed_file, file_size, filename
        )

        allocation_info = self.get_file_path(
            blobber,
            remote_path=f"/{filename}",
            headers=upload_headers,
        )

        prev_allocation_root = allocation_info["latest_write_marker"]["allocation_root"]

        # Append new file meta to blobber tree
        allocation_info["list"].append(file_meta)

        res = self._commit(
            connection_id,
            prev_allocation_root,
            allocation_info,
            file_size,
        )

        print(res.text)

    def _upload_shards(
        self,
        file_shards,
        filename,
        filesize,
        hashed_file,
        headers,
        connection_id,
    ):
        blobber = self.blobbers[0]

        meta = {
            "connection_id": connection_id,
            "filename": filename,
            "filepath": f"/{filename}",
            "actualHash": hashed_file,
            "actual_size": filesize,
        }

        data = {"uploadMeta": json.dumps(meta), "connection_id": connection_id}

        files = {"uploadFile": file_shards}

        results = []

        for blobber in self.blobbers:
            url = f"{blobber['url']}/v1/file/upload/{self.id}"
            res = requests.post(url=url, data=data, files=files, headers=headers)
            results.append(res)

        # return res.json()
        return results

    def _commit(
        self,
        connection_id,
        prev_allocation_root,
        new_allocation_info,
        file_size,
    ):
        blobber = self.blobbers[0]
        url = f"{blobber['url']}/v1/connection/commit/{self.id}"
        timestamp = str(int(time()))
        new_allocation_root = hash_string(
            f"{new_allocation_info['meta_data']['hash']}:{timestamp}"
        )
        signature_payload = hash_string(
            f"{new_allocation_root}:{prev_allocation_root}:{self.id}:{blobber['id']}:{self.wallet.client_id}:{file_size}:{timestamp}"
        )
        signature = self.wallet.sign(signature_payload)

        results = []

        # for blobber in self.blobbers:
        data = MultipartEncoder(
            fields={
                "connection_id": connection_id,
                "write_marker": json.dumps(
                    {
                        "allocation_root": new_allocation_root,
                        "prev_allocation_root": prev_allocation_root,
                        "allocation_id": self.id,
                        "size": file_size,
                        "blobber_id": blobber["id"],
                        "timestamp": timestamp,
                        "client_id": self.wallet.client_id,
                        "signature": signature,
                    }
                ),
            }
        )

        headers = {
            "X-App-Client-Id": self.wallet.client_id,
            "X-App-Client-Key": self.wallet.public_key,
            "Connection": "Keep-Alive",
            "Cache-Control": "no-cache",
            "Transfer-Encoding": "chunked",
            "Content-Type": data.content_type,
        }

        # req = requests.Request(url=url, data=data, headers=headers)

        res = requests.post(
            url=url,
            data=data,
            headers=headers,
        )
        return res

    def _build_file_meta(self, upload_result, hashed_file, file_size, filename):
        meta_data = {
            "type": "f",
            "name": filename,
            "path": f"/{filename}",
            "size": upload_result["size"],
            "content_hash": upload_result["content_hash"],
            "merkle_root": upload_result["merkle_root"],
            "actual_file_hash": hashed_file,
            "actual_file_size": file_size,
            "attributes": {},
            "hash": None,
            "path_hash": None,
        }

        attributes = json.dumps(meta_data["attributes"])

        meta_data["hash"] = hash_string(
            f"{self.id}:{meta_data['type']}:{meta_data['name']}:{meta_data['path']}:{meta_data['size']}:{meta_data['content_hash']}:{meta_data['merkle_root']}:{meta_data['actual_file_size']}:{meta_data['actual_file_hash']}:{attributes}"
        )
        meta_data["path_hash"] = hash_string(f"{self.id}:{meta_data['path']}")

        return {"meta_data": meta_data}

    def __str__(self) -> str:
        return json.dumps(
            {
                "id": self.id,
                "wallet_id": self.wallet.client_id,
                "network_url": self.wallet.network.url,
            },
            indent=4,
        )

    def __repr__(self) -> str:
        return f"Allocation(id, wallet)"
