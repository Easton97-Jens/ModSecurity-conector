# FND-FRAMEWORK-0006 — NGINX-Archiv-Digest kann vor Framework-Provisioning unset sein

## Identität

| Feld | Wert |
| --- | --- |
| ID | `FND-FRAMEWORK-0006` |
| Kategorie | `security_validated` |
| Repository / Ownership | `framework` / `framework` |
| Priorität | `P2` |
| Severity / Confidence | `medium` / `validated` |
| Status / Machbarkeit | `fixed` / `feasible_now` |
| Release-Blocker / Security-Relevanz | `false` / `true` |

## Zusammenfassung und Auswirkung

Vor der Reparatur akzeptierte der Framework-NGINX-GitHub-Release-Archivpfad ein leeres `NGINX_SHA256`, zeichnete einen nur lokalen Hash auf und extrahierte das ausgewählte Archiv. Ersetzte Release-Bytes konnten dadurch ohne einen überprüften passenden Digest den NGINX-Build-Pfad erreichen.

Der Task-Branch verwendet jetzt standardmäßig das überprüfte offizielle
Release-Tupel `release-1.31.2`, `nginx-1.31.2.tar.gz` und SHA-256
`af2a957c41da636ddc4f883e4523c6d140b4784dbce42000c364ae5092aa473c`.
Er weist explizit leere, fehlerhafte, abweichende oder tupel-inkonsistente
Konfigurationen vor Netzwerknutzung zurück, verifiziert gecachte oder per
Refresh erneuerte Candidates, staged ein privates Archiv unter
`NGINX_BUILD_DIR`, verifiziert genau diese Extraction-Eingabe erneut und gibt
ausschließlich sie an `tar`. Die Source-Archive-Kontrolle ist lokal `fixed`; vor
`verified` oder `closed` bleibt eine Post-Merge-Verifikation erforderlich.

## Beobachtetes und erwartetes Verhalten

Der Pre-Fix-Pfad wies nicht gesetzte, nur-Whitespace-, mit nachgestelltem Whitespace versehene oder malformed Digest-Werte nicht vor Archive-Selection/Download zurück. Er verglich einen Digest nur bedingt bei Nicht-Leerheit, sodass der ausgewählte Candidate nach Aufzeichnung eines lokalen Hashes extrahiert werden konnte.

Jeder `github-release`-Candidate muss jetzt vor Latest-Resolution, Cache-Nutzung, Download, Extraction oder Build-Arbeit einen nicht leeren, syntaktisch gültigen Digest besitzen. Ein passender Digest muss sowohl den ausgewählten Candidate als auch die exakte private Archive-Eingabe für `tar` abdecken. Bei einem festen Release muss der Source-Ref dem Release-Tag entsprechen und der Asset-Name das erwartete NGINX-Release-Asset für diesen Tag sein.

## Betroffene Dateien und Symbole

- `modules/ModSecurity-test-Framework/ci/lib/common.sh` — `NGINX_SHA256`-Konfigurationsvertrag.
- `modules/ModSecurity-test-Framework/ci/provisioning/prepare-nginx-build.sh` — `validate_nginx_archive_configuration`, `resolve_nginx_release_tag`, `verify_nginx_archive_digest`, `stage_verified_nginx_archive` und `download_nginx_source`.
- `modules/ModSecurity-test-Framework/ci/tools/check-common-versions.py` —
  Release-Asset-Metadaten und No-Partial-Update-Provenance-Prüfung.
- `modules/ModSecurity-test-Framework/tests/security_regression/test_nginx_archive_digest.py` und `tests/fixtures/nginx-archive-digest/` — isolierte lokale Regression-Fixtures und Archive-Boundary-Controls.
- `modules/ModSecurity-test-Framework/tests/security_regression/test_nginx_release_provenance.py`
  — no-network Release-Metadaten-Tupel-Regression-Controls.

## Voraussetzungen und Reproduktion

1. Der Framework-`github-release`-NGINX-Source-Build-Pfad wird mit Digest-, Source-, Release-Tag-, Cache- oder Refresh-Konfiguration aufgerufen.
2. Die zurückgehaltene Assessment- und Task-Run-Evidence ist verfügbar.
3. Pre-Fix `tests.security_regression.test_nginx_archive_digest` ausführen und beobachten, dass die erforderlichen Empty-/Whitespace-/Malformed-Fail-Closed-Assertions fehlschlagen.
4. Post-Fix `rtk env TMPDIR=<task-run>/tmp python3 -B -m unittest tests.security_regression.test_nginx_archive_digest tests.security_regression.test_nginx_release_provenance -v` ausführen. Alle zwölf Fälle müssen bestehen.

## Grundursache und Remediation

Der Release-Archivpfad verglich `NGINX_SHA256` nur, wenn es nicht leer war; andernfalls zeichnete er einen lokalen Hash auf und extrahierte das Candidate-Archiv. Dies war die Framework-NGINX-Release-Archive-Integrity-Grenze.

Die Reparatur verlangt `NGINX_SHA256` vor der Preparation und erneut am Use-Point. Sie validiert feste und per `latest` aufgelöste Tags, verwendet einen vorhandenen Candidate nur ohne `REFRESH=1`, führt Refresh über einen temporären Download-Pfad aus, validiert den Candidate, staged und revalidiert eine private Kopie und extrahiert ausschließlich diese finale verifizierte Kopie. Der feste Standard bindet den überprüften offiziellen Release-Tag, Asset-Namen und veröffentlichten Release-Asset-Digest; ein explizit leerer Override bleibt fail closed.

## Evidence und Validierung

- Retained Assessment-Run `20260716T193351Z-repository-full-assessment-0cb855ad`: `.codex/reports/repository-full-assessment.md:221-227,238-244`, SHA-256 `5721a77efe2baf948a163ae0ee1d981fbba37119b89b9becdd5ccebdf99c5ed4`, Exit `0`, beobachtet `2026-07-16T22:46:50Z`.
- Retained Task-Run `20260718T092116Z-fnd-framework-0006-nginx-digest-5251a4f1`: `/var/tmp/codex/ModSecurity-conector/runs/20260718T092116Z-fnd-framework-0006-nginx-digest-5251a4f1/evidence/fnd-framework-0006-local-validation.md`, SHA-256 `dd220e8700629516ceb87c3a330b2ad6d8b9f8ebf64f010f46457ec4fa11a488`, Exit `0`, beobachtet `2026-07-18T10:15:25Z`.
- Retained Delivery-Evidence für Framework-Draft-PR [#25](https://github.com/Easton97-Jens/ModSecurity-test-Framework/pull/25): `/var/tmp/codex/ModSecurity-conector/runs/20260718T092116Z-fnd-framework-0006-nginx-digest-5251a4f1/evidence/fnd-framework-0006-delivery-blocker.md`, SHA-256 `89e9d095ee8648b7970919ae5913a5a1624590b0a14bdeb0d994721dc259d162`, Evidence-Collection-Exit `0`, beobachtet `2026-07-18T10:35:27Z`.
- Retained Release-Provenance-Fortsetzung `20260719T081017Z-framework-pr-resolution-20260719-840082e0`: offizieller Metadaten-Receipt SHA-256 `037826df6ebd25594a9b4cc7068cf72aeb804aa43672ccb6f44d8890df863c53`, direkter Asset-Verifikations-Receipt SHA-256 `d2d27b6770d7d6c345762b771e7dde3bcda021c729d8fb887aa25c739c8efcd5` sowie lokaler Validierungs-Receipt `/var/tmp/codex/ModSecurity-conector/runs/20260719T081017Z-framework-pr-resolution-20260719-840082e0/evidence/pr25-release-provenance-local-validation.md`, SHA-256 `6b448efd1ca708e7e51a74f181dc320e6115743f4d7a937492861c1f651fb2af`.

Die lokale Evidence hält eine verwundbare Baseline und das Post-Fix-Ergebnis fest. Die Post-Fix-Suite mit sieben Testmethoden deckt Empty, nur-Whitespace-, mit nachgestelltem Whitespace versehene und Malformed-Digests, Mismatch, passenden Kontrollfall, Candidate-Replacement nach dem ersten Hash, gecachte Latest-Metadaten, Release-/Source-Overrides, Revalidation vorhandener Archive und Refresh ab. Kein negativer Fall erreicht `tar`; der passende Kontrollfall erreicht es nur über `verified-archives`. Shell-Syntax, Framework-Dokumentationschecks, statischer Framework-Lint und `git diff --check` bestanden ebenfalls.

## Akzeptanzkriterien und legitime Kontrollen

- Nicht gesetzte, nur-Whitespace-, mit nachgestelltem Whitespace versehene, malformed und abweichende Digests scheitern vor der Extraction.
- Ein passender Digest ist erfolgreich und `tar` erhält ausschließlich die erneut verifizierte private Archive-Kopie.
- Latest, Source-/Release-Overrides, Cache/Refresh, vorhandene Archive und Candidate-Replacement behalten dieselbe Fail-Closed-Kontrolle.
- Passende Fixed-Tag-, Latest-Cache- und `REFRESH=1`-lokale Fixture-Kontrollen bleiben erfolgreich.
- Konfigurierter fester Tag, passender Source-Ref, erwarteter Release-Asset-Name und veröffentlichter SHA-256 bleiben ein überprüftes Tupel; ein neueres Release darf keine automatische Tag-only-Änderung erzeugen.

## Grundursachen-Triage, Abhängigkeiten und Grenzen

Die Grundursachen-Gruppe ist `RC-FW-004-nginx-archive-digest-fail-closed`; sie ist ein Singleton und nur als Archive-Integrity-Familie mit `FND-FRAMEWORK-0005` verwandt. Sie darf keinen Patch oder PR mit FND-FRAMEWORK-0005 teilen.

Dies bleibt ein Framework-only-Delivery. Draft-PR [#25](https://github.com/Easton97-Jens/ModSecurity-test-Framework/pull/25) hat übereinstimmende lokale, Remote- und PR-Head-SHA; SonarCloud und `scaffold-lint` bestanden und es gibt keinen Review-Thread. Der anwendbare `test-common`-/`common-structure`-Check ist jedoch eine bereits bestehende Baseline-Fehlerbedingung: Er erwartet 141 YAML-Fälle und findet 179, und derselbe Workflow scheitert bereits auf `master` bei `cdc91a398d6c156eaff927d742b23018a3817fb6`. Kein Parent-Gitlink-Update, Merge, MRTS-Change oder unabhängiger CI-Fix ist autorisiert.

## Blocker, Restrisiko und Disposition

Es gibt keinen lokalen Implementierungsblocker. Das Finding bleibt `fixed`, nicht `verified`: Der überprüfte Standard besitzt nun direkte Release-Asset-Digest-Evidenz, aber sein neuer PR-Head hat noch keine aktuellen externen Checks/Review oder einen Post-Merge-Current-Master-Rerun. Es wurde kein NGINX-Source-Build und keine reale Archive-Substitution versucht; deterministische lokale Archive übten die Kontrollgrenze aus. Es wurde kein Risiko akzeptiert.

## Historie

- `2026-07-17T10:43:59Z`: `bootstrap_created` — zurückgehaltene Assessment-Evidence wurde ohne Remediation oder Closure registriert.
- `2026-07-18T08:09:21Z`: `root_cause_triaged` — optionale NGINX-Digest-Enforcement wurde als unabhängig von FND-FRAMEWORK-0005 bestätigt.
- `2026-07-18T10:15:25Z`: `local_fail_closed_remediation_validated` — der Task-Branch bestand die fokussierte Suite mit sieben Testmethoden, einschließlich der Zurückweisung nachgestellten Whitespace, sowie Shell-, Dokumentations-, Lint- und Diff-Checks und hielt hash-adressierte lokale Evidence zurück; Draft-PR- und Post-Merge-Verifikation bleiben ausstehend.
- `2026-07-18T10:35:27Z`: `delivery_blocked_preexisting_ci_baseline` — Draft-PR #25 hatte die übereinstimmende lokale/Remote/PR-SHA `7a61a34ed5531f1f399a88e26e6242c7cacae412`; SonarCloud und `scaffold-lint` bestanden, und es gab keine Review-Threads. `test-common/common-structure` scheiterte jedoch am bestehenden Master-YAML-Count-Mismatch (`expected 141`, `found 179`). Der unabhängige Fix liegt außerhalb dieses Tasks, daher ist der Zustand blockiert und nicht `verified_pr`.

### Aktuelle synchronisierte Revalidierung

PR #25 wurde mit dem Framework-Master auf dem exakten Head
`c5e7553cf5f3eb7c5535e392798e03ae21f81981` synchronisiert. Die fokussierte
NGINX-Regressionssuite bestand 7/7, Shell-Syntax und der gesamte Lint liefen
erfolgreich, ebenso alle Exact-Head-Checks einschließlich common-structure,
CodeQL und SonarCloud. Der frühere YAML-Count-Blocker ist damit behoben. Die
Auslieferung bleibt blockiert, weil kein im Repository konfigurierter oder
anderweitig autorisierter, nichtleerer `NGINX_SHA256` für ein echtes
Upstream-`github-release`-Archiv vorhanden ist. Es wurde kein Digest erfunden
und die Fail-Closed-Kontrolle nicht geschwächt. Zurückgehaltene Blocker-Receipt:
`/var/tmp/codex/ModSecurity-conector/runs/20260718T192214Z-framework-pr-resolution-20260718-b30403da/evidence/pr25-current-blocker-receipt.json`
(SHA-256 `b0ac58f0ee57f215829bd185de73c09ff1221e38a5356c9270e9ec274a972e00`).

### Aktuelle Release-Provenance-Fortsetzung

Die Fortsetzung vom 2026-07-19 ersetzt die frühere Missing-Evidence-
Disposition. Sie behält die vorhandene Version `release-1.31.2`, statt sie
stillschweigend auf aktuelles `release-1.31.3` zu erhöhen, pinnt nun aber das
exakte offizielle Release-Asset und dessen veröffentlichten SHA-256. GitHubs
Tag-Metadaten lösen den annotierten Tag zu
`2fd01ed47a1fd2965754c83f53b33a789d0e07f1` auf; GitHub markiert ihn als
unsigniert. Die implementierte Integrity-Grenze ist daher der überprüfte
Release-Asset-SHA, nicht eine nicht gemachte Signaturbehauptung.

Der neue lokale Worktree bestand 12 fokussierte Archiv-/Provenance-Tests,
Shell-/Python-Syntaxchecks, den vollständigen nativen Framework-Lint,
Dokumentation, Whitespace und einen Live-Updater-Readback. Der Updater
verifizierte Asset und Digest, meldete danach neueres `release-1.31.3` als
`unknown` ohne Update-Änderungen. Damit bleibt die erforderliche atomare
Tag-/Asset-/Digest-Prüfung erhalten.

Die Auslieferung wartet nur noch auf die externen Checks/Review für den neuen
exakten Framework-PR-#25-Head und die unabhängigen Current-Master-Gates; dies
ist kein Waiver für den dynamisch fehlgeschlagenen GitHub-Advanced-Security-Run
oder `FND-SONAR-0002`.

## Historienfortsetzung

- `2026-07-19T09:15:37Z`: `release_provenance_default_locally_validated` —
  offizielle Release-Metadaten und ein direkter Asset-Digest-Vergleich
  etablierten das überprüfte Standard-Tupel; 12 Tests, Syntax-/Static-Checks,
  vollständiger nativer Lint, No-Partial-Update-Prüfung, Parent-clean und
  no-MRTS-diff bestanden. Exact-new-head-Delivery und Post-Merge-Verifikation
  bleiben ausstehend.

### Master-Integrationsfortsetzung

PR #25 wurde nach der aktuellen Exact-Head-Review ready gesetzt und am
`2026-07-19T09:50:22Z` normal per Squash gemergt. Der autoritative PR-Merge-
bzw. resultierende Framework-`master`-SHA ist
`9954b99a31fab0006cdf903ab477c8158c50fea8`; der Pre-Merge-Task-Head war
`c6ba5e11359d6eb30e8717b766d49697f9bed74f`. Die exakten Master-Runs für Lint,
test-common/common-structure und CodeQL bestanden, aber das Master-SonarCloud-
Quality-Gate schlug fehl. Dieser Check ist der unabhängig getrackte
vorbestehende `FND-SONAR-0002`-Backlog und kein Beleg, dass diese NGINX-
Kontrolle regressiert ist. Das Finding bleibt `fixed`, nicht `verified` oder
`closed`, bis die erforderliche Current-Master-Quality-Gate-Evidence vorliegt.
Parent und MRTS bleiben unverändert.

- `2026-07-19T09:52:00Z`: `pr25_squash_merged_master_gate_blocked` — exakte
  Merge- und Master-Evidence ist in
  `pr25-9954b99-post-merge-master-verification.md`, SHA-256
  `fdda0551354ccc8cb28794a1f7ca8e35f6aa333a9d6272743e15e7e12aacca34`,
  zurückgehalten.

### Direkte Stale-PR-Rückeinführungsgefahr — 2026-07-19

Der aktuelle Framework-`master` enthält bereits die überprüfte, fail-closed
Release-Tag-/Release-Asset-/nichtleere-SHA-256-Bindung. Direkte Vergleiche
zeigen, dass die veralteten ungemergten Heads #24, #26, #27 und #29 sie
entfernen und einen tag-only-Archivpfad mit bedingtem Digest-Vergleich vor der
Extraction wiederherstellen. Dies ist nur ein Merge-Blocker: `master`
`9954b99a31fab0006cdf903ab477c8158c50fea8` bleibt `fixed`, und das Finding
wird nicht wieder geöffnet.

Zurückgehaltene Evidence: Run
`20260719T081017Z-framework-pr-resolution-20260719-840082e0`,
`analysis/direct-merge-hazards.md`, SHA-256
`d28d88c9b1f034e1798cfa805d3b4e7210e3e3742dc4014d19ef78238c5c2004`;
beobachtet am `2026-07-19T12:01:55Z` durch RTK-präfixierte Direct-Diff- und
statische NGINX-Source-to-Sink-Review.
