from typing import Any
from timeit import default_timer as timer
from aaa.sim_handler import SimHandler
from aaa.logger import pkg_logger as pl


def test_received_config() -> dict:
    return {}

def run_sim(configs: dict = {}) -> Any:

    start = timer()
    conf_to_submit: dict = configs | test_received_config()
    sim = SimHandler()

    sim.run()

if __name__ == "__main__":
    run_sim()

