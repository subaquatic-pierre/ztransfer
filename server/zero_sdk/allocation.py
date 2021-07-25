import json


class Allocation:
    def __init__(self, id, wallet) -> None:
        self.id = id
        self.wallet = wallet

    def __str__(self) -> str:
        return json.dumps(
            {
                "id": self.id,
                "wallet_id": self.wallet.client_id,
                "network_url": self.wallet.network.url,
            },
            indent=4,
        )

    def __repr__(self) -> str:
        return f"Allocation(id, wallet)"
