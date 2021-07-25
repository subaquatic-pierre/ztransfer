from server.zero_sdk.wallet import Wallet
from server.zero_sdk.allocation import Allocation
from server.zero_sdk.const import MAIN_ALLOCATION_ID

wallet = Wallet()
print(wallet.network)
main_aloc = Allocation(MAIN_ALLOCATION_ID, wallet)

print(main_aloc)
