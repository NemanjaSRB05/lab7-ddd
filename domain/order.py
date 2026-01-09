from domain.money import Money
from domain.order_status import OrderStatus


class OrderLine:
    def __init__(self, price: Money, qty: int):
        if qty <= 0:
            raise ValueError("Quantity must be positive")
        self.price = price
        self.qty = qty

    def total(self) -> Money:
        return Money(self.price.amount * self.qty)


class Order:
    def __init__(self, order_id: int):
        self.id = order_id
        self.lines: list[OrderLine] = []
        self.status = OrderStatus.NEW

    def add_line(self, line: OrderLine):
        if self.status == OrderStatus.PAID:
            raise ValueError("Cannot modify paid order")
        self.lines.append(line)

    def total_amount(self) -> Money:
        total = Money(0)
        for line in self.lines:
            total += line.total()
        return total

    def pay(self):
        if not self.lines:
            raise ValueError("Cannot pay empty order")
        if self.status == OrderStatus.PAID:
            raise ValueError("Order already paid")
        self.status = OrderStatus.PAID
