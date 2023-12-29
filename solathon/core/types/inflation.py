from typing import Optional, TypedDict


class InflationGovernorType(TypedDict):
    '''
    JSON Response type of Inflation Governer Information received by RPC
    '''
    foundation: float
    foundationTerm: int
    initial: float
    taper: float
    terminal: float

class InflationGovernor:
    '''
    Convert Inflation Governer Information JSON to Class
    '''
    def __init__(self, response: InflationGovernorType) -> None:
        self.foundation = response['foundation']
        self.foundation_term = response['foundationTerm']
        self.initial = response['initial']
        self.taper = response['taper']
        self.terminal = response['terminal']

class InflationRateType(TypedDict):
    '''
    JSON Response type of Inflation Rate Information received by RPC
    '''
    epoch: int
    foundation: float
    validator: float
    total: float

class InflationRate:

    def __init__(self, response: InflationRateType) -> None:
        self.epoch = response['epoch']
        self.foundation = response['foundation']
        self.validator = response['validator']
        self.total = response['total']

class InflationRewardType(TypedDict):
    '''
    JSON Response type of Inflation Reward Information received by RPC
    '''
    epoch: int
    effectiveSlot: int
    amount: int
    postBalance: int
    commission: Optional[int]

class InflationReward:
    '''
    Convert Inflation Reward Information JSON to Class
    '''
    def __init__(self, response: InflationRewardType) -> None:
        self.epoch = response['epoch']
        self.effective_slot = response['effectiveSlot']
        self.amount = response['amount']
        self.post_balance = response['postBalance']
        self.commission = response['commission']