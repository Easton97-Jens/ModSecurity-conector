# Proposed master checks

**Language:** English | [Deutsch](rules-review.de.md)

Status: **PROPOSED_NOT_APPLIED**. The existing 2026-11-02 proposal was refreshed on 3 November 2026 at 13:32 CET (12:32 UTC). Administrative application still requires separate approval. No ruleset, branch protection, workflow or remote setting was changed. The explicit local Sonar exception leaves hosted Sonar/CodeQL checks intact.

[Before snapshot](rules-before.json) contains freshly read visible rulesets. [After proposal](rules-after-proposal.json) preserves those exact existing objects and adds only the unchanged [15-context Connector payload](connector-ruleset-create-proposal.json) and [6-context Framework payload](framework-ruleset-create-proposal.json). Their exact names and GitHub Actions integration ID 15368 were revalidated; no payload churn is needed when evidence confirms the existing selection.

## Current protection readback

Live master revisions are Parent `11fab78a5447f75cb254ddf963eca770fa04ba04` and Framework `bb6c7580208a05c17d6d6674571731b6a71028cb`. GitHub connector GET of ruleset collections with `includes_parents=true` returned one active repository ruleset each; individual details and authenticated read-only CLI GET of effective master rules agree:

- [Parent 19138299](https://api.github.com/repos/Easton97-Jens/ModSecurity-conector/rulesets/19138299): deletion and force-push prevention, resolved review threads, zero mandatory approvals, strict up-to-date checks `actions`, `bounded-c-cpp`, `envoy-go`, `traefik-go`, `actionlint`, `zizmor`; no bypass actors.
- [Framework 19700778](https://api.github.com/repos/Easton97-Jens/ModSecurity-test-Framework/rulesets/19700778): deletion and force-push prevention, resolved review threads, zero mandatory approvals; no required-status-check rule or bypass actors.

Both classic branch-protection reads remain **unreadable through the connector** (403, Resource not accessible by integration). The existing authenticated CLI GET returns 404, Branch not protected, for both; no classic configuration object was returned. These different access results are retained, not silently collapsed into “no protection”: effective rulesets apply. Administrative UI/settings beyond these readable responses remain **unchecked**. The connector rejected effective-branch-rules URLs at its endpoint allowlist; the documented GET-only CLI fallback supplied those reads.

## Exact check delivery

Fresh API check runs were correlated by Actions run ID, app ID and exact head SHA with `event=pull_request` workflow runs. All 42 context/PR rows have actual completed execution, not skipped-job substitutes. Sampled PRs are same-repository:

- Parent [442](https://github.com/Easton97-Jens/ModSecurity-conector/pull/442), head `4fcf094b7b93deda07c9b990d113f32d5d6a62da`; [440](https://github.com/Easton97-Jens/ModSecurity-conector/pull/440), head `6e72c42133ad4a9b9ddeb964724cb95805d27b84`.
- Framework [165](https://github.com/Easton97-Jens/ModSecurity-test-Framework/pull/165), head `44ce463261d1a4617d136580c6b61df4285d54b5`; [164](https://github.com/Easton97-Jens/ModSecurity-test-Framework/pull/164), head `6ac8c947b8a1f84a5d4cc79d05ee61bd7222430c`.

| Exact context | Workflow | PR 442 | PR 440 |
| --- | --- | --- | --- |
| `scaffold-lint` | `lint.yml` | [success](https://github.com/Easton97-Jens/ModSecurity-conector/actions/runs/41589921495/job/125764045488) | [success](https://github.com/Easton97-Jens/ModSecurity-conector/actions/runs/41474802514/job/125377424853) |
| `common-structure` | `test-common.yml` | [success](https://github.com/Easton97-Jens/ModSecurity-conector/actions/runs/41589921243/job/125764044568) | [success](https://github.com/Easton97-Jens/ModSecurity-conector/actions/runs/41474802290/job/125377421781) |
| `apache-autotools-bootstrap` | `test-apache.yml` | [success](https://github.com/Easton97-Jens/ModSecurity-conector/actions/runs/41589921226/job/125764044736) | [success](https://github.com/Easton97-Jens/ModSecurity-conector/actions/runs/41474802162/job/125377421385) |
| `apache-structure` | `test-apache.yml` | [success](https://github.com/Easton97-Jens/ModSecurity-conector/actions/runs/41589921226/job/125764044385) | [success](https://github.com/Easton97-Jens/ModSecurity-conector/actions/runs/41474802162/job/125377421044) |
| `nginx-structure` | `test-nginx.yml` | [success](https://github.com/Easton97-Jens/ModSecurity-conector/actions/runs/41589921322/job/125764044920) | [success](https://github.com/Easton97-Jens/ModSecurity-conector/actions/runs/41474802413/job/125377423128) |
| `nginx-exact-head` | `test-nginx-exact-head.yml` | [success](https://github.com/Easton97-Jens/ModSecurity-conector/actions/runs/41589921331/job/125764044911) | [success](https://github.com/Easton97-Jens/ModSecurity-conector/actions/runs/41474802341/job/125377424639) |
| `haproxy-structure` | `test-haproxy.yml` | [success](https://github.com/Easton97-Jens/ModSecurity-conector/actions/runs/41589921428/job/125764045090) | [success](https://github.com/Easton97-Jens/ModSecurity-conector/actions/runs/41474802086/job/125377420617) |
| `envoy-contract` | `test-envoy.yml` | [success](https://github.com/Easton97-Jens/ModSecurity-conector/actions/runs/41589921203/job/125764044402) | [success](https://github.com/Easton97-Jens/ModSecurity-conector/actions/runs/41474802430/job/125377425651) |
| `lighttpd-contract` | `test-lighttpd.yml` | [success](https://github.com/Easton97-Jens/ModSecurity-conector/actions/runs/41589921357/job/125764045299) | [success](https://github.com/Easton97-Jens/ModSecurity-conector/actions/runs/41474802178/job/125377422143) |
| `traefik-contract` | `test-traefik.yml` | [success](https://github.com/Easton97-Jens/ModSecurity-conector/actions/runs/41589921310/job/125764044724) | [success](https://github.com/Easton97-Jens/ModSecurity-conector/actions/runs/41474802094/job/125377420195) |
| `quick-check` | `quick-framework-check.yml` | [success](https://github.com/Easton97-Jens/ModSecurity-conector/actions/runs/41589921262/job/125764044623) | [success](https://github.com/Easton97-Jens/ModSecurity-conector/actions/runs/41474802518/job/125377427397) |
| `report-governance` | `verified-report-governance.yml` | [success](https://github.com/Easton97-Jens/ModSecurity-conector/actions/runs/41589921246/job/125764044728) | [success](https://github.com/Easton97-Jens/ModSecurity-conector/actions/runs/41474802406/job/125377424863) |
| `protocol-contract` | `protocol-contract.yml` | [success](https://github.com/Easton97-Jens/ModSecurity-conector/actions/runs/41589921312/job/125764044814) | [success](https://github.com/Easton97-Jens/ModSecurity-conector/actions/runs/41474802165/job/125377421228) |
| `apr-util-provenance` | `ci-security-workflow-lint.yml` | [success](https://github.com/Easton97-Jens/ModSecurity-conector/actions/runs/41589921343/job/125764045127) | [success](https://github.com/Easton97-Jens/ModSecurity-conector/actions/runs/41474802084/job/125377421862) |
| `pull-request-range` | `ci-security-secrets.yml` | [success](https://github.com/Easton97-Jens/ModSecurity-conector/actions/runs/41589921257/job/125764044969) | [success](https://github.com/Easton97-Jens/ModSecurity-conector/actions/runs/41474802117/job/125377421757) |

| Exact context | Workflow | PR 165 | PR 164 |
| --- | --- | --- | --- |
| `scaffold-lint` | `lint.yml` | [success](https://github.com/Easton97-Jens/ModSecurity-test-Framework/actions/runs/41587537426/job/125756418317) | [success](https://github.com/Easton97-Jens/ModSecurity-test-Framework/actions/runs/41468640209/job/125356060906) |
| `common-structure` | `test-common.yml` | [success](https://github.com/Easton97-Jens/ModSecurity-test-Framework/actions/runs/41587537773/job/125756419391) | [success](https://github.com/Easton97-Jens/ModSecurity-test-Framework/actions/runs/41468640054/job/125356059827) |
| `CodeQL PR (actions)` | `ci-security-codeql-pr.yml` | [success](https://github.com/Easton97-Jens/ModSecurity-test-Framework/actions/runs/41587537447/job/125756418387) | [success](https://github.com/Easton97-Jens/ModSecurity-test-Framework/actions/runs/41468639916/job/125356059652) |
| `CodeQL PR (python)` | `ci-security-codeql-pr.yml` | [success](https://github.com/Easton97-Jens/ModSecurity-test-Framework/actions/runs/41587537447/job/125756418598) | [success](https://github.com/Easton97-Jens/ModSecurity-test-Framework/actions/runs/41468639916/job/125356060366) |
| `CodeQL PR (c-cpp)` | `ci-security-codeql-pr.yml` | [success](https://github.com/Easton97-Jens/ModSecurity-test-Framework/actions/runs/41587537447/job/125756419300) | [success](https://github.com/Easton97-Jens/ModSecurity-test-Framework/actions/runs/41468639916/job/125356059948) |
| `pull-request-range` | `ci-security-secrets.yml` | [success](https://github.com/Easton97-Jens/ModSecurity-test-Framework/actions/runs/41587537446/job/125756419351) | [failure](https://github.com/Easton97-Jens/ModSecurity-test-Framework/actions/runs/41468640416/job/125356061346) |

Framework 164's `pull-request-range` executed and **failed**; this refresh does not relabel that history. Framework 165's current sampled head passed. Requiring a check enforces its actual conclusion at the selected future PR head; it does not mean all historical runs passed.

The 18 owning workflows were read from the exact master Git objects. Selected PR jobs have no path/fork exclusion; PR-only guards permit the relevant event. Ten pinned Framework composite actions backing Parent jobs have no fork/event conditional or continue-on-error marker. This supports the proposed continuous master-PR configuration, while the two same-repository samples do **not** establish fork execution, docs-only PR coverage, merge-queue delivery or results for the current task head. No merge queue is currently proposed; selected workflows lack `merge_group`.

## Explicit exclusions

| Checks | Current reason to remain outside this proposal |
| --- | --- |
| Framework actionlint-and-contract, zizmor, python-ci-security-quality, check-action-versions, portable-contract | Current PR path filters can suppress workflow delivery. Same-repository successes do not establish every PR. |
| Parent go-candidate variants, nginx-b09-regression, five-cell CRS aggregate | Current PR path filters. Do not promote solely because both sampled code-changing PRs delivered them. |
| Framework OSV/Scorecard pull-request-head | Duplicate check names remain observable in both sampled heads; distinguish producers before considering requirements. |
| Parent OSV pull-request-diff | Some underlying scan steps continue on error; fork/upload semantics remain unqualified. A green wrapper is insufficient findings evidence. |
| Hosted Sonar/external SonarCloud | Preserve existing checks and delivery-policy gates. Fork exclusions or delivery outside sampled heads are not qualified by this selection. |
| Scheduled/advisory jobs, C++20/23, manual root broker, H2/H3 preflight | Not continuous mandatory PR execution. `nginx-profile-and-client-preflight` is skipped in both sampled Parent PRs and remains excluded. |

`nginx-exact-head` is the ordinary hosted H1 path, separate from manual protected broker admission and H2/H3 qualification. Framework CodeQL PR uses `upload: never`; requiring execution does not prove zero findings. GitHub accepts some skipped/neutral conclusions as successful status checks, so check presence alone cannot establish execution. See [GitHub required-check troubleshooting](https://docs.github.com/en/pull-requests/how-tos/merge-and-close-pull-requests/troubleshooting-required-status-checks) and [effective branch-rules API](https://docs.github.com/en/rest/repos/rules#get-rules-for-a-branch).

## Application handoff and evidence limits

Repository integration remains separate from protection-rule application. Parent
keeps its current Framework gitlink at `bb6c7580208a05c17d6d6674571731b6a71028cb`;
do not pin an unmerged Framework candidate. The generated inline broker caller
already comes from that exact canonical blob and truthfully retains its `bb6`
source header. Framework/MRTS Draft PRs have independent delivery boundaries.
Only after separately authorized integration propagate the actual merge SHA,
regenerate projections and rerun exact-pair generator/pin checks. A successful
review here authorizes none of those merges or administrative writes.

Keep existing archive branch coverage, required reviews/threads, strictness, deletion/force-push prevention and no-bypass policy unchanged. The hypothetical combined visible context count is 21 for Parent and 6 for Framework; this is a proposal, not server state. Before administrative approval, refresh all protection layers and verify the actual final PR head, expected app identity, fork policy and applicable Sonar gate. Reassess `merge_group` before enabling a queue. Do not require manual/regularly skipped jobs or invent a green aggregate.

Fresh run-scoped evidence below the invoking project's approved external storage root: `runs/20261103T115937Z-runtime-readiness/github/governance`. It retains exact GET URLs, timestamps, immutable source hashes, current ruleset objects, classic access errors and 42 check/run correlations. JSON validation confirms existing rulesets preserved verbatim, payload references identical, exact app-bound contexts delivered and no selected skipped/missing execution. No secret values, administrative write, new PR, commit or campaign is included.
