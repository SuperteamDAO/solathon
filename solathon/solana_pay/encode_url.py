from typing import List, Optional, TypedDict, Union
from urllib.parse import urlencode, urlparse, urlunparse

class TransactionRequestURLParams(TypedDict):
    link: str
    label: Optional[str]
    message: Optional[str]

class TransferRequestURLParams(TypedDict):
    recipient: str
    amount: Optional[float]
    label: Optional[str]
    message: Optional[str]
    memo: Optional[str]
    reference: Optional[Union[List[str], str]]


def encode_url(data: Union[TransactionRequestURLParams, TransferRequestURLParams]) -> str:
    """
    Field parameters for creating a transaction request URL

    Args
        data (TransactionRequestURLParams | TransferRequestURLParams) - data to encode into a transaction request URL
        TransactionRequestURLParams:
            link (str) - link to a transaction
            label (str, optional) - label for the transaction
            message (str, optional) - message for the transaction

        TransferRequestURLParams:
            recipient (str) - recipient of the transfer
            amount (float, optional) - amount of the transfer
            label (str, optional) - label for the transfer
            message (str, optional) - message for the transfer
            memo (str, optional) - memo for the transfer
            reference (str, optional) - reference for the transfer
    """

    if data.get("link", None) != None:
        return encode_transaction_request_url(data["link"], data.get("label", None), data.get("message", None))
    if data.get("recipient", None) == None:
        raise ValueError("Recipient is missing from data")
    return encode_transfer_request_url(data["recipient"], data.get("amount", None), data.get("label", None), data.get("message", None), data.get("memo", None), data.get("reference", None))

def encode_transaction_request_url(link: str, label: Optional[str], message: Optional[str]) -> str:
    parsed_url = urlparse(link)
    pathname = (
        urlencode(
            parsed_url.path) if parsed_url.query else parsed_url.path.rstrip("/")
    )
    params = {}
    if label:
        params['label'] = label

    if message:
        params['message'] = message

    encoded_params = urlencode(params)
    url = urlunparse((parsed_url.scheme, parsed_url.netloc, pathname, parsed_url.params,
                     f"{parsed_url.query}&{encoded_params}", parsed_url.fragment))

    return f"solana:{url}"

def encode_transfer_request_url(recipient: str, amount: Optional[float], label: Optional[str], message: Optional[str], memo: Optional[str], reference: Optional[Union[List[str], str]]) -> str:
    params = {}

    if amount:
        params['amount'] = amount

    if label:
        params['label'] = label

    if message:
        params['message'] = message

    if memo:
        params['memo'] = memo

    if reference:
        if isinstance(reference, list):
            params['reference'] = []
            for ref in reference:
                params['reference'].append(ref)
        else:
            params['reference'] = reference

    encoded_params = urlencode(params)
    return f"solana:{recipient}?{encoded_params}"
