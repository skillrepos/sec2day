"""
Lab 10 -- A runaway agent. VULNERABLE ON PURPOSE.

No budget, no kill switch, no egress control. Once it starts looping (or is
tricked into it) it will call tools forever and reach any URL. Run it and watch
it make 50 tool calls and hit an attacker domain, unchecked.

  python runaway_agent.py
"""


def fetch(url):
    return f"fetched {url}"


def main():
    # A confused/hijacked plan: fetch the same thing over and over, and reach out.
    targets = ["http://attacker.example/collect"] + ["http://api.omnitech.example/x"] * 49
    calls = 0
    for url in targets:
        calls += 1
        print(f"  call {calls}: {fetch(url)}")
    print(f"\nMade {calls} calls with no limit and no egress check. Nothing stopped it.")


if __name__ == "__main__":
    main()
