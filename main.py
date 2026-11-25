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
    if gate(got.decode("utf-8")):
        raise SystemExit("written file fails the gate on re-read")
    return path


def main(argv=None):
    args = sys.argv[1:] if argv is None else argv
    out = TARGET
    if "--output" in args:
        out = Path(args[args.index("--output") + 1])
    emit(out)
    print("wrote %d characters to %s" % (len(JOKE), out))
    return 0


if __name__ == "__main__":
    sys.exit(main())
