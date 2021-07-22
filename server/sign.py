from sys import stdout
from pathlib import Path
import requests
import subprocess
from server.wallet_data import wallet_data

root_dir = Path(__file__).parent.resolve()

SIGN_PUB_KEY = "d137d561a41be6a76c1998168d0b8561658576851e9006cde7538fd705093f022d41b0cbc78be80e562e4f5ccbc0bbc6690d7a2b765de96f645ac5d18a21ac11"
PASSPHRASE = "0chain-client-split-key"
MNEMONIC = wallet_data["mnemonics"]


def sign_payload(private_key, hash_payload):
    file_path = f"{root_dir}/lib/bn254_signature_js/index.js"

    command = subprocess.Popen(
        ["node", file_path, private_key, hash_payload],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    )

    sig, err = command.communicate()
    if err == None:
        return sig.decode()
    else:
        return False


def heroku_sign(payload):
    url = f"https://example-0chain-crypto.herokuapp.com/sign?data={payload}&mnemonics={MNEMONIC}&passphrase={PASSPHRASE}"
    res = requests.get(url)
    return res.json()["hexString"]
