import json
from hashlib import sha3_256


def pprint(res):
    print(json.dumps(res.json(), indent=4))


def hash_string(payload_string):
    hash_object = sha3_256(bytes(payload_string, "utf-8"))
    return f"{hash_object.hexdigest()}"
