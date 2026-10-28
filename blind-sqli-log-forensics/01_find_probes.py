"""Show the first Boolean-based SQL injection probes and their observed outcomes."""
import argparse
from audit_parser import read_transactions

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("log", help="Path to the local ModSecurity audit log")
parser.add_argument("--limit", type=int, default=10)
args = parser.parse_args()

count = 0
for request, outcome in read_transactions(args.log):
    if " AND " not in request:
        continue
    print(f"Probe: {request[:190]}")
    print(f"Response classification: {'TRUE' if outcome else 'FALSE'}\n")
    count += 1
    if count >= args.limit:
        break
print(f"Displayed {count} samples.")
