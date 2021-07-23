from server.zero_sdk.wallet import Wallet
import pytest

wallet = Wallet()
# no_config_wallet = Wallet(default_config=False)

print(hasattr(wallet, "client_id"))

# Test error raise if no config pass to wallet
with pytest.raises(Exception) as e:
    error_wallet = Wallet(default_config=False)
    assert (
        str(error_wallet.value)
        == "If default config not selected a config object needs to passed to constructor"
    ), "Error not raised on incorrect wallet config"

# Test Not default wallet
# no_config_wallet.get_balance()


# Test get_balance
balance = wallet.get_balance()
assert isinstance(balance, int), "Balance is not integer"
# ---------------


# wallet.add_tokens()
# new_balance = wallet.get_balance()
# print(balance)
# print(new_balance)
# assert new_balance == balance + (
#     1 * 100000000
# ), "add_token method did not add to wallet balance"
