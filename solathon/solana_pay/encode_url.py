from typing import Optional
from urllib.parse import urlencode, urlparse

def encode_url(link: str, label: Optional[str], message: Optional[str]) -> str:
    """
    Field parameters for creating a transaction request URL

    Args
        link (str) - [Solana Pay Spec](https://github.com/solana-labs/solana-pay/blob/master/SPEC.md#link) link to encode.
        label (str, optional) - Label for the transaction request URL.
        message (str, optional) - Message to be included in the transaction request URL.

    """

    parsed_url = urlparse(link)
    pathname = (
        urlencode(parsed_url.path) if parsed_url.query else parsed_url.path.rstrip("/")
    )

    url = urlparse(f"solana:{pathname}")
    if label:
        url = url._replace(query=f'label={label}&{url.query}')

    if message:
        url = url._replace(query=f'message={message}&{url.query}')

    return url.geturl()
