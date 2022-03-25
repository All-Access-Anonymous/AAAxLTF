from defi.sim_handler import SimHandler
from defi.config import sim_conf
# import os
# os.remove("simulation.log") 

s = SimHandler(sim_conf)
res = s.run()

print('DF')
print(res['df'])
print('DFA')
print(res['dfa'])