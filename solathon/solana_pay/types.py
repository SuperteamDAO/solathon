from typing import List, TypedDict, Optional, Union
from solathon.publickey import PublicKey


class CreateTransferFields(TypedDict):
    """
    Parameters for creating a transfer
    """

    sender: str
    recipient: PublicKey
    amount: int
    spl_token: Optional[PublicKey]
    references: Optional[Union[List[PublicKey], PublicKey]]
    memo: Optional[str]