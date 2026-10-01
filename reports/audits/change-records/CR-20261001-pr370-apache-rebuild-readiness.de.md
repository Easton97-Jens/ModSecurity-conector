# Change Record: CR-20261001-pr370-apache-rebuild-readiness

**Sprache:** [English](CR-20261001-pr370-apache-rebuild-readiness.md) | Deutsch

Eingegrenzter Parent-Folgepatch für PR #370. Neue NGINX-Arbeit und ein tatsächlicher Merge sind ausgeschlossen.

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | CR-20261001-pr370-apache-rebuild-readiness |
| Datum (UTC) | 2026-10-01 |
| Basis-Revision | `327daf723e0e6798ee82a39577ecca1077f6188d` |

## Motivation und Problemstellung

Die angeforderte Merge-Vorbereitung zeigte, dass der Apache-APXS-Wrapper sein
eigenes reguläres Profil-Registry-Staging-Verzeichnis bei einem zweiten Build
oder Wiederanlauf abwies. Ein gezielter Regressionstest reproduzierte den
Fehler. Die bisher grüne Single-Build-CI konnte ihn nicht erkennen. Dieser
Record behandelt dieses Korrekturinkrement, nicht die vollständige G1–G9-Abnahme
der neun logischen Nicht-NGINX-Profile.

## Akzeptanzkriterien

- Wiederholte Builds und Wiederanlauf nach APXS-Fehler funktionieren unter derselben externen Root.
- Gestagte Registry-Symlinks/-Artefakte werden weder vertraut noch überschrieben;
  Symlink-Kinder und Ausgaben innerhalb des Checkouts bleiben abgewiesen.
- CI führt die Containment-/Retry-Unit-Tests und zwei echte Builds ausdrücklich
  aus; ein Fehler eines Builds lässt das Gate scheitern, statt durch Retry verdeckt zu werden.
- EN/DE-Dokumentation und Traceability bleiben gleichwertig. Delivery erfordert
  frische Current-Head-CI und Sonar einschließlich 0.0% New-Code-Duplikation.
- Keine neuen NGINX-Änderungen/-Läufe, Framework-/MRTS-Source- oder Gitlink-Änderungen,
  abgeschwächten Controls, direkten `master`-Writes, Merge oder Neun-Profil-B-Hochstufung.

## Implementierungsentscheidung und Begründung

Existiert bereits eine reguläre Registry-Stage `connectors`, wird ein privates
Verzeichnis `rebuild.XXXXXX` unter der kanonischen externen Staging-Root angelegt.
Jeder Aufruf kopiert Registry-Quellen in sein frisches `connectors`-Kind.
Bisherige Registry-Eingaben/-Libtool-Artefakte werden weder gelöscht, überschrieben
noch wiederverwendet. Das Common-Source-Staging behält sein bestehendes Verhalten.
Die Bootstrap-Prüfung führt `make` zweimal mit derselben Staging-Root aus und
gibt jeden Fehler ausdrücklich weiter: `set -e` allein schützt eine Schleife
innerhalb von `if ! (...)` nicht.

## Geänderte Dateien

- `connectors/apache/build/apxs-wrapper.in`
- `tests/test_apache_apxs_profile_registry_staging.py`
- `ci/checks/connectors/apache/check-apache-autotools-bootstrap.sh`
- `.github/workflows/test-apache.yml`
- `connectors/apache/README.md` und `connectors/apache/README.de.md`
- Dieses Change-Record-Paar und `reports/audits/change-records/README.md` /
  `reports/audits/change-records/README.de.md`

## Ausgeführte Befehle

Die Befehle liefen im task-eigenen externen Parent-Worktree über RTK. Ausgaben
und temporäre Dateien nutzten die externe Task-Run-Root; kein Paket wurde installiert.

- `rtk proxy env TMPDIR=/var/tmp/codex/ModSecurity-conector/runs/pr370-ready-without-nginx-20261001/tmp PYTHONNOUSERSITE=1 PYTHONDONTWRITEBYTECODE=1 MODSECURITY_INCLUDE_DIR=/usr/include MODSECURITY_LIB_DIR=/usr/lib/x86_64-linux-gnu python3 -m unittest tests.test_apache_apxs_profile_registry_staging tests.test_apache_request_transaction_cleanup tests.test_envoy_transport_hardening_contract connectors.lighttpd.tests.test_stock_sidecar_contract -q`
  — 95 Tests bestanden mit CPython 3.14.7 und installiertem ModSecurity-SDK;
  enthält Stock-Sidecar-Loopback-Tests, keine Stock-lighttpd-Host-Abnahme.
- Die Wiederholungsbuild-Regression scheiterte vor der Wrapper-Korrektur.
  Die Bootstrap-Fehlerweitergabe-Regression scheiterte beim Erstbuild-Fehler vor
  der expliziten Fehlerbehandlung je Iteration; beide bestehen jetzt.
- `rtk proxy env TMPDIR=/var/tmp/codex/ModSecurity-conector/runs/pr370-ready-without-nginx-20261001/tmp PYTHONDONTWRITEBYTECODE=1 timeout 120s make check-common-helpers-c17 check-http-authorization-service-timeout BUILD_ROOT=/var/tmp/codex/ModSecurity-conector/runs/pr370-ready-without-nginx-20261001/build PYTHON=python3`
  — bestanden, einschließlich echter Authorization-Service- und Response-Companion-
  Lifecycle-Smokes. Dies sind keine vollständigen Connector-Host-Ergebnisse.
- `rtk proxy env TMPDIR=/var/tmp/codex/ModSecurity-conector/runs/pr370-ready-without-nginx-20261001/tmp APACHE_AUTOTOOLS_TEST_PARENT=/var/tmp/codex/ModSecurity-conector/runs/pr370-ready-without-nginx-20261001/tmp MODSECURITY_PREFIX=/usr timeout 120s make check-apache-autotools-bootstrap`
  — beide APXS-Builds erfolgreich; das Gesamtziel scheiterte vor Hoststart,
  weil lokales `chown` auf dem gemappten Dateisystem `EINVAL` lieferte. Dies
  war vor der anschließenden expliziten Schleifen-Fehlerweitergabe-Korrektur.
- `rtk proxy sh -n connectors/apache/build/apxs-wrapper.in`,
  `rtk proxy sh -n ci/checks/connectors/apache/check-apache-autotools-bootstrap.sh`
  und `rtk proxy git diff --check` — während der Implementierung bestanden;
  finaler Wiederholungslauf und Exact-Head-Hosted-Delivery-Status stehen in PR #370.
- `rtk proxy env PYTHONNOUSERSITE=1 PYTHONDONTWRITEBYTECODE=1 make check-bilingual-docs PYTHON=python3`
  — anfangs durch bestehende Framework-Links blockiert, weil das gepinnte
  Framework-Submodul im Task-Worktree nicht materialisiert war. Nach Initialisierung
  nur des unveränderten gepinnten Framework-Checkouts bestand folgender Befehl:
  `rtk proxy env PYTHONNOUSERSITE=1 PYTHONDONTWRITEBYTECODE=1 TMPDIR=/var/tmp/codex/ModSecurity-conector/runs/pr370-ready-without-nginx-20261001/tmp timeout 60s make check-bilingual-docs check-doc-links PYTHON=python3`.
  MRTS wurde nicht initialisiert; keine Links oder Checker abgeschwächt.
- Ein CI-Security-Testversuch mit System-Python hatte kein `yaml`; danach wurde
  die bestehende Parent-Umgebung mit CPython 3.14.7 und PyYAML 6.0.3 read-only
  gewählt. `rtk proxy env TMPDIR=/var/tmp/codex/ModSecurity-conector/runs/pr370-ready-without-nginx-20261001/tmp PYTHONNOUSERSITE=1 PYTHONDONTWRITEBYTECODE=1 /var/tmp/codex/ModSecurity-conector/pr393-python3147-hInzILPJ/venv/bin/python -m unittest tests.test_ci_security_workflows tests.test_change_record -q`
  — 51 Tests bestanden. Keine Umgebungs- oder Dependency-Mutation.
- `rtk proxy env PYTHONNOUSERSITE=1 PYTHONDONTWRITEBYTECODE=1 python3 ci/tools/new-change-record.py check`
  — Change-Record-Struktur bestanden; dies ist keine Runtime-/Evidenzvalidierung.

## Security-Auswirkung

Build-Output-Isolation bleibt erhalten. Vorhandene Registry-Quell-/Artefakt-Symlinks
können einen Wiederholungsbuild nicht in den Checkout umleiten; jeder Build
erhält frische Eingaben. Bestehende Absolute-Root-, kanonische Containment- und
Child-Symlink-Prüfungen bleiben aktiv. Tests decken abgewiesene Roots,
Symlink-Kinder, alte gestagte Quell-Symlinks, APXS-Wiederanlauf und Fehler jedes
CI-Builds ab. Keine Authentifizierung, Runtime-Fail-Closed-Semantik, Compilerwarnungen,
CI-Anforderungen oder Quality Gates werden abgeschwächt. Die extern gewählte
Root bleibt ein vertrauenswürdiger Build-Input; dies schützt nicht gegen
gleichzeitig bösartig agierende Verzeichniseigentümer.

## Runtime-Evidence

Die lokale native Apache-Prüfung bewies zwei Kompilierungen, nicht Hoststart
oder Traffic: Ownership-Setup scheiterte, bevor der Worker lief. Lokale
Common-/Sidecar-Smokes beweisen nur ihre Service-/Komponentenebenen. Frühere
Exact-Head-Receipts an `327daf72` bewiesen die ausgewählten CRS-Zellen Apache,
HAProxy-SPOP-Request, Envoy ext_proc, Traefik native und patched lighttpd;
keine vollständige G1–G9-Abnahme. Ein neuer Nachfolger benötigt frische
Hosted-Evidence. Am früheren Head meldete Sonar Quality Gate `OK` und neue
Duplikationsdichte/-Zeilen/-Blöcke `0.0%` / `0` / `0`; dies ist keine Nachfolger-Evidence.

## Bekannte Einschränkungen

Die vollständige G1–G9-Abnahme aller neun Nicht-NGINX-Profile bleibt unbewiesen:
HAProxy HTX, Envoy ext_authz, Traefik forwardAuth und Stock-lighttpd fehlt die
geforderte vollständige Host-Kampagne; SPOP-Request-only-Ergebnisse beweisen
seinen Response-Companion nicht. Drei vollständige Starts je Profil, vollständige
Phasengrenzen, Fehler-/Restartprüfungen und Parallelitätsproben mit RSS-/FD-
Messungen bleiben getrennte Evidenzanforderungen. Keine Produktionsfreigabe.

## Verbleibende Risiken

Frische Hosted-CI/Sonar müssen den veröffentlichten Nachfolger validieren.
Private Registry-Stages sammeln sich an, bis die zugehörige externe Build-Root
bereinigt wird; der Wrapper löscht keine potenziell benutzereigenen früheren
Ausgaben. Das lokale Dateisystem kann die geforderte Non-Root-Apache-Start-Evidence
nicht liefern. Die vollständige Neun-Profil-Abnahme wird weder durch diesen
begrenzten Build-Fix noch durch grüne Selected-Cell-CI ersetzt.

## Nicht ausgeführte Prüfungen mit Begründung

Keine neuen dedizierten NGINX-Läufe, vollständige Neun-Profil-G1–G9-Kampagne,
Last-/Produktionsfreigabe, Framework-/MRTS-Implementierung oder Merge durchgeführt.
Fehlende vollständige Host-Voraussetzungen und profilspezifische Abnahmebelege
bleiben Lücken, keine Waiver. Current-Head-Hosted-Verifikation erfolgt nach
Veröffentlichung und wird getrennt in PR #370 berichtet.

## Finaler Diff- und Review-Status

Das unabhängige Read-only-Review bestätigte die Rebuild-Containment-Korrektur
und identifizierte den anfangs verdeckten Erstfehler der Schleife; dieser wurde
reproduziert, korrigiert und durch die neue Shell-Control-Flow-Regression
abgedeckt. Finales Current-Diff-Review, exakter Nachfolger-SHA, Checks, Sonar,
Base-Freshness, Conversations und Draft-/Readiness-Status sind Delivery-Fakten
in PR #370. Dieser Record behauptet keinen tatsächlichen Merge oder
vollständigen Neun-Profil-Readiness-B-Nachweis.
