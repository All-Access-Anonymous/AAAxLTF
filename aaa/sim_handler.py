from typing import List
from aaa import Config
from aaa.attendee import Attendee
from aaa.temporal import Temporal
from aaa.logger import pkg_logger as pl

Log = pl.Logger().get_logger()

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
        self.configs: dict = self.load_config(configs)

    def load_config(self, config: dict) -> None:
        '''
        If no configuration was provided, we source a
        default
        '''
        if not config:
            self.config: dict = Config.sim_confs

    def prepare_attendees(self, player_count: int):
        return [ Attendee() for _ in range(player_count) ]

    def run(self) -> None | dict:

        attendees: List[Attendee] = self.prepare_attendees(self.config['player_count'])

        for _ in range(self.config["days"]):
            Temporal.elapse_day()
            #Log.debug("Hmm")

        #print(attendees)


