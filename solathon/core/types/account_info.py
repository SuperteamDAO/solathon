from typing import Any, TypedDict, Union

class AccountInfoType(TypedDict):
    '''
    JSON Response type of Account Information received by RPC
    '''
    lamports: int
    owner: str
    executable: bool
    rentEpoch: int
    size: int
    data: Union[str, dict[str, Any]]

class AccountInfo():
    '''
    Convert Account Information JSON to Class
    '''
    def __init__(self, result: AccountInfoType) -> None:
        self.lamports = result['lamports']
        self.owner = result['owner']
        self.executable = result['executable']
        self.rent_epoch = result['rentEpoch']
        self.size = result['size']
        self.data = result['data']