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
        # Deposit 9,000,000 DAI to treasury, 600,000 AHM gets minted to deployer and 8,400,000 are in treasury as excesss reserves
        self.balances: dict() = {'DAI': 9000, 'AHM': 0}
        self.ratio: dict() = {
            'reserve': 0.2,
            'lp': 0.6,
            'lend': 0.2
        }
        self.id: int = Treasury.instance_number

        Treasury.instance_number += 1
        Treasury.all.append(self)



    def __repr__(self):
        return f'Treasury-{self.id}: Bal={self.balances}'
