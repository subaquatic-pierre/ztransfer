from pathlib import Path

from server.zero_sdk.utils import (
    from_yaml,
    from_json,
    get_home_path,
    hash_string,
    network_url_from_config,
    verify_data,
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
# -------------


# Test network_url_from_netwok_config
network_config = {"block_worker": "https://beta.0chain.net/dns"}
url = network_url_from_config(network_config)
assert url == DEFAULT_NETWORK, "network_url_from_config not returning correct url"
# -------------

# Test from_json
wallet_config = from_json(f"{HOME_DIR}/.zcn/wallet.json")
assert (
    wallet_config["client_id"] is not None
), "from_json not returining correct wallet config"
# -------------

# Test verify_data
data = {"key": "value"}
verified_data = verify_data(data)
assert verified_data["key"] == "value", "verify_data not returning correct data object"
# -------------
