# Developer reference: https://github.com/solana-labs/solana/blob/master/sdk/program/src/system_instruction.rs

from dataclasses import dataclass
from typing import Optional, Union
import struct

@dataclass
class PublicKey:
    value: str

@dataclass
class RustString:
    length: int
    chars: str

@dataclass
class CreateAccount:
    lamports: int
    space: int
    program_id: PublicKey

@dataclass
class Assign:
    program_id: PublicKey

@dataclass
class Transfer:
    lamports: int

@dataclass
class CreateAccountWithSeed:
    base: PublicKey
    seed: RustString
    lamports: int
    space: int
    program_id: PublicKey

@dataclass
class WithdrawNonceAccount:
    lamports: int

@dataclass
class InitializeNonceAccount:
    authorized: PublicKey

@dataclass
class AuthorizeNonceAccount:
    authorized: PublicKey

@dataclass
class Allocate:
    space: int

@dataclass
class AllocateWithSeed:
    base: PublicKey
    seed: RustString
    space: int
    program_id: PublicKey

@dataclass
class AssignWithSeed:
    base: PublicKey
    seed: RustString
    program_id: PublicKey

@dataclass
class TransferWithSeed:
    lamports: int
    from_seed: RustString
    from_owner: PublicKey

@dataclass
class SystemInstructions:
    type: int
    args: Optional[Union[CreateAccount, Assign, Transfer, CreateAccountWithSeed,
                        WithdrawNonceAccount, InitializeNonceAccount, AuthorizeNonceAccount,
                        Allocate, AllocateWithSeed, AssignWithSeed, TransferWithSeed]] = None

# Helper functions for packing and unpacking

def pack_public_key(public_key: PublicKey) -> bytes:
    return public_key.value.encode("utf-8")

def unpack_public_key(data: bytes) -> PublicKey:
    return PublicKey(value=data.decode("utf-8"))

def pack_rust_string(rust_string: RustString) -> bytes:
    return struct.pack("<I", rust_string.length) + rust_string.chars.encode("utf-8")

def unpack_rust_string(data: bytes) -> RustString:
    length = struct.unpack("<I", data[:4])[0]
    chars = data[4:].decode("utf-8")
    return RustString(length=length, chars=chars)

# Pack and Unpack functions for SystemInstructions

def pack_system_instruction(instruction: SystemInstructions) -> bytes:
    packed_data = struct.pack("<I", instruction.type)
    if instruction.args is not None:
        args_packer = {
            CreateAccount: pack_create_account,
            Assign: pack_assign,
            Transfer: pack_transfer,
            CreateAccountWithSeed: pack_create_account_with_seed,
            WithdrawNonceAccount: pack_withdraw_nonce_account,
            InitializeNonceAccount: pack_initialize_nonce_account,
            AuthorizeNonceAccount: pack_authorize_nonce_account,
            Allocate: pack_allocate,
            AllocateWithSeed: pack_allocate_with_seed,
            AssignWithSeed: pack_assign_with_seed,
            TransferWithSeed: pack_transfer_with_seed,
        }[type(instruction.args)]
        packed_data += args_packer(instruction.args)
    return packed_data

def unpack_system_instruction(data: bytes) -> SystemInstructions:
    type_value = struct.unpack("<I", data[:4])[0]
    args_unpacker = {
        0: unpack_create_account,
        1: unpack_assign,
        2: unpack_transfer,
        3: unpack_create_account_with_seed,
        4: unpack_withdraw_nonce_account,
        5: unpack_initialize_nonce_account,
        6: unpack_authorize_nonce_account,
        7: unpack_allocate,
        8: unpack_allocate_with_seed,
        9: unpack_assign_with_seed,
        10: unpack_transfer_with_seed,
    }[type_value]
    args_length = struct.unpack("<I", data[4:8])[0]
    args_data = data[8: 8 + args_length]
    args = args_unpacker(args_data)
    return SystemInstructions(type=type_value, args=args)

# Layouts

SYSTEM_INSTRUCTIONS_LAYOUT = Struct(
    "type" / Int32ul,
    "args"
    / Switch(
        lambda this: this.type,
        {
            0: CREATE_ACCOUNT_LAYOUT,
            1: ASSIGN_LAYOUT,
            2: TRANFER_LAYOUT,
            3: CREATE_ACCOUNT_WTIH_SEED_LAYOUT,
            4: Pass,  # Placeholder or Pass if no args for ADVANCE_NONCE_ACCOUNT
            5: WITHDRAW_NONCE_ACCOUNT_LAYOUT,
            6: INITIALIZE_NONCE_ACCOUNT_LAYOUT,
            7: AUTHORIZE_NONCE_ACCOUNT_LAYOUT,
            8: ALLOCATE_LAYOUT,
            9: ALLOCATE_WITH_SEED_LAYOUT,
            10: ASSIGN_WITH_SEED_LAYOUT,
            11: TRANSFER_WITH_SEED_LAYOUT,
        },
    ),
)
