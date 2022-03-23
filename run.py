from defi.sim_handler import SimHandler
from defi.config import sim_conf

s = SimHandler(sim_conf)
df, dfa, f = s.run()

print(df)