# https://github.com/OlympusDAO/olympus-contracts/blob/Version-1.1/contracts/Treasury.sol
from typing import List, Dict

class Treasury():
    """
    A Treasury has following baskets: 
        - non LP bonds
        - LP bonds


    """
    instance_number: int = 1
    all: List = []

    def __init__(self, received_conf: Dict = {}):
        self.balances: dict() = received_conf["treasury_config"]["staked_native_assets"]
        
        
        self.id: int = Treasury.instance_number

        Treasury.instance_number += 1
        Treasury.all.append(self)

    def __repr__(self):
        return f'Treasury-{self.id}: Bal={self.balances}'
