from typing import Any
from timeit import default_timer as timer


def test_received_config() -> dict:
    pass

def run_sim(configs: dict = {}) -> Any:

    start = timer()

    conf_to_submit: dict = configs | test_received_config()

    pass

