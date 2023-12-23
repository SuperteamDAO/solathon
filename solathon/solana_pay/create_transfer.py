from solathon.client import Client
from solathon.publickey import PublicKey
from solathon.solana_pay.types import CreateTransferFields


def create_transfer(client: Client,  sender: PublicKey, transfer_fields: CreateTransferFields):
    sender_info = client.get_account_info(sender)
    
    recipient_info = client.get_account_info(transfer_fields['recipient'])

    


