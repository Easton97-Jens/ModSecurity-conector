"""Expose Envoy-local I12 controls to Parent unittest discovery."""
from pathlib import Path
import unittest


def load_tests(_loader, _tests, _pattern):
    controls = Path(__file__).resolve().parents[1] / 'ci/runtime/lifecycle/i12/envoy'
    return unittest.TestLoader().discover(str(controls), pattern='test_*.py', top_level_dir=str(controls))


if __name__ == '__main__':
    unittest.main()
