#!/usr/bin/env python3
"""One Line, No Deadline Met — make.fun entry.

Writes a single-line joke giving an excuse for missing a deadline
(87 characters) to /output/entry.txt, with no trailing newline, so the
sealed gate scorer reads exactly the line and nothing else.

Usage:
    python3 main.py [--output PATH] [--self-test]
"""

import argparse
import sys
from pathlib import Path

LINE = "I finished it on time, but my laptop autosaved it into a folder I've never seen before."

MAX_CHARS = 200
DEFAULT_OUTPUT = Path("/output/entry.txt")


def validate(text: str) -> str:
    """Return an error message if text fails the gate, else ''."""
    if not isinstance(text, str):
        return "entry is not text"
    if len(text) < 1:
        return "entry is empty"
    if len(text) > MAX_CHARS:
        return f"entry is {len(text)} characters, over the {MAX_CHARS} limit"
    if text.strip() == "":
        return "entry is only whitespace"
    if text != text.strip():
        return "entry has leading or trailing whitespace"
    if "\n" in text or "\r" in text:
        return "entry spans more than one line"
    if any(ord(ch) < 32 for ch in text):
        return "entry contains a control character"
    return ""


def write_entry(output: Path) -> Path:
    """Write exactly LINE to output and read it back to confirm."""
    error = validate(LINE)
    if error:
        raise SystemExit(f"invalid entry: {error}")
    expected_bytes = LINE.encode("utf-8")
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_bytes(expected_bytes)
    actual_bytes = output.read_bytes()
    if actual_bytes != expected_bytes:
        raise SystemExit("read-back mismatch: file does not hold the entry")
    return output


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Write the one-line entry to /output/entry.txt.")
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT,
                        help="where to write entry.txt (default: %(default)s)")
    args = parser.parse_args(argv)
    write_entry(args.output)
    print(f"wrote {len(LINE)} characters to {args.output}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
