import json
from pathlib import Path
from hashlib import sha3_256


def pprint(res):
    print(json.dumps(res.json(), indent=4))


def hash_string(payload_string):
    hash_object = sha3_256(bytes(payload_string, "utf-8"))
    return f"{hash_object.hexdigest()}"


def get_project_root():
    return Path(__file__).parent.resolve().parent.resolve()


def get_home_path():
    return f"{Path().home()}"


def network_url_from_dns_path(dns_path: str) -> str:
    dns_path.split("/")
    return dns_path[:-1].join()
