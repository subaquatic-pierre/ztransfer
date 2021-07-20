from urllib.request import Request
import urllib
import json

BASE_URL = "https://beta.0chain.net/"


def make_request(req):
    response = None
    with urllib.request.urlopen(req) as resp:
        response = json.loads(resp.read().decode("utf-8"))

    return response


def get_network_info():
    url = f"{BASE_URL}/dns/network"
    request = Request(url, method="GET")
    response = make_request(request)
    obj = json.dumps(response, indent=4)
    print(obj)
