## import class objects 
from typing import List, Dict
from AAA.user import User
from AAA.bond import Bond
from AAA.staked_AHM import Staked_AHM
from AAA.config import sim_conf

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
        self.staked_AHM = None # a staked_AHM object or Contract

    def instantiate_Users(self, number: int = 4) -> None:
        for i in range(number):
            user = User(sim_conf)
            self.users.append(user)
        return None

    def instantiate_Staked_AHM(self) -> None:
        self.staked_AHM = Staked_AHM()


    def instantiate_Bonds(self, number: int = 4) -> None:
        pass

    
    def instantiate_Simulation(self) -> None:
        self.instantiate_Users() # instantiate users and store in self.users
        self.instantiate_Staked_AHM() # instantiated & stored in self.staked_AHM
        self.staked_AHM.stake_AHM(self.users[0], 50)
        self.staked_AHM.stake_AHM(self.users[1], 100)
        self.staked_AHM.stake_AHM(self.users[2], 100)
        self.staked_AHM.stake_AHM(self.users[3], 200)
        return None

    def run(self):
        self.instantiate_Simulation()
        for i in range(10):
            self.staked_AHM.add_interest_to_balances(interest_rate=1, users=self.users)
            # print(self.users)

        # Elaspse epochs 
        # for _ in range(5):#self.configs["days"]
        #     Temporal.elapse_epoch()
        return None
