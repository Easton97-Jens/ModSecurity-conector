#!/usr/bin/env python3
"""Qualify bounded Traefik composite start/recovery/keepalive/concurrency gates."""
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'composite_harness'))
from qualification import main

if __name__ == '__main__':
    sys.exit(main('traefik'))
