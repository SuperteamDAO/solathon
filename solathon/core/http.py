from typing import Any, Union
import base64
import httpx
import asyncio

from .. import __version__
from ..publickey import PublicKey
from .types import RPCResponse

# Add this import for Commitment type
from solana.commitment import Commitment
from solana.utils import validate_commitment

class HTTPClient:
    """HTTP Client to interact with Solana JSON RPC"""

    def __init__(self, endpoint: str):
        self.endpoint = endpoint
        version = sys.version_info
        self.headers = {
            "Content-Type": "application/json",
            "User-Agent": (
                "Solathon (https://github.com/GitBolt/solathon "
                f"{__version__}) Python{version[0]} {version[1]}"
            ),
        }
        self.request_id = 0
        self.client = httpx.Client()

    def send(self, data: dict[str, Any], commitment: Union[None, Commitment] = None) -> RPCResponse:
        if commitment:
            data["params"].append({"commitment": validate_commitment(commitment)})

        res = self.client.post(url=self.endpoint, headers=self.headers, json=data)
        return res.json()

    def build_data(
        self, method: str, params: list[Any], commitment: Union[None, Commitment] = None
    ) -> dict[str, Any]:
        self.request_id += 1
        params: list[Any] = [
            str(i) if isinstance(i, PublicKey) else i for i in params
        ]

        if isinstance(params[0], bytes):
            params[0] = base64.b64encode(params[0]).decode("utf-8")

        # Include commitment in the params
        if commitment:
            params.append({"commitment": validate_commitment(commitment)})

        return {
            "jsonrpc": "2.0",
            "id": self.request_id,
            "method": method,
            "params": None if params[0] is None else params,
        }

    def refresh(self) -> None:
        self.client.close()
        self.request_id = 0
        self.client = httpx.Client()


class AsyncHTTPClient:
    """Asynchronous HTTP Client to interact with Solana JSON RPC"""

    def __init__(self, endpoint: str):
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
        self.endpoint = endpoint
        version = sys.version_info
        self.headers = {
            "Content-Type": "application/json",
            "User-Agent": (
                "Solathon (https://github.com/GitBolt/solathon "
                f"{__version__}) Python{version[0]} {version[1]}"
            ),
        }
        self.request_id = 0
        self.client = httpx.AsyncClient()

    async def send(self, data: dict[str, Any], commitment: Union[None, Commitment] = None) -> RPCResponse:
        if commitment:
            data["params"].append({"commitment": validate_commitment(commitment)})

        res = await self.client.post(url=self.endpoint, headers=self.headers, json=data)
        return res.json()

    def build_data(
        self, method: str, params: list[Any], commitment: Union[None, Commitment] = None
    ) -> dict[str, Any]:
        self.request_id += 1
        params: list[Any] = [
            str(i) if isinstance(i, PublicKey) else i for i in params
        ]

        if isinstance(params[0], bytes):
            params[0] = base64.b64encode(params[0]).decode("utf-8")

        # Include commitment in the params
        if commitment:
            params.append({"commitment": validate_commitment(commitment)})

        return {
            "jsonrpc": "2.0",
            "id": self.request_id,
            "method": method,
            "params": None if params[0] is None else params,
        }

    async def refresh(self) -> None:
        await self.client.aclose()
        self.request_id = 0
        self.client = httpx.AsyncClient()
