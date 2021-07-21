import json
from blspy import AugSchemeMPL
import requests
from hashlib import sha3_256
from time import time
from server.network_data import network_data
from server.wallet_data import wallet_data
from server.utils import gen_sign_seed_array

TO_CLIENT_ID = "6dba10422e368813802877a85039d3985d96760ed844092319743fb3a76712d3"
BASE_URL = "https://beta.0chain.net"
WALLET_PUBLIC_KEY = wallet_data["Public_Key"]
WALLET_ID = wallet_data["ID"]
MNEMONIC = wallet_data["Secret_Phrase"]
PASSPHRASE = "0chain-client-split-key"


def heroku_sign(payload):
    url = f"https://example-0chain-crypto.herokuapp.com/sign?data={payload}&mnemonics={MNEMONIC}&passphrase={PASSPHRASE}"
    res = requests.get(url)
    return res.json()["hexString"]


def pprint(res):
    print(json.dumps(res.json(), indent=4))


def hash(string):
    hash_object = sha3_256(bytes(string, "utf-8"))
    return f"{hash_object.hexdigest()}"


def sign(payload):
    # Create seed from mnemonic and '0chai'
    seed = f"{MNEMONIC} 0chain-client-split-key"

    # Convert array to bytes
    seed_bytes = bytes(seed, "utf-8")

    # Generate private key sith seed
    private_key = AugSchemeMPL.key_gen(seed_bytes)

    # Convert payload string to bytes
    message_bytes = bytes(payload, "utf-8")

    # Generate signature
    signature = AugSchemeMPL.sign(private_key, message_bytes)
    return signature.hex()


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

    # signature = sign(hash_payload)
    signature = heroku_sign(hash_payload)
    print(signature)

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
