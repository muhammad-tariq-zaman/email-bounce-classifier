"""Classify email bounces as hard, soft or unknown, with the action to take.

Usage: python3 main.py bounces.csv
CSV columns: message_id,smtp_code,reason.
- HARD BOUNCE: a 5xx SMTP code — permanent failure. Action: REMOVE
  the address from the mailing list.
- SOFT BOUNCE: a 4xx SMTP code, or a "mailbox full" reason — a
  temporary failure. Action: RETRY later.
- UNKNOWN: any other code, or an empty reason with a 5xx code that
  gives no detail. Action: INVESTIGATE.
A "user unknown" / "no such user" reason is always a HARD BOUNCE,
even on a 4xx code, because the address does not exist.
Hard bounces first, so the addresses to remove are on top.
"""
import argparse, csv, sys

def classify(code, reason):
    text = (reason or "").strip().lower()
    code = str(code).strip()
    if "user unknown" in text or "no such user" in text:
        return "HARD BOUNCE", "REMOVE"
    if "mailbox full" in text:
        return "SOFT BOUNCE", "RETRY"
    if code.startswith("5"):
        return "HARD BOUNCE", "REMOVE"
    if code.startswith("4"):
        return "SOFT BOUNCE", "RETRY"
    return "UNKNOWN", "INVESTIGATE"

def classify_rows(rows):
    out = []
    for row in rows:
        category, action = classify(row["smtp_code"], row.get("reason", ""))
        out.append((row["message_id"].strip(), row["smtp_code"].strip(),
                    (row.get("reason") or "").strip(), category, action))
    rank = {"HARD BOUNCE": 0, "SOFT BOUNCE": 1, "UNKNOWN": 2}
    return sorted(out, key=lambda r: (rank[r[3]], r[0]))

def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("path")
    args = parser.parse_args(argv)
    with open(args.path, newline="", encoding="utf-8") as f:
        results = classify_rows(list(csv.DictReader(f)))
    for message_id, code, reason, category, action in results:
        print(f"{message_id} ({code}): {category} — {action} ({reason})")
    print(f"{sum(1 for *_, c, _ in results if c == 'HARD BOUNCE')} hard bounce(s), "
          f"{sum(1 for *_, c, _ in results if c == 'SOFT BOUNCE')} soft bounce(s), "
          f"{sum(1 for *_, c, _ in results if c == 'UNKNOWN')} unknown.")
    return 0

if __name__ == "__main__":
    sys.exit(main())
