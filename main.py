"""Entry for make.fun bounty "Describe Your Ex in One Word".

Writes exactly one word -- the verdict on the ex -- to
/output/entry.txt. Deterministic: no time, randomness, network,
or unordered iteration. Standard library only.
"""

import os
from pathlib import Path

WORD = "Depreciated"

OUTPUT_NAME = "entry.txt"


def gate(word: str) -> str:
    """Validate the entry word against the sealed-gate rules.

    Exactly one word, no whitespace inside, 1-111 characters,
    not only whitespace, spelled correctly, no punctuation.
    """
    if not isinstance(word, str):
        raise ValueError("word must be a string")
    if not word:
        raise ValueError("word must not be empty")
    if word != word.strip():
        raise ValueError("word must not have leading/trailing whitespace")
    if any(ch.isspace() for ch in word):
        raise ValueError("word must contain no whitespace")
    if not 1 <= len(word) <= 111:
        raise ValueError("word must be 1-111 characters")
    if not word.isalpha():
        raise ValueError("word must be letters only (no punctuation)")
    if len(word.split()) != 1:
        raise ValueError("word must be exactly one token")
    return word


def verify(path: Path, word: str) -> None:
    """Re-read the written file and assert byte-exact content.

    The file must decode as UTF-8, hold 1-111 characters, not be
    only whitespace, and match WORD + newline exactly.
    """
    raw = path.read_bytes()
    expected = (word + "\n").encode("utf-8")
    if raw != expected:
        raise ValueError(f"{path}: content mismatch: {raw!r} != {expected!r}")
    text = raw.decode("utf-8")
    if not 1 <= len(text) <= 111:
        raise ValueError(f"{path}: length {len(text)} outside 1-111")
    if not text.strip():
        raise ValueError(f"{path}: content is only whitespace")


def publish(word: str) -> Path:
    """Write WORD + newline to /output/entry.txt.

    Falls back to ./output/entry.txt when /output is not writable.
    Returns the path that was written.
    """
    content = word + "\n"
    candidates = [Path("/output") / OUTPUT_NAME, Path("output") / OUTPUT_NAME]
    last_error = None
    for target in candidates:
        try:
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(content, encoding="utf-8")
            return target
        except OSError as exc:  # /output not writable; try the fallback
            last_error = exc
    raise OSError(f"could not write {OUTPUT_NAME}: {last_error}")


def main() -> int:
    word = gate(WORD)
    path = publish(word)
    verify(path, word)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
