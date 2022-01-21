from typing import Optional
from .publickey import PublicKey
from .core.http import HTTPClient
from .core.types import RPCResponse
from .transaction import Transaction

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

    def get_account_info(self, public_key: PublicKey | str) -> RPCResponse:
        data = self.http.build_data(
            method="getAccountInfo", params=[public_key]
        )
        res = self.http.send(data)
        return res

    def get_balance(self, public_key: PublicKey | str) -> RPCResponse:
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

    # Will switch to getFeeForMessage (latest)
    def get_recent_blockhash(self) -> RPCResponse:
        data = self.http.build_data(
            method="getRecentBlockhash", params=[None]
        )
        res = self.http.send(data)
        return res

    def get_token_accounts_by_owner(self, public_key: str | PublicKey,
                                    **kwargs) -> RPCResponse:
        if "mint_id" not in kwargs and "program_id" not in kwargs:
            raise ValueError("You must pass either mint_id or program_id keyword argument")

        mint_id = kwargs.get("mint_id")
        program_id = kwargs.get("program_id")
        encoding = kwargs.get("encoding", "jsonParsed") # Who doesn't like JSON?

        data = self.http.build_data(
                method="getTokenAccountsByOwner", 
                params=[
                    str(public_key),
                    {"mint": mint_id} if mint_id else {"programId": program_id},
                    {"encoding": encoding}
                ]
        )
        res = self.http.send(data)
        return res

    def send_transaction(self, transaction: Transaction, recent_blockhash: Optional[str] = None,) -> RPCResponse:

        if recent_blockhash is None:
            blockhash_resp = self.get_recent_blockhash()
            recent_blockhash = blockhash_resp["result"]["value"]["blockhash"]

        transaction.recent_blockhash = recent_blockhash
        transaction.sign()

        data = self.http.build_data(
            method="sendTransaction",
            params=[transaction.serialize(), {"encoding": "base64"}]
        )
        res = self.http.send(data)
        return res

