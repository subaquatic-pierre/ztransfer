from sys import stdout
from pathlib import Path
import requests
import subprocess
from server.zero_sdk.wallet_data import wallet_data

root_dir = Path(__file__).parent.resolve()

PUBLIC_KEY = "8aab74ef0f6cdb3a6f170001d3383ea6a0043a2df9e3094351cdc4dc14ec52093370860c4ff730c7199afd64b2451b64cc4772ce4e66ee51f0d396e1a0fc5d02"
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