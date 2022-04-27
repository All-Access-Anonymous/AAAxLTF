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

A representation of a reserve for a token.

Used to calculate reserves for tokens and analyze inflation.
This module houses many utilities for that.
"""

import numpy as np


class Reserve:
    """Represents reserve for a token.

    A token is backed by a reserve. An inflation is created when reserve power increases.

    Attributes:
        reserve_power: float above 0 value closer to 0 will decrease the differece between 
            reserve and token price.
        token_price: np.linspace token price. An array of one token price as token gets
            minted.
        total_token_amount: np.linspace above 0 amount of token minted. Needs
            np.ndarray created from np.linspace with amount of tokens and
            the number of points to plot.
    """

    def __init__(self,
                 reserve_power: float,
                 token_price: np.ndarray,
                 total_token_amount: np.ndarray):
        """Initialize this class with parameter values."""

        try:
            if reserve_power < 0:
                raise ValueError("reserve_power value cannot be negative.")

            elif len(total_token_amount) != len(token_price):
                raise ValueError("np.ndarray size of total_token_amount and token_price \
                        needs to be equal")

        except ValueError as err:
            print(err)

        else:
            self.reserve_power: float = reserve_power
            self.token_price: np.ndarray = token_price
            self.total_token_amount: np.ndarray = total_token_amount

    def find_reserve (self) -> np.ndarray:
        """Find reserve of token price.

            Return:
                np.ndarray reserve of token.
        """

        reserve_power = np.power(self.total_token_amount, self.reserve_power)

        return self.token_price * reserve_power
