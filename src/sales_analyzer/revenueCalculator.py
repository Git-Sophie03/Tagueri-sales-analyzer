from sales_analyzer.parser import Order

def total_revenue(orders: list[Order]):
    return sum(order.quantity * order.unit_price for order in orders)

def top_products_by_revenue(orders: list[Order]):
    product_revenue_dict = {}

    for order in orders:
        if order.product_name in product_revenue_dict:
           product_revenue_dict[order.product_name] = product_revenue_dict.get(order.product_name) + order.quantity * order.unit_price
        else:
            product_revenue_dict[order.product_name] = order.quantity * order.unit_price

    sorted_by_revenue = sorted(product_revenue_dict.items(), key=lambda item: item[1], reverse=True)  #.items() macht dict zu ner liste von tupeln, item[1] holt den value, reverse sortiert absteigend

    return sorted_by_revenue[0:5] #erste 5 einträge aus sortierer liste


def top_customers_by_revenue(orders: list[Order]):
    customer_revenue_dict = {}

    for order in orders:
        if order.customer_id in customer_revenue_dict:
            customer_revenue_dict[order.customer_id] = customer_revenue_dict.get(order.customer_id) + (order.quantity * order.unit_price)
        else:
            customer_revenue_dict[order.customer_id] = order.quantity * order.unit_price

    sorted_by_revenue = sorted(customer_revenue_dict.items(), key=lambda item: item[1], reverse=True)

    return sorted_by_revenue[0:5]


def revenue_per_month(orders: list[Order]):
    month_revenue_dict = {}

    for order in orders:
        month_key = order.order_date.strftime("%Y-%m")  # speichert datum als string z.B. "2024-01"

        if month_key in month_revenue_dict:
            month_revenue_dict[month_key] = month_revenue_dict.get(month_key) + (order.quantity * order.unit_price)
        else:
            month_revenue_dict[month_key] = order.quantity * order.unit_price

    sorted_by_month = sorted(month_revenue_dict.items(), key=lambda item: item[0]) #monate sortieren

    return sorted_by_month