from aaa.temporal import Temporal
from aaa import Config
from plotly.subplots import make_subplots

import plotly.graph_objects as go

from typing import List

class Market(Temporal):

    def __init__(self, seating_levels: int,
                       base_ticket_price: float,
                       log_day: bool) -> None:
        super().__init__()

        # Configurables
        self.base_ticket_price: float = 50
        self.tiers: int = seating_levels
        self.tier_multiplier: float = 1.5
        self.log_day: bool = log_day

        # States
        self.ticket_registry: dict = self.prepare_ticket_registry(self.tiers)
        self.USDC_received: float = 0
        self.logs: List[List] = [ [ [], [], [] ]  for x in range(self.tiers)]
        self._days_elapsed: int = 0

    def __repr__(self) -> str:
       return f'MAR - {self.ticket_registry} - ${self.USDC_received}'

    def prepare_ticket_registry(self, seating_levels) -> dict:
        '''
        Before the market is able to accept any transactions
        and record the purchases to ticket registry,
        it must first derive how many tiers there are because
        that determines how many keys there will be for the
        ticket registry.
        '''

        registry_dict: dict = {}
        for i in range(seating_levels):
            registry_dict[i + 1] = {'Quantities Sold': 0, 'USDC Received': 0}

        return registry_dict

    @property
    def days_elapsed(self) -> int:
        '''
        Inhertied from Temporal
        '''
        return self._days_elapsed

    def day_pass(self) -> None:
        '''
        Inherited from Temporal
        '''
        self._days_elapsed += 1
        self.day_assess()

    def day_assess(self) -> None:
        '''
        day_assess contains the daily responsibilities
        assigned to each instance of this class.
        '''
        self.base_ticket_price *= 1.05

        if self.log_day:
            self.daily_log()

    # BTW make this a static method.
    def daily_log(self) -> None:
        '''
        What is there to log?
        The state of the ticket_registry each day.
        How would you save all this in dataframe form?

        It's going to be n plots depending on how many tiers
        there are. For each tier, the dataframe will look like this.
        Overlay the plots, check source code from prior works.
         _________________________________________
        | Day | Quantities Sold | USDC Received   |
         -----------------------------------------
        | 1   | 14              |  $600           |
        | 2   | 24              |  $900           |
        | 3   | 27              |  $1053          |
        | 4   | 35              |  $1332          |
        | 5   | 45              |  $1643          |
                    ...

        The list for each Tier will will contain 3 sub-lists.
        Think of these as the columns for the dataframe. There will be
        one for the current day, one for the quantities sold,
        one for the USDC received.

        [ [ [], [], [] ] , [ [], [], [] ], [ [], [], [] ] ]
        '''
        for tier, _ in enumerate(self.logs):
            self.logs[tier][0].append(self._days_elapsed) # Day index
            self.logs[tier][1].append(self.ticket_registry[tier + 1]['Quantities Sold']) # Quantities index
            self.logs[tier][2].append(self.ticket_registry[tier + 1]['USDC Received']) # USDC index

    def ticket_price_query(self, tier: int) -> float:
        '''
        Before a purchase, Attendees make a price query.
        The Market takes into account the Attendee's desired
        seating level / tier before sending back the price quote.

        return is BASE_TICKET_PRICE * TIER_MULTIPIER ^ [TOTAL_TIERS - BUYER_TIER + 1]
        ex:
            For a Tier 5 buyer
            cost = 50 * 1.5 ^ (5 - 5)
                 = 50 * 1

            For a Tier 1 buyer
            cost = 50 * 1.5 ^ (5 - 1)
                 = 50 * 1.5 ^ 4
                 = 253.125
        '''
        return self.base_ticket_price * self.tier_multiplier ** self.tiers - tier


    def construct_tier_plot(self, tier, index_number):
        # Create figure with secondary y-axis
        fig = make_subplots(specs=[[{"secondary_y": True}]])

        # Add traces
        fig.add_trace(
            go.Scatter(x=[i+1 for i in range(Config.sim_confs['days']) ], y=tier[1], name="Tickets"),
            secondary_y=False,
        )

        fig.add_trace(
            go.Scatter(x=[i+1 for i in range(Config.sim_confs['days']) ], y=tier[2], name="USDC"),
            secondary_y=True,
        )

        # Add figure title
        fig.update_layout(
            title_text=f"Sales of Tier-{index_number + 1}"
        )

        # Set x-axis title
        fig.update_xaxes(title_text="Days")

        # Set y-axes titles
        fig.update_yaxes(title_text="<b>Tickets</b> sold", secondary_y=False)
        fig.update_yaxes(title_text="<b>UDSC</b> collected", secondary_y=True)
        return fig.to_json()

    def export_plots(self):

        tier_plots = []

        for index, tier in enumerate(self.logs):
            tier_plots.append(self.construct_tier_plot(tier, index))

        return tier_plots

    def purchase_ticket(self, payment: dict) -> None:
        '''
        A ticket is purchased. Method receives a dict
        containing the Ticket's tier and payment amount.
        USDC earned and tickets sold for that tier is updated.
        '''
        rounded: float = round(payment['Payment'])
        self.USDC_received += rounded
        self.ticket_registry[payment['Tier']]['Quantities Sold']  += 1
        self.ticket_registry[payment['Tier']]['USDC Received']  += rounded
