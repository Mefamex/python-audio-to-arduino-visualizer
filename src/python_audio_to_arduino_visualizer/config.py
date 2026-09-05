"""Configuration settings for the PulseAudio visualizer."""

SERIAL_PORT = ""  # e.g., "/dev/ttyUSB0" or "/dev/ttyACM0"
BAUD_RATE = 115200
SAMPLE_RATE = 16000
CHUNK_SIZE = 300
DEVICE_NAME = (
    ""  # e.g., "alsa_output.pci-0000_00_1f.3.analog-stereo.monitor" or "bluez_output.A8_99_DC_52_C7_A8.1.monitor"
)
