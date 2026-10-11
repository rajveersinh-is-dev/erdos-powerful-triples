"""Make the repository runnable from a fresh clone without setting PYTHONPATH.

Every experiment script begins with

    import _bootstrap  # noqa: F401

which inserts ``<repo>/src`` onto ``sys.path``.  ``import _bootstrap`` works because
Python puts the script's own directory at the front of ``sys.path`` when a script is
run as ``python experiments/foo.py``.
"""

from __future__ import annotations

import json
import os
import sys


REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_SRC = os.path.join(REPO_ROOT, "src")
if os.path.isdir(_SRC) and _SRC not in sys.path:
    sys.path.insert(0, _SRC)


def write_result(name: str, payload) -> str:
    """Write ``payload`` as JSON into ``<repo>/results/name`` and return the path.

    Works from any working directory, and creates ``results/`` if needed.
    """
    out_dir = os.path.join(REPO_ROOT, "results")
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, name)
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(payload, fh, indent=2, default=str)
    return path