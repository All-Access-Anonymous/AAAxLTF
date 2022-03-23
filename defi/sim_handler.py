## LOGGING 
import logging

# DEBUG: Detailed information, typically of interest only when diagnosing problems.

# INFO: Confirmation that things are working as expected.

# WARNING: An indication that something unexpected happened, or indicative of some problem in the near future (e.g. ‘disk space low’). The software is still working as expected.

# ERROR: Due to a more serious problem, the software has not been able to perform some function.

# CRITICAL: A serious error, indicating that the program itself may be unable to continue running.

import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
# # now if you use logger it will not log to console.
logger.propagate = False

# formatter = logging.Formatter('%(asctime)s:%(name)s:%(message)s')
formatter = logging.Formatter('%(levelname)s:%(name)s::: %(message)s')

file_handler = logging.FileHandler('simulation.log')
# # Only logs above ERROR gets to file
# file_handler.setLevel(logging.ERROR)
file_handler.setFormatter(formatter)

# # Only logs above DEBUG gets to console, its hierarchy is default to logger level
# stream_handler = logging.StreamHandler()
# stream_handler.setFormatter(formatter)

logger.addHandler(file_handler)
# logger.addHandler(stream_handler)

## import class objects 
from typing import List, Dict
from defi.user import User
from defi.bond import Bond
from defi.revenue import Revenue
from defi.treasury import Treasury
from defi.staking_AHM import Staking_AHM
from defi.config import sim_conf
# from pprint import pprint
import pandas as pd
import plotly.express as px
import copy

class SimHandler:
    """
    Responsiblities:
        Instantiate Objects
        Run simulation
        Generate dataframes and plots

    """

    def __init__(self, _config: dict):
        # self.config = self.load_config(configs)
        self.config = _config
        self.users = [] # all user objects
        self.minter = None # minter object instance of User with starting balance
        self.bonds = [] # all bond objects
        self.staking_AHM = None # a staking_AHM object or Contract
        self.treasury_obj = None
        self.revenue_obj = None

        logger.info('Simulation Handler instantiated')

    def instantiate_Users(self, number: int = 4) -> None:
        
        logger.info(f'instantiate {number} Users')        
        
        minter_bal = {
            'DAI': 0,
            'AHM': 600,
            'sAHM': 0,
            'ETH': 0,
        }
        minter = User(minter_bal)
        self.minter = minter

        for i in range(number):
            user = User(sim_conf['user_config']['balances'])
            self.users.append(user)
        return None

    def instantiate_Bonds(self, number: int = 1) -> None:
        logger.info(f'instantiate {number} Bonds')
        for i in range(number):
            bond = Bond(self.config['bond_config'])
            self.bonds.append(bond)
        return None

    def instantiate_Staking_AHM(self) -> None:
        self.staking_AHM = Staking_AHM()
        return None

    def instantiate_Treasury(self) -> None:
        self.treasury_obj = Treasury()
        return None

    def instantiate_Revenue(self) -> None:
        self.revenue_obj = Revenue()
        return None

    def instantiate_Simulation(self) -> pd.DataFrame:
        self.instantiate_Users(10) # instantiate users and store in self.users
        self.instantiate_Bonds(1) # instantiate bonds and store in self.bonds
        self.instantiate_Staking_AHM() # instantiated & stored in self.staking_AHM        
        self.instantiate_Treasury() # instantiated & stored in self.treasury_obj
        self.instantiate_Revenue() # instantiated & stored in self.revenue_obj
        # self.staking_AHM.stake_AHM(self.users[0], 50)
        # self.staking_AHM.stake_AHM(self.users[1], 100)
        # self.staking_AHM.stake_AHM(self.users[2], 100)
        # self.staking_AHM.stake_AHM(self.users[3], 200)
        return None

    # def reset_simulation(self) -> None:
    #     self.users = []
    #     self.bonds = []
    #     self.staking_AHM = None
    #     self.treasury_obj = None
    #     self.revenue_obj = None
    #     return None

    def run(self):
        logger.info('$$$------------Starting Simulation------------$$$')
        # self.reset_simulation()
        self.instantiate_Simulation()
        ## paramteer to record every epoch
        totalDebt = []
        treasury_balance = []
        user_balance = []
        total_sAHM = []
        total_AHM = []
        #dfa
        adjustments = []
        current_debt = []
        total_supply = []   # AHM supply
        bond_price = [] #USD
        bcv = [] 
        debt_ratio = []
        excess_reserve = []

        for i in range(self.config['days']):
            logger.info(f'Epoch ------------------------------------------------ {i}')
            # self.staking_AHM.add_interest_to_balances(interest_rate=1, users=self.users)
            #### Daily epoch routine ==before loop
            # update total AHM balance from users
            self.bonds[0].sum_AHM_users = sum(
                [i.balances['AHM'] + i.balances['sAHM'] for i in self.users]) +\
                    self.minter.balances['AHM']

            # all users bond after every 7th epoch 
            if self.bonds[0].debt_ratio() > self.bonds[0].max_debt:
                logger.warning("Bond is over debt limit, Max Capacity Reached")
            else:
                for user in self.users:
                    if user.balances['DAI'] > 0:
                        self.bonds[0].deposit(user, 10)

            ## add revenue to treasury
            self.revenue_obj.add_lp_reward(self.treasury_obj, 6)
            self.revenue_obj.add_interest_from_fiat_loan(self.treasury_obj, 20)
            self.bonds[0].treasury = self.treasury_obj.balances

            # after bonding, update treasury balance
            for k,v in self.bonds[0].treasury.items():
                if k in self.treasury_obj.balances.items():
                    self.treasury_obj.balances[k] += v
                else:
                    self.treasury_obj.balances[k] = v
    
            #### Daily epoch routine ==after loop
            # All user Redeemclaimable bonds
            self.bonds[0].redeem(self.users)
            # Adjust BCV if required
            
            

            ## - all users stake AHM
            # all users stake redeemed bonds
            for user in self.users:
                self.staking_AHM.stake_AHM(user, user.balances['AHM'])
            
            ## update epoch
            self.bonds[0].epochNumber += 1
            self.staking_AHM.epochNumber += 1

            logger.info(self.bonds[0].BondInfo)
            ## record every epoch
            # df
            totalDebt.append(copy.deepcopy(self.bonds[0].totalDebt))
            treasury_balance.append(copy.deepcopy(self.treasury_obj.balances))

            #df user
            user_balance.append(copy.deepcopy([i.balances for i in self.users]))
            
            # dfa #df adjustments
            adjustments.append(copy.deepcopy(self.bonds[0].adjustment))
            current_debt.append(copy.deepcopy(self.bonds[0].current_debt()))
            total_supply.append(copy.deepcopy(self.bonds[0].total_supply()))
            bond_price.append(copy.deepcopy(self.bonds[0].bond_price()))
            bcv.append(copy.deepcopy(self.bonds[0].bond_control_variable))
            debt_ratio.append(copy.deepcopy(self.bonds[0].debt_ratio()))
            excess_reserve.append(copy.deepcopy(self.bonds[0].excess_reserve()))
            
        # Outside loop
        logger.info('$$$------------ Simulation Completed ------------$$$')
        #df
        df = pd.DataFrame(
            [totalDebt, treasury_balance]
             ).T
        df.columns = ['totalDebt', 'treasury']
        ##dfa
        dfa = pd.DataFrame(
            [adjustments, current_debt, total_supply, bond_price, bcv, debt_ratio, excess_reserve]
            ).T
        dfa.columns = ['adjustments', 'current_debt', 'total_supply', 'bond_price',
                       'bcv', 'debt_ratio', 'excess_reserve']
        ## df user
        df_user = pd.DataFrame(user_balance)

        df_totalDebt = pd.DataFrame(
            totalDebt,
            columns=['DAI']
            )

        ## Charts
        charts = {
            'treasury': self.etl_plot_stacked_bar(df, 'treasury', 'treasury'),
            'user1': self.etl_plot_stacked_bar(df_user, 0, 'Balance User 0'),
            
            #     self.etl_plot_stacked_bar(df_user, i, f'Balance User-{i}') for i in range(len(df_user.columns))
            'totalDebt': self.plot_stacked_bar(df_totalDebt, 'totalDebt').to_json()
        }

        return {'df': df, 'dfa': dfa, 'charts': charts}

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
        # fig.show()
        return fig
    
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
        fig = SimHandler.plot_stacked_bar(df_out, title)
        return fig.to_json()