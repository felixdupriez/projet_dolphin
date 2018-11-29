from DataframeOperations import *
from Toolbox import *
from Conversion import *

if __name__ == '__main__':
    df = import_csv('export6')
    filtered_df = df[df['CLOSE_2012_01_02'].notnull()]
    filtered_df = filtered_df.sort_values('Sharpe', ascending=False)
    correlation = df_correlation(filtered_df)
    export_as_csv(correlation, "correlation")
    print('End')
