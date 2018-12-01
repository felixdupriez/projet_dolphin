from Toolbox import put_portfolio

class Item:
    def __init__(self, asset, price, qty):
        self.asset = asset
        self.price = price
        self.qty = qty


class Portfolio:
    def __init__(self, df):
        self.items = []  # liste d'item
        for index, row in df.iterrows():
            self.items.append(Item(row.ASSET_DATABASE_ID, row.CLOSE_2012_01_02, 1))
        self.sharpe = None
        self.sum = 0
        for item in self.items:
            self.sum += item.price      # calculer somme du portefeuille

    def generate2(self):
        nb = 0
        while not self.check_portfolio():
            nb += 1
            for item in self.items:
                while item.qty * item.price / self.sum < 0.01:
                    item.qty += 1
                    self.sum += item.price
                while item.qty * item.price / self.sum > 0.1:
                    for item2 in self.items:
                        i = 0.01
                        while (item2.qty + 1) * item2.price / self.sum < i and item.qty * item.price / self.sum > 0.1:
                            i += 0.01
                            item2.qty += 1
                            self.sum += item.price

    def generate(self):
        while not self.check_portfolio():
            for item in self.items:
                if item.price * item.qty / self.sum < 0.05:
                    item.qty += 1
                    self.sum += item.price

    def check_portfolio(self):
        for item in self.items:
            if item.price * item.qty / self.sum < 0.01 or item.price * item.qty / self.sum > 0.1:
                return False
        return True

    def optimize(self):
        cur_sharpe = put_portfolio(self)
        second = self
        for item in second.items:
            if item.price * (item.qty + 1) / self.sum < 0.1:
                item.qty += 1
                second.sum += item.price
                tmp_sharpe = put_portfolio(second)
                if tmp_sharpe > cur_sharpe:
                    cur_sharpe = tmp_sharpe
                else:
                    put_portfolio(self)
