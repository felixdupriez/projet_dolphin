from DataframeOperations import *
from Toolbox import *
from Conversion import *

def test_conversion():
    df = import_csv('export6')
    filtered_df = df[df['CLOSE_2012_01_02'].notnull()]
    filtered_df = filtered_df.sort_values('Sharpe', ascending=False)
    currs = get_unique_currs(filtered_df)
    rates = get_conversion_rates(currs)
    test = convert_to_eur(rates, filtered_df, "CLOSE_2012_01_02")
    export_as_csv(test, "test_curr_convert")

if __name__ == '__main__':
    test_conversion()