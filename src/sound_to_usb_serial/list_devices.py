import subprocess


def list_devices() -> list[str]:
    """Retrieve a list of available PulseAudio sources."""
    result = subprocess.run(
        ["pactl", "list", "sources", "short"],
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode != 0:
        raise RuntimeError(
            f"Failed to list PulseAudio sources: {result.stderr.strip()}"
        )

    devices = []
    for line in result.stdout.splitlines():
        parts = line.split("\t")
        if len(parts) >= 2:
            devices.append(parts[1])
    return devices


def print_devices() -> None:
    devices = list_devices()
    if not devices:
        print("No PulseAudio sources found.")
        return
    print("Available PulseAudio sources:")
    for device in devices:
        print(f"  {device}")


def choose_device() -> str:
    devices = list_devices()
    if not devices:
        raise RuntimeError("No PulseAudio sources found.")
    if len(devices) == 1:
        return devices[0]

    print("Available PulseAudio sources:")
    for i, device in enumerate(devices, 1):
        print(f"  {i}. {device}")

    while True:
        choice = input(f"Choose a device (1-{len(devices)}): ")
        if choice.isdigit():
            index = int(choice) - 1
            if 0 <= index < len(devices):
                return devices[index]
        print("Invalid choice. Please try again.")


def check_device(device: str) -> bool:
    return device in list_devices()


def init_device(args_device: str) -> str:
    if args_device and check_device(args_device):
        return args_device

    devices = list_devices()
    if not devices:
        raise RuntimeError("No PulseAudio sources found.")
    if len(devices) == 1:
        print(f"Only one PulseAudio source found: {devices[0]}. Using it.")
        return devices[0]

    return choose_device()


if __name__ == "__main__":
    print_devices()
