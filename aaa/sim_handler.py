from typing import List
from aaa import Config
from aaa.attendee import Attendee
from aaa.temporal import Temporal
from aaa.logger import pkg_logger as pl

import scipy.stats as stats

'''
from aaa import Config
from attendee import Attendee
from temporal import Temporal
from logger import pkg_logger as pl
'''
Log = pl.Logger().get_logger()


class SimHandler:
    """
    Responsiblities:
        Instantiate Attender based on Series level (A, AA, AAA)
        Instantiate Ticket Market, with varying prices based on Tier Partitions.
            For Series A - 1 Partition
            For Series AA - 3 Partitions
            For Series AA - 5-7 Partitions

        Let ticket market take a JSON as configs for
        every object
    """

    def __init__(self, configs: dict = {}):
        self.configs: dict | None = self.load_config(configs)


    def load_config(self, config: dict) -> None:
        """
        If no configuration was provided, we source a
        default
        """
        if not config:
            self.config: dict = Config.sim_confs


    def generate_buy_dates(self, lower: int, upper: int, mean: int,
                            standard_deviation: int) -> List[int]:

        buy_dates = stats.truncnorm(
            (lower - mean) / standard_deviation, (upper - mean) / standard_deviation,
            loc = mean, scale=standard_deviation)

        return [2,4]


    @staticmethod
    def fibonnaci_of(n: int):
        """
        Recursive Fibonnaci, a helper method for
        seating disributor.
        """
        if n in {0, 1}:
            return n
        return SimHandler.fibonnaci_of(n - 1) + SimHandler.fibonnaci_of(n - 2)


    def fix_rounding_imprecision(self, seating_allocations: List[int]) -> List[int]:
        """
        When building the discrete seating allocations (how many people per seating level),
        as a result of rounding floats we may get extra or missing people in the allocations
        that makes their sum unequal with config['attendee_count'].
        This method adds back what's missing or negates any extras, and then gives
        back the fixed list of seating allocations.
        """

        alloc_sum = sum(seating_allocations)

        if alloc_sum > self.config["attendee_count"]:
            seating_allocations[0] -= alloc_sum - self.config["attendee_count"]
            return seating_allocations
        elif alloc_sum < self.config["attendee_count"]:
            seating_allocations[0] += self.config["attendee_count"] - alloc_sum
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
            int(self.config["attendee_count"] * i) for i in seating_allocations
        ]
        seating_allocations = self.fix_rounding_imprecision(
            discrete_allocations)

        return seating_allocations


    def prepare_attendees(self, player_count: int):
        """
        Instantiating the attendees based on their Seat level.
        """

        seating_tiers: int = self.config["seating_levels"]
        seating_distribution: List[int] = self.seating_distributor(
            seating_tiers, player_count
        )

        attendees: List[Attendee] = []

        for index, seat_tier in enumerate(seating_distribution):

            seating_tier_number: int = seating_tiers - index

            for _ in range(seat_tier):
                # print(f"Instantiated Attendee with Tier {seating_tier_number}")
                attendees.append(Attendee(seating_tier=seating_tier_number))

        return attendees


    def run(self) -> None | dict:
        """
        Sets the stage for the simulation by instantiating all
        necessary objects / agents, and then runs the simulation.

        :rtype: dict
        """

        attendees: List[Attendee] = self.prepare_attendees(
            self.config["attendee_count"]
        )

        for _ in range(self.config["days"]):
            Temporal.elapse_day()

        print(attendees)
