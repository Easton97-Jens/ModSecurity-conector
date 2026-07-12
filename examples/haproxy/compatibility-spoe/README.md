# HAProxy SPOE/SPOP compatibility example

**Language:** English | [Deutsch](README.de.md)

This directory preserves the former HAProxy SPOE/SPOP examples. It is separate
from the native HTX P1--P4 Safe reference in [../safe/](../safe/).

| File | Scope |
| --- | --- |
| haproxy-request-only.cfg | Request SPOE group for P1/P2-style request decisions. |
| haproxy-response-headers.cfg | Adds response-header SPOE; it is not response-body processing. |
| spoe-modsecurity.conf | SPOE agent, group, message, and returned-variable mapping. |
| modsecurity-agent.conf | SPOA process settings. |
| legacy-phase4-strict-abort.cfg | Disabled historical sample; never use as P4 evidence. |

## Values to adapt

| Name | Purpose and format | Required/default, setter, scope | Example and boundary |
| --- | --- | --- | --- |
| filter spoe engine modsecurity config | HAProxy SPOE filter and readable agent file | Required; host configuration; frontend scope | /etc/haproxy/spoe-modsecurity.conf. This selects compatibility SPOE, not native HTX. |
| send-spoe-group | Request or response-header SPOE message group | Required for its matching file; host configuration; request/response scope | request-check or response-check. response-check does not send a response body. |
| be_spoa_modsecurity | SPOP backend name and endpoint | Required; host configuration; backend scope | 127.0.0.1:12345. It must match the agent listen value. |
| groups and register-var-names | SPOE group names and returned transaction variables | Required; spoe-modsecurity.conf; agent scope | request-check response-check and blocked/action/status fields. Names must match HAProxy enforcement expressions. |
| max-frame-size | Positive SPOE frame byte limit | Required; spoe-modsecurity.conf; agent scope | 65532. It bounds a frame; it does not create P4 body support. |
| rules-file | Readable agent rules file | Required; modsecurity-agent.conf; SPOA scope | /etc/modsecurity/haproxy-rules.conf. A reviewed ruleset can block traffic. |
| decision-log, audit-log, log-file | Writable process log paths | decision-log required; others optional; SPOA scope | /var/log/haproxy-modsecurity. Protect metadata and do not log secrets. |
| response-body-limit and response-body-timeout | Compatibility response-body controls | Explicitly disabled; SPOA scope | 0 and 0. They must not be presented as P4 support. |

The SPOP address 127.0.0.1:12345, HAProxy listener 127.0.0.1:8080, upstream
127.0.0.1:8081, and /etc or /var/log paths are host examples, not
repository-relative paths.

This path must not be used to claim native HTX behavior, P4 response-body
handling, Safe late behavior, Strict abort behavior, first-byte-before-EOS
behavior, or no-full-response-buffer behavior.
