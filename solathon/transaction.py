"""
Currently thanks to https://github.com/michaelhly/solana-py
"""

from dataclasses import dataclass
from typing import Dict, List, NamedTuple, NewType, Optional
from base58 import b58decode, b58encode
from nacl.exceptions import BadSignatureError
from nacl.signing import VerifyKey
from .keypair import Keypair
from .publickey import PublicKey
from .core.instructions import (
            transfer, 
            TransactionInstruction, 
            AccountMeta
        )

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


TransactionSignature = NewType("TransactionSignature", str)
PACKET_DATA_SIZE = 1280 - 40 - 8
SIG_LENGTH = 64


class CompiledInstruction(NamedTuple):
    accounts: bytes | List[int]
    program_id_index: int
    data: bytes


class MessageHeader(NamedTuple):
    num_required_signatures: int
    num_readonly_signed_accounts: int
    num_readonly_unsigned_accounts: int


class MessageArgs(NamedTuple):
    header: MessageHeader
    account_keys: List[str]
    recent_blockhash: str
    instructions: List[CompiledInstruction]


class Message:
    def __init__(self, args: MessageArgs) -> None:
        self.header = args.header
        self.account_keys = [PublicKey(key) for key in args.account_keys]
        self.recent_blockhash = args.recent_blockhash
        self.instructions = args.instructions

    def __encode_message(self) -> bytes:
        MessageFormat = NamedTuple(
            "MessageFormat",
            [
                ("num_required_signatures", bytes),
                ("num_readonly_signed_accounts", bytes),
                ("num_readonly_unsigned_accounts", bytes),
                ("pubkeys_length", bytes),
                ("pubkeys", bytes),
                ("recent_blockhash", bytes),
            ],
        )
        return b"".join(
            MessageFormat(
                num_required_signatures=to_uint8_bytes(self.header.num_required_signatures),
                num_readonly_signed_accounts=to_uint8_bytes(self.header.num_readonly_signed_accounts),
                num_readonly_unsigned_accounts=to_uint8_bytes(self.header.num_readonly_unsigned_accounts),
                pubkeys_length=encode_length(len(self.account_keys)),
                pubkeys=b"".join([bytes(pubkey) for pubkey in self.account_keys]),
                recent_blockhash=b58decode(self.recent_blockhash),
            )
        )

    @staticmethod
    def __encode_instruction(
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
        writable = index < (self.header.num_required_signatures - self.header.num_readonly_signed_accounts)
        return writable or self.header.num_required_signatures <= index < (
            len(self.account_keys) - self.header.num_readonly_unsigned_accounts
        )

    def serialize(self) -> bytes:
        message_buffer = bytearray()
        # Message body
        message_buffer.extend(self.__encode_message())
        # Instructions
        instruction_count = encode_length(len(self.instructions))
        message_buffer.extend(instruction_count)
        for instr in self.instructions:
            message_buffer.extend(Message.__encode_instruction(instr))
        
        return bytes(message_buffer)



@dataclass
class SigPubkeyPair:
    pubkey: PublicKey
    signature: Optional[bytes] = None


class Transaction:

    def __init__(
        self,
        sender,
        receiver,
        lamports,
        recent_blockhash: Optional[str] = None,
    ) -> None:
        self.sender = sender
        self.instructions: List[TransactionInstruction] = [transfer(sender.public_key, receiver, lamports)]
        self.signatures: List[SigPubkeyPair] =[]
            
        self.recent_blockhash, self.nonce_info = recent_blockhash, None


    def signature(self) -> Optional[bytes]:
        return None if not self.signatures else self.signatures[0].signature


    def compile_message(self) -> Message:

        if self.nonce_info and self.instructions[0] != self.nonce_info.nonce_instruction:
            self.recent_blockhash = self.nonce_info.nonce
            self.instructions = [
                self.nonce_info.nonce_instruction] + self.instructions

        if not self.recent_blockhash:
            raise AttributeError("transaction recentBlockhash required")
        if len(self.instructions) < 1:
            raise AttributeError("no instructions provided")

        fee_payer = self.signatures[0].pubkey

        account_metas, program_ids = [], set()
        for instr in self.instructions:
            if not instr.program_id:
                raise AttributeError("invalid instruction:", instr)
            account_metas.extend(instr.keys)
            program_ids.add(str(instr.program_id))

        # Append programID account metas.
        for pg_id in program_ids:
            account_metas.append(AccountMeta(PublicKey(pg_id), False, False))

        # Sort. Prioritizing first by signer, then by writable and converting from set to list.
        account_metas.sort(key=lambda account: (
            not account.is_signer, not account.is_writable))

        # Cull duplicate accounts
        fee_payer_idx = 1
        seen: Dict[str, int] = {}
        uniq_metas: List[AccountMeta] = []
        for sig in self.signatures:

            pubkey = str(sig.pubkey)
            if pubkey in seen:
                uniq_metas[seen[pubkey]].is_signer = True
            else:
                uniq_metas.append(AccountMeta(sig.pubkey, True, True))
                seen[pubkey] = len(uniq_metas) - 1
                if sig.pubkey == fee_payer:
                    fee_payer_idx = min(fee_payer_idx, seen[pubkey])

        for a_m in account_metas:
            pubkey = str(a_m.pubkey)
            if pubkey in seen:
                idx = seen[pubkey]
                uniq_metas[idx].is_writable = uniq_metas[idx].is_writable or a_m.is_writable
            else:
                uniq_metas.append(a_m)
                seen[pubkey] = len(uniq_metas) - 1
                if a_m.pubkey == fee_payer:
                    fee_payer_idx = min(fee_payer_idx, seen[pubkey])

        if fee_payer_idx == 1:
            uniq_metas = [AccountMeta(fee_payer, True, True)] + uniq_metas
        else:
            uniq_metas = (
                [uniq_metas[fee_payer_idx]] + uniq_metas[:fee_payer_idx] + uniq_metas[fee_payer_idx + 1:]
            )

        signed_keys: List[str] = []
        unsigned_keys: List[str] = []
        num_required_signatures = num_readonly_signed_accounts = num_readonly_unsigned_accounts = 0
        for a_m in uniq_metas:
            if a_m.is_signer:
                signed_keys.append(str(a_m.pubkey))
                num_required_signatures += 1
                num_readonly_signed_accounts += int(not a_m.is_writable)
            else:
                num_readonly_unsigned_accounts += int(not a_m.is_writable)
                unsigned_keys.append(str(a_m.pubkey))
        if not self.signatures:
            self.signatures = [SigPubkeyPair(pubkey=PublicKey(
                key), signature=None) for key in signed_keys]

        account_keys: List[str] = signed_keys + unsigned_keys
        account_indices: Dict[str, int] = {
            str(key): i for i, key in enumerate(account_keys)}
        compiled_instructions: List[CompiledInstruction] = [
            CompiledInstruction(
                accounts=[account_indices[str(a_m.pubkey)]
                          for a_m in instr.keys],
                program_id_index=account_indices[str(instr.program_id)],
                data=b58encode(instr.data),
            )
            for instr in self.instructions
        ]


        return Message(
            MessageArgs(
                header=MessageHeader(
                    num_required_signatures=num_required_signatures,
                    num_readonly_signed_accounts=num_readonly_signed_accounts,
                    num_readonly_unsigned_accounts=num_readonly_unsigned_accounts,
                ),
                account_keys=account_keys,
                instructions=compiled_instructions,
                recent_blockhash=self.recent_blockhash,
            )
        )

    def serialize_message(self) -> bytes:
        return self.compile_message().serialize()

    def sign_partial(self, *partial_signers: PublicKey | Keypair) -> None:

        def partial_signer_pubkey(account_or_pubkey: PublicKey | Keypair):
            return account_or_pubkey.public_key if isinstance(account_or_pubkey, Keypair) else account_or_pubkey

        signatures: List[SigPubkeyPair] = [
            SigPubkeyPair(pubkey=partial_signer_pubkey(partial_signer)) for partial_signer in partial_signers
        ]
        self.signatures = signatures
        sign_data = self.serialize_message()

        for idx, partial_signer in enumerate(partial_signers):
            if isinstance(partial_signer, Keypair):
                sig = partial_signer.sign(sign_data).signature
                if len(sig) != SIG_LENGTH:
                    raise RuntimeError("signature has invalid length", sig)
                self.signatures[idx].signature = sig

    def sign(self) -> None:
        self.sign_partial(self.sender)

    def add_signature(self, pubkey: PublicKey, signature: bytes) -> None:
        if len(signature) != SIG_LENGTH:
            raise ValueError("signature has invalid length", signature)
        idx = next((i for i, sig_pair in enumerate(self.signatures)
                   if sig_pair.pubkey == pubkey), None)
        if idx is None:
            raise ValueError("unknown signer: ", str(pubkey))
        self.signatures[idx].signature = signature

    def add_signer(self, signer: Keypair) -> None:
        signed_msg = signer.sign(self.serialize_message())
        self.add_signature(signer.public_key, signed_msg.signature)

    def verify_signatures(self) -> bool:
        return self.__verify_signatures(self.serialize_message())

    def __verify_signatures(self, signed_data: bytes) -> bool:
        for sig_pair in self.signatures:
            if not sig_pair.signature:
                return False
            try:

                VerifyKey(bytes(sig_pair.pubkey)).verify(
                    signed_data, sig_pair.signature)
            except BadSignatureError:
                return False
        return True


    def serialize(self) -> bytes:
        if not self.signatures:
            raise AttributeError("transaction has not been signed")

        sign_data = self.serialize_message()
        if not self.__verify_signatures(sign_data):
            raise AttributeError("transaction has not been signed correctly")

        return self.__serialize(sign_data)


    def __serialize(self, signed_data: bytes) -> bytes:
        if len(self.signatures) >= SIG_LENGTH * 4:
            raise AttributeError("too many singatures to encode")
        wire_transaction = bytearray()
        # Encode signature count
        signature_count = encode_length(len(self.signatures))
        wire_transaction.extend(signature_count)
        # Encode signatures
        for sig_pair in self.signatures:
            if sig_pair.signature and len(sig_pair.signature) != SIG_LENGTH:
                raise RuntimeError(
                    "signature has invalid length", sig_pair.signature)

            if not sig_pair.signature:
                wire_transaction.extend(bytearray(SIG_LENGTH))
            else:
                wire_transaction.extend(sig_pair.signature)
        # Encode signed data
        wire_transaction.extend(signed_data)

        if len(wire_transaction) > PACKET_DATA_SIZE:
            raise RuntimeError(
                f"transaction too large: {len(wire_transaction)} > {PACKET_DATA_SIZE}")

        return bytes(wire_transaction)

