## import class objects 
from typing import List, Dict
from AAA.user import User
from AAA.bond import Bond
from AAA.staking_AHM import Staking_AHM
from AAA.config import sim_conf
from pprint import pprint

class SimHandler:
    """
    Responsiblities:
        Instantiate Users
        Instantiate 

    """

    def __init__(self, configs: dict = {}):
        # self.config = self.load_config(configs)
        self.users = [] # all user objects
        self.bonds = [] # all bond objects
        self.staking_AHM = None # a staking_AHM object or Contract

    def instantiate_Users(self, number: int = 4) -> None:
        print('instantiate_Users')
        for i in range(number):
            user = User(sim_conf)
            self.users.append(user)
        return None

    def instantiate_Bonds(self, number: int = 1) -> None:
        print('instantiate_Bonds')
        for i in range(number):
            bond = Bond()
            self.bonds.append(bond)
        return None

    def instantiate_Staking_AHM(self) -> None:
        self.staking_AHM = Staking_AHM()
    
    def instantiate_Simulation(self) -> None:
        self.instantiate_Users() # instantiate users and store in self.users
        self.instantiate_Bonds(1) # instantiate bonds and store in self.bonds
        self.instantiate_Staking_AHM() # instantiated & stored in self.staking_AHM        
        self.staking_AHM.stake_AHM(self.users[0], 50)
        self.staking_AHM.stake_AHM(self.users[1], 100)
        self.staking_AHM.stake_AHM(self.users[2], 100)
        self.staking_AHM.stake_AHM(self.users[3], 200)
        return None

    def run(self):
        self.instantiate_Simulation()
    
        for i in range(10):
            self.staking_AHM.add_interest_to_balances(interest_rate=1, users=self.users)
            ## all users bond at epoch 1
            if i==1:
                for user in self.users:
                    self.bonds[0].deposit(user, 100)
            self.bonds[0].epochNumber += 1
            
            print('Iteration------------------------',i)
            pprint(self.users)
            print(self.bonds)

        # Elaspse epochs 
        # for _ in range(5):#self.configs["days"]
        #     Temporal.elapse_epoch()
        return None
