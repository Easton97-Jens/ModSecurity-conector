# HAProxy SPOE/SPOA Example Syntax Validation

**Language:** English | [Deutsch](syntax-validation.de.md)

## Status
validation_status: documentation_only
runtime_verified: false
syntax_executed: false
decision_status: undecided
promoted: false

## Purpose
This document only checks in a documentary manner which example lines are provided by external
HAProxy/SPOE documentation is supported. It does not perform any configuration and
does not prove runtime capability.

## Sources

| Source | URL/path | Retrieval date | Relevance |
|---|---|---|---|
| HAProxy Configuration Manual (latest) | https://www.haproxy.com/documentation/haproxy-configuration-manual/latest/ | 2026-05-24 | External classification of the HAProxy directive structure including SPOE filter form |
| HAProxy SPOE/SPOP reference (referenced via HAProxy documentation) | https://raw.githubusercontent.com/haproxy/haproxy/master/doc/SPOE.txt | 2026-05-24 | External detailed reference for SPOE/SPOP syntax and terms |
| Local example configuration | connectors/haproxy/poc/spoe/haproxy.cfg.example | 2026-05-24 | Example-only HAProxy placeholders to be validated |
| Local SPOE-Agent-Playdatei | connectors/haproxy/poc/spoe/spoe-agent.conf.example | 2026-05-24 | Zu validating example-only SPOE/SPOA-Platzhalter |
| Local classification | connectors/haproxy/poc/spoe/README.md | 2026-05-24 | Documented example-only/not runtime verified framework |
| Local evidence | connectors/haproxy/docs/spoe-external-evidence.md | 2026-05-24 | Already documented external SPOE facts in the repository |

## Validation rules
Each line/directive is marked with a status:
- externally documented
- repo documented
- illustrative placeholders
- needs external verification
- not proven

## haproxy.cfg.example section check

| Section/Directive | Status | receipt | Comment |
|---|---|---|---|
| `global` | externally documented | HAProxy Configuration Manual (latest) | Section type is externally documented; Specific values ​​in the example remain placeholders. |
| `defaults` | externally documented | HAProxy Configuration Manual (latest) | Section type documented externally; Semantics of the example values ​​not runtime verified. |
| `frontend` | externally documented | HAProxy Configuration Manual (latest) | Section type documented externally. |
| `backend` | externally documented | HAProxy Configuration Manual (latest) | Section type documented externally. |
| `filter spoe [engine <name>] config <file>` (commented form) | externally documented | HAProxy Configuration Manual (latest) | Only this form is documented externally; Specific engine/path values ​​in the example are not documented. |
| SPOE backend (`be_spoe_agent_poc`) | needs external verification | HAProxy Manual + SPOE external evidence (repo) | Dedicated backends are mentioned externally; The specific backend topology in the example remains open. |
| Example ports (`:8080`, `:18080`, `:19090`) | illustrative placeholders | Local file `haproxy.cfg.example` | Placeholder values ​​without production statement. |
| Timeouts (`5s/30s`) | illustrative placeholders | Local file `haproxy.cfg.example` | example values; Suitability still to be checked. |
| Logging (`log stdout format raw local0`) | needs external verification | HAProxy Manual (general) + local file | Directive interpretation not proven in the specific PoC context. |
| Comment warnings (`example_only`, `runtime_verified: false`, external audit notes) | repo documented | `connectors/haproxy/poc/spoe/haproxy.cfg.example` | Consistent with local documentation-only framework. |

## spoe-agent.conf.example Section check

| Section/Directive | Status | receipt | Comment |
|---|---|---|---|
| Engine/Agent Section (`[spoe-engine placeholder]`, `spoe-agent backend ...`) | needs external verification | SPOE/SPOP reference + local file | Designed as an illustrative structure; exact syntax compatibility not proven. |
| Messages/Events (`[spoe-message ...]`, `event on-frontend-http-request`) | needs external verification | SPOE/SPOP reference + local file | Event/message form in the example is not runtime tested. |
| Request metadata fields (method/path/query/headers as comment) | illustrative placeholders | Local file `spoe-agent.conf.example` | Planned fields, not confirmed completeness. |
| Response fields | not proven | Local file + SPOE external evidence | Response field coverage not used in the example. |
| Intervention result fields (`allow|block|log` placeholder) | illustrative placeholders | Local file `spoe-agent.conf.example` | Mapping semantics explicitly open; no confirmation of term. |
| Error/Timeout Behavior | not proven | Local file + external sources | Not specified, therefore unproven. |
| Comments on Response Body (`Noch zu prüfen.`) | repo documented | `spoe-agent.conf.example` | Correctly marked as open; no availability claim. |
| Comments on Intervention Mapping (`Noch zu prüfen.`) | repo documented | `spoe-agent.conf.example` | Correctly marked as open; no final mapping claimed. |

## Result
- Above all, the basic HAProxy section types are documented externally
  (`global/defaults/frontend/backend`) and the SPOE filter form
  `filter spoe [engine <name>] config <file>`. (Externally occupied)
- Parts with concrete names, ports, timeout values and local paths are only
  illustrative placeholders. (Derived)
- Exact SPOE agent syntax, full field coverage and concrete
  Runtime semantics remain unproven. (To be checked / not proven)
- The files must still be clearly verified as example-only/not runtime
  be treated. (Proven by repository)

## Not proven
- The sample configuration was not executed.
- HAProxy was not started.
- No SPOA agent has been started.
- No request check was carried out.
- No block/allow decision was verified.
- No response header/response body behavior was verified.
- No runtime report was generated.

## Next step
Then create a documentation-only agent design plan at
`connectors/haproxy/poc/spoe/agent/design.md` without writing any code.
