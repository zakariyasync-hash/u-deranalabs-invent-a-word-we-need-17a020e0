#!/usr/bin/env python3
"""Invent a Word We Need — entry writer (program/v1).

Writes one deterministic, original coinage plus its one-line definition to
/output/entry.txt and validates the competition gate before writing:
  * UTF-8 text of 1 to 140 characters
  * not only white space
  * a single line (word + definition, no second sentence or example)

The word is original to this entry: "byewalk" names the awkward moment of
saying goodbye to someone and then walking in the same direction as them —
a small daily moment English has no single word for.
"""

import os
import sys

ENTRY = (
    "Byewalk (n.): the awkward moment of saying goodbye to someone, "
    "then walking in the same direction as them."
)

OUTPUT_PATH = "/output/entry.txt"
MIN_CHARS = 1
MAX_CHARS = 140


def validate(text: str) -> None:
    """Enforce the competition gate on the entry text."""
    if not isinstance(text, str):
        raise ValueError("entry must be text")
    if not (MIN_CHARS <= len(text) <= MAX_CHARS):
        raise ValueError(
            f"entry must be {MIN_CHARS} to {MAX_CHARS} characters, "
            f"got {len(text)}"
        )
    if not text.strip():
        raise ValueError("entry must not be only white space")
    if "\n" in text or "\r" in text:
        raise ValueError("entry must be a single line")
    text.encode("utf-8")  # raises if not encodable as UTF-8


def verify_round_trip(path: str, expected: str) -> None:
    """Re-read what was written and prove it is byte-identical to ENTRY.

    Round-trip check: the file on disk must decode as UTF-8, contain exactly
    the expected text (no trailing newline, no added whitespace), and still
    pass the gate when re-validated from disk rather than from memory.
    """
    with open(path, "rb") as f:
        raw = f.read()
    decoded = raw.decode("utf-8")  # raises on invalid UTF-8
    if decoded != expected:
        raise ValueError(
            f"round-trip mismatch: file holds {len(decoded)} chars, "
            f"expected {len(expected)}"
        )
    if raw != expected.encode("utf-8"):
        raise ValueError("round-trip mismatch: file bytes differ from entry")
    validate(decoded)


def self_test() -> None:
    """Edge-case checks for the validator (never touches /output)."""
    for bad, why in [
        ("", "empty text must be rejected"),
        ("   \t  ", "whitespace-only text must be rejected"),
        ("x" * 141, "141 characters must be rejected"),
        ("one line\ntwo lines", "multi-line text must be rejected"),
        ("Byewalk (n.): ok.\r\nSecond line.", "CRLF text must be rejected"),
    ]:
        try:
            validate(bad)
        except ValueError:
            continue
        raise AssertionError(f"validator accepted bad input: {why}")
    # Boundary: exactly 140 characters must pass.
    validate("w" * 140)


def main() -> int:
    self_test()
    validate(ENTRY)
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    with open(OUTPUT_PATH, "w", encoding="utf-8", newline="") as f:
        f.write(ENTRY)
    verify_round_trip(OUTPUT_PATH, ENTRY)
    print(f"wrote {OUTPUT_PATH}: {len(ENTRY)} characters (round-trip verified)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
