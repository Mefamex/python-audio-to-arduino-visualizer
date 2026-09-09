import serial
import serial.tools.list_ports

from python_audio_to_arduino_visualizer.ui import choose_option


def list_ports() -> list[str]:
    """Retrieve a list of valid Arduino serial ports."""
    ports = serial.tools.list_ports.comports()
    valid_ports = [
        port.device for port in ports if "ttyU" in port.device or "ttyA" in port.device
    ]
    return sorted(valid_ports)


def print_ports() -> None:
    ports = list_ports()
    if not ports:
        print("No Arduino serial ports found.")
        return
    print("Available Arduino serial ports:")
    for port in ports:
        print(f"  {port}")


def choose_port() -> str:
    ports = list_ports()
    if not ports:
        raise RuntimeError("No Arduino serial ports found.")
    if len(ports) == 1:
        return ports[0]

    return choose_option("Available Arduino serial ports", ports, "Choose a port")


def check_port(port: str) -> bool:
    return port in list_ports()


def init_port(args_port: str) -> str:
    if args_port and check_port(args_port):
        return args_port

    ports = list_ports()
    if not ports:
        raise RuntimeError("No Arduino serial ports found.")
    if len(ports) == 1:
        return ports[0]

    return choose_port()


if __name__ == "__main__":
    print_ports()
