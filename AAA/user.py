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

    def __init__(self, config: Dict = {}):
        self.balances: dict() = copy.deepcopy(config["user_config"]["balances"])
        ## WHY copy.deepcopy?
        # https://stackoverflow.com/questions/47499998/modifying-dictionary-in-one-instance-of-a-class-makes-same-change-to-all-other-i
        
        self.id: int = User.instance_number
        
        User.instance_number += 1
        User.all.append(self)

    # def buy_bond(self, asset: str, amount: int) -> None:
    #     pass

    # def redeem_AHM(self, amount: int) -> None:
    #     pass

    # def sell_AHM(self, amount: int) -> None:
    #     pass

    # def stake_AHM(self, amount: int) -> None:
    #     """ 
    #     Stake AHM to earn interest
    #     """
    #     pass

    def sub_bal(self, asset: str, amount: int) -> None:
        """
        Subtract amount from asset
        """
        if self.balances[asset] >= amount:
            self.balances[asset] -= amount
        else:
            raise Exception(f'Not enough {asset}')
        return None

    def add_bal(self, asset: str, amount: int) -> None:
        """
        Add amount to asset
        """
        self.balances[asset] += amount
        return None

    def __repr__(self):
        return f'User-{self.id}: Bal={self.balances}'
