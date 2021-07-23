import requests
from time import time

from server.zero_sdk.utils import pprint, hash_string
from server.zero_sdk.network_data import network_data
from server.zero_sdk.sign import sign_payload
from server.zero_sdk.const import (
    MAIN_ALLOCATION_ID,
    TO_CLIENT_ID,
    BASE_URL,
    WALLET_PUBLIC_KEY,
    WALLET_PRIVATE_KEY,
    WALLET_ID,
)


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



