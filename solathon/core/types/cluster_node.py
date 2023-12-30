from typing import Optional, TypedDict

class ClusterNodeType(TypedDict):
    '''
    JSON Response type of Cluster Node Information received by RPC
    '''
    pubkey: str
    gossip: Optional[str]
    tpu: Optional[str]
    rpc: Optional[str]
    version: Optional[str]
    featureSet: Optional[int]
    shredVersion: Optional[int]

class ClusterNode:
    '''
    Convert Cluster Node Information JSON to Class
    '''
    def __init__(self, response: ClusterNodeType) -> None:
        self.pubkey = response['pubkey']
        self.gossip = response['gossip']
        self.tpu = response['tpu']
        self.rpc = response['rpc']
        self.version = response['version']
        self.feature_set = response['featureSet']
        self.shred_version = response['shredVersion']