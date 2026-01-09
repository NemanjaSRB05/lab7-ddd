import pytest
from domain.order import Order, OrderLine
from domain.money import Money
from application.pay_order_use_case import PayOrderUseCase
from infrastructure.in_memory_order_repository import InMemoryOrderRepository
from infrastructure.fake_payment_gateway import FakePaymentGateway


def create_order_with_lines():
    order = Order(1)
    order.add_line(OrderLine(Money(100), 2))
    return order


def test_successful_payment():
    repo = InMemoryOrderRepository()
    gateway = FakePaymentGateway()
    order = create_order_with_lines()
    repo.add(order)

    use_case = PayOrderUseCase(repo, gateway)
    result = use_case.execute(1)

    assert result["status"] == "PAID"
    assert result["total"] == 200


def test_cannot_pay_empty_order():
    repo = InMemoryOrderRepository()
    gateway = FakePaymentGateway()
    order = Order(1)
    repo.add(order)

    use_case = PayOrderUseCase(repo, gateway)

    with pytest.raises(ValueError):
        use_case.execute(1)


def test_cannot_pay_twice():
    repo = InMemoryOrderRepository()
    gateway = FakePaymentGateway()
    order = create_order_with_lines()
    repo.add(order)

    use_case = PayOrderUseCase(repo, gateway)
    use_case.execute(1)

    with pytest.raises(ValueError):
        use_case.execute(1)


def test_cannot_modify_after_payment():
    order = create_order_with_lines()
    order.pay()

    with pytest.raises(ValueError):
        order.add_line(OrderLine(Money(10), 1))


def test_total_is_correct():
    order = Order(1)
    order.add_line(OrderLine(Money(50), 2))
    order.add_line(OrderLine(Money(30), 1))

    assert order.total_amount().amount == 130
