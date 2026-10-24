# Logging, Evidence, and Data Disclosure Check

Check error/audit/access/event logs, scanner output, temporary files, crash/debug output, evidence JSON/JSONL, and responses for request/response bodies, cookies, authorization data, API keys/tokens, session/request/transaction IDs, private paths, internal hosts/ports, configuration, rule content, prior-request data, and stack/memory disclosure.

Assess log/JSONL injection, CRLF/newline/control sequences, unsafe path creation, symlink/hardlink issues, permissions, rotation races, and cross-request leakage.

Retain sanitized evidence using hashes, lengths, categories, and bounded excerpts rather than sensitive raw payloads.
