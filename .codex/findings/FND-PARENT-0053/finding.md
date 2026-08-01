# FND-PARENT-0053 — Exact #74 runtime producer is blocked at Apache HTTPD preparation

## Identity

| Field | Value |
| --- | --- |
| ID | FND-PARENT-0053 |
| Category | ci_failure |
| Repository / ownership | parent / parent |
| Priority / severity / confidence | P1 / not_applicable / confirmed |
| Status / feasibility | fixed / feasible_now |
| Release blocker / security relevant | true / true |
| Affected delivery | Parent PR #74 at exact head `d93446a1b53be344f5599c48272060e2c664ae86` |
| MRTS impact | none; MRTS remains read-only |

## Observation and impact

Both exact-head `verified-report-governance` runs fail closed in the required
runtime producer at `prepare-runtime-components: FAILED apache_httpd:
missing_local_httpd_build`. Their readiness, matrix, report, lint, and
terminal-gate consumers cannot run successfully after that producer failure.

The observed classification proves a Parent-owned Apache-runtime preparation
blocker, not an Apache source-root cause, integrity bypass, secret exposure,
or successful hostile input. Parent PR #74 must not be integrated while the
fresh strict/full producer remains failed.

## Scope and constraints

The currently observed path is Parent CI/runtime orchestration and the Parent
Apache component preparation route. Framework source, the Parent/Framework
gitlink, and MRTS source are outside this finding's remediation scope. The
strict producer and terminal evidence gate must remain fail-closed.

## Evidence and limitation

The retained exact-head artifact records both GitHub run/job identifiers and
the reported classifier. Its outer producer log does not contain the internal
Apache source-build error, so selecting a package, configuration, source, or
code remediation now would be speculative. Follow-up `d93446a` has been
locally validated and normally published; it exposes only the current-run
preparation log and the fixed Apache build log through regular-file,
non-symlink, 300-line, command-shielded paths. Its fresh hosted result remains
required before that diagnostic or any Apache remedy is accepted.

## Acceptance criteria

1. A fresh exact-head failure diagnostic exposes only the fixed, task-owned
   Apache build log through a bounded, command-shielded path.
2. The underlying Apache preparation error is reproduced and classified from
   that evidence.
3. The smallest Parent-owned correction preserves cache/path containment,
   source provenance, and strict producer behavior.
4. Focused local tests and a fresh exact-head strict/full producer plus its
   terminal evidence gate pass before this finding is closed.

## Validation plan

- Inspect the fresh exact-head hosted result of published `d93446a` and classify the inner Apache
  failure without weakening the producer or gate.
- Implement and test only the evidenced Parent remedy, then repeat exact-head
  CI, SonarCloud, review/thread, and protected-integration checks.

## Evidence

- Artifact: `.codex/runs/20260726T073000Z-pr74-apache-runtime-blocker/evidence/exact-head-ci-failure.md`
- Run IDs: `30192356697`, `30192358331`
- Exact head: `28a4a1af5e764860d27ecb670bd82283e7b1aa74`
- Published follow-up: `d93446a1b53be344f5599c48272060e2c664ae86`
- Local follow-up controls: 19 workflow-security tests,
  `make check-ci-security-contract`, `make check-bilingual-docs`, and
  `git diff --check` passed; these are not hosted runtime evidence.

## Residual risk

No runtime evidence or merge assurance is accepted from the failed producer.
The strict terminal gate remains intact; no risk acceptance is recorded.

## History

- 2026-07-26 — Created from two terminal exact-head #74 hosted failures. The
  bounded outer diagnostic identified `missing_local_httpd_build`, but the
  inner Apache source-build cause remains pending fresh bounded evidence.
- 2026-07-26 — Published `d93446a` with a two-path, command-shielded,
  regular-file-only diagnostic. The new exact-head producer run is pending;
  neither the finding nor the delivery is closed by static/local controls.

## Root-cause update and current remediation (2026-07-26)

The fresh hosted run of `d93446a1b53be344f5599c48272060e2c664ae86` reached
the bounded diagnostic. Run `30193495484`, job `89770795068`, emitted the
inner cause:

```text
apache_poc: blocked missing required SHA256 digest for pcre2
```

Parent's unconditional `export PCRE2_SHA256` turned its absent value into an
explicit empty environment override. Framework deliberately distinguishes an
unset value (which receives its reviewed default pin) from an explicit empty
value (which fails closed). The no-write Make reproduction recorded in
`.codex/runs/20260726T083803Z-pr74-pcre2-digest-remediation/evidence/exact-head-pcre2-digest-blocker.md`
observed `PCRE2_SHA256=<>`; the artifact SHA-256 is
`f226e3d727c384c55abc80cea24aec506341e831d52c9e695892ecad617e29a5`.

The same source review confirmed a Parent cache-integrity gap: before the
Framework's extraction-time verifier, `prepare_archive` could accept an empty
PCRE2 digest, use its checksum URL as fallback, download and parse archive
content, and mark a cache entry complete. The Framework still prevented a
demonstrated extraction bypass, but Parent must not process or publish that
unverified cache state.

The active Parent-only correction is therefore to export `PCRE2_SHA256` only
when GNU Make reports an actual caller-provided value, and to require a
literal 64-hex PCRE2 digest before Parent creates archive/cache state. A valid
digest is normalized to lowercase; empty, whitespace-only, malformed, and
mismatching inputs are rejected. `PCRE2_SHA256_URL` cannot repair a missing
literal PCRE2 digest. Framework remains the single default-pin authority and
its extraction verifier is unchanged.

The updated acceptance criteria are: (1) absent, explicit-empty, and valid
caller values retain those exact Make-boundary semantics; (2) invalid PCRE2
input reaches no Parent download, parser, checksum-URL fallback, or cache
publication; (3) matching input remains a `checksum_status` `PASS`
legitimate control and mismatching input leaves no complete marker; (4) the
focused Parent Make, cache-contract, cache-identity, CI-security, component,
documentation, and diff checks pass; and (5) a fresh hosted exact-head
strict/full producer plus terminal evidence gate passes before this finding is
verified or PR #74 is integrated.

The only remaining finding-level blocker is that fresh hosted exact-head
producer and terminal-gate evidence after normal Parent-branch publication.
Related records are `FND-CROSS-0001`, `FND-PARENT-0052`,
`FND-FRAMEWORK-0005`, and the separate Framework fixture regression
`FND-FRAMEWORK-0056`. No failing runtime output is accepted as evidence and no
risk is accepted.
