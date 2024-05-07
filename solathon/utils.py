from __future__ import annotations

from typing import Any, Union
from nacl.signing import VerifyKey
from .publickey import PublicKey
from solathon.core.types import Commitment, RPCErrorType, RPCResponse

class RPCRequestError(Exception):
    def __init__(self, message: str = "Failed to fetch data from RPC endpoint"):
        self.message = message
        super().__init__(self.message)


LAMPORTS_PER_SOL: int = 1_000_000_000
SOL_FLOATING_PRECISION: int = 9


def truncate_float(number: float, length: int) -> float:
    return float(f'{number:.{length}f}')


def validate_commitment(value: Commitment) -> Commitment:
    allowed_commitments = {"processed", "confirmed", "finalized",
                           "recent", "single", "singleGossip", "root", "max"}

    if value not in allowed_commitments:
        raise ValueError(
            f"Invalid commitment value. Allowed values are {allowed_commitments}")

    return value


def lamports_to_sol(lamports: int) -> float:
    return truncate_float(lamports / LAMPORTS_PER_SOL, SOL_FLOATING_PRECISION)


def sol_to_lamports(sol: Union[float, int]) -> int:
    return int(sol * LAMPORTS_PER_SOL)


def verify_signature(
    public_key: Union[PublicKey, str],
    signature: bytes,
    message: Union[bytes, None] = None
) -> None:
    if not message:
        message = bytes(public_key)

    if isinstance(public_key, str):
        public_key = PublicKey(public_key)

    vk = VerifyKey(bytes(public_key))
    vk.verify(message, signature)


def clean_response(response: RPCResponse) -> Union[dict[str, Any], RPCErrorType]:
    if "error" in response:
        return response["error"]

    result = response["result"]

    if isinstance(result, dict):
        result.pop("context", None)
        result.pop("id", None)
        if "value" in result:
            return result["value"]

    return result