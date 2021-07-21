from blspy import AugSchemeMPL
import requests
from hashlib import sha3_256
from time import time

TO_CLIENT_ID = "6dba10422e368813802877a85039d3985d96760ed844092319743fb3a76712d3"
BASE_URL = "https://beta.0chain.net"
WALLET_PUBLIC_KEY = "b922221df8b9c84c87b864abd302c433a977776d5592638730c78b4b5301fb21b036a51d338d0096bbac1cfb38ffb5a5ebd5fbae69eded75d19ae1f154184d1c"
WALLET_ID = "895017f11f09cf9e173af81a3c47bf7ce9574f87ace390ebc0eac45ce18da352"


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

    res = requests.post(url, data=data, headers=headers)
    print(res)


def gen_sign_seed_array():
    return bytes(
        [
            0,
            50,
            6,
            244,
            24,
            199,
            1,
            25,
            52,
            88,
            192,
            19,
            18,
            12,
            89,
            6,
            220,
            18,
            102,
            58,
            209,
            82,
            12,
            62,
            89,
            110,
            182,
            9,
            44,
            20,
            254,
            22,
        ]
    )


# Request Data
# method = "POST"
# url = "https://beta.0chain.net/miner01/v1/transaction/put"
# headers = {"Content-Type": "application/json; charset=utf-8"}
# data = {
#     "hash": "232aef674a1fc71d079eabd3c99e273269dd3572aaf12f368829feff72ba5770",
#     "signature": "99620f5fc419b96ed1954d2d001f196dcc44a1cb434bdbd77f394234a9e480c0e52d8ca419a8876ed0ac9566fd88f3060777412e5d12373c6e0c07ea98ae6c9833e955ff535aed10031f873d1ab36ccb28deb2710e37dde04d6e377225392582",
#     "version": "1.0",
#     "client_id": "895017f11f09cf9e173af81a3c47bf7ce9574f87ace390ebc0eac45ce18da352",
#     "creation_date": 1626861193,
#     "to_client_id": "6dba10422e368813802877a85039d3985d96760ed844092319743fb3a76712d3",
#     "transaction_data": '{"name":"pour","input":{},"name":null}',
#     "transaction_fee": 0,
#     "transaction_type": 1000,
#     "transaction_value": 10000000000,
#     "txn_output_hash": "",
#     "public_key": "b922221df8b9c84c87b864abd302c433a977776d5592638730c78b4b5301fb21b036a51d338d0096bbac1cfb38ffb5a5ebd5fbae69eded75d19ae1f154184d1c",
# }

if __name__ == "__main__":
    add_tokens()
