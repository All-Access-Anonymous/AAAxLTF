from typing import List, Dict

class Staked_AHM():
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
        self.balances: dict = {} #to record all balances of sAHM

        #id management
        self.id: int = Staked_AHM.instance_number        
        Staked_AHM.instance_number += 1
        Staked_AHM.all.append(self)

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
        return f'staked_AHM-{self.id}: total sAHM ={self.get_total_sAHM()}'