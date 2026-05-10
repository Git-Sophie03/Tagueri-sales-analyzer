import argparse
from pathlib import Path
from sales_analyzer.parser import parse_csv
from sales_analyzer.revenueCalculator import total_revenue, top_products_by_revenue, top_customers_by_revenue


def main() -> None: #return typehint, funktion gibt nichts zurück
    parser = argparse.ArgumentParser(description="Sales Analyzer") #parser für den programmaufruf in cli
    parser.add_argument("--file", required=True, help="Path to CSV file") #default="samples/sales.csv"
    args = parser.parse_args() #übersetzt argumente in datei
    path = Path(args.file) #gibt die tatsächliche datei

    if not path.exists():
        print(f"Error: File '{path}' not found.")
        return

    if not path.suffix == ".csv":
        print(f"Error: '{path}' is not a CSV-File.")
        return

    orders, skipped = parse_csv(path)
    revenue = total_revenue(orders)
    top_products = top_products_by_revenue(orders)
    top_customers = top_customers_by_revenue(orders)

    print()
    print(f"File read: {path}")
    print(f"Total number of orders: {len(orders)}") #valide zeilen
    print(f"total revenue: {revenue}€")
    print(f"top 5 products by revenue: {top_customers}")
    for product, revenue in top_products:
        print(f"  {product}: {revenue:.2f} €")
    print()
    print(f"top 5 customers by revenue: {top_customers}")
    print(f"skipped rows: {len(skipped)}")

    if skipped:
        for s in skipped:
            print(f"  Row {s.row_number}: {s.reason}")

if __name__ == "__main__": #damit programm nur aus dieser datei ausgeführt wird, nicht beim starten von tests
    main()

