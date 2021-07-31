import requests
import subprocess
from zero_sdk.utils import get_project_root

root_dir = get_project_root()

PUBLIC_KEY = "Needs to be secret from wallet"
PASSPHRASE = "Super secret passphrase"
MNEMONIC = "This needs to be super secret from wallet"


def sign_payload(private_key, hash_payload):
    file_path = f"{root_dir}/lib/bn254_signature_js/index.js"

    command = subprocess.Popen(
        ["node", file_path, private_key, hash_payload],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    )

    sig, err = command.communicate()
    if err == None:
        if len(sig.decode()) != 64:
            return False
        else:
            return sig.decode()
    else:
        return False


def heroku_sign(payload):
    url = f"https://example-0chain-crypto.herokuapp.com/sign?data={payload}&mnemonics={MNEMONIC}&passphrase={PASSPHRASE}"
    res = requests.get(url)
    return res.json()["hexString"]
