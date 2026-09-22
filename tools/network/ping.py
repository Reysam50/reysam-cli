import platform
import subprocess

TOOL = {
    "name": "ping",
    "description": "Ping a host using the system ping utility.",
    "category": "network",
}


def main(args: list[str]) -> int:
    if len(args) != 1:
        print("Usage: reysam network ping <host>")
        return 2

    host = args[0]
    count_flag = "-n" if platform.system().lower() == "windows" else "-c"
    result = subprocess.run(["ping", count_flag, "4", host], check=False)
    return result.returncode
