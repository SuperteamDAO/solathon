from typing import List
from ..core.types import TransactionSignature
from ..client import Client
from ..publickey import PublicKey

def find_reference(client: Client, reference: PublicKey) -> TransactionSignature:
    '''
    Finds the oldest signature for a reference account.

    Args
        client (Client) - A connection client to the cluster.
        reference (PublicKey) - Account that will be referenced to check for signature.

    Raises
        ValueError - If `reference` is not found in the response.

    :type client: solathon.client.Client
    :type reference: solathon.publickey.PublicKey
    :rtype: solathon.core.types.TransactionSignature
    '''

    signatures: List[TransactionSignature] = []
    if client.clean_response == False:
        raw_signatures = client.get_signatures_for_address(str(reference))
        signatures = [TransactionSignature(signature)
                      for signature in raw_signatures]
    else:
        signatures = client.get_signatures_for_address(str(reference))

    if len(signatures) == 0:
        raise ValueError("Reference not found")

    oldest = signatures[-1]
    return oldest
