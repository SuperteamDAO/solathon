from dataclasses import dataclass
from typing import List, TypedDict, Optional, Union
from solathon.publickey import PublicKey


class CreateTransferFields(TypedDict):
    """
    Parameters for creating a transfer

    Args
        sender (str) - Account that will send the transfer.
        recipient (PublicKey) - Account that will receive the transfer.
        amount (int) - Amount to be transferred in Sol.
        spl_token (PublicKey, optional) - SPL token account to transfer from.
        references (List[PublicKey], optional) - List of accounts to be referenced in the transfer.
        memo (str, optional) - Memo to be included in the transfer.
    """

    sender: str
    recipient: PublicKey
    amount: int
    spl_token: Optional[PublicKey]
    references: Optional[Union[List[PublicKey], PublicKey]]
    memo: Optional[str]

@dataclass
class TransactionRequestURL():
    link: str
    label: Optional[str]
    message: Optional[str]

