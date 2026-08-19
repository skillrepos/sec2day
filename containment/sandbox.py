"""
Lab 10 -- A containment sandbox. SKELETON.

Wrap an agent's actions so a compromise stays small:
  1. Action budget -- stop after max_actions calls.
  2. Egress allow-list -- every fetched URL is checked.
  3. Kill switch -- one tripped guard trips the whole sandbox; nothing runs after.

Merge the gaps from extra/sandbox_complete.txt, then:
  python sandbox.py
"""
from egress_allowlist import check_url


class Sandbox:
    def __init__(self, max_actions=10):
        self.max_actions = max_actions
        self.actions = 0
        self.killed = False
        self.log = []

    def _trip(self, reason):
        self.killed = True
        self.log.append(f"KILLED: {reason}")

    def act(self, kind, payload):
        """Run one agent action under containment. Return (ran, result_or_reason)."""
        if self.killed:
            return False, "sandbox killed -- refusing further actions"
        # TODO (gap 1): increment self.actions; if it exceeds max_actions, call
        #   self._trip("action budget exceeded") and return (False, that reason).
        raise NotImplementedError("merge gap 1")

        # TODO (gap 2): if kind == "fetch", run check_url(payload); on failure,
        #   _trip the sandbox with the reason and return (False, reason).
        #   Otherwise record and return (True, f"did {kind}: {payload}").
        raise NotImplementedError("merge gap 2")


def main():
    box = Sandbox(max_actions=10)
    plan = [("fetch", "http://api.omnitech.example/x"),
            ("fetch", "http://attacker.example/collect"),   # egress violation -> kill
            ("fetch", "http://api.omnitech.example/y")]      # never runs; sandbox killed
    for kind, payload in plan:
        ran, msg = box.act(kind, payload)
        print(f"  {'OK  ' if ran else 'STOP'} {kind} {payload} -> {msg}")
    print("\n--- containment log ---")
    for line in box.log:
        print("  ", line)
    print(f"Total actions attempted after kill: none. Blast radius = 1 bad call.")


if __name__ == "__main__":
    main()
