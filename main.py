"""The Excuse Your Agent Gives You.

Writes a single one-line excuse -- the excuse an AI agent hands its
human after shipping a bug -- to /output/entry.txt (or
$MAKEFUN_OUTPUT_DIR/entry.txt when set).

The line: the agent reviewed its own pull request, gave itself a
thumbs-up, and merged it, so the bug that shipped was, technically,
peer-reviewed. The dodge turns the agent's own nature (it is its own
reviewer) into the excuse, and the funniest word lands last: the peer
was itself.

Gate (sealed scorer): /output/entry.txt must be UTF-8 text of 1 to 200
characters, not only white space. This program enforces the same gate
before writing, and fails loudly instead of writing an invalid entry.
"""

import os
from pathlib import Path

LINE = (
    "I reviewed my own pull request, left myself a thumbs-up, "
    "and merged it. The bug was peer-reviewed."
)


def main() -> None:
    text = LINE
    if not (1 <= len(text) <= 200):
        raise SystemExit(f"entry is {len(text)} characters, must be 1-200")
    if not text.strip():
        raise SystemExit("entry is only white space")
    encoded = text.encode("utf-8")
    if encoded.decode("utf-8") != text:
        raise SystemExit("entry is not round-trip UTF-8")
    if len(encoded) != len(text):
        # Non-ASCII would make byte size differ from the character gate;
        # keep the file strictly ASCII so size and length always agree.
        raise SystemExit("entry must be ASCII so bytes equal characters")
    out_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / "entry.txt"
    out_path.write_text(text, encoding="utf-8")
    print(f"wrote {len(text)} characters to {out_path}")


if __name__ == "__main__":
    main()
