# Build - Connector Template

**Language:** English | [Deutsch](build.de.md)

## Purpose

This document records the build evidence a concrete connector must provide.
The template itself does not contain build commands for a not-yet-implemented
connector.

## Build checklist

- [ ] Build command documented.
- [ ] Include paths documented.
- [ ] Library paths documented.
- [ ] Build artifacts documented.
- [ ] Build log path documented.
- [ ] Clean/refresh behavior documented.
- [ ] External dependency versions or pins documented.
- [ ] Build output location under `BUILD_ROOT` documented.
- [ ] Compiler/linker failures documented without guessing.

## Required fields for a concrete connector

```text
Connector:
Source path:
Build command:
Environment:
Include paths:
Library paths:
Artifacts:
Build log:
Exit code:
```

## Makefile integration checklist

- [ ] `smoke-<name>` target found or added with evidence.
- [ ] Optional `build-<name>` or `check-<name>` target documented, if present.
- [ ] Required environment variables documented.
- [ ] Artifacts remain below the documented build root.
- [ ] No global source tree is deleted or overwritten by the build flow.

## Evidence rules

- A build claim requires the exact command, exit code, artifact path, and log
  path.
- A copied build recipe from Apache or NGINX must be reviewed against the new
  server's build system.
- Include/library paths must be found in the build command, generated Makefile,
  or build log.
- If a dependency path is not found, document `Nicht im Repository gefunden`.

## Not included

This template intentionally does not provide concrete build commands, compiler
flags, server SDK assumptions, or generated artifacts for a future connector.
