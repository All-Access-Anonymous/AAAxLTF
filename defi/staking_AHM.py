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

class Staking_AHM:
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

    def __init__(self, rebase_period: int, reward_rate: float) -> None:
        self.reward_rate = 0.2
        self.warmup_period = 0
        self.epochNumber = 0
        self.rebase_period = 1
        super().__init__()
        self.balances: dict = {} #to record all balances of sAHM

        #id management
        self.id: int = Staking_AHM.instance_number        
        Staking_AHM.instance_number += 1
        Staking_AHM.all.append(self)

    def stake_AHM(self, user: object, amount: int) -> None:
        """ 
        Stake AHM to earn interest
        """
        if user.balances['AHM'] > 0:
            if user.id in self.balances.keys():
                #debit
                user.sub_bal('AHM', amount)            
                #update sAHM in contract and in user Wallet
                self.balances[user.id]['sAHM'] += amount
                user.add_bal('sAHM', amount)
                logger.debug(f'user {user.id} successfully staked {amount} AHM ')
            else:
                #debit
                user.sub_bal('AHM', amount)            
                #update sAHM in contract and in user Wallet
                self.balances[user.id] = {
                    'sAHM': amount,
                }
                user.add_bal('sAHM', amount)
                logger.debug(f'user {user.id} successfully staked {amount} AHM ')
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

    def forfeit_sAHM(self, user: object, amount: int) -> None:
        """
        Forfeit sAHM from staking contract
        Used when user unstakes sAHM, when still in warmup period
        """
        # #debit
        # user.sub_bal('sAHM', amount)
        # #update AHM in contract and in user Wallet
        # self.balances[user.id]['sAHM'] -= amount
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

    def rebase(self, users: object, excess_reserve: float, total_sAHM: float) -> None:
        """
        Rebase sAHM into AHM
        """
        if self.epochNumber % self.rebase_period == 0:
            ##[skipped] Check if there is excess reserves backing AHM, then only mint new AHM
            ## Excess reserve in USD
            reward_amount = excess_reserve * self.reward_rate * 0.01
            self.add_rebase_rewards(reward_amount, users, total_sAHM)
            logger.info(f'{self.epochNumber} rebase')
            ##adjust from bond.py after every rebase
        else:
            pass
        return None

    def add_rebase_rewards(self, reward_amount: float, users: object, total_sAHM: float) -> None:
        """
        Add interest to all sAHM in the contract
        """
        if total_sAHM != 0:
            reward_amount_per_sOHM = reward_amount / total_sAHM
        else:
            reward_amount_per_sOHM = 0
        for k in self.balances.keys():
            to_add = self.balances[k]['sAHM'] * reward_amount_per_sOHM
            self.balances[k]['sAHM'] += to_add 
            #update balances in user wallets
            users[k-1].add_bal('sAHM', to_add)
        logger.info(f'{reward_amount} sAHM distributed as rebase')
        return None