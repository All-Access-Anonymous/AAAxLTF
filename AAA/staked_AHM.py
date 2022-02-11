from typing import List, Dict

class Staked_AHM():
    """
    A staked_AHM earns the rebase rewards on top of the treasury balance
    https://www.jordanmmck.com/crypto/olympus-dao?s=09
        

    """
    id: int = 0
    all: List = []

    def __init__(self):
        self.balances: dict() = {}
        Staked_AHM.id += 1
        Staked_AHM.all.append(self)

    def stake_AHM(self, user: object(), amount: int) -> None:
        """ 
        Stake AHM to earn interest
        """
        if user.id in self.balances.keys():
            #debit
            user.balances['AHM'] -= amount
            print('debited {} AHM from user {}'.format(amount, user.id))
            
            #update sAHM in contract and in user Wallet
            self.balances[user.id]['sAHM'] += amount
            user.balances['sAHM'] += amount
            print('Issued {} sAHM'.format(amount))
        else:
            #debit
            user.balances['AHM'] -= amount
            print('debited {} AHM from user {}'.format(amount, user.id))

            #update sAHM in contract and in user Wallet
            self.balances[user.id] = {
                'sAHM': amount,
            }
            user.balances['sAHM'] += amount
            print('Issued {} sAHM'.format(amount))
        return None

    def get_total_sAHM(self) -> int:
        sum=0
        bals = self.balances
        for i in bals:
            sum += bals[i]['sAHM']
        return sum

    def __repr__(self):
        return f'staked_AHM-{self.id}: total sAHM ={self.get_total_sAHM()}'
