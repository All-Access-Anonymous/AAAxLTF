from typing import List, Dict
from aaa.temporal import Temporal

class Attendee(Temporal):

    inst_count: int = 0
    attendee_instances: List = []


    def __init__(self, received_conf: Dict = {},
                       buy_day: int = 0,
                       seating_tier: int = 0):
        super().__init__()
        self.seating_tier = seating_tier
        self.USDC_balance: float = 1000
        self.ticket: List = []
        self.id: int = Attendee.inst_count
        self.buy_day: int = buy_day
        self._days_elapsed: int = 0

        Attendee.inst_count += 1
        Attendee.attendee_instances.append(self)


    def __repr__(self):
        """
        String representation when evaluated.
        """
        return f'ATTN-{self.id}-{self.seating_tier}-{self.buy_day}-{self.ticket}'


    def day_pass(self) -> None:
        """
        Inherited from Temporal ABC
        This will be called by Temporal to initiate
        this instance's daily routines / responsibilities.
        """
        self._days_elapsed += 1
        self.day_assess()

    def buy_ticket(self) -> None:

        ticket_cost: float = self.mediator.ticket_price_query() # type: ignore (Runtime attribute)
        self.mediator.purchase_ticket(ticket_cost)              # type: ignore (Runtime attribute)
        # self.USDC_balance -= ticket_cost
        self.ticket.append("Ticket")

        '''
        if self.USDC_balance >= ticket_cost:
            self.mediator.purchase_ticket(ticket_cost)          # type: ignore (Runtime attribute)
            self.USDC_balance -= ticket_cost
            self.ticket.append("Ticket")
        else:
            print(f"{self} can't afford {ticket_cost} ")
        '''

    def day_assess(self) -> None:
        """
        day_assess contains the daily responsibilities
        assigned to each instance of this class.
        """
        if self.buy_day == self.days_elapsed:
            self.buy_ticket()

    @property
    def days_elapsed(self) -> int | None:
        """
        Inherited from Temporal ABC.
        Returns the days elapsed for this object but
        without needing to call this as a function.
        """
        return self._days_elapsed
