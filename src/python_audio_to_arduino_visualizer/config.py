"""Configuration settings for the PulseAudio visualizer."""

SERIAL_PORT = ""  # e.g., "/dev/ttyUSB0" or "/dev/ttyACM0"
BAUD_RATE = 115200
SAMPLE_RATE = 16000
CHUNK_SIZE = 300
DEVICE_NAME = (
    ""  # e.g., "alsa_output.pci-0000_00_1f.3.analog-stereo.monitor" or "bluez_output.A8_99_DC_52_C7_A8.1.monitor"
)

# LED smoothing / flash-speed range: how fast the LEDs react to audio changes.
# A single smoothing factor is derived from the current audio "activeness" and
# clamped between SMOOTHING_MIN and SMOOTHING_MAX. Higher values make the LEDs
# flash/react faster, lower values keep them smoother with a slower fade.
#   smoothing = clip(SMOOTHING_MIN + activeness * SMOOTHING_SCALE, SMOOTHING_MIN, SMOOTHING_MAX)
# Activeness roughly: ~0.0 = quiet, ~0.5 = energetic, ~1.0 = very loud.
# What changing each knob does (defaults in parentheses):
#
# SMOOTHING_MIN (=0.1) - calm-floor, how smooth the LEDs get during silence.
#   Lower (e.g. 0.02): nearly frozen/glowing LED at quiet parts.
#   Raise (e.g. 0.4):  stays a bit reactive even at silence.
#
# SMOOTHING_MAX (=0.85) - speed ceiling on loud parts.
#   Lower (e.g. 0.5):  peaks stay smooth, no sharp flashes at all.
#   Raise (e.g. 0.95): very snappy, jittery flashes on loud beats.
#
# SMOOTHING_SCALE (=2.5) - sensitivity: how fast smoothing ramps calm -> reactive.
#   Lower (e.g. 0.5): gentle, gradual response across a wide activeness range.
#   Raise (e.g. 5.0): saturates almost instantly, LED snaps between calm and
#                     fast (binary on/off feel).
#
# What each final smoothing value feels like on the LEDs:
#   ~0.10  -> nearly still, slow breath/glow
#   ~0.30  -> gentle, sluggish follow
#   ~0.50  -> balanced, medium reactivity
#   ~0.70  -> snappy, clearly tracks every beat
#   ~0.85+ -> maximum: sharp, jittery flashes on loud beats
SMOOTHING_MIN = 0.1
SMOOTHING_SCALE = 5
SMOOTHING_MAX = 0.85
