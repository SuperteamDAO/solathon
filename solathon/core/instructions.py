# Developer reference: https://github.com/solana-labs/solana/blob/master/sdk/program/src/system_instruction.rs
from __future__ import annotations

from typing import NamedTuple
from dataclasses import dataclass
from ..publickey import PublicKey
from ..core.layouts import (
    InstructionType,
    SYSTEM_INSTRUCTIONS_LAYOUT,
    SYSTEM_PROGRAM_ID
)


@dataclass
class AccountMeta:
    public_key: PublicKey | str
    is_signer: bool
    is_writable: bool


class Instruction(NamedTuple):
    keys: list[AccountMeta]
    program_id: PublicKey
    data: bytes = bytes(0)


def create_account(
        from_public_key: PublicKey,
        new_account_public_key: PublicKey,
        lamports: int,
        space: int,
        program_id: PublicKey
) -> Instruction:
    account_metas: list[AccountMeta] = [
        AccountMeta(
            public_key=from_public_key,
            is_signer=True,
            is_writable=True
        ),
        AccountMeta(
            public_key=new_account_public_key,
            is_signer=True,
            is_writable=True
        ),
    ]
    data: bytes = SYSTEM_INSTRUCTIONS_LAYOUT.build(
        dict(
            type=InstructionType.CREATE_ACCOUNT,
            args=dict(
                lamports=lamports, space=space,
                program_id=bytes(program_id)
            ),
        )
    )
    return Instruction(
        keys=account_metas,
        program_id=SYSTEM_PROGRAM_ID,
        data=data,
    )


def create_account_with_seed(
        from_public_key: PublicKey,
        new_account_public_key: PublicKey,
        base_public_key: PublicKey,
        seed: str,
        lamports: int,
        space: int,
        program_id: PublicKey
) -> Instruction:
    account_metas: list[AccountMeta] = [
        AccountMeta(
            public_key=from_public_key,
            is_signer=True,
            is_writable=True
        ),
        AccountMeta(
            public_key=new_account_public_key,
            is_signer=False,
            is_writable=True
        ),
    ]
    
    data: bytes = SYSTEM_INSTRUCTIONS_LAYOUT.build(
        dict(
            type=InstructionType.CREATE_ACCOUNT_WITH_SEED,
            args=dict(
                base=bytes(base_public_key),
                seed=seed,
                lamports=lamports,
                space=space,
                program_id=bytes(program_id),
            ),
        )
    )

    if base_public_key != from_public_key:
        account_metas.append(AccountMeta(
            public_key=base_public_key,
            is_signer=True,
            is_writable=False
        ))
    return Instruction(
        keys=account_metas, program_id=SYSTEM_PROGRAM_ID, data=data
    )


def assign(
        account_public_key: PublicKey,
        program_id: PublicKey
) -> Instruction:

    data = SYSTEM_INSTRUCTIONS_LAYOUT.build(
        dict(type=InstructionType.ASSIGN,
             args=dict(program_id=bytes(program_id)
                       ))
    )
    return Instruction(
        keys=[
            AccountMeta(
                public_key=account_public_key,
                is_signer=True,
                is_writable=True
            ),
        ],
        program_id=SYSTEM_PROGRAM_ID,
        data=data,
    )


# Need to implement assign_with_seed_here


def transfer(
        from_public_key: PublicKey | str,
        to_public_key: PublicKey | str,
        lamports: int
) -> Instruction:
    account_metas: list[AccountMeta] = [
        AccountMeta(
            public_key=from_public_key,
            is_signer=True,
            is_writable=True
        ),
        AccountMeta(
            public_key=to_public_key,
            is_signer=False,
            is_writable=True
        ),
    ]
    data: bytes = SYSTEM_INSTRUCTIONS_LAYOUT.build(
        dict(
            type=InstructionType.TRANSFER,
            args=dict(lamports=lamports)
        )
    )
    return Instruction(
        keys=account_metas,
        program_id=SYSTEM_PROGRAM_ID,
        data=data,
    )


def allocate(
        account_public_key: PublicKey,
        space: int
) -> Instruction:

    data: bytes = SYSTEM_INSTRUCTIONS_LAYOUT.build(
        dict(type=InstructionType.ALLOCATE, args=dict(space=space))
    )
    return Instruction(
        keys=[AccountMeta(
            public_key=account_public_key,
            is_signer=True,
            is_writable=True
        )],
        program_id=SYSTEM_PROGRAM_ID,
        data=data,
    )


def allocate_with_seed(
    account_public_key: PublicKey,
    base_public_key: PublicKey,
    seed: str,
    space: int,
    program_id: PublicKey
) -> Instruction:

    data: bytes = SYSTEM_INSTRUCTIONS_LAYOUT.build(
        dict(
            type=InstructionType.ALLOCATE_WITH_SEED,
            args=dict(
                base=bytes(base_public_key),
                seed=seed,
                space=space,
                program_id=bytes(program_id),
            ),
        )
    )
    return Instruction(
        keys=[AccountMeta(
            public_key=account_public_key,
            is_signer=True,
            is_writable=True
        )],
        program_id=SYSTEM_PROGRAM_ID,
        data=data,
    )
