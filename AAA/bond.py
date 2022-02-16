from typing import List, Dict
# https://github.com/OlympusDAO/olympus-contracts/blob/Version-1.1/contracts/BondDepository.sol

class Bond():
    """
    A Bond has following terms: 
    - control Variable; // scaling variable for price
    - vesting Term; // in blocks
    - minimum Price; // vs principle value
    - maxPayout; // in thousandths of a %. i.e. 500 = 0.5%
    - fee; // as % of bond payout, in hundreths. ( 500 = 5% = 0.05 for every 1 paid)
    - maxDebt; // 9 decimal debt ratio, max % total supply created as debt
    """
    
    instance_number: int = 1
    all: List = []

    def __init__(self, received_conf: Dict = {}):
        self.bond_control_variable: int = 0.2
        self.vesting_term: int = 5 #days; at least 36 hrs
        self.min_price: int = 0.8
        self.max_payout: int = 500 # 0.5% , can't be above 1%
        self.fee: int = 2 # % goes to AAA Treasury
        self.max_debt: int = 0.9
        self.asset_token = 'DAI'
        self.is_Liquidity_Bond = False # true if LP bond
        self.id: int = Bond.instance_number
        Bond.instance_number += 1
        Bond.all.append(self)

    # Info for incremental adjustments to control variable 
        # bool add; // addition or subtraction
        # uint rate; // increment
        # uint target; // BCV when adjustment finished
        # uint buffer; // minimum length (in blocks) between adjustments
        # uint lastBlock; // block when last adjustment made

    ##Events

    def adjust_BCV(self, block_number: int) -> None:
        pass

    #Info for bond holder
        # uint payout; // OHM remaining to be paid
        # uint vesting; // Blocks left to vest
        # uint lastBlock; // Last interaction
        # uint pricePaid; // In DAI, for front end viewing

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


    def calc_bond_price(self) -> int:
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


    def __repr__(self):
        return f'Bond-{self.asset_token}'
