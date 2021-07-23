from pathlib import Path

from server.zero_sdk.utils import (
    from_yaml,
    get_home_path,
    hash_string,
    network_url_from_config,
)

HOME_DIR = f"{Path.home()}"
DEFAULT_NETWORK = "https://beta.0chain.net"


# Test get_home_path

res = get_home_path()
assert res == HOME_DIR, "get_home_path method not returning correct home path"

# -------------


# Test hash_string

message = "this is a super secret message"
res = hash_string(message)
assert len(res) == 64, "hash_string method not returning correct hash string length"

# -------------

# Test from_yaml

network_config = from_yaml(f"{HOME_DIR}/.zcn/config.yaml")
assert (
    network_config["block_worker"] is not None
), "from_yaml not returning correct config object"


# Test network_url_from_netwok_config
network_config = from_yaml(f"{HOME_DIR}/.zcn/config.yaml")
url = network_url_from_config(network_config)
assert url == DEFAULT_NETWORK, "network_url_from_config not returning correct url"
