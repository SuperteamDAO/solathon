from typing import Union
from urllib.parse import parse_qs, urlparse
import re

from ..publickey import PublicKey
from ..solana_pay.types import TransactionRequestURL, TransferRequestURL


def parse_url(url: str) -> Union[TransactionRequestURL, TransferRequestURL]:
    '''
    Parses a Solana Pay transaction request URL. Returns a `TransactionRequestURL` class object.

    Args
        url (str) - A Solana Pay transaction request URL.

    Raises
        ValueError - If `url` is invalid.
    
    :rtype: solathon.solana_pay.types.TransactionRequestURL
    '''
    if len(url) > 2048:
        raise ValueError('URL Length is Invalid (Max 2048 characters)')

    parsed_url = urlparse(url)
    if parsed_url.scheme != 'solana':
        raise ValueError('Invalid Protocol, must be `solana`')

    if not parsed_url.path:
        raise ValueError('Invalid URL, path missing')

    if re.search(r'[:%]', parsed_url.path) != None:
        return parse_transaction_request_url(parsed_url.path, parsed_url.query)
    return parse_transfer_request_url(parsed_url.path, parsed_url.query)

def parse_transaction_request_url(path: str, query: str) -> TransactionRequestURL:
    transaction_url = f"{path}?{query}"
    parsed_transaction_url = urlparse(transaction_url)
    if parsed_transaction_url.scheme != 'https':
        raise ValueError('Invalid Protocol, must be `https`')

    parsed_qs = parse_qs(parsed_transaction_url.query)
    label = parsed_qs['label'][0] if 'label' in parsed_qs else None
    message = parsed_qs['message'][0] if 'message' in parsed_qs else None

    return TransactionRequestURL(link=transaction_url, label=label, message=message)
    
def parse_transfer_request_url(path: str, query: str) -> TransferRequestURL:
    recipient: PublicKey
    try:
        recipient = PublicKey(path)
    except Exception as e:
        raise ValueError('Invalid Recipient')
    parsed_qs = parse_qs(query)
    amount = parsed_qs['amount'][0] if 'amount' in parsed_qs else None
    
    if amount != None:
        if re.search(r'^\d+(\.\d+)?(e[+-]?\d+)?$', amount) is None:
            raise ValueError('Invalid Amount')
        
        amount = float(amount)
        if amount < 0:
            raise ValueError('Invalid Amount')
        
    label = parsed_qs['label'][0] if 'label' in parsed_qs else None
    message = parsed_qs['message'][0] if 'message' in parsed_qs else None
    reference = parsed_qs['reference'][0] if 'reference' in parsed_qs else None

    return TransferRequestURL(recipient=recipient, amount=amount, label=label, message=message, reference=reference)    
