from solathon.client import Client
from solathon.core.types.block import BlockHash, BlockHashType
from solathon.publickey import PublicKey
from solathon.core.types import Commitment, RPCResponse
from solathon.transaction import Transaction

from typing import Optional
from nacl.signing import VerifyKey
from nacl.exceptions import BadSignatureError
import httpx
import json


def fetch_transaction(client: Client, account: PublicKey, link: str, commitment: Optional[Commitment] = None) -> Transaction:
    '''
    Fetches a transaction from a Solana Pay transaction link.

    Args
        client (Client) - A connection client to the cluster.
        account (PublicKey) - Account that may sign the transaction.
        link (str) - [Solana Pay Spec](https://github.com/solana-labs/solana-pay/blob/master/SPEC.md#link) link to fetch the transaction from.
        commitment (Commitment, optional) - commitment option for `getRecentBlockhash`.

    Raises
        ValueError - If `transaction` is not found in the response.
    
    :type client: solathon.client.Client
    :type account: solathon.publickey.PublicKey
    :type commitment: solathon.core.types.Commitment
    :rtype: solathon.transaction.Transaction
    '''
    http = httpx.Client()
    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json'
    }
    data = json.dumps({'account': account.byte_value})
    response = http.post(url=link, headers=headers, data=data)
    json_data = response.json()

    if json_data.get("transaction", None) == None:
        raise ValueError("Transaction not found")

    if not isinstance(json_data['transaction'], str):
        raise ValueError("Invalid Transaction")

    transaction: Transaction = Transaction.from_buffer(
        bytes.fromhex(json_data['transaction']))

    if len(transaction.signatures):
        if transaction.fee_payer == None:
            raise ValueError("Transaction Fee payer missing")

        if transaction.fee_payer == transaction.signatures[0].public_key:
            raise ValueError("Invalid Fee payer")

        if transaction.recent_blockhash == None:
            raise ValueError("Transaction recent blockhash missing")

        message = transaction.serialize()
        for signature in transaction.signatures:
            if signature.signature:
                public_key = VerifyKey(signature.public_key)
                try:
                    public_key.verify(signature.signature)
                except BadSignatureError:
                    raise ValueError("Invalid Signature")
            elif signature.public_key == account:
                if len(transaction.signatures) == 1:
                    if client.clean_response == False:
                        raw_blockhash: RPCResponse[BlockHashType] = client.get_recent_blockhash(
                            commitment=commitment)
                        transaction.recent_blockhash = BlockHash(
                            raw_blockhash['result']['value']).blockhash
                    else:
                        transaction.recent_blockhash = client.get_recent_blockhash(
                            commitment=commitment).blockhash
            else:
                raise ValueError("Missing Signature")
    else:
        transaction.fee_payer = account
        if client.clean_response == False:
            raw_blockhash: RPCResponse[BlockHashType] = client.get_recent_blockhash(
                commitment=commitment)
            transaction.recent_blockhash = BlockHash(
                raw_blockhash['result']['value']).blockhash
        else:
            transaction.recent_blockhash = client.get_recent_blockhash(
                commitment=commitment).blockhash

    return transaction
