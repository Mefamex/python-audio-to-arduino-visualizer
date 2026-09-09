# USAGE.md — RUNNING THE VISUALIZER

Quick reference for the `python-audio-to-arduino-visualizer` CLI — every command
and the output it actually produces.

<br><br>

## 1. Install

```bash
git clone https://github.com/mefamex/python-audio-to-arduino-visualizer.git
cd python-audio-to-arduino-visualizer
make install
```

Full instructions: **[INSTALL.md](INSTALL.md)**.

<br><br>

## 2. Find your hardware

### Arduino serial port

```bash
uv run python-audio-to-arduino-visualizer --list-ports
```

Output:

```
Available Arduino serial ports:
  /dev/ttyUSB0
```

### Audio monitor source

The visualizer only works with PulseAudio monitor sources, not sinks.

**Prefer .monitor** sources.


```bash
uv run python-audio-to-arduino-visualizer --list-devices
```

Output:

```
Available PulseAudio sources:
  alsa_output.pci-0000_00_1f.3.analog-stereo.monitor
  easyeffects_sink.monitor
  easyeffects_source
```

<br><br>

## 3. Start the visualizer

```bash
make run
# or
uv run python-audio-to-arduino-visualizer
```

or, passing the port and device directly (no interactive prompts):

```bash
uv run python-audio-to-arduino-visualizer --port /dev/ttyUSB0 --device alsa_output.pci-0000_00_1f.3.analog-stereo.monitor
```

Expected startup output:

```

============================================================
 PulseAudio Music Visualizer for Three Arduino LEDs
============================================================

  › Searching Arduino serial ports...

============================================================
 Selected port: /dev/ttyUSB0
============================================================

  › Searching PulseAudio sources...

============================================================
 Selected device: alsa_output.pci-0000_00_1f.3.analog-stereo.monitor
============================================================


Connecting...
  • Port:   /dev/ttyUSB0
  • Device: alsa_output.pci-0000_00_1f.3.analog-stereo.monitor

============================================================
 Connecting to port /dev/ttyUSB0...
 ✔ Arduino connection successful!
 ✔ Starting PulseAudio (parec)...
 ✔ Audio-reactive LEDs are running. Press Ctrl+C to exit.
 ↻ Auto-retry on: every 5s for 5 min if the link drops.
============================================================

```

Stop it any time with `Ctrl+C`:

```

Closing program gracefully...
```

<br><br>

## 4. All configuration flags

```bash
uv run python-audio-to-arduino-visualizer --help
```

Output:

```
usage: python-audio-to-arduino-visualizer [-h] [--port PORT] [--device DEVICE]
                                          [--sample-rate SAMPLE_RATE]
                                          [--chunk-size CHUNK_SIZE]
                                          [--baud-rate BAUD_RATE]
                                          [--list-devices] [--list-ports]

PulseAudio music visualizer for three Arduino LEDs

options:
  -h, --help            show this help message and exit
  --port PORT           Arduino serial port
  --device DEVICE       PulseAudio monitor source
  --sample-rate SAMPLE_RATE
                        Audio sample rate (default: 16000)
  --chunk-size CHUNK_SIZE
                        Audio chunk size (default: 300)
  --baud-rate BAUD_RATE
                        Arduino serial baud rate (default: 115200)
  --list-devices        List PulseAudio sources and exit
  --list-ports          List Arduino serial ports and exit
```

<br><br>

## 5. Notes

* If `--port` / `--device` are omitted (and `config.py` defaults are empty), the
  CLI lists the available hardware and prompts you to pick one — same as the
  `--list-ports` / `--list-devices` output above.
* If the Arduino or the audio source drops mid-session, the visualizer retries
  every `RETRY_INTERVAL` seconds (default 5s) for up to `RETRY_TIMEOUT` seconds
  (default 300s), printing a compact timestamped error, then gives up cleanly.