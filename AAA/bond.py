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
    
    bond_id: int = 0
    all: List = []

    def __init__(self, received_conf: Dict = {}):
        self.control_varriable: int = 0.2
        self.vesting_term: int = 5 #days; at least 36 hrs
        self.min_price: int = 0.8
        self.max_payout: int = 500 # 0.5% , can't be above 1%
        self.fee: int = 2 # % goes to AAA Treasury
        self.max_debt: int = 0.9
        self.asset_token = 'DAI'
        
        self.id: int = Bond.bond_id
        Bond.bond_id += 1
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

    def __repr__(self):
        return f'Bond-{self.asset_token}'
