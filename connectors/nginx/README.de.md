# NGINX-Connector

**Sprache:** [English](README.md) | Deutsch

Status: Common-SDK-Adoption, Compile-/Structure-Evidence.

Der NGINX-Connector behält NGINX-eigene Integrationspunkte (`ngx_command_t`,
`ngx_http_request_t`, `ngx_chain_t`, `ngx_buf_t`, Filter, Pools, Return-Codes
und Build-Glue). Semantik für Config, Direktiven, Mapper-Verträge, Events und
Limits wird über `common/` angebunden, soweit diese Adoption implementiert ist.

Die C17-Prüfung ist hart, benötigt aber lokale NGINX- und libmodsecurity-Header;
fehlen diese Header, meldet der Check `BLOCKED` mit Exit 77. C23/future-C sind
optionale Compiler-Smokes. Diese Checks sind keine Production-, CRS-,
Full-Matrix- oder Runtime-Verifikation.

NGINX-Common-SDK-Modul-Builds mit kopiertem Connector-Quellbaum müssen `MSCONNECTOR_COMMON_SRC` (oder `CONNECTOR_COMMON_SRC` / `COMMON_SRC_ROOT`) auf den Common-Source-Root des Repositories setzen; `MSCONNECTOR_COMMON_INC` bleibt der Common-Include-Root. Ohne diese Variable wird nur auf `$ngx_addon_dir/../../common/src` zurückgefallen, wenn dieser Pfad existiert.


NGINX registriert `modsecurity_transaction_id` für NGINX-Variablen/Complex-Values, aber nicht die Apache-Ausdrucksdirektive `modsecurity_transaction_id_expr`. `modsecurity_phase4_body_limit` ist ein begrenzender Phase-4-Inspektionswert; überschrittene Bytes werden nicht an ModSecurity übergeben und nur als Metadaten markiert.
