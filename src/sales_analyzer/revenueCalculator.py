from sales_analyzer.parser import Order

def total_revenue(orders: list[Order]):
    return sum(order.quantity * order.unit_price for order in orders)