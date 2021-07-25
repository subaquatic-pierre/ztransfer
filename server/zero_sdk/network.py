import json
from server.zero_sdk.utils import network_url_from_config


class Network:
    def __init__(self, config):
        self.url = network_url_from_config(config)
        self.miners = config.get("miners")
        self.sharders = config.get("sharders")
        self.remote_client_id = config.get("remote_client_id")
        self.blobbers = config.get("blobbers")

    def __str__(self) -> str:
        return json.dumps(
            {
                "url": self.url,
                "miners": self.miners,
                "sharders": self.sharders,
                "remote_client_id": self.remote_client_id,
                "blobbers": self.blobbers,
            },
            indent=4,
        )

    def __repr__(self) -> str:
        return f"Network(config)"
