from typing import TypedDict, Literal, Any


class RPCError(TypedDict):
    status_code: int
    message: str


class RPCResponse(TypedDict):
    jsonrpc: Literal["2.0"]
    id: int
    result: Any
    error: RPCError

Commitment = Literal["processed", "confirmed", "finalized", "recent", "single", "singleGossip", "root", "max"]