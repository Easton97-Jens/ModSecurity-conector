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
