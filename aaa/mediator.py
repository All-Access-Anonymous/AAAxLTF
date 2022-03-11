from aaa.logger import pkg_logger as pl
import numpy as np

Log = pl.Logger().get_logger()

class BaseMediator():
    '''
    Generic Mediator
    '''

    def __init__(self, *args) -> None:
        """
        The generic mediator must take on a variable number of 'colleagues'
        """
        self.colleague_list = list(args)

    def __repr__(self) -> str:

        msg = 'Mediator object.\nCurrently watching:\n'
        for colleague in self.colleague_list:
            msg = msg + \
                f'Colleague: {colleague}\nType: type{type(colleague)}\n'
        return msg


class Mediator(BaseMediator):

    def __init__(self, *args) -> None:
        Log.info("Mediator instantiated.")
        # Log.info(f"Mediator has received: {args}")
        '''
        Objects of various kinds will be passed onto the mediator
        to be registered and to allow for intercommunication.

        Since there will be a variable number of users in the system,
        the provided argument for the mediator will be in a pattern like so:
         (wooshi_market, player_market, wooshi_pool, *players)

        This way, we can pop the first few arguments to be recognized as
        distinct models in the system and the rest of *args
        can be looped through as Attendees.
        '''
        super().__init__(*args)

        self.market = self.colleague_list[0]
        self.market.mediator = self
        self.colleague_list.pop(0)

        # Users don't require special distinction
        # so we can safely loop through them
        for attendee in self.colleague_list:
            attendee.mediator = self

    def ticket_price_query(self, seating_tier: int) -> float:
        '''
        Invocation of the Market object's ticket
        price query to send price information back to an Attendee.
        '''
        return self.market.ticket_price_query(seating_tier)

    def purchase_ticket(self, payment: dict) -> None:
        '''
        The player sends a signal to make a purchase,
        Mediator invokes the Market's purchase_ticket() method.
        '''
        self.market.purchase_ticket(payment)
