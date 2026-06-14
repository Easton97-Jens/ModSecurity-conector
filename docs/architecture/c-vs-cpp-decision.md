# C vs C++ Decision

Status: accepted for the current connector refactor phases.

## Decision

The public common connector API remains C-first.

The repository may provide thin C++ header wrappers over C structs and may use
C++ for build tools, test tools, or optional helper programs. Productive
Apache, NGINX, and future server connector cores must not be ported to C++ as
part of the common refactor.

## Rationale

- libmodsecurity v3 is integrated here through its public C API.
- The imported Apache connector is C-oriented and built through APXS/Autotools.
- NGINX modules are C modules and cross server ABI boundaries directly.
- C++ would add ABI and linker complexity to server-module loading paths.
- The HAProxy SPOA/SPOP runtime path and future Lighttpd integrations are
  expected to stay close to C.

## Allowed C++ Use

- Thin `.hpp` aliases around C structs.
- Build and test utilities.
- Optional helper programs that do not cross server module ABI boundaries.

## Disallowed C++ Use

- Porting productive Apache or NGINX connector code to C++.
- Passing C++ objects across Apache, NGINX, or future server ABI boundaries.
- Hiding libmodsecurity transaction ownership behind undocumented C++ lifetime
  rules.
- Replacing C-first common headers with a C++-only adapter API.

## Current Mapping

The current harnesses are shell/Python. They do not use FFI to instantiate the
C structs directly. Instead, they write JSON fields that intentionally mirror
the C-first common data shapes:

- `msconnector_status` -> `operation_status` and `status_model`
- `msconnector_origin` -> connector `origin`
- `msconnector_intervention` -> per-case `intervention`

This keeps the evidence layer portable while preserving the C-first public API
for future compiled adapters.
