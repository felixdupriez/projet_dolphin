import json
import pandas as pd


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

