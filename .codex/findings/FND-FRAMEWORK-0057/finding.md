# FND-FRAMEWORK-0057 — Connector-neutral security/data-flow descriptors are treated as executable runtime cases

## Identity

| Field | Value |
| --- | --- |
| ID | FND-FRAMEWORK-0057 |
| Category | ci_failure |
| Repository / ownership | framework / framework |
| Priority / severity / confidence | P1 / not_applicable / reproduced |
| Status / feasibility | fixed / blocked_external_dependency |
| Release blocker / security relevant | true / true |
| Affected revision | `a7ebf5a1d9cad2b0a65a7603476a1434fdb16cf6` |
| Parent/MRTS disposition | Framework PR #51 is merged and adopted by Parent #126; Parent #74 needs a fresh exact-head producer and strict gate; MRTS remains unchanged |

## Summary, observed behavior, and impact

## 2026-07-26 Framework revalidation and remaining blocker

Current Framework master `47e50e7bc43ba7a3b5bad1a9448111794f664cc0` passes
the Framework-owned case-schema, matrix-report, and security-data-flow checker
controls. This is therefore not a remaining Framework source defect. The
record remains blocked, rather than verified, until Parent PR #74 supplies a
fresh exact-head producer, strict terminal gate, SonarQube Cloud, review, and
protected-integration evidence. Parent and MRTS were not changed in this task.

The exact Parent PR #74 runtime producer at
`c6db0f8ab5b95be67a92ba925a1f4caa3d3d0a1d` prepared native Apache and NGINX
successfully, then Framework force-all case discovery failed with `ValueError:
case requires rules` for a Framework-owned `security-data-flow` descriptor.

All 15 descriptors in `tests/cases/security-data-flow/**` are connector-neutral
former-XFAIL connector-gap inventory with `capabilities.runtime_verified:
false`; none has a connector-owned ModSecurity rule. The runner additionally
normalizes their declared `security_data_flow` capability to
`security-data-flow`, but that normalized capability was unknown. Consequently
the schema cannot distinguish an explicitly non-executable descriptor from an
incomplete active runtime case.

The defect blocks fresh legitimate Parent #74 runtime evidence. A placeholder
rule or broad exception would risk inventing connector runtime behavior and
promoting unsupported security results. No production exploit is claimed.

## Reproduction and root cause

Hosted evidence is GitHub Actions Parent PR #74 run `30205593649`, job
`89802976898`. A direct Framework force-all `case_cli.py list-cases` control
reproduced the prior failure; after the staged repair it completes without
selecting those descriptors.

The runner assumes every YAML is materializable and therefore requires
`rules`, request, and expectation data. It also omits the normalized
`security-data-flow` token from its capability allowlist. These descriptors
intentionally have no connector implementation rules and must not enter a
connector runtime.

## Remediation and acceptance criteria

The remediation introduces `runtime_materializable: false`, accepted only when
all of the following hold:

1. `status` is `connector-gap`;
2. `former_xfail` is exactly true; and
3. `capabilities.runtime_verified` is exactly false.

The runner excludes such cases even under force-all discovery, direct
materialization rejects them, and the report generator emits
`NOT_EXECUTABLE` / non-promotable metadata. The normal non-empty `rules`
requirement continues for materializable cases; the normalized capability is
registered without accepting arbitrary capability strings.

Acceptance requires the 15 descriptors to pass this constrained contract;
focused runner/CLI and report tests to pass; force-all discovery not to select
the descriptors; direct materialization to fail; Framework PR #51's hosted CI,
SonarQube Cloud, review, and protected integration to complete; and then the
adopted Parent #74 exact-head producer and strict terminal gate to pass.

## Evidence, validation, and residual risk

Retained bounded evidence:
`/var/tmp/codex/runs/framework/20260726T145000Z-security-data-flow-case-schema/evidence/security-data-flow-case-schema-summary.md`
(SHA-256 `72c36838d9d868f50df8cc7e6dfe35fd0e72c59928415b9da1c84e828ad2ee90`).
It records failure identifiers, the contract, and local results without raw
hosted logs or runner environments.

Focused runner/CLI and report-generator suites passed 22 tests. Force-all
discovery, syntax compilation, the 15-case security-data-flow checker, and
documentation/Change Record checks passed. Ruff and Pyright are unavailable
and were not installed. An isolated no-MRTS generator smoke exited 0 but did
not have canonical input inventory; its generated output was discarded.

The residual risk remains visible connector-gap inventory until a
connector-owned implementation supplies rules and live evidence. No runtime
result, promotion, test weakening, or risk acceptance is claimed. Framework
PR #51 is merged as `de705a5`; Parent #126 already adopts that Gitlink. The
remaining evidence gap is the fresh Parent #74 producer and strict terminal
gate, not a Framework or MRTS change.

## History

- 2026-07-26 — Reproduced from exact Parent #74 hosted failure and direct
  Framework force-all discovery; the full 15-case audit identified the missing
  explicit descriptor state and normalized-capability allowlist omission.
- 2026-07-26 — Implemented and locally validated the narrow Framework repair
  in an isolated worktree; Framework Draft PR
  [#51](https://github.com/Easton97-Jens/ModSecurity-test-Framework/pull/51)
  is open at exact head `792bbffb1eefc7be0a9f76911729917d606eb00b`. Its hosted
  check cycle is in progress; no Framework merge is authorized.
- 2026-07-26 — All visible exact-head GitHub Actions checks passed. SonarQube
  Cloud has not produced a PR analysis: the Quality Gate is `NONE` and
  new-code measures are empty. The empty issues endpoint is not treated as a
  zero-issue/zero-duplication result; the Draft must receive real Sonar
  analysis before review/integration evidence can be complete.
- 2026-07-26 — Framework PR #51 later received completed SonarQube Cloud
  analysis and merged normally as `de705a5efb872f95f010346fe2e6143c88876ad4`.
  Final visible PR checks, including SonarQube Cloud Code Analysis, succeeded.
  Direct PR #51 readback reports zero open/confirmed issues and zero
  new-code duplication. Parent #126 has already adopted the resulting
  Gitlink; a refreshed Parent #74 exact-head producer and strict gate are now
  the only outstanding acceptance controls.
