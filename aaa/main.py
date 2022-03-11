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

    conf_to_submit: dict = configs 
    validated_conf = SimConfig(**conf_to_submit)

    sim = SimHandler(conf_to_submit)
    return sim.run()



if __name__ == "__main__":

    start = timer()
    # Test config
    config={
      "days": 31,
      "buy_day_weights": [
        0.2,
        0.3,
        0.2,
        0.2,
        0.1
      ],
      "attendee_count": 200,
      "attendee_config": {
        "lateness": [
          0.5,
          0.9
        ]
      },
      "market_config": {
        "price_increase_multiplier": 1.05,
        "log_day": True
      },
      "seating_levels": 5
    }
    sim_res: dict = run_sim(config)
    end = timer()
    Log.info(f'Simulation time: {end - start}')
    print(sim_res)

