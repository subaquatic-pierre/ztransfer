from server.zero_sdk.const import MAIN_ALLOCATION_ID
from server.zero_sdk.allocation import Allocation
from server.zero_sdk.wallet import Wallet
from server.zero_sdk.network import Network

wallet = Wallet()
main_alloc = Allocation(MAIN_ALLOCATION_ID, wallet)

assert hasattr(main_alloc, "id"), "Allocation does not have an ID"
assert hasattr(main_alloc, "wallet"), "Wallet was not assigned to allocation"
