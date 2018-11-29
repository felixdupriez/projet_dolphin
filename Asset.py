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


class Portfolio:
    def __init__(self, assets, sum):
        self.assets = assets
        self.sum = sum


def check_portfolio(portfolio):
    assets = portfolio.assets
    min_close = assets[0].asset.get_nav()
    max_close = assets[0].asset.get_nav()
    for asset in assets:
        if asset.get_nav() < min_close:
            if asset.get_nav() < max_close / 10:
                return False
            else:
                min_close = asset.get_nav()
        elif asset.get_nav > max_close:
            if asset.get_nav > 10 * min_close:
                return False
            else:
                max_close = asset.get_nav
        if asset.get_nav() < (portfolio.sum / 100) or asset.get_nav() > (portfolio.sum / 10):
            return False
    return True
