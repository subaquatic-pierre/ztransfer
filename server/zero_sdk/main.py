import requests
from time import time

from zero_sdk.utils import pprint, hash_string
from zero_sdk.network_data import network_data
from zero_sdk.sign import sign_payload
from zero_sdk.const import (
    MAIN_ALLOCATION_ID,
    TO_CLIENT_ID,
    BASE_URL,
    WALLET_PUBLIC_KEY,
    WALLET_PRIVATE_KEY,
    WALLET_ID,
)


def get_network_info():
    url = f"{BASE_URL}/dns/network"
    res = requests.get(url)
    pprint(res)


def restore_wallet():
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
    transaction_data_hash = hash_string(transaction_data_string)

    # Main hash payload
    payload_string = f"{creation_date}:{WALLET_ID}:{TO_CLIENT_ID}:10000000000:{transaction_data_hash}"
    hashed_payload = hash_string(payload_string)

    signature = sign_payload(WALLET_PRIVATE_KEY, hashed_payload)
    if signature == False:
        raise Exception("There was an error signing the transaction")

    # Build raw data
    data = {
        "hash": hashed_payload,
        "signature": signature,
        "version": "1.0",
        "client_id": WALLET_ID,
        "creation_date": creation_date,
        "to_client_id": TO_CLIENT_ID,
        "transaction_data": transaction_data_string,
        "transaction_fee": 0,
        "transaction_type": 1000,
        "transaction_value": 10000000000,
        "txn_output_hash": "",
        "public_key": WALLET_PUBLIC_KEY,
    }

    res = requests.post(url, json=data, headers=headers)
    print(res.text)
    return res
