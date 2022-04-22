# Thanks to https://github.com/michaelhly/solana-py/blob/master/src/solana/system_program.py
from __future__ import annotations

from enum import IntEnum
from construct import (
    Bytes,
    Int32ul,
    Int64ul,
    PaddedString,
    Padding,
    Pass,
    Switch,
    Struct,
)
from ..publickey import PublicKey


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


SYSTEM_PROGRAM_ID: PublicKey = PublicKey("11111111111111111111111111111111")

PUBLIC_KEY_LAYOUT: Bytes = Bytes(32)

RUST_STRING_LAYOUT: Struct = Struct(
    "length" / Int32ul,
    Padding(4),
    "chars" / PaddedString(lambda this: this.length, "utf-8"),
)

CREATE_ACCOUNT_LAYOUT = Struct(
    "lamports" / Int64ul,
    "space" / Int64ul,
    "program_id" / PUBLIC_KEY_LAYOUT,
)

ASSIGN_LAYOUT = Struct("program_id" / PUBLIC_KEY_LAYOUT)

TRANFER_LAYOUT = Struct("lamports" / Int64ul)

CREATE_ACCOUNT_WTIH_SEED_LAYOUT = Struct(
    "base" / PUBLIC_KEY_LAYOUT,
    "seed" / RUST_STRING_LAYOUT,
    "lamports" / Int64ul,
    "space" / Int64ul,
    "program_id" / PUBLIC_KEY_LAYOUT,
)

WITHDRAW_NONCE_ACCOUNT_LAYOUT = Struct("lamports" / Int64ul)

INITIALIZE_NONCE_ACCOUNT_LAYOUT = Struct("authorized" / PUBLIC_KEY_LAYOUT)

AUTHORIZE_NONCE_ACCOUNT_LAYOUT = Struct("authorized" / PUBLIC_KEY_LAYOUT)

ALLOCATE_LAYOUT = Struct("space" / Int64ul)

ALLOCATE_WITH_SEED_LAYOUT = Struct(
    "base" / PUBLIC_KEY_LAYOUT, "seed" / RUST_STRING_LAYOUT, "space" /
    Int64ul, "program_id" / PUBLIC_KEY_LAYOUT
)

ASSIGN_WITH_SEED_LAYOUT = Struct(
    "base" / PUBLIC_KEY_LAYOUT, "seed" /
    RUST_STRING_LAYOUT, "program_id" / PUBLIC_KEY_LAYOUT
)

TRANSFER_WITH_SEED_LAYOUT = Struct(
    "lamports" / Int64ul,
    "from_seed" / RUST_STRING_LAYOUT,
    "from_ower" / PUBLIC_KEY_LAYOUT,
)

SYSTEM_INSTRUCTIONS_LAYOUT = Struct(
    "type" / Int32ul,
    "args"
    / Switch(
        lambda this: this.type,
        {
            InstructionType.CREATE_ACCOUNT: CREATE_ACCOUNT_LAYOUT,
            InstructionType.ASSIGN: ASSIGN_LAYOUT,
            InstructionType.TRANSFER: TRANFER_LAYOUT,
            InstructionType.CREATE_ACCOUNT_WITH_SEED: CREATE_ACCOUNT_WTIH_SEED_LAYOUT,
            InstructionType.ADVANCE_NONCE_ACCOUNT: Pass,  # No args
            InstructionType.WITHDRAW_NONCE_ACCOUNT: WITHDRAW_NONCE_ACCOUNT_LAYOUT,
            InstructionType.INITIALIZE_NONCE_ACCOUNT: INITIALIZE_NONCE_ACCOUNT_LAYOUT,
            InstructionType.AUTHORIZE_NONCE_ACCOUNT: AUTHORIZE_NONCE_ACCOUNT_LAYOUT,
            InstructionType.ALLOCATE: ALLOCATE_LAYOUT,
            InstructionType.ALLOCATE_WITH_SEED: ALLOCATE_WITH_SEED_LAYOUT,
            InstructionType.ASSIGN_WITH_SEED: ASSIGN_WITH_SEED_LAYOUT,
            InstructionType.TRANSFER_WITH_SEED: TRANSFER_WITH_SEED_LAYOUT,
        },
    ),
)
