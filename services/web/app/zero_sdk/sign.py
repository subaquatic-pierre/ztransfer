import requests
import subprocess
from zero_sdk.utils import get_project_root

root_dir = get_project_root()

PUBLIC_KEY = "8aab74ef0f6cdb3a6f170001d3383ea6a0043a2df9e3094351cdc4dc14ec52093370860c4ff730c7199afd64b2451b64cc4772ce4e66ee51f0d396e1a0fc5d02"
PASSPHRASE = "0chain-client-split-key"
MNEMONIC = "crunch sheriff find bicycle demand review negative urge approve boy autumn panther bench know shock aerobic satoshi stomach roof stove brother eight core harbor"


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
