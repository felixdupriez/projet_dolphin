from Toolbox import get_data, json_to_data_frame, df_to_value, get_quote, get_ratio, post_data
import numpy as np
import pandas as pd
import json


def export_as_csv(df, name):
    df.to_csv(name, sep='\t', encoding='utf-8', index=False)


def import_csv(file):
    return pd.read_csv(file, sep='\t')


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


def get_correlation(asset_id, benchmark):
    correlation = 19
    content = json.dumps({'ratio': [correlation],
            'asset': [asset_id],
            'benchmark': benchmark,
            'start_date': '2012-02-01',
            'end_date': '2018-08-01',
            'frequency': None})
    return post_data("/ratio/invoke", json=content)


def df_correlation(filtered_df):
    listofitems = filtered_df['ASSET_DATABASE_ID'].tolist()
    corr = pd.DataFrame(np.zeros(shape=(298, 298)), columns=listofitems, index=listofitems)
    line = 0
    for index, row in corr.iterrows():
        print("Ligne %d/%d" % (++line, 298))
        for column in corr:
            if index == column:
                corr[index][column] = 1     # 0.99939795304
            elif corr[index][column] == 0:
                tmp = get_correlation(int(index), int(column))
                tmp = json.loads(tmp)[str(index)]['19']['value']
                tmp = float(tmp.replace(',', '.'))
                corr[index][column] = tmp
                corr[column][index] = tmp
    return corr
