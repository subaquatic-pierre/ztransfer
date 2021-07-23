import requests
import json
import yaml

from zero_sdk.utils import get_home_path, network_url_from_dns_path


default_wallet = {}
default_network = {}
network_url = ""

with open(f"{get_home_path()}/.zcn/wallet.json", "r") as f:
    default_wallet = json.loads(f)

with open(f"{get_home_path()}/.zcn/wallet.json", "r") as f:
    default_network = yaml.safe_load(f)
    if default_network["block_worker"]:
        network_url = network_url_from_dns_path(default_network["block_worker"])


class Wallet:
    def __init__(self, config=default_wallet, network_url=network_url, default=True):
        if default == True:
            self.client_id = config["client_id"]
            self.client_key = config["client_key"]
            self.public_key = config["keys"][0]["public_key"]
            self.private_key = config["keys"][0]["public_key"]
            self.mnemonics = config["mnemonics"]
            self.version = config["version"]
            self.date_created = config["date_created"]
            self.network_url = network_url

    def get_network_info(self):
        url = f"{self.network_url}/dns/network"
        res = requests.get(url)
        error_message = f"An error occured fetching network info: {res.text}"
        self.return_response(res, error_message)

    def get_balance(self):
        url = f"{self.network_url}/sharder01/v1/client/get/balance?client_id={self.client_id}"
        res = requests.get(url)
        error_message = f"An error occured getting network info: {res.text}"
        self.return_response(res, error_message)

    def return_response(self, res, error_message):
        if res.status_code == 200:
            return res.json()
        else:
            return error_message

    def __repr__(self):
        return f"Wallet(config={default_wallet}, default=True/False)"

    def __str__(self):
        return f"""
            client_id: {self.client_id}, \n
            public_key: {self.public_key}, \n 
            private_key: {self.private_key}, \n
            mnemonics: {self.mnemonics}, \n     
            date_created: {self.date_created} \n   
            version: {self.version}
        """
