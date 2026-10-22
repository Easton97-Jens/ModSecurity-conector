# Change Record: CR-20261022-i12-nginx-historical-anchor

**Language:** English | [Deutsch](CR-20261022-i12-nginx-historical-anchor.de.md)

Historical source-storage repair only.

## Identity

| Field | Value |
| --- | --- |
| Change ID | CR-20261022-i12-nginx-historical-anchor |
| Date (UTC) | 2026-10-22 |
| Base revision | `7284aa598adf04c8321163d5e7c5f45e3f1bd649` |

## Motivation and problem statement

The NGINX product update advanced `ngx_http_modsecurity_access.c`. The complete
I12 registry still resolved its historical `3ad4e4d8…` object through the live
repository file, so registry verification failed before any route could stage.

## Acceptance criteria

The object reconstructs the exact 38,520 historical bytes. Its SHA256 identity,
dependent delta and profile hashes remain unchanged, while complete registry and
capture controls pass.

## Implementation decision and rationale

Freeze the authenticated historical source as lossless `text_lines`, following
the existing HAProxy, lighttpd and Traefik anchor pattern. Do not skip complete
registry verification or relabel current product bytes with a historical hash.

## Changed files

`ci/runtime/lifecycle/i12/manifest.json`, the EN/DE I12 capture READMEs, the
`3ad4e4d8…-ngx_http_modsecurity_access.c.lines.json` object, and this EN/DE record.

## Commands executed

`capture_sources.py verify`: PASS (155 objects/10 profiles). The focused capture
suite: PASS (57 tests). Independent reconstruction produced 38,520 bytes with
SHA256 `3ad4e4d801672b0aec1c94326e6e0a2e12e2422e57d1e747121a0bbc2c1b73c8`.
The Traefik current-capture test belongs to PR #413 and is run after integration.

## Security impact

No product, protocol, authentication, authorization or isolation behavior changes.
Strict whole-registry, source-input and delta hashes remain active.

## Runtime evidence

No host was launched; source verification grants no lifecycle qualification.

## Known limitations

Current NGINX and other current product inputs remain subject to their existing
profile and complete-export contracts.

## Remaining risks

The owning route task must still create fresh current-head inputs and runtime evidence.

## Checks not run and rationale

Go/Race/Vet and host checks are outside this storage-only repair and remain in the
owning Traefik acceptance task.

## Final diff and review status

Scoped review confirms that the historical identity, dependent delta, profiles and
capture implementation are unchanged. The Change Record contract and diff check
pass. The full bilingual check reaches only 22 existing missing links into the
uninitialized Framework gitlink; the changed EN/DE pairs and local links match.
The integrated Traefik capture check runs after the normal #410 into #413 merge.
