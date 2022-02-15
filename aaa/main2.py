from aaa.schema import SimConfig
from aaa.buy_day_generator import reduce, generate_buy_days

#a = SimConfig()

DAYS_TILL_CONCERT: int = 60
POPULATION = 50

float_buy_days = generate_buy_days(POPULATION, DAYS_TILL_CONCERT)
rounded_buy_days = [round(i) for i in float_buy_days]
print(float_buy_days)
print(rounded_buy_days)

