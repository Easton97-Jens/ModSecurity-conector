# Envoy Architecture

Status: unknown

Official Envoy documentation describes HTTP filters with decoder, encoder, and
decoder/encoder behavior. Candidate approaches include:

- Native C++ HTTP filter.
- External authorization service.
- Lua HTTP filter.
- Wasm HTTP filter.

No approach is selected yet. Filter ordering and route-cache behavior must be
documented before implementation.
