import subprocess
from typing import IO


def open_audio(device: str, sample_rate: int) -> subprocess.Popen[bytes]:
    command = [
        "parec",
        "--format=s16le",
        f"--rate={sample_rate}",
        "--channels=1",
        "--latency-msec=30",
        "--process-time-msec=5",
        f"--device={device}",
    ]
    return subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)


def read_audio_chunk(stream: IO[bytes], size: int) -> bytes:
    data = bytearray()
    while len(data) < size:
        part = stream.read(size - len(data))
        if not part:
            break
        data.extend(part)
    return bytes(data)
