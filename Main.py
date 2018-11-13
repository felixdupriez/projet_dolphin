import requests
import os
import urllib3
from Toolbox import json_to_data, df_to_value

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


def get_data(endpointapi, date=None, full_response=False, columns=list()):
    payload = {'date': date, 'fullResponse': full_response}
    res = requests.get(URL + endpointapi + columns_to_str(columns), params=payload, auth=AUTH, verify=False)
    return res.content.decode('utf-8')


if __name__ == '__main__':
    result = get_data("/asset", columns=['ASSET_DATABASE_ID', 'LABEL', 'TYPE'])
    df = json_to_data(result)
    df = df_to_value(df)
    df = df[df.TYPE == "STOCK"]
    print("End")
