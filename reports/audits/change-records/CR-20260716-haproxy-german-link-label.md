# Change Record: German HAProxy compiler-guide link label

**Language:** English | [Deutsch](CR-20260716-haproxy-german-link-label.de.md)

## Identity

| Field | Value |
| --- | --- |
| Change ID | `CR-20260716-haproxy-german-link-label` |
| Date (UTC) | `2026-07-16` |
| Base revision | `c8450a9feaef3da9c999586ea60398653601f037` |
| Boundary | Parent repository only; Framework and MRTS unchanged. |

## Motivation and problem statement

`connectors/haproxy/README.de.md` displayed `docs/build/compilers/haproxy.md`
while its existing Markdown destination was the German companion
`../../docs/build/compilers/haproxy.de.md`. The visible label should identify
the actual German guide.

## Acceptance criteria

- The visible German link label is `docs/build/compilers/haproxy.de.md`.
- The existing destination remains `../../docs/build/compilers/haproxy.de.md`.
- No HAProxy source, runtime behavior, Framework content, MRTS content, or
  gitlink changes are included.

## Implementation decision and rationale

Change only the reader-visible label in the German HAProxy README. The English
companion is already internally consistent and is intentionally unchanged.
This concise Change Record pair records only this replacement PR's actual
scope; it does not reproduce historical PR records.

## Changed files

- `connectors/haproxy/README.de.md`
- `reports/audits/change-records/CR-20260716-haproxy-german-link-label.md`
- `reports/audits/change-records/CR-20260716-haproxy-german-link-label.de.md`

## Commands executed

| Command | Result |
| --- | --- |
| `PYTHONDONTWRITEBYTECODE=1 make check-bilingual-docs` | failed only on pre-existing missing audit/architecture index targets outside this replacement scope; this Change Record pair has no language-switch or Change Record error. |
| `PYTHONDONTWRITEBYTECODE=1 make check-doc-links` | failed only on the same pre-existing missing targets outside this replacement scope. |
| Focused `check_change_record_pair` invocation and HAProxy-label assertion | passed. |
| `git diff --check` | passed. |

No runtime command was executed or claimed.

## Security impact

No security control, trust boundary, dependency, credential, logging behavior,
or executable configuration changes. This correction reduces the risk of a
reader selecting the English guide by mistake.

## Runtime evidence

Not applicable. This change does not alter HAProxy code, configuration, build
inputs, or runtime behavior.

## Known limitations

The correction validates the repository documentation path only. It does not
build or exercise HAProxy, SPOA/SPOP, HTTP/1.1, HTTP/2, HTTP/3, CRS, or MRTS.

## Remaining risks

The guide's content is not revalidated by this label-only change. Normal link
and bilingual-documentation checks are the evidence boundary.

## Checks not run and rationale

HAProxy build/configuration, runtime, protocol, sanitizer, static-analysis,
and CRS/MRTS checks are not applicable to a visible Markdown-label correction.
Broader `make lint` is disproportionate and is not documentation evidence.

## Final diff and review status

Pending focused local checks, exact-SHA replacement-PR verification, and final
scoped-diff review. This record does not claim legacy PR checks as replacement
PR evidence.
