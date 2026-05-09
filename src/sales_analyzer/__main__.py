import argparse
from pathlib import Path

def main() -> None: #typehint, funktion gibt nichts zurück
    parser = argparse.ArgumentParser(description="Sales Analyzer") #parser für den programmaufruf in cli
    parser.add_argument("--file", required=True, help="Path to CSV file") #default="samples/sales.csv"
    args = parser.parse_args() #übersetzt argumente in datei
    path = Path(args.file) #gibt die tatsächliche datei

    if not path.exists():
        print(f"Fehler: Datei '{path}' wurde nicht gefunden.")
        return

    if not path.suffix == ".csv":
        print(f"Fehler: '{path}' ist keine CSV-Datei.")
        return

    print(f"Datei gelesen: {path}")

if __name__ == "__main__": #damit programm nur aus dieser datei ausgeführt wird, nicht beim starten von tests
    main()

