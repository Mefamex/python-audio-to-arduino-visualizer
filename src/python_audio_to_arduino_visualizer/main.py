from __future__ import annotations

import argparse
import subprocess
import sys
import time

import numpy as np
import serial

from python_audio_to_arduino_visualizer import config
from python_audio_to_arduino_visualizer.audio_analyzer import AudioAnalyzer
from python_audio_to_arduino_visualizer.list_devices import init_device, print_devices
from python_audio_to_arduino_visualizer.list_ports import init_port, print_ports
from python_audio_to_arduino_visualizer.ro_audio import open_audio, read_audio_chunk
from python_audio_to_arduino_visualizer.ui import (
    WIDTH,
    cyan,
    dim,
    fail,
    green,
    header,
    hint_for,
    red,
    selection_box,
    step,
)

RETRY_INTERVAL = config.RETRY_INTERVAL
RETRY_TIMEOUT = config.RETRY_TIMEOUT


def _now() -> str:
    return time.strftime("[%H:%M:%S]")


def _classify(error: BaseException | object | None) -> str:
    """Short label telling whether Arduino or the audio source failed."""
    text = str(error).lower() if isinstance(error, BaseException) else ""
    if any(
        key in text
        for key in (
            "could not open port",
            "/dev/tty",
            "ttyusb",
            "ttyacm",
            "serial",
            "arduino",
            "write failed",
            "input/output error",
        )
    ):
        return "NO ARDUINO connection found"
    if any(key in text for key in ("parec", "pulseaudio", "audio stream")):
        return "NO AUDIO source found"
    return "Connection lost"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="PulseAudio music visualizer for three Arduino LEDs"
    )
    parser.add_argument(
        "--port", default=config.SERIAL_PORT, help="Arduino serial port"
    )
    parser.add_argument(
        "--device", default=config.DEVICE_NAME, help="PulseAudio monitor source"
    )
    parser.add_argument(
        "--sample-rate",
        type=int,
        default=config.SAMPLE_RATE,
        help="Audio sample rate (default: 16000)",
    )
    parser.add_argument(
        "--chunk-size",
        type=int,
        default=config.CHUNK_SIZE,
        help="Audio chunk size (default: 300)",
    )
    parser.add_argument(
        "--baud-rate",
        type=int,
        default=config.BAUD_RATE,
        help="Arduino serial baud rate (default: 115200)",
    )
    parser.add_argument(
        "--list-devices", action="store_true", help="List PulseAudio sources and exit"
    )
    parser.add_argument(
        "--list-ports", action="store_true", help="List Arduino serial ports and exit"
    )
    return parser.parse_args()


def initialize_system(args_port: str, args_device: str) -> tuple[str, str]:
    header("PulseAudio Music Visualizer for Three Arduino LEDs")

    step("Searching Arduino serial ports")
    print()
    port = init_port(args_port)
    selection_box("Selected port", port)

    step("Searching PulseAudio sources")
    print()
    device = init_device(args_device)
    selection_box("Selected device", device)

    return port, device


def run(
    port: str,
    device: str,
    sample_rate: int,
    chunk_size: int,
    baud_rate: int,
    printDebug: bool = True,
) -> None:
    line = cyan("=" * WIDTH)
    if printDebug:
        print("\nConnecting...")
        print(f"  • Port:   {port}")
        print(f"  • Device: {device}")
    process: subprocess.Popen[bytes] | None = None

    try:
        with serial.Serial(port, baud_rate, timeout=0.2) as arduino:
            time.sleep(2)

            process = open_audio(device, sample_rate)
            if process.stdout is None:
                raise RuntimeError("parec failed to create an audio stream.")

            analyzer = AudioAnalyzer(sample_rate=sample_rate, chunk_size=chunk_size)

            # Always announce success: retries stay silent on failure,
            # but a (re)connection must be visible.
            print("")
            print(line)
            print(f" Connecting to port {port}...")
            print(f" {green('✔')} Arduino connection successful!")
            print(f" {green('✔')} Starting PulseAudio (parec)...")
            print(
                f" {green('✔')} Audio-reactive LEDs are running. Press Ctrl+C to exit."
            )
            print(f" {dim('↻ Auto-retry on: every 5s for 5 min if the link drops.')}")
            print(line)
            print("")

            while True:
                raw_data = read_audio_chunk(process.stdout, chunk_size * 2)
                if len(raw_data) < chunk_size * 2:
                    raise RuntimeError("parec closed the audio stream.")

                chunk = np.frombuffer(raw_data, dtype=np.int16)
                brightness = analyzer.brightness(chunk)
                arduino.write(bytes(brightness))

    except KeyboardInterrupt:
        print("\nClosing program gracefully...")
    except (OSError, serial.SerialException, RuntimeError) as error:
        raise SystemExit(1) from error
    finally:
        if process is not None:
            process.terminate()
            try:
                process.wait(timeout=1)
            except subprocess.TimeoutExpired:
                process.kill()
                process.wait()


def main() -> None:
    args = parse_args()

    if args.list_devices:
        print_devices()
        return

    if args.list_ports:
        print_ports()
        return

    # 1. Device Initialization (Executes once and caches the selection)
    try:
        port, device = initialize_system(args.port, args.device)
    except KeyboardInterrupt:
        print("\n[INFO] Initialization aborted by user.")
        sys.exit(0)
    except (RuntimeError, OSError, serial.SerialException) as error:
        fail(str(error), hint_for(str(error)))
        sys.exit(1)

    # 2. Auto-Recovery: fixed interval (RETRY_INTERVAL) until RETRY_TIMEOUT.
    first_failure: float | None = None

    # 3. Fault-Tolerant Main Loop
    while True:
        start_time = time.time()
        try:
            # Execute the main workflow (Runs continuously until an exception is raised)
            printdebug = True if first_failure is None else False
            run(
                port,
                device,
                args.sample_rate,
                args.chunk_size,
                args.baud_rate,
                printDebug=printdebug,
            )
            # Exit the loop if run() finishes gracefully without exceptions
            break

        except KeyboardInterrupt:
            print("\n[INFO] User requested exit (Ctrl+C). Shutting down...")
            sys.exit(0)

        except (Exception, SystemExit) as e:
            # Ignore successful manual exits
            if isinstance(e, SystemExit) and e.code == 0:
                sys.exit(0)

            # Stable for a while -> treat the next failure as a fresh outage.
            if time.time() - start_time > 10:
                first_failure = None
            is_first = first_failure is None
            if first_failure is None:
                first_failure = time.time()
            elapsed = time.time() - first_failure

            # The original exception rides along as __cause__ for classification.
            orig = getattr(e, "__cause__", None)
            if orig is None and isinstance(e, Exception):
                orig = e
            label = _classify(orig)

            if is_first:
                # Full detail only once per outage; retries stay compact.
                sys.stdout.flush()
                if orig is not None:
                    print(f"✖ Error: {orig}", file=sys.stderr)
                print(f"{red('=' * WIDTH, sys.stdout)}")
            print(
                f"{_now()} [ERROR] {label} (elapsed {int(elapsed)}s / {RETRY_TIMEOUT}s)"
            )

            if elapsed < RETRY_TIMEOUT:
                time.sleep(RETRY_INTERVAL)
            else:
                print(
                    f"\n{_now()} [FATAL] Retry timeout reached ({RETRY_TIMEOUT}s). Giving up."
                )
                sys.exit(1)


if __name__ == "__main__":
    main()
