from __future__ import annotations

from dataclasses import dataclass
from base58 import b58encode
from .keypair import Keypair
from .publickey import PublicKey
from nacl.signing import VerifyKey
from nacl.exceptions import BadSignatureError
from .core.instructions import Instruction, AccountMeta
from .core.message import (
    Message,
    MessageHeader,
    CompiledInstruction,
    encode_length
)

PACKET_DATA_SIZE = 1232


@dataclass
class PKSigPair:
    public_key: PublicKey
    signature: bytes | None = None


class Transaction:
    def __init__(self, **config):
        self.fee_payer: PublicKey = config.get("fee_payer")
        self.nonce_info = config.get("nonce_info")
        self.recent_blockhash = config.get("recent_blockhash")
        self.signers: list[Keypair] = config.get("signers")
        self.instructions: list[Instruction] = []
        self.signatures: list[PKSigPair] = []
        if "instructions" in config:
            instructions: Instruction = config.get("instructions")
            if (
                type(instructions) is list and
                isinstance(instructions[0], Instruction)
            ):
                self.instructions.extend(config["instructions"])
            else:
                raise TypeError((
                                "instructions keyword argument"
                                "must be a list of Instruction objects"
                                ))

    def compile_transaction(self) -> bytes:
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

        account_metas: list[AccountMeta] = []
        program_ids: list[str] = []

        for instruction in self.instructions:
            if not instruction.program_id:
                raise AttributeError(
                    "Invalid instruction (no program ID found): ",
                    instruction
                )
            account_metas.extend(instruction.keys)
            if str(instruction.program_id) not in program_ids:
                program_ids.append(str(instruction.program_id))

        for program_id in program_ids:
            account_metas.append(AccountMeta(
                public_key=PublicKey(program_id),
                is_signer=False,
                is_writable=False
            ))

        account_metas.sort(key=lambda account: (
            not account.is_signer, not account.is_writable))

        fee_payer_idx = 0
        seen: dict[str, int] = {}
        uniq_metas: list[AccountMeta] = []

        for sig in self.signatures:
            public_key = str(sig.public_key)
            if public_key in seen:
                uniq_metas[seen[public_key]].is_signer = True
            else:
                uniq_metas.append(AccountMeta(sig.public_key, True, True))
                seen[public_key] = len(uniq_metas) - 1
                if sig.public_key == self.fee_payer:
                    fee_payer_idx = min(fee_payer_idx, seen[public_key])

        for a_m in account_metas:
            public_key = str(a_m.public_key)
            if public_key in seen:
                idx = seen[public_key]
                uniq_metas[idx].is_writable = uniq_metas[idx].is_writable or a_m.is_writable
            else:
                uniq_metas.append(a_m)
                seen[public_key] = len(uniq_metas) - 1
                if a_m.public_key == self.fee_payer:
                    fee_payer_idx = min(fee_payer_idx, seen[public_key])

        if fee_payer_idx == 1:
            uniq_metas = [AccountMeta(self.fee_payer, True, True)] + uniq_metas
        else:
            uniq_metas = (
                [uniq_metas[fee_payer_idx]] + uniq_metas[:fee_payer_idx] +
                uniq_metas[fee_payer_idx + 1:]
            )

        signed_keys: list[str] = []
        unsigned_keys: list[str] = []
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
            self.signatures = [PKSigPair(public_key=PublicKey(
                key), signature=None) for key in signed_keys]

        account_keys: list[str] = signed_keys + unsigned_keys
        account_indices: dict[str, int] = {
            str(key): i for i, key in enumerate(account_keys)}
        compiled_instructions: list[CompiledInstruction] = [
            CompiledInstruction(
                accounts=[account_indices[str(a_m.public_key)]
                          for a_m in instr.keys],
                program_id_index=account_indices[str(instr.program_id)],
                data=b58encode(instr.data),
            )
            for instr in self.instructions
        ]
        message: Message = Message(
            MessageHeader(
                num_required_signatures=num_required_signatures,
                num_readonly_signed_accounts=num_readonly_signed_accounts,
                num_readonly_unsigned_accounts=num_readonly_unsigned_accounts,
            ),
            account_keys,
            compiled_instructions,
            self.recent_blockhash,
        )
        serialized_message: bytes = message.serialize()
        return serialized_message

    def sign(self) -> None:

        def to_public_key(signer: PublicKey | Keypair) -> PublicKey:
            if isinstance(signer, Keypair):
                return signer.public_key
            elif isinstance(signer, PublicKey):
                return signer
            else:
                raise TypeError(("The argument must be either "
                                "PublicKey or Keypair object."))

        pk_sig_pairs: list[PKSigPair] = [PKSigPair(
            public_key=to_public_key(signer)
        ) for signer in self.signers]

        self.signatures = pk_sig_pairs
        sign_data: bytes = self.compile_transaction()
        for idx, signer in enumerate(self.signers):
            signature = signer.sign(sign_data).signature
            if len(signature) != 64:
                raise RuntimeError(
                    "Signature has invalid length: ",
                    signature
                )
            self.signatures[idx].signature = signature

    def verify_signatures(self, signed_data: bytes | None = None) -> bool:
        if signed_data is None:
            signed_data: bytes = self.compile_transaction()
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

        sign_data: bytes = self.compile_transaction()
        if not self.verify_signatures(sign_data):
            raise AttributeError("Transaction has not been signed correctly.")

        if len(self.signatures) >= 64 * 4:
            raise AttributeError("Too many signatures to encode.")

        wire_transaction = bytearray()
        signature_count = encode_length(len(self.signatures))
        wire_transaction.extend(signature_count)
        for sig_pair in self.signatures:
            if sig_pair.signature and len(sig_pair.signature) != 64:
                raise RuntimeError(
                    "Signature has invalid length: ", sig_pair.signature
                )

            if not sig_pair.signature:
                wire_transaction.extend(bytearray(64))
            else:
                wire_transaction.extend(sig_pair.signature)

        wire_transaction.extend(bytearray(sign_data))

        if len(wire_transaction) > PACKET_DATA_SIZE:
            raise RuntimeError(
                "Transaction too large: ",
                len(wire_transaction)
            )
        return bytes(wire_transaction)

    def add_instructions(self, *instructions: Instruction) -> None:
        for instr in instructions:
            if not isinstance(instr, Instruction):
                raise ValueError(
                    "Argument not an instruction object: ",
                    instr
                )
            self.instructions.append(instr)
