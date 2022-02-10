from typing import List, Dict
from aaa.temporal import Temporal

class Attendee(Temporal):

    inst_count: int = 0
    attendee_instances: List = []


    def __init__(self, received_conf: Dict = {}):
        super().__init__()
        self.USDC_balance: float = 10
        self.ticket: List = []
        self.id: int = Attendee.inst_count
        self._days_elapsed: int = 0

        Attendee.inst_count += 1
        Attendee.attendee_instances.append(self)


    def __repr__(self):
        return f'ATTN-{self.id}-{self.USDC_balance}'


    def day_pass(self) -> None:
        self._days_elapsed += 1
        self.day_assess()


    def day_assess(self) -> None:
        '''
        day_assess contains the daily responsibilities
        assigned to each instance of this class.
        '''
        self.USDC_balance += 2


    @property
    def days_elapsed(self) -> int | None:
        return self._days_elapsed

