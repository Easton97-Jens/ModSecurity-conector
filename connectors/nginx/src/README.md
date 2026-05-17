# NGINX Source

Status: adapter-owned NGINX connector source

NGINX-specific adapter source belongs here. The monorepo-default NGINX smoke
build materializes this tree under `$BUILD_ROOT/nginx-build/connector-src` and
builds the NGINX dynamic module from that generated copy.

Current files include:

- the NGINX module `config` file;
- NGINX connector module sources derived from ModSecurity-nginx base commit
  `9eb44fd9ab0988756e1ab8ce5aa5548ddbe57846`;
- selected ModSecurity-nginx PR #377 source changes at
  `3d72b004ff27a78ea19c6b945870e2cae62a97ac` for phase-4 / late intervention
  handling;
- the repo-owned `ddebug.h` compatibility header;
- adapter metadata helpers used by report and drift checks;
- `SOURCE_MAP.json`, which records base and PR provenance per file.

This migration does not promote `RESPONSE_BODY` to a verified variable. Phase-4
and response-body blocking remain xfail/mapped-only until separate real-world
Apache and NGINX evidence proves stable HTTP behavior.
