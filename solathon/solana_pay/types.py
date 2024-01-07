from publickey import PublicKey

from dataclasses import dataclass
from typing import List, TypedDict, Optional, Union


class CreateTransferFields(TypedDict):
    """
    Parameters for creating a transfer

    Args
        sender (str) - Account that will send the transfer.
        recipient (PublicKey) - Account that will receive the transfer.
        amount (int) - Amount to be transferred in Sol.
        references (List[PublicKey], optional) - List of accounts to be referenced in the transfer.
        memo (str, optional) - Memo to be included in the transfer.
    """

    sender: str
    recipient: PublicKey
    amount: int
    references: Optional[Union[List[PublicKey], PublicKey]]
    memo: Optional[str]


@dataclass
class TransactionRequestURL():
    link: str
    label: Optional[str]
    message: Optional[str]

@dataclass
class TransferRequestURL():
    recipient: str
    amount: Optional[float]
    label: Optional[str]
    message: Optional[str]
    memo: Optional[str]
    reference: Optional[Union[List[str], str]]