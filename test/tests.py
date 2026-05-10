import subprocess
from sales_analyzer.parser import parse_csv, Order
from datetime import date
from sales_analyzer.revenueCalculator import total_revenue, top_products_by_revenue, top_customers_by_revenue, revenue_per_month


def test_parses_valid_row(tmp_path): #temporärer test ordner
    # Arrange
    csv_file = tmp_path / "test.csv"
    #test csv erstellen
    csv_file.write_text(
        "order_id,order_date,customer_id,product_name,quantity,unit_price\n"
        "1001,2024-01-05,C-001,Screwdriver Set,2,19.90\n"
    )

    # Act
    orders, skipped = parse_csv(csv_file)

    # Assert
    assert len(orders) == 1
    assert len(skipped) == 0

    order_row = orders[0]
    assert order_row.order_id == 1001
    assert order_row.order_date == date(2024, 1, 5)
    assert order_row.customer_id == "C-001"
    assert order_row.product_name == "Screwdriver Set"
    assert order_row.quantity == 2
    assert order_row.unit_price == 19.90

def test_skipps_empty_row(tmp_path): #temporärer test ordner
    # Arrange
    csv_file = tmp_path / "test.csv"
    #test csv erstellen
    csv_file.write_text(
        "order_id,order_date,customer_id,product_name,quantity,unit_price\n"
        ",,,,,\n"
    )

    # Act
    orders, skipped = parse_csv(csv_file)

    # Assert
    assert len(orders) == 0
    assert len(skipped) == 1

    skipped_row = skipped[0]
    assert skipped_row.row_number == 2
    assert skipped_row.reason == "empty row"

def test_skips_row_with_invalid_quantity(tmp_path):
    # Arrange
    csv_file = tmp_path / "test.csv"
    csv_file.write_text(
        "order_id,order_date,customer_id,product_name,quantity,unit_price\n"
        "1001,2024-01-05,C-001,Screwdriver Set,three,19.90\n"
    )

    # Act
    orders, skipped = parse_csv(csv_file)

    # Assert
    assert len(orders) == 0
    assert len(skipped) == 1

    skipped_row = skipped[0]
    assert skipped_row.row_number == 2
    assert "three" in skipped_row.reason


def test_skips_row_with_negative_quantity(tmp_path):
    # Arrange
    csv_file = tmp_path / "test.csv"
    csv_file.write_text(
        "order_id,order_date,customer_id,product_name,quantity,unit_price\n"
        "1001,2024-01-05,C-001,Screwdriver Set,-3,19.90\n"
    )

    # Act
    orders, skipped = parse_csv(csv_file)

    # Assert
    assert len(orders) == 0
    assert len(skipped) == 1

    skipped_row = skipped[0]
    assert skipped_row.row_number == 2
    assert "-3" in skipped_row.reason


def test_skips_row_with_missing_unit_price(tmp_path):
    # Arrange
    csv_file = tmp_path / "test.csv"
    csv_file.write_text(
        "order_id,order_date,customer_id,product_name,quantity,unit_price\n"
        "1001,2024-01-05,C-001,Screwdriver Set,2,\n"
    )

    # Act
    orders, skipped = parse_csv(csv_file)

    # Assert
    assert len(orders) == 0
    assert len(skipped) == 1

    skipped_row = skipped[0]
    assert skipped_row.row_number == 2
    assert "unit price" in skipped_row.reason

def test_total_revenue_calculates_correctly_with_skipped_row(tmp_path):
    # Arrange
    csv_file = tmp_path / "test.csv"
    csv_file.write_text(
        "order_id,order_date,customer_id,product_name,quantity,unit_price\n"
        "1001,2024-01-05,C-001,Screwdriver Set,2,19.90\n"
        "1002,2024-01-08,C-002,Cordless Drill Pro,1,149.00\n"
        "1003,2024-01-12,C-003,Wood Glue 250ml,3,oooo\n" #keine gültige zeile
    )
    orders, skipped = parse_csv(csv_file)

    #Act
    revenue = total_revenue(orders)

    #Assert
    assert revenue == 188.80

def test_top_products_by_revenue_calculated_correctly(tmp_path):
    # Arrange
    csv_file = tmp_path / "test.csv"
    csv_file.write_text(
        "order_id,order_date,customer_id,product_name,quantity,unit_price\n"
        "1001,2024-01-05,C-001,Screwdriver Set,2,19.90\n"
        "1002,2024-01-08,C-002,Cordless Drill Pro,1,149.00\n"
        "1003,2024-01-12,C-003,Wood Glue 250ml,3,4.50\n"
        "1004,2024-01-12,C-004,Wood Glue 250ml,1,4.50\n"
    )
    orders, skipped = parse_csv(csv_file)

    #Act
    top_products = top_products_by_revenue(orders)

    #Assert
    assert len(top_products) == 3
    expected = [("Cordless Drill Pro", 149.00), ("Screwdriver Set", 39.80), ("Wood Glue 250ml", 18.00)]

    for product_index, product in enumerate(top_products):
        assert top_products[product_index] == expected[product_index]


def test_top_customers_by_revenue_calculated_correctly_with_skipped_row(tmp_path):
    # Arrange
    csv_file = tmp_path / "test.csv"
    csv_file.write_text(
        "order_id,order_date,customer_id,product_name,quantity,unit_price\n"
        "1001,2024-01-05,C-001,Screwdriver Set,2,19.90\n"
        "1002,2024-01-08,C-002,Cordless Drill Pro,1,149.00\n"
        "1003,2024-01-12,C-002,Wood Glue 250ml,3,4.50\n"
        "absda,2024-01-12,C-003,Wood Glue 250ml,1,4.50\n" #keine gültige zeile
    )
    orders, skipped = parse_csv(csv_file)

    #Act
    top_customers = top_customers_by_revenue(orders)

    #Assert
    assert len(top_customers) == 2
    expected = [("C-002", 162.50), ("C-001", 39.80)]

    for customer_index, product in enumerate(top_customers):
        assert top_customers[customer_index] == expected[customer_index]

def test_revenue_per_month_calculated_correctly(tmp_path):
    # Arrange
    csv_file = tmp_path / "test.csv"
    csv_file.write_text(
        "order_id,order_date,customer_id,product_name,quantity,unit_price\n"
        "1001,2024-01-05,C-001,Screwdriver Set,2,19.90\n"
        "1002,2024-02-08,C-002,Cordless Drill Pro,1,149.00\n"
        "1003,2024-03-12,C-002,Wood Glue 250ml,3,4.50\n"
        "1004,2024-03-12,C-003,Wood Glue 250ml,1,4.50\n"
    )
    orders, skipped = parse_csv(csv_file)

    #Act
    month = revenue_per_month(orders)

    #Assert
    assert len(month) == 3
    expected = [("2024-01", 39.80), ("2024-02", 149.00), ("2024-03", 18.00)]

    for month_index, product in enumerate(month):
        assert month[month_index] == expected[month_index]

def test_end_to_end():
    # Act
    result = subprocess.run(
        ["python", "-m", "sales_analyzer", "--file", "test/sales_test.csv"],
        capture_output=True,  # Ausgabe abfangen
        text=True,             # Ausgabe als String
        encoding="utf-8"
    )

    # Assert
    assert result.returncode == 0 #programm ist nicht abgestürzt

    expected_console_output = """File read: test\\sales_test.csv
total number of orders: 5
total revenue: 254.5 €

top 5 products by revenue: 
  Cordless Drill Pro: 149.00 €
  Hammer: 39.80 €
  Screwdriver Set: 29.70 €
  Sandpaper Pack: 27.00 €
  Wood Glue 250ml: 9.00 €

top 5 customers by revenue: 
  C-002: 158.00 €
  C-001: 69.50 €
  C-003: 27.00 €

revenue per month: 
  2024-01: 188.80 €
  2024-02: 56.70 €
  2024-03: 9.00 €

skipped rows: 5
  Row 7: empty row
  Row 8: quantity is not a number: 'three'
  Row 9: quantity must be greater than 0: '-1'
  Row 10: unit price is not a number: ''
  Row 11: order date is not a valid date: '2024-03-33'"""

    assert expected_console_output == result.stdout