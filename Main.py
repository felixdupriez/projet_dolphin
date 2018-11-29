from DataframeOperations import *
from Toolbox import *
from Conversion import *
from Test import *

def generate_correlation_csv():
    df = import_csv('export6')
    filtered_df = df[df['CLOSE_2012_01_02'].notnull()]
    filtered_df = filtered_df.sort_values('Sharpe', ascending=False)
    correlation = df_correlation(filtered_df['ASSET_DATABASE_ID'].tolist())
    export_as_csv(correlation, "asset_correlation", index=True)


if __name__ == '__main__':
    df = import_csv('asset_correlation')
    df.set_index('Index', inplace=True)
    print('End')
