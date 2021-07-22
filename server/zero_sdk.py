import json
from blspy import AugSchemeMPL
import requests
from hashlib import sha3_256
from time import time
from server.network_data import network_data
from server.wallet_data import wallet_data
from server.sign import sign

TO_CLIENT_ID = "6dba10422e368813802877a85039d3985d96760ed844092319743fb3a76712d3"
BASE_URL = "https://beta.0chain.net"
WALLET_PUBLIC_KEY = wallet_data["Public_Key"]
WALLET_PRIVATE_KEY = wallet_data["Private_Key"]
WALLET_ID = wallet_data["ID"]


def pprint(res):
    print(json.dumps(res.json(), indent=4))


def hash(string):
    hash_object = sha3_256(bytes(string, "utf-8"))
    return f"{hash_object.hexdigest()}"


def get_network_info():
    url = f"{BASE_URL}/dns/network"
    res = requests.get(url)
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
        res = requests.put(url, json=data, headers=headers)
        results.append(res)

    for res in results:
        print(res.text)


def get_balance():
    url = f"{BASE_URL}/sharder01/v1/client/get/balance?client_id={WALLET_ID}"
    res = requests.get(url)
    pprint(res)


def add_tokens():
    url = f"{BASE_URL}/miner01/v1/transaction/put"
    headers = {"Content-Type": "application/json; charset=utf-8"}

    # Creation date
    creation_date = int(time())

    # Transaction data hash
    transaction_data_string = '{"name":"pour","input":{},"name":null}'
    transaction_data_hash = hash(transaction_data_string)

    # Main hash payload
    hash_string = f"{creation_date}:{WALLET_ID}:{TO_CLIENT_ID}:10000000000:{transaction_data_hash}"
    hash_payload = hash(hash_string)

    signature = sign(WALLET_PRIVATE_KEY, hash_payload)
    if signature == False:
        raise Exception("There was an error signing the transaction")

    # Build raw data
    data = {
        "hash": hash_payload,
        "signature": signature,
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

    res = requests.post(url, json=data, headers=headers)
    print(res)
    return res
