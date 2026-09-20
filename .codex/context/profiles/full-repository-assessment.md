# Full Repository Security, Quality, and Readiness Assessment

## Trigger

Use when the user requests a complete repository-wide security/quality/readiness assessment or the evidence-based 100-percent score.

## Mode

`analysis_only`

No product fixes, normal test changes, dependency changes, delivery, capability promotion, or Git writes are implied.

## Required scope

Assess:

- Parent repository integrity and architecture;
- all six connector families and ten logical profiles;
- Common SDK/runtime and phase/intervention/evidence contracts;
- Framework and MRTS integration boundaries;
- repository build/test/runtime/evidence systems;
- CI/workflow security and current read-only remote state where available;
- dependencies and supply chain;
- Python/Go/C/C++/Shell/toolchain quality boundaries;
- SonarQube and configured OpenAI security-analysis services when explicitly required and currently accessible;
- findings, code quality, technical debt, operational/readiness evidence;
- resource and cleanup integrity.

## Load

- `../command-execution-policy.md` for every local shell/project command;

- all relevant core policies from `../index.md`;
- `../security/connector-deep-assessment.md`;
- all six connector deltas;
- common security modules required by those deltas;
- `../security/quality-scoring-policy.md` when scoring is requested;
- `../security/analysis-services-policy.md` when external analysis services are requested;
- `../connector-matrix.md` when CRS/MRTS matrix completeness is in scope.

## Python assessment environment

Resolve the current repository-pinned Python requirement from the checkout. When the assessment requires a fresh isolated test environment, create it under the configured external run/tool root with the matching verified interpreter. Do not substitute another system Python merely because it is easier to invoke.

Record interpreter identity, version, origin, venv isolation, installed test-tool versions/provenance, `pip check`, actual test discovery/execution, and coverage artifacts. Do not mutate system Python, user site, repository dependency files, or pre-existing user environments.

## Assessment chain

For every applicable logical connector profile distinguish:

source/dependencies -> build -> binary/module/service -> config -> start -> readiness -> allow -> rule-based block -> P2 -> P3 -> P4 -> failure/recovery -> cleanup -> evidence validation.

No stage proves a later stage.

## Test completeness

Maintain a coverage ledger of all discovered applicable mandatory target tests/checks. Setup/prerequisite attempts have their own IDs and do not count as executed target tests. Missing applicable target results remain visible and prevent a complete assessment.

## External analysis

When required, use `analysis-services-policy.md`. OpenAI/TAC and SonarQube results are independent candidate/evidence sources and never substitute for local builds/runtime checks.

## Scoring

When requested, predeclare and calculate the 100-point score under `quality-scoring-policy.md`. Keep test completeness, test success, code coverage, Quality Gate, findings, connector readiness, and score separate.

## Durable outputs

Minimum:

- execution contract and policy resolution
- repository/tool/dependency inventories
- connector/profile coverage ledger
- build/runtime matrix
- findings inventory
- CI/supply-chain/security/quality summaries
- analysis-service reconciliation when used
- scoring spec/scorecard/validation when used
- cleanup manifest/report
- final report

Do not create dozens of empty placeholder reports. Split only when a section has substantial independent content.

## Outcome

Use repository-wide outcome vocabulary from `definition-of-done.md`. `complete` means the assessment was completely executed and reconciled, not that the product passed everything.

Every final report states: **Diese Analyse ist keine Produktionsfreigabe.**
