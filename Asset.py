class Asset:
  def __init__(self, id, currency, label, sub_type, type, close):
    self.id = id
    self.currency = currency
    self.label = label
    self.sub_type = sub_type
    self.type = type
    self.close = close


class AssetChosen:
    def __init__(self, asset, quantity):
        self.asset = asset
        self.quantity = quantity

    def get_nav(self):
        return self.asset.close * self.quantity


def check_portfolio(portfolio):
    assets = portfolio.assets
    if assets.amount() != 20:
        return False
    for asset in assets:
        if asset.get_nav() < (portfolio.sum / 100) or asset.get_nav() > (portfolio.sum / 10):
            return False
    return True


def get_sum_corr(df, id_list):
    dic = {}
    for id in id_list:
        sum = 0
        for id_ in id_list:
            sum += df[str(id)][id_]
        sum -= df[str(id)][id]
        dic[id] = abs(sum)
    return dic


def get_20_out_of_50(df, id_list):
    for i in range(6):
        dic = get_sum_corr(df, id_list)
        dic = sorted(dic.items(), reverse=True)
        for index, key in enumerate(dic):
            if index > 4:
                break
            del dic[index]
            id_list.remove(key[0])
    return dic


def brute_force():
    #import random
    max = 0
    range_ = 10
    for i in range(range_):
        for j in range(range_):
            for k in range(range_):
                #magicformula(i,j,k)
                sharpe = 0  # get_sharpe
                if sharpe > max:
                    print(i, j, k, max)
