from server.zero_sdk.wallet import Wallet

wallet = Wallet()

balance = wallet.get_balance()
assert isinstance(balance, int), "Balance is not integer"

# wallet.add_tokens()
# new_balance = wallet.get_balance()
# print(balance)
# print(new_balance)
# assert new_balance == balance + (
#     1 * 100000000
# ), "add_token method did not add to wallet balance"
