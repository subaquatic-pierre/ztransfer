import json
from server.zero_sdk.utils import get_home_path
from server.zero_sdk.wallet import Wallet
from server.zero_sdk.allocation import Allocation
from server.zero_sdk.const import ALT_ALLOCATION_ID, MAIN_ALLOCATION_ID, STORAGE_ADDRESS

wallet = Wallet()
main_alloc = Allocation(ALT_ALLOCATION_ID, wallet, STORAGE_ADDRESS)

path = f"{get_home_path()}/.zcn/uploads/TOPS.txt"
main_alloc.upload_file(path)
