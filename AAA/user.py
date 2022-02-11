from typing import List, Dict

class User():
    """
    A user 
        - buy bond
        - redeem AHM
        - sell AHM
        - stake AHM

    """
    user_id: int = 1
    all: List = []

    def __init__(self, received_conf: Dict = {}):
        self.balances: dict() = received_conf["user_config"]["balances"]
        self.id: int = User.user_id

        User.user_id += 1
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

    def __repr__(self):
        return f'User-{self.id}: Bal={self.balances}'
