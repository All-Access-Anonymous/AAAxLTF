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

    def __init__(self, config: Dict = {}):

        # self.balances: dict() = copy.deepcopy(config["user_config"]["balances"])
        ## WHY copy.deepcopy?
        # https://stackoverflow.com/questions/47499998/modifying-dictionary-in-one-instance-of-a-class-makes-same-change-to-all-other-i
        
        self.id: int = User.instance_number
        
        Revenue.instance_number += 1
        Revenue.all.append(self)

    def add_rewards(self, amount: int) -> None:
        """
        Add amount to asset
        """
        self.balances[asset] += amount
        return None

    def __repr__(self):
        return f'User-{self.id}: Bal={self.balances}'
