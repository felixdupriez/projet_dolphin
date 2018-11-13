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


def get_quote(asset_id, start_date, end_date):
    payload = {'start_date': start_date, 'end_date': end_date}
    stock_nav = get_data("/asset/" + asset_id + "/quote", payload=payload)
    if stock_nav == '[]':
        return
    return json.loads(stock_nav)[0]['nav']['value']


def add_nav_col(df, column_name, start_date, end_date):
    df[column_name] = 0
    for index, row in df.iterrows():
        df.loc[index, column_name] = get_quote(row.ASSET_DATABASE_ID, start_date, end_date)
    df[column_name] = df[column_name].str.replace(',', ".").astype(float)
    return df


if __name__ == '__main__':
    #result = get_data("/asset", columns=['ASSET_DATABASE_ID', 'LABEL', 'TYPE', 'MODIFICATION_DATE', 'CURRENCY'])
    #df = json_to_data_frame(result)
    #df = df_to_value(df)
    #df = add_nav_col(df, 'NAV_2012_01_02', '2012-01-02', '2012-01-02')
    #df = add_nav_col(df, 'NAV_2018_11_12', '2018-11-13', '2018-11-13')
    #df.to_csv('export', sep='\t', encoding='utf-8', index=False)      #Exporter le Dataframe en csv
    #df = df[df.TYPE == "STOCK"]
    #df = add_nav_col(df, 'NAV_2012_01_02')
    #df.to_csv('export', sep='\t', encoding='utf-8', index=False)
    df = pd.read_csv('export', sep='\t')
    df = df[(df.NAV_2012_01_02 >= 1) & (df.NAV_2012_01_02 <= 10) & (df.TYPE == 'STOCK')]
    print("Nombre d'action avec un NAV entre 1% et 10% au 2 janvier 2012 :", len(df.index))
    #print('test')
