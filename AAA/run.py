## import class objects 
from user import User
from bond import Bond
from staked_AHM import Staked_AHM
from config import sim_conf

u1 = User(sim_conf)
u2 = User(sim_conf)
u3 = User(sim_conf)
u4 = User(sim_conf)

print(User.all)

s1 = Staked_AHM()

s1.stake_AHM(u1, 20)

print(User.all)