from __future__ import annotations

from dataclasses import dataclass
from typing import List, Tuple
from base58 import b58decode, b58encode
from .keypair import Keypair
from .publickey import PublicKey
from nacl.signing import VerifyKey
from nacl.exceptions import BadSignatureError
from .core.instructions import Instruction, AccountMeta
from .core.message import (
    Message,
    MessageHeader,
    CompiledInstruction,
    encode_length,
    decode_length
)

PACKET_DATA_SIZE = 1232
DEFAULT_SIGNATURE = bytes([0] * 64)


@dataclass
class PKSigPair:
    public_key: PublicKey
    signature: bytes | None = None


class Transaction:
    def __init__(self, **config):
        self.fee_payer: PublicKey = config.get("fee_payer")
        self.nonce_info = config.get("nonce_info")
        self.recent_blockhash = config.get("recent_blockhash")
        self.signers: List[Keypair] = config.get("signers", [])
        self.instructions: List[Instruction] = config.get("instructions", [])
        self.signatures: List[PKSigPair] = []

        if not all(isinstance(signer, Keypair) for signer in self.signers):
            raise TypeError("All signers must be instances of Keypair.")

    def compile_transaction(self) -> bytes:
        self.validate_transaction()

        account_metas, program_ids = self.extract_account_metas_and_program_ids()

        uniq_metas, fee_payer_idx = self.process_signatures(account_metas)

        compiled_instructions = self.compile_instructions(program_ids)

        message = self.create_message(uniq_metas, compiled_instructions)

        serialized_message = message.serialize()
        return serialized_message

    def validate_transaction(self) -> None:
        if self.nonce_info:
            self.recent_blockhash = self.nonce_info.nonce

        if not self.instructions:
            raise AttributeError("No instructions provided.")

        if not self.recent_blockhash:
            raise AttributeError("Recent blockhash not provided.")

        if not self.signatures:
            raise AttributeError("No signatures found in the transaction.")

        if not self.fee_payer:
            self.fee_payer = self.signatures[0].public_key

    def extract_account_metas_and_program_ids(self) -> Tuple[List[AccountMeta], List[str]]:
        account_metas: List[AccountMeta] = []
        program_ids: List[str] = []

        for instruction in self.instructions:
            if not instruction.program_id:
                raise AttributeError("Invalid instruction (no program ID found): ", instruction)
            account_metas.extend(instruction.keys)
            if str(instruction.program_id) not in program_ids:
                program_ids.append(str(instruction.program_id))

        return account_metas, program_ids

    def process_signatures(self, account_metas: List[AccountMeta]) -> Tuple[List[AccountMeta], int]:
        fee_payer_idx = 0
        seen = {}
        uniq_metas = []

        for idx, sig in enumerate(self.signatures):
            public_key = str(sig.public_key)
            if public_key in seen:
                uniq_metas[seen[public_key]].is_signer = True
            else:
                uniq_metas.append(AccountMeta(sig.public_key, True, True))
                seen[public_key] = len(uniq_metas) - 1
                if sig.public_key == self.fee_payer:
                    fee_payer_idx = min(fee_payer_idx, seen[public_key])

        return uniq_metas, fee_payer_idx

    def compile_instructions(self, program_ids: List[str]) -> List[CompiledInstruction]:
        account_metas = []
        for program_id in program_ids:
            account_metas.append(AccountMeta(
                public_key=PublicKey(program_id),
                is_signer=False,
                is_writable=False
            ))

        account_metas.sort(key=lambda account: (not account.is_signer, not account.is_writable))

        compiled_instructions = [
            CompiledInstruction(
                accounts=[account_indices[str(a_m.public_key)] for a_m in instr.keys],
                program_id_index=account_indices[str(instr.program_id)],
                data=b58encode(instr.data),
            )
            for instr in self.instructions
        ]
        return compiled_instructions

    def create_message(self, uniq_metas: List[AccountMeta], compiled_instructions: List[CompiledInstruction]) -> Message:
        account_keys, account_indices = self.create_account_keys_and_indices(uniq_metas)

        message = Message(
            MessageHeader(
                num_required_signatures=num_required_signatures,
                num_readonly_signed_accounts=num_readonly_signed_accounts,
                num_readonly_unsigned_accounts=num_readonly_unsigned_accounts,
            ),
            account_keys,
            compiled_instructions,
            self.recent_blockhash,
        )

        return message

    def create_account_keys_and_indices(self, uniq_metas: List[AccountMeta]) -> Tuple[List[str], dict[str, int]]:
        signed_keys = []
        unsigned_keys = []
        num_required_signatures = num_readonly_signed_accounts = num_readonly_unsigned_accounts = 0
        for a_m in uniq_metas:
            if a_m.is_signer:
                signed_keys.append(str(a_m.public_key))
                num_required_signatures += 1
                num_readonly_signed_accounts += int(not a_m.is_writable)
            else:
                num_readonly_unsigned_accounts += int(not a_m.is_writable)
                unsigned_keys.append(str(a_m.public_key))

        if not self.signatures:
            self.signatures = [PKSigPair(public_key=PublicKey(key), signature=None) for key in signed_keys]

        account_keys = signed_keys + unsigned_keys
        account_indices = {str(key): i for i, key in enumerate(account_keys)}
        return account_keys, account_indices

    def sign(self) -> None:
        self.validate_transaction()

        def to_public_key(signer: PublicKey | Keypair) -> PublicKey:
            if isinstance(signer, Keypair):
                return signer.public_key
            elif isinstance(signer, PublicKey):
                return signer
            else:
                raise TypeError("The argument must be either PublicKey or Keypair object.")

        pk_sig_pairs = [PKSigPair(public_key=to_public_key(signer)) for signer in self.signers]

        self.signatures = pk_sig_pairs
        sign_data = self.compile_transaction()
        for idx, signer in enumerate(self.signers):
            signature = signer.sign(sign_data).signature
            if len(signature) != 64:
                raise RuntimeError("Signature has invalid length: ", signature)
            self.signatures[idx].signature = signature

    def verify_signatures(self, signed_data: bytes | None = None) -> bool:
        if signed_data is None:
            signed_data = self.compile_transaction()
        for sig_pair in self.signatures:
            if not sig_pair.signature:
                return False
            try:
                VerifyKey(bytes(sig_pair.public_key)).verify(
                    signed_data, sig_pair.signature)
            except BadSignatureError:
                return False
        return True

    def serialize(self) -> bytes:
        if not self.signatures:
            raise AttributeError("Transaction has not been signed.")

        sign_data = self.compile_transaction()
        if not self.verify_signatures(sign_data):
            raise AttributeError("Transaction has not been signed correctly.")

        if len(self.signatures) >= 64 * 4:
            raise AttributeError("Too many signatures to encode.")

        wire_transaction = bytearray()
        signature_count = encode_length(len(self.signatures))
        wire_transaction.extend(signature_count)
        for sig_pair in self.signatures:
            if sig_pair.signature and len(sig_pair.signature) != 64:
                raise RuntimeError("Signature has invalid length: ", sig_pair.signature)

            if not sig_pair.signature:
                wire_transaction.extend(bytearray(64))
            else:
                wire_transaction.extend(sig_pair.signature)

        wire_transaction.extend(bytearray(sign_data))

        if len(wire_transaction) > PACKET_DATA_SIZE:
            raise RuntimeError("Transaction too large: ", len(wire_transaction))
        return bytes(wire_transaction)

    def add_instructions(self, *instructions: Instruction) -> None:
        for instr in instructions:
            if not isinstance(instr, Instruction):
                raise ValueError("Argument not an instruction object: ", instr)
            self.instructions.append(instr)

    @classmethod
    def populate(cls, message: Message, signatures: List[bytes]) -> Transaction:
        decoded_signatures = [
            PKSigPair(
                public_key=message.account_keys[x[0]],
                signature=None if x[1] == b58encode(DEFAULT_SIGNATURE) else b58decode(x[1])
            ) for x in enumerate(signatures)
        ]

        instructions = []
        for instruction in message.instructions:
            acc_metas = [
                AccountMeta(
                    public_key=message.account_keys[account],
                    is_signer=message.is_account_signer(account) or
                    message.account_keys[account] in [x.public_key for x in decoded_signatures],
                    is_writable=message.is_account_writable(account)
                ) for account in instruction.accounts
            ]
            instructions.append(Instruction(
                program_id=message.account_keys[instruction.program_id_index],
                keys=acc_metas,
                data=b58decode(instruction.data)
            ))

        fee_payer = message.account_keys[0] if message.header.num_required_signatures > 0 else None
        return cls(
            fee_payer=fee_payer,
            recent_blockhash=message.recent_blockhash,
            signatures=decoded_signatures,
            instructions=instructions
        )

    @classmethod
    def from_buffer(cls, buffer: bytes) -> Transaction:
        if not isinstance(buffer, bytes):
            raise TypeError("Buffer must be a bytes object.")

        buffer_array = list(buffer)
        signature_length = decode_length(buffer_array)

        signatures = []
        for _ in range(signature_length):
            signature = bytes(buffer_array[:64])
            buffer_array = buffer_array[64:]
            signatures.append(b58encode(signature))

        message = Message.from_buffer(bytes(buffer_array))
        return cls.populate(message, signatures)
