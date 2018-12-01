import json
import pandas as pd
import requests
import os
import urllib3


urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
URL = os.environ['URL']
AUTH = (os.environ['USERNAME'], os.environ['PASSWORD'])


def json_to_data_frame(content):
    data = json.loads(content)
    df = pd.DataFrame.from_records(data)
    return df


def get_value_from_dict(content):
    return content['value']


def df_to_value(df):
    for column in df:
        df[column] = df.apply(lambda row: get_value_from_dict(row[column]), axis=1)
    return df


def get_data(endpointapi, date=None, full_response=False, columns=list(), payload=None):
    if payload is None:
        payload = {'date': date, 'fullResponse': full_response}
    res = requests.get(URL + endpointapi + columns_to_str(columns), params=payload, auth=AUTH, verify=False)
    return res.content.decode('utf-8')


def post_data(endpointapi, date=None, full_response=False, columns=list(), json=None):
    if json is None:
        json = {'date': date, 'fullResponse': full_response}
    res = requests.post(URL + endpointapi + columns_to_str(columns), data=json, auth=AUTH, verify=False)
    return res.content.decode('utf-8')


def put_data(endpointapi, date=None, full_response=False, columns=list(), json=None):
    if json is None:
        json = {'date': date, 'fullResponse': full_response}
    res = requests.put(URL + endpointapi + columns_to_str(columns), json=json, auth=AUTH, verify=False)
    return res.content.decode('utf-8')


def get_ratios(assets_id):
    sharpe_id = 20
    performance_id = 21
    volatility_id = 18
    for asset_id in assets_id:
        json = {"ratio": [sharpe_id, performance_id, volatility_id], "asset": [asset_id]}
        ratio_invoke = post_data("/ratio/invoke", json=json)
    if ratio_invoke == '[]':
        return
    return ratio_invoke


def get_ratio(asset_id):
    sharpe_id = 20
    performance_id = 21
    volatility_id = 18
    json = {"ratio": [sharpe_id, performance_id, volatility_id], "asset": [asset_id]}
    ratio_invoke = post_data("/ratio/invoke", json=json)
    if ratio_invoke == '[]':
        return
    return ratio_invoke


def columns_to_str(columns):
    if len(columns) <= 0:
        return ''
    res = '?columns=' + columns.pop()
    for c in columns:
        res += '&columns=' + c
    return res


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


def get_sharpe_portfolio():
    data = json.dumps({
        'asset': [1031],
        'ratio': [20],
        'start_date': '2012-01-02',
        'end_date': '2018-08-31'
    })
    result = post_data("/ratio/invoke", json=data)
    if result == '[]':
        return
    return json.loads(result)['1031']['20']['value']


def get_portfolio():
    portfolio_id = "1031"
    portfolio = get_data("/portfolio/" + portfolio_id +"/dyn_amount_compo")
    if portfolio == '[]':
        return
    return portfolio


# json = {
#     "currency":
#         {
#             "code": "EUR"
#         },
#     "label": "epita_ptf_4",
#     "type": "front",
#     "values":
#         {
#             "2012-01-02":
#                 [
#                     {
#                         "asset":
#                             {
#                                 "asset": 906, "quantity": 2
#                             }
#                     },
#                     {
#                         "asset":
#                             {
#                                 "asset": 899, "quantity": 1
#                             }
#                     }
#                 ]
#         }
# }
def put_portfolio(portfolio):
    portfolio_id = "1031"
    my_assets = "{\"currency\":{\"code\":\"EUR\"},\"label\":\"epita_ptf_4\",\"type\":\"front\",\"values\":{\"2012-01-02\":[{\"asset\": { \"asset\": "
    for item in portfolio.items[:-1]:
        my_assets += str(item.asset) + ", \"quantity\": " + str(item.qty) + "}}, {\"asset\": { \"asset\": "
    my_assets += str(portfolio.items[-1].asset) + ", \"quantity\": " + str(item.qty) + "}}]}}"
    my_json = json.loads(my_assets)
    portfolio = put_data("/portfolio/" + portfolio_id + "/dyn_amount_compo", json=my_json)
    if portfolio == '[]':
        return
    return portfolio


def put_portfolio_exemple():
    portfolio_id = "1031"
    json = {
        "currency":
            {
                "code": "EUR"
            },
        "label": "epita_ptf_4",
        "type": "front",
        "values":
            {
                "2012-01-02":
                    [
                        {
                            "asset":
                                {
                                    "asset": 906, "quantity": 2
                                }
                        },
                        {
                            "asset":
                                {
                                    "asset": 899, "quantity": 1
                                }
                        }
                    ]
            }
    }
    portfolio = put_data("/portfolio/" + portfolio_id + "/dyn_amount_compo", json=json)
    if portfolio == '[]':
        return
    return portfolio


#Fix later
def compute_sharpe(df):
    ref = 0 #Taux de placement sans riques
    ret = 0 #Rendement de l'actif sur la période
    vola = 0 #Volatilité de l'actif
    sharpe = (ret - ref)/vola
    return sharpe
