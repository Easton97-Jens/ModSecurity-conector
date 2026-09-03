"""Static regression checks for NGINX's pre-commit ModSecurity error paths."""

from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
ACCESS = (ROOT / "connectors/nginx/src/ngx_http_modsecurity_access.c").read_text()
HEADERS = (ROOT / "connectors/nginx/src/ngx_http_modsecurity_header_filter.c").read_text()
BODY = (ROOT / "connectors/nginx/src/ngx_http_modsecurity_body_filter.c").read_text()


class NginxFailClosedContractTest(unittest.TestCase):
    def test_connection_and_uri_processing_fail_closed(self):
        self.assertIn('ret = msc_process_connection(ctx->modsec_transaction', ACCESS)
        self.assertIn('"ModSecurity: connection phase processing failed"', ACCESS)
        self.assertIn('ret = msc_process_uri(ctx->modsec_transaction', ACCESS)
        self.assertIn('"ModSecurity: URI phase processing failed"', ACCESS)

    def test_request_header_mapping_and_processing_fail_closed(self):
        self.assertIn('"ModSecurity: request hostname mapping failed"', ACCESS)
        self.assertIn('"ModSecurity: failed to add request header for inspection"', ACCESS)
        self.assertIn('return NGX_ERROR;', ACCESS)
        self.assertIn('if (ngx_http_modsecurity_add_request_headers(r, ctx) != NGX_OK)', ACCESS)
        self.assertIn('ret = msc_process_request_headers(ctx->modsec_transaction);', ACCESS)
        self.assertIn('"ModSecurity: request headers phase processing failed"', ACCESS)

    def test_response_header_mapping_and_processing_fail_closed(self):
        self.assertIn('if (ngx_http_modsecurity_add_response_headers(r, ctx) != NGX_OK)', HEADERS)
        self.assertIn('ret = msc_process_response_headers(ctx->modsec_transaction, status,', HEADERS)
        self.assertIn('"ModSecurity: response headers phase processing failed"', HEADERS)
        self.assertIn('NGX_HTTP_INTERNAL_SERVER_ERROR);', HEADERS)

    def test_request_and_response_body_append_fail_closed(self):
        self.assertIn('ret = msc_append_request_body(ctx->modsec_transaction, data,', ACCESS)
        self.assertIn('"ModSecurity: request body chunk processing failed"', ACCESS)
        self.assertIn('if (ret != 1) {', ACCESS)
        self.assertIn('ret = msc_request_body_from_file(ctx->modsec_transaction, file_name);', ACCESS)
        self.assertIn('"ModSecurity: request body file processing failed"', ACCESS)
        self.assertIn('if (ret != 1) {', ACCESS)
        self.assertIn('msc_append_response_body(ctx->modsec_transaction, data, allowed) != 1', BODY)


if __name__ == "__main__":
    unittest.main()
