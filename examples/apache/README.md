# Apache ModSecurity Examples

These examples show request-only and bounded Phase 4 response-body inspection
for Apache httpd.

- Load `mod_security3.so`, enable `modsecurity on`, and point
  `modsecurity_rules_file` at a production config under `/etc/modsecurity`.
- Put CRS under `/etc/modsecurity/crs` and include it from the ModSecurity
  config.
- Request-only mode sets `SecResponseBodyAccess Off`; it is the safer default
  when late response disruption is not acceptable.
- Phase 4 mode sets `SecResponseBodyAccess On`, MIME restrictions, and bounded
  response-body limits. The Apache connector also uses
  `modsecurity_phase4_body_limit` to bound connector buffering.
- If Apache can inspect the buffered response before commit, a disruptive Phase
  4 rule can return a blocking status. If the response has already committed,
  the connector records strict-abort evidence instead.
- Connector decisions are JSON lines in
  `/var/log/modsecurity/apache-phase4.jsonl`; Apache access/error logs stay
  under `/var/log/apache2` or `/var/log/httpd` depending on distribution.
- Audit logs come from libmodsecurity through `SecAuditLog`; rotate connector,
  audit, and server logs with normal production log rotation.
- Validate filter ordering with compression disabled first. Document whether
  your deployment inspects compressed or uncompressed bytes before enabling
  response compression.
- RESPONSE_BODY support remains bounded/non-promoted unless full-body behavior is
  separately proven in live runtime evidence.
