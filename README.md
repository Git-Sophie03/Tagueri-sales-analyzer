# Sales Analyzer

A Python command-line tool that reads CSV files of a certain format,
calculates key revenue metrics, and reports broken rows.

---

## Requirements

- Python 3.10+
- Git

---

## Installation & Run instructions

1. Clone the repository:
   ```bash
   git clone https://github.com/Git-Sophie03/Tagueri-sales-analyzer
   cd Tagueri-sales-analyzer
   ```

2. Open the project in IntelliJ and open the terminal.

3. Install the following to run the project:
   ```bash
   pip install -e ".[dev]"
   ```

4. Run the analyzer:
   ```bash
   sales-analyzer --file samples/sales.csv
   ```

---

## Running the Tests

run in terminal:
```bash
pytest test/tests.py -v  
```

---

## Decisions

**1. setuptools as build backend**
Setuptools is already included in most Python installations. Therefore, no extra install for a more modern build tool is required, which makes running easier.

**2. No external dependencies**
The Python standard library covers all functions that are needed: `argparse` for CLI arguments, `datetime` for date parsing, `csv` for reading files, and `collections` for aggregation. This is a plus because we don´t need to manually install pip. Hence, we have less errorpotential.

**3. Row numbers start at 2**
The row counter in the for loop starts at 2 so that row numbers match the actual line numbers in the CSV file — line 1 is the header, so the first data row is line 2.

**4. Separate files for parsing and analysis**
`parser.py` handles reading and validating rows, `revenueCalculator.py` handles calculations. This maintains a good overview and avoids a single large "god class" that is hard to read and test.

**5. Explicit error handling**
Instead of `defaultdict`, explicit `if/else` checks are used when building dictionaries. In a real application, silent fallbacks can hide bugs — being explicit about missing keys makes the code easier to debug.

**6. Dataclasses for valid rows**
Valid rows are stored as `Order` dataclasses instead of plain dictionaries. This makes accessing fields more readable.

**7. Separate ValueError and KeyError handling**
Both error types are caught so the reported error is as precise as possible. This gives a clear and more direct clue of what went wrong.

---

## What I Would Do Differently Next Time

- **Test-driven development:** Write the tests before the implementation. This would have made edge cases clearer earlier and led to a more testable structure from the start.

- **Use defaultdict for aggregation:** While explicit error handling was a conscious choice here, `defaultdict` would make the aggregation functions shorter — worth reconsidering for a larger dataset.

- **More granular error messages for dates:** Currently an empty date and a malformed date produce similar messages. Splitting these into two separate checks would give the user clearer feedback.