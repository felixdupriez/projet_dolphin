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
    id_list = magic_power()
    print("id_list1 : ")
    print(id_list)
    df = import_csv('asset_correlation')
    df.set_index('Index', inplace=True)
    dic = get_20_out_of_50(df, id_list)
    df_all = import_csv('export6', export=True)
    df_all.set_index('ASSET_DATABASE_ID', inplace=True)
    result = get_csv_from_list(df_all, id_list)

    #Convert and replace the currencies
    rates = get_conversion_rates(get_unique_currs(result))
    convert_to_eur(rates,result, "CLOSE_2012_01_02")


    result = result.reset_index()
    result = result.drop(['ASSET_DATABASE_ID'], axis=1)
    result = result.rename(index=str, columns={"index": "ASSET_DATABASE_ID"})
    export_as_csv(result, "df_result_20_best", index=False)

    df = import_csv('df_result_20_best')
    df = df.sort_values('CLOSE_2012_01_02', ascending=False)
    p = Portfolio(df)
    p.generate()
    print_portfolio(p)
    put_portfolio(p)
    print('End')
