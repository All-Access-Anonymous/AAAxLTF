from defi.sim_handler import SimHandler
from defi.config import sim_conf
# import os
# os.remove("simulation.log") 

s = SimHandler(sim_conf)
df, dfa, f = s.run()

print('DF')
print(df)
print('DFA')
print(dfa)