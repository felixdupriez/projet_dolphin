import json
import pandas as pd


def json_to_data(content):
    data = json.loads(content)
    df = pd.DataFrame.from_records(data)
    return df


