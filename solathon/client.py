from __future__ import annotations

from typing import Any, List, Text
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
    def __init__(self, endpoint: Text, local: bool = False):
        """
        Initializes a new instance of the Client class.

        Args:
            endpoint (str): The endpoint to connect to.
            local (bool, optional): Whether to use a local development endpoint. Defaults to False.

        Raises:
            ValueError: If the endpoint is not valid and local is False.
        """
        if not local and endpoint not in ENDPOINTS:
            raise ValueError(
                "Invalid cluster RPC endpoint provided"
                " (Refer to https://docs.solana.com/cluster/rpc-endpoints)."
                " Use the argument local to use a local development endpoint."
            )
        self.http = HTTPClient(endpoint)
        self.endpoint = endpoint

    def refresh_http(self) -> None:
        """
        Refreshes the HTTP client.
        """
        self.http.refresh()

    def get_account_info(self, public_key: PublicKey | Text) -> RPCResponse:
        """
        Returns all the account info for the specified public key.

        Args:
            public_key (PublicKey | str): The public key of the account.

        Returns:
            RPCResponse: The response from the RPC endpoint.
        """
        return self.build_and_send_request("getAccountInfo", [public_key])

    def get_balance(self, public_key: PublicKey | Text) -> RPCResponse:
        """
        Returns the balance of the specified public key.

        Args:
            public_key (PublicKey | Text): The public key of the account.

        Returns:
            RPCResponse: The response from the RPC endpoint.
        """
        return self.build_and_send_request("getBalance", [public_key])

    def get_block(self, slot: int) -> RPCResponse:
        """
        Returns the block at the specified slot.

        Args:
            slot (int): The slot of the block.

        Returns:
            RPCResponse: The response from the RPC endpoint.
        """
        return self.build_and_send_request("getBlock", [slot])

    def get_block_height(self) -> RPCResponse:
        """
        Returns the current block height.

        Returns:
            RPCResponse: The response from the RPC endpoint.
        """
        return self.build_and_send_request("getBlockHeight", [None])

    def get_block_production(self) -> RPCResponse:
        """
        Returns the block production information.

        Returns:
            RPCResponse: The response from the RPC endpoint.
        """
        return self.build_and_send_request("getBlockProduction", [None])

    def get_block_commitment(self, block: int) -> RPCResponse:
        """
        Returns the block commitment information for the specified block.

        Args:
            block (int): The block number.

        Returns:
            RPCResponse: The response from the RPC endpoint.
        """
        return self.build_and_send_request("getBlockCommitment", [block])

    def get_blocks(self, start_slot: int, end_slot: int | None = None) -> RPCResponse:
        """
        Returns the blocks in the specified range.

        Args:
            start_slot (int): The start slot.
            end_slot (int | None, optional): The end slot. Defaults to None.

        Returns:
            RPCResponse: The response from the RPC endpoint.
        """
        params = [start_slot]
        if end_slot:
            params.append(end_slot)

        return self.build_and_send_request("getBlocks", params)

    def get_blocks_with_limit(self, start_slot: int, limit: int) -> RPCResponse:
        """
        Returns the blocks in the specified range with a limit.

        Args:
            start_slot (int): The start slot.
            limit (int): The limit.

        Returns:
            RPCResponse: The response from the RPC endpoint.
        """
        return self.build_and_send_request("getBlocksWithLimit", [start_slot, limit])

    def get_block_time(self, block: int) -> RPCResponse:
        """
        Returns the block time for the specified block.

        Args:
            block (int): The block number.

        Returns:
            RPCResponse: The response from the RPC endpoint.
        """
        return self.build_and_send_request("getBlockTime", [block])

    def get_cluster_nodes(self) -> RPCResponse:
        """
        Returns the cluster nodes.

        Returns:
            RPCResponse: The response from the RPC endpoint.
        """
        return self.build_and_send_request("getClusterNodes", [None])

    def get_epoch_info(self) -> RPCResponse:
        """
        Returns the epoch information.

        Returns:
            RPCResponse: The response from the RPC endpoint.
        """
        return self.build_and_send_request("getEpochInfo", [None])

    def get_epoch_schedule(self) -> RPCResponse:
        """
        Returns the epoch schedule.

        Returns:
            RPCResponse: The response from the RPC endpoint.
        """
        return self.build_and_send_request("getEpochSchedule", [None])

    def get_fee_for_message(self, message: Text) -> RPCResponse:
        """
        Returns the fee for the specified message.

        Args:
            message (str): The message.

        Returns:
            RPCResponse: The response from the RPC endpoint.
        """
        return self.build_and_send_request("getFeeForMessage", [message])

    # Going to be deprecated
    def get_fees(self) -> RPCResponse:
        """
        Returns the fees.

        Returns:
            RPCResponse: The response from the RPC endpoint.
        """
        return self.build_and_send_request("getFees", [None])

    def get_first_available_block(self) -> RPCResponse:
        """
        Returns the first available block.

        Returns:
            RPCResponse: The response from the RPC endpoint.
        """
        return self.build_and_send_request("getFirstAvailableBlock", [None])

    def get_genesis_hash(self) -> RPCResponse:
        """
        Returns the genesis hash.

        Returns:
            RPCResponse: The response from the RPC endpoint.
        """
        return self.build_and_send_request("getGenesisHash", [None])

    def get_health(self) -> RPCResponse:
        """
        Returns the health.

        Returns:
            RPCResponse: The response from the RPC endpoint.
        """
        return self.build_and_send_request("getHealth", [None])

    def get_identity(self) -> RPCResponse:
        """
        Returns the identity.

        Returns:
            RPCResponse: The response from the RPC endpoint.
        """
        return self.build_and_send_request("getIdentity", [None])

    def get_inflation_governor(self) -> RPCResponse:
        """
        Returns the inflation governor.

        Returns:
            RPCResponse: The response from the RPC endpoint.
        """
        return self.build_and_send_request("getInflationGovernor", [None])

    def get_inflation_rate(self) -> RPCResponse:
        """
        Returns the inflation rate.

        Returns:
            RPCResponse: The response from the RPC endpoint.
        """
        return self.build_and_send_request("getInflationRate", [None])

    def get_inflation_reward(self, addresses: List[Text]) -> RPCResponse:
        """
        Returns the inflation reward for the specified addresses.

        Args:
            addresses (list[str]): The addresses.

        Returns:
            RPCResponse: The response from the RPC endpoint.
        """
        return self.build_and_send_request("getInflationReward", addresses)

    def get_largest_accounts(self) -> RPCResponse:
        """
        Returns the largest accounts.

        Returns:
            RPCResponse: The response from the RPC endpoint.
        """
        return self.build_and_send_request("getLargestAccounts", [None])

    def get_leader_schedule(self) -> RPCResponse:
        """
        Returns the leader schedule.

        Returns:
            RPCResponse: The response from the RPC endpoint.
        """
        return self.build_and_send_request("getLeaderSchedule", [None])

    def get_max_retransmit_slot(self) -> RPCResponse:
        """
        Returns the maximum retransmit slot.

        Returns:
            RPCResponse: The response from the RPC endpoint.
        """
        return self.build_and_send_request("getMaxRetransmitSlot", [None])

    def get_max_shred_insert_slot(self) -> RPCResponse:
        """
        Returns the maximum shred insert slot.

        Returns:
            RPCResponse: The response from the RPC endpoint.
        """
        return self.build_and_send_request("getMaxShredInsertSlot", [None])

    def get_minimum_balance_for_rent_exemption(self, acct_length: int) -> RPCResponse:
        """
        Returns the minimum balance for rent exemption.

        Args:
            acct_length (int): The length of the account.

        Returns:
            RPCResponse: The response from the RPC endpoint.
        """
        return self.build_and_send_request(
            "getMinimumBalanceForRentExemption", [acct_length]
        )

    def get_multiple_accounts(self, pubkeys: List) -> RPCResponse:
        """
        Returns the multiple accounts.

        Args:
            pubkeys (list): The public keys.

        Returns:
            RPCResponse: The response from the RPC endpoint.
        """
        return self.build_and_send_request("getMultipleAccounts", pubkeys)

    def get_program_accounts(self, public_key: PublicKey) -> RPCResponse:
        """
        Returns the program accounts.

        Args:
            public_key (PublicKey): The public key.

        Returns:
            RPCResponse: The response from the RPC endpoint.
        """
        return self.build_and_send_request("getProgramAccounts", [public_key])

    # Will switch to getFeeForMessage (latest)
    def get_recent_blockhash(self) -> RPCResponse:
        """
        Returns the recent blockhash.

        Returns:
            RPCResponse: The response from the RPC endpoint.
        """
        return self.build_and_send_request("getRecentBlockhash", [None])

    def get_recent_performance_samples(self) -> RPCResponse:
        """
        Returns the recent performance samples.

        Returns:
            RPCResponse: The response from the RPC endpoint.
        """
        return self.build_and_send_request("getRecentPerformanceSamples", [None])

    def get_signatures_for_address(self, acct_address: Text) -> RPCResponse:
        """
        Returns the signatures for the specified account address.

        Args:
            acct_address (str): The account address.

        Returns:
            RPCResponse: The response from the RPC endpoint.
        """
        return self.build_and_send_request("getSignaturesForAddress", [acct_address])

    def get_signature_statuses(self, transaction_sigs: List[Text]) -> RPCResponse:
        """
        Returns the signature statuses for the specified transaction signatures.

        Args:
            transaction_sigs (list[str]): The transaction signatures.

        Returns:
            RPCResponse: The response from the RPC endpoint.
        """
        return self.build_and_send_request("getSignatureStatuses", transaction_sigs)

    def get_slot(self) -> RPCResponse:
        """
        Returns the current slot.

        Returns:
            RPCResponse: The response from the RPC endpoint.
        """
        return self.build_and_send_request("getSlot", [None])

    def get_supply(self) -> RPCResponse:
        """
        Returns the supply.

        Returns:
            RPCResponse: The response from the RPC endpoint.
        """
        return self.build_and_send_request("getSupply", [None])

    def get_token_accounts_by_owner(
        self, public_key: Text | PublicKey, **kwargs
    ) -> RPCResponse:
        """
        Returns the token accounts for the specified owner.

        Args:
            public_key (str | PublicKey): The public key of the owner.
            **kwargs: Additional keyword arguments.

        Raises:
            ValueError: If neither mint_id nor program_id is passed as a keyword argument.

        Returns:
            RPCResponse: The response from the RPC endpoint.
        """
        if "mint_id" not in kwargs and "program_id" not in kwargs:
            raise ValueError(
                "You must pass either mint_id or program_id keyword argument"
            )
        mint_id = kwargs.get("mint_id")
        program_id = kwargs.get("program_id")
        # Who doesn't like JSON?
        encoding = kwargs.get("encoding", "jsonParsed")
        return self.build_and_send_request(
            "getTokenAccountsByOwner",
            [
                str(public_key),
                {"mint": mint_id} if mint_id else {"programId": program_id},
                {"encoding": encoding},
            ],
        )

    def get_transaction(self, signature: Text) -> RPCResponse:
        """
        Sends a request to the Solana RPC endpoint to retrieve a transaction by its signature.

        Args:
            signature (str): The signature of the transaction to retrieve.

        Returns:
            RPCResponse: The response from the Solana RPC endpoint.
        """
        return self.build_and_send_request("getTransaction", [signature])

    def build_and_send_request(self, method, params: List[Any]) -> RPCResponse:
        """
        Builds and sends an RPC request to the server.

        Args:
            method (str): The RPC method to call.
            params (List[Any]): The parameters to pass to the RPC method.

        Returns:
            RPCResponse: The response from the server.
        """
        data: dict[str, Any] = self.http.build_data(method=method, params=params)
        res: RPCResponse = self.http.send(data)
        return res

    # Non "get" methods
    def request_airdrop(
        self, public_key: PublicKey | Text, lamports: int
    ) -> RPCResponse:
        """
        Requests an airdrop of lamports to the specified public key.

        Args:
            public_key (PublicKey | Text): The public key of the account to receive the airdrop.
            lamports (int): The amount of lamports to request in the airdrop.

        Returns:
            RPCResponse: The response from the Solana JSON RPC API.
        """
        return self.build_and_send_request("requestAirdrop", [public_key, lamports])

    def send_transaction(self, transaction: Transaction) -> RPCResponse:
        """
        Sends a transaction to the Solana network.

        Args:
            transaction (Transaction): The transaction to send.

        Returns:
            RPCResponse: The response from the Solana network.
        """
        recent_blockhash = transaction.recent_blockhash

        if recent_blockhash is None:
            blockhash_resp = self.get_recent_blockhash()
            recent_blockhash = blockhash_resp["result"]["value"]["blockhash"]

        transaction.recent_blockhash = recent_blockhash
        transaction.sign()

        return self.build_and_send_request(
            "sendTransaction", [transaction.serialize(), {"encoding": "base64"}]
        )
