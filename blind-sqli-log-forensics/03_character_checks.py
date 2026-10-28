"""Report character-comparison coverage without displaying recovered values."""
import argparse
import re
from collections import defaultdict
from audit_parser import read_transactions

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("log")
args = parser.parse_args()
coverage = defaultdict(set)
for request, outcome in read_transactions(args.log):
    field = "password" if "CAST(password AS NCHAR)" in request else (
        "username" if "CAST(`user` AS NCHAR)" in request else None
    )
    if not field:
        continue
    row = re.search(r"LIMIT\s+(\d+),1", request)
    pos = re.search(r"\),(\d+),1\)\)>\d+", request)
    if row and pos:
        coverage[(field, int(row.group(1)))].add(int(pos.group(1)))
for (field, row), positions in sorted(coverage.items()):
    print(f"{field}, row {row}: {len(positions)} character positions tested")
