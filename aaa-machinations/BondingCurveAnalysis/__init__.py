"""MIT License

Copyright (c) 2022 Longtail Financial

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

Author: Daniel Ahn

Bonding Curve Analysis module.

BondingCurveAnalysis class represents a class with collection of analytical utilities.
Houses a bonding curve function and reserve for analytics.

    Typical usage example:

    curve = SigmoidCurve(2, 5, 2)
    total_token_amount = 2000000

    # Create BondingCurve
    bonding_curve = BondingCurveAnalysis(curve, total_token_amount)
"""

import Reserve
import Curves 

import numpy as np
import plotly.express as px

class BondingCurveAnalysis:
    """A class that houses a bonding curve function and reserve to analyze the market.

        It contains various analytical utilities to identify inflation and trend.

        Attributes:
            curve_function: a bonding curve function.
            total_token_amount: int total amount of tokens circulating the market.
            reserve: reserve asset backing the token.
            detail_level: int above 0 value amount of points to plot.
    """
    
    def __init__(self,
                 curve_function: Curves.SigmoidCurve,
                 total_token_amount: int,
                 reserve_power: float,
                 detail_level: int = 1000):
        """Initialize this class with the parameter values"""

        try:
            if total_token_amount < 0:
                raise ValueError("total_token_amount need to be non-negative integer.")
            elif detail_level < 0:
                raise ValueError("detail_level need to be non-negative integer.")

        except ValueError as err:
            print(err)

        else:
            self.curve_function: Curves.SigmoidCurve = curve_function
            self.total_token_amount: int = total_token_amount
            self.reserve_power: float = reserve_power 
            self.detail_level: int = detail_level

            # This is required to plot the curve and draw sexy graphs
            self._linear_space_token_amount: np.ndarray = np.linspace(0, total_token_amount, detail_level)
            self._bonding_curve = None
            self._reserve = None

    @property
    def bonding_curve(self):
        # Calculating the bonding curve over linear space can become very costly computation if
        # the detail_level goes over 100000.
        # Hence, this variable is not initialized at __init__ and only initialized when the user
        # needs it.

        # Here we check if self._bonding_curve is defined.
        if self._bonding_curve == None:
            self._bonding_curve = self.curve_function.f(self._linear_space_token_amount)

        return self._bonding_curve

    def build_bonding_curve_figure(self):
        return px.line(x=self._linear_space_token_amount,
                       y=self.curve_function.f(self._linear_space_token_amount))

    def get_reserve(self):
        # Creating reserve can become a costly computation as the number of plots increase.
        # Hence, reserve will only be created when it's required by user.

        # Here we check if self.reserve is defined.
        if self._reserve == None:
            # At class initialization, self.reserve is not defined.
            # So when user calls this function, initialize the variable now.
            self._reserve = Reserve.Reserve(self.reserve_power, 
                                           self._bonding_curve,
                                           self._linear_space_token_amount)

        return self._reserve.find_reserve()

