from multiprocessing.dummy import Pool as ThreadPool
import json


class Correlation:
    def __init__(self, index, column):
        self.index = index
        self.column = column
        self.res = None


def get_correlation(corr):
    tmp = get_correlation(int(corr.index), int(corr.column))
    tmp = json.loads(tmp)[str(corr.index)]['19']['value']
    tmp = float(tmp.replace(',', '.'))
    corr.res = tmp
    return tmp


# function to be mapped over
def calculateparallel(corr, threads=10):
    pool = ThreadPool(threads)
    results = pool.map(get_correlation, corr)
    pool.close()
    pool.join()
    return results


def launch_thread_pool(index, id_list):
    correlations = []
    for column in id_list:
        corr = Correlation(index, column)
        res = calculateparallel(corr)
        correlations.append(corr)
    print('end')
