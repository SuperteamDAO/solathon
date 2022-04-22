from __future__ import annotations

import sys
import asyncio
import base64
import httpx
from typing import Any


from .. import __version__
from ..publickey import PublicKey
from ..core.types import RPCResponse

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

    def send(self, data: dict[str, Any]) -> RPCResponse:
        res = self.client.post(
                url=self.endpoint, headers=self.headers, json=data)
        return res.json()

    def build_data(self, method: str, params: list[Any]) -> dict[str, Any]:
        self.request_id += 1
        params: list[Any] = [
            str(i) if isinstance(i, PublicKey) else i for i in params
            ]

        if isinstance(params[0], bytes):
            params[0] = base64.b64encode(params[0]).decode("utf-8")

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
        

    async def send(self, data: dict[str, Any]) -> RPCResponse:
        res = await self.client.post(
                url=self.endpoint, headers=self.headers, json=data)
        return res.json()

    def build_data(self, method: str, params: list[Any]) -> dict[str, Any]:
        self.request_id += 1
        params: list[Any] = [
            str(i) if isinstance(i, PublicKey) else i for i in params
            ]

        if isinstance(params[0], bytes):
            params[0] = base64.b64encode(params[0]).decode("utf-8")

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
