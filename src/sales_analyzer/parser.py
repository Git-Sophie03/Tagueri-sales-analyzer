import csv
from dataclasses import dataclass
from datetime import date, datetime
from pathlib import Path
import re

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


ORDER_ID_COLUMN_NAME = "order_id"
UNIT_PRICE_COLUMN_NAME = "unit_price"
QUANTITY_COLUMN_NAME = "quantity"
PRODUCT_NAME_COLUMN_NAME = "product_name"
CUSTOMER_ID_COLUMN_NAME = "customer_id"
ORDER_DATE_COLUMN_NAME = "order_date"


def parse_csv(path: Path): #path ist der dateipfad
    orders: list[Order] = [] #leere listen initialisieren
    skipped: list[SkippedRow] = []

    with open(path, newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file) # die datei basically

            #zähler,    zeile; start ist für row number
        for row_number, row in enumerate(reader, start=2):  # start=2 weil Zeile 1 der Header ist

            # 1. Leere Zeile prüfen
            if not any(row.values()):
                skipped.append(SkippedRow(row_number, "empty row"))
                continue #sobald es irgendwo knallt die anderen Felder nicht mehr betrachten und nächste zeile checken

            # 2. order_id prüfen
            try:
                order_id = int(row[ORDER_ID_COLUMN_NAME]) #wenn dieser key nicht gefunden wird keyError
            except KeyError:
                skipped.append(SkippedRow(row_number, "column name could not be found: " + ORDER_ID_COLUMN_NAME))
                continue

            except ValueError:
                skipped.append(SkippedRow(row_number, f"order id is not a number: '{row.get(ORDER_ID_COLUMN_NAME)}'")) #gibt den value zu dem key ohne error
                continue

            if order_id <= 0:
                skipped.append(SkippedRow(row_number, f"order id can´t be negative: '{order_id}'"))
                continue

            # 3. order_date prüfen
            try:
                order_date = datetime.fromisoformat(row[ORDER_DATE_COLUMN_NAME]).date()
            except KeyError:
                skipped.append(SkippedRow(row_number, "column name could not be found: " + ORDER_DATE_COLUMN_NAME))
                continue

            except ValueError:
                skipped.append(SkippedRow(row_number, f"order date is not a valid date: '{row.get(ORDER_DATE_COLUMN_NAME)}'"))
                continue

            # 4. customer_id prüfen
            customer_id = row.get(CUSTOMER_ID_COLUMN_NAME, "").strip()
            if not customer_id:
                skipped.append(SkippedRow(row_number, "customer id is missing"))
                continue

            elif not re.match(r"^C-\d{3}$", customer_id): #prüfen, dass es das richtige format hat
                skipped.append(SkippedRow(row_number, f"customer id has wrong format: '{customer_id}' (expected: C-001)"))
                continue

            # 5. product_name prüfen
            product_name = row.get(PRODUCT_NAME_COLUMN_NAME, "").strip() #"" default, wenn der wert nicht existiert
            if not product_name:
                skipped.append(SkippedRow(row_number, "product name is missing"))
                continue

            # 6. quantity prüfen
            try:
                quantity = int(row[QUANTITY_COLUMN_NAME])
            except KeyError:
                skipped.append(SkippedRow(row_number, "column name could not be found: " + QUANTITY_COLUMN_NAME))
                continue

            except ValueError:
                skipped.append(SkippedRow(row_number, f"quantity is not a number: '{row.get(QUANTITY_COLUMN_NAME)}'"))
                continue

            if quantity <= 0:
                skipped.append(SkippedRow(row_number, f"quantity must be greater than 0: '{quantity}'"))
                continue

            # 7. unit_price prüfen
            try:
                unit_price = float(row[UNIT_PRICE_COLUMN_NAME])
            except KeyError:
                skipped.append(SkippedRow(row_number, "column name could not be found: " + UNIT_PRICE_COLUMN_NAME))
                continue

            except ValueError:
                skipped.append(SkippedRow(row_number, f"unit price is not a number: '{row.get(UNIT_PRICE_COLUMN_NAME)}'"))
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

    return orders, skipped #die beiden befüllten listen