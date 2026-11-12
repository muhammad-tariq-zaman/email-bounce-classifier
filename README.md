# email-bounce-classifier

Classify email bounces from a CSV of SMTP codes and reasons: 5xx is a HARD BOUNCE (REMOVE the address), 4xx or 'mailbox full' is a SOFT BOUNCE (RETRY later), anything else is UNKNOWN (INVESTIGATE) — 'user unknown' is always hard, even on a 4xx code, hard bounces first.

## How to run

```sh
python3 main.py bounces.csv
```

## Example output

```
M-1 (550): HARD BOUNCE — REMOVE (user unknown)
M-2 (421): SOFT BOUNCE — RETRY (try again later)
1 hard bounce(s), 1 soft bounce(s), 0 unknown.
```

Standard library only. Run the tests with `python3 -m unittest discover`.
