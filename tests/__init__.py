"""Default unittest discovery uses the same admitted Parent inventory as CI."""
from pathlib import Path


def load_tests(loader, standard_tests, pattern):
    from ci.lib.active_test_inventory import load_inventory

    inventory = load_inventory(Path(__file__).resolve().parents[1])
    targets = [execution["selector"]["target"] for execution in inventory.executions
               if execution["selector"]["kind"] == "python"]
    return loader.loadTestsFromNames(targets)
