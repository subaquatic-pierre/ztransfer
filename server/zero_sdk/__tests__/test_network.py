from server.zero_sdk.network import Network
from server.zero_sdk.const import TO_CLIENT_ID, BASE_URL
from server.zero_sdk.utils import from_json, from_yaml, get_home_path

default_network_config = from_yaml(f"{get_home_path()}/.zcn/config.yaml")


# Test network has miners
network = Network(default_network_config, TO_CLIENT_ID)
assert len(network.miners) > 0, "No miners were loaded"

# Test network has sharders
network = Network(default_network_config, TO_CLIENT_ID)
assert len(network.sharders) > 0, "No sharders were loaded"

# Test network url
network = Network(default_network_config, TO_CLIENT_ID)
assert len(network.url) == BASE_URL, "Base network url not loaded correctly"

# Test network has remote client ID
network = Network(default_network_config, TO_CLIENT_ID)
assert network.remote_client_id is not None, "Base network url not loaded correctly"
