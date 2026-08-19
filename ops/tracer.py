"""
Lab 11 -- A minimal tracer. (Provided complete.)

Wrap any agent step in a span; the tracer records name, duration, inputs and
outputs to a JSONL trace you can later inspect or ship to an observability tool.
Real stacks (LangSmith, Phoenix, Weave) do this at scale; the shape is the same.
"""
import json
import time
from contextlib import contextmanager

TRACE = []


@contextmanager
def span(name, **attrs):
    start = time.time()
    record = {"name": name, "attrs": attrs}
    try:
        yield record
    finally:
        record["ms"] = round((time.time() - start) * 1000, 1)
        TRACE.append(record)


def dump(path="trace.jsonl"):
    with open(path, "w") as f:
        for r in TRACE:
            f.write(json.dumps(r) + "\n")
    return path


def summary():
    print(f"{'SPAN':<28}{'ms':>8}  attrs")
    for r in TRACE:
        print(f"{r['name']:<28}{r['ms']:>8}  {r['attrs']}")
