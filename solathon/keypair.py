from __future__ import annotations

import base58
from .publickey import PublicKey
from nacl.signing import SigningKey, SignedMessage
from nacl.public import PrivateKey as NaclPrivateKey


class PrivateKey(PublicKey):
    LENGTH = 64


class Keypair:

    def __init__(self, value: NaclPrivateKey | None = None) -> None:
        if value is None:
            self.key_pair = NaclPrivateKey.generate()
        elif isinstance(value, NaclPrivateKey):
            self.key_pair = value
        else:
            raise ValueError(
                "Keypair initialization value must be a "
                "nacl.public.PrivateKey object. To initialize with "
                "private key string, use 'from_private_key' method"
            )
        verify_key: bytes = bytes(
                            SigningKey(bytes(self.key_pair)).verify_key
                            )
        self.public_key = PublicKey(verify_key)
        self.private_key = PrivateKey(
            bytes(self.key_pair) + bytes(self.public_key)
        )

    def sign(self, message: str | bytes) -> SignedMessage:
        if isinstance(message, str):
            signing_key = SigningKey(bytes(self.key_pair))
            return signing_key.sign(bytes(message, encoding="utf-8"))

        if isinstance(message, bytes):
            signing_key = SigningKey(bytes(self.key_pair))
            return signing_key.sign(message)

        raise ValueError(
            "Message argument must be either string or bytes"
        )

    @classmethod
    def from_private_key(cls, private_key: str | bytes) -> Keypair:
        private_key = base58.b58decode(private_key)
        seed = private_key[:32]
        return cls(NaclPrivateKey(seed))
