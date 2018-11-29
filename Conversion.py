import json
import pandas as pd
from Main import *

def get_unique_currs(df):
    currs = df.CURRENCY.unique()
    return currs

#Taux au 2 janvier 2012
def get_conversion_rates(currs):
    payload = {'start_date': '2012-01-02', 'end_date': '2012-01-02'}
    rates = {}
    for curr in currs:
        rate = get_data("/currency/rates/" + curr + "/to/EUR", payload=payload)
        rate = json.loads(rate)[0]["rate"]["value"]
        rate = rate.replace(",", ".")
        rates[curr] = float(rate)
    return rates

def convert_to_eur(rates, df):
    for index, row in df.iterrows():
        curr = df.at[index, "CURRENCY"]
        amount = df.at[index, "CLOSE_2012_01_02"]
        amount = amount / rates.get(curr)
        df.loc[index, "CLOSE_2012_01_02"] = amount
        df.loc[index, "CURRENCY"] = 'EUR'
    return df