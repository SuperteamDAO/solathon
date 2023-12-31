from urllib.parse import parse_qs, urlparse, unquote
from solathon.solana_pay.types import TransactionRequestURL

def parse_url(url: str) -> TransactionRequestURL:
    '''
    Parses a Solana Pay transaction request URL. Returns a `TransactionRequestURL` class object.

    Args
        url (str) - A Solana Pay transaction request URL.
    
    Raises
        ValueError - If `url` is invalid.
    '''
    if len(url) > 2048:
        raise ValueError('URL Length is Invalid (Max 2048 characters)')
    
    parsed_url = urlparse(url)
    if parsed_url.scheme != 'solana':
        raise ValueError('Invalid Protocol, must be `solana`')
    
    if not parsed_url.path:
        raise ValueError('Invalid URL, path missing')
    
    transaction_url = unquote(parsed_url.path)
    parsed_transaction_url = urlparse(transaction_url)
    if parsed_transaction_url.scheme != 'https':
        raise ValueError('Invalid Protocol, must be `https`')
    
    parsed_qs = parse_qs(parsed_transaction_url.query)
    label = parsed_qs['label'][0] if 'label' in parsed_qs else None
    message = parsed_qs['message'][0] if 'message' in parsed_qs else None

    return TransactionRequestURL(link=transaction_url, label=label, message=message)

    

    
