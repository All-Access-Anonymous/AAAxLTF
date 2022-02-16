from aaa.temporal import Temporal

class Market(Temporal):

    def __init__(self) -> None:
        super().__init__()

        # Configurables
        self.base_ticket_price: float = 200
        self.tier_multiplier: float = 1.5

        # States
        self.ticket_registry: dict = self.prepare_ticket_registry()
        self.USDC_received: float = 0
        self._days_elapsed: int = 0

    def __repr__(self) -> str:
        return f'MAR - {self.ticket_registry} - {self.USDC_received}'

    def prepare_ticket_registry(self) -> dict:
        '''
        Before the market is able to accept any transactions
        and record the purchases to ticket registry,
        it must first derive how many tiers there are because
        that determines how many keys there will be for the
        ticket registry.
        '''

        return {
            1: 0,
            2: 0,
            3: 0,
            4: 0,
            5: 0,
        }

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

        self.base_ticket_price *= 1.05
        self._days_elapsed += 1

    def log_day(self) -> None:
        '''
        Inherited from Temporal
        '''
        pass

    def ticket_price_query(self, tier: int) -> float:
        '''
        Before a purchase, Attendees make a price query.
        The Market takes into account the Attendee's desired
        seating level / tier before sending back the price quote.
        '''
        return self.base_ticket_price * self.tier_multiplier * tier

    def purchase_ticket(self, payment: dict) -> None:
        '''
        A ticket is purchased. Method receives a dict
        containing the Ticket's tier and payment amount.
        USDC earned and tickets sold for that tier is updated.
        '''
        self.USDC_received += payment['Payment']
        self.ticket_registry[payment['Tier']]  += 1
