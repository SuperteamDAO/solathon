from typing import Union

from solathon.publickey import PublicKey
from .core.http import HTTPClient
from .core.types import RPCResponse

ENDPOINTS = (
    "https://api.mainnet-beta.solana.com",
    "https://api.devnet.solana.com",
    "https://api.testnet.solana.com",
)


class Client:
    def __init__(self, endpoint: str, local=False):
        if not local and endpoint not in ENDPOINTS:
            raise ValueError(
                "Invalid cluster RPC endpoint provided"
                " (Refer to https://docs.solana.com/cluster/rpc-endpoints)."
                " Use the argument local to use a local development endpoint."
            )
        self.http = HTTPClient(endpoint)

    def get_account_info(self, public_key: Union[PublicKey, str]
                         ) -> RPCResponse:
        data = self.http.build_data(
            method="getAccountInfo", params=[public_key]
        )
        res = self.http.send(data)
        return res

    def get_balance(self, public_key: Union[PublicKey, str]) -> RPCResponse:
        data = self.http.build_data(
            method="getBalance", params=[public_key]
        )
        res = self.http.send(data)
        return res

    def get_block(self, slot: int) -> RPCResponse:
        data = self.http.build_data(
            method="getBlock", params=[slot]
        )
        res = self.http.send(data)
        return res

    def get_transaction(self, signature: str) -> RPCResponse:
        data = self.http.build_data(
            method="getTransaction", params=[signature]
        )
        res = self.http.send(data)
        return res
