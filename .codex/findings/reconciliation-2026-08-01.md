# Finding reconciliation — 2026-08-01

**Language:** English | [Deutsch](reconciliation-2026-08-01.de.md)

## Scope and evidence boundary

This register is the current, read-only reconciliation of every canonical
active finding in `.codex/findings/` at `2026-08-01T17:36:54Z`. It covers 80
canonical triplets and preserves the reserved, empty legacy directory
`FND-PARENT-0032`. The existing archive was checked for collisions,
regular-file safety, and its 300-member checksum manifest; it is not
retroactively rewritten under this task.

The initial Parent evidence snapshot was `origin/master`
`d7dfbc505b5aa0adf22d10d8517a518ff05b95be` (PR #226). Before staging, the
current Parent baseline advanced through PR #228 to PR #227,
`522e791c1efa21da6101f9a0908d5e185736b518`, then through test-only PR #229 to
the current `origin/master` `59aba762f2d852fd917079ca8519e4ea7f49169c`.
PR #229 changes 29 test modules, including the generated-report evidence suite;
the targeted current-base controls were rerun after the rebase. PR #228 changes
only the Parent→Framework gitlink to `5cb371949ceafec6685cf716ba50a75d0f448bd1`;
its Framework snapshot changes only CodeQL workflow/lock files and retains
Framework→MRTS at `615b13bacbd008562c17408246c41ab27dca3104`. PR #227
intentionally retires individual historical Change Records while retaining
Git-history/commit/PR traceability; no Finding Markdown link targets a retired
report. Parent, Framework, and MRTS remained in separate ownership boundaries,
and this task changed no Gitlink.

The action labels use the repository lifecycle vocabulary. `fixed` means a
merged root-cause change is present but one or more current acceptance controls
remain absent; it is not treated as archive eligibility. `ARCHIVE` is used only
where the original PR/closure, default-branch reachability, current source or
scanner evidence, legitimate control, and no contradictory open task-specific
scanner signal were established.

Fresh remote evidence: PRs and commits were checked against the correct
repository and current default branch; GitHub has no open Code Scanning, secret
scanning, Dependabot, or security-advisory alert. The default-branch Sonar
Quality Gate is `ERROR` because of the separately active `FND-SONAR-0001`
security-rating condition (not a pass substitute). This documentation task's
final PR must separately obtain an exact-head green Sonar analysis.

## Per-finding decision matrix

| Finding | Prior status | Determined status / action | Archive | Evidence or remaining blocker |
| --- | --- | --- | --- | --- |
| FND-CROSS-0001 | validated | validated · UPDATE_EVIDENCE | no | 58 stale and 9 SHA-mismatch assessment entries; retained governance artifacts absent. |
| FND-CROSS-0002 | validated | validated · UPDATE_EVIDENCE | no | No fresh canonical JSON receipt or attributable remediation PR. |
| FND-CROSS-0003 | blocked | blocked · KEEP_UNCHANGED | no | No isolated restart/port-release matrix evidence. |
| FND-CROSS-0004 | blocked | blocked · KEEP_UNCHANGED | no | No current external-copy CRS Allow/Block profile evidence. |
| FND-CROSS-0005 | blocked | blocked · KEEP_UNCHANGED | no | Dependent cross-repository and scanner prerequisites remain unresolved. |
| FND-CROSS-0007 | fixed | fixed · UPDATE_EVIDENCE | no | Claimed commits are gitlink updates, not an attributable policy-fix PR. |
| FND-CROSS-0008 | in_progress | fixed · UPDATE_STATUS_AND_EVIDENCE | no | #74 root fix exists; retained runtime/terminal artifact proof is absent. |
| FND-FRAMEWORK-0007 | blocked | blocked · UPDATE_EVIDENCE | no | Finalizer source exists, but no raw lifecycle/Allow-Block receipt. |
| FND-FRAMEWORK-0009 | blocked | blocked · UPDATE_EVIDENCE | no | H2 source support is not a retained NGINX H2 runtime result. |
| FND-FRAMEWORK-0057 | blocked | fixed · UPDATE_STATUS_AND_EVIDENCE | no | Framework #51 and Parent #126/#74 are merged; Parent runtime proof is absent. |
| FND-HOST-0003 | blocked | blocked · UPDATE_EVIDENCE | no | NGINX is unavailable and no service/harness runtime was started. |
| FND-HOST-0006 | blocked | blocked · UPDATE_EVIDENCE | no | sqlite3 headers/pkg-config remain unavailable; no authorized rebuild. |
| FND-MRTS-0001 | blocked | blocked · UPDATE_EVIDENCE | no | Read-only MRTS tip is clean, but no external-copy Allow/Block profile ran. |
| FND-MRTS-0002 | fixed | fixed · UPDATE_EVIDENCE | no | Marker remains; validator passes, but its regression suite currently fails 1/30. |
| FND-PARENT-0002 | triaged | triaged · UPDATE_EVIDENCE | no | Historical ShellCheck diagnostics lack a fresh equivalent rerun. |
| FND-PARENT-0003 | triaged | triaged · UPDATE_EVIDENCE | no | Historical Staticcheck diagnostics lack a fresh equivalent rerun. |
| FND-PARENT-0005 | validated | fixed · UPDATE_STATUS_AND_EVIDENCE | no | #74 deadline fix is merged; current timeout control was not replayed. |
| FND-PARENT-0006 | validated | validated · UPDATE_EVIDENCE | no | NGINX still retains only the configured body prefix. |
| FND-PARENT-0007 | validated | validated · UPDATE_EVIDENCE | no | Traefik has no maximum worker-admission bound. |
| FND-PARENT-0008 | fixed | fixed · UPDATE_EVIDENCE | no | #183 is merged; current compiler-warning control was not rerun. |
| FND-PARENT-0009 | triaged | triaged · UPDATE_EVIDENCE | no | No fresh production artifact linker-hardening scan. |
| FND-PARENT-0010 | blocked | blocked · UPDATE_EVIDENCE | no | HAProxy contract still expressly forbids capability promotion. |
| FND-PARENT-0011 | blocked | blocked · UPDATE_EVIDENCE | no | Envoy remains partial/minimal; no promotion authority. |
| FND-PARENT-0013 | blocked | blocked · UPDATE_EVIDENCE | no | Same-UID final-unlink race lacks a hostile race harness. |
| FND-PARENT-0014 | blocked | blocked · UPDATE_EVIDENCE | no | Storage final-leaf replacement window remains untested. |
| FND-PARENT-0015 | blocked | blocked · UPDATE_EVIDENCE | no | UDS readiness-to-dial peer-identity rebinding control is absent. |
| FND-PARENT-0020 | verified | fixed · UPDATE_STATUS_AND_EVIDENCE | no | #51 is reachable but current native middleware control was not rerun. |
| FND-PARENT-0021 | blocked | blocked · KEEP_UNCHANGED | no | Storage helper fails closed; corrective control-plane work is out of scope. |
| FND-PARENT-0026 | fixed | fixed · UPDATE_EVIDENCE | no | #58 root confinement is present; current negative runtime-path control is absent. |
| FND-PARENT-0028 | triaged | triaged · UPDATE_EVIDENCE | no | Pinned outer actions still reference mutable inner Docker tags. |
| FND-PARENT-0029 | in_progress | closed · ARCHIVE | yes | #56 merge `a73c335…`, current canonical return, two current controls pass, original Sonar key resolved. |
| FND-PARENT-0032 | reserved | reserved · KEEP_UNCHANGED | no | Deliberately empty legacy directory in the structure manifest. |
| FND-PARENT-0036 | fixed | fixed · KEEP_UNCHANGED | no | Strongest ASan/allocator replay remains unavailable. |
| FND-PARENT-0039 | in_progress | closed · ARCHIVE | yes | #65 closure merge `1fa024ca…`; #227 retired the corrected records, so stale wording is no longer published; exact PR checks green. |
| FND-PARENT-0042 | blocked | blocked · UPDATE_EVIDENCE | no | #55 is closed unmerged; tag archive source remains in current code. |
| FND-PARENT-0043 | blocked | blocked · KEEP_UNCHANGED | no | Native Apache/APR/LibModSecurity sanitizer run remains absent. |
| FND-PARENT-0046 | triaged | triaged · UPDATE_EVIDENCE | no | Current Python-version regex remains semantically incorrect. |
| FND-PARENT-0047 | verified | closed · ARCHIVE | yes | #90 merge `ad953cd…`; fixed Go selector unchanged and exact PR checks green. |
| FND-PARENT-0048 | in_progress | closed · ARCHIVE | yes | #92 merge `95fb491…`; locked install and current quick-check workflow succeeded. |
| FND-PARENT-0050 | in_progress | fixed · UPDATE_STATUS_AND_EVIDENCE | no | #74 root source change exists; full producer/cross-repository validation missing. |
| FND-PARENT-0052 | in_progress | fixed · UPDATE_STATUS_AND_EVIDENCE | no | #74 strict immutable EXPAT path exists; full producer validation missing. |
| FND-PARENT-0053 | in_progress | fixed · UPDATE_STATUS_AND_EVIDENCE | no | #74 literal PCRE2 hash path exists; terminal producer gate missing. |
| FND-PARENT-0054 | verified | in_progress · UPDATE_STATUS_AND_EVIDENCE | no | The historical bounded diagnostic commit `b28b874…` is not reachable from current master; the current lightweight workflow explicitly excludes that strict-producer path. |
| FND-PARENT-0055 | verified | blocked · UPDATE_STATUS_AND_EVIDENCE | no | Referenced files lack authorized-removal or replacement provenance. |
| FND-PARENT-0056 | in_progress | fixed · UPDATE_STATUS_AND_EVIDENCE | no | #74/#126 source and gitlink evidence exists; strict producer replay absent. |
| FND-PARENT-0057 | in_progress | in_progress · UPDATE_EVIDENCE | no | Staging-root repair is not present on current master. |
| FND-PARENT-0058 | in_progress | fixed · UPDATE_STATUS_AND_EVIDENCE | no | #74 port-plan source fix remains; full matrix/hosted replay absent. |
| FND-PARENT-0059 | in_progress | fixed · UPDATE_STATUS_AND_EVIDENCE | no | #74 locking fix remains; retained target receipt/hosted run absent. |
| FND-PARENT-0060 | fixed | fixed · UPDATE_EVIDENCE | no | #74 FIFO fix and test exist; current control replay absent. |
| FND-PARENT-0061 | fixed | fixed · UPDATE_EVIDENCE | no | #74 wrapper/FD control exists; current runtime replay absent. |
| FND-PARENT-0062 | validated | validated · KEEP_UNCHANGED | no | Current governance-job mismatch reproduces. |
| FND-PARENT-0063 | validated | validated · REQUIRES_USER_DECISION | no | Release provenance policy needs an owner choice. |
| FND-PARENT-0064 | verified | verified · UPDATE_EVIDENCE | no | #183 and focused harness pass; broad live-Apache closure control missing. |
| FND-PARENT-0065 | validated | fixed · UPDATE_STATUS_AND_EVIDENCE | no | #175 safe-file root fix and regressions exist; current resulting-master control absent. |
| FND-PARENT-0066 | fixed | fixed · UPDATE_EVIDENCE | no | #178 merged; original bypass not freshly rerun. |
| FND-PARENT-0067 | validated | validated · KEEP_UNCHANGED | no | Independent leak root cause remains unfixed. |
| FND-PARENT-0068 | in_progress | in_progress · UPDATE_EVIDENCE | no | #183 fixes one runner; sibling root cause remains. |
| FND-PARENT-0069 | validated | validated · KEEP_UNCHANGED | no | Current C17/Werror hardening gap remains. |
| FND-PARENT-0070 | fixed | fixed · UPDATE_EVIDENCE | no | #183 source fix exists; normal APXS/DSO/HTTP control absent. |
| FND-PARENT-0071 | fixed | fixed · UPDATE_EVIDENCE | no | #183 source fix exists; live start/readiness control absent. |
| FND-PARENT-0072 | fixed | fixed · UPDATE_EVIDENCE | no | #183 PR Sonar clean; direct default-branch key readback absent. |
| FND-PARENT-0073 | fixed | verified · UPDATE_STATUS_AND_EVIDENCE | no | #182 focused controls pass; full Framework suite intentionally blocked. |
| FND-PARENT-0074 | closed | closed · ARCHIVE | yes | #213 merge `f335965…`; current root/symlink controls passed (107 tests). |
| FND-PARENT-0075 | not_applicable | not_applicable · UPDATE_EVIDENCE | no | #213 clean-history replacement is merged; formal supersession remains active. |
| FND-SONAR-0001 | blocked | blocked · UPDATE_EVIDENCE | no | Current master QG ERROR is attributed to this security-rating blocker. |
| FND-SONAR-0004 | blocked | blocked · KEEP_UNCHANGED | no | Sonar administration authority remains external. |
| FND-SONAR-0009 | blocked | blocked · UPDATE_EVIDENCE | no | Framework coverage workflow/owner configuration is still absent. |
| FND-SONAR-0016 | in_progress | in_progress · KEEP_UNCHANGED | no | Aggregated remaining items, including 0001, remain open. |
| FND-SONAR-0019 | fixed | fixed · UPDATE_EVIDENCE | no | #150 merged; current Traefik runtime revalidation absent. |
| FND-SONAR-0020 | closed | closed · ARCHIVE | yes | #197 `caddd86…`, current Sonar key CLOSED/FIXED, PR checks green. |
| FND-SONAR-0021 | closed | closed · ARCHIVE | yes | #177 `a1c839…`, current S131 key CLOSED/FIXED, PR checks green. |
| FND-SONAR-0022 | fixed | fixed · UPDATE_EVIDENCE | no | #200 source fix; global QG is not a valid resulting-master pass. |
| FND-SONAR-0023 | verified | verified · UPDATE_EVIDENCE | no | #200 key resolution; lifecycle is not a formal closure. |
| FND-SONAR-0024 | verified | verified · UPDATE_EVIDENCE | no | #200 key resolution; lifecycle is not a formal closure. |
| FND-SONAR-0025 | verified | verified · UPDATE_EVIDENCE | no | #201 merged; direct current key readback absent. |
| FND-SONAR-0026 | verified | verified · UPDATE_EVIDENCE | no | #198 key absent from master analysis; formal closure not evidenced. |
| FND-SONAR-0027 | verified | verified · UPDATE_EVIDENCE | no | #206 merged; global QG remains separately blocked. |
| FND-SONAR-0028 | verified | verified · UPDATE_EVIDENCE | no | #221 original key is currently CLOSED/FIXED, but record remains verified. |
| FND-SONAR-0029 | verified | verified · UPDATE_EVIDENCE | no | #221 original key CLOSED/FIXED; record needs schema/evidence repair first. |
| FND-SONAR-0030 | fixed | fixed · UPDATE_EVIDENCE | no | #226 merged; two current direct Sonar-key readbacks remain missing. |
| FND-SONAR-0031 | verified | verified · UPDATE_EVIDENCE | no | #225 resolved keys and controls; lifecycle remains verified. |

## Archive decision set

The seven `ARCHIVE` rows are moved losslessly with their English, German, and
JSON records. Their records are first brought to `closed` where necessary, and
the archive README and SHA-256 manifest are updated. All other canonical
findings remain active; no status is elevated solely because a PR or commit
exists.

## Validation performed during this reconciliation

- Current Parent PR/merge/default-branch reachability, GitHub Actions, CodeQL,
  Code Scanning, secret-scanning, Dependabot, and Sonar API readbacks.
- Current `python3 -B -m unittest` root/symlink controls for `FND-PARENT-0074`:
  107 tests passed.
- Current two specified `FND-PARENT-0029` optional-prerequisite controls: both
  passed.
- Portable documentation links: all relative Markdown targets resolve in this
  checkout. Historical task-local evidence paths are preserved as literals,
  rather than nonportable absolute hyperlinks or invented replacement targets;
  this includes 24 historical paths no longer present on this host.
- Read-only source/revision comparisons for all remaining records; unavailable
  runtime, native, external-copy, and retained-artifact controls are recorded
  as gaps, never as passing evidence.
