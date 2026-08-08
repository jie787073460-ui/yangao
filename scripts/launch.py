#!/usr/bin/env python3
"""Serve the bundled Yangao UI fidelity inspector on loopback only."""

from __future__ import annotations

import argparse
import contextlib
import http.server
import os
import socket
import socketserver
from pathlib import Path


APP_DIR = Path(__file__).resolve().parent.parent / "assets" / "app"


def available_port(preferred: int) -> int:
    with contextlib.closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as sock:
        try:
            sock.bind(("127.0.0.1", preferred))
            return preferred
        except OSError:
            sock.bind(("127.0.0.1", 0))
            return int(sock.getsockname()[1])


class QuietHandler(http.server.SimpleHTTPRequestHandler):
    def log_message(self, format: str, *args: object) -> None:
        return


class ReusableTCPServer(socketserver.TCPServer):
    allow_reuse_address = True


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--port", type=int, default=4179)
    args = parser.parse_args()
    if not (APP_DIR / "index.html").exists():
        raise SystemExit(f"App entry not found: {APP_DIR / 'index.html'}")
    port = available_port(args.port)
    os.chdir(APP_DIR)
    with ReusableTCPServer(("127.0.0.1", port), QuietHandler) as server:
        print(f"yangao ready: http://127.0.0.1:{port}", flush=True)
        try:
            server.serve_forever()
        except KeyboardInterrupt:
            pass


if __name__ == "__main__":
    main()
