import json
from zero_sdk.utils import network_url_from_config


class ConnectionBase:
    def _validate_response(self, res, error_message) -> object:
        """Validate network response
        Check network response status on each request
        Return error message if status code is not 200
        """
        if res.status_code == 200:
            return res.json()
        else:
            raise Exception(f"{error_message} - Message: {res.text}")


class Network:
    def __init__(self, config):
        self.url = network_url_from_config(config)
        self.miners = config.get("miners")
        self.sharders = config.get("sharders")
        self.remote_client_id = config.get("remote_client_id")

    def __str__(self) -> str:
        return json.dumps(
            {
                "url": self.url,
                "miners": self.miners,
                "sharders": self.sharders,
                "remote_client_id": self.remote_client_id,
            },
            indent=4,
        )

    def __repr__(self) -> str:
        return f"Network(config)"
