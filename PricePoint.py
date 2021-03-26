class PricePoint:

    def __init__(self, price, size):
        self.price = float(price)
        self.size = float(size)
        self.next = None
        self.prev = None

    