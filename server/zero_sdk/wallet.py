import requests
import json
from time import time

from server.zero_sdk.utils import hash_string
from server.zero_sdk.sign import sign_payload, heroku_sign
from server.zero_sdk.network import Network
from server.zero_sdk.utils import (
    get_home_path,
    from_json,
    from_yaml,
)

from server.zero_sdk.const import (
    MAIN_ALLOCATION_ID,
    TO_CLIENT_ID,
)


default_wallet_config = {}
default_network_config = {}
network = ""

try:
    default_wallet_config = from_json(f"{get_home_path()}/.zcn/wallet.json")
except:
    print("Default wallet not loaded")

try:
    default_network_config = from_yaml(f"{get_home_path()}/.zcn/network_config.json")
except:
    print("Defualt network not loaded")


class Wallet:
    def __init__(self, default_config=True, config=None, network=None):
        # Raise error if no config object passed in and not default config
        if default_config == False and config == None:
            raise Exception(
                "If default config not selected a config object needs to passed to constructor"
            )
        # Set default config
        if default_config == True:
            config = default_wallet_config
            network = Network(default_network_config)

            # Set custom config
            self.client_id = config.get("client_id")
            self.client_key = config.get("client_key")
            self.public_key = config.get("keys")[0]["public_key"]
            self.private_key = config.get("keys")[0]["private_key"]
            self.mnemonics = config.get("mnemonics")
            self.version = config.get("version")
            self.date_created = config.get("date_created")
            self.network = network

        else:
            # Set custom config
            self.client_id = config.get("client_id")
            self.client_key = config.get("client_key")
            self.public_key = config.get("public_key")
            self.private_key = config.get("private_key")
            self.mnemonics = config.get("mnemonics")
            self.version = config.get("version")
            self.date_created = config.get("date_created")
            self.network = network

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
        # Implement wallet init
        pass

    def _validate_wallet(method):
        """Initialize wallet
        Check the wallet is initialized before every API request
        If wallet is not initialized, create a new wallet.
        """

        def wrapper(self, *args, **kwargs):
            if self.client_id is not None:
                return method(self, *args, **kwargs)
            else:
                self._init_wallet()
                raise Exception(
                    "Wallet is not initialized, call 'create_wallet, init_wallet or recover_wallet' methods to configure wallet"
                )

        return wrapper

    @_validate_wallet
    def get_network_info(self) -> object:
        url = f"{self.network.url}/dns/network"
        res = requests.get(url)
        error_message = f"An error occured fetching network info"
        res = self._validate_response(res, error_message)
        return res

    @_validate_wallet
    def get_balance(self) -> int:
        """Get Wallet balance
        Return float value of tokens
        """
        url = f"{self.network.url}/sharder01/v1/client/get/balance?client_id={self.client_id}"
        res = requests.get(url)
        error_message = f"An error occured getting wallet balance"
        res = self._validate_response(res, error_message)
        balance = int(res["balance"])
        return balance

    @_validate_wallet
    def add_tokens(self, amount=1) -> object:
        url = f"{self.network.url}/miner01/v1/transaction/put"
        headers = {"Content-Type": "application/json; charset=utf-8"}

        # Creation date
        creation_date = int(time())

        # Transaction data hash
        transaction_data_string = '{"name":"pour","input":{},"name":null}'
        transaction_data_hash = hash_string(transaction_data_string)

        # Main hash payload
        payload_string = f"{creation_date}:{self.client_id}:{self.network.remote_client_id}:10000000000:{transaction_data_hash}"
        hashed_payload = hash_string(payload_string)

        # signature = heroku_sign(hashed_payload)
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
            "to_client_id": self.network.remote_client_id,
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

    def restore_wallet(self):
        miners = self.network.miners
        results = []
        for miner in miners:
            # Build URL
            miner_id = miner["id"]
            url = f"{self.network.url}/{miner_id}/v1/client/put"

            # Build Data
            headers = {"Accept": "application/json", "Content-Type": "application/json"}
            data = {
                "id": self.client_id,
                "version": None,
                "creation_date": None,
                "public_key": self.public_key,
            }

            # Make request
            res = requests.put(url, json=data, headers=headers)
            results.append(res)

        for res in results:
            print(res.text)

    def __repr__(self):
        return f"Wallet(default_config=True, config={default_wallet_config}, network=Network({default_network_config}))"

    def __str__(self):
        return json.dumps(
            {
                "client_id": self.client_id,
                "public_key": self.public_key,
                "private_key": self.private_key,
                "mnemonics": self.mnemonics,
                "date_created": self.date_created,
                "version": self.version,
                "network_url": self.network.url,
            },
            indent=4,
        )
