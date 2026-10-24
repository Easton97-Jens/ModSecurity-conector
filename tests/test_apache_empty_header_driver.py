"""Real loopback HTTP controls for the Apache case request driver."""

from pathlib import Path
import unittest

if __package__:
    from . import header_driver_test_support
else:
    import header_driver_test_support


HARNESS = Path(__file__).resolve().parents[1] / "connectors/apache/harness/run_apache_smoke.sh"


class ApacheEmptyHeaderDriverTest(header_driver_test_support.RealHeaderDriverCase):
    harness = HARNESS
    empty_header_forms = ("X-No-Crs-Empty: \n", "X-No-Crs-Empty:\n")
    ordinary_value = "one: two "
    environment_options = {"CURL_HTTP_STATUS_FORMAT": "%{http_code}"}


if __name__ == "__main__":
    unittest.main()
