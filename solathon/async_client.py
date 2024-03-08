from __future__ import annotations

from typing import Any, List, Text, Union
from .publickey import PublicKey
from .core.http import AsyncHTTPClient
from .core.types import RPCResponse
from .transaction import Transaction

ENDPOINTS = (
    "https://api.mainnet-beta.solana.com",
    "https://api.devnet.solana.com",
    "https://api.testnet.solana.com",
)


class AsyncClient:
    def __init__(self, endpoint: Text, local: bool = False):
        """
        Initializes an AsyncClient object.

        Args:
        - endpoint (str): The endpoint URL for the Solana RPC server.
        - local (bool): Whether to use a local development endpoint or not. Defaults to False.

        Raises:
        - ValueError: If the endpoint is not valid and not a local development endpoint.
        """
        if not local and endpoint not in ENDPOINTS:
            raise ValueError(
                "Invalid cluster RPC endpoint provided"
                " (Refer to https://docs.solana.com/cluster/rpc-endpoints)."
                " Use the argument local to use a local development endpoint."
            )
        self.http = AsyncHTTPClient(endpoint)
        self.endpoint = endpoint

    async def refresh_http(self) -> None:
        """
        Refreshes the HTTP client.
        """
        await self.http.refresh()

    async def get_account_info(self, public_key: PublicKey | Text) -> RPCResponse:
        """
        Returns the account information for a given public key.

        Args:
        - public_key (PublicKey | str): The public key of the account.

        Returns:
        - RPCResponse: The response from the Solana RPC server.
        """
        return await self.build_and_send_request_async("getAccountInfo", [public_key])

    async def get_balance(self, public_key: PublicKey | Text) -> RPCResponse:
        """
        Returns the balance of a given account.

        Args:
        - public_key (PublicKey | str): The public key of the account.

        Returns:
        - RPCResponse: The response from the Solana RPC server.
        """
        return await self.build_and_send_request_async("getBalance", [public_key])

    async def get_block(self, slot: int) -> RPCResponse:
        """
        Returns the block information for a given slot.

        Args:
        - slot (int): The slot of the block.

        Returns:
        - RPCResponse: The response from the Solana RPC server.
        """
        return await self.build_and_send_request_async("getBlock", [slot])

    async def get_block_height(self) -> RPCResponse:
        """
        Returns the current block height.

        Returns:
        - RPCResponse: The response from the Solana RPC server.
        """
        return await self.build_and_send_request_async("getBlockHeight", [None])

    async def get_block_production(self) -> RPCResponse:
        """
        Returns the block production information.

        Returns:
        - RPCResponse: The response from the Solana RPC server.
        """
        return await self.build_and_send_request_async("getBlockProduction", [None])

    async def get_block_commitment(self, block: int) -> RPCResponse:
        """
        Returns the block commitment information for a given block.

        Args:
        - block (int): The block number.

        Returns:
        - RPCResponse: The response from the Solana RPC server.
        """
        return await self.build_and_send_request_async("getBlockCommitment", [block])

    async def get_blocks(
        self, start_slot: int, end_slot: int | None = None
    ) -> RPCResponse:
        """
        Returns the block information for a range of slots.

        Args:
        - start_slot (int): The starting slot.
        - end_slot (int | None): The ending slot. Defaults to None.

        Returns:
        - RPCResponse: The response from the Solana RPC server.
        """
        params = [start_slot]
        if end_slot:
            params.append(end_slot)

        return await self.build_and_send_request_async("getBlocks", params)

    async def get_blocks_with_limit(self, start_slot: int, limit: int) -> RPCResponse:
        """
        Returns the block information for a range of slots with a limit.

        Args:
        - start_slot (int): The starting slot.
        - limit (int): The maximum number of blocks to return.

        Returns:
        - RPCResponse: The response from the Solana RPC server.
        """
        return await self.build_and_send_request_async(
            "getBlocksWithLimit", [start_slot, limit]
        )

    async def get_block_time(self, block: int) -> RPCResponse:
        """
        Returns the block time for a given block.

        Args:
        - block (int): The block number.

        Returns:
        - RPCResponse: The response from the Solana RPC server.
        """
        return await self.build_and_send_request_async("getBlockTime", [block])

    async def get_cluster_nodes(self) -> RPCResponse:
        """
        Returns the cluster nodes information.

        Returns:
        - RPCResponse: The response from the Solana RPC server.
        """
        return await self.build_and_send_request_async("getClusterNodes", [None])

    async def get_epoch_info(self) -> RPCResponse:
        """
        Returns the epoch information.

        Returns:
        - RPCResponse: The response from the Solana RPC server.
        """
        return await self.build_and_send_request_async("getEpochInfo", [None])

    async def get_epoch_schedule(self) -> RPCResponse:
        """
        Returns the epoch schedule information.

        Returns:
        - RPCResponse: The response from the Solana RPC server.
        """
        return await self.build_and_send_request_async("getEpochSchedule", [None])

    async def get_fee_for_message(self, message: Text) -> RPCResponse:
        """
        Returns the fee for a given message.

        Args:
        - message (str): The message.

        Returns:
        - RPCResponse: The response from the Solana RPC server.
        """
        return await self.build_and_send_request_async("getFeeForMessage", [message])

    # Going to be deprecated
    async def get_fees(self) -> RPCResponse:
        """
        Returns the fees information.

        Returns:
        - RPCResponse: The response from the Solana RPC server.
        """
        return await self.build_and_send_request_async("getFees", [None])

    async def get_first_available_block(self) -> RPCResponse:
        """
        Returns the first available block.

        Returns:
        - RPCResponse: The response from the Solana RPC server.
        """
        return await self.build_and_send_request_async("getFirstAvailableBlock", [None])

    async def get_genesis_hash(self) -> RPCResponse:
        """
        Returns the genesis hash.

        Returns:
        - RPCResponse: The response from the Solana RPC server.
        """
        return await self.build_and_send_request_async("getGenesisHash", [None])

    async def get_health(self) -> RPCResponse:
        """
        Returns the health information.

        Returns:
        - RPCResponse: The response from the Solana RPC server.
        """
        return await self.build_and_send_request_async("getHealth", [None])

    async def get_identity(self) -> RPCResponse:
        """
        Returns the identity information.

        Returns:
        - RPCResponse: The response from the Solana RPC server.
        """
        return await self.build_and_send_request_async("getIdentity", [None])

    async def get_inflation_governor(self) -> RPCResponse:
        """
        Returns the inflation governor information.

        Returns:
        - RPCResponse: The response from the Solana RPC server.
        """
        return await self.build_and_send_request_async("getInflationGovernor", [None])

    async def get_inflation_rate(self) -> RPCResponse:
        """
        Returns the inflation rate.

        Returns:
        - RPCResponse: The response from the Solana RPC server.
        """
        return await self.build_and_send_request_async("getInflationRate", [None])

    async def get_inflation_reward(self, addresses: List[Text]) -> RPCResponse:
        """
        Get the inflation reward for a list of addresses.

        Args:
            addresses (list[Text]): A list of addresses to get the inflation reward for.

        Returns:
            RPCResponse: The response from the RPC server.
        """
        return await self.build_and_send_request_async("getInflationReward", [addresses])

    async def get_largest_accounts(self) -> RPCResponse:
        """
        Returns the largest accounts on the Solana blockchain.

        :return: An RPCResponse object containing the response from the Solana node.
        """
        return await self.build_and_send_request_async("getLargestAccounts", [None])

    async def get_leader_schedule(self) -> RPCResponse:
        """
        Sends a request to the Solana RPC endpoint to retrieve the leader schedule.

        Returns:
            RPCResponse: The response from the RPC endpoint.
        """
        return await self.build_and_send_request_async("getLeaderSchedule", [None])

    async def get_max_retransmit_slot(self) -> RPCResponse:
        """
        Sends a request to get the maximum retransmit slot from the server.

        Returns:
            An RPCResponse object containing the server's response.
        """
        return await self.build_and_send_request_async("getMaxRetransmitSlot", [None])

    async def get_max_shred_insert_slot(self) -> RPCResponse:
        """
        Sends a request to get the maximum shred insert slot from the Solana RPC endpoint.

        Returns:
            RPCResponse: The response from the RPC endpoint.
        """
        return await self.build_and_send_request_async("getMaxShredInsertSlot", [None])

    async def get_minimum_balance_for_rent_exemption(
        self, acct_length: int
    ) -> RPCResponse:
        """
        Returns the minimum balance needed to create an account with the given data size.

        :param acct_length: The length of the account data.
        :type acct_length: int
        :return: The minimum balance needed to create an account with the given data size.
        :rtype: RPCResponse
        """
        return await self.build_and_send_request_async(
            "getMinimumBalanceForRentExemption", [acct_length]
        )

    async def get_multiple_accounts(self, pubkeys: List) -> RPCResponse:
        """
        Sends a request to the Solana RPC endpoint to retrieve multiple accounts
        associated with the given public keys.

        Args:
            pubkeys (list): A list of public keys associated with the accounts to retrieve.

        Returns:
            RPCResponse: The response from the Solana RPC endpoint.
        """
        return await self.build_and_send_request_async("getMultipleAccounts", [pubkeys])

    async def get_program_accounts(self, public_key: PublicKey) -> RPCResponse:
        """
        Returns accounts associated with a given program.

        Args:
            public_key (PublicKey): The public key of the program.

        Returns:
            RPCResponse: The response from the RPC server.
        """
        return await self.build_and_send_request_async("getProgramAccounts", [public_key])

    # Will switch to getFeeForMessage (latest)
    async def get_recent_blockhash(self) -> RPCResponse:
        """
        Returns a recent blockhash from the ledger.

        :return: RPCResponse object containing the recent blockhash.
        """
        return await self.build_and_send_request_async("getRecentBlockhash", [None])

    async def get_recent_performance_samples(self) -> RPCResponse:
        """
        Sends a request to the server to get recent performance samples.

        Returns:
            RPCResponse: The response from the server.
        """
        return await self.build_and_send_request_async("getRecentPerformanceSamples", [None])

    async def get_signatures_for_address(self, acct_address: Text) -> RPCResponse:
        """
        Returns signatures for a given account address.

        :param acct_address: The account address to get signatures for.
        :type acct_address: str
        :return: The RPC response containing the signatures for the account address.
        :rtype: RPCResponse
        """
        return await self.build_and_send_request_async(
            "getSignaturesForAddress", [acct_address]
        )

    async def get_signature_statuses(self, transaction_sigs: list[Text]) -> RPCResponse:
        """
        Returns the current status of a list of signatures.

        Args:
            transaction_sigs (list[str]): List of transaction signatures to check status for.

        Returns:
            RPCResponse: Response object containing the status of the signatures.
        """
        return await self.build_and_send_request_async(
            "getSignatureStatuses", [transaction_sigs]
        )

    async def get_slot(self) -> RPCResponse:
        """
        Sends a request to the Solana RPC endpoint to retrieve the current slot.

        Returns:
            RPCResponse: The response from the RPC endpoint.
        """
        return await self.build_and_send_request_async("getSlot", [None])

    async def get_supply(self) -> RPCResponse:
        """
        Sends a request to the Solana blockchain to retrieve the current supply.

        Returns:
            RPCResponse: The response from the Solana blockchain.
        """
        return await self.build_and_send_request_async("getSupply", [None])

    async def get_token_accounts_by_owner(
        self, public_key: Union[Text, PublicKey], **kwargs
    ) -> RPCResponse:
        """
        Returns token accounts owned by a particular address.

        Args:
            public_key (Union[Text, PublicKey]): The public key of the address to query.
            **kwargs: Additional keyword arguments.
                mint_id (Optional[Text]): The mint ID of the token to query.
                program_id (Optional[Text]): The program ID of the token to query.
                encoding (Optional[Text]): The encoding format of the response. Defaults to "jsonParsed".

        Returns:
            RPCResponse: The response from the RPC server.
        """
        if "mint_id" not in kwargs and "program_id" not in kwargs:
            raise ValueError(
                "You must pass either mint_id or program_id keyword argument"
            )

        mint_id = kwargs.get("mint_id")
        program_id = kwargs.get("program_id")
        # Who doesn't like JSON?
        encoding = kwargs.get("encoding", "jsonParsed")
        return await self.build_and_send_request_async(
            "getTokenAccountsByOwner",
            [
                str(public_key),
                {"mint": mint_id} if mint_id else {"programId": program_id},
                {"encoding": encoding},
            ],
        )

    async def get_token_account_balance(
        self, token_account: Text | PublicKey, commitment: Optional[Commitment]=None,
    ) -> RPCResponse:
        """
        Returns the token account balance for the specified owner.

        Args:
            token_account (str | PublicKey): The token account pubkey.
            commitment (Commitment, optional): The level of commitment desired when querying state.

        Returns:
            RPCResponse: The response from the RPC endpoint.
        """

        commitment = validate_commitment(commitment) if commitment else None
        response = self.build_and_send_request(
            "getTokenAccountBalance",
            [
                str(token_account),
            ],
        )
        if self.clean_response:
            return response['value']
        return response


    async def get_transaction(self, signature: Text) -> RPCResponse:
        """
        Sends a request to the Solana RPC endpoint to retrieve a transaction by its signature.

        Args:
            signature (Text): The signature of the transaction to retrieve.

        Returns:
            RPCResponse: The response from the Solana RPC endpoint.
        """
        return await self.build_and_send_request_async("getTransaction", [signature])

    # Non "get" methods
    async def request_airdrop(
        self, public_key: Union[PublicKey, Text], lamports: int
    ) -> RPCResponse:
        """
        Requests an airdrop of the specified number of lamports to the specified public key.

        Args:
            public_key (PublicKey | Text): The public key to receive the airdrop.
            lamports (int): The number of lamports to request in the airdrop.

        Returns:
            RPCResponse: The response from the Solana JSON RPC API.
        """
        return await self.build_and_send_request_async(
            "requestAirdrop", [public_key, lamports]
        )

    async def send_transaction(self, transaction: Transaction) -> RPCResponse:
        """
        Sends a transaction to the Solana network.

        Args:
            transaction (Transaction): The transaction to send.

        Returns:
            RPCResponse: The response from the Solana network.
        """
        if not transaction.recent_blockhash:
            transaction.recent_blockhash = (await self.get_recent_blockhash())[
                "result"
            ].blockhash

        transaction.sign()

        return await self.build_and_send_request_async(
            "sendTransaction", [transaction.serialize(), {"encoding": "base64"}]
        )

    async def build_and_send_request_async(
        self, method: Text, params: List[Any]
    ) -> RPCResponse:
        """
        Builds and sends an RPC request to the server.

        Args:
            method (Text): The RPC method to call.
            params (List[Any]): The parameters to pass to the RPC method.

        Returns:
            RPCResponse: The response from the server.
        """
        data: dict[Text, Any] = self.http.build_data(method=method, params=params)
        res: RPCResponse = await self.http.send(data)
        return res
