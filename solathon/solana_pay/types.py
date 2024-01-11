from solathon.publickey import PublicKey
from dataclasses import dataclass
from typing import List, TypedDict, Optional, Union


class CreateTransferFields(TypedDict):
    """
    Parameters for creating a transfer

    Args
        recipient (PublicKey) - Account that will receive the transfer.
        amount (float) - Amount to be transferred in Sol.
        reference (List[PublicKey], optional) - List of accounts to be referenced in the transfer.
    """

    recipient: PublicKey
    amount: float
    reference: Optional[Union[List[PublicKey], PublicKey]]
    # memo: Optional[str]


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
    # memo: Optional[str]
    reference: Optional[Union[List[str], str]]
