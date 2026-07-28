# Change Record: Parent Traefik start-smoke diagnostic-literal cleanup for SonarQube Cloud S1192

**Language:** English | [Deutsch](CR-20260728-sonar-traefik-start-smoke-literal.de.md)

## Identity

| Field | Value |
| --- | --- |
| Change ID | CR-20260728-sonar-traefik-start-smoke-literal |
| Date (UTC) | 2026-07-28 |
| Base revision | 8e8acb8dab1cd03723de269cab7da7dd62e5e010 |
| Boundary | Parent Traefik start-smoke runner and its direct static wiring checker, plus this English/German Change Record pair and indexes only. Framework, MRTS, both gitlinks, workflow, scanner policy, and generated reports remain unchanged. |
| Finding linkage | SonarQube Cloud item AZ9Mwiwj-bUaKQ_zSGA2, rule shelldre:S1192, reports the diagnostic 1,160p literal four times in connectors/traefik/scripts/start-smoke.sh. This local candidate does not itself close the external item before a fresh exact-head analysis. |

## Motivation and problem statement

The Traefik process-only start smoke used the immutable diagnostic sed program
1,160p in four separate failure branches. The repeated literal is the scoped
SonarQube Cloud maintainability issue; retaining four independently editable
copies would make a future diagnostic-range change easier to apply
inconsistently.

The runner manages paths, subprocesses, liveness checks, and cleanup. The
change must therefore centralize only the fixed diagnostic program and keep
every branch predicate, stderr operand, error message, exit status, trap, and
cleanup behavior unchanged.

## Acceptance criteria

- connectors/traefik/scripts/start-smoke.sh contains exactly one
  unconditional, non-exported TRAEFIK_DIAGNOSTIC_SED_RANGE='1,160p'
  declaration after the cleanup trap and before the first diagnostic use.
- The four existing failure diagnostics use the quoted declaration with their
  unchanged quoted operands: "$CONFIG_STDERR", "$SERVICE_STDERR", and
  "$TRAEFIK_STDERR" twice.
- The direct static wiring checker rejects an exported, duplicated, legacy, or
  incorrectly ordered range and pins the affected error-branch controls.
- Shell syntax, the focused start-wiring check, and scoped whitespace checking
  have passed; the known ShellCheck baseline is not represented as a clean
  result.
- No Traefik host runtime, commit, push, pull request, hosted analysis,
  Ready-for-review transition, merge, master update, Framework/MRTS action, or
  scanner-policy change is claimed.

## Implementation decision and rationale

The selected declaration is an unconditional shell assignment rather than a
defaulted or inherited environment value. It is intentionally not exported,
so an invoker cannot choose the sed program and child-process environments
are not changed. Each of the four existing sed -n calls now passes the same
fixed value and its existing stderr file as distinct quoted arguments.

The direct source contract checks one declaration, four direct uses, absence
of the legacy literal call, the unchanged per-branch operands, and the
existing lifecycle guards. It does not change the separate template-rewrite
sed -e command, start-root validation, loopback checks, process launches,
wait/exit ordering, traps, or cleanup.

## Retained diagnostic calls

| Failure branch | Retained diagnostic command |
| --- | --- |
| Config check | sed -n "$TRAEFIK_DIAGNOSTIC_SED_RANGE" "$CONFIG_STDERR" >&2 |
| Service liveness | sed -n "$TRAEFIK_DIAGNOSTIC_SED_RANGE" "$SERVICE_STDERR" >&2 |
| Traefik liveness | sed -n "$TRAEFIK_DIAGNOSTIC_SED_RANGE" "$TRAEFIK_STDERR" >&2 |
| Nonempty Traefik stderr | sed -n "$TRAEFIK_DIAGNOSTIC_SED_RANGE" "$TRAEFIK_STDERR" >&2 |

## Changed files

- connectors/traefik/scripts/start-smoke.sh
- ci/checks/connectors/all/check-remaining-connectors-start-wiring.py
- reports/audits/change-records/README.md and README.de.md
- this English/German Change Record pair

## Commands executed

| Command or control | Result |
| --- | --- |
| sh -n connectors/traefik/scripts/start-smoke.sh | passed; syntax-only validation without starting a host process. |
| make check-remaining-connectors-start-wiring | passed; the focused static contract reported remaining connectors start wiring: ok. |
| Scoped git diff --check for the runner and direct static checker | passed. |
| ShellCheck of the target runner | did not pass as a clean check: it reported only three unchanged SC1007 diagnostics on lines 4–6. This record does not treat that baseline as a passing result. |
| Scoped English/German Change Record and index structure, technical-literal, reciprocal-link, and trailing-whitespace inspection | passed. |

## Security impact

This is a code-quality remediation, not a validated security finding. The
focused shell/process/path review classified the fixed-literal condition as
already_safe: no environment, request, response, log, path, process, or
configuration value controls the sed program. The unconditional local
assignment overwrites any inherited value, remains unexported, and the four
stderr operands remain quoted.

The remediation preserves set -eu, start-root and loopback guards, quoted
diagnostic paths, kill -0 and wait ordering, trap cleanup EXIT HUP INT TERM,
the original error branches, and their exits. No security control is weakened.

## Runtime evidence

No real Traefik, connector, Common/libmodsecurity, or host runtime was run.
The passed syntax and direct static wiring checks are source-contract evidence
only; they do not demonstrate a host-runtime capability.

## Checks not run and rationale

- The real Traefik start smoke is a deliberate non-goal for this literal-only
  change and remains not_run.
- Repository-wide bilingual-documentation and link checks are not run in this
  agent scope. The candidate worktree has an empty Parent-pinned Framework
  gitlink, so root will run those checks in a disposable exact-revision overlay
  rather than treating this local prerequisite as a product failure.
- Exact-PR-head GitHub checks and SonarQube Cloud analysis require a normal
  task-owned Draft PR delivery cycle and do not yet exist.

## Known limitations

The direct checker is intentionally static. It proves the literal ownership,
quoted diagnostic operands, and retained branch controls, but it does not
start a service or validate a complete Traefik deployment. ShellCheck retains
the three pre-existing SC1007 diagnostics noted above.

## Remaining risks

This candidate does not prove behavior under a real host, plugin, or
Common/libmodsecurity installation. Existing broader trust assumptions around
the process environment and diagnostic-log content are outside this
literal-only SonarQube Cloud remediation and were not broadened by it.

## Final diff and review status

This record is written before staging, commit, push, pull-request creation,
and hosted analysis. The recorded local source validation and focused security
review are positive within their stated scopes. No global duplicate-lines
reduction or external issue closure is claimed until a fresh SonarQube Cloud
analysis observes the final exact PR head.
