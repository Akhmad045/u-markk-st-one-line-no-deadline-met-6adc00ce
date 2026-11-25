#!/usr/bin/env python3
"""One Line, No Deadline Met — make.fun entry.

Writes a single-line joke giving an excuse for missing a deadline
(87 characters) to /output/entry.txt, with no trailing newline, so the
sealed gate scorer reads exactly the line and nothing else.

Usage:
    python3 main.py [--output PATH] [--self-test]

--self-test validates the gate on the entry itself plus rejection
cases (empty, whitespace-only, multi-line, over-limit, control
characters) and a write/read round-trip in a temporary directory.
"""

import argparse
import sys
import tempfile
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
    if len(actual_bytes) != len(expected_bytes):
        raise SystemExit("read-back mismatch: file has the wrong byte length")
    return output


def check_file(path: Path) -> str:
    """Validate an existing entry file against the gate; '' when valid."""
    try:
        raw = path.read_bytes()
    except OSError as exc:
        return f"cannot read {path}: {exc}"
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError:
        return "file is not valid UTF-8"
    if raw != text.encode("utf-8"):
        return "file's bytes are not the entry's UTF-8 encoding"
    return validate(text)


def self_test() -> int:
    """Check the gate on the entry and on rejection cases."""
    failures = []

    def check(name: str, text: str, should_pass: bool) -> None:
        error = validate(text)
        if should_pass and error:
            failures.append(f"{name}: expected pass, got {error!r}")
        if not should_pass and not error:
            failures.append(f"{name}: expected rejection, passed")

    check("entry", LINE, True)
    check("one-char boundary", "!", True)
    check("200-char boundary", "x" * 200, True)
    check("empty", "", False)
    check("whitespace-only", "   ", False)
    check("over-limit", "x" * 201, False)
    check("multi-line", "one\ntwo", False)
    check("carriage return", "one\rtwo", False)
    check("leading space", " " + LINE, False)
    check("trailing space", LINE + " ", False)
    check("control character", "a\x01b", False)

    with tempfile.TemporaryDirectory() as tmp:
        target = Path(tmp) / "entry.txt"
        write_entry(target)
        if target.read_bytes() != LINE.encode("utf-8"):
            failures.append("round-trip: bytes differ from the entry")
        if target.read_bytes().endswith(b"\n"):
            failures.append("round-trip: file ends with a newline")
        file_error = check_file(target)
        if file_error:
            failures.append(f"round-trip: written file fails the gate: {file_error}")
        target.write_bytes(b"too\nlong\n" + b"x" * 250)
        if not check_file(target):
            failures.append("check_file: over-limit multi-line file passed")

    if failures:
        print("self-test FAILED:")
        for failure in failures:
            print(f"  - {failure}")
        return 1
    print(f"self-test passed: entry is {len(LINE)} characters, "
          f"{len(LINE.encode('utf-8'))} bytes, single line")
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Write the one-line entry to /output/entry.txt.")
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT,
                        help="where to write entry.txt (default: %(default)s)")
    parser.add_argument("--self-test", action="store_true",
                        help="validate the gate and exit")
    args = parser.parse_args(argv)
    if args.self_test:
        return self_test()
    write_entry(args.output)
    print(f"wrote {len(LINE)} characters to {args.output}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
