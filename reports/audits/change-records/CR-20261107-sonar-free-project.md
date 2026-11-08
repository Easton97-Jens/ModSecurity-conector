# CR-20261107-sonar-free-project

**Language:** English | [Deutsch](CR-20261107-sonar-free-project.de.md)

## Identity

| Field | Value |
| --- | --- |
| Change ID | CR-20261107-sonar-free-project |
| Date (UTC) | 2026-11-07 |
| Base revision | a5f697c35acb5386d2037f91dfed10ad4b469cd9 |

## Motivation and problem statement

The installed global Sonar integration already performs Secrets-only automatic checks. Parent instructions still permitted MCP and applied RTK universally to installed hooks; they lacked the explicit Free/file-before-read contract. Update the existing authority and developer guide without modifying the accepted global installation.

## Acceptance criteria

Existing AGENTS and routed policy consistently require Secrets before reads/searches, fail on findings/errors, permit development after a clean Secrets check, forbid automatic aggregate/paid analysis and keep MCP disabled. Preserve explicit per-project Cloud binding, revision-bound evidence, full existing CI Scanner analyses and independent current-head PR gates. Deliver only task changes on a codex/ branch as a Draft PR against master; never merge.

## Implementation decision and rationale

Keep one canonical Sonar policy and adapt the existing RTK policy with the narrow installed Codex-hook exception. Preserve the independent project RTK hook. Refresh only changed Parent policy digests. Add equivalent EN/DE current guidance before clearly historical analysis records; remove obsolete Parent-local scope-check/test examples. No runtime, scanner-workflow, analyzer-scope or gate configuration changes were needed. The documented old Change Record generator is absent from the current checkout; the pair uses the current Framework-owned Parent checker schema directly.

## Changed files

- `AGENTS.md`
- `.codex/context/command-execution-policy.md`
- `.codex/context/index.md`
- `.codex/context/security/analysis-services-policy.md`
- `.codex/context/sonarqube-policy.md`
- `.codex/inheritance-manifest.toml`
- `docs/sonarqube-analysis.md`
- `docs/sonarqube-analysis.de.md`
- `reports/audits/change-records/CR-20261107-sonar-free-project.md`
- `reports/audits/change-records/CR-20261107-sonar-free-project.de.md`

## Commands executed

| Command / procedure | Result |
| --- | --- |
| `rtk bypass /usr/local/bin/sonar-with-env analyze secrets --stdin` | Scoped instruction, proposed/changed-file and installed validation-input scans exited 0. Parent Markdown/TOML/Python pre-read: 735 files, 20 bounded batches, all exit 0. Active remaining configuration/scripts: 129 files, 683652 bytes, exit 0 before content search. |
| `rtk bypass python3 .codex/bin/validate-codex-inheritance.py --check --repository parent` | Exit 0; Parent catalog and digests consistent. |
| `rtk bypass python3 .codex/bin/validate-v32-structure.py` | Exit 0; V3.2 structure OK. |
| `rtk make check-bilingual-docs PYTHON=/var/tmp/codex/ModSecurity-test-Framework/venv/bin/python` | Exit 0; bilingual docs OK. |
| `rtk make check-doc-links PYTHON=/var/tmp/codex/ModSecurity-test-Framework/venv/bin/python` | Exit 0; repository path references PASS and doc links OK. |
| `rtk bypass git diff --check` | Exit 0. |
| `rtk bypass /usr/local/bin/sonar-with-env quality-gate status -p Easton97-Jens_ModSecurity-conector` | Query exit 0; no current-task-head Gate pass inferred. |
| `rtk bypass /usr/local/bin/sonar-with-env api get '/api/measures/component?component=Easton97-Jens_ModSecurity-conector&metricKeys=coverage,duplicated_lines_density'` | Query exit 0; available duplication measure returned, coverage omitted. Last Cloud analysis only. |

Initial docs checks with the explicit original Framework checkout exited 2 because this isolated Parent worktree had no materialized submodule link targets. A separate detached Framework worktree at the unchanged pinned commit `62b411e073551ef0fef22ab3d372e2489f2ae168` supplied those targets; both checks then passed. Framework/MRTS sources and gitlinks remain unchanged.

## Security impact

Secrets and error handling remain fail-closed; raw findings and credentials are suppressed. No rules, exclusions, authentication, trust, privileges or Quality Gates were weakened. The installed global hooks and their direct starter/scanner paths were not changed. CI retains its existing scanner and authentication context.

## Runtime evidence

No runtime evidence was collected or claimed. Supplied global automation acceptance dated 2026-11-07 is earlier evidence: both scanner children exited 0; handler-process exits were not recorded. This task's manual scans and query successes are not a new automatic-hook acceptance or a new full quality analysis.

## Known limitations

A report-inclusive ancillary configuration scan of about 19 MB exited 1 and was not treated as a pass. Reads/changes stopped; the relevant active selection was bounded to 129 files and rescanned successfully before search. Historical JSON reports were outside that inventory and were not opened or claimed scanned successfully. Current-head hosted checks and any applicable Cloud gate must be read from the PR; prior Cloud results do not qualify this change.

## Remaining risks

No new connector runtime risk is introduced by this documentation/control-plane change. Separate repositories retain their existing policy pins; this Parent-only task neither repins child manifests nor claims an all-repository inheritance pass. The original checkout's modified AGENTS.md and local .sonar-config.json are preserved.

## Checks not run and rationale

Connector builds/runtime matrices and new automatic hook-event acceptance were not run because the change affects instructions and documentation only. Paid/aggregate analysis and MCP were not invoked. No Framework/MRTS source changes or delivery occurred. Current-head external CI/Gate status is reported in the Draft PR after push, never inferred here.

## Final diff and review status

The scoped instructions and guide diff was reviewed by the main agent and an independent read-only reviewer; no blocker was found. Existing CI workflows, project scanner properties and hook configuration remain byte-for-byte unchanged. Exact delivery SHA, PR link and current-head check limitations belong to the PR metadata and task closeout.
