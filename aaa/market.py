from aaa.temporal import Temporal

class Market(Temporal):

    def __init__(self, seating_levels: int) -> None:
        super().__init__()

        # Configurables
        self.base_ticket_price: float = 50
        self.tier_multiplier: float = 1.5

        # States
        self.ticket_registry: dict = self.prepare_ticket_registry(seating_levels)
        self.USDC_received: float = 0
        self._days_elapsed: int = 0

    def __repr__(self) -> str:
        '''
        A convoluted REPR repr because I really want
        the market results to print beautifully.
        '''
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

        self.base_ticket_price *= 1.05
        self._days_elapsed += 1

    def log_day(self) -> None:
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
        rounded: float = round(payment['Payment'])
        self.USDC_received += rounded
        self.ticket_registry[payment['Tier']]['Quantities Sold']  += 1
        self.ticket_registry[payment['Tier']]['USDC Received']  += rounded
