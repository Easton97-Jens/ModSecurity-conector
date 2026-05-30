# TODO - New Connector From Template

Status: partially suitable

Template evaluation: partially suitable

Reason: the template now describes a repeatable connector flow, but it is still
not an implementation. Origin, metadata, build, runtime, CRS, and promotion
evidence must be provided by each concrete connector.

Legend:

- [x] done / backed by template files
- [ ] open / must be answered for a concrete connector
- [ ] blocked / cannot be checked without connector source, build artifacts,
      or runtime setup
- [ ] not verified / no sufficient runtime evidence

Status vocabulary:

- `template`: generic starting point, not an implementation.
- `scaffolded`: structure exists, no repository-backed adapter implementation
  is proven.
- `adapter-owned`: productive connector code lives in the connector tree with
  provenance and metadata.
- `runtime-smoke-verified`: only specific smoke cases with recorded command and
  result are verified.
- `crs-verified`: With-CRS target or case claim has recorded command, CRS
  evidence, and result.
- `partial`: structure or partial runtime evidence exists, but full validation
  is not proven.
- `not-verified`: insufficient runtime evidence.

## Phase 0: Scaffold erstellen

Status: partially complete for the generic template.

- [x] `README.md` vorhanden.
- [x] `TODO.md` vorhanden.
- [x] `docs/architecture.md` vorhanden.
- [x] `docs/build.md` vorhanden.
- [x] `docs/validation.md` vorhanden.
- [x] `docs/coverage-decision-matrix.md` vorhanden.
- [x] `harness/README.md` vorhanden.
- [x] `src/README.md` vorhanden.
- [x] Lokaler Template-Testordner ist entfernt.
- [x] Template warnt, dass es keine produktive Implementierung ist.
- [ ] Connector-name-specific placeholders replaced.
- [ ] No runtime claims added during scaffold creation.

## Phase 1: Origin/Metadata belegen

Status: open for each concrete connector.

Metadata checklist:

- [ ] `metadata.*` angelegt.
- [ ] Connector-Name eindeutig.
- [ ] Upstream-Projekt/Version dokumentiert.
- [ ] Build-Modus dokumentiert.
- [ ] Maintainer/Ownership dokumentiert.

Origin/license checklist:

- [ ] `ORIGIN.md` angelegt.
- [ ] Upstream-Quelle dokumentiert.
- [ ] Lizenz dokumentiert.
- [ ] importierte Dateien dokumentiert.
- [ ] lokale Änderungen dokumentiert.
- [ ] `SOURCE_MAP.json` or equivalent provenance file completed.

Blocked until evidence exists:

- [ ] Do not mark `adapter-owned` until source, build, metadata, and origin
      evidence exist.
- [ ] If a source, license, or version is missing, write
      `Nicht im Repository gefunden`.

## Phase 2: Build integrieren

Status: blocked until a concrete connector build exists.

Build checklist:

- [ ] Build-Command dokumentiert.
- [ ] Include-Pfade dokumentiert.
- [ ] Library-Pfade dokumentiert.
- [ ] Build-Artefakte dokumentiert.
- [ ] Build-Log-Pfad dokumentiert.
- [ ] Clean/refresh behavior documented.
- [ ] External dependency version/pin documented when found.

Blocked items:

- [ ] Server module/plugin SDK identified.
- [ ] Build output remains below documented `BUILD_ROOT`.
- [ ] Reproducible local build command exits 0.
- [ ] Compiler/linker logs reviewed.

## Phase 3: No-CRS Runtime validieren

Status: not verified for the template.

- [ ] `make test-no-crs` ausgeführt, if the target exists.
- [ ] Connector-specific smoke target executed, if present.
- [ ] Command, exit code, and environment documented.
- [ ] PASS/FAIL/BLOCKED counts documented.
- [ ] Summary JSON paths documented.
- [ ] `phase1_header_block` or equivalent Phase 1 case documented.
- [ ] Request-body blocking documented.
- [ ] Response-header blocking documented, when framework-supported.
- [ ] Negative/pass-through case documented.
- [ ] Audit/log evidence documented.

No-CRS PASS must not be used as With-CRS PASS.

## Phase 4: With-CRS Runtime validieren

Status: not verified for the template.

- [ ] `make test-with-crs` ausgeführt, if the target exists.
- [ ] CRS source path documented.
- [ ] CRS runtime preamble path documented.
- [ ] CRS loaded/effective evidence documented.
- [ ] CRS-specific case result documented.
- [ ] PASS/FAIL/BLOCKED counts documented.
- [ ] Summary JSON paths documented.
- [ ] Cases with No-CRS/With-CRS expectation differences documented as
      variant-specific expectations.

Do not change a base No-CRS expectation to satisfy a With-CRS result.

## Phase 5: Coverage Matrix ausfüllen

Status: not verified for the template.

- [ ] Framework cases present column completed.
- [ ] No-CRS status column completed.
- [ ] With-CRS status column completed.
- [ ] Evidence path column completed.
- [ ] Decision column completed.
- [ ] Phase 1 row completed.
- [ ] Phase 2 row completed.
- [ ] Phase 3 row completed.
- [ ] Phase 4 row completed.
- [ ] RESPONSE_BODY gate completed.
- [ ] Negative/pass-through gate completed.
- [ ] Audit/log gate completed.
- [ ] Startup/reload validation gate completed.
- [ ] Promotion gate completed.

Generated coverage is planning evidence. It is not runtime proof by itself.

## Phase 6: Promotion prüfen

Status: blocked until runtime evidence exists.

- [ ] `scaffolded`: structure and docs exist, no runtime claims.
- [ ] `adapter-owned`: source/build/metadata/origin evidence exists.
- [ ] `runtime-smoke-verified`: current No-CRS and connector smoke PASS for
      the claimed scope, with command and result paths.
- [ ] `crs-verified`: current With-CRS PASS for the claimed scope, CRS
      evidence, and CRS-specific expectations documented.
- [ ] `more-than-partial`: full minimum matrix documented with no open
      FAIL/BLOCKED rows.

More than `partial` requires:

- [ ] No-CRS PASS.
- [ ] With-CRS PASS.
- [ ] Phase 1/2/3/4 minimum matrix PASS.
- [ ] Negative/pass-through PASS.
- [ ] Audit/log evidence present.
- [ ] RESPONSE_BODY blocking verified, or explicitly documented as unsupported
      or known gap with evidence.
- [ ] Startup/reload validation documented.

## Phase 7: Offene Gaps dokumentieren

Status: open for each concrete connector.

- [ ] Missing upstream/source/license evidence documented.
- [ ] Missing metadata documented.
- [ ] Missing build evidence documented.
- [ ] Missing No-CRS evidence documented.
- [ ] Missing With-CRS evidence documented.
- [ ] Any FAIL/BLOCKED row documented without reclassifying it as PASS.
- [ ] RESPONSE_BODY blocking remains `not-verified` until minimum evidence
      exists.
- [ ] Unsupported behavior documented with evidence.

## External tests

- [x] Local Template tests folder removed.
- [x] New connectors must not create `connectors/<name>/tests`.
- [x] Executable tests are framework-owned.
- [x] Framework test paths documented:
      `modules/ModSecurity-test-Framework/tests/cases/`,
      `modules/ModSecurity-test-Framework/tests/cases/connector-specific/<connector>/`,
      `modules/ModSecurity-test-Framework/tests/runners/case_cli.py`.

## Full evaluation

The complete Template evaluation is documented in:

```text
reports/template-verification-nginx-apache/template-evaluation.md
```
