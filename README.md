# python-audio-to-arduino-visualizer

|             |            |
| ----------- | ---------- |
| AUTHOR :    | Mefamex    |
| LICENSE :   | MIT        |
| CREATED :   | 2024-07-18 |
| PUBLISHED : | 2026-08-29 |
| UPDATED :   | 2026-09-05 |

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
| **Python**           | Python 3.14 or higher.                                |
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
uv run python-audio-to-arduino-visualizer --port /dev/ttyUSB0 --device alsa_output.pci-0000.analog-stereo.monitor

```

**Helpful Commands:**

* `uv run python-audio-to-arduino-visualizer --list-ports` (Find your Arduino port)
* `uv run python-audio-to-arduino-visualizer --list-devices` (Find your audio monitor)
* `uv run python-audio-to-arduino-visualizer --help` (View all configuration flags like sample rate and chunk size)

<br><br>


## Configuration & Customization

You can permanently bypass the interactive prompts or tweak the core DSP settings by editing the `src/python_audio_to_arduino_visualizer/config.py` file.

```python
SERIAL_PORT = "/dev/ttyUSB0"  # Set your default Arduino port
DEVICE_NAME = "alsa_output.pci-0000_00_1f.3.analog-stereo.monitor" # Set default audio monitor
BAUD_RATE = 115200            # Serial communication speed
SAMPLE_RATE = 16000           # Lightweight audio sampling rate
CHUNK_SIZE = 300              # Buffer size for FPS rendering (~50 FPS)

# LED smoothing / flash speed
SMOOTHING_MIN = 0.1           # Calm floor: how smooth LEDs stay during silence
SMOOTHING_SCALE = 2.5         # Sensitivity: how fast smoothing ramps with activeness
SMOOTHING_MAX = 0.85          # Speed ceiling: sharpest flashes on loud parts

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
Project Structure:

PYTHON AUDIO TO ARDUINO VISUALIZER
.
├── arduino_usb_to_led
│   └── arduino_usb_to_led.ino
├── LICENSE
├── makefile
├── pyproject.toml
├── README.md
├── src
│   └── python_audio_to_arduino_visualizer
│       ├── audio_analyzer.py
│       ├── config.py
│       ├── __init__.py
│       ├── list_devices.py
│       ├── list_ports.py
│       ├── main.py
│       └── ro_audio.py
├── tree.txt
└── uv.lock

4 directories, 14 files

Generated on 2026-09-05 08:33:53
```

<br><br>

## License

Distributed under the MIT License. Developed by [Mefamex](https://www.mefamex.com).














