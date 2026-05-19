#!/bin/sh
set -eu

BUILD_ROOT="${BUILD_ROOT:-/src/ModSecurity-conector-build}"
HTTPD_BIN="${HTTPD_BIN:-$BUILD_ROOT/apache-runtime/httpd/bin/httpd}"
APXS_BIN="${APXS_BIN:-$BUILD_ROOT/apache-runtime/httpd/bin/apxs}"
APACHE_MODULE="${APACHE_MODULE:-$BUILD_ROOT/apache-build/output/apache/mod_security3.so}"
APACHE_LIBMODSEC="${APACHE_LIBMODSEC:-$BUILD_ROOT/apache-build/output/modsecurity/lib/libmodsecurity.so}"
NGINX_BIN="${NGINX_BIN:-$BUILD_ROOT/nginx-runtime/nginx/sbin/nginx}"
NGINX_MODULE="${NGINX_MODULE:-$BUILD_ROOT/nginx-runtime/nginx/modules/ngx_http_modsecurity_module.so}"
NGINX_LIBMODSEC="${NGINX_LIBMODSEC:-$BUILD_ROOT/nginx-build/output/modsecurity/lib/libmodsecurity.so}"

missing=0
check_file(){ [ -e "$1" ] || { echo "blocked: missing cached artifact: $1"; missing=1; }; }
check_exec(){ [ -x "$1" ] || { echo "blocked: missing executable cached artifact: $1"; missing=1; }; }

echo "smoke-cached: checking cached artifacts under BUILD_ROOT=$BUILD_ROOT"
check_exec "$HTTPD_BIN"
check_exec "$APXS_BIN"
check_file "$APACHE_MODULE"
check_file "$APACHE_LIBMODSEC"
check_exec "$NGINX_BIN"
check_file "$NGINX_MODULE"
check_file "$NGINX_LIBMODSEC"

if [ "$missing" -ne 0 ]; then
  echo "blocked: cached smoke prerequisites not satisfied; run full build smoke first (make smoke-all)"
  exit 77
fi

echo "smoke-cached: artifacts present; running smoke without rebuild"
BUILD_HTTPD_FROM_SOURCE=0 BUILD_PCRE2_FROM_SOURCE=0 BUILD_NGINX_FROM_SOURCE=0 make smoke-all
