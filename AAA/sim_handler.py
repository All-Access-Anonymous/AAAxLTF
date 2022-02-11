class SimHandler:
    """
    Responsiblities:
        Instantiate Attender based on Series level (A, AA, AAA)
        Instantiate Ticket Market, with varying prices based on Tier Partitions.
            For Series A - 1 Partition
            For Series AA - 3 Partitions
            For Series AA - 5-7 Partitions

        Let ticket market take a JSON as configs for
        every object
    """

    def __init__(self, configs: dict = {}):
        self.config = self.load_config(configs)
        self.market = None

    @staticmethod
    def load_config(config: dict):
        if not config:
            print("No config")
        return {  }

    def run(self) -> None | dict:
        pass
