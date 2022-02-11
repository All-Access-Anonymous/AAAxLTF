from typing import List, Dict
from aaa.temporal import Temporal

class Attendee(Temporal):

    inst_count: int = 0
    attendee_instances: List = []


    def __init__(self, received_conf: Dict = {},
                       seating_tier: int = 0):
        super().__init__()
        self.seating_tier = seating_tier
        self.USDC_balance: float = 10
        self.ticket: List = []
        self.id: int = Attendee.inst_count
        self._days_elapsed: int = 0

        Attendee.inst_count += 1
        Attendee.attendee_instances.append(self)


    def __repr__(self):
        """
        String representation when evaluated.
        """
        return f'ATTN-{self.id}-{self.seating_tier}'


    def day_pass(self) -> None:
        """
        Inherited from Temporal ABC
        This will be called by Temporal to initiate
        this instance's daily routines / responsibilities.
        """
        self._days_elapsed += 1
        self.day_assess()


    def day_assess(self) -> None:
        """
        day_assess contains the daily responsibilities
        assigned to each instance of this class.
        """
        pass

    @property
    def days_elapsed(self) -> int | None:
        """
        Inherited from Temporal ABC.
        Returns the days elapsed for this object but
        without needing to call this as a function.
        """
        return self._days_elapsed

    def predecide_buy_day(self) -> int:
        pass
