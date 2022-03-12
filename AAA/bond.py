from typing import List, Dict
import pprint
# https://github.com/OlympusDAO/olympus-contracts/blob/Version-1.1/contracts/BondDepository.sol

class Bond():
    """
    ## Events
    - When Bond is created
    - When Bond is claimed
    - When Bond price changed
    - When BCV changes

    ## State Variables
    - Address public immutable
        - AHM: token given as payout
        - principle: token used to create bond
        - treasury: mints AHM when receives principle
        - DAO: receives profit share from bond
        --------------------------------------------------
        - staking: to auto stake payment
        - stakingHelper: to stake and claim if no staking warmup
    - is_Liquidity_Bond: bool 
    
    - totalDebt: total value of outstanding bonds; used for pricing
    - lastDecay: reference block for debt decay 

    terms: stores terms for new bonds
        - control Variable: scaling variable for price
        - vesting Term: in blocks
        - minimum Price: vs principle value
        - maxPayout: in thousandths of a %. i.e. 500 = 0.5%
        - fee: as % of bond payout, in hundreths. ( 500 = 5% = 0.05 for every 1 paid)
        - maxDebt: 9 decimal debt ratio, max % total supply created as debt

    adjustment: stores adjustment to BCV data
    (Info for incremental adjustments to control variable )
        - add: addition or subtraction
        - rate: increment
        - target: BCV when adjustment finished
        - buffer: minimum length (in blocks) between adjustments
        - lastBlock: block when last adjustment made

    BondInfo: stores bond information for depositors (dict)
        - payout: OHM remaining to be paid
        - vesting: Blocks left to vest
        - lastBlock: Last interaction
        - pricePaid: In DAI, for front end viewing

    """
    
    instance_number: int = 1
    all: List = []

    def __init__(self, received_conf: Dict = {}):
        self.bond_control_variable: int = 0 # Bonds must be initialized from 0
        self.vesting_term: int = 3 #epoch (day) ; at least 36 hrs
        self.min_price: int = 0.8
        self.max_payout: int = 500 # 0.5% , can't be above 1%
        self.fee: int = 2 # % goes to AAA Treasury
        self.max_debt: int = 0.9

        # - AHM: token given as payout
        # - principle: token used to create bond
        self.principle = 'DAI'
        # - treasury: mints AHM when receives principle
        # - DAO: receives profit share from bond
        # --------------------------------------------------
        # - staking: to auto stake payment
        # - stakingHelper: to stake and claim if no staking warmup
        # - is_Liquidity_Bond: bool 
        self.is_Liquidity_Bond = False # true if LP bond

        # - totalDebt: total value of outstanding bonds; used for pricing
        self.totalDebt = 0
        # - lastDecay: reference block for debt decay 
        self.lastDecay = 0

        # adjustment: stores adjustment to BCV data
        # (Info for incremental adjustments to control variable )
        #     - add: addition or subtraction
        #     - rate: increment
        #     - target: BCV when adjustment finished
        #     - buffer: minimum length (in blocks) between adjustments
        #     - lastBlock: block when last adjustment made
        self.adjustment = {
            'add': False,
            'rate': 0.1,
            'target': 1,
            'buffer': 5,
            'lastBlock': 0
        }
        # BondInfo: stores bond information for depositors (dict)
        #     - payout: OHM remaining to be paid
        #     - vesting: Blocks left to vest
        #     - lastBlock: Last interaction
        #     - pricePaid: In DAI, for front end viewing
        self.BondInfo = {}

        self.treasury = {'DAI':0, 'AHM':0}
        self.DAO = {'DAI':0, 'AHM':0}
        self.epochNumber = 0
        self.sum_AHM_users = 0

        self.id: int = Bond.instance_number
        Bond.instance_number += 1
        Bond.all.append(self)

    ## View Functions
    def maxPayout(self) -> int:
        """
        Calculate max bond size
        """
        return self.total_supply() * self.max_payout / 100000

    def get_minimal_bond_price(self) -> int:
        """
        Calculate minimal bond price
        Returns minimal bond price
        """
        market_price = self.get_market_price()
        discount = market_price * self.maximum_discount
        price = market_price - discount
        if self.is_Liquidity_Bond:
            return 99 ##
        else:
            return price


    def bond_price(self) -> int:
        """
        Calculate bond price to DAI Value
        """
        p = 1 + (self.bond_control_variable * self.debt_ratio())
        if p < self.min_price:
            p = self.min_price
        print(f'bond_price: {p}')
        return p

    def _bond_price(self) -> int:
        """
        Calculate bond price to DAI Value
        """
        p = 1 + (self.bond_control_variable * self.debt_ratio())
        if p < self.min_price:
            p = self.min_price
        elif self.min_price != 0:
            self.min_price = 0
        return p

    def bond_Price_in_USD(self) -> int:
        """
        Calculate bond price to DAI Value
        """
        if self.is_Liquidity_Bond:
            return 99 ##
        else:
            return self.bond_price() * 1 #DAI 

    def debt_ratio(self) -> int:
        """
        Calculate current ratio of debt to AHM supply
        Returns debt ratio
        """
        return self.current_debt() / self.total_supply()

    def total_supply(self) -> int:
        """
        Calculate total supply of AHM
        """
        sum_AHM = self.treasury['AHM'] + self.DAO['AHM'] + self.sum_AHM_users
        if sum_AHM == 0:
            return 1
        print(f'Total AHM supply: {sum_AHM}')
        return sum_AHM

    def standardized_Debt_Ratio(self) -> int:
        """
        Calculate the debt ratio in same terms for reserve or liquidity bonds
        Returns debt ratio
        """
        if is_Liquidity_Bond:
            return self.debt_ratio() # **
        else:
            return self.debt_ratio()

    def current_debt(self) -> int:
        """
        calculate debt factoring in decay
        Returns int
        """
        return self.totalDebt - self.debt_decay()

    ## Internal Helper functions
    def debt_decay(self) -> int:
        """
        amount to decay total debt by
        Returns amount to decay
        """
        epochSinceLast = self.epochNumber - self.lastDecay
        decay = self.totalDebt * (epochSinceLast / self.vesting_term)
        if decay > self.totalDebt:
            decay = self.totalDebt
        return decay

    # def decay_Debt(self) -> None:
    #     """
    #     """
    #     self.totalDebt = self.totalDebt - self.debt_decay()
    #     self.lastDecay = self.epochNumber
    #     return None

    def adjust(self) -> None:
        if self.epochNumber >= self.adjustment['lastBlock'] + self.adjustment['buffer']:
            initial = self.bond_control_variable
            if self.adjustment['add']: #if rate should increase
                self.bond_control_variable += self.adjustment['rate'] #raise rate
                if self.bond_control_variable > self.adjustment['target']: #if target met
                    self.adjustment['rate'] = 0 #turn off adjustment
            else: #if rate should decrease
                self.bond_control_variable -= self.adjustment['rate'] #lower rate
                if self.bond_control_variable <= self.adjustment['target']: #if target met
                    self.adjustment['rate'] = 0 #turn off adjustment
            self.adjustment['lastBlock'] = self.epochNumber
        return None

    # def adjust_BCV(self) -> None:
    #     if self.epochNumber >= self.adjustment['lastBlock'] + self.adjustment['buffer']:
    #         increment <= self.bond_control_variable*0.025
    #         self.adjustment['rate'] = increment
    #         if self.adjustment['add']:
    #             self.bond_control_variable += self.adjustment['rate']
    #             if self.bond_control_variable >= self.adjustment['target']:
    #                 self.adjustment['rate']=0
    #         else:
    #             self.bond_control_variable -= self.adjustment['rate']
    #             if self.bond_control_variable <= self.adjustment['target']:
    #                 self.adjustment['rate']=0
    #         return None

    

    ## USer Functions

    def deposit(self, user: object, amount: int) -> None:
        """
        Deposit amount of principle into bond
        """
        if user.balances[self.principle] < amount:
            return "Insufficient funds"
        ##
        # self.decay_Debt()
        if self.totalDebt <= self.max_debt:
            pass
        else:
            RuntimeWarning("Bond is over debt limit, Max Capacity Reached")
        
        price_in_USD = self.bond_Price_in_USD()
        native_price = self.bond_price()

        value = amount * 1 # DAI rate
        pay_out = value/price_in_USD
        ## Payout Min max warning
        if pay_out < 0.01:
            RuntimeWarning("Payout Too Low, must be above 0.01 AHM")
        elif pay_out > self.max_payout:
            RuntimeWarning("Payout Too High, must be below {} AHM".format(self.max_payout))
        else:
            pass
        
        ##profit calculation
        fee = pay_out * self.fee * 0.01
        profit = pay_out - fee
                
        ## Treasury deposit function
        user.sub_bal(self.principle, amount)   
        self.treasury['DAI'] += amount
        self.DAO['AHM'] += fee

        ##update bond Info
        if user.id in self.BondInfo.keys():
            print(f'{user.id} already has a bond')
            self.BondInfo[user.id]['payout'] += pay_out
            self.BondInfo[user.id]['vesting'] = self.vesting_term
            self.BondInfo[user.id]['lastBlock'] = self.epochNumber
            self.BondInfo[user.id]['pricePaid'] += value
        else:
            self.BondInfo[user.id] = {
                'payout': pay_out,
                'vesting': self.vesting_term,
                'lastBlock': self.epochNumber,
                'pricePaid': value #in USD
            }

        ##update debt info
        self.totalDebt = self.totalDebt + pay_out 
        # print(f'Inc Debt == Total Debt: {self.totalDebt}')

        self.adjust() ##Control Variable Adjustment

        return pay_out

    def redeem(self, users:object) -> None:
        """
        Redeem all user's AHM and auto stake
        """
        # update BondInfo
        # update user wallets
        for user in users:
            if user.id in self.BondInfo.keys():
                if self.epochNumber >= self.BondInfo[user.id]['lastBlock'] + self.BondInfo[user.id]['vesting']:
                    user.add_bal('AHM', self.BondInfo[user.id]['payout'])
                    ##debt freed
                    self.totalDebt = self.totalDebt - self.BondInfo[user.id]['payout']
                    self.BondInfo[user.id]['payout'] = 0
                    self.BondInfo[user.id]['pricePaid'] = 0
                    ##remove item from BondInfo
                    self.BondInfo.pop(user.id)
                    ##logging
                    print(f'Redeemed bonds for {user.id}')
        return None

    def __repr__(self):
        print('Tresury')
        pprint.pp(self.treasury)
        print('DAO')
        pprint.pp(self.DAO)
        print('BondInfo')
        pprint.pp(self.BondInfo)
        print('Total Debt')
        print(self.totalDebt)
        return f'Bond-{self.principle}'
