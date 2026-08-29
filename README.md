# python-audio-to-arduino-visualizer

|             |            |
| ----------- | ---------- |
| AUTHOR :    | Mefamex    |
| LICENSE :   | MIT        |
| CREATED :   | 2024-07-18 |
| PUBLISHED : | 2026-08-29 |

A high-performance, lag-free music visualizer that captures system audio via PulseAudio and drives 3-channel LEDs using an Arduino.

Instead of relying on basic volume triggers, this tool uses digital signal processing (DSP) to separate audio into precise frequency bands, delivering a club-standard, visually pleasing light show right on your desk.

<br><br>

## Key Features
* **Precise Frequency Mapping:** Deep Bass (50-100Hz), Mid Bass (100-300Hz), and Treble/Cymbals (5000-7000Hz) mapped to 3 distinct PWM channels.
* **Auto Gain Control (AGC):** Dynamically adapts to volume changes. LEDs won't get stuck at 100% on loud songs or fade out completely on quiet acoustic tracks.
* **Cinematic Smoothing:** Built-in Exponential Moving Average (EMA) and Gamma Correction prevent harsh flickering and align LED brightness with human eye perception.
* **Bulletproof Serial Sync:** Uses a non-blocking `255` sync-byte protocol. Zero serial desync, no channel bleeding, and minimal CPU footprint.

<br><br>

## Hardware Setup
1. Any Arduino board (Uno, Nano, etc.).
2. 3 LEDs (or LED strips powered via MOSFETs) connected to PWM-supported pins: **9, 10, and 11**.
3. A Linux environment running PulseAudio.

<br><br>

## Requirements
|                      |                                                            |
| -------------------- | ---------------------------------------------------------- |
| **Arduino IDE**      | For uploading the Arduino sketch.                          |
| **Operating System** | Linux (Uses PulseAudio subsystem).                         |
| **PulseAudio**       | For capturing system audio.                                |
| **System Packages**  | `pulseaudio-utils` (for `parec` & `pactl`).                |
| **Python**           | Python 3.12 or higher.                                     |
| **Package Manager**  | [uv](https://github.com/astral-sh/uv) (Lightning-fast PM). |
| **Make**             | For automating installation and running the visualizer.    |

<br><br>

## Installation
This project relies on `uv` for lightning-fast dependency management and environment isolation.

```bash
git clone https://github.com/mefamex/python-audio-to-arduino-visualizer.git
cd python-audio-to-arduino-visualizer

# Automatically create the virtual environment and sync dependencies
make install

```

<br><br>

## Usage

First, upload the `arduino_usb_to_led/arduino_usb_to_led.ino` sketch to your Arduino via the Arduino IDE.

Once the hardware is ready, start the visualizer:

```bash
# Run the interactive CLI (auto-prompts for port and audio device)
make run

```

You can also run it in a single command by passing arguments directly:

```bash
uv run sound-to-usb-serial --port /dev/ttyUSB0 --device alsa_output.pci-0000.analog-stereo.monitor

```

**Helpful Commands:**

* `uv run sound-to-usb-serial --list-ports` (Find your Arduino port)
* `uv run sound-to-usb-serial --list-devices` (Find your audio monitor)
* `uv run sound-to-usb-serial --help` (View all configuration flags like sample rate and chunk size)

<br><br>


## Configuration & Customization

You can permanently bypass the interactive prompts or tweak the core DSP settings by editing the `src/sound_to_usb_serial/config.py` file.

```python
SERIAL_PORT = "/dev/ttyUSB0"  # Set your default Arduino port
DEVICE_NAME = "alsa_output.pci-0000_00_1f.3.analog-stereo.monitor" # Set default audio monitor
BAUD_RATE = 115200            # Serial communication speed
SAMPLE_RATE = 16000           # Lightweight audio sampling rate
CHUNK_SIZE = 300              # Buffer size for FPS rendering (~50 FPS)

```

Note:
- **Empty Values**: If you leave SERIAL_PORT or DEVICE_NAME empty (""), the CLI will automatically prompt you to choose from available devices upon startup.
- **Safety**: If your configured hardware isn't found, the program won't crash—it will safely catch the error and automatically fall back to the interactive selection menu.
- **Flexibility**: You can always override the default settings by passing command-line arguments when running the program.
- **Robustness**: Don't worry about hardcoding an incorrect or disconnected device/port: the system has built-in safety checks.
- **User Experience**: The program is designed to provide a smooth user experience even in the face of unexpected situations.

<br><br>

## Project Structure

`make tree`

```text
PYTHON AUDIO TO ARDUINO VISUALIZER
.
├── arduino_usb_to_led         # Arduino firmware directory
│   └── arduino_usb_to_led.ino # C++ sketch for high-speed serial parsing & PWM output
├── makefile                   # Shortcut commands for setup, formatting, and execution
├── pyproject.toml             # Python project metadata, dependencies, and CLI configs
├── README.md                  # Project documentation
├── src                        # Main source code directory
│   └── sound_to_usb_serial    # Core Python package
│       ├── audio_analyzer.py  # DSP logic: frequency filtering, AGC, and EMA smoothing
│       ├── config.py          # Centralized configuration variables (port, sample rate)
│       ├── __init__.py        # Package initialization and versioning
│       ├── list_devices.py    # PulseAudio source discovery, validation, and selection
│       ├── list_ports.py      # Arduino serial port discovery and validation
│       ├── main.py            # CLI entry point, arg parsing, and main execution loop
│       └── ro_audio.py        # Audio subprocess handling (parec) and chunk reading
├── tree.txt                   # Auto-generated directory structure record
└── uv.lock                    # Strict dependency lockfile for reproducible environments

4 directories, 13 files

Generated on Cts 29 Ağu 2026 21:48:33 +03
```

<br><br>

## License

Distributed under the MIT License. Developed by [Mefamex](https://www.mefamex.com).














