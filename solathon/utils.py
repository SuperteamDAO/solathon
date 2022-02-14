from typing import Any
from solathon import PublicKey
from nacl.signing import VerifyKey
from solathon.core.types import RPCResponse


LAMPORT_PER_SOL: int = 1000000000
SOL_PER_LAMPORT: float = 1 / LAMPORT_PER_SOL
SOL_FLOATING_PRECISION: int = 9


def truncate_float(number: int, length: int) -> float:
    number = number * pow(10, length)
    number = int(number)
    number = float(number)
    number /= pow(10, length)
    return number


def lamport_to_sol(lamports: int) -> float:
    return truncate_float(lamports * SOL_PER_LAMPORT, SOL_FLOATING_PRECISION)


def sol_to_lamport(sol: float) -> int:
    return int(sol * LAMPORT_PER_SOL)


def verify_signature(
    public_key: PublicKey | str,
    signature: list,
    message: bytes | str
    ) -> None:
    if isinstance(public_key, str):
        public_key = PublicKey(public_key)

    if isinstance(message, str):
        message = bytes(message, encoding="utf8")

    if not message:
        message = public_key.base58_encode()

    bytes_pk = bytes(public_key)
    vk = VerifyKey(bytes_pk)
    vk.verify(message, bytes(signature))


def clean_response(response: RPCResponse) -> dict[str, Any]:
    if "error" in response.keys():
        return response["error"]

    result = response["result"]

    if isinstance(result, dict):
        result.pop("context", None)
        result.pop("id", None)
        if "value" in result.keys():
            return result["value"]

    return result
