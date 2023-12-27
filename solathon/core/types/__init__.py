from .account_info import AccountInfo, AccountInfoType
from .block import Block, BlockType, BlockProduction, BlockProductionType, BlockCommitment, BlockCommitmentType
from .cluster_node import ClusterNode, ClusterNodeType
from .epoch import Epoch, EpochType, EpochSchedule, EpochScheduleType
from .inflation import InflationGovernor, InflationGovernorType, InflationRate, InflationRateType, InflationReward, InflationRewardType
from typing import Generic, TypeVar, TypedDict, Literal, Any, Union

T = TypeVar('T')

class RPCErrorType(TypedDict):
    '''
    JSON Response type of RPC Error
    '''
    status_code: int
    message: str

class RPCError():
    '''
    Convert RPC Error JSON to Class
    '''

    def __init__(self, error: RPCErrorType):
        self.status_code = error['status_code']
        self.message = error['message']


class Context(TypedDict):
    slot: int
    apiVersion: int

class Result(Generic[T], TypedDict):
    context: Context
    value: Union[T, None]

class RPCResponse(Generic[T], TypedDict):
    jsonrpc: Literal["2.0"]
    id: int
    result: Union[Result[T], T]
    error: RPCErrorType

class FeeCalculator(TypedDict):
    lamportsPerSignature: int

class BlockHash(TypedDict):
    blockhash: str
    feeCalculator: FeeCalculator

Commitment = Literal["processed", "confirmed", "finalized", "recent", "single", "singleGossip", "root", "max"]

class PubKeyIdentityType(TypedDict):
    '''
    JSON Response type of PubKey Identity received by RPC
    '''
    identity: str

class PubKeyIdentity:
    '''
    Convert PubKey Identity JSON to Class
    '''

    def __init__(self, response: PubKeyIdentityType) -> None:
        self.identity = response['identity']

class LargestAccountsType(TypedDict):
    '''
    JSON Response type of Largest Accounts received by RPC
    '''
    lamports: int
    address: str

class LargestAccounts:
    '''
    Convert Largest Accounts JSON to Class
    '''
    def __init__(self, response: LargestAccountsType) -> None:
        self.lamports = response['lamports']
        self.address = response['address']