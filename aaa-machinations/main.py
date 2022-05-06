from Curves import SigmoidCurve 
from Reserve import Reserve
from BondingCurveAnalysis import BondingCurveAnalysis

import numpy as np

def main():
    # Example usage
    sigmoid_curve = SigmoidCurve(2, 4, 5)

    print(sigmoid_curve.f(23))

    bca = BondingCurveAnalysis(curve_function=sigmoid_curve,
                               total_token_amount=1000, 
                               reserve_power=0.5, 
                               detail_level=10)

    print(bca.bonding_curve)

    print(bca.get_reserve())

if __name__ == "__main__":
    main()
