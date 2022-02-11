# https://github.com/OlympusDAO/olympus-contracts/blob/Version-1.1/contracts/Treasury.sol
from typing import List, Dict

class Treasury():
    """
    A Treasury has following baskets: 
        - non LP bonds
        - LP bonds
        

    """
    id: int = 0
    all: List = []

    def __init__(self, received_conf: Dict = {}):
        self.balances: dict() = received_conf["treasury_config"]["staked_native_assets"]
        self.id: int = Treasury.id

        Treasury.id += 1
        Treasury.all.append(self)

    def buy_bond(self, asset: str, amount: int) -> None:
        pass

    def redeem_AHM(self, amount: int) -> None:
        pass

    def sell_AHM(self, amount: int) -> None:
        pass

    def stake_AHM(self, amount: int) -> None:
        """ 
        Stake AHM to earn interest
        """
        print('deposited {} AHM to and issuing equivalent sAHM'.format(amount))
        ## deposit to treasury
        self.balances['sAHM'] += amount
        self.balances['sAHM'] += amount
        pass

    def __repr__(self):
        return f'Treasury-{self.id}: Bal={self.balances}'
