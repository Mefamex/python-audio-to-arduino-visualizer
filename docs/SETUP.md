# SETUP.md — From Scratch Development Setup

How the project is assembled step by step, for anyone who wants to build it from an empty directory.

## Prerequisites

* **Arduino :** IDE to flash `arduino_usb_to_led/arduino_usb_to_led.ino`
* **Python :** >=3.14  |
* **uv :** Dependency / environment manager
* **Make :** For the `make` shortcuts
* **System :** Linux + PulseAudio (`pulseaudio-utils` for `parec` & `pactl`)
* **Tree :** Optional, only for regenerating `docs/TREE.md` via `make tree`



<br><br>

## 1. Create the project

```bash
mkdir python-audio-to-arduino-visualizer
cd python-audio-to-arduino-visualizer
uv init
```

`uv init` bootstraps everything at once: `pyproject.toml`, `README.md`,
`.python-version`, `.gitignore`, a sample `main.py`, and it runs `git init`
automatically. It does **not** create the virtual environment yet — `.venv` is
created on the first `uv add` / `uv run` / `uv sync` (see steps 3–4).

> (the console script points at `python_audio_to_arduino_visualizer.main:main`).



<br><br>

## 2. Add the console script to `pyproject.toml`

`uv init` already created a basic `pyproject.toml`; add the console script
entrypoint so the CLI is exposed as a runnable command:

```toml
[project.scripts]
python-audio-to-arduino-visualizer = "python_audio_to_arduino_visualizer.main:main"
```

This maps the `python-audio-to-arduino-visualizer` command to the `main()`
function in the package, which is why `make run` / `uv run` work without
invoking Python directly.



<br><br>

## 3. Add the libraries

```bash
uv add numpy pyserial scipy
```

`uv add` resolves the latest Python-compatible versions, updates `pyproject.toml`
and `uv.lock`, and writes the packages into the project virtual environment.



<br><br>

## 4. Create the virtual environment / install

```bash
uv sync
```

`uv sync` ensures `.venv` exists (first `uv add` above already created it) and
installs the package as a venv entrypoint. The `make install` target does
exactly this.



<br><br>

## 5. Flash the Arduino and run

1. Upload `arduino_usb_to_led/arduino_usb_to_led.ino` via the Arduino IDE
   (pins 9/10/11, baud 115200).
2. Run the visualizer:

```bash
make run
# or
uv run python-audio-to-arduino-visualizer
```

The run loop is Linux/PulseAudio-only and requires a real serial device and an
audio monitor source — there is no mock/headless mode.



<br><br>

## Full Command Sequence

All the terminal commands above in one copy-paste block:

```bash
# 1. Create the project (uv init also runs git init)
mkdir python-audio-to-arduino-visualizer
cd python-audio-to-arduino-visualizer
uv init

# 2. Add the console script to pyproject.toml — see section 2 above for contents

# 3. Add the libraries
uv add numpy pyserial scipy

# 4. Create the virtual environment / install
uv sync

# 5. Flash the Arduino, then run
make run
# or
uv run python-audio-to-arduino-visualizer --port /dev/ttyUSB0 --device <monitor>
```