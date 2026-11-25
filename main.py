#!/usr/bin/env python3
"""One-Line Office Joke Laugh-Off -- make.fun entry.

Writes exactly one original one-line office joke to entry.txt.
Standard library only. Deterministic: the same input always yields
the same bytes, so two runs produce an identical sha256.
"""

import hashlib
import os
import sys

# The joke: a dead office plant outlasting every meeting culture cliche.
# Angle: the plant is the only "coworker" that never demands a status
# update -- the punchline flips a neglected desk plant into the ideal
# colleague, which lands instantly because every office worker knows
# both the dead plant and the status-update treadmill.
LINE = (
    "The office plant by my desk has been dead for six months and it is "
    "still the only thing here that never asks me for a status update."
)

MAX_CHARS = 160


def validate(line):
    """Enforce every competition rule on the joke line."""
    if not isinstance(line, str) or not line:
        raise ValueError("joke line must be a non-empty string")
    if line != line.strip():
        raise ValueError("joke line must not have leading/trailing whitespace")
    if "\n" in line or "\r" in line:
        raise ValueError("joke line must be exactly one line")
    if any(ord(ch) < 0x20 for ch in line):
        raise ValueError("joke line must not contain control characters")
    if len(line) > MAX_CHARS:
        raise ValueError(
            "joke line is %d characters, over the %d limit" % (len(line), MAX_CHARS)
        )
    try:
        line.encode("ascii")
    except UnicodeEncodeError:
        raise ValueError("joke line must be plain ASCII")
    return line


def output_dir():
    """Resolve the output directory, honouring MAKEFUN_OUTPUT_DIR."""
    chosen = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    return chosen


def main():
    line = validate(LINE)
    out_dir = output_dir()
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    payload = (line + "\n").encode("ascii")
    with open(path, "wb") as handle:
        handle.write(payload)
    # Round-trip check: what we wrote must read back byte-for-byte.
    with open(path, "rb") as handle:
        back = handle.read()
    if back != payload:
        raise SystemExit("round-trip check failed: entry.txt bytes differ")
    digest = hashlib.sha256(payload).hexdigest()
    print("chars: %d" % len(line))
    print("sha256: %s" % digest)
    print("wrote: %s" % path)
    return 0


if __name__ == "__main__":
    sys.exit(main())
