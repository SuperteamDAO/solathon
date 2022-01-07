from dataclasses import dataclass
from ..publickey import PublicKey

SYSTEM_ID: PublicKey = PublicKey("11111111111111111111111111111111")


@dataclass
class InstructionAccounts:
    from_pubkey: PublicKey
    to_pubkey: PublicKey
    signer: PublicKey
    lamports: int


@dataclass
class Instruction:
    instruction_accounts: InstructionAccounts
    program_id: PublicKey
    data: bytes


def transfer(from_pubkey: str, to_pubkey: str, lamports: str) -> Instruction:
    data = "placeholder"
    return Instruction(
        instruction_accounts=InstructionAccounts(
            from_pubkey, to_pubkey, from_pubkey, lamports
        ),
        program_id=SYSTEM_ID,
        data=data
    )
