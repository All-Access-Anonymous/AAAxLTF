from typing import List

from aaa import Config
from aaa.attendee import Attendee
from aaa.market import Market
from aaa.temporal import Temporal
from aaa.logger import pkg_logger as pl
from aaa.mediator import Mediator

import plotly.express as px
import numpy as np
import random
import pwlf


Log = pl.Logger().get_logger()


class SimHandler:
    """
    Responsiblities:
        Instantiate Attender based on Series level (A, AA, AAA)
        Instantiate Ticket Market, with varying prices based on Tier Partitions.
            For Series A - 1 Partition
            For Series AA - 3 Partitions
            For Series AAA - 5-7 Partitions

        Let ticket market take a JSON as configs for
        every object
    """

    def __init__(self, configs: dict):
        #self.configs: dict = configs | self.load_config(configs)
        self.configs: dict = configs
        self.day_weights = self.buy_date_weights()

        self.res_a, self.res_b, self.res_c = self.generate_buy_days(self.day_weights)
        self.buy_frequency_line_plot = self.res_a
        self.buy_days: List[int] = self.res_b
        self.buy_frequency_bar_plot = self.res_c

    def load_config(self, config: dict) -> dict:
        """
        If no configuration was provided, we source a
        default
        """
        return Config.sim_confs

    @staticmethod
    def rand_chance(low: float = 0, high: float = 1) -> float:
        '''
        Random number generator, then bounded and rounded.
        '''
        randnum = np.random.uniform(low, high)
        return round(randnum, 2)

    @staticmethod
    def fibonnaci_of(n: int):
        """
        Recursive Fibonnaci, a helper method for
        seating disributor.
        """
        if n in {0, 1}:
            return n
        return SimHandler.fibonnaci_of(n - 1) + SimHandler.fibonnaci_of(n - 2)

    @staticmethod
    def reduce(sample: np.ndarray, count: int) -> List[float]:
        '''
        The z list from generate_buy_days() will have too many points (intended).
        One point for each person in the population is needed.
        The range has to be the same but not as many elements.

        :param sample: The List of points from where we derive a buy_day for each Attendee.
        :type sample: np.ndarray

        :param count: To how many elements do we condense the sample of values.
            Let it be an int (one for each person)
        :type count: int
        '''
        indexed: List = [item for item in enumerate(sample)]
        random.shuffle(indexed)
        trimmed = indexed[:count]
        trimmed.sort()
        return [item for index, item in trimmed]

    def buy_date_weights(self) -> List[List]:
        '''
        :param days_range: The duration of the simulation in days.
        :type days_range: int

        :param weights: The weights for segments of the days_range
        :type weights: List[float | int]
        '''

        weights_length: int = len(self.configs['buy_day_weights'])

        day_segment: float = self.configs['days'] / weights_length
        day_partitions: List[int] = [
            0, *[int(day_segment * (i+1)) for i in range(weights_length)]]
        # Pop off an extra element such that len(day_partitions) == len(weights)
        day_partitions.pop()

        return day_partitions

    def generate_buy_days(self, day_partitions: List[int]):
        '''
        Given a population, and day_range, we return a list of ints
        that determine a buy date for each Attendee in the population
        such that when plotted in a histogram, that comes from the
        probability density suggested by the control points.

        :param control_xy: Contains information that influences the buying
        trend of the population buy specifying what days get the most/least purchases

        :type control_xy: List[List]

        :param population: How many people will be in the simulation
        :type population: int

        :return: A list containing the determined buy date for everyone in the population
        :rtype: List[int]
        '''
        # Creating a Piecewise Linear Fit for the Points
        # Let's use numpy and the pwlf package (pwlf stands for piecewise linear fit).
        # In general, we would want the x and y below to be control points that we
        # can adjust in fitting the distribution.

        # Small check, x and y should be same length
        assert len(day_partitions) == len(self.configs['buy_day_weights'])
        days: int = self.configs['days']

        # x is day paritions
        # y is day weights
        x = np.array(day_partitions)
        y = np.array(self.configs['buy_day_weights'])

        my_pwlf = pwlf.PiecewiseLinFit(x, y)
        breaks = my_pwlf.fit(len(x) - 1)

        my_y_vals = [my_pwlf.predict(x)[0] for x in range(days)]
        my_x_vals = range(days)

        # Creating plot
        fig_a = px.line(y=my_y_vals, x=my_x_vals)

        # Normalizing
        my_weights = 1/sum(my_y_vals) * np.array(my_y_vals)

        sample = random.choices(range(days),
                                weights=my_weights,
                                k=self.configs['attendee_count'])  # Sampling

        result = px.histogram(sample, nbins=days)

        # First return is the line plot
        # Second return is the list of buy dates we'll actually use
        # Third return is the bar plot of the frequency of buys by day
        return fig_a, sample, result

    '''
    def generate_buy_days(self, *args):
        ls: List[int] = [int(SimHandler.rand_chance(
            1, self.configs['days'])) for _ in range(self.configs['attendee_count'])]
        return ls
    '''

    def fix_rounding_imprecision(self, seating_allocations: List[int]) -> List[int]:
        """
        When building the discrete seating allocations (how many people per seating level),
        as a result of rounding floats we may get extra or missing people in the allocations
        that makes their sum unequal with config['attendee_count'].
        This method adds back what's missing or negates any extras, and then gives
        back the fixed list of seating allocations.
        """

        alloc_sum = sum(seating_allocations)

        if alloc_sum > self.configs["attendee_count"]:
            seating_allocations[0] -= alloc_sum - \
                self.configs["attendee_count"]
            return seating_allocations
        elif alloc_sum < self.configs["attendee_count"]:
            seating_allocations[0] += self.configs["attendee_count"] - alloc_sum
            return seating_allocations

        return seating_allocations

    def seating_distributor(self, distributions: int, attendee_count: int) -> List[int]:
        """
        The seating distribution follows a Fibonnaci sequence pattern that
        starts from the third digit.

        Consider a case where we have five seating levels.
        The seating levels are tiered by exclusivity. Seating Level 1
        will be akin to first class, Seating Level 5 will be just like economy.

        Following a realistic distribution, the least purchased Seating Level would
        be of Seating Level 1 (because very expensive), and the most purchased Seating Level
        would be of Seatling Level 5 (because most affordable)

        -- Procedure --

            Given n seating distributions, we will take the first n+2 digits of the Fibonacci sequence.
            [ 0, 1, 1, 2, 3, 5, 8 ]

            We will discard the first two digits.
            [ 1, 2, 3, 5, 8 ]

            Sum up the digits.
            sum(1, 2, 3, 5, 8) = 19

            Divide each number of our fibonacci sequence by the sum.
            [ 0.0526, 0.1052, 0.1578, 0.2631, 0.4210 ]

            Multiply each of these values by the config['attendee_count'] (the total population)
            Let's say the attendee_count is 1000
            [ 52.6, 105.2, 157.8, 263.1, 421 ]

            Typecast it into int.
            [ 52, 105, 157, 263, 421 ]

            Submit these ints into fix_rounding_imprecision() as a List.
            Now you have the distribution from Seating Level 1 up to Seating Level 5.
            The masses take the more affordable seats.
        """

        distribution_nos: int = max(1, distributions)

        distribution_allocations: List[int] = [
            SimHandler.fibonnaci_of(n) for n in range(distribution_nos + 2)
        ]
        distribution_allocations = distribution_allocations[-distribution_nos:]
        distribution_allocations.reverse()
        distribution_sum: int = sum(distribution_allocations)

        seating_allocations: List[float] | List[int] = [
            round((i / distribution_sum), 4) for i in distribution_allocations
        ]

        discrete_allocations = [
            int(attendee_count * i) for i in seating_allocations
        ]
        seating_allocations = self.fix_rounding_imprecision(
            discrete_allocations)

        return seating_allocations

    def prepare_attendees(self, player_count: int):
        """
        Instantiating the attendees based on their Seat level.
        """

        seating_tiers: int = self.configs["seating_levels"]
        seating_distribution: List[int] = self.seating_distributor(
            seating_tiers, player_count
        )

        buy_days: List[int] = self.buy_days
        attendees: List[Attendee] = []

        for index, seat_tier in enumerate(seating_distribution):

            seating_tier_number: int = seating_tiers - index

            for _ in range(seat_tier):
                attendees.append(
                    Attendee(seating_tier=seating_tier_number, buy_day=buy_days.pop()))

        return attendees

    def diagnostics(self) -> None:
        pass

    def run(self) -> None | dict:
        """
        Sets the stage for the simulation by instantiating all
        necessary objects / agents, and then runs the simulation.

        :rtype: dict
        """

        attendees: List[Attendee] = self.prepare_attendees(
            self.configs["attendee_count"]
        )

        market = Market(self.configs["seating_levels"],
                        self.configs["market_config"]['price_increase_multiplier'],
                        self.configs['market_config']['log_day'])
        med = Mediator(market, *attendees)

        for _ in range(self.configs["days"]):
            Temporal.elapse_day()

        res_dict: dict =  {
            "USDC Received by Market": market.USDC_received,
            "Last Day Base Ticket Price": market.base_ticket_price
        }

        return res_dict
