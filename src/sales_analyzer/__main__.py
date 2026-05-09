import argparse

def main() -> None: #typehint, funktion gibt nichts zurück
    parser = argparse.ArgumentParser(description="Sales Analyzer") #parser für den programmaufruf in cli
    parser.add_argument("--file", required=True,help="Path to CSV file") #default="samples/sales.csv"    args = parser.parse_args()

    print(f"Analyzing file: {args.file}")

if __name__ == "__main__": #damit programm nur aus dieser datei ausgeführt wird, nicht beim starten von tests
    main()

