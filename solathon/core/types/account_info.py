from typing import Any, TypedDict, Union

class AccountInfoType(TypedDict):
    '''
    JSON Response type of Account Information received by RPC
    '''
    lamports: int
    owner: str
    executable: bool
    rentEpoch: int
    size: Union[int, None]
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
        self.size = result.get('size', None)
        self.data = result['data']

class ProgramAccountType(TypedDict):
    '''
    JSON Response type of Program Account Information received by RPC
    '''
    pubkey: str
    account: AccountInfoType

class ProgramAccount:
    '''
    Convert Program Account Information JSON to Class
    '''
    def __init__(self, result: ProgramAccountType) -> None:
        self.pubkey = result['pubkey']
        self.account = AccountInfo(result['account'])
