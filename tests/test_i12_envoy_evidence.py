"""Expose Envoy-local I12 controls to Parent unittest discovery."""
from pathlib import Path
import unittest


def load_tests(_loader, _tests, _pattern):
    controls = Path(__file__).resolve().parents[1] / 'ci/runtime/lifecycle/i12/envoy'
    return unittest.TestLoader().discover(str(controls), pattern='test_*.py', top_level_dir=str(controls))



# Parent default discovery uses the one admitted active-case inventory.
if __import__("os").environ.get("ON_DEMAND_TESTS") != "1":
    def load_tests(loader, standard_tests, pattern):
        from ci.lib.active_test_inventory import module_load_tests
        return module_load_tests(loader, standard_tests, pattern)

if __name__ == '__main__':
    unittest.main()
