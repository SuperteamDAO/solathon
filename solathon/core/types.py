from typing import Generic, TypeVar, TypedDict, Literal, Any, Union

T = TypeVar('T')

class RPCError(TypedDict):
    status_code: int
    message: str

class Context(TypedDict):
    slot: int
    apiVersion: int

class Result(Generic[T], TypedDict):
    context: Context
    value: Union[T, None]

class RPCResponse(Generic[T], TypedDict):
    jsonrpc: Literal["2.0"]
    id: int
    result: Result[T]
    error: RPCError

class AccountInfo(TypedDict):
    lamports: int
    owner: str
    executable: bool
    rentEpoch: int

class FeeCalculator(TypedDict):
    lamportsPerSignature: int

class BlockHash(TypedDict):
    blockhash: str
    feeCalculator: FeeCalculator

Commitment = Literal["processed", "confirmed", "finalized", "recent", "single", "singleGossip", "root", "max"]