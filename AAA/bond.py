from typing import List, Dict
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
        self.vesting_term: int = 5 #epoch (day) ; at least 36 hrs
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
            'rate': 0,
            'target': 0,
            'buffer': 0,
            'lastBlock': 0
        }
        # BondInfo: stores bond information for depositors (dict)
        #     - payout: OHM remaining to be paid
        #     - vesting: Blocks left to vest
        #     - lastBlock: Last interaction
        #     - pricePaid: In DAI, for front end viewing
        self.BondInfo = {
            'payout': 0,
            'vesting': 0,
            'lastBlock': 0,
            'pricePaid': 0
        }

        self.id: int = Bond.instance_number
        Bond.instance_number += 1
        Bond.all.append(self)


    def adjust_BCV(self) -> None:
        
        increment <= self.bond_control_variable*0.025
        self.adjustment['rate'] = increment
        if self.adjustment['add']:
            self.bond_control_variable += self.adjustment['rate']
            if self.bond_control_variable >= self.adjustment['target']:
                self.adjustment['rate']=0
        else:
            self.bond_control_variable -= self.adjustment['rate']
            if self.bond_control_variable <= self.adjustment['target']:
                self.adjustment['rate']=0
        return None

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
        elif p!=0:
            self.min_price = 0
        minimal_bond_price = self.get_minimal_bond_price()
        if p < minimal_bond_price:
            p = minimal_bond_price
        return p

    def bond_Price_in_USD(self) -> int:
        """
        Calculate bond price to DAI Value
        """
        if self.is_Liquidity_Bond:
            return 99 ##
        else:
            return 99 ##

    def debt_ratio(self) -> int:
        """
        Calculate current ratio of debt to FHM supply
        Returns debt ratio
        """
        return self.current_debt() / self.total_supply()

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
        # return total_debt - self.debt_decay()
        pass

    
    def debt_decay(self) -> int:
        """
        amount to decay total debt by
        Returns amount to decay
        """

        pass

    def calc_percent_vested_for(self, userId: int) -> int:
        """
        calculate how far into vesting a depositor is
        Returns percent vested
        """
        pass



    def calc_pending_payout(self, userId: int) -> int:
        """
        Calculate amount of AHM available for claim by depositor
        Returns pending payout AHM
        """
        pass
    
    def decay_Debt(self) -> None:
        """
        decay debt by 1% per block
        """
        pass
    ## USer Functions

    def deposit(self, userId: int, amount: int) -> None:
        """
        Deposit amount of principle into bond
        """
        self.decay_Debt()
        if self.totalDebt <= self.max_debt:
            pass
        else:
            RuntimeWarning("Bond is over debt limit, Max Capacity Reached")
        
        price_in_USD = self.bond_Price_in_USD()
        native_price = self.bond_price()

        



        pass


    def __repr__(self):
        return f'Bond-{self.principle}'
