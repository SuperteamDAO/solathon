from typing import Any
from solathon import PublicKey
from nacl.signing import VerifyKey
from solathon.core.types import RPCResponse


def lamport_to_sol(lamports: int) -> int:
    return int(lamports / 1000000000)


def sol_to_lamport(sols: int) -> int:
    return int(sols * 1000000000)


def verify_signature(public_key: PublicKey | str, signature: list, message: bytes | str) -> bool:
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
