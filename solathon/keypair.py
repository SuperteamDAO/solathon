from typing import Optional, Union
from nacl.public import PrivateKey as NaclPrivateKey
from nacl.signing import SigningKey, SignedMessage, VerifyKey
from .publickey import PublicKey


class PrivateKey(PublicKey):
    LENGTH = 64

class Keypair:

    def __init__(self, value: Optional[NaclPrivateKey | PublicKey] = None):
        if value is None:
            self.key_pair = NaclPrivateKey.generate()
        elif isinstance(value, NaclPrivateKey):
            self.key_pair = value
        else:
            raise ValueError(
                "Keypair must be initialised with either "
                "nacl.public.PrivateKey or solathon.PublicKey object"
            )
        verify_key = SigningKey(bytes(self.key_pair)).verify_key
        self._public_key = PublicKey(verify_key)
        self._private_key = PrivateKey(
            bytes(self.key_pair) + bytes(self._public_key)
        )


    def sign(self, message: bytes | str) -> SignedMessage:
        if isinstance(message, str):
            signing_key = SigningKey(bytes(self.key_pair))
            return signing_key.sign(bytes(message, encoding="utf-8"))

        if isinstance(message, bytes):
            signing_key = SigningKey(bytes(self.key_pair))
            return signing_key.sign(message)

        raise ValueError(
            "Message argument must be either string or bytes"
        )

    @property
    def public_key(self) -> PublicKey:
        return self._public_key

    @property
    def private_key(self) -> PrivateKey:
        return self._private_key

    @classmethod
    def from_private_key(cls, private_key: bytes):
        seed = private_key[:32]
        return cls(NaclPrivateKey(seed))