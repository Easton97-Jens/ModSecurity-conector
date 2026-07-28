# Change Record: Parent test-fixture duplication reduction for SonarQube Cloud

**Language:** English | [Deutsch](CR-20260727-sonar-parent-test-duplication.de.md)

## Identity

| Field | Value |
| --- | --- |
| Change ID | CR-20260727-sonar-parent-test-duplication |
| Date (UTC) | 2026-07-27 |
| Base revision | 1b0f8825f3510b99b603bb6cd6f0777e1710358e |
| Tracking | Parent duplication baseline: 2,013 duplicated lines and 0.4 percent density. Candidate components: `tests/test_runtime_component_cache_contract.py` (187) and `tests/test_connector_capabilities.py` (38); component counts may overlap. |
| Boundary | The two Parent test modules and this English/German Change Record pair. Product source, test cases/assertions, Framework/MRTS source, Gitlinks, workflows, generated reports, SonarQube Cloud configuration, suppressions, external issue state, and master remain unchanged. |

## Motivation and problem statement

The current SonarQube Cloud baseline reports a 0.4-percent duplicated-lines
density. The two selected Parent test modules contain repeated local-fixture
setup that obscures the independently meaningful cache-integrity and
Framework-provenance assertions. This candidate removes only that repeated
setup; it does not remove, merge, or weaken tests.

## Acceptance criteria

- Every existing test method, assertion, negative case, and temporary-root
  isolation remains present and semantically equivalent.
- Shared private helpers remain local to their owning test class and retain
  local-only Git, expected remote, clone/fetch, cache, and Framework-gitlink
  contracts.
- No production implementation, Framework/MRTS source, Gitlink, workflow,
  generated report, Sonar configuration, suppression, or `master` changes.
- The full two focused modules, documentation checks, and diff hygiene pass.
- A new exact-head SonarQube Cloud analysis, not this local refactor alone,
  determines the actual global duplication reduction.

## Implementation decision and rationale

`RuntimeComponentCacheContractTest` now owns private helpers for the repeated
Expat fixture, local upstream repository, and clone/fetch interception. The
individual test cases retain their distinct expected ref, error, mutation, and
assertion logic. `ConnectorCapabilitiesTest` similarly owns one helper that
creates a local Framework checkout and records its Parent gitlink; matching,
mismatch, and stale-record tests retain their own outcome setup and assertions.

This extracts only demonstrably identical test scaffolding. It deliberately
does not change cache production, source provenance, Framework validation, or
the content/number of control cases.

## Changed files

- tests/test_runtime_component_cache_contract.py
- tests/test_connector_capabilities.py
- reports/audits/change-records/CR-20260727-sonar-parent-test-duplication.md
- reports/audits/change-records/CR-20260727-sonar-parent-test-duplication.de.md
- reports/audits/change-records/README.md
- reports/audits/change-records/README.de.md

## Commands executed

```sh
rtk proxy env PYTHONDONTWRITEBYTECODE=1 PYTHONNOUSERSITE=1 /root/git/ModSecurity-conector/.venv/bin/python -B -m unittest -v tests.test_runtime_component_cache_contract
rtk proxy env PYTHONDONTWRITEBYTECODE=1 PYTHONNOUSERSITE=1 /root/git/ModSecurity-conector/.venv/bin/python -B -m unittest -v tests.test_connector_capabilities
rtk proxy make check-bilingual-docs
rtk proxy make check-doc-links
rtk proxy git diff --check
```

## Tests and actual results

| Command or check | Result |
| --- | --- |
| `tests.test_runtime_component_cache_contract` | passed: 27 tests. |
| `tests.test_connector_capabilities` | passed: 13 tests. |
| Cache/provenance negative controls | passed: clean/dirty/corrupt/moving Git checkout, complete manifest, cache identity, Framework matching/mismatch, and stale-record contracts remain covered by the focused modules. |
| `git diff --check` | passed: no whitespace errors. |

## Security impact

The patch changes test-only fixture setup around security-relevant cache and
provenance controls. It does not alter product command execution, network
access, safe-root/path handling, cache-validation code, Framework/MRTS source,
or a security control. The focused modules exercise the retained local-only
Git and negative provenance/cache contracts. No new security finding was
identified; hosted security analysis remains pending.

## Documentation status

This complete English/German Change Record pair records the scope, actual
validation, and limitation that local duplicate counts do not prove the global
SonarQube Cloud metric. The record indexes are updated in both languages.

## Runtime evidence

No runtime connector, protocol, host, report-generation, or production
behavior changed or is claimed. The focused tests are test-contract evidence,
not connector runtime evidence.

## Known limitations

The isolated Parent worktree initialized the existing Parent-recorded
Framework Gitlink `47e50e7bc43ba7a3b5bad1a9448111794f664cc0` only so the
Framework-dependent test could run. No Framework/MRTS source or Gitlink was
modified. SonarQube Cloud has not yet analyzed the candidate; it is therefore
incorrect to claim an observed reduction from the 0.4-percent baseline.

## Remaining risks

The helpers are intentionally narrow, but a future test might depend on a
fixture detail not covered by the current focused modules. Keeping helpers
private, retaining per-test outcome setup, and running both full focused
modules reduce that risk. This candidate makes no conclusion about other
duplicate blocks or the broader 1,022-item backlog.

## Checks not run and rationale

- Connector builds, full runtime matrices, and MRTS tests are not applicable:
  no product/runtime or cross-repository source changed.
- Hosted GitHub checks and exact-head SonarQube Cloud analysis have not yet
  occurred. This record provides neither a global duplication result nor
  master-merge authority.

## Final diff and review status

The candidate is limited to two Parent test modules and required bilingual
traceability material. A dedicated independent semantic review is required
before delivery; facts about commit, push, PR, hosted checks, Sonar analysis,
or merge will be recorded only after they are observed.
