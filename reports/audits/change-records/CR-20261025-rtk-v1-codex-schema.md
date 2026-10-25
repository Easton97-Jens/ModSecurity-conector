# Change Record: CR-20261025-rtk-v1-codex-schema

**Language:** English | [Deutsch](CR-20261025-rtk-v1-codex-schema.de.md)

## Identity

| Field | Value |
| --- | --- |
| Change ID | CR-20261025-rtk-v1-codex-schema |
| Date (UTC) | 2026-10-25 |
| Base revision | `42fd5a8e895aca3a36b09eb09fe5c7cf9c3399e3` |

## Motivation and problem statement

The Parent required RTK execution in its local policy but had no versioned native Codex hook registration. This change adopts the Codex hook schema supported by RTK v1.0.1 and documents the v1 command naming. Existing `rtk make` commands remain valid; historical `rtk proxy` evidence is preserved as executed.

## Acceptance criteria

- The project hook configuration matches `rtk init --codex` from RTK v1.0.1.
- Supported Git and Make commands rewrite through `updatedInput`; other input fields survive, and already wrapped or unsupported inputs are not rewritten.
- Unfiltered execution uses `rtk bypass` and preserves stdout, stderr, and the child exit code.
- The structure validator checks exactly one native RTK handler while allowing independent hooks. The changed policy digest is current, and unrelated baseline findings remain visible.

## Implementation decision and rationale

Register `rtk hook codex` under `hooks.PreToolUse` with matcher `Bash`. Keep execution instructions in the existing policy instead of generating another `RTK.md` or modifying `AGENTS.md`. Document host-local project/hook trust, explicit RTK execution when interception is unavailable, and `bypass` as the current name of the deprecated `proxy` alias. No custom filters, pipeline, or provider-API proxy are needed.

References: [RTK v1.0.1 Codex integration](https://github.com/rtk-ai/rtk/blob/v1.0.1/hooks/codex/README.md), [v1.0.0 migration](https://github.com/rtk-ai/rtk/releases/tag/v1.0.0), and [Codex hooks](https://developers.openai.com/codex/hooks).

## Changed files

- `.codex/hooks.json`: native project hook registration.
- `.codex/context/command-execution-policy.md`: current schema, invocation, trust, and fallback guidance.
- `.codex/bin/validate-v32-structure.py`: minimal JSON validation of the RTK registration, preserving other hooks.
- `.codex/inheritance-manifest.toml`: update only the `COMMAND-EXECUTION` digest.
- `reports/audits/change-records/CR-20261025-rtk-v1-codex-schema.md` and `reports/audits/change-records/CR-20261025-rtk-v1-codex-schema.de.md`: equivalent English/German records.

## Commands executed

Checks ran from the Parent checkout with the absolute task-local RTK v1.0.1 executable. In the command payloads below, `rtk` denotes that executable; `RTK_DB_PATH` selected a task-local database, with `PYTHONNOUSERSITE=1` and `PYTHONDONTWRITEBYTECODE=1`.

| Command or procedure | Actual result |
| --- | --- |
| `rtk bypass python3 -` with an inline acceptance-check heredoc | PASS: all nine checks listed below |
| `rtk init --codex` in an isolated fixture, invoked by that harness | PASS: generated hook configuration equals the versioned JSON |
| `rtk bypass python3 .codex/bin/validate-v32-structure.py` | Exit 0: `V3.2 structure: OK` |
| `rtk bypass python3 .codex/bin/validate-codex-inheritance.py --check --repository parent --json` | Exit 1: the same six unrelated stale digests as the baseline; no `COMMAND-EXECUTION` finding |
| `rtk bypass make check-bilingual-docs` | Exit 0: `bilingual docs ok` |
| `rtk bypass make check-doc-links` | Exit 0: `repository path references: PASS` and `doc links ok` |
| `rtk bypass python3 ci/tools/new-change-record.py check` | Exit 0: `Change Record contract: PASS (structure only, not evidence validation)` |
| `rtk bypass git diff --check` and `rtk bypass git diff --cached --check` | Exit 0: no whitespace errors |

The official Linux musl release archive was checked against SHA-256 `5b919c3bccb799b67a61866d0e617410a4fcdf173e2614440e59de2fa2003436`.

## Security impact

This changes the Parent agent control plane, not connector product behavior. Hook protocol `permissionDecision = "allow"` enables input replacement; normal command approvals, sandbox checks, and action-specific authority still apply. No global configuration, trust bypass, or automatic host trust is introduced. Existing authentication wrappers remain mandatory. Framework and MRTS are unchanged.

## Runtime evidence

The real RTK v1.0.1 binary passed these fresh local checks:

| Scenario | Result |
| --- | --- |
| Configuration matches isolated `rtk init --codex` output | PASS |
| `git status` becomes `rtk git status`; `timeout` and `description` survive in `updatedInput` | PASS |
| `make quick-check` becomes `rtk make quick-check` | PASS |
| Already RTK-wrapped command: no rewrite | PASS |
| Unknown `permission_mode`: no rewrite | PASS |
| Missing `permission_mode`: no rewrite | PASS |
| Malformed JSON: no rewrite | PASS |
| File redirection: no rewrite | PASS |
| `rtk bypass` preserves stdout, stderr, and exit code 7 | PASS |

These checks demonstrate the binary protocol and unfiltered execution. They do not demonstrate hook activation in the user's running Codex session or execution of a connector build/test target.

## Known limitations

The Parent inheritance check already fails on six stale digests: `CHANGE-WORKFLOW`, `CONNECTOR-MATRIX`, `DEFINITION-OF-DONE`, `INDEX`, `PHASE4-TARGET-SEMANTICS`, and `TESTING-AND-EVIDENCE`. They are outside this fix and remain unchanged. The native hook deliberately leaves unsupported inputs untouched; the explicit RTK execution requirement still applies.

## Remaining risks

The host needs a compatible RTK binary on the Codex process's `PATH` and support for native hook rewriting. The exact project hook must be reviewed and trusted through `/hooks`; committing its JSON does not grant trust. Command classification can differ for an RTK-wrapped command, as documented upstream. No active host session or end-to-end host interception is claimed.

## Checks not run and rationale

Connector builds, runtime suites, I12 tests, and child-repository validation were not run because this change is limited to the Parent RTK control plane. The Parent documentation-link check used the Framework helper at the unchanged Parent-pinned revision `99a7985c1be92a2297b1b59208f64df6768f2cbf`; this is not Framework or MRTS qualification. End-to-end activation in the user's Codex session and remote CI/Quality Gates remain unverified.

## Final diff and review status

The six-file change is prepared on `fix/rtk-v1-codex-schema`. The focused RTK acceptance checks, structure validator, documentation checks, and diff checks pass; the inheritance result retains the known baseline failure. The coordinating diff review confirms the Parent-only scope and unchanged submodule pointer. This record captures pre-delivery local evidence; remote delivery and CI status must be read from the actual pull request. No merge, deployment, or active host interception is claimed.
