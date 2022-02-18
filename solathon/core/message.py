from __future__ import annotations

from typing import NamedTuple
from base58 import b58decode
from ..publickey import PublicKey


def encode_length(value: int) -> bytes:
    elems, rem_len = [], value
    while True:
        elem = rem_len & 0x7F
        rem_len >>= 7
        if not rem_len:
            elems.append(elem)
            break
        elem |= 0x80
        elems.append(elem)
    return bytes(elems)

def to_uint8_bytes(val: int) -> bytes:
    return val.to_bytes(1, byteorder="little")

class CompiledInstruction(NamedTuple):
    accounts: bytes | list[int]
    program_id_index: int
    data: bytes

class MessageHeader(NamedTuple):
    num_required_signatures: int
    num_readonly_signed_accounts: int
    num_readonly_unsigned_accounts: int


class Message:
    def __init__(
        self,
        header: MessageHeader,
        account_keys: list[str],
        instructions: list[CompiledInstruction],
        recent_blockhash: str
    ):
        self.header = header
        self.account_keys = [PublicKey(key) for key in account_keys]
        self.recent_blockhash = recent_blockhash
        self.instructions = instructions

    def encode_message(self) -> bytes:
        MessageFormat = NamedTuple(
            "MessageFormat",
            [
                ("num_required_signatures", bytes),
                ("num_readonly_signed_accounts", bytes),
                ("num_readonly_unsigned_accounts", bytes),
                ("public_keys_length", bytes),
                ("public_keys", bytes),
                ("recent_blockhash", bytes),
            ],
        )

        return b"".join(
            MessageFormat(
                num_required_signatures=to_uint8_bytes(
                    self.header.num_required_signatures),
                num_readonly_signed_accounts=to_uint8_bytes(
                    self.header.num_readonly_signed_accounts),
                num_readonly_unsigned_accounts=to_uint8_bytes(
                    self.header.num_readonly_unsigned_accounts),
                public_keys_length=encode_length(len(self.account_keys)),
                public_keys=b"".join([bytes(public_key)
                                      for public_key in self.account_keys]),
                recent_blockhash=b58decode(self.recent_blockhash),
            )
        )

    @staticmethod
    def encode_instruction(
        instruction: "CompiledInstruction",
    ) -> bytes:
        InstructionFormat = NamedTuple(
            "InstructionFormat",
            [
                ("program_idx", bytes),
                ("accounts_length", bytes),
                ("accounts", bytes),
                ("data_length", bytes),
                ("data", bytes),
            ],
        )
        data = b58decode(instruction.data)
        data_length = encode_length(len(data))
        return b"".join(
            InstructionFormat(
                program_idx=to_uint8_bytes(instruction.program_id_index),
                accounts_length=encode_length(len(instruction.accounts)),
                accounts=bytes(instruction.accounts),
                data_length=data_length,
                data=data,
            )
        )

    def is_account_writable(self, index: int) -> bool:
        writable = index < (self.header.num_required_signatures -
                            self.header.num_readonly_signed_accounts)
        return writable or self.header.num_required_signatures <= index < (
            len(self.account_keys) - self.header.num_readonly_unsigned_accounts
        )

    def serialize(self) -> bytes:
        message_buffer = bytearray()
        # Message body
        message_buffer.extend(self.encode_message())
        # Instructions
        instruction_count = encode_length(len(self.instructions))
        message_buffer.extend(instruction_count)
        for instr in self.instructions:
            message_buffer.extend(Message.encode_instruction(instr))

        return bytes(message_buffer)
