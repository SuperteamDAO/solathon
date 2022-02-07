import base58


class PublicKey:
    LENGTH = 32

    def __init__(self, value: bytearray | bytes | int | str | list[int]):
        if isinstance(value, str):
            try:
                self.public_key = base58.b58decode(value)
            except ValueError:
                raise ValueError("Invalid public key.")
            if len(self.public_key) != self.LENGTH:
                raise ValueError("Invalid public key, the length is wrong.")
        elif isinstance(value, int):
            self.public_key = bytes([value])
        else:
            self.public_key = bytes(value)

        if len(self.public_key) > self.LENGTH:
            raise ValueError("Invalid public key, the length is wrong.")

    def __bytes__(self) -> bytes:
        return (
            self.public_key
            if len(self.public_key) == self.LENGTH
            else self.public_key.rjust(self.LENGTH, b"\0")
        )

    def __repr__(self) -> str:
        return str(self)

    def __str__(self) -> str:
        return self.to_base58().decode("utf-8")

    def to_base58(self) -> bytes:
        return base58.b58encode(bytes(self))
