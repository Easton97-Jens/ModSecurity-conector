# Change Record: NGINX H1 case request binding

**Language:** English | [Deutsch](CR-20261001-nginx-h1-request-binding.de.md)

## Identity

| Field | Value |
| --- | --- |
| Change ID | `CR-20261001-nginx-h1-request-binding` |
| Date (UTC) | `2026-10-01` |
| Base revision | `75e2a24bcdc3ee97dab0d6f5a0e52e76b0b542c4` |

## Motivation and problem statement

The NGINX legacy case request used Curl without an explicit H1 option or a
guard inside `send_case_request`. Caller selection of an H1 profile alone did
not bind this actual client command, and an inherited `curlrc` could alter it.

## Acceptance criteria

An H1 case request places `-q --http1.1` first in Curl's arguments. Direct
H2/H3 calls to this H1-only function exit `77` before a request. Existing
headers, body, timeout, URL, response/error output validation, and status
handling remain intact. No protocol version or runtime event is synthesized.

## Implementation decision and rationale

The Parent harness checks `NGINX_DOWNSTREAM_PROTOCOL` at the function
boundary and adds `-q --http1.1` before its existing Curl arguments. Curl's
`-q` must be its first option to ignore `curlrc`. The H2/H3 host route already
marks legacy cases non-executable; the local guard prevents accidental direct
reuse. The separate Parent selection/init protocol wiring is another change.

## Changed files

- `connectors/nginx/harness/run_nginx_smoke.sh`
- `tests/test_nginx_h1_request_protocol.py`
- `connectors/nginx/README.md` and `connectors/nginx/README.de.md`
- This English/German Change Record pair and both archive index entries.

## Commands executed

All shell commands used RTK. The command-capture regression first failed for
missing `-q --http1.1` and for both direct H2/H3 calls. After the fix, its two
tests passed. The combined Parent focus run completed 65 tests with exit `0`
(`analysis/parent-canonical-protocol-focus-20261001.log`). `sh -n`,
`shellcheck -S error`, and `git diff --check` passed. A full ShellCheck run on
the preceding audit-pointer base reported warnings at unchanged lines. The
first bilingual check flagged the
German archive link; after correction, `make check-bilingual-docs
check-doc-links` passed with Framework pin
`cc36b37d0f6a0fbc3512f3878a691751e91c5fbb`.

## Security impact

Ignoring `curlrc` prevents a local user configuration from redirecting or
changing this bounded case request. The existing verified output-path checks,
root-master/`nobody`-worker boundary, native event validation, and collector
authority remain unchanged. A custom `CURL` wrapper must accept `-q` and
`--http1.1`.

## Runtime evidence

The isolated diagnostic at
`/var/tmp/codex/ModSecurity-conector/runs/diagnosis/nginx-transaction_id_generated_or_fallback-oQ6cvxLb`
made a real request with HTTP `200`. Its actual audit request line recorded
`HTTP/1.1`; the role record observed master UID `0` and worker UID `65534`
with worker replacement after reload. The native event carried rule `1100502`.
The unchanged official Parent collector marked this single source case PASS,
but its one-case aggregate remained `FAIL` because other required cases were
not run. This diagnostic is not canonical or exact-head lifecycle PASS.

## Known limitations

The H2/H3 legacy case route still produces no promoted case request. The
remaining 54 required H1 cases still need genuine runner and request coverage.
This record does not include the separate selection/init protocol change.

## Remaining risks

The command test proves requested Curl options, not the negotiated HTTP
version for every future run. Custom `CURL` wrappers lacking these options
will fail. A complete exact-head lifecycle is still required for PASS.

## Checks not run and rationale

No new full E2E, canonical PASS, or SHA256SUMS is claimed while required runner
coverage remains red. No remote CI, push, PR mutation, merge, Framework/MRTS
source or Gitlink change is part of this H1 correction.

## Final diff and review status

The H1 source diff is limited to `send_case_request`; this record documents
the local successor to the audit-pointer base. Review and
delivery of the combined Parent changes remain with the coordinating task.
