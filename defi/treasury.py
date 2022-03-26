# Logging
import logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger.propagate = False
formatter = logging.Formatter('%(levelname)s:%(name)s     %(message)s')
file_handler = logging.FileHandler('simulation.log')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)
#------------------------------------------------------------------------------

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
        # Deposit 90,000 DAI to treasury, 6,000 AHM gets minted to deployer and 84,000 are in treasury as excesss reserves
        self.balances: dict() = {'DAI': 90000, 'AHM': 0}    #update according the minter balance
        self.ratio: dict() = {
            'reserve': 0.2,
            'lp': 0.6,
            'lend': 0.2
        }
        self.id: int = Treasury.instance_number

        Treasury.instance_number += 1
        Treasury.all.append(self)

        logger.info(msg=f'Treasury-{self.id} created')



    def __repr__(self):
        return f'Treasury-{self.id}'
