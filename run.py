from defi.sim_handler import SimHandler
from defi.config import sim_conf
import pandas as pd
# import os
# os.remove("simulation.log") 

s = SimHandler(sim_conf)
res = s.run()

print('DF')
print(pd.read_json(res['df']))
print('DFA')
print(pd.read_json(res['dfa']))