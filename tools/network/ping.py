import subprocess


TOOL = {
    "name": "ping",
    "description": "Ping a host using the system ping utility.",
    "category": "network",
}


def main(args):
    if not args:
        print("Usage: reysam network ping <host>")
        return

    host = args[0]

    subprocess.run(
        ["ping", "-n", "4", host]
    )
