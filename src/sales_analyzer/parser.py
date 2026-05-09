import csv
from dataclasses import dataclass
from datetime import date, datetime
from pathlib import Path

@dataclass #generiert to string und equals methoden im hintergrund
class Order: #datenklasse für valide zeilen
    order_id: int
    order_date: date
    customer_id: str
    product_name: str
    quantity: int
    unit_price: float


@dataclass #datenklasse für nicht valide zeilen
class SkippedRow:
    row_number: int
    reason: str


def parse_csv(path: Path): #path ist der dateipfad
    orders: list[Order] = [] #leere listen initialisieren
    skipped: list[SkippedRow] = []

    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f) # die datei basically

            #zähler,    zeile; start ist für row number
        for row_number, row in enumerate(reader, start=2):  # start=2 weil Zeile 1 der Header ist

            # 1. Leere Zeile prüfen
            if not any(row.values()):
                skipped.append(SkippedRow(row_number, "empty row"))
                continue #sobald es irgendwo knallt die anderen Felder nicht mehr betrachten und nächste zeile checken

            # 2. order_id prüfen
            try:
                order_id = int(row["order_id"])
            except (ValueError, KeyError):
                skipped.append(SkippedRow(row_number, f"order id is not a number: '{row.get('order_id')}'"))
                continue

            # 3. order_date prüfen
            try:
                order_date = datetime.fromisoformat(row["order_date"]).date()
            except (ValueError, KeyError):
                skipped.append(SkippedRow(row_number, f"order date is not a valid date: '{row.get('order_date')}'"))
                continue

            # 4. customer_id prüfen
            customer_id = row.get("customer_id", "").strip()
            if not customer_id:
                skipped.append(SkippedRow(row_number, "customer id is missing"))
                continue

            # 5. product_name prüfen
            product_name = row.get("product_name", "").strip()
            if not product_name:
                skipped.append(SkippedRow(row_number, "product name is missing"))
                continue

            # 6. quantity prüfen
            try:
                quantity = int(row["quantity"])
            except (ValueError, KeyError):
                skipped.append(SkippedRow(row_number, f"quantity is not a number: '{row.get('quantity')}'"))
                continue

            if quantity <= 0:
                skipped.append(SkippedRow(row_number, f"quantity must be greater than 0: '{quantity}'"))
                continue

            # 7. unit_price prüfen
            try:
                unit_price = float(row["unit_price"])
            except (ValueError, KeyError):
                skipped.append(SkippedRow(row_number, f"unit price is not a number: '{row.get('unit_price')}'"))
                continue

            if unit_price <= 0:
                skipped.append(SkippedRow(row_number, f"unit price must be greater than 0: '{unit_price}'"))
                continue

            # Alles ok → Order anlegen
            orders.append(Order(
                order_id=order_id,
                order_date=order_date,
                customer_id=customer_id,
                product_name=product_name,
                quantity=quantity,
                unit_price=unit_price,
            ))

    return orders, skipped #die beiden befüllten listen als tuple