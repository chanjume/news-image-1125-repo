#!/usr/bin/env python3
"""Copy the finished front page to the grader's output directory.

Entry for news-image-20261125: THE WORLD, Wednesday 25 November 2026.
The picture itself is drawn by render.py (Pillow, DejaVu fonts) and
shipped here as entry.png; this program only places a byte-identical
copy at $MAKEFUN_OUTPUT_DIR/entry.png, using the standard library.
"""

import hashlib
import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))


def _digest(path):
    digest = hashlib.sha256()
    with open(path, "rb") as handle:
        for block in iter(lambda: handle.read(65536), b""):
            digest.update(block)
    return digest.hexdigest()


def main():
    source = os.path.join(HERE, "entry.png")
    if not os.path.isfile(source):
        print("entry.png is missing from this repository", file=sys.stderr)
        sys.exit(1)
    destination_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(destination_dir, exist_ok=True)
    destination = os.path.join(destination_dir, "entry.png")
    shutil.copyfile(source, destination)
    if _digest(source) != _digest(destination):
        print("copy check failed: sha256 differs", file=sys.stderr)
        sys.exit(1)
    print("wrote %s sha256=%s" % (destination, _digest(destination)))


if __name__ == "__main__":
    main()
