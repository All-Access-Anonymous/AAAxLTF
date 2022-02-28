from typing import Any
from timeit import default_timer as timer
from aaa.sim_handler import SimHandler
from aaa.logger import pkg_logger as pl
from aaa.schema import AttendeeConfig, MarketConfig, SimConfig
from aaa import Config


Log = pl.Logger().get_logger()

def test_received_config() -> dict:
    # This is indeed a dictionary

    print(Config.sim_confs)
    return Config.sim_confs

def run_sim(configs: dict = {}) -> Any:

    conf_to_submit: dict = configs | test_received_config()
    validated_conf = SimConfig(**conf_to_submit)

    sim = SimHandler(conf_to_submit)
    return sim.run()



if __name__ == "__main__":

    start = timer()
    sim_res: dict = run_sim()
    end = timer()
    Log.info(f'Simulation time: {end - start}')
    print(sim_res)

