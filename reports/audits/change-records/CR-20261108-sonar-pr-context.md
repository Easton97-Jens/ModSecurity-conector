# Change Record: CR-20261108-sonar-pr-context

**Language:** English | [Deutsch](CR-20261108-sonar-pr-context.de.md)


## Identity

| Field | Value |
| --- | --- |
| Change ID | CR-20261108-sonar-pr-context |
| Date (UTC) | 2026-11-08 |
| Base revision | `400c47ebd5a6fe32dc43ec6875968ce7ebae04d0` |

## Motivation and problem statement

C++20 and C++23 explicitly forced the `master` branch even for pull requests. Their red master gates could not establish the requested PR state. Restore each variant's actual GitHub event context while keeping all source files and independent project keys.

## Acceptance criteria

All three configured standards must produce their own current-head PR analysis. Missing PR contexts remain missing evidence. The final task also requires zero open/accepted PR issues, zero unchecked hotspots and Gate OK in every associated project, plus the separately recorded full final-pair regression.

## Implementation decision and rationale

Remove the three matrix `branch_args` fields and their scanner interpolation. Keep automatic GitHub event detection, exact checkout/SCM SHA, project keys, standards, full scope, secrets guard and gate waiting. The existing advisory flags are preserved; they do not satisfy the task's independent requirement that all three gates pass. A separate Framework contract change rejects reintroduced context overrides.

## Changed files

- `.github/workflows/sonarqube.yml`
- `docs/sonarqube-analysis.md` and `docs/sonarqube-analysis.de.md`
- This English/German Change Record pair.

The subsequent Framework gitlink, version lock and registered workflow projection handoff uses the native publisher; Framework-owned tests and records remain in their separate repository.

## Commands executed

`rtk bypass /usr/local/bin/sonar-with-env analyze secrets --stdin` completed with exit 0 for each selected changed file. The native `ci/tools/new-change-record.py create --name sonar-pr-context --base-revision 400c47ebd5a6fe32dc43ec6875968ce7ebae04d0 --date 2026-11-08` scaffold command completed with exit 0 using explicit Parent/Framework context. Six Framework-owned focused Sonar methods passed against the corrected workflow, including eight effective context-override mutations; the Framework record owns their full command and logs.

## Security impact

No new credentials, secret consumers, permissions, triggers or source exclusions. The scanner token remains restricted to its existing pinned action. Event-derived PR routing restores evidence attribution; it does not change the new-code baseline, quality rules or gates.

## Runtime evidence

No fresh host-runtime result is claimed by this workflow/documentation change. The required final-pair host executions are recorded separately after the delivered pair is frozen.

## Known limitations

The initial Cloud snapshot still describes Parent `400c47ebd5a6fe32dc43ec6875968ce7ebae04d0` and Framework `d14937ce8fe7a534bb755cffa6597e62eadbb126`. Framework has 29 OPEN occurrences and Gate ERROR; no server FP transition is stored. C++20/C++23 PR contexts must be verified after hosted analysis. Historical master findings remain separate.

## Remaining risks

Local contract success cannot prove hosted PR routing or a passing gate. The regular SSH receiver advertises `allowed_mutations=[]`; individually justified server decisions still require an existing authorized write session. No access restriction is bypassed.

## Checks not run and rationale

Final-head hosted analyses and the full regression with 92 host executions, 237 affected methods, 88 reader methods, Go/vet/native/CRS/CodeQL are not claimed here: they require the final committed and published pair. The full acceptance campaign remains `NOT_RUN`; both PRs remain Draft and no merge is authorized.

## Final diff and review status

The focused workflow diff removes only the incorrect branch-routing arguments. Documentation records the resulting context contract. The final report and PR descriptions must reconcile actual delivery, validation and remaining blockers; this record does not assert the SonarCloud zero goal is achieved.
