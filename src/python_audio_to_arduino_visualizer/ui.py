"""Minimal terminal styling helpers (stdlib only, no new dependencies)."""

from __future__ import annotations

import os
import sys

WIDTH = 60


def _use_color(stream) -> bool:
    return not (os.environ.get("NO_COLOR") or os.environ.get("TERM") == "dumb") and stream.isatty()


def _paint(code: str, text: str, stream) -> str:
    return text if not _use_color(stream) else f"\033[{code}m{text}\033[0m"


def red(text: str, stream=sys.stderr) -> str:
    return _paint("31", text, stream)


def green(text: str, stream=sys.stdout) -> str:
    return _paint("32", text, stream)


def cyan(text: str, stream=sys.stdout) -> str:
    return _paint("36", text, stream)


def dim(text: str, stream=sys.stdout) -> str:
    return _paint("2", text, stream)


def header(title: str) -> None:
    line = "=" * WIDTH
    print(f"\n{cyan(line)}")
    print(cyan(f" {title}"))
    print(f"{cyan(line)}\n")


def step(label: str) -> None:
    print(f"  {cyan('›')} {label}...")


def ok(message: str) -> None:
    print(f"  {green('✔')} {message}")


def fail(message: str, hint: str = "") -> None:
    """Single clean error block on stderr (no traceback)."""
    sys.stdout.flush()
    mark = red("✖", sys.stderr)
    print(f"\n  {mark} {red(message, sys.stderr)}", file=sys.stderr)
    if hint: print(f"    {dim('→', sys.stderr)} {dim(hint, sys.stderr)}", file=sys.stderr)
    print(file=sys.stderr)


def selection_box(label: str, value: str) -> None:
    line = "=" * WIDTH
    print(f"{cyan(line)}")
    print(f" {label}: {green(value)}")
    print(f"{cyan(line)}\n")


def choose_option(title: str, options: list[str], prompt: str) -> str:
    """Print a colored selection list and return the chosen option."""
    print(f"  {title}:")
    for i, item in enumerate(options, 1):
        print(f"    {cyan(f'{i}.', sys.stdout)} {item}")
    print()

    while True:
        try:
            raw = input(f"  {cyan('›', sys.stdout)} {prompt} (1-{len(options)}): ").strip()
        except KeyboardInterrupt, EOFError:
            print()
            raise KeyboardInterrupt from None
        if raw.isdigit():
            index = int(raw) - 1
            if 0 <= index < len(options):
                print()
                return options[index]
        print(f"  {red('✖', sys.stdout)} Invalid choice. Please try again.")


def hint_for(error: str) -> str:
    low = error.lower()
    if "arduino" in low or "serial" in low or "ttyu" in low or "ttya" in low:
        return "Check the USB connection, then try: --list-ports"
    if "pulseaudio" in low or "source" in low or "pactl" in low or "parec" in low:
        return "Check PulseAudio/PipeWire, then try: --list-devices"
    return ""
