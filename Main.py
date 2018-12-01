from DataframeOperations import *
from Toolbox import *
from Conversion import *
from Test import *
from Portfolio import *
from Asset import *
from Correlation import *

def generate_correlation_csv():
    df = import_csv('export6')
    filtered_df = df[df['CLOSE_2012_01_02'].notnull()]
    filtered_df = filtered_df.sort_values('Sharpe', ascending=False)
    correlation = df_correlation(filtered_df['ASSET_DATABASE_ID'].tolist())
    export_as_csv(correlation, "asset_correlation", index=True)


def print_portfolio(p):
    for item in p.items:
        print("%d, %d, %d" % (item.asset, item.price, item.qty))


if __name__ == '__main__':
    df = import_csv('df_result_20_best')
    p = Portfolio(df)
    p.generate()
    print_portfolio(p)
    put_portfolio(p)
    print('End')
