from typing import List, Dict

class Attendee(Temporal):

    inst_count: int = 0
    attendee_instances: List = []


    def __init__(self, received_conf: Dict = {}):
        self.USDC_balance: float = 50
        self.ticket: List = []
        self.id: int = Attendee.inst_count

        Attendee.inst_count += 1
        Attendee.attendee_instances.append(self)

    def __repr__(self):
        return f'ATTN-{self.id}-{self.USDC_balance}'
