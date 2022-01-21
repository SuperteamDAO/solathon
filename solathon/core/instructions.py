"""
Currently thanks to https://github.com/michaelhly/solana-py
"""

from enum import IntEnum
from dataclasses import dataclass
from typing import NamedTuple, List
from construct import Struct as cStruct
from construct import (
                Bytes, 
                Int32ul, 
                Int64ul, 
                PaddedString, 
                Padding, 
                Pass,
                Switch
        )
from ..publickey import PublicKey


SYS_PROGRAM_ID: PublicKey = PublicKey("11111111111111111111111111111111")
PUBLIC_KEY_LAYOUT = Bytes(32)
RUST_STRING_LAYOUT = cStruct(
    "length" / Int32ul,
    Padding(4),
    "chars" / PaddedString(lambda this: this.length, "utf-8"),
)


class InstructionType(IntEnum):
    CREATE_ACCOUNT = 0
    ASSIGN = 1
    TRANSFER = 2
    CREATE_ACCOUNT_WITH_SEED = 3
    ADVANCE_NONCE_ACCOUNT = 4
    WITHDRAW_NONCE_ACCOUNT = 5
    INITIALIZE_NONCE_ACCOUNT = 6
    AUTHORIZE_NONCE_ACCOUNT = 7
    ALLOCATE = 8
    ALLOCATE_WITH_SEED = 9
    ASSIGN_WITH_SEED = 10
    TRANSFER_WITH_SEED = 11


_CREATE_ACCOUNT_LAYOUT = cStruct(
    "lamports" / Int64ul,
    "space" / Int64ul,
    "program_id" / PUBLIC_KEY_LAYOUT,
)

_ASSIGN_LAYOUT = cStruct("program_id" / PUBLIC_KEY_LAYOUT)

_TRANFER_LAYOUT = cStruct("lamports" / Int64ul)

_CREATE_ACCOUNT_WTIH_SEED_LAYOUT = cStruct(
    "base" / PUBLIC_KEY_LAYOUT,
    "seed" / RUST_STRING_LAYOUT,
    "lamports" / Int64ul,
    "space" / Int64ul,
    "program_id" / PUBLIC_KEY_LAYOUT,
)

_WITHDRAW_NONCE_ACCOUNT_LAYOUT = cStruct("lamports" / Int64ul)

_INITIALIZE_NONCE_ACCOUNT_LAYOUT = cStruct("authorized" / PUBLIC_KEY_LAYOUT)

_AUTHORIZE_NONCE_ACCOUNT_LAYOUT = cStruct("authorized" / PUBLIC_KEY_LAYOUT)

_ALLOCATE_LAYOUT = cStruct("space" / Int64ul)

_ALLOCATE_WITH_SEED_LAYOUT = cStruct(
    "base" / PUBLIC_KEY_LAYOUT, "seed" / RUST_STRING_LAYOUT, "space" / Int64ul, "program_id" / PUBLIC_KEY_LAYOUT
)

_ASSIGN_WITH_SEED_LAYOUT = cStruct(
    "base" / PUBLIC_KEY_LAYOUT, "seed" / RUST_STRING_LAYOUT, "program_id" / PUBLIC_KEY_LAYOUT
)

_TRANSFER_WITH_SEED_LAYOUT = cStruct(
    "lamports" / Int64ul,
    "from_seed" / RUST_STRING_LAYOUT,
    "from_ower" / PUBLIC_KEY_LAYOUT,
)

SYSTEM_INSTRUCTIONS_LAYOUT = cStruct(
    "instruction_type" / Int32ul,
    "args"
    / Switch(
        lambda this: this.instruction_type,
        {
            InstructionType.CREATE_ACCOUNT: _CREATE_ACCOUNT_LAYOUT,
            InstructionType.ASSIGN: _ASSIGN_LAYOUT,
            InstructionType.TRANSFER: _TRANFER_LAYOUT,
            InstructionType.CREATE_ACCOUNT_WITH_SEED: _CREATE_ACCOUNT_WTIH_SEED_LAYOUT,
            InstructionType.ADVANCE_NONCE_ACCOUNT: Pass,  # No args
            InstructionType.WITHDRAW_NONCE_ACCOUNT: _WITHDRAW_NONCE_ACCOUNT_LAYOUT,
            InstructionType.INITIALIZE_NONCE_ACCOUNT: _INITIALIZE_NONCE_ACCOUNT_LAYOUT,
            InstructionType.AUTHORIZE_NONCE_ACCOUNT: _AUTHORIZE_NONCE_ACCOUNT_LAYOUT,
            InstructionType.ALLOCATE: _ALLOCATE_LAYOUT,
            InstructionType.ALLOCATE_WITH_SEED: _ALLOCATE_WITH_SEED_LAYOUT,
            InstructionType.ASSIGN_WITH_SEED: _ASSIGN_WITH_SEED_LAYOUT,
            InstructionType.TRANSFER_WITH_SEED: _TRANSFER_WITH_SEED_LAYOUT,
        },
    ),
)


class TransferParams(NamedTuple):
    from_pubkey: PublicKey
    to_pubkey: PublicKey
    lamports: int

@dataclass
class AccountMeta:
    pubkey: PublicKey
    is_signer: bool
    is_writable: bool


class TransactionInstruction(NamedTuple):
    keys: List[AccountMeta]
    program_id: PublicKey
    data: bytes = bytes(0)



def transfer(sender, receiver, lamports) -> TransactionInstruction:
    data = SYSTEM_INSTRUCTIONS_LAYOUT.build(
        dict(instruction_type=InstructionType.TRANSFER, args=dict(lamports=lamports))
    )
    return TransactionInstruction(
        keys=[
            AccountMeta(pubkey=sender, is_signer=True, is_writable=True),
            AccountMeta(pubkey=receiver, is_signer=False, is_writable=True),
        ],
        program_id=SYS_PROGRAM_ID,
        data=data,
    )

