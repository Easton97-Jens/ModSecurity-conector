# Change Record: Correct the German HAProxy compiler-guide path label

**Language:** English | [Deutsch](CR-20260714-haproxy-guide-path-label.de.md)

## Identity

| Field | Value |
| --- | --- |
| Title | Correct the German HAProxy compiler-guide path label |
| Change ID | CR-20260714-haproxy-guide-path-label |
| Date (UTC) | 2026-07-14T14:44:03Z |
| Author or executing agent | Codex |
| Base revision | be0356af96ef582c3a7dbc0169c7c8b27b7b6b34 |
| Related issue or pull request | None at record creation; the authorized draft PR is created only after the initial commit. |
| Final revision | not committed |

## Motivation and problem statement

The German HAProxy connector README displayed
`docs/build/compilers/haproxy.md` while its Markdown destination already
correctly targeted `../../docs/build/compilers/haproxy.de.md`. Both compiler
guides exist, and the English companion consistently displays and targets its
English guide. The mismatch made the visible German path misleading even
though the click destination was correct.

## Affected components and security boundaries

The scope is one visible Markdown label in
`connectors/haproxy/README.de.md`, the paired Change Record, and its paired
index entries. It changes documentation routing only: no connector source,
build configuration, request processing, trust boundary, or security behavior
changes. The Framework worktree and Parent submodule Gitlink are excluded.
Ignored local Codex governance files are intentionally outside the versioned
diff.

## Acceptance criteria

| Criterion | Status | Evidence |
| --- | --- | --- |
| The displayed German compiler-guide path is `docs/build/compilers/haproxy.de.md` and matches its existing Markdown destination. | met | Source review, `make check-bilingual-docs`, and `make check-doc-links` |
| The correct English companion path and destination remain unchanged. | met | Scoped diff review |
| The versioned scope contains only this correction, the EN/DE Change Record pair, and the paired Change-Record index entries. | met | Cached name-status, stat, check, and full-diff review |
| The delivery smoke remains documentation-only and makes no runtime, release, or production-readiness claim. | met before delivery | This record's bounded scope and final delivery review |

## Alternatives investigated

Changing the German destination to the English guide was rejected because the
German guide already exists and the existing destination is correct. Changing
the English README was rejected because its visible path and destination are
already consistent. A broader HAProxy documentation rewrite was excluded as
unrelated to this one-label discrepancy.

## Implementation decision and rationale

Change only the German visible link label from `haproxy.md` to
`haproxy.de.md`; retain the existing German destination. This makes the text a
reader sees agree with the file a reader opens while preserving all build and
runtime documentation content.

## Changed files

- `connectors/haproxy/README.de.md`
- `reports/audits/change-records/CR-20260714-haproxy-guide-path-label.md`
- `reports/audits/change-records/CR-20260714-haproxy-guide-path-label.de.md`
- `reports/audits/change-records/README.md`
- `reports/audits/change-records/README.de.md`

Local `AGENTS.md` and `.codex/` governance additions are ignored and are not
part of this versioned diff.

## Tests added or changed

None. This is a documentation-label correction; existing documentation checks
are the appropriate verification.

## Commands executed

| Exact command | Exit code or result | Sanitized relevant summary | Canonical evidence path | Run ID |
| --- | --- | --- | --- | --- |
| `rtk git blame -L 81,81 -- connectors/haproxy/README.de.md` | `0` | The mismatched visible label was traced to the current tracked line. | None | None |
| `rtk ls -l docs/build/compilers/haproxy.md docs/build/compilers/haproxy.de.md` | `0` | Both English and German compiler-guide files exist. | None | None |
| `rtk make check-bilingual-docs` | `0` | The bilingual documentation check passed. | None | None |
| `rtk make check-doc-links` | `0` | Repository path references and Framework documentation links passed. | None | None |
| `rtk git diff --check` | `0` | No whitespace errors were found in the tracked worktree diff. | None | None |
| `rtk git diff --cached --name-status` | `0` | Exactly five scoped documentation and Change-Record paths were staged. | None | None |
| `rtk git diff --cached --stat` | `0` | The staged change is limited to the expected five files. | None | None |
| `rtk git diff --cached --check` | `0` | No whitespace errors were found in the staged diff. | None | None |
| `rtk proxy git diff --cached` | `0` | Full staged-diff review found only the intended link-label correction and paired records/indexes. | None | None |

## Security impact

No security behavior, validation, default, logging format, or trust boundary
changes. Correcting the visible documentation path reduces reader confusion
only; it does not establish a security property.

## Documentation changes

`connectors/haproxy/README.de.md` now displays its existing German compiler
guide destination accurately. The paired Change Record and paired index rows
record the bounded correction. The English HAProxy README was reviewed and is
unchanged because it is already correct.

## Runtime evidence

No runtime evidence was collected or claimed for this change. Documentation
checks, a commit, a draft PR, and CI are not HAProxy runtime evidence.

## Known limitations

This change corrects one visible path label only. It does not test, rebuild, or
change HAProxy, its SPOA/SPOP integration, compiler requirements, or the
underlying guides.

## Remaining risks

Future moves or renames of the compiler guide must update both the visible
label and its Markdown destination together. The scoped documentation checks
reduce, but cannot eliminate, future documentation drift.

## Checks not run and rationale

HAProxy build, configuration, H1/H2/H3, CRS/MRTS, hardening, sanitizer, static
analysis, smoke, and lifecycle checks are not applicable to a documentation
label correction and would not provide relevant runtime evidence. There is no
standalone `make check-repository-path-references` target; the existing path
checker ran within `make check-doc-links` and passed. `make lint` and
`make quick-check` are not run because their broader
build and framework scope is not proportionate to this one-label change.

## Final diff and review status

The local bilingual, link/path-reference, and whitespace checks passed. The
five staged paths and their full cached diff were manually reviewed, and
`git diff --cached --check` passed. Commit, push, draft PR, and exact-final-SHA
CI verification remain pending. This delivery smoke is not a release approval
and must remain unmerged with auto-merge disabled.
