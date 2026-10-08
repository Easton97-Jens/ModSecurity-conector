# Bounded native URI event projection

The NGINX event boundary projects only its URI into a bounded stack buffer,
retains explicit truncation/redaction flags and preserves `?<redacted>` even
when the query begins beyond the maximum safe prefix. Escaped JSON bytes, not
only input characters, determine the limit. All other Common serializer fields
and strict write-error behavior remain unchanged.

Five URI boundary controls and 15 actual request-error producer controls passed
with real Common JSON serialization and C17 warnings as errors. Oversized
non-URI metadata still fails. The materializer explicitly lists the new header.
These compiled controls are not live runtime, canonical or Exact-Head proof;
the fresh source-bound native build and Required case execution are pending.
