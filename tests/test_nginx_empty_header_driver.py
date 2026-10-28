"""Real loopback HTTP controls for the NGINX case request driver."""

from pathlib import Path
import unittest

if __package__:
    from . import header_driver_test_support
else:
    import header_driver_test_support


HARNESS = Path(__file__).resolve().parents[1] / "connectors/nginx/harness/run_nginx_smoke.sh"


class NginxEmptyHeaderDriverTest(header_driver_test_support.RealHeaderDriverCase):
    harness = HARNESS
    shell_helpers = "validate_nginx_request_output_path() { :; }\n"
    environment_options = {"NGINX_DOWNSTREAM_PROTOCOL": "http1", "SEND_CASE_MAX_TIME_SECONDS": "2"}



# Parent default discovery uses the one admitted active-case inventory.
if __import__("os").environ.get("ON_DEMAND_TESTS") != "1":
    def load_tests(loader, standard_tests, pattern):
        from ci.lib.active_test_inventory import module_load_tests
        return module_load_tests(loader, standard_tests, pattern)

if __name__ == "__main__":
    unittest.main()
