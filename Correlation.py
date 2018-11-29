from DataframeOperations import import_csv
from Asset import *


def magic_formula(sharpe, perf, vol):
    return sharpe + perf - (10 * vol)


def magic_power():
    df = import_csv('export6', export=True)
    df['Ponderation'] = df.apply(lambda x: magic_formula(x['Sharpe'], x['Performance'], x['Volatility']), axis=1)
    df = df[df['CLOSE_2012_01_02'].notnull()]
    df = df.sort_values('Ponderation', ascending=False)
    id_list = df[0:50]['ASSET_DATABASE_ID'].tolist()
    return id_list


if __name__ == '__main__':
    id_list = magic_power()
    print("id_list1 : ")
    print(id_list)
    df = import_csv('asset_correlation')
    df.set_index('Index', inplace=True)
    dic = get_20_out_of_50(df, id_list)
    print("END")
