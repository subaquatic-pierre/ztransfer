import json
from server.zero_sdk.sign import sign_payload

import requests
import os
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

    def _upload_shards(
        self,
        file_shards,
        blobber,
        filename,
        filesize,
        hashed_file,
        headers,
        connection_id,
    ):
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

        return results

    def upload_file(self, filepath):
        split = filepath.split("/")
        filename = split.pop()

        file_size = os.path.getsize(filepath)
        hashed_file = self._hash_file(filepath)
        file_shards = self._shard_file(filepath)

        hashed_allocation_id = hash_string(self.id)
        signature = self.wallet.sign(hashed_allocation_id)

        upload_headers = {
            "X-App-Client-Id": self.wallet.client_id,
            "X-App-Client-Signature": signature,
            "X-App-Client-Key": self.wallet.public_key,
        }

        # while file_shards:
        connection_id = str(randint(100000000, 999999999))

        # shard = file_shards.pop()
        self._upload_shards(
            file_shards,
            blobber,
            filename,
            file_size,
            hashed_file,
            upload_headers,
            connection_id,
        )

        allocation_info = self.get_file_path(
            self.blobbers[0],
            remote_path=f"/{filename}",
            headers=upload_headers,
        )

        self.commit(
            blobber,
        )

    def commit(self, blobber, connection_id):
        data = {"connection_id": connection_id, "write_marker": json.dumps({})}

        headers = {
            "X-App-Client-Id": self.wallet.client_id,
            "X-App-Client-Key": self.wallet.public_key,
            "Connection": "Keep-Alive",
            "Cache-Control": "no-cache",
            "Transfer-Encoding": "chunked",
        }

        results = []
        for blobber in self.blobbers:
            url = f"{blobber['url']}/v1/connection/commit/{self.id}"
            res = requests.post(url=url, headers=headers, data=data)
            results.appned(res)

        return results

    def get_file_path(self, blobber, remote_path, headers):
        url = (
            f'{blobber["url"]}/v1/file/referencepath/{self.id}?paths=["{remote_path}"]'
        )
        res = requests.get(url, headers=headers)
        return res

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
