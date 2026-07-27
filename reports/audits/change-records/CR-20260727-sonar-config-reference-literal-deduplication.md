# Change Record: Parent connector-config-reference literal deduplication and SonarQube Cloud S3358 follow-up

**Language:** English | [Deutsch](CR-20260727-sonar-config-reference-literal-deduplication.de.md)

## Identity

| Field | Value |
| --- | --- |
| Change ID | CR-20260727-sonar-config-reference-literal-deduplication |
| Date (UTC) | 2026-07-27 |
| Base revision | 1b0f8825f3510b99b603bb6cd6f0777e1710358e |
| Tracking | Parent PR #131: SonarQube Cloud python:S1192 Code Smells: 69 current OPEN receipt keys in ci/checks/documentation/connector_config_reference.py; its initial exact PR-head analysis reported Quality Gate `OK` with zero new duplication and one new task-owned `python:S3358` issue at ci/checks/documentation/connector_config_reference.py:3495. |
| Boundary | Parent configuration-reference generator/checker, this English/German Change Record pair, their indexes, and the local `python:S3358` follow-up. Generated configuration-reference files, connector or runtime behavior, Framework, MRTS, Gitlinks, workflows, SonarQube Cloud configuration, Quality Gates, suppressions, and external issue state remain unchanged. PR #131 remains Draft; no merge has occurred. |

## Motivation and problem statement

The current SonarQube Cloud receipt inventory reports 69 open python:S1192
findings in the Parent connector-configuration reference generator. Repeated
schema labels, source paths, explanatory text, and option identifiers make
the source harder to maintain while carrying no distinct behavior.

The initial exact head of Draft PR #131 received a SonarQube Cloud Quality Gate
`OK` with zero new duplication, but it also reported one new task-owned
`python:S3358` issue at
ci/checks/documentation/connector_config_reference.py:3495. The reported
nested conditional is a required local follow-up, not an accepted Quality-Gate
exception. The initial remote result cannot establish the status of the later
locally corrected candidate.

## Acceptance criteria

- Address exactly the 69 receipt-backed python:S1192 occurrences in
  connector_config_reference.py through semantically identical module-local
  constants.
- Replace the nested conditional reported as `python:S3358` at
  ci/checks/documentation/connector_config_reference.py:3495 with equivalent
  normal conditional logic, without a suppression or scanner-configuration
  change.
- Preserve schema, option order, JSON or Markdown rendering, and every
  generated configuration-reference file.
- Pass the native configuration-reference generation/checker contract,
  receipt-level static audit, whitespace review, and repository
  documentation checks.
- Maintain an equivalent English/German Change Record pair and do not claim
  any SonarQube Cloud issue closed or a clean post-correction result before a
  new exact changed-candidate-head analysis.

## Implementation decision and rationale

Only repeated, byte-identical values are named once at module scope and used
at their existing call sites. The extraction, YAML handling, renderer order,
default values, diagnostics, and generator output contracts remain unchanged.
No generated document is edited directly.

After the initial PR #131 analysis, the local follow-up gives the source path
and localized label explicit names, selects a link or code-formatted path with
an ordinary `if`/`else`, and then assembles the same source-example line. It
replaces the reported nested conditional without a SonarQube Cloud suppression,
Quality-Gate change, or scanner-configuration change. No fresh remote analysis
has been observed for that locally changed candidate.

## Changed files

- ci/checks/documentation/connector_config_reference.py
- reports/audits/change-records/CR-20260727-sonar-config-reference-literal-deduplication.md
- reports/audits/change-records/CR-20260727-sonar-config-reference-literal-deduplication.de.md
- reports/audits/change-records/README.md
- reports/audits/change-records/README.de.md

## Commands executed

The following local commands are confirmed evidence for the initial S1192
candidate before the `python:S3358` follow-up. They are not represented as
post-correction source-validation evidence.

- rtk proxy make check-connector-config-reference
- Receipt-backed AST literal audit for the 69 current python:S1192 keys
- rtk proxy git diff --check
- rtk proxy env PYTHONDONTWRITEBYTECODE=1 make check-bilingual-docs
- rtk proxy env PYTHONDONTWRITEBYTECODE=1 make check-doc-links

Documentation-only validation for this record update used:

- rtk proxy env PYTHONDONTWRITEBYTECODE=1 make check-bilingual-docs
- rtk proxy git diff --check

The isolated task worktree initializes the Parent-recorded Framework Gitlink
only as a documentation-check dependency. No Framework source, Parent
Gitlink, Framework branch, or Framework pull request changes.

## Tests and actual results

| Command or check | Result |
| --- | --- |
| Configuration-reference generation/checker (initial S1192 candidate) | passed: 21 generated files are current; the checker passed apache=14, nginx=18, haproxy=41, envoy=141, traefik=71, lighttpd=19, common=25, engine=12. This is not claimed as post-`python:S3358` correction evidence. |
| Receipt-backed AST literal audit (initial S1192 candidate) | passed: receipt_issues=69 and all_literals_singleton. This is not claimed as post-`python:S3358` correction evidence. |
| git diff --check (initial S1192 candidate) | passed: no whitespace error. This is not claimed as post-`python:S3358` correction evidence. |
| Direct source-diff review (initial S1192 candidate) | passed: only byte-identical module-local constants and direct uses changed in the scoped generator. This predates the later normal conditional correction. |
| make check-bilingual-docs (initial S1192 candidate) | passed: bilingual docs ok. This is not claimed as post-`python:S3358` correction evidence. |
| make check-doc-links (initial S1192 candidate) | passed: repository path references: PASS and doc links ok. This is not claimed as post-`python:S3358` correction evidence. |
| Documentation-only make check-bilingual-docs (this record update) | passed: bilingual docs ok. This validates the paired documentation only; it does not validate the local `python:S3358` source correction or a changed remote SonarQube Cloud head. |
| Documentation-only git diff --check (this record update) | passed: no whitespace error in the candidate diff. This is not source or remote-analysis evidence. |
| Initial exact Draft PR #131 SonarQube Cloud analysis | observed: Quality Gate `OK` with zero new duplication, but one new task-owned `python:S3358` issue at ci/checks/documentation/connector_config_reference.py:3495. This is not a clean exact-head result. |
| Local `python:S3358` follow-up | applied locally: the nested conditional was replaced with the normal conditional construction described above; no post-correction remote analysis is recorded. |
| Post-correction SonarQube Cloud analysis | not_run: no analysis for the changed candidate head has been observed. |

## Security impact

The focused security assessment is not_applicable. This is an
output-equivalent configuration-documentation generator refactor; it changes
no runtime path validation, network, subprocess, connector, credential,
permission, or security control. No security finding is claimed fixed.

## Documentation status

The initial native configuration-reference check confirms that all 21 generated
files were current before the `python:S3358` follow-up. This paired Change
Record now distinguishes that initial S1192 evidence from the local normal
conditional correction. The completed initial repository documentation checks
reported bilingual docs ok, repository path references PASS, and doc links ok;
they are not a claim about the changed candidate head.

## Runtime evidence

No connector, host, protocol, or production runtime behavior changed or is
claimed. The generator/checker verification is source and documentation
evidence, not runtime evidence.

## Known limitations

SonarQube Cloud analyzed the initial exact Draft PR #131 head, but that
analysis reported the task-owned `python:S3358` follow-up despite Quality Gate
`OK` and zero new duplication. The later locally corrected candidate has not
received a changed-head analysis. The 69 current findings and the S3358 status
can be resolved only by a fresh analysis of the exact delivered head.

## Remaining risks

A mistaken extraction or the normal conditional rewrite could alter a rendered
option, diagnostic, link, or label. The initial native generation/checker
evidence lowers the extraction risk, but a fresh exact-head analysis and
post-correction source validation remain required before a clean result is
claimed.

## Checks not run and rationale

- A fresh SonarQube Cloud analysis and GitHub CI result for the locally changed
  post-`python:S3358` candidate are not_run: no changed-head remote analysis
  has been observed. The initial Draft PR #131 result applies only to its
  initial exact head.
- Connector builds, host configuration checks, runtime smokes, protocol
  matrices, Framework checks, and MRTS checks are not applicable because no
  connector/runtime implementation or cross-repository source changed.
- No merge or Parent `master` update has occurred. PR #131 remains Draft, and
  later delivery evidence will be recorded only from observed results for its
  changed head.

## Delivery status

PR #131 remains Draft. Its initial exact head has the observed SonarQube Cloud
result recorded above: Quality Gate `OK`, zero new duplication, and one
task-owned `python:S3358` follow-up. The normal nested-conditional correction
is local, with no observed subsequent remote analysis. No merge or Parent
`master` update is claimed.

## Final diff and review status

The Draft PR #131 history contains the configuration-reference literal
deduplication and its required bilingual traceability material; the local
candidate additionally contains the normal `python:S3358` conditional
correction and this synchronized record update. The only observed remote
SonarQube Cloud result belongs to the initial exact PR head and must not be
treated as evidence for the changed candidate. The authoritative Parent
checkout, Framework source, MRTS source, Parent Gitlink, scanner controls,
and external SonarQube Cloud configuration remain unchanged; PR #131 is Draft
and unmerged.
