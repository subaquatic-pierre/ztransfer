import requests
import json
from time import time

from server.zero_sdk.utils import hash_string
from server.zero_sdk.sign import sign_payload
from server.zero_sdk.utils import (
    get_home_path,
    network_url_from_config,
    from_json,
    from_yaml,
)

from server.zero_sdk.const import (
    MAIN_ALLOCATION_ID,
    TO_CLIENT_ID,
    BASE_URL,
)


default_wallet = {}
default_network = {}
network_url = ""

try:
    default_wallet = from_json(f"{get_home_path()}/.zcn/wallet.json")
except:
    print("Default wallet not loaded")

try:
    default_network = from_yaml(f"{get_home_path()}/.zcn/config.yaml")
except:
    print("Defualt network not loaded")

try:
    network_url = network_url_from_config(default_network)
except:
    print("Default network not loaded")
    network_url = BASE_URL


class Wallet:
    def __init__(self, default_config=True, config=None, network_url=None):
        self.initialized = False

        # Raise error if no config object passed in and not default config
        if default_config == False and config == None:
            raise Exception(
                "If default config not selected a config object needs to passed to constructor"
            )

        # Set custom config
        if default_config == False:
            self.initialized = True
            self.client_id = config.get("client_id")
            self.client_key = config.get("client_key")
            self.public_key = config.get("client_id")
            self.private_key = config.get("client_id")
            self.mnemonics = config.get("mnemonics")
            self.version = config.get("version")
            self.date_created = config.get("date_created")
            self.network_url = network_url

        # Set default config
        if default_config == True:
            config = default_wallet
            network_url = network_url_from_config(default_network)

            self.initialized = True
            self.client_id = config["client_id"]
            self.client_key = config["client_key"]
            self.public_key = config["keys"][0]["public_key"]
            self.private_key = config["keys"][0]["private_key"]
            self.mnemonics = config["mnemonics"]
            self.version = config["version"]
            self.date_created = config["date_created"]
            self.network_url = network_url

    def _validate_response(self, res, error_message) -> object:
        """Validate network response
        Check network response status on each request
        Return error message if status code is not 200
        """
        if res.status_code == 200:
            return res.json()
        else:
            raise Exception(f"{error_message} - Message: {res.text}")

    def _init_wallet(self):
        print("Initialize the wallet if the wallet is not valid")

    def _validate_wallet(method):
        """Initialize wallet
        Check the wallet is initialized before every API request
        If wallet is not initialized, create a new wallet.
        """

        def wrapper(self, *args, **kwargs):
            # Check valid valid configutaion
            try:
                assert hasattr(self, "client_id")
            except Exception:
                raise Exception("Wallet as incorrect configutaion settings")

            if self.initialized == True:
                return method(self, *args, **kwargs)
            else:
                self._init_wallet()
                raise Exception(
                    "Wallet is not initialized, call 'create_wallet, init_wallet or recover_wallet' methods to configure wallet"
                )

        return wrapper

    @_validate_wallet
    def get_network_info(self) -> object:
        url = f"{self.network_url}/dns/network"
        res = requests.get(url)
        error_message = f"An error occured fetching network info"
        res = self._validate_response(res, error_message)
        return res

    @_validate_wallet
    def get_balance(self) -> int:
        """Get Wallet balance
        Return float value of tokens
        """
        url = f"{self.network_url}/sharder01/v1/client/get/balance?client_id={self.client_id}"
        res = requests.get(url)
        error_message = f"An error occured getting wallet balance"
        res = self._validate_response(res, error_message)
        return int(res["balance"])

    @_validate_wallet
    def add_tokens(self, amount=1) -> object:
        url = f"{self.network_url}/miner01/v1/transaction/put"
        headers = {"Content-Type": "application/json; charset=utf-8"}

        # Creation date
        creation_date = int(time())

        # Transaction data hash
        transaction_data_string = '{"name":"pour","input":{},"name":null}'
        transaction_data_hash = hash_string(transaction_data_string)

        # Main hash payload
        payload_string = f"{creation_date}:{self.client_id}:{TO_CLIENT_ID}:10000000000:{transaction_data_hash}"
        hashed_payload = hash_string(payload_string)

        signature = sign_payload(self.private_key, hashed_payload)
        if signature == False:
            raise Exception("There was an error signing the transaction")

        # Build raw data
        data = {
            "hash": hashed_payload,
            "signature": signature,
            "version": "1.0",
            "client_id": self.client_id,
            "creation_date": creation_date,
            "to_client_id": TO_CLIENT_ID,
            "transaction_data": transaction_data_string,
            "transaction_fee": 0,
            "transaction_type": 1000,
            "transaction_value": amount * 10000000000,
            "txn_output_hash": "",
            "public_key": self.public_key,
        }

        res = requests.post(url, json=data, headers=headers)
        error_message = "An error occurred adding tokens to wallet"
        res = self._validate_response(res, error_message)
        return res

    def __repr__(self):
        return (
            f"Wallet(default_config=True, config={default_wallet}, network_url=String)"
        )

    def __str__(self):
        return json.dumps(
            {
                "client_id": self.client_id,
                "public_key": self.public_key,
                "private_key": self.private_key,
                "mnemonics": self.mnemonics,
                "date_created": self.date_created,
                "version": self.version,
            },
            indent=4,
        )
