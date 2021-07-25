from server.zero_sdk.utils import network_url_from_config


class Network:
    def __init__(self, config, remote_client_id=None):
        self.url = network_url_from_config(config)
        self.miners = config.get("miners")
        self.sharders = config.get("sharders")
        self.remote_client_id = remote_client_id
