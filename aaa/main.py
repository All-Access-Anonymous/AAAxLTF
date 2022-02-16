from typing import Any
from timeit import default_timer as timer
from aaa.sim_handler import SimHandler
from aaa.logger import pkg_logger as pl
from aaa import Config


def test_received_config() -> dict:
    # This is indeed a dictionary
    return Config.sim_confs

def run_sim(configs: dict = {}) -> Any:

    start = timer()
    conf_to_submit: dict = configs | test_received_config()
    sim = SimHandler(conf_to_submit)

    sim.run()

if __name__ == "__main__":
    run_sim()

