    from DataframeOperations import import_csv


if __name__ == '__main__':
    df = import_csv('export6')
    df.set_index('Index', inplace=True)
    print('End')