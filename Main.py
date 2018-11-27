import requests
import os
import urllib3
import json
import pandas as pd
from Toolbox import json_to_data_frame, df_to_value

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
URL = os.environ['URL']
AUTH = (os.environ['USERNAME'], os.environ['PASSWORD'])


def columns_to_str(columns):
    if len(columns) <= 0:
        return ''
    res = '?columns=' + columns.pop()
    for c in columns:
        res += '&columns=' + c
    return res


def get_data(endpointapi, date=None, full_response=False, columns=list(), payload=None):
    if payload is None:
        payload = {'date': date, 'fullResponse': full_response}
    res = requests.get(URL + endpointapi + columns_to_str(columns), params=payload, auth=AUTH, verify=False)
    return res.content.decode('utf-8')


def post_data(endpointapi, date=None, full_response=False, columns=list(), json=None):
    if json is None:
        json = {'date': date, 'fullResponse': full_response}
    res = requests.post(URL + endpointapi + columns_to_str(columns), json=json, auth=AUTH, verify=False)
    return res.content.decode('utf-8')


def get_quote(asset_id, start_date, end_date):
    payload = {'start_date': start_date, 'end_date': end_date}
    stock_nav = get_data("/asset/" + asset_id + "/quote", payload=payload)
    if stock_nav == '[]':
        return
    return json.loads(stock_nav)[0]['close']['value']


def get_ratio(asset_id):
    sharpe_id = 20
    performance_id = 21
    volatility_id = 18
    json = {"ratio": [sharpe_id, performance_id, volatility_id], "asset": [asset_id]}
    ratio_invoke = post_data("/ratio/invoke", json=json)
    if ratio_invoke == '[]':
        return
    return ratio_invoke


def get_ratios(assets_id):
    sharpe_id = 20
    performance_id = 21
    volatility_id = 18
    for asset_id in assets_id :
        json = {"ratio": [sharpe_id, performance_id, volatility_id], "asset": [asset_id]}
        ratio_invoke = post_data("/ratio/invoke", json=json)

    if ratio_invoke == '[]':
        return
    return ratio_invoke


def add_nav_col(df, column_name, start_date, end_date):
    df[column_name] = 0
    for index, row in df.iterrows():
        df.loc[index, column_name] = get_quote(str(row.ASSET_DATABASE_ID), start_date, end_date)
    df[column_name] = df[column_name].str.replace(',', ".").astype(float)
    return df


def add_ratio_col(df):
    df_size = len(df.index)
    for index, row in df.iterrows():
        data = get_ratio(row.ASSET_DATABASE_ID)
        data = json.loads(data)["%s" % row.ASSET_DATABASE_ID]
        df.loc[index, "Sharpe"] = data["20"]["value"]
        df.loc[index, "Performance"] = data["21"]["value"]
        df.loc[index, "Volatility"] = data["18"]["value"]
        print("%d / %d" % (index, df_size))
    return df


def convert_currency(df):
    df['CLOSE_2012_01_02'] = df['CLOSE_2012_01_02'].apply(lambda x: x * 0.88 if x.CURRENCY == 'USD' else x)
    print('test')
    return df

def get_unique_curr(df):
    currs = df.CURRENCY.unique()
    return currs

if __name__ == '__main__':
    #result = get_data("/asset", columns=['ASSET_DATABASE_ID', 'LABEL', 'CURRENCY', 'TYPE', 'SUB_TYPE', 'MODIFICATION_DATE'])
    #df = json_to_data_frame(result)
    #df = df_to_value(df)
    df = pd.read_csv('export4', sep='\t')
    df = df[(df['CLOSE_2012_01_02'].notna()) | (df['CLOSE_2012_01_03'].notna())] #Conserver uniquement les actifs qui un prix de close
    df['FIRST_CLOSE'] = df['CLOSE_2012_01_02']
    for index, row in df.iterrows():
        print(df.loc[index, "CLOSE_2012_01_02"])
        if pd.isna(df.loc[index, "FIRST_CLOSE"]):
            df.loc[index, "FIRST_CLOSE"] = df.loc[index, "CLOSE_2012_01_03"]
    df = df.drop('CLOSE_2012_01_03', 1)
    df = df.drop('CLOSE_2012_01_02', 1)
    df.to_csv('export5', sep='\t', encoding='utf-8', index=False)

    #df = add_nav_col(df, 'CLOSE_2012_01_03', '2012-01-03', '2012-01-03')
    #df.to_csv('export4', sep='\t', encoding='utf-8', index=False)      #Exporter le Dataframe en csv
    #df = df[df.TYPE == "STOCK"]
    #df = convert_currency(df)
    #df['CURRENCY'] = df.filter(like='USD', axis=1)['CURRENCY'].apply(lambda x: x * 0.88)
    #df = df[(df.NAV_2012_01_02 >= 1) & (df.NAV_2012_01_02 <= 10)]
    #df = df.sort_values(by=['Sharpe'], ascending=False)
    #df = df[(df.NAV_2012_01_02 >= 1) & (df.NAV_2012_01_02 <= 10) & (df.TYPE == 'STOCK')]
    #df = add_ratio_col(df)
    #df.to_csv('export2', sep='\t', encoding='utf-8', index=False)
    #df = add_nav_col(df, [18, 20, 21])
    print('test')
