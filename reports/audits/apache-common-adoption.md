# Apache Common SDK adoption report

**Language:** English | [Deutsch](apache-common-adoption.de.md)

This report records the pre-change duplicate scan and the resulting Apache/Common split. It is a structure-level adoption report only; it does not claim Apache production readiness, CRS readiness, full-matrix coverage, or runtime verification.

| Apache local function / field | Common replacement | Action | Reason |
|---|---|---|---|
| `msc_conf_t.msc_state` | `msconnector_config.enable` | replaced | Enable/default/merge semantics are connector-neutral config semantics. |
| `msc_conf_t.use_error_log` | `msconnector_config.use_error_log` | replaced | Common owns the boolean setting; Apache only consumes it for APLOG forwarding. |
| `msc_conf_t.transaction_id` | `msconnector_config.transaction_id` | replaced | Static transaction ID storage/merge/validation belongs to Common. |
| `msc_conf_t.transaction_id_expr` string semantic | `msconnector_config.transaction_id_expr` | kept as thin adapter | Apache must keep compiled `ap_expr_info_t`; the raw expression is mirrored in Common config. |
| `msc_conf_t.phase4_mode` | `msconnector_config.phase4_mode` and `msconnector_parse_phase4_mode` | replaced | Phase-4 mode names and defaults are Common semantics. |
| `msc_conf_t.phase4_content_types_file` | `msconnector_config.phase4_content_types_file` | replaced | Path storage and merge are Common; APR file parsing remains Apache adapter code. |
| `msc_conf_t.phase4_log_path` | `msconnector_config.phase4_log_path` | replaced | Common config owns the setting; Apache only opens the APR file. |
| `msc_conf_t.phase4_body_limit` | `msconnector_config.phase4_body_limit` and `msconnector_parse_size` | replaced | Size parsing/default/merge are Common semantics. |
| Manual bool parsing in directive handlers | `msconnector_parse_bool` | replaced | On/off parsing is Common parser behavior. |
| Manual phase4 parsing | `msconnector_parse_phase4_mode` | replaced | Avoids duplicated minimal/safe/strict logic. |
| Manual size parsing | `msconnector_parse_size` | replaced | Avoids duplicated positive-decimal size logic. |
| Manual directory config merge | `msconnector_config_merge` | replaced | Common now merges semantic config fields; Apache still merges libmodsecurity rulesets and APR-owned arrays. |
| Apache `command_rec` directive table | `msconnector/directives.h` plus `msconnector_directive_adapter_find` | kept as thin adapter | `command_rec` is Apache API, while names/spec lookup come from Common. |
| Apache request header loops | `msc_apache_map_request` with `msconnector_request_mapper_contract` | kept as thin adapter | `request_rec` access is Apache-specific; output validates against Common mapper contract. |
| Apache response header loops | `msc_apache_map_response` with `msconnector_response_mapper_contract` | kept as thin adapter | Response extraction is Apache-specific; response model/contract are Common. |
| Response content-type lookup from `request_rec` | `msconnector_headers_*` for mapped models | kept because Apache-specific | Existing live filter still reads Apache response tables directly; Common mapper path is available for contract validation. |
| `apache_json_escape` | `msconnector_event_write_jsonl_line` / `msconnector_json_escape` | replaced | Event JSON escaping and JSONL formatting are Common semantics. |
| `apache_phase4_rule_id` | `msconnector_rule_id_extract_from_message` | replaced | Rule ID extraction is Common semantics. |
| Phase-4 event JSON string formatting | `msconnector_event` and `msconnector_event_write_jsonl_line` | replaced | Common owns metadata-only event JSONL shape; no body payload is written. |
| APR pools, bucket brigades, filters, hooks, APLOG, return codes | none | kept because Apache-specific | These are host server integration primitives and must not enter Common. |
| libmodsecurity `RulesSet` loading calls | `msconnector_rule_load_stats` | kept as thin adapter | Native rule loading is Apache/libmodsecurity integration; stats use Common structures. |

## C standard smoke coverage

Apache/Common-adoption compile compatibility is checked by
`ci/checks/connectors/apache/check-apache-c-standards.sh` and the Makefile targets
`check-apache-c17`, `check-apache-c23`, `check-apache-future-c`, and
`check-apache-c-standards`.

- C17 is mandatory and uses `-std=c17 -Wall -Wextra -Werror`.
- C23 and future-C are optional and skip when `ci/provisioning/toolchains/detect-c-standard.py` reports
  that the compiler lacks the requested mode.
- Missing APXS or Apache/APR/libmodsecurity headers is reported as `BLOCKED`
  with exit code `77`.

This is compile/structure evidence for the Apache/Common adoption layer only. It
is not production, CRS, full-matrix, or runtime verification evidence.

## Review follow-up fixes

- Apache APXS build path now appends the Common SDK source list used by the
  Apache adoption layer, so non-inline `msconnector_*` calls are built into the
  module rather than left as unresolved symbols.
- Directory merge now keeps a child static `modsecurity_transaction_id` ahead of
  any parent compiled `modsecurity_transaction_id_expr`; only a child expression
  or the absence of a merged static ID can inherit an expression pointer.
- `make lint` uses `check-apache-c17-lint`, which treats Apache C17
  `BLOCKED`/exit-77 header discovery as a lint skip while preserving
  `make check-apache-c17` as the hard compile check.
- Phase-4 intervention events set a non-OK Common status and record body
  truncation with metadata separate from JSON serialization truncation.
- The Apache response mapper includes `err_headers_out`, `headers_out`, and a
  synthetic `Content-Type` from `request_rec.content_type` only when no
  Content-Type header is already mapped.
