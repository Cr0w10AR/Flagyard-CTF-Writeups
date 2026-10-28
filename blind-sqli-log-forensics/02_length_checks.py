"""Summarize recorded password-length comparisons by database row and position."""
import argparse
import re
from collections import Counter
from audit_parser import read_transactions

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("log")
args = parser.parse_args()
counts = Counter()
for request, outcome in read_transactions(args.log):
    if "CHAR_LENGTH(password)" not in request:
        continue
    row = re.search(r"LIMIT\s+(\d+),1", request)
    pos = re.search(r"\),(\d+),1\)\)>\d+", request)
    if row and pos:
        counts[(int(row.group(1)), int(pos.group(1)))] += 1
for (row, position), total in sorted(counts.items()):
    print(f"Row {row}, length digit {position}: {total} comparisons")
