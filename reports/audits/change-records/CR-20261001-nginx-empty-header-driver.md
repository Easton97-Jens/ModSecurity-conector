# Change Record: NGINX present empty-header driver

**Language:** English | [Deutsch](CR-20261001-nginx-empty-header-driver.de.md)

## Identity

| Field | Value |
| --- | --- |
| Change ID | `CR-20261001-nginx-empty-header-driver` |
| Date (UTC) | `2026-10-01` |
| Base revision | `e9d022ed16d9df469baa9b12070786468706ced7` |

## Motivation and problem statement

The host request driver passed generated `Header: ` directly to Curl. Curl
suppresses that header instead of sending a present empty value, so the
selected required empty-header scenario could not receive its real stimulus.

## Acceptance criteria

A real loopback request observes one present empty header. Absent headers
stay absent; nonempty colon-bearing and duplicate headers are preserved.
H1 forcing, body/output controls and containment remain intact.

## Implementation decision and rationale

At the Curl boundary only, convert empty or one-space values after the first
colon into `Header;`. Keep the Framework header-file format unchanged. No
fixture-specific special case, new result writer, event producer, C/Common
change or automatic commit of prepared protocol wiring is included.

## Security impact

The actual stimulus matches the fixture instead of producing a false absence.
Drivers emit no native/canonical events. Root/nobody ownership, verified paths,
native evidence validation and payload/privacy controls are unchanged.

## Changed files

- `connectors/nginx/harness/run_nginx_smoke.sh`
- `tests/test_nginx_empty_header_driver.py`
- `connectors/nginx/README.md` / `.de.md`
- This EN/DE Change Record and archive index pair

The companion Framework runner/catalog change has separate repository
ownership and delivery. Parent Framework/MRTS gitlinks remain unchanged.

## Commands executed

All commands used RTK. Three real loopback controls first yielded one expected
failure: the empty header was absent. After the driver fix all three pass;
the combined H1 command regression passes five tests. The corrected broad
Parent focus run passes 103 tests (exit0), including runtime-path resolver,
security, lifecycle/projection and native-sink checks, at the unchanged old
physical Framework pin. `sh -n`, `shellcheck -S error`, `git diff --check` and
`make check-bilingual-docs check-doc-links` pass. Initial guessed module names
and record headings failed and were corrected; their failed logs are not
counted as passes. Full ShellCheck retains pre-existing warnings at unchanged
lines; no warning control was removed or suppressed.

## Runtime evidence

One isolated network-namespace probe reused the retained C build without
downloads: `nginx-empty_header_value-MKUpI7qd`. The task harness and external
Framework fixture observed HTTP 200, native phase-1 rule 1100503, master UID 0,
worker UID/GID 65534 and replacement worker after reload. The port cleanup
probe reported freed. The unchanged official collector saw the native event;
unchanged Framework normalization accepted the individual source case.
The one-case source aggregate is FAIL because other required scenarios were
not executed. This is diagnostic evidence, not new exact-head canonical PASS.

The isolated nonempty-header control `nginx-empty_header_value-pvB0el3W`
returned HTTP200 but harness exit1/source-case FAIL, with no target rule or
native event. Both attempts freed their ports. The unchanged canonical
normalizer and individual PASS completeness check accept only the positive
case. The unchanged coverage diagnostic reports 53 missing paths after 54;
selection remains 97. These are local path counts, not fresh full-E2E coverage.

## Checks not run and rationale

No full E2E, gitlink update, remote CI, push, PR mutation or merge. Required
coverage remains red, so no full canonical PASS or E2E SHA256SUMS is claimed.

## Known limitations

The Framework requires both header presence and empty value for rule 1100503;
HTTP 200 alone is not proof. One of the original 54 missing paths has a local
real trigger; the other paths need separate drivers/evidence.

## Remaining risks

Custom Curl wrappers must preserve `Header;` semantics. A full lifecycle on a
new exact head remains necessary; the retained build is diagnostic only.

## Final diff and review status

An independent read-only review found no blocker in this bounded driver,
fixture and negative controls. The scoped diff/whitespace review preserves
the two prepared uncommitted protocol files outside this slice. The separate
Parent commit is local only; no remote or gitlink action is included. Final
documentation checks are rerun before commit. No secrets or unrelated edits
are included.
