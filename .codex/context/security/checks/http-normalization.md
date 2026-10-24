# HTTP Representation and Normalization Check

Compare the security-relevant representation at every applicable boundary: wire request/response, host parser, router/location selection, connector mapping, Common/libmodsecurity input, upstream/backend representation, and evidence/log representation.

Assess applicable cases such as raw versus decoded paths, percent-encoding and double-encoding, dot segments, encoded slash/backslash, duplicate separators, query duplicates/order, invalid UTF-8, control characters, NUL handling, Host/authority differences, duplicate headers, forwarded headers, body content types, partial/truncated bodies, and transformations before/after security evaluation.

A differential matters when it changes routing, rule matching, identity, body limits, host action, upstream data, or evidence meaning.

Record for each high-risk differential: source representation, transformed representation, component responsible, security control, downstream representation, observed/expected consequence, legitimate control, and remaining uncertainty.
