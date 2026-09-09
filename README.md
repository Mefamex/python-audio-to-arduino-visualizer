# python-audio-to-arduino-visualizer

|             |            |
| ----------- | ---------- |
| AUTHOR :    | Mefamex    |
| LICENSE :   | MIT        |
| CREATED :   | 2024-07-18 |
| PUBLISHED : | 2026-08-29 |
| UPDATED :   | 2026-09-09 |

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
| **Python**           | Python 3.14 or higher.                                     |
| **Package Manager**  | [uv](https://github.com/astral-sh/uv) (Lightning-fast PM). |
| **Make**             | For automating installation and running the visualizer.    |



<br><br>

## Usage

1. Upload `arduino_usb_to_led/arduino_usb_to_led.ino` to your Arduino (pins 9/10/11, baud 115200).
2. Start the visualizer:

```bash
make run
```

It auto-detects your serial port and audio source; pass `--port` / `--device` to skip the prompts. Stop anytime with `Ctrl+C`.

## Install

```bash
git clone https://github.com/mefamex/python-audio-to-arduino-visualizer.git
cd python-audio-to-arduino-visualizer
make install
```

`make install` runs `uv sync` — creates `.venv` and installs the CLI.

## Setup

Built the project from scratch (empty directory, `uv init`, adding the libraries one by one)? That's written up in the Setup guide.

> **Note:** The docs cover everything in detail — read them in order:
> **[docs/USAGE.md](docs/USAGE.md)** → **[docs/INSTALL.md](docs/INSTALL.md)** → **[docs/SETUP.md](docs/SETUP.md)**.

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

# Auto-retry after a disconnection or crash
RETRY_INTERVAL = 5            # Wait this many seconds between reconnect attempts
RETRY_TIMEOUT  = 300          # Give up after this many seconds (5 minutes)
```

Note:
- **Empty Values**: If you leave SERIAL_PORT or DEVICE_NAME empty (""), the CLI will automatically prompt you to choose from available devices upon startup.
- **Safety**: If your configured hardware isn't found, the program won't crash—it will safely catch the error and automatically fall back to the interactive selection menu.
- **Flexibility**: You can always override the default settings by passing command-line arguments when running the program.
- **Robustness**: If the Arduino or audio source drops mid-session, the visualizer retries every `RETRY_INTERVAL` seconds for up to `RETRY_TIMEOUT` seconds, then gives up cleanly. The error output is compact and timestamped, and each failure is labeled so you know whether the Arduino link or the audio source is the problem.
- **User Experience**: The program is designed to provide a smooth user experience even in the face of unexpected situations.

<br><br>

## Project Structure

```
make tree
```

The up-to-date markdown tree lives in **[docs/TREE.md](docs/TREE.md)** — refresh it with `make tree`.

<br><br>

## License

Distributed under the MIT License. Developed by [Mefamex](https://www.mefamex.com).





