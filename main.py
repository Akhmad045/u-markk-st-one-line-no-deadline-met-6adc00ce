#!/usr/bin/env python3
"""One Line, No Deadline Met — make.fun entry.

The entry is a single joke (87 characters) that excuses a missed
deadline. This program puts exactly that joke, and nothing else, into
/output/entry.txt, so the gate scorer sees one line of 1-200 UTF-8
characters with no trailing newline.

    python3 main.py               # write the entry
    python3 main.py --self-test   # check the entry and the gate
"""

import sys
import tempfile
from pathlib import Path

JOKE = "I finished it on time, but my laptop autosaved it into a folder I've never seen before."
LIMIT = 200
TARGET = Path("/output/entry.txt")


def gate(text):
    """Check a candidate entry against the gate.

    Returns an empty string when the text passes, otherwise a short
    reason it fails.
    """
    if not isinstance(text, str):
        return "not text"
    if len(text) == 0:
        return "empty"
    if len(text) > LIMIT:
        return "too long: %d characters, limit is %d" % (len(text), LIMIT)
    if text.strip() == "":
        return "only whitespace"
    if text.strip() != text:
        return "leading or trailing whitespace"
    for ch in text:
        if ch in "\n\r" or ord(ch) < 32:
            return "not a single clean line"
    return ""


def emit(path=TARGET):
    """Write JOKE to path, then prove the file holds exactly JOKE."""
    problem = gate(JOKE)
    if problem:
        raise SystemExit("entry fails the gate: " + problem)
    wanted = JOKE.encode("utf-8")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(wanted)
    got = path.read_bytes()
    if got != wanted:
        raise SystemExit("wrote %d bytes but the file holds %d"
                         % (len(wanted), len(got)))
    if got.endswith(b"\n"):
        raise SystemExit("written file ends with a newline")
    if gate(got.decode("utf-8")):
        raise SystemExit("written file fails the gate on re-read")
    return path


CASES = [
    # (label, text, True when the gate should accept it)
    ("entry", JOKE, True),
    ("one character", "!", True),
    ("exactly at the limit", "x" * 200, True),
    ("empty", "", False),
    ("only spaces", "   ", False),
    ("one over the limit", "x" * 201, False),
    ("two lines", "one\ntwo", False),
    ("carriage return", "one\rtwo", False),
    ("leading space", " " + JOKE, False),
    ("trailing space", JOKE + " ", False),
    ("control character", "a\x01b", False),
]


def run_checks():
    """Run the gate over JOKE and every rejection case.

    Returns 0 when everything behaves, 1 otherwise, printing each
    failure.
    """
    bad = []
    for label, text, should_pass in CASES:
        problem = gate(text)
        if should_pass and problem:
            bad.append("%s: should pass, gate says %r" % (label, problem))
        if not should_pass and not problem:
            bad.append("%s: should fail, gate passed it" % label)
    with tempfile.TemporaryDirectory() as tmp:
        target = Path(tmp) / "entry.txt"
        emit(target)
        blob = target.read_bytes()
        if blob != JOKE.encode("utf-8"):
            bad.append("round-trip: bytes differ from the entry")
        if blob.endswith(b"\n"):
            bad.append("round-trip: file ends with a newline")
        if gate(blob.decode("utf-8")):
            bad.append("round-trip: written file fails the gate")
        target.write_bytes(b"too\nlong\n" + b"x" * 250)
        if not gate(target.read_bytes().decode("utf-8")):
            bad.append("gate: over-limit multi-line file passed")
    if bad:
        print("self-test FAILED:")
        for item in bad:
            print("  - " + item)
        return 1
    print("self-test passed: entry is %d characters, %d bytes, "
          "single line" % (len(JOKE), len(JOKE.encode("utf-8"))))
    return 0


def main(argv=None):
    args = sys.argv[1:] if argv is None else argv
    if "--self-test" in args:
        return run_checks()
    out = TARGET
    if "--output" in args:
        pos = args.index("--output") + 1
        if pos >= len(args):
            raise SystemExit("--output needs a path after it")
        out = Path(args[pos])
    emit(out)
    print("wrote %d characters to %s" % (len(JOKE), out))
    return 0


if __name__ == "__main__":
    sys.exit(main())
