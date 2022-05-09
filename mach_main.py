from aaaMachinations import BondingCurveAnalysis, Curves


def main():
    # Example usage:
    total_token_supply = 1000000
    reserve_power = 0.2
    detail_level = 1000

    # Initiate classes
    sigmoid_curve = Curves.SigmoidCurve(200, 5, 20000000)

    wsAAA = BondingCurveAnalysis(token_name = "wsAAA",
                                 curve_function = sigmoid_curve, 
                                 total_token_supply = total_token_supply,
                                 reserve_power = reserve_power,
                                 detail_level = detail_level)
    
    wsAAA.show_figure()
