# INSTALL.md — INSTALLATION INSTRUCTIONS

The end-user install: clone the repository and let `uv` create the virtual
environment and sync dependencies.

## Prerequisites

|                     |                                                                |
| ------------------- | -------------------------------------------------------------- |
| **Python**          | 3.14 or higher                                                 |
| **Package Manager** | [uv](https://github.com/astral-sh/uv)                          |
| **Make**            | For automating the `make install` shortcut                     |
| **Tree**            | Optional, only for regenerating `docs/TREE.md` via `make tree` |

## Install

This project relies on `uv` for lightning-fast dependency management and
environment isolation.

```bash
git clone https://github.com/mefamex/python-audio-to-arduino-visualizer.git
cd python-audio-to-arduino-visualizer

# Automatically create the virtual environment and sync dependencies
make install
```

`make install` runs `uv sync`: it creates `.venv` and installs the package
(with its console script) as a venv entrypoint.



<br><br>

## Next steps

* Upload the Arduino sketch (`arduino_usb_to_led/arduino_usb_to_led.ino`) and run
  the visualizer — see **Usage** in [README.md](../README.md).
* Building the project **from scratch** (empty directory, `uv init`, adding the
  libraries one by one, etc.)? See **[SETUP.md](SETUP.md)**.