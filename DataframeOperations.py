from Toolbox import get_data, json_to_data_frame, df_to_value, get_quote, get_ratio, post_data
import numpy as np
import pandas as pd
import json


def export_as_csv(df, name, index=False):
    df.to_csv(name, sep='\t', encoding='utf-8', index=index)


def import_csv(file, export=False):
    df = pd.read_csv(file, sep='\t')
    if export:
        return df_string_to_float(df)
    else:
        return df


def df_with_asset():
    result = get_data("/asset", columns=['ASSET_DATABASE_ID', 'LABEL', 'CURRENCY', 'TYPE', 'SUB_TYPE', 'MODIFICATION_DATE'])
    df = json_to_data_frame(result)
    df = df_to_value(df)
    return df


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


def get_ratio_asset(asset, ratio):
    data = json.dumps({
        'asset': [asset],
        'ratio': [ratio],
        'start_date': '2012-01-02',
        'end_date': '2018-08-31'
    })
    result = post_data("/ratio/invoke", json=data)
    if result == '[]':
        return
    return json.loads(result)[str(asset)][str(ratio)]['value']


def add_ratio_col_sharpe(df):
    for index, row in df.iterrows():
        df.loc[index, "Sharpe2"] = get_ratio_asset(index, 20)
    return df


def first_close(df):
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


def get_correlation(asset_list, benchmark):
    correlation = 19
    content = json.dumps({'ratio': [correlation],
            'asset': asset_list,
            'benchmark': benchmark,
            'start_date': '2012-02-01',
            'end_date': '2018-08-01',
            'frequency': None})
    return post_data("/ratio/invoke", json=content)


def df_correlation(assets):
    corr = pd.DataFrame(np.zeros(shape=(298, 298)), columns=assets, index=assets)
    line = 1
    for asset in assets:
        print("Ligne %d/%d" % (line, 298))
        line += 1
        corr_json = json.loads(get_correlation(assets, asset))
        for key in corr_json:
            value = float(corr_json[key]['19']['value'].replace(',', '.'))
            corr[asset][int(key)] = value
            print(corr[asset][int(key)])
    return corr


def df_string_to_float(df):
    df.Performance = df.Performance.str.replace(',', '.')
    df.Performance = df.Performance.astype(float)
    df.Sharpe = df.Sharpe.str.replace(',', '.')
    df.Sharpe = df.Sharpe.astype(float)
    df.Volatility = df.Volatility.str.replace(',', '.')
    df.Volatility = df.Volatility.astype(float)
    return df