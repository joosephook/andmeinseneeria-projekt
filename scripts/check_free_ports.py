#!/usr/bin/env python3
"""
Check host ports for availability.

Usage:
  python scripts/check_free_ports.py --compose-file docker-compose.example.yml
  python scripts/check_free_ports.py --ports 5432,80,443

Returns exit code 0 if all ports are free, 1 if any are in use.
"""
import argparse
import re
import socket
import sys
from pathlib import Path


def parse_ports_from_compose(path: Path):
    ports = set()
    if not path.exists():
        return ports
    text = path.read_text(encoding='utf-8')
    # crude parsing: find lines with - "HOST:CONTAINER" or - HOST:CONTAINER
    for line in text.splitlines():
        m = re.match(r"\s*-\s*\"?(\d+)(?:\:\d+)?\"?", line)
        if m:
            ports.add(int(m.group(1)))
        else:
            m2 = re.match(r"\s*-\s*(\d+):(\d+)", line)
            if m2:
                ports.add(int(m2.group(1)))
    return ports


def is_port_free(host: str, port: int) -> bool:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(0.5)
    try:
        s.bind((host, port))
        s.listen(1)
        return True
    except OSError:
        return False
    finally:
        try:
            s.close()
        except Exception:
            pass


def main(argv=None):
    p = argparse.ArgumentParser(description="Check host ports for availability")
    p.add_argument("--compose-file", help="Path to docker-compose file to parse ports from", default="docker-compose.example.yml")
    p.add_argument("--ports", help="Comma separated list of ports to check (overrides compose file)")
    p.add_argument("--host", help="Host to check (default 127.0.0.1)", default="127.0.0.1")
    args = p.parse_args(argv)

    ports = set()
    if args.ports:
        for part in args.ports.split(','):
            try:
                ports.add(int(part.strip()))
            except ValueError:
                print(f"Ignored invalid port: {part}")
    else:
        ports = parse_ports_from_compose(Path(args.compose_file))

    # default fallback ports if none found
    if not ports:
        ports = {5432, 80, 443, 8000, 8080}

    in_use = []
    free = []
    for port in sorted(ports):
        ok = is_port_free(args.host, port)
        if ok:
            free.append(port)
        else:
            in_use.append(port)

    if in_use:
        print("Ports in use on host {}:".format(args.host))
        for pnum in in_use:
            print(f"  - {pnum}")
        print("\nPlease free these ports or update docker-compose port mappings before starting containers.")
        return 1

    print("All checked ports are free:")
    for pnum in free:
        print(f"  - {pnum}")
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
