class InMemoryOrderRepository:
    def __init__(self):
        self.orders = {}

    def add(self, order):
        self.orders[order.id] = order

    def get_by_id(self, order_id):
        return self.orders[order_id]

    def save(self, order):
        self.orders[order.id] = order
