from DataframeOperations import import_csv, export_as_csv
from Asset import *
from Conversion import *


def magic_formula(sharpe, perf, vol):
    return sharpe + perf - (10 * vol)


def magic_power():
    df = import_csv('export6', export=True)
    df['Ponderation'] = df.apply(lambda x: magic_formula(x['Sharpe'], x['Performance'], x['Volatility']), axis=1)
    df = df[df['CLOSE_2012_01_02'].notnull()]
    df = df.sort_values('Ponderation', ascending=False)
    id_list = df[0:50]['ASSET_DATABASE_ID'].tolist()
    return id_list


def get_csv_from_list(df, id_list):
    result = import_csv('df_base', export=True)
    for id in id_list:
        result = result.append(df.loc[id])
    return result


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

    print("END")
