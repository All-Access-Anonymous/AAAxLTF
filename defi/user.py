# Logging
import logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger.propagate = False
formatter = logging.Formatter('%(levelname)s:%(name)s::: %(message)s')
file_handler = logging.FileHandler('simulation.log')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)
#------------------------------------------------------------------------------

from typing import List, Dict
import copy

class User():
    """
    A user 
        - buy bond
        - redeem AHM
        - sell AHM
        - stake AHM

    """
    
    instance_number: int = 1
    all: List = []

    def __init__(self, init_bal: Dict = {}):
        self.balances: dict() = init_bal
        ## WHY copy.deepcopy?
        # https://stackoverflow.com/questions/47499998/modifying-dictionary-in-one-instance-of-a-class-makes-same-change-to-all-other-i
        
        self.id: int = User.instance_number
        
        User.instance_number += 1
        User.all.append(self)
        logger.info(f'User-{self.id} created')

    def sub_bal(self, asset: str, amount: int) -> None:
        """
        Subtract amount from asset
        """
        if self.balances[asset] >= amount:
            self.balances[asset] -= amount
        else:
            logger.exception(f'Not enough {asset}')
        return None            

    def add_bal(self, asset: str, amount: int) -> None:
        """
        Add amount to asset
        """
        self.balances[asset] += amount
        return None

    def __repr__(self):
        return f'User-{self.id}: Bal={self.balances}'
