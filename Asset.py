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
    if assets.amount() != 20:
        return False
    for asset in assets:
        if asset.get_nav() < (portfolio.sum / 100) or asset.get_nav() > (portfolio.sum / 10):
            return False
    return True
