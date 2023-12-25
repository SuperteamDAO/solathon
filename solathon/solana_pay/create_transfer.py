from typing import Optional
from solathon.client import Client
from solathon.core.instructions import AccountMeta, transfer
from solathon.core.types import Commitment
from solathon.publickey import PublicKey
from solathon.solana_pay.types import CreateTransferFields
from solathon.transaction import Transaction
from solathon.utils import sol_to_lamport


def create_transfer(client: Client,  sender: PublicKey, transfer_fields: CreateTransferFields, commitment: Optional[Commitment]=None) -> Transaction:
    sender_info = client.get_account_info(sender)
    if sender_info['result']['value'] == None:
        raise ValueError("Sender account does not exist")
    
    if transfer_fields.get("recipient", None) == None:
        raise ValueError("Recipient is missing from transfer_fields")

    if transfer_fields.get("amount", None) == None:
        raise ValueError("Amount is missing from transfer_fields")
    lamports = sol_to_lamport(transfer_fields['amount'])
    
    if lamports > sender_info['result']['value']['lamports']:
        raise ValueError("Insufficient funds in sender account")

    instruction = transfer(from_public_key=sender, to_public_key=transfer_fields['recipient'], lamports=lamports)

    if transfer_fields.get("references", None) != None:
        for ref in transfer_fields['references']:
            acc_ref = AccountMeta(
                public_key=ref,
                is_signer=False,
                is_writable=False
            )
            instruction.keys.append(acc_ref)
    
    block_hash = client.get_recent_blockhash(commitment=commitment)
    if block_hash['result']['value'] == None:
        raise ValueError("No recent blockhash found")
    transaction = Transaction(instructions=[instruction], signers=[sender], fee_payer=sender,recent_blockhash=block_hash['result']['value']['blockhash'])

    return transaction

