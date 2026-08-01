# FND-PARENT-0065 — Body-processor metadata can read an out-of-root request body through an artifact-derived case ID

## Identity

| Field | Value |
| --- | --- |
| ID | \`FND-PARENT-0065\` |
| Category | \`security_validated\` |
| Repository / ownership | Parent / Parent |
| Priority / severity / confidence | P2 / low / validated |
| Status / feasibility | \`fixed\` / \`feasible_now\` |
| Release blocker / security relevant | false / true |
| Connector / profile | NGINX branch validated; body-processor analysis generated report |

## Summary

At Parent source revision \`9f23ae2c5fe908cef38f203be03f93fda75a8dd7\`,
a controlled pre-fix NGINX probe proved that an artifact-derived \`case_id\` of
\`../../../outside\` can move the generated request-body candidate outside the
configured safe root. \`request_body_bytes()\` then read the external
\`conf/request-body.bin\` sentinel and emitted its preview and matching SHA-256,
while the legitimate in-root control remained readable. The probe does not
establish an external content disclosure through \`generated_body_length()\`.

## Observed and expected behavior

\`generated_config_path()\` concatenates \`entry["case_id"]\` into a path derived
from a safe evidence file. On the validated NGINX branch,
\`request_body_bytes()\` then reads
\`config_path.parent / "request-body.bin"\` directly, without first routing the
derived path through \`safe_existing_file()\`; this is the confirmed
content-read/disclosure sink. \`generated_body_length()\` also constructs the
candidate and makes an unguarded \`is_file()\` probe, but its later
\`read_text()\` path already applies safe-root gating before content is read.

The safe-root containment invariant must hold after every artifact-derived path
segment is resolved. An external derived body must be rejected and use the
already supported request-body fallback instead. The repair must not broaden
safe roots or weaken report-path validation.

## Impact, source-to-sink path, and preconditions

\`\`\`text
artifact record case_id -> generated_config_path -> config_path.parent /
request-body.bin -> request_body_bytes() direct read_bytes() -> body preview / SHA-256
\`\`\`

The filename is fixed to \`conf/request-body.bin\`; the probe chooses only its
parent through the traversal-bearing \`case_id\`. A party must be able to supply
such an artifact record, the selected out-of-root parent must contain a regular
readable file at that exact suffix, and \`case_metadata()\` must reach
\`request_body_bytes()\` for the record. Evidence and case paths themselves
remained inside the configured safe root in the proof.

This is a bounded CI report-read boundary violation. It does not establish a
normal hosted-CI attacker path, arbitrary filename read, file write, code
execution, secret exposure, or external report publication. No release blocker
or risk acceptance is claimed.

## Reproduction and baseline evidence

The retained controlled pre-fix probe used the Parent \`.venv\` with
\`PYTHONNOUSERSITE=1\`, \`PYTHONDONTWRITEBYTECODE=1\`, task-owned \`TMPDIR\`, and
task-owned \`PYTHONPYCACHEPREFIX\`:

\`\`\`sh
rtk proxy env PYTHONNOUSERSITE=1 PYTHONDONTWRITEBYTECODE=1 \
  TMPDIR=<task-tmp> PYTHONPYCACHEPREFIX=<task-pycache> \
  /root/git/ModSecurity-conector/.venv/bin/python -B \
  artifacts/03_validation/pre_fix_body_processor_path_probe.py
\`\`\`

It exited \`0\`. The retained result reports \`vulnerability_reproduced:true\`;
\`traversal_preview\` is \`outside-root-sentinel\` and its SHA-256 equals
\`outside_sha256\` (\`afeb199d897b997c4b32330b4fa18c6ae6694cd153edd9ddacabb6bcfbfa2c2b\`).
The legitimate preview remains \`legitimate-in-root-body\`. No raw request body
is retained.

The focused regression was intentionally run before the source fix and exited
\`1\`: it expected \`fallback-body\` but received the out-of-root sentinel. That
proves the real \`case_metadata()\` report-generation boundary rather than only a
helper-level source pattern.

| Field | Value |
| --- | --- |
| Run | \`20260729-parent-ci-sonar-remediation\` |
| Baseline source | \`9f23ae2c5fe908cef38f203be03f93fda75a8dd7\` |
| Pre-fix result | \`/var/tmp/codex/ModSecurity-conector/runs/20260729-parent-ci-sonar-remediation/evidence/security-diff-ci-a-9f23ae2-20260729T074736Z/artifacts/03_validation/pre_fix_body_processor_path_probe.result.json\` |
| Pre-fix SHA-256 | \`1ac99356e987dc8a95f5715ec508da16b1007cfbc93f31e4c48bdd2485cdc826\` |
| Regression failure | \`.../artifacts/03_validation/focused_regression_failure.md\` |
| Regression SHA-256 | \`5deb32d93b42a4b71ec6fe7cb19e927c4c544a9d576685f61708c15b75512392\` |

## Local candidate evidence, deliberately not a status change

The local candidate routes the body candidate through \`safe_existing_file()\`.
Its retained post-fix probe reports \`vulnerability_reproduced:false\`; both the
traversal and symlink variants fall back to \`fallback-body\`, while the
legitimate in-root control remains readable. Its result SHA-256 is
\`1dcce56a4de6b03f63d1b459d865211eb39fc5a93fa3f2cda2d13a8dbb6a223a\`.

The retained final local diff review has SHA-256
\`a2904a5561dca0fd7646f27b0987baf64ba84fc39dd4c33e74c86466fa86e5ad\` and
reports no remaining changed-path candidate. These are local remediation
evidence only. They do not make the record \`fixed\` or \`verified\`, and they do
not establish PR, hosted exact-head, merge, or master evidence.

## Root cause and remediation direction

The generator validates artifact evidence and the case file through
\`safe_existing_file()\`, but treats the artifact-derived \`case_id\` as a path
component and then constructs the sibling body candidate without reapplying that
control. \`request_body_bytes()\` directly reads that candidate;
\`generated_body_length()\` makes an unguarded \`is_file()\` probe before its
separately gated \`read_text()\` call.

Make both \`generated_body_length()\` and \`request_body_bytes()\` resolve
\`config_path.parent / "request-body.bin"\` through \`safe_existing_file()\`
before inspection or read. Add focused negative coverage for a traversal-bearing
\`case_id\` and an in-root \`request-body.bin\` symlink that resolves outside,
together with an in-root control and fallback body control. Do not change
scanner rules, exclusions, suppressions, Quality Gates, report-output
containment, or allowed-root policy.

## Acceptance criteria and validation plan

1. The original \`../../../outside\` reproduction no longer returns an external
   preview or SHA-256.
2. A traversal-bearing \`case_id\` and an in-root \`request-body.bin\` symlink
   resolving outside cannot cause \`request_body_bytes()\` to disclose content
   outside configured safe roots; both body helpers consistently reject the
   derived candidate.
3. A legitimate in-root \`request-body.bin\` keeps its existing metadata.
4. Missing or rejected generated body files preserve fallback request-body
   behavior.
5. Focused tests, Python compilation, and an exact-diff security review pass
   without control weakening.

The next verification must rerun the original proof (or an equivalent focused
test) against the repaired source, then its legitimate in-root and in-root
symlink-resolving-outside controls through the same \`case_metadata()\` boundary.

## Dependencies, deduplication, and residual risk

There are no external dependencies or blockers for a Parent-only repair.
\`FND-PARENT-0026\` is related but distinct: it concerns broad caller-controlled
runtime roots. Archived \`FND-PARENT-0034\` is also distinct: it concerns
report-publication writes and symlink clobbering, not this bounded read path.

Until a repair is verified, the baseline permits the bounded external read
described above. This record claims no normal hosted-CI attacker reachability,
secret exposure, risk acceptance, PR, delivery, merge, or master result.

## History

- \`2026-07-29T08:11:35Z\`: controlled pre-fix safe-root bypass reproduced.
- \`2026-07-29T08:11:35Z\`: local candidate control and final diff review retained
  without changing the finding from \`validated\`.
