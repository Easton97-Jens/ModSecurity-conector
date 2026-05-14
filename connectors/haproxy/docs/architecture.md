# HAProxy Architecture

Status: unknown

Official HAProxy SPOE documentation describes a filter that communicates with an
external SPOA service over SPOP. This may be a candidate architecture, but this
repo does not yet prove that it can support all libmodsecurity v3 phases.

Known candidate paths:

- SPOE/SPOA service.
- Lua extension.
- Native HAProxy filter.

No path is selected yet.
