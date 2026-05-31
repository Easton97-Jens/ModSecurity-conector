# lighttpd Source

Status: bridge-starter
Runtime status: not-verified

`lighttpd_build_starter.c` is repo-owned metadata/probe code.

`lighttpd_bridge.h`, `lighttpd_bridge.c`, and `lighttpd_bridge_main.c` are
repo-owned decision-service bridge-starter code. They compile and self-test a
local probe flow using connector-neutral `common/` helpers.

This is not production lighttpd adapter source. It does not include lighttpd
headers, call lighttpd APIs, call ModSecurity APIs, implement FastCGI/SCGI,
inspect real traffic, block requests, load CRS, or write audit logs.

Production source may only be added with repository-backed ORIGIN, license,
source-map, metadata, build, harness, No-CRS, With-CRS, and runtime evidence.
