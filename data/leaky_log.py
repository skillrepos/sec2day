"""
Lab 4 (part 1) -- The problem. VULNERABLE ON PURPOSE.

A typical support-agent logging line: it dumps the whole customer record --
card, SSN, email -- into a log and into the model prompt. Run it and look at
what just landed in the log file and in the "prompt sent to model".

  python leaky_log.py
"""
import json
import os

RECORDS = json.load(open(os.path.join(os.path.dirname(__file__), "customer_records.json")))


def handle(order_id):
    rec = next(r for r in RECORDS if r["order_id"] == order_id)
    # Everything gets logged...
    print("LOG:", json.dumps(rec))
    # ...and everything gets sent to the model.
    prompt = f"Help this customer: {json.dumps(rec)}"
    print("PROMPT SENT TO MODEL:", prompt)
    return prompt


if __name__ == "__main__":
    handle("A1001")
    print("\nBoth the log and the model now hold this customer's card and SSN.")
