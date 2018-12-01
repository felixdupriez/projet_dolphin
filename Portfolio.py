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

    def generate(self):
        nb = 0
        while not self.check_portfolio():
            nb += 1
            print('Iteration number %d', nb)
            for item in self.items:
                while item.qty * item.price < self.sum / 100:
                    item.qty += 1
                    self.sum += item.price
        print('End')

    def check_portfolio(self):
        for item in self.items:
            if not item.price * item.qty > self.sum / 100 and item.price * item.qty < self.sum / 10:
                return False
        return True
