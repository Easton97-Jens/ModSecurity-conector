# Request/Response Desynchronization Check

Assess protocol/framing ambiguity only where the selected host/profile supports the relevant transport and backend path.

Consider CL.TE, TE.CL, conflicting Content-Length, duplicate/malformed Transfer-Encoding, chunk framing errors, trailers, data after message end, HTTP/2 or HTTP/3 translation to HTTP/1, pseudo-header/Host conflicts, upgrade/WebSocket boundaries, keepalive/reuse after parser error, retry behavior, and queue poisoning.

Correlate the host-parsed request, connector transaction, libmodsecurity input, upstream request count/bytes, backend processing, client-visible result, and connection reuse. HTTP status alone is insufficient.

Do not claim transport coverage for unexecuted H2/H3 paths.
