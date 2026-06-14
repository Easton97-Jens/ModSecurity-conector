# NGINX Public Sources

Status: current references

Repository-owned NGINX connector source lives under `connectors/nginx/`.
External references are used for provenance, comparison, and optional
read-only rebuilds:

- Upstream ModSecurity-nginx source:
  https://github.com/owasp-modsecurity/ModSecurity-nginx
- NGINX Open Source: https://github.com/nginx/nginx
- NGINX configure documentation: https://nginx.org/en/docs/configure.html

Source pins and generated build roots for clean-clone runtime validation are
documented in `COMPILE_NGINX.md` and the framework `ci/common.sh` helpers.
