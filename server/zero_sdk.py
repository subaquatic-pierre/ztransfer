import json
from blspy import PrivateKey, Util, AugSchemeMPL, PopSchemeMPL, G1Element, G2Element
import requests
from hashlib import sha3_256
from time import time
from server.network_data import network_data
from server.wallet_data import wallet_data
from server.utils import gen_sign_seed_array

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
    headers = {"Content-Type": "application/json; charset=utf-8"}

    # Creation date
    creation_date = int(time())

    # Transaction data hash
    transaction_data_hash = sha3_256(b'{"name":"pour","input":{},"name":null}')
    payload_string = f'"creation_date":{creation_date},"wallet_id":{WALLET_ID},"to_client_id":{TO_CLIENT_ID},"transaction_value":10000000000,"transaction_data":{transaction_data_hash.hexdigest()}'

    sign_key = AugSchemeMPL.key_gen(gen_sign_seed_array())
    payload_bytes = bytes(payload_string, "utf-8")

    signature = AugSchemeMPL.sign(sign_key, payload_bytes)
    payload_hash = sha3_256(payload_bytes)

    # Build raw data
    data = {
        "hash": payload_hash.hexdigest(),
        "signature": f"{signature}",
        "version": "1.0",
        "client_id": WALLET_ID,
        "creation_date": creation_date,
        "to_client_id": "6dba10422e368813802877a85039d3985d96760ed844092319743fb3a76712d3",
        "transaction_data": '{"name":"pour","input":{},"name":null}',
        "transaction_fee": 0,
        "transaction_type": 1000,
        "transaction_value": 10000000000,
        "txn_output_hash": "",
        "public_key": WALLET_PUBLIC_KEY,
    }

    res = make_request(url, method="POST", data=data, headers=headers)
    print(res)
