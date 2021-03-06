import json
import yaml
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


def network_url_from_config(network_config) -> str:
    split = network_config["block_worker"].split("/")
    new_split = split[:-1]
    url = "/".join(new_split)
    return url


def from_json(filename) -> object:
    data = None
    with open(filename, "r") as f:
        data = json.load(f)

    verified_data = verify_data(data)
    return verified_data


def from_yaml(filename) -> object:
    data = None
    with open(filename, "r") as f:
        data = yaml.safe_load(f)

    verified_data = verify_data(data)
    return verified_data


def verify_data(data):
    if data == None:
        raise Exception("No data loaded")
    else:
        return data
