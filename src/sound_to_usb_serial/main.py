from __future__ import annotations

import argparse
import subprocess
import sys
import time

import numpy as np
import serial

from sound_to_usb_serial import config
from sound_to_usb_serial.audio_analyzer import AudioAnalyzer
from sound_to_usb_serial.list_devices import init_device, print_devices
from sound_to_usb_serial.list_ports import init_port, print_ports
from sound_to_usb_serial.ro_audio import open_audio, read_audio_chunk


RETRY_DELAYS = [3, 5, 10, 30, 60]  # seconds


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
    print("\n\n")
    time.sleep(0.5)
    print("====================================================")
    print(" PulseAudio Music Visualizer for Three Arduino LEDs")
    print("====================================================\n")

    time.sleep(0.5)
    print("\tINITIALIZING ARDUINO SERIAL PORTS...\n")
    port = init_port(args_port)
    print("\n====================================================\n")

    time.sleep(0.5)
    print("\tINITIALIZING PULSEAUDIO SOURCES...\n")
    device = init_device(args_device)
    print("\n====================================================\n")

    return port, device


def run(
    port: str, device: str, sample_rate: int, chunk_size: int, baud_rate: int
) -> None:
    print(f"Connecting to port {port}...")
    process: subprocess.Popen[bytes] | None = None

    try:
        with serial.Serial(port, baud_rate, timeout=0.2) as arduino:
            time.sleep(2)
            print("Arduino connection successful!")
            print("Starting PulseAudio (parec)...")

            process = open_audio(device, sample_rate)
            if process.stdout is None:
                raise RuntimeError("parec failed to create an audio stream.")

            analyzer = AudioAnalyzer(sample_rate=sample_rate, chunk_size=chunk_size)
            print("Audio-reactive LEDs are running. Press Ctrl+C to exit.")

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
        print(f"Error: {error}", file=sys.stderr)
        raise SystemExit(1) from error
    finally:
        if process is not None:
            process.terminate()
            process.wait(timeout=1)



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

    # 2. Auto-Recovery Configuration (Exponential Backoff)
    retry_delays = RETRY_DELAYS
    retry_count = 0

    # 3. Fault-Tolerant Main Loop
    while True:
        start_time = time.time()
        try:
            print(f"\nConnecting... Port: {port} | Device: {device}")
            
            # Execute the main workflow (Runs continuously until an exception is raised)
            run(port, device, args.sample_rate, args.chunk_size, args.baud_rate)
            
            # Exit the loop if run() finishes gracefully without exceptions
            break

        except KeyboardInterrupt:
            print("\n[INFO] User requested exit (Ctrl+C). Shutting down...")
            sys.exit(0)

        except (Exception, SystemExit) as e:
            # Ignore successful manual exits
            if isinstance(e, SystemExit) and e.code == 0:
                sys.exit(0)

            # Uptime Check: If the system remained stable for over 10 seconds,
            # consider it a fresh disconnect and reset the retry counter.
            if time.time() - start_time > 10:
                retry_count = 0

            # Extract the underlying error (since run() wraps exceptions in SystemExit)
            actual_error = getattr(e, "__cause__", e) or e
            print(f"\n[ERROR] Connection lost or process failed: {actual_error}")

            if retry_count < len(retry_delays):
                wait_time = retry_delays[retry_count]
                print(f"🔄 Retrying with cached settings in {wait_time}s... (Attempt {retry_count + 1}/{len(retry_delays)})")
                time.sleep(wait_time)
                retry_count += 1
            else:
                print("\n[FATAL] Maximum retry limit reached. Target device unreachable. Exiting.")
                sys.exit(1)


if __name__ == "__main__":
    main()
