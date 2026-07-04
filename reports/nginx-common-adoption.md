# NGINX Common SDK adoption report

**Scope:** compile/structure evidence only. No production, CRS, full-matrix, or runtime verification is claimed.

| NGINX local function / field | Common replacement | Action | Reason |
| --- | --- | --- | --- |
| `enable` / `use_error_log` transitional flags | `msconnector_config.enable`, `msconnector_config.use_error_log`, `msconnector_parse_bool` | kept as thin adapter | NGINX merge and `ngx_conf_set_flag_slot` need native storage; values are synchronized into `common_config`. |
| `phase4_mode` integer constants/parser | `msconnector_config.phase4_mode`, `msconnector_parse_phase4_mode` | replaced | Phase-4 mode semantics are connector-neutral. |
| Phase-4 content-type validation helper | `msconnector_validate_content_type_token` | replaced | Content-type token validation is shared semantics; NGINX keeps file reading/allocation. |
| Config defaults/merge/validation in `ngx_http_modsecurity_merge_conf` | `msconnector_config_init`, `msconnector_config_merge`, `msconnector_config_validate` | replaced | Defaults and policy are Common-owned. |
| `ngx_command_t` directive table | Common directive macros/specs/adapters | kept as thin adapter | Registration is NGINX API, names/spec contracts are Common-owned. |
| Request header iteration over `ngx_list_t` and request strings | `msconnector_request`, `msconnector_request_mapper_contract`, Common header helpers | kept as thin adapter | NGINX owns `ngx_list_t`; mapper is exercised in the access path, emits Common request model, NUL-terminates request string fields, and validates it. |
| Response header iteration over `ngx_list_t` plus special headers | `msconnector_response`, `msconnector_response_mapper_contract` | kept as thin adapter | NGINX owns response state; mapper is exercised in header/body filter paths, emits Common response model, synthesizes Content-Type/Content-Length metadata when needed, and validates it. |
| Host fallback from `r->headers_in.server` | `msconnector_headers_host` plus NGINX fallback | kept as thin adapter | Common handles header lookup; NGINX fallback remains API-specific. |
| Body payload mapping | Common mapper contract body metadata | kept NGINX-specific | Mapper sets body size zero unless NGINX safely owns a buffered body; no payload logging. |
| Rule loading via libmodsecurity callbacks | Common rule load stats | kept as thin adapter | libmodsecurity loading is backend-specific; stats use Common structure. |
| Build source list | Common SDK source objects, including `transaction_state.c` with `event.c` | replaced | NGINX module build now includes Common objects needed by adopted calls and avoids unresolved `msconnector_phase_name`. |
| C standard checks | `ci/check-nginx-c-standards.sh` | replaced | C17 is hard when headers exist; C23/future-C are optional and skip safely. |

| Phase-4 intervention log text | metadata-only redaction summary plus Common JSON escaping/rule-id extraction | replaced | Raw ModSecurity intervention messages can contain payload/matched data; NGINX writes only presence markers and rule metadata. |
| Phase-4 content-type file wildcards | NGINX exact-match-only validation after Common token validation | kept as thin adapter | NGINX runtime scope matching is exact, so wildcard and malformed MIME entries are rejected during config load. |
| NGINX callback signatures | explicit `(void)` annotations for intentionally unused parameters | kept as NGINX-specific | NGINX callback ABI requires parameters that some callbacks do not use; annotations keep `-Wall -Wextra -Werror` meaningful without suppressing warnings. |
| Phase-4 rule-id extraction failures | positive-only `msconnector_rule_id_extract_from_message` result handling | replaced | Malformed or overlong IDs are not treated as success and the extraction buffer is initialized before use. |
| Phase-4 body limit directive | `MSCONNECTOR_DIRECTIVE_PHASE4_BODY_LIMIT` and `msconnector_parse_size` | replaced | NGINX registers the Common-known directive and maps it into `common_config.phase4_body_limit`. |
