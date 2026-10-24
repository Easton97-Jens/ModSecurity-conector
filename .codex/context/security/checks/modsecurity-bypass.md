# ModSecurity and Transformation Bypass Check

Assess whether the bytes/metadata inspected by libmodsecurity match the security-relevant data actually used by the host/upstream/client.

Consider decoding/normalization order, empty and one-byte inputs, embedded NUL, URL/HTML/Unicode transformations, length changes, parser errors, JSON duplicate keys, XML/multipart edge cases, regex/backtracking pressure, chained/negative rules, `ctl` and target/rule removal, request-body error handling, DetectionOnly versus enforcement, body-limit behavior, rule loading, and engine errors.

Keep engine rule execution, match, requested intervention, connector decision, host action, and client-visible outcome separate.
