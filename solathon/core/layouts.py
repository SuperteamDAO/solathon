# Developer reference: https://github.com/solana-labs/solana/blob/master/sdk/program/src/system_instruction.rs

from dataclasses import dataclass, asdict
from typing import Optional, Union, Type
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
        InstructionType.CREATE_ACCOUNT: unpack_create_account,
        InstructionType.ASSIGN: unpack_assign,
        InstructionType.TRANSFER: unpack_transfer,
        InstructionType.CREATE_ACCOUNT_WITH_SEED: unpack_create_account_with_seed,
        InstructionType.WITHDRAW_NONCE_ACCOUNT: unpack_withdraw_nonce_account,
        InstructionType.INITIALIZE_NONCE_ACCOUNT: unpack_initialize_nonce_account,
        InstructionType.AUTHORIZE_NONCE_ACCOUNT: unpack_authorize_nonce_account,
        InstructionType.ALLOCATE: unpack_allocate,
        InstructionType.ALLOCATE_WITH_SEED: unpack_allocate_with_seed,
        InstructionType.ASSIGN_WITH_SEED: unpack_assign_with_seed,
        InstructionType.TRANSFER_WITH_SEED: unpack_transfer_with_seed,
    }[type_value]
    args_length = struct.unpack("<I", data[4:8])[0]
    args_data = data[8: 8 + args_length]
    args = args_unpacker(args_data)
    return SystemInstructions(type=type_value, args=args)
