from solathon.client import Client
from solathon.publickey import PublicKey
from solathon.core.types import Commitment
from solathon.transaction import Transaction

from typing import Optional
import httpx
import json


def fetch_transaction(client: Client, account: PublicKey, link: str, commitment: Optional[Commitment]=None) -> Transaction:
    http = httpx.Client()
    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json'
    }
    data = json.dumps({ 'account': account.byte_value })
    response = http.post(url=link, headers=headers, data=data)
    json_data = response.json()

    if json_data.get("transaction", None) == None:
        raise ValueError("Transaction not found")
    
    if not isinstance(json_data['transaction'], str):
        raise ValueError("Invalid Transaction")
    
    # TODO: Add more checks for transaction validity and return