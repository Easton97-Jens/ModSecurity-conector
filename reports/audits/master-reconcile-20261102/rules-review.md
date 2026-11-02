# Proposed master checks

**Language:** English | [Deutsch](rules-review.de.md)

Status: proposed, not applied. The user must separately approve administrative changes. The local Sonar exception changes no GitHub workflow or general policy.

[Before snapshot](rules-before.json) and [after proposal](rules-after-proposal.json) retain the full visible configurations. [Connector create payload](connector-ruleset-create-proposal.json) and [Framework create payload](framework-ruleset-create-proposal.json) are standalone API request bodies. Existing rulesets remain unchanged, including archive branch coverage, strict checks, review requirements, deletion/force-push controls and absence of bypass actors. Only an additional master-only ruleset is proposed per repository.

## Existing protections

Connector ruleset 19138299 requires six contexts: actions, bounded-c-cpp, envoy-go, traefik-go, actionlint, zizmor. Framework ruleset 19700778 has no required_status_checks rule. Classic branch-protection reads return HTTP 403 Resource not accessible by integration for both repositories; further classic requirements are unknown. This is a read-access limitation, not evidence that protection is absent.

Sources: [Connector ruleset](https://api.github.com/repos/Easton97-Jens/ModSecurity-conector/rulesets/19138299), [Framework ruleset](https://api.github.com/repos/Easton97-Jens/ModSecurity-test-Framework/rulesets/19700778).

## Proposed required checks

The additional Connector list has 15 exact contexts and the Framework list 6, all bound to GitHub Actions integration 15368. Together with existing rules, this gives 21 visible Connector contexts. Source review found continuous master-PR delivery without path/fork job exclusions for these contexts. Require current-head GitHub checks; a display name alone does not establish runtime or findings status.

| Repository | Added checks |
| --- | --- |
| Connector | scaffold-lint; common-structure; apache-autotools-bootstrap; apache-structure; nginx-structure; nginx-exact-head; haproxy-structure; envoy-contract; lighttpd-contract; traefik-contract; quick-check; report-governance; protocol-contract; apr-util-provenance; pull-request-range |
| Framework | scaffold-lint; common-structure; CodeQL PR (actions); CodeQL PR (python); CodeQL PR (c-cpp); pull-request-range |

nginx-exact-head executes real hosted Functional-A H1 tests, including adapter provisioning and the nginx-hosted group. It is distinct from manual protected broker jobs and does not qualify H2/H3. Framework CodeQL PR jobs use upload: never; requiring them enforces analysis execution, not zero findings. All selected workflows lack merge_group; reassess before enabling a merge queue.

## Checks requiring further work

| Checks | Reason to remain outside this proposal |
| --- | --- |
| Framework actionlint-and-contract, zizmor, python-ci-security-quality, check-action-versions, portable-contract | PR path filters prevent universal delivery; remove filters and verify docs-only PR delivery before requiring. Existing maintenance PRs are not modified. |
| Parent go-candidate variants, nginx-b09-regression, five-cell CRS aggregate | PR path filters; retain real tests and qualify exact-head delivery before promotion. |
| Framework OSV and Scorecard | Duplicate pull-request-head identities; require explicit distinct job names and delivery qualification first. |
| Parent OSV pull-request-diff | Fork SARIF upload/permissions need qualification; same-repository success is insufficient. |
| Hosted Sonar and external SonarCloud checks | Fork-skipped jobs or missing external check delivery; existing CI remains intact. |
| C++20/23, scheduled scans, maintenance jobs | Explicitly advisory or operational rather than universally required PR checks. |
| Manual host/broker jobs and H2/H3 preflight | Not continuous runtime acceptance; never require an unimplemented campaign or fabricate an aggregate success. |

## Evidence and limits

Inspected current Parent and Framework workflow/composite sources on 2026-11-02, plus live rulesets and delivered check metadata. No fork PR or administrative mutation was performed. Before applying, refresh the before snapshot, resolve the inaccessible classic protection layer and verify current PR-head delivery. Existing protections must never be reduced.

Lokale Sonar-Secrets-Prüfung aufgrund ausdrücklicher Benutzeranweisung nicht ausgeführt.
