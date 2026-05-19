#!/bin/sh
set -eu

echo "smoke-installed: probing installed/system components (no build triggered)"

find_bin(){ command -v "$1" 2>/dev/null || true; }
HTTPD_BIN="${APACHE_BIN:-$(find_bin httpd)}"
[ -n "$HTTPD_BIN" ] || HTTPD_BIN="${APACHE_BIN:-$(find_bin apache2)}"
APXS_BIN="${APXS_BIN:-$(find_bin apxs)}"
[ -n "$APXS_BIN" ] || APXS_BIN="${APXS_BIN:-$(find_bin apxs2)}"
NGINX_BIN="${NGINX_BIN:-$(find_bin nginx)}"
PKG_CONFIG_BIN="${PKG_CONFIG_BIN:-$(find_bin pkg-config)}"

missing=0
req(){ [ -n "$2" ] || { echo "blocked: missing installed component: $1"; missing=1; }; }
req "apache/httpd binary" "$HTTPD_BIN"
req "apxs/apxs2" "$APXS_BIN"
req "nginx binary" "$NGINX_BIN"
req "pkg-config" "$PKG_CONFIG_BIN"

if [ "$missing" -ne 0 ]; then
  echo "blocked: installed smoke prerequisites incomplete"
  echo "hint: use make doctor for toolchain/install hints or run make smoke-all for source build path"
  exit 77
fi

echo "smoke-installed: detected apache_bin=$HTTPD_BIN"
echo "smoke-installed: detected apxs_bin=$APXS_BIN"
echo "smoke-installed: detected nginx_bin=$NGINX_BIN"

if "$PKG_CONFIG_BIN" --exists libmodsecurity; then
  echo "smoke-installed: pkg-config libmodsecurity found"
else
  echo "blocked: pkg-config cannot resolve libmodsecurity"
  echo "hint: install libmodsecurity development package or use source-build smoke path"
  exit 77
fi

echo "blocked: installed-runtime smoke execution is not yet wired to harness runtime configuration"
echo "blocked: no PASS reported; use make smoke-all (full source-build) or make smoke-cached"
exit 77
