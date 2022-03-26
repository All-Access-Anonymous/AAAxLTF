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

from typing import List, Dict
import copy

class Revenue():
    """
    This classes manages revenue stream for the treasury
    Two types of revenue streams:
        1. LP rewards
        2. Fiat Loan Revenue

    """
    instance_number: int = 1
    all: List = []

    def __init__(self):

        # self.balances: dict() = copy.deepcopy(config["user_config"]["balances"])
        ## WHY copy.deepcopy?
        # https://stackoverflow.com/questions/47499998/modifying-dictionary-in-one-instance-of-a-class-makes-same-change-to-all-other-i
        
        self.id: int = Revenue.instance_number
        
        Revenue.instance_number += 1
        Revenue.all.append(self)

    def add_lp_reward(self, treasury_obj: object, apy:int) -> None:
        """
        Add reward to LP ratio of tresaury
        inupt:
            treasury_obj: Treasury object
            apy: int
        """
        treasury_obj.balances['DAI'] += treasury_obj.balances['DAI'] *\
            treasury_obj.ratio['lp'] * (apy/(100*365))
        logger.info(f'LP reward updated to Treasury')
        return None

    def add_interest_from_fiat_loan(self, treasury_obj: object, apy:int) -> None:
        """
        Add amount to asset
        """
        treasury_obj.balances['DAI'] += treasury_obj.balances['DAI'] *\
            treasury_obj.ratio['lend'] * (apy/(100*365))
        logging.info(f'Interest from fiat loan updated to Treasury')
        return None

    ## staking rewards are accrued at frequency of EMI payout from Vendor
    ## staking rewards from vendor revenue are awarded seperately from pool rewards

    def __repr__(self):
        return f'User-{self.id}: Bal={self.balances}'
