"""Cross-platform helpers for generator scripts."""

from __future__ import annotations

import os
import shutil
import sys
from pathlib import Path

IS_WINDOWS = os.name == "nt"


def exe_name(name: str) -> str:
    """Return an executable name with the correct platform suffix."""
    suffix = ".exe" if IS_WINDOWS else ""
    lname = name.lower()
    if lname.endswith(suffix):
        return name
    return f"{name}{suffix}"


def shared_lib_name(name: str) -> str:
    """Return a shared library name with the correct suffix."""
    suffix = ".dll" if IS_WINDOWS else ".so"
    lname = name.lower()
    if lname.endswith(suffix):
        return name
    return f"{name}{suffix}"


def delete_file(path: str) -> None:
    """Best-effort removal of a file without raising if it is absent."""
    target = Path(path)
    try:
        target.unlink()
    except FileNotFoundError:
        return
    except IsADirectoryError:
        shutil.rmtree(target, ignore_errors=True)


def delete_files(*paths: str) -> None:
    for path in paths:
        delete_file(path)


def python_cmd() -> str:
    """Return the Python executable for subprocess calls."""
    if sys.executable:
        return sys.executable
    return "python" if IS_WINDOWS else "python3"


def addchain_executable() -> str:
    """Resolve the addchain binary, adding .exe on Windows when needed."""
    configured = os.environ.get("ADDCHAIN", "addchain")
    candidates = [configured]
    if IS_WINDOWS and not configured.lower().endswith(".exe"):
        candidates.append(f"{configured}.exe")
    for candidate in candidates:
        found = shutil.which(candidate)
        if found:
            return found
    raise FileNotFoundError(
        "addchain executable not found. Build it from https://github.com/mmcloughlin/addchain "
        "and ensure it (or the ADDCHAIN env var) is on your PATH."
    )


def find_size_tool():
    """Return the best available size tool command (or None)."""
    for tool in ("size", "llvm-size"):
        found = shutil.which(tool)
        if found:
            return [found]
    return None
