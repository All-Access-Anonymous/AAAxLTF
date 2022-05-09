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
    total_token_supply = 2000000

    # Create BondingCurve
    bonding_curve = BondingCurveAnalysis(curve, total_token_supply)
"""

import Reserve
import Curves 

import numpy as np
import plotly.graph_objects as go 

class BondingCurveAnalysis:
    """A class that houses a bonding curve function and reserve to analyze the market.

        It contains various analytical utilities to identify inflation and trend.

        Attributes:
            curve_function: a bonding curve function.
            total_token_supply: int total amount of tokens circulating the market.
            reserve: reserve asset backing the token.
            detail_level: int above 0 value amount of points to plot.
    """

    # Used for graphing curves in graph_objects
    # Options are: lines, markers, lines+markers
    go_fig_mode = "lines"
    xaxes_title = "Token supply"
    yaxes_title = "Price"
    
    def __init__(self,
                 token_name: str,
                 curve_function: Curves.SigmoidCurve,
                 total_token_supply: int,
                 reserve_power: float,
                 bonding_curve: np.ndarray = np.empty(0),
                 detail_level: int = 1000):
        """Initialize this class with the parameter values"""
        try:
            if total_token_supply < 0:
                raise ValueError("total_token_supply need to be non-negative integer.")
            elif detail_level < 0:
                raise ValueError("detail_level need to be non-negative integer.")

        except ValueError as err:
            print(err)

        else:
            # Here we initialize the properties
            self.token_name: str = token_name
            self.curve_function: Curves.SigmoidCurve = curve_function
            self.total_token_supply: int = total_token_supply
            self.reserve_power: float = reserve_power 
            self.detail_level: int = detail_level


            # This is required to plot the curve and draw sexy graphs
            self._linear_space_token_amount: np.ndarray = np.linspace(0, 
                                                                      total_token_supply, 
                                                                      detail_level)

            # Do not use this variable directly as it's desiged to be initialized by
            # property methods like the one below.
            self._reserve = None 
            # User can supply this value from other instance of this class at 
            # initialization but when nothing is passed, np.empty(0) will be used as 
            # default value.
            self._bonding_curve: np.ndarray = bonding_curve
            self._inflation: np.ndarray = np.empty(0)

    @property
    def bonding_curve(self):
        # Calculating the bonding curve over linear space can become very costly computation if
        # the detail_level goes over 100000.
        # Hence, this variable is not initialized at __init__ and only initialized when the user
        # needs it.
        
        # Recall that _bonding_curve was initialized with empty np.ndarray at class construction,
        # so, check its length.
        if len(self._bonding_curve) == 0:
    
            self._bonding_curve = np.linspace(0, self.total_token_supply, self.detail_level)

            for i in range(self.detail_level):
                self._bonding_curve[i] = self.curve_function.f(self._linear_space_token_amount[i])

        return self._bonding_curve

    def build_bonding_curve_figure(self, name: str = "Bonding Curve"):
        return go.Scatter(x = self._linear_space_token_amount,
                          y = self.bonding_curve,
                          name = name,
                          mode = self.go_fig_mode) 

    @property
    def reserve(self):
        # As discussed above creating reserve can become a costly computation as the 
        # number of plots increase.
        # Hence, reserve will only be created when it's required by user.

        # Here we check if self.reserve is defined.
        if self._reserve == None:
            # At class initialization, self.reserve is not defined.
            # So when user calls this function, initialize the variable now.
            self._reserve = Reserve.Reserve(self.reserve_power, 
                                            self.bonding_curve,
                                            self.detail_level)

        return self._reserve.find_reserve()

    def build_reserve_figure(self, name: str = "Reserve"):
        return go.Scatter(x = self._linear_space_token_amount,
                          y = self.reserve,
                          name = name,
                          mode = self.go_fig_mode) 

    @property
    def inflation(self):
        # Same concern as bonding_curve and reserve methods above.

        # Recall that _inflation was initialized with empty np.ndarray at class construction,
        # so, check its length.
        if len(self._inflation) == 0:
        # When the length is zero it means the inflation was not computed yet,
        # so, do it now.
            self._inflation = np.linspace(0, self.total_token_supply, self.detail_level)

            for i in range (self.detail_level):
                self._inflation[i] = self.bonding_curve[i] - self.reserve[i]

        return self._inflation

    def build_inflation_figure(self, name: str = "Inflation"):
        return go.Scatter(x = self._linear_space_token_amount,
                          y = self.inflation,
                          name = name,
                          mode = self.go_fig_mode) 

    def build_figure(self):
        fig = go.Figure()

        fig.add_trace(self.build_bonding_curve_figure())
        fig.add_trace(self.build_reserve_figure())
        fig.add_trace(self.build_inflation_figure())

        fig.update_xaxes(title_text = self.xaxes_title)
        fig.update_yaxes(title_text = self.yaxes_title)
        fig.update_layout(title = self.token_name, hovermode = "x unified")

        return fig

    def show_figure(self) -> None:
        fig = self.build_figure()

        fig.show()

    def fig_as_json(self):
        return self.build_figure().to_json()
