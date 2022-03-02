from typing import List, Dict
from AAA.temporal import Temporal

class Staking_AHM(Temporal):
    """

    Is a staking contract where users can stake AHM to earn rebase rewards.
    Users can stake AHM and they receive equivalent sAHM as a receipt of staking.

    Unstaking is generally without the warmup period, however it can be programmed
    to be with the warmup period. Warmup period is a period of time until a user
    can unstake their sAHM.

    The rebase rewards are paid from the treasury.
    https://www.jordanmmck.com/crypto/olympus-dao?s=09
        
    """
    instance_number: int = 1
    all: List = []

    def __init__(self):
        super().__init__()
        self.balances: dict = {} #to record all balances of sAHM
        self._epochs_elapsed: int = 0 #For Sim
        #id management
        self.id: int = Staking_AHM.instance_number        
        Staking_AHM.instance_number += 1
        Staking_AHM.all.append(self)

    def stake_AHM(self, user: object, amount: int) -> None:
        """ 
        Stake AHM to earn interest
        """
        if user.id in self.balances.keys():
            #debit
            user.sub_bal('AHM', amount)            
            #update sAHM in contract and in user Wallet
            self.balances[user.id]['sAHM'] += amount
            user.add_bal('sAHM', amount)
            print(f'user {user.id} successfully staked {amount} AHM ')
        else:
            #debit
            user.sub_bal('AHM', amount)            
            #update sAHM in contract and in user Wallet
            self.balances[user.id] = {
                'sAHM': amount,
            }
            user.add_bal('sAHM', amount)
            print(f'user {user.id} successfully staked {amount} AHM ')
        return None

    def unstake_AHM(self, user: object, amount: int) -> None:
        """
        Redeem AHM from staking contract
        """
        #debit
        user.sub_bal('sAHM', amount)
        #update AHM in contract and in user Wallet
        self.balances[user.id]['sAHM'] -= amount
        user.add_bal('AHM', amount)
        return None

    def get_total_sAHM(self) -> int:
        """
        Get total sAHM minted or in circulation
        """
        sum=0
        bals = self.balances
        for i in bals:
            sum += bals[i]['sAHM']
        return sum

    def __repr__(self):
        return f'staking_AHM-{self.id}: total sAHM ={self.get_total_sAHM()}'

    def add_interest_to_balances(self, interest_rate: float, users:list) -> None:
        """
        Add interest to all sAHM in the contract
        """
        for k in self.balances.keys():
            to_add = self.balances[k]['sAHM'] * interest_rate * 0.01
            self.balances[k]['sAHM'] += to_add 
            #update balances in user wallets
            users[k-1].add_bal('sAHM', to_add)
        return None

    def run_epoch(self) -> None:
        """
        Inherited from Temporal ABC
        This will be called by Temporal to initiate
        this instance's daily routines / responsibilities.
        """
        self._epochs_elapsed += 1
        self.epoch_assess()
    
    def epoch_assess(self) -> None:
        """
        day_assess contains the daily responsibilities
        assigned to each instance of this class.
        """
        self.add_interest_to_balances(interest_rate=1)# 1 percent

    @property
    def epochs_elapsed(self):
        """
        Inherited from Temporal ABC.
        Returns the days elapsed for this object but
        without needing to call this as a function.
        """
        return self._epochs_elapsed