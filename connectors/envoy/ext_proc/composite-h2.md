# Composite response policy

**Language:** English | [Deutsch](composite-h2.de.md)

The shared `msconnector_composite` service accepts
`--late-action-policy off|safe|strict` (default `safe`). Strict is admitted only
by a native engine whose parsed Common runtime uses `phase4_mode=strict`;
the inverse strict/safe mismatch is also rejected before a listener starts.

This policy applies independently to the complete Envoy ext_authz plus
response-companion and Traefik ForwardAuth plus response-companion paths.
It does not supply a response path to an unpaired authorization protocol.
Safe retains the committed response. Strict sends Envoy's late native local
reply or Traefik's `http.ErrAbortHandler` sentinel after releasing the retained
transaction. Small inspected Traefik chunks are flushed before upstream EOS.

The lifecycle record `host_action_request` describes the requested late host
operation. It does not claim a Common-confirmed downstream reset. Real H2
frames and independent host access records must prove the abort and isolation
of simultaneously active streams. The coordinator emits a bounded SHA256 of
method, NUL and URI for independent request/retained-transaction correlation;
it never emits the lease or response body.

An actual companion protocol close without EOS is finalized with Common's
typed protocol terminal. It does not fabricate EOS or attribute the cause to
a client or upstream. Unknown close reasons retain the existing native phase
sequence guard. The shared CGo engine retains its `envoy`/`ext_proc` backend
identity; native host and coordinator handoff evidence identify each complete
logical profile separately.
