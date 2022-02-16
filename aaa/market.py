from aaa.temporal import Temporal

class Market(Temporal):

    def __init__(self) -> None:
        super().__init__()
        self.current_ticket_price: float = 200
        self.tickets_sold: int = 0
        self.USDC_received: float = 0
        self._days_elapsed: int = 0

    def __repr__(self) -> str:
        return f'MAR-{self.tickets_sold}-{self.USDC_received}'

    @property
    def days_elapsed(self) -> int:
        return self._days_elapsed

    def day_pass(self) -> None:
        self.current_ticket_price *= 1.05
        self._days_elapsed += 1

    def log_day(self) -> None:
        pass

    def purchase_ticket(self, payment: float) -> None:
        self.USDC_received += payment
        self.tickets_sold += 1

    def ticket_price_query(self):
        return self.current_ticket_price
