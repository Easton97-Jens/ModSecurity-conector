"""Default unittest discovery uses the same admitted Parent inventory as CI."""
from pathlib import Path


def load_tests(loader, standard_tests, pattern):
    from ci.lib.active_test_inventory import load_inventory, python_discovery_suite

    inventory = load_inventory(Path(__file__).resolve().parents[1])
    return python_discovery_suite(inventory, loader)
