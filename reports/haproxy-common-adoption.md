# HAProxy Common SDK adoption

**Language:** English

This report records the HAProxy adoption layer migration boundary. The evidence is compile/structure evidence only: it is not a production, CRS, full-matrix, or runtime verification claim.

| HAProxy local function / field | Common replacement | Action | Reason |
| --- | --- | --- | --- |
| `haproxy_modsecurity_engine_config.common_config` | `msconnector_config` | replaced | HAProxy engine configuration embeds the connector-neutral config; HAProxy keeps only SPOA/libmodsecurity paths and process glue locally. |
| local config defaults/merge/validate | `msconnector_config_init`, `msconnector_config_apply_defaults`, `msconnector_config_merge`, `msconnector_config_validate` | replaced | Semantic defaults, inheritance, and validation live in Common. |
| HAProxy option names for ModSecurity directives | `MSCONNECTOR_DIRECTIVE_*`, `msconnector_directive_spec`, `msconnector_directive_adapter` | kept as thin adapter | HAProxy parsing/registration remains host glue; directive semantics and argument policy are Common-owned. |
| bool / phase4 / size / HTTP status parsing | `msconnector_parse_bool`, `msconnector_parse_phase4_mode`, `msconnector_parse_size`, `msconnector_parse_http_status` | replaced | Common owns primitive option parsing. |
| request structure projection | `msconnector_request`, `msconnector_request_mapper_contract` | kept as thin adapter | HAProxy/SPOE fields are mapped to Common request output and validated by the Common mapper contract. |
| response structure projection | `msconnector_response`, `msconnector_response_mapper_contract` | kept as thin adapter | HAProxy response metadata is mapped to Common response output and validated by the Common mapper contract. |
| host/header lookup | `msconnector_headers_host`, `msconnector_headers_find*`, `msconnector_headers_parse_content_length` | replaced | Header semantics are Common-owned; HAProxy keeps only frame/string lifetime mapping. |
| decision/intervention fields | `msconnector_decision`, `msconnector_late_intervention` | kept as thin adapter | libmodsecurity intervention capture remains HAProxy binding glue, while decision semantics are represented by Common primitives. |
| JSON escaping / event JSONL | `msconnector_json_escape`, `msconnector_event_write_jsonl_line` | kept as thin adapter | HAProxy-specific log transport may remain local; JSON syntax and event semantics are Common-owned. |
| rule id extraction | `msconnector_rule_id_extract_from_message` | replaced | Rule-id extraction is connector-neutral. |
| log sanitizing/redaction | `msconnector_sanitize_log_message`, `msconnector_redaction` | replaced | Sanitizing and redaction semantics are Common-owned; body payloads are not logged. |
| limits / DoS / flow / integrity | `msconnector_resource_limits`, `msconnector_dos_guard_check_*`, `msconnector_flow_guard`, `msconnector_integrity_event_hash` | kept as thin adapter | Global limits and guards are Common-owned; HAProxy runtime state decides when phases are observable. |
| rule loading stats | `msconnector_rule_load_stats`, `msconnector_rule_loader` | kept as thin adapter | libmodsecurity loading callbacks remain HAProxy binding glue; stats use Common structures where semantic counting is exposed. |
| CRS setup fields | `msconnector_crs_config` | kept as thin adapter | CRS setup consistency is Common-owned; no CRS runtime-verified claim is made. |
| SPOE/SPOP frame parsing and socket runtime | none | kept because HAProxy-specific | Protocol, process lifecycle, socket handling, return/action encoding, and generated HAProxy cfg snippets are connector-owned. |

## Removed duplicates

The HAProxy adoption layer no longer carries standalone duplicate parser, JSON escape, rule-id, config merge, config validation, header lookup, or status-normalization helpers when a Common primitive exists. Remaining code is connector glue around HAProxy/SPOE/SPOP and libmodsecurity APIs.

## C standard evidence

`ci/check-haproxy-c-standards.sh` performs a hard C17 object compile when HAProxy and libmodsecurity headers are discoverable. C23 and future-C (`c2y`) are optional and report skipped when unsupported by the compiler. Missing HAProxy or libmodsecurity headers are reported as `BLOCKED` with exit code 77.
