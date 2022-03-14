## import class objects 
from typing import List, Dict
from AAA.user import User
from AAA.bond import Bond
from AAA.revenue import Revenue
from AAA.staking_AHM import Staking_AHM
from AAA.config import sim_conf
from pprint import pprint
import pandas as pd
import plotly.express as px
import copy

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
        print(f'instantiating {number} Users')
        for i in range(number):
            user = User(sim_conf)
            self.users.append(user)
        return None

    def instantiate_Bonds(self, number: int = 1) -> None:
        print(f'instantiate {number} Bonds')
        for i in range(number):
            bond = Bond()
            self.bonds.append(bond)
        return None

    def instantiate_Staking_AHM(self) -> None:
        self.staking_AHM = Staking_AHM()
    
    def instantiate_Simulation(self) -> pd.DataFrame:
        self.instantiate_Users(5) # instantiate users and store in self.users
        self.instantiate_Bonds(1) # instantiate bonds and store in self.bonds
        self.instantiate_Staking_AHM() # instantiated & stored in self.staking_AHM        
        # self.staking_AHM.stake_AHM(self.users[0], 50)
        # self.staking_AHM.stake_AHM(self.users[1], 100)
        # self.staking_AHM.stake_AHM(self.users[2], 100)
        # self.staking_AHM.stake_AHM(self.users[3], 200)
        return None

    def run(self):
        self.instantiate_Simulation()
        ## paramteer to record every epoch
        totalDebt = []
        treasury_balance = []
        DAO_balance = []
        user_balance = []
        total_sAHM = []
        total_AHM = []
        #dfa
        adjustments = []
        current_debt = []
        total_supply = []   # AHM supply
        bond_price = [] #USD
        bcv = [] 


        for i in range(60):
            print('Epoch------------------------',i,'------------------------------')
            self.staking_AHM.add_interest_to_balances(interest_rate=1, users=self.users)

            ## all users bond at epoch 1
            if i%7 == 0:
                for user in self.users:
                    self.bonds[0].deposit(user, 100)
                print('all users bond')
                print(self.bonds)
    
            ## epoch routine
            # update total AHM balance from users
            self.bonds[0].sum_AHM_users = sum(
                [i.balances['AHM'] + i.balances['sAHM'] for i in self.users])
        
            ## All user Redeem
            # all users redeem claimable bonds
            self.bonds[0].redeem(self.users)

            ## - all users stake AHM
            # all users stake redeemed bonds
            for user in self.users:
                self.staking_AHM.stake_AHM(user, user.balances['AHM'])
            
            pprint(self.users)
            ## update epoch
            self.bonds[0].epochNumber += 1
            self.staking_AHM.epochNumber += 1

            ## record every epoch
            # df
            totalDebt.append(copy.deepcopy(self.bonds[0].totalDebt))
            treasury_balance.append(copy.deepcopy(self.bonds[0].treasury))
            DAO_balance.append(copy.deepcopy(self.bonds[0].DAO))
            user_balance.append(copy.deepcopy(self.users[0].balances))
            
            # dfa #df adjustments
            adjustments.append(copy.deepcopy(self.bonds[0].adjustment))
            current_debt.append(copy.deepcopy(self.bonds[0].current_debt()))
            total_supply.append(copy.deepcopy(self.bonds[0].total_supply()))
            bond_price.append(copy.deepcopy(self.bonds[0].bond_Price_in_USD()))
            bcv.append(copy.deepcopy(self.bonds[0].bond_control_variable))
            
        # Outside loop
        #df
        df = pd.DataFrame(
            [totalDebt, treasury_balance,
             DAO_balance, user_balance]
             ).T
        df.columns = ['totalDebt', 'treasury', 'DAO', 'User1Bal']
        ##dfa
        dfa = pd.DataFrame(
            [adjustments, current_debt, total_supply, bond_price, bcv]
            ).T
        dfa.columns = ['adjustments', 'current_debt', 'total_supply', 'bond_price',
                       'bcv']
        
        # Elaspse epochs 
        # for _ in range(5):#self.configs["days"]
        #     Temporal.elapse_epoch()
        print(self.bonds)

        ## Charts
        self.etl_plot_stacked_bar(df, 'treasury', 'treasury')
        self.etl_plot_stacked_bar(df, 'DAO', 'DAO')
        self.etl_plot_stacked_bar(df, 'User1Bal', 'User1Bal')

        df_totalDebt = pd.DataFrame(
            totalDebt,
            columns=['DAI']
            )
        self.plot_stacked_bar(df_totalDebt, 'totalDebt')

        return [df, dfa]

    @staticmethod
    def plot_stacked_bar(df:pd.DataFrame, title:str):
        colors = px.colors.qualitative.T10
        # plotly
        fig = px.bar(df, 
                    x = df.index,
                    y = [c for c in df.columns],
                    # template = 'plotly_dark',
                    color_discrete_sequence = colors,
                    title = title, 
                    )
        fig.show()
        return None
    
    @staticmethod
    def get_etl_df(df:pd.DataFrame, col:str) -> pd.DataFrame:
        ## ETL data
        if col in df.columns:
            colnames = list(df[col][0].keys())
            df_out = pd.DataFrame(
                [[i[j] for j in colnames] for i in df[col]],
                columns=colnames
            )
        else:
            RuntimeWarning('col not in df')

        return df_out

    @staticmethod
    def etl_plot_stacked_bar(df:pd.DataFrame, col:str, title:str):
        df_out = SimHandler.get_etl_df(df, col)
        SimHandler.plot_stacked_bar(df_out, title)
        return None