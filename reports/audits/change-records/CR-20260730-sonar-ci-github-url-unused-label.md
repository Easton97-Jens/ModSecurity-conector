# Change Record: Parent CI GitHub URL-validation unused-parameter cleanup for SonarQube Cloud S1172

**Language:** English | [Deutsch](CR-20260730-sonar-ci-github-url-unused-label.de.md)

## Identity

| Field | Value |
| --- | --- |
| Change ID | CR-20260730-sonar-ci-github-url-unused-label |
| Date (UTC) | 2026-07-30 |
| Base revision | fe4840a0a72449bbdb8f7b2f77f09922c9e66a9f |
| Tracking | Parent SonarQube Cloud `python:S1172` Code Smell `AZ9cRyj3HhV2CayPTPyt` at `ci/provisioning/components/prepare-runtime-components.py:245`. |
| Boundary | Parent CI URL configuration validation, its direct Parent tests, this English/German Change Record pair, and the paired indexes. Framework, MRTS, Gitlinks, connector source, SonarQube Cloud configuration, Quality Gates, exclusions, suppressions, and `master` remain unchanged. |

## Motivation and problem statement

SonarQube Cloud reports that `label` is unused by
`require_https_github_repo_url(url, label)`. The helper is on a source URL
validation boundary, so this change removes only that unused signature value
and its sole caller argument while retaining the existing validation behavior.

## Acceptance criteria

- Remove only the unused `label` parameter and its direct caller argument.
- Preserve `github_repo_path()` validation: exact HTTPS, exact `github.com`,
  no query or fragment, and exactly one owner/repository pair.
- Preserve blocked behavior before cache/build setup for invalid configured
  GitHub URLs, and add direct canonical-acceptance and rejection coverage.
- Maintain an equivalent English/German Change Record pair and paired indexes.
- Do not claim the baseline SonarQube Cloud issue closed before an exact PR-head
  analysis observes it.

## Implementation decision and rationale

`require_https_github_repo_url()` now accepts only `url`; `label` was not read
by the helper, its return value was discarded by its only caller, and it never
appeared in a validation error. The new direct test preserves canonicalization
of an HTTPS GitHub URL with a `.git` suffix and rejects non-HTTPS, wrong-host,
host-port, query, fragment, incomplete, and overlong repository forms through
the configuration-level caller.

## Changed files

- `ci/provisioning/components/prepare-runtime-components.py`
- `tests/test_prepare_runtime_components.py`
- `reports/audits/change-records/README.md` and `README.de.md`
- this English/German Change Record pair

## Commands executed

Focused commands use the selected Parent `.venv` Python with
`PYTHONNOUSERSITE=1`, `PIP_REQUIRE_VIRTUALENV=true`,
`PIP_DISABLE_PIP_VERSION_CHECK=1`, `PYTHONDONTWRITEBYTECODE=1`, and task-owned
external `TMPDIR`/bytecode paths:

- `rtk proxy -- <Parent .venv python> -m pip check`
- `rtk proxy -- <Parent .venv python> -m py_compile ci/provisioning/components/prepare-runtime-components.py tests/test_prepare_runtime_components.py`
- `rtk proxy -- <Parent .venv python> -m unittest -v tests.test_prepare_runtime_components.PrepareRuntimeComponentsTest.test_github_repo_url_config_preserves_canonical_and_rejection_policy tests.test_runtime_component_cache_contract.RuntimeComponentCacheContractTest.test_clean_managed_git_checkout_is_reused_across_target_preparations`
- `rtk proxy -- <Parent .venv python> -m unittest -v tests.test_prepare_runtime_components`
- `rtk proxy -- <Parent .venv python> -m unittest -v tests.test_bilingual_docs`
- `rtk proxy -- <Parent .venv python> -c <direct Change Record pair validation>`
- `rtk proxy -- make check-bilingual-docs`
- `rtk proxy -- make check-doc-links`
- `rtk proxy -- git diff --check`

## Tests and actual results

- Parent Python environment selection and `pip check` passed; the selected
  interpreter is Python `3.14.4` in the Parent virtual environment.
- Python syntax compilation passed for the changed source and test files.
- The new URL-validator contract test passed, covering valid canonicalization
  and seven rejected configuration forms.
- The existing managed-checkout reuse control passed with a canonical GitHub
  URL and one controlled local clone.
- The complete `tests.test_prepare_runtime_components` module ran before the
  edit: 24 tests passed; four unrelated HAProxy cache tests were blocked by the
  intentionally uninitialized Framework gitlink in this isolated Parent
  worktree. No Framework initialization or fallback was used.
- The direct Change Record pair contract passed with no errors, and
  `tests.test_bilingual_docs` passed 21 tests.
- `make check-bilingual-docs` is `blocked_environment` only by 20 existing
  missing Framework-gitlink link targets; no reported error cites this pair or
  its indexes. `make check-doc-links` is blocked by the corresponding 16
  existing missing Framework-gitlink link targets.
- `git diff --check` passed after the source, test, and documentation edits.

## Security impact

The focused security assessment is `already_safe` for this signature-only
change. Environment-provided GitHub URLs remain controlled input;
`github_repo_path()` still enforces the HTTPS/exact-host/plain-owner-repository
policy before any cache, build, Git, or network sink. Invalid configurations
still raise `RuntimeError` and follow the existing blocked path. No security
finding is claimed fixed.

## Documentation status

This record and its German companion describe the same source boundary, tests,
limitations, and delivery boundary. The paired record-index entries provide
traceability. The direct pair contract and bilingual unit suite pass; full
repository documentation checks are blocked only by pre-existing absent
Framework-gitlink targets, not by this record or its indexes.

## Runtime evidence

No connector, host, protocol, or production runtime behavior changed or is
claimed. The focused unit controls validate the CI configuration boundary; they
are not connector runtime evidence.

## Known limitations

This candidate addresses one live Parent `ci/` SonarQube Cloud row from the
current 304-item CI inventory. The row remains open until SonarQube Cloud
analyzes the exact delivered PR head.

## Remaining risks

An accidental missed call site could make future URL validation fail. The
current Parent call inventory found one caller, and the direct configuration
test plus existing managed-checkout control exercise both validation and the
downstream canonical URL path. This change makes no claim about unrelated
Sonar findings or scanner vulnerability leads.

## Checks not run and rationale

- The complete `tests.test_prepare_runtime_components` module cannot pass in
  this isolated Parent worktree because four unrelated tests require an
  initialized read-only Framework submodule. C11 does not initialize or modify
  that boundary solely to satisfy those tests.
- Hosted GitHub Actions, SonarQube Cloud candidate-head analysis, commit, push,
  and Draft PR creation have not yet occurred at record authoring and are not
  claimed.
- Connector builds, host configuration checks, runtime smokes, protocol
  matrices, Framework checks, and MRTS checks are not applicable because no
  connector/runtime implementation or cross-repository content changes.

## Final diff and review status

The scoped implementation removes only the unused signature parameter and the
matching caller argument, then adds direct preservation coverage. Delivery and
exact-head hosted evidence are intentionally recorded only after they occur;
no `master` merge is authorized by this Change Record.
