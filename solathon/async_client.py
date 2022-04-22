from __future__ import annotations

from typing import Any
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
    def __init__(self, endpoint: str, local: bool = False):
        if not local and endpoint not in ENDPOINTS:
            raise ValueError(
                "Invalid cluster RPC endpoint provided"
                " (Refer to https://docs.solana.com/cluster/rpc-endpoints)."
                " Use the argument local to use a local development endpoint."
            )
        self.http = AsyncHTTPClient(endpoint)
        self.endpoint = endpoint

    async def refresh_http(self) -> None:
        await self.http.refresh()

    async def get_account_info(self, public_key: PublicKey | str) -> RPCResponse:
        data: dict[str, Any] = self.http.build_data(
            method="getAccountInfo", params=[public_key]
        )
        res: RPCResponse = await self.http.send(data)
        return res

    async def get_balance(self, public_key: PublicKey | str) -> RPCResponse:
        data: dict[str, Any] = self.http.build_data(
            method="getBalance", params=[public_key]
        )
        res: RPCResponse = await self.http.send(data)
        return res

    async def get_block(self, slot: int) -> RPCResponse:
        data: dict[str, Any] = self.http.build_data(
            method="getBlock", params=[slot]
        )
        res: RPCResponse = await self.http.send(data)
        return res

    async def get_block_height(self) -> RPCResponse:
        data: dict[str, Any] = self.http.build_data(
            method="getBlockHeight", params=[None]
        )
        res: RPCResponse = await self.http.send(data)
        return res

    async def get_block_production(self) -> RPCResponse:
        data: dict[str, Any] = self.http.build_data(
            method="getBlockProduction", params=[None]
        )
        res: RPCResponse = await self.http.send(data)
        return res

    async def get_block_commitment(self, block: int) -> RPCResponse:
        data: dict[str, Any] = self.http.build_data(
            method="getBlockCommitment", params=[block]
        )
        res: RPCResponse = await self.http.send(data)
        return res

    async def get_blocks(self, start_slot: int, end_slot: int | None = None
                   ) -> RPCResponse:
        params = [start_slot]
        if end_slot:
            params.append(end_slot)

        data: dict[str, Any] = self.http.build_data(
            method="getBlocks", params=params
        )
        res: RPCResponse = await self.http.send(data)
        return res

    async def get_blocks_with_limit(self, start_slot: int, limit: int
                              ) -> RPCResponse:

        data: dict[str, Any] = self.http.build_data(
            method="getBlocksWithLimit", params=[start_slot, limit]
        )
        res: RPCResponse = await self.http.send(data)
        return res

    async def get_block_time(self, block: int) -> RPCResponse:

        data: dict[str, Any] = self.http.build_data(
            method="getBlockTime", params=[block]
        )
        res: RPCResponse = await self.http.send(data)
        return res

    async def get_cluster_nodes(self) -> RPCResponse:

        data: dict[str, Any] = self.http.build_data(
            method="getClusterNodes", params=[None]
        )
        res: RPCResponse = await self.http.send(data)
        return res

    async def get_epoch_info(self) -> RPCResponse:

        data: dict[str, Any] = self.http.build_data(
            method="getEpochInfo", params=[None]
        )
        res: RPCResponse = await self.http.send(data)
        return res

    async def get_epoch_schedule(self) -> RPCResponse:

        data: dict[str, Any] = self.http.build_data(
            method="getEpochSchedule", params=[None]
        )
        res: RPCResponse = await self.http.send(data)
        return res

    async def get_fee_for_message(self, message: str) -> RPCResponse:

        data: dict[str, Any] = self.http.build_data(
            method="getFeeForMessage", params=[message]
        )
        res: RPCResponse = await self.http.send(data)
        return res

    # Going to be deprecated
    async def get_fees(self) -> RPCResponse:

        data: dict[str, Any] = self.http.build_data(
            method="getFees", params=[None]
        )
        res: RPCResponse = await self.http.send(data)
        return res

    async def get_first_available_block(self) -> RPCResponse:

        data: dict[str, Any] = self.http.build_data(
            method="getFirstAvailableBlock", params=[None]
        )
        res: RPCResponse = await self.http.send(data)
        return res

    async def get_genesis_hash(self) -> RPCResponse:
        data: dict[str, Any] = self.http.build_data(
            method="getGenesisHash", params=[None]
        )
        res: RPCResponse = await self.http.send(data)
        return res

    async def get_health(self) -> RPCResponse:
        data: dict[str, Any] = self.http.build_data(
            method="getHealth", params=[None]
        )
        res: RPCResponse = await self.http.send(data)
        return res

    async def get_identity(self) -> RPCResponse:
        data: dict[str, Any] = self.http.build_data(
            method="getIdentity", params=[None]
        )
        res: RPCResponse = await self.http.send(data)
        return res

    async def get_inflation_governor(self) -> RPCResponse:
        data: dict[str, Any] = self.http.build_data(
            method="getInflationGovernor", params=[None]
        )
        res: RPCResponse = await self.http.send(data)
        return res
    
    async def get_inflation_rate(self) -> RPCResponse:
        data: dict[str, Any] = self.http.build_data(
            method="getInflationRate", params=[None]
        )
        res: RPCResponse = await self.http.send(data)
        return res

    async def get_inflation_reward(self , addresses: list[str]) -> RPCResponse:
        data: dict[str, Any] = self.http.build_data(
            method="getInflationReward", params=[addresses]
        )
        res: RPCResponse = await self.http.send(data)
        return res

    async def get_largest_accounts(self) -> RPCResponse:
        data: dict[str, Any] = self.http.build_data(
            method="getLargestAccounts", params=[None]
        )
        res: RPCResponse = await self.http.send(data)
        return res

    async def get_leader_schedule(self) -> RPCResponse:
        data: dict[str, Any] = self.http.build_data(
            method="getLeaderSchedule", params=[None]
        )
        res: RPCResponse = await self.http.send(data)
        return res

    async def get_max_retransmit_slot(self) -> RPCResponse:
        data: dict[str, Any] = self.http.build_data(
            method="getMaxRetransmitSlot", params=[None]
        )
        res: RPCResponse = await self.http.send(data)
        return res
    
    async def get_max_shred_insert_slot(self) -> RPCResponse:
        data: dict[str, Any] = self.http.build_data(
            method="getMaxShredInsertSlot", params=[None]
        )
        res: RPCResponse = await self.http.send(data)
        return res
   
    async def get_minimum_balance_for_rent_exemption(self, acct_length: int) -> RPCResponse:
        data: dict[str, Any] = self.http.build_data(
            method="getMinimumBalanceForRentExemption", params=[acct_length]
        )
        res: RPCResponse = await self.http.send(data)
        return res

    async def get_multiple_accounts(self, pubkeys: list) -> RPCResponse:
        data: dict[str, Any] = self.http.build_data(
            method="getMultipleAccounts", params=[pubkeys]
        )
        res: RPCResponse = await self.http.send(data)
        return res
    
    async def get_program_accounts(self, public_key: PublicKey) -> RPCResponse:
        data: dict[str, Any] = self.http.build_data(
            method="getProgramAccounts", params=[public_key]
        )
        res: RPCResponse = await self.http.send(data)
        return res

    # Will switch to getFeeForMessage (latest)
    async def get_recent_blockhash(self) -> RPCResponse:
        data: dict[str, Any] = self.http.build_data(
            method="getRecentBlockhash", params=[None]
        )
        res: RPCResponse = await self.http.send(data)
        return res
    
    async def get_recent_performance_samples(self) -> RPCResponse:
        data: dict[str, Any] = self.http.build_data(
            method="getRecentPerformanceSamples", params=[None]
        )
        res: RPCResponse = await self.http.send(data)
        return res

    async def get_signatures_for_address(self, acct_address: str) -> RPCResponse:
        data: dict[str, Any] = self.http.build_data(
            method="getSignaturesForAddress", params=[acct_address]
        )
        res: RPCResponse = await self.http.send(data)
        return res
        
    async def get_signature_statuses(self, transaction_sigs: list[str]) -> RPCResponse:
        data: dict[str, Any] = self.http.build_data(
            method="getSignatureStatuses", params=[transaction_sigs]
        )
        res: RPCResponse = await self.http.send(data)
        return res 
        
    async def get_slot(self) -> RPCResponse:
        data: dict[str, Any] = self.http.build_data(
            method="getSlot", params=[None]
        )
        res: RPCResponse = await self.http.send(data)
        return res

    async def get_supply(self) -> RPCResponse:
        data: dict[str, Any] = self.http.build_data(
            method="getSupply", params=[None]
        )
        res: RPCResponse = await self.http.send(data)
        return res

    async def get_token_accounts_by_owner(self, public_key: str | PublicKey,
                                    **kwargs) -> RPCResponse:
        if "mint_id" not in kwargs and "program_id" not in kwargs:
            raise ValueError(
                "You must pass either mint_id or program_id keyword argument")

        mint_id = kwargs.get("mint_id")
        program_id = kwargs.get("program_id")
        # Who doesn't like JSON?
        encoding = kwargs.get("encoding", "jsonParsed")

        data: dict[str, Any] = self.http.build_data(
            method="getTokenAccountsByOwner",
            params=[
                str(public_key),
                {"mint": mint_id} if mint_id else {"programId": program_id},
                {"encoding": encoding}
            ]
        )
        res: RPCResponse = await self.http.send(data)
        return res

    async def get_transaction(self, signature: str) -> RPCResponse:
        data: dict[str, Any] = self.http.build_data(
            method="getTransaction", params=[signature]
        )
        res: RPCResponse = await self.http.send(data)
        return res

    # Non "get" methods
    async def request_airdrop(self, public_key: PublicKey | str, lamports: int
                        ) -> RPCResponse:

        data: dict[str, Any] = self.http.build_data(
            method="requestAirdrop",
            params=[public_key, lamports]
        )
        res: RPCResponse = await self.http.send(data)
        return res

    async def send_transaction(self, transaction: Transaction) -> RPCResponse:

        if transaction.recent_blockhash is None:
            blockhash_resp = self.get_recent_blockhash()
            recent_blockhash = blockhash_resp["result"]["value"]["blockhash"]

        transaction.recent_blockhash = recent_blockhash
        transaction.sign()

        data: dict[str, Any] = self.http.build_data(
            method="sendTransaction",
            params=[transaction.serialize(), {"encoding": "base64"}]
        )
        res: RPCResponse = await self.http.send(data)
        return res