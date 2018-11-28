import json
import pandas as pd
from Main import *


def get_unique_curr(df):
    currs = df.CURRENCY.unique()
    return currs

#Taux au 2 janvier 2012
def get_conversion_rates(currs):
    rates = []
    for curr in currs:
        rate = get_data("/currency/" + curr + "/to/EUR")
        rate = json.loads(rate)["rate"]["value"]
        rates.append(rate)
    return rates


def convert_to_eur(curr, amount):
    value = 0
    return value
