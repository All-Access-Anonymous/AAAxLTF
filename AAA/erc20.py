from typing import List, Dict
from aaa.temporal import Temporal

class ERC20(Temporal):

    id: int = 0
    all: List = []

    def __init__(self, received_conf: Dict = {},
                       seating_tier: int = 0):
        super().__init__()
        self.name = erc20_token_name
        self.id: int = ERC20.id
        self._days_elapsed: int = 0

        ERC20.id += 1
        ERC20.all.append(self)


    def __repr__(self):
        """
        String representation when evaluated.
        """
        return f'ERC20-{self.name}'


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