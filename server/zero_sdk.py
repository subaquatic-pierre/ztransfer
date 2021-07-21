import json
import requests
from server.network_data import network_data
from server.wallet_data import wallet_data

print(wallet_data)


BASE_URL = "https://beta.0chain.net/"
WALLET_PUBLIC_KEY = wallet_data["Public_Key"]
WALLET_ID = wallet_data["ID"]


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
    print(json.dumps(res.json(), indent=4))


def create_wallet():
    miners = network_data.get("miners")
    results = []
    for miner in miners:
        # Build URL
        split = miner.split("/")
        miner_id = split[len(split) - 1]
        url = f"{BASE_URL}{miner_id}/v1/client/put"

        # Build Data
        headers = {"Accept": "application/json", "Content-Type": "application/json"}
        data = {
            "id": WALLET_ID,
            "version": None,
            "creation_date": None,
            "public_key": WALLET_PUBLIC_KEY,
        }

        # Make request
        res = make_request(url, data, method="PUT", headers=headers)
        results.append(res)

    print(results)


def get_balance():
    url = f"{BASE_URL}sharder01/v1/client/get/balance?client_id={WALLET_ID}"
    res = make_request(url)
    print(res)
