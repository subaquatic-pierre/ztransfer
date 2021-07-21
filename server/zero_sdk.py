import json
import requests
import hashlib
from time import time
from server.network_data import network_data
from server.wallet_data import wallet_data

TO_CLIENT_ID = "6dba10422e368813802877a85039d3985d96760ed844092319743fb3a76712d3"
BASE_URL = "https://beta.0chain.net"
WALLET_PUBLIC_KEY = wallet_data["Public_Key"]
WALLET_ID = wallet_data["ID"]


def pprint(res):
    print(json.dumps(res.json(), indent=4))


def make_request(url, method="GET", data=None, headers=None):
    if method == "GET":
        res = requests.get(url, headers=headers)
        return res
    elif method == "POST":
        res = requests.post(url, data=data, headers=headers)
        return res
    elif method == "PUT":
        res = requests.put(url, data=data, headers=headers)
        return res


def get_network_info():
    url = f"{BASE_URL}/dns/network"
    res = make_request(url)
    pprint(res)


def create_wallet():
    miners = network_data.get("miners")
    results = []
    for miner in miners:
        # Build URL
        split = miner.split("/")
        miner_id = split[len(split) - 1]
        url = f"{BASE_URL}/{miner_id}/v1/client/put"

        # Build Data
        headers = {"Accept": "application/json", "Content-Type": "application/json"}
        data = {
            "id": WALLET_ID,
            "version": None,
            "creation_date": None,
            "public_key": WALLET_PUBLIC_KEY,
        }

        # Make request
        res = make_request(url, method="PUT", data=data, headers=headers)
        results.append(res)

    for res in results:
        print(res.text)


def get_balance():
    url = f"{BASE_URL}/sharder01/v1/client/get/balance?client_id={WALLET_ID}"
    res = make_request(url)
    pprint(res)


def add_tokens():
    url = f"{BASE_URL}/miner01/v1/transaction/put"
    headers = {"content-type: application/json; charset=utf-8"}

    # Creation date
    creation_date = int(time())

    # Transaction data hash
    transaction_data_hash = hashlib.sha3_256()
    transaction_data_hash.update(b'{"name":"pour","input":{},"name":null}')

    hash_array = [
        f"{creation_date}",
        WALLET_ID,
        TO_CLIENT_ID,
        f"{10000000000}",
        f"{transaction_data_hash.digest()}",
    ]

    hash_string = ":".join(hash_array)
    print(hash_string)

    # Build raw data
    # data = {
    #     "hash": "{{hash_of_request_data}}",
    #     "signature": "{{signature}}",
    #     "version": "1.0",
    #     "client_id": wallet_id,
    #     "creation_date": creation_date,
    #     "to_client_id": "6dba10422e368813802877a85039d3985d96760ed844092319743fb3a76712d3",
    #     "transaction_data": '{"name":"pour","input":{},"name":null}',
    #     "transaction_fee": 0,
    #     "transaction_type": 1000,
    #     "transaction_value": 10000000000,
    #     "txn_output_hash": "",
    #     "public_key": wallet_public_key,
    # }
