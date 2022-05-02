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

SigmoidCurve module.
The SigmoidCurve class can be instantiated with various values (a, b and c) to 
customize the curve. It's used later to find f(x).

Mathmatical formula:
    f(x) = a * ((x - b / sqrt(c + (x - b)**2)) + 1)
Graph representation:
    https://www.desmos.com/calculator/j1yxue0euk
"""

import numpy as np
import math


class SigmoidCurve:
    """A sigmoid curve.
        
        Mathmatical formula:
            f(x) = a * ((x - b / sqrt(c + (x - b)**2)) + 1)
        Graphing representation:
            https://www.desmos.com/calculator/j1yxue0euk
            
        Attributes:
            slope_height: float changes height of the curve.
            x_transition: float x-axis transition of the curve.
            steepness: float controls the steepness of the curve.
    """
    def __init__(self,
                 slope_height: float,
                 x_transition: float,
                 steepness: float):
        """Initialize this class with the parameter values."""
        
        self.slope_height: float = slope_height
        self.x_transition: float = x_transition
        self.steepness: float = steepness
    
    def f(self, x: float) -> float:
        """A sigmoid function that returns f(x).
            
            Arg:
                x: float or numpy.ndarray x value of f(x).
            
            Return:
                Same datatype of input(float or numpy.ndarray) value of f(x).
        """
        y = self.slope_height * (((x - self.x_transition) / math.sqrt(self.steepness + ((x - self.x_transition) ** 2))) + 1)
        return y
