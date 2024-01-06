from solathon.core.message import Message as CoreMessage, MessageHeader
from typing import Any, List, TypedDict, Union

class HeaderType(TypedDict):
    '''
    JSON Response type of Header Information received by RPC
    '''
    numReadonlySignedAccounts: int
    numReadonlyUnsignedAccounts: int
    numRequiredSignatures: int

class Header:

    def __init__(self, response: HeaderType) -> None:
        self.num_readonly_signed_accounts = response['numReadonlySignedAccounts']
        self.num_readonly_unsigned_accounts = response['numReadonlyUnsignedAccounts']
        self.num_required_signatures = response['numRequiredSignatures']

class InstructionType(TypedDict):
    '''
    JSON Response type of Instruction Information received by RPC
    '''
    accounts: List[int]
    data: str
    programIdIndex: int

class Instruction:
    '''
    Convert Instruction JSON to Class
    '''
    def __init__(self, response: InstructionType) -> None:
        self.accounts = response['accounts']
        self.data = response['data']
        self.program_id_index = response['programIdIndex']

class MessageType(TypedDict):
    '''
    JSON Response type of Message Information received by RPC
    '''
    accountKeys: List[str]
    header: HeaderType
    instructions: List[InstructionType]
    recentBlockhash: str

class Message:
    '''
    Convert Message JSON to Class
    '''
    def __init__(self, response: MessageType) -> None:
        self.account_keys = response['accountKeys']
        header = Header(response['header'])
        self.header = MessageHeader(
            num_required_signatures=header.num_required_signatures,
            num_readonly_signed_accounts=header.num_readonly_signed_accounts,
            num_readonly_unsigned_accounts=header.num_readonly_unsigned_accounts
        )
        self.instructions = [Instruction(instruction) for instruction in response['instructions']]
        self.recent_blockhash = response['recentBlockhash']


class TransactionType(TypedDict):
    '''
    JSON Response type of Transaction Information received by RPC
    '''
    message: MessageType
    signatures: List[str]

class Transaction:
    '''
    Convert Transaction JSON to Class
    '''
    def __init__(self, response: TransactionType) -> None:
        message = Message(response['message'])
        self.message = CoreMessage(
            header=message.header,
            account_keys=message.account_keys,
            instructions=message.instructions,
            recent_blockhash=message.recent_blockhash
        )
        self.signatures = response['signatures']

class MetaType(TypedDict):
    '''
    JSON Response type of Meta Information received by RPC
    '''
    err: Union[Any, None]
    fee: int
    innerInstructions: List[Any]
    logMessages: List[Any]
    postBalances: List[int]
    postTokenBalances: List[Any]
    preBalances: List[int]
    preTokenBalances: List[Any]
    rewards: Union[Any, None]

class Meta:
    '''
    Convert Meta JSON to Class
    '''
    def __init__(self, response: MetaType) -> None:
        self.err = response['err']
        self.fee = response['fee']
        self.inner_instructions = response['innerInstructions']
        self.log_messages = response['logMessages']
        self.post_balances = response['postBalances']
        self.post_token_balances = response['postTokenBalances']
        self.pre_balances = response['preBalances']
        self.pre_token_balances = response['preTokenBalances']
        self.rewards = response['rewards']

class TransactionElementType(TypedDict):
    '''
    JSON Response type of Transaction Information received by RPC
    '''
    meta: MetaType
    transaction: TransactionType

class TransactionElement:
    '''
    Convert Transaction JSON to Class
    '''
    def __init__(self, response: TransactionElementType) -> None:
        self.meta = Meta(response['meta'])
        self.transaction = Transaction(response['transaction'])

class BlockType(TypedDict):
    '''
    JSON Response type of Block Information received by RPC
    '''
    blockHeight: int
    blockTime: None
    blockhash: str
    parentSlot: int
    previousBlockhash: str
    transactions: List[TransactionElementType]

class Block:
    '''
    Convert Block JSON to Class
    '''

    def __init__(self, response: BlockType) -> None:
        self.block_height = response['block_height']
        self.block_time = response['block_time']
        self.blockhash = response['blockhash']
        self.parent_slot = response['parent_slot']
        self.previous_blockhash = response['previous_blockhash']
        self.transactions = [TransactionElement(transaction) for transaction in response['transactions']]

class RangeType(TypedDict):
    '''
    JSON Response type of Range Information received by RPC
    '''
    firstSlot: int
    lastSlot: int

class Range:
    '''
    Convert Range JSON to Class
    '''
    def __init__(self, response: RangeType) -> None:
        self.first_slot = response['firstSlot']
        self.last_slot = response['lastSlot']

class BlockProductionType(TypedDict):
    '''
    JSON Response type of Block Production Information received by RPC
    '''
    byIdentity: dict[str, Any]
    range: RangeType

class BlockProduction:
    '''
    Convert Block Production JSON to Class
    '''
    def __init__(self, response: BlockProductionType) -> None:
        self.by_identity = response['byIdentity']
        self.range = Range(response['range'])

class BlockCommitmentType(TypedDict):
    '''
    JSON Response type of Block Commitment Information received by RPC
    '''
    commitment: List[int]
    totalStake: int

class BlockCommitment:
    '''
    Convert Block Commitment JSON to Class
    '''
    
    def __init__(self, response: BlockCommitmentType) -> None:
        self.commitment = response['commitment']
        self.total_stake = response['totalStake']

class FeeCalculatorType(TypedDict):
    '''
    JSON Response type of Fee Calculator Information received by RPC
    '''
    lamportsPerSignature: int

class BlockHashType(TypedDict):
    '''
    JSON Response type of Block Hash Information received by RPC
    '''
    blockhash: str
    feeCalculator: FeeCalculatorType

class FeeCalculator:
    '''
    Convert Fee Calculator JSON to Class
    '''

    def __init__(self, response: FeeCalculatorType) -> None:
        self.lamports_per_signature = response['lamportsPerSignature']

class BlockHash:
    '''
    Convert Block Hash JSON to Class
    '''
    def __init__(self, response: BlockHashType) -> None:
        self.blockhash = response['blockhash']
        self.fee_calculator = FeeCalculator(response['feeCalculator'])