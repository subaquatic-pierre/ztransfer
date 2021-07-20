from urllib import parse
from urllib.request import Request
import urllib
import json
from server.network_data import network_data
from server.config import Config

config = Config()

BASE_URL = "https://beta.0chain.net/"
WALLET_PUBLIC_KEY = config.WALLET_PUBLIC_KEY
WALLET_ID = config.WALLET_ID


def make_request(req, data=None):
    response = None
    if data:
        with urllib.request.urlopen(req, data) as resp:
            response = json.loads(resp.read().decode("utf-8"))
    else:
        with urllib.request.urlopen(req) as resp:
            response = json.loads(resp.read().decode("utf-8"))

    return response


def get_network_info():
    url = f"{BASE_URL}/dns/network"
    request = Request(url, method="GET")
    response = make_request(request)
    obj = json.dumps(response, indent=4)
    print(obj)


def create_wallet():
    miners = network_data.get("miners")
    results = []
    for miner in miners:
        split = miner.split("/")
        miner_id = split[len(split) - 1]
        url = f"{BASE_URL}{miner_id}/v1/client/put"
        data = parse.urlencode(
            {
                "id": WALLET_ID,
                "version": None,
                "creation_date": None,
                "public_key": WALLET_PUBLIC_KEY,
            }
        )
        data = data.encode("ascii")
        request = Request(url, data, method="PUT")
        request.add_header("Accept", "application/json")
        request.add_header("Content-Type", "application/json")
        response = make_request(request, data)
        results.append(response)

    print(results)


def get_balance():
    url = f"{BASE_URL}sharder01/v1/client/get/balance?client_id={WALLET_ID}"
    res = make_request(url)
