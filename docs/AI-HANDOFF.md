# AI handoff

**Language:** English | [Deutsch](AI-HANDOFF.de.md)

## Snapshot and goal

- Date: **2026-11-14 (Europe/Berlin)**; checkout: `/root/git/ModSecurity-conector`.
- Branch: `codex/ai-handoff-and-framework-pin-20261114`; Parent HEAD **before the initial PR commit**: `5672c5ff562495ddbc47a1932b1641e0073746f5`. This document records that precommit snapshot; resolve the later HEAD, index and PR status from Git/GitHub.
- **Conversation context:** first prepare a documentation-only Claude Code handoff, then create a PR including the other existing changes. The second request authorizes the task-branch commit/push/PR and inclusion of the Framework pin. It does not authorize a merge. No earlier product-task conversation or test transcript is available here.
- **Verified facts:** local diffs and native command definitions were inspected. Fresh remote reads confirmed Parent `master` at the base above and Framework `master` at `31531f74cfe26c2a40d4bb5f6eaae4c0920127e1`.
- **Assumption:** Claude Code resumes in this checkout, where ignored local instructions remain available. Reconcile this snapshot before relying on it.

## Relevant components and completed work

- `common/` owns shared product contracts/runtime; `connectors/` owns Apache, NGINX, HAProxy, Envoy, Traefik and lighttpd adapters. Logical profiles retain separate runtime claims; see [connector overview](connectors/README.md) and [architecture](architecture.md).
- Root `Makefile` owns product-build entry points and delegates test/check targets to `modules/ModSecurity-test-Framework/connector_suite/connector.mk`. Framework and its nested `tools/MRTS` remain separate repositories.
- Existing Parent HEAD updates workflow-tool pins in `.github/workflows/`, `ci/tooling/security-tools.lock.yml` and `docs/security/ci-security-tooling{,.de}.md` (#447). Commit presence does not prove passing checks.
- This work adds the handoff pair, permanent handoff rules in `AGENTS.md`, a local `CLAUDE.md` entry and the [Change Record](../reports/audits/change-records/CR-20261114-ai-handoff-and-framework-pin.md).
- The native `ci/tools/sync-framework-component-versions.py` synchronized the Parent lock and 22 workflow identities for the selected Framework commit. Independent byte comparison confirmed that every workflow change only replaces the old Framework SHA with the new SHA; only `framework_sha` changes in the lock. No connector, Framework or MRTS source was edited.

## Changes selected for the PR

The initial handoff task began with no staged changes or non-ignored new files. The following table records the precommit selection; after commit, these paths are no longer uncommitted changes. Inspect both `git diff` and `git diff --cached` before further staging.

| Path | Origin / PR content |
| --- | --- |
| `.gitignore` | Existing unstaged additions `.claude`, `.rtk`, `.aws`; final extra blank line removed during PR preparation to satisfy whitespace validation. |
| `AGENTS.md` | Three permanent handoff rules; original rules preserved. |
| `docs/AI-HANDOFF.md`, `docs/AI-HANDOFF.de.md` | New English/German handoff pair, untracked before explicit staging. |
| `modules/ModSecurity-test-Framework` | Existing checkout difference selected for Parent commit: `62b411e073551ef0fef22ab3d372e2489f2ae168` to `31531f74cfe26c2a40d4bb5f6eaae4c0920127e1`. |
| `ci/tooling/project-versions.lock.json`, 22 files under `.github/workflows/` | Required generated Framework identity projections, synchronized through their native owner. |
| `reports/audits/change-records/CR-20261114-ai-handoff-and-framework-pin.md`, `reports/audits/change-records/CR-20261114-ai-handoff-and-framework-pin.de.md` | New native-scaffolded Change Record pair. |
| `CLAUDE.md` | Existing ignored local file, updated with the project-instruction entry; original RTK guidance retained. Excluded from the PR and not transferred by a normal clone. |

Framework is internally clean on `master`; the selected commit is its already-published maintenance update #170. MRTS stays at `ee2174431c4edf97e66afe32558ce8454deb2397`, matching its Framework gitlink. No nested repository was staged or committed. `CLAUDE.md` remains ignored by `.gitignore:50`; no credential stores or authentication files were inspected.

## Decisions, rejected approaches and open work

- Permanent rules belong in `AGENTS.md`, changing work state here. Keep EN/DE companions synchronized, RTK mandatory and Secrets scanning before content reads. Consult `.codex/context/index.md` and applicable directory instructions.
- Reject a pointer-only Framework update: the Parent lock and workflow identities must agree. The existing synchronizer owns those generated projections; no manual workflow edits or weakened gates were used.
- Earlier rejected product approaches are not evidenced in the available conversation. The historical `prepare-reviewed-framework-handoff.py` repair was not used because it targets unrelated fixed revisions.
- The initial whole-worktree whitespace check failed at `.gitignore:55`; PR preparation removed that blank line. No product bug was reproduced here.
- No current-head runtime qualification or merge readiness is claimed. The [2026-11-03 readiness record](../reports/audits/change-records/CR-20261103-runtime-readiness-prerequisites.md) is historical evidence with older pins, not a fresh result for this branch.

## Executed checks and limitations

**Current delivery blocker:** the installed Sonar pre-commit hook requires an operator-owned exact Gitlink admission for this worktree, Framework commit and index. That admission is absent. All 30 paths remain staged; no commit, push or PR exists. Separate Secrets scans of 29 staged Parent blobs and 11 changed Framework blobs exited 0; those scans do not grant admission.

| Command or procedure | Observed result |
| --- | --- |
| `rtk bypass git status --short --branch --untracked-files=all`; staged/unstaged diff inspection; `rtk bypass git submodule status --recursive` | Identities and changes above inspected; Framework clean internally. |
| `rtk bypass git ls-remote https://github.com/Easton97-Jens/ModSecurity-conector.git refs/heads/master`; equivalent Framework remote read | Exit 0; confirmed the two remote master identities above. |
| `rtk bypass /usr/local/bin/sonar-with-env analyze secrets --stdin` on selected instruction/source/diff/documentation bytes | Completed explicit scans exited 0; raw output suppressed. An earlier external-helper edit hook was incomplete, followed by a successful explicit scan. No code-quality result is implied. |
| `rtk bypass python3 -B /var/tmp/codex/ModSecurity-conector/ai-handoff-20261114/validate_handoff.py` | Initial handoff scoped checks passed; a previous German switch/four-link failure was corrected before that pass. |
| Native candidate verifier before/after synchronization; native synchronizer `--check` and `--verify-primary` | Exit 0; candidate verified, `changed=[]`, `FRAMEWORK_PRIMARY_VERIFIED`. Exact commands are in the Change Record. |
| `rtk make check-doc-links`; `rtk bypass git diff --cached --check` | Exit 0; repository paths, local links and staged whitespace clean. |
| `rtk make check-bilingual-docs` | Stopped after 15 minutes CPU-bound in repeated ignored-path lookup; exit 2 after termination, not a PASS. |
| `rtk bypass env CONNECTOR_REVISION=5672c5ff562495ddbc47a1932b1641e0073746f5 .venv/bin/python -B /var/tmp/codex/ModSecurity-conector/ai-handoff-pr-20261114/check_bilingual.py` | Exit 0, `bilingual docs ok`; all existing full-checker rules/discovery retained, with an equivalent indexed ignored-path predicate. No checker source changed. |
| Native Change Record archive check | Exit 0; structural contract passed. |
| `rtk bypass git commit -m 'Prepare AI handoff and synchronize Framework maintenance pin'` | Exit 1; pre-commit hook denied the staged Gitlink: `No exact operator V2 admission for selected Gitlink`. No commit or PR created. |

The first scaffold attempts lacked the explicit Framework environment/import path; the successful native invocation supplied both. System-Python candidate verification lacked `yaml`; using the repository `.venv/bin/python` passed. The first synchronizer invocation rejected an input outside its allowed temporary root; selecting the task-owned `RUNNER_TEMP` passed without relaxing path checks.

**Not run:** product builds, `quick-check`, `test`, host/config/runtime probes, CI or Cloud Quality Gates. Current-head CI/review status must be read after push; no older result qualifies the new commit.

## Repository-derived start, build and test commands

References below are not executed product-test results. Run from the Parent root with the selected prerequisites in [getting started](getting-started.md) and external writable build/runtime roots from `.codex/config.toml`.

| Purpose | Command / source |
| --- | --- |
| Framework directory / active selection | `rtk make check-framework`; `rtk make check-active-inventory` — root `Makefile`, `README.md`. Directory existence does not verify pin equality. |
| Fast checks / default tests | `rtk make quick-check`; `rtk make test` — root `Makefile`, `README.md`; bare `make` defaults to `test`. |
| NGINX build / configuration | `rtk make build-nginx BUILD_ROOT=/var/tmp/codex/ModSecurity-conector/build`; `rtk make check-config-nginx BUILD_ROOT=/var/tmp/codex/ModSecurity-conector/build` — `docs/getting-started.md`. |
| Documentation | `rtk make check-bilingual-docs`; `rtk make check-doc-links` — `README.md`, delegated Framework targets. Stage selected new files before checks using tracked-file selection. |
| Envoy ext_proc service | `rtk make -C connectors/envoy serve-envoy-ext-proc BUILD_ROOT=/var/tmp/codex/ModSecurity-conector/build EXT_PROC_RULES_FILE=/absolute/path/to/reviewed/rules.conf` — `connectors/envoy/Makefile`. Replace the rule path with an existing reviewed file; requires Go/CGo/libmodsecurity inputs. Starts the service, not the Envoy host. |

## Next steps

1. Read `AGENTS.md`, applicable directory instructions and this handoff; reconcile branch/HEAD, staged/unstaged files, Framework and MRTS identities.
2. Obtain explicit operator authorization for the exact Gitlink admission, then commit/push only the selected paths and open a Draft PR with the recorded local check results and limitations. Read back the committed lock/gitlink, actual PR head and CI status; merge needs separate authorization.
3. Choose the next concrete product objective. Inspect affected source and select only relevant checks; do not restart archived I12/matrix campaigns without an explicit request.
4. Record actual results and remaining gaps in both handoff versions before the next Codex/Claude Code switch. Preserve the ignored local `CLAUDE.md` separately when moving workspaces.
