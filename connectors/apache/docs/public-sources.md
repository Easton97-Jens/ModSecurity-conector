# Apache Public Sources

Status: current references

Repository-owned Apache connector source lives under `connectors/apache/`.
External references are used for provenance, comparison, and optional
read-only rebuilds:

- Upstream ModSecurity-apache source:
  https://github.com/owasp-modsecurity/ModSecurity-apache
- Apache httpd source: https://github.com/apache/httpd
- Apache module/APXS build context: Apache httpd documentation

Source pins and generated build roots for clean-clone runtime validation are
documented in `COMPILE_APACHE.md` and the framework `ci/common.sh` helpers.
