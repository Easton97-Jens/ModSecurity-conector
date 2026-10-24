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

Frische CI am Zwischenstand `ac76cdbe` zeigte anschließend einen weiteren
aktuellen Merge-Blocker: Das gepinnte HTTPD 2.4.68 wurde vom konfigurierten
Download-Endpunkt nicht mehr geliefert (HTTP 404), vor dem Apache-Connector-
Build. Das offizielle Archiv entsprach der geprüften gepinnten SHA-256.
Eine zweite gezielte Parent-Korrektur stellt diese Quelle ohne Framework-Pin-
Änderung oder Abschwächung der Quellverifikation wieder her.

Die spätere Benutzerfreigabe erlaubt einen separaten Framework-Fix/PR und die
Einbindung seines geprüften veröffentlichten Commits. Framework PR
[#133](https://github.com/Easton97-Jens/ModSecurity-test-Framework/pull/133)
korrigiert den zweiten Downloader, der das Parent-geprüfte Archiv verwarf und
den nicht verfügbaren Endpunkt erneut abfragte. Dieser Parent-Schritt erhöht
ausschließlich den Framework-Gitlink und seine exakten CI-SHA-Projektionen;
Upstream-Komponenten-Pins und MRTS bleiben unverändert.

## Akzeptanzkriterien

- Wiederholte Builds und Wiederanlauf nach APXS-Fehler funktionieren unter derselben externen Root.
- Gestagte Registry-Symlinks/-Artefakte werden weder vertraut noch überschrieben;
  Symlink-Kinder und Ausgaben innerhalb des Checkouts bleiben abgewiesen.
- CI führt die Containment-/Retry-Unit-Tests und zwei echte Builds ausdrücklich
  aus; ein Fehler eines Builds lässt das Gate scheitern, statt durch Retry verdeckt zu werden.
- Entfernte offizielle HTTPD-Download-Endpunkte dürfen das offizielle Archiv nur
  bei typisiertem HTTP 404 mit identischem Dateinamen/Version und geprüftem literalem Hash nutzen.
- EN/DE-Dokumentation und Traceability bleiben gleichwertig. Delivery erfordert
  frische Current-Head-CI und Sonar einschließlich 0.0% New-Code-Duplikation.
- Framework-Delivery erfolgt separat und geprüft vor dem autorisierten Parent-
  Pointer-Update. Exakte Workflow-/Test-SHA-Verbraucher folgen dem veröffentlichten Commit.
- Keine neue NGINX-Implementierung oder manuell gestarteten NGINX-Läufe, MRTS-
  Änderungen, abgeschwächten Controls, direkten `master`-Writes, Merge oder Neun-Profil-B-Hochstufung.

## Implementierungsentscheidung und Begründung

Existiert bereits eine reguläre Registry-Stage `connectors`, wird ein privates
Verzeichnis `rebuild.XXXXXX` unter der kanonischen externen Staging-Root angelegt.
Jeder Aufruf kopiert Registry-Quellen in sein frisches `connectors`-Kind.
Bisherige Registry-Eingaben/-Libtool-Artefakte werden weder gelöscht, überschrieben
noch wiederverwendet. Das Common-Source-Staging behält sein bestehendes Verhalten.
Die Bootstrap-Prüfung führt `make` zweimal mit derselben Staging-Root aus und
gibt jeden Fehler ausdrücklich weiter: `set -e` allein schützt eine Schleife
innerhalb von `if ! (...)` nicht.

Der HTTPD-only-Downloader akzeptiert die exakte `.tar.bz2`-URL unter
`downloads.apache.org/httpd/` und literale SHA-256, bevor er bei typisiertem
HTTP 404 den offiziellen Fallback unter `archive.apache.org/dist/httpd/`
berücksichtigt. Andere HTTP-/Netzwerkfehler, unerwartete URLs/Komponenten,
fehlende Hashes und Integritätsfehler wählen keine andere Quelle. Dieselbe
Prüfsumme wird vor Tar-Inspektion geprüft. Kanonisch konfigurierte URL und
Cache-Identität bleiben erhalten; das Komponenten-JSON erfasst die tatsächliche
`download_url`. Ein geprüfter Cache-Hit verwendet leere `download_url` und
`download_status=cached`, statt ursprüngliche Fetch-Provenienz zu erfinden.

Der Framework-Vertrag wird von
`9181dc77dfb0685d87fa109e6800dc6052d77cc9` auf den remote verfügbaren geprüften
`a35ac6d02a4e2e7a94ec7679e4e94877cc0126f9` erhöht. Die Framework-eigene Änderung
prüft sichere reguläre HTTPD-Cache-Bytes erneut, stellt ausschließlich bei
direktem HTTP 404/Curl 22/null Redirects wieder her, erhält die kanonische
Metadatenvalidierung und extrahiert eine private erneut gehashte Kopie.
Gemeinsamer Downloader, APR-util-Controls, Upstream-Pins und MRTS-Gitlink bleiben
unverändert. Der native Parent-Synchronisierer projiziert exakt vier Workflow-
SHA-Literale und eine Test-Fixture; dynamische Identitäten und geschützte
NGINX-Projektionen bleiben erhalten.

## Geänderte Dateien

- `connectors/apache/build/apxs-wrapper.in`
- `tests/test_apache_apxs_profile_registry_staging.py`
- `tests/test_apache_httpd_archive_fallback.py`
- `ci/provisioning/components/prepare-runtime-components.py`
- `ci/checks/connectors/apache/check-apache-autotools-bootstrap.sh`
- `.github/workflows/test-apache.yml`
- `modules/ModSecurity-test-Framework` (nur Gitlink; separat gelieferte Source)
- `.github/workflows/test-connectors-with-crs-no-mrts.yml`
- `tests/test_ci_security_workflows.py` (exakte Framework-SHA-Fixture)
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
- Nachfolger-Suite: Derselbe fokussierte Befehl oben mit zusätzlichem Modul
  `tests.test_apache_httpd_archive_fallback` bestand 105/105 Tests. Die zehn neuen
  Quelltests enthalten Managed-Cache-Identität/-Reuse und Literal-before-List-
  CI-Caller-Wiring. Die HTTP-404-Regression scheiterte vor ihrer Korrektur.
- `rtk proxy curl --fail --location --silent --show-error --max-time 60 --output /var/tmp/codex/ModSecurity-conector/runs/pr370-ready-without-nginx-20261001/httpd-2.4.68-archive.tar.bz2 https://archive.apache.org/dist/httpd/httpd-2.4.68.tar.bz2`
  und `rtk proxy sha256sum /var/tmp/codex/ModSecurity-conector/runs/pr370-ready-without-nginx-20261001/httpd-2.4.68-archive.tar.bz2`
  — Download bestanden; exakte gepinnte SHA-256
  `68c74d4df38c26bed4dfbdb8f3baf1eb532f3872357becc1bba5d136f6b63c06`.
- Ein tatsächlicher ungemockter Aufruf von `prepare_archive("httpd", ..., required_literal_sha256=True, verify_digest_before_archive_list=True)`
  über RTK/CPython 3.14.7 bestand den Primary-404-/Official-Archive-Pfad,
  mit demselben Hash vor erfolgreicher Tar-Inspektion. Nur Quellvorbereitung
  geprüft; daraus folgt keine zusätzliche Host-Runtime-Aussage.

Framework-Kandidatendaten wurden unter dem externen kontrollierten temporären
Root materialisiert und an den veröffentlichten Commit gebunden: Git-Blob-
Identität und `git hash-object` der kopierten Daten sind jeweils
`e206cb6595c08aa1a13781d47e86a981ce96d1e5`. Über RTK und Parent-eigenes
Python3.14.7 bestanden `ci/tools/sync-framework-component-versions.py --validate`,
dann `--sync` und `--check` mit
`--framework-sha a35ac6d02a4e2e7a94ec7679e4e94877cc0126f9`. Nur Workflow-/Test-
SHA-Projektionen änderten sich; der finale Check listet keine Abweichungen.
`ci/tools/verify-framework-candidate-contract.py` bestand vor und nach Projektion
mit dem jeweils erwarteten Parent-SHA. Dies sind statische Kompatibilitätsprüfungen,
keine NGINX-Ausführung oder Runtime-Nachweise.

Der native Wiederholungslauf `make check-ci-security-contract` mit dem vorhandenen
Parent-Python und externem `BUILD_ROOT` als Umgebungsvariable bestand: 170 Tests,
fünf ausdrückliche Skips mangels Namespace-/Identity-Integrationsfähigkeiten sowie
actionlint-/zizmor-/gitleaks-Lockvalidierung. Der erste Versuch verwendete ein
Make-Kommandozeilen-`BUILD_ROOT`, das über `MAKEFLAGS` vererbt wurde und die
Nested-Make-Prioritäts-Fixture ungültig machte; dies wurde unabhängig reproduziert.
Kein Test oder Runtime-Helfer wurde für das erfolgreiche Ergebnis geändert.

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

Die HTTPD-Quellwiederherstellung erhält kanonische Quell-/Versions-/Hash-/Cache-
Identität und ergänzt Digest-before-List-Enforcement; kein neuer Dependency-
Pin oder NGINX-Quellpfad wird gewählt. Das unabhängige Review fand keinen
konkreten Bypass; Managed-Cache- und Caller-Guard-Tests ergänzen die zunächst
geprüften acht Fälle. Tatsächliche Archivbytes wurden hashgeprüft, nicht aus
dem HTTP-Status für vertrauenswürdig erklärt.

## Runtime-Evidence

Die lokale native Apache-Prüfung bewies zwei Kompilierungen, nicht Hoststart
oder Traffic: Ownership-Setup scheiterte, bevor der Worker lief. Lokale
Common-/Sidecar-Smokes beweisen nur ihre Service-/Komponentenebenen. Frühere
Exact-Head-Receipts an `327daf72` bewiesen die ausgewählten CRS-Zellen Apache,
HAProxy-SPOP-Request, Envoy ext_proc, Traefik native und patched lighttpd;
keine vollständige G1–G9-Abnahme. Ein neuer Nachfolger benötigt frische
Hosted-Evidence. Am früheren Head meldete Sonar Quality Gate `OK` und neue
Duplikationsdichte/-Zeilen/-Blöcke `0.0%` / `0` / `0`; dies ist keine Nachfolger-Evidence.

Zwischenstand `ac76cdbe`: Frischer Apache-Bootstrap bestanden (einschließlich
acht Staging-Units und echtem Non-Root-Traffic), vier CRS-Zellen bestanden,
Apache CRS vor Build durch HTTPD HTTP 404 gescheitert; das Fail-Closed-Aggregat
scheiterte folgerichtig. Diese Ergebnisse bleiben erhalten, statt durch Retry
gelöscht zu werden. Sonar meldete an diesem exakten Zwischenstand Gate `OK`,
0.0% neue Duplikation, null OPEN/CONFIRMED-Issues und null TO_REVIEW-Hotspots.
Der Quellwiederherstellungs-Nachfolger erfordert eine eigene neue CI-/Sonar-Runde.

Der Quellfallback-Head `8a3999f3` behielt 0.0% neue Duplikation, Sonar meldete
jedoch vier neue Wartbarkeits-Issues: duplizierte SHA-256-Regex und ausführliche
Ziffernklassen. Die letzte gezielte Korrektur teilt ein kompiliertes Lowercase-
Digestmuster und nutzt `\d` mit `re.ASCII`; der ursprüngliche ASCII-only-URL-
Vertrag bleibt erhalten. Die bestehende Regression prüft die Ablehnung von
Unicode-Ziffern-URLs. Keine NGINX-Funktion und kein NGINX-Quellvertrag wird geändert.
Nach dieser Korrektur bestanden erneut die fokussierten 105 Tests sowie alle
sieben Tests aus `tests.test_apr_util_static_contract`, Bilingual-/Doc-Links,
Change-Record-Struktur und Diff-Whitespace. Das unabhängige Review bestätigte
äquivalentes Regex-Matching; Published-Head-Sonar/CI benötigen frische Rückprüfung.

Am Parent-Head `221e1068ecde20ec04355b8009aabcb0302c4cbb` bestand der Apache-
Bootstrap, aber die Apache-CRS-Zelle scheiterte mit `missing_local_httpd_build`
und das Aggregat fail-closed; die vier anderen Zellen bestanden. Ein direkter
Reproducer des unveränderten Framework-Helfers lieferte HTTP 404/Exit 77 nach
Verwerfen seiner task-eigenen geprüften Stage-Kopie. Das Originalarchiv blieb
erhalten.

Die separat gelieferte Framework-Abhängigkeit an `a35ac6d0` hat 13 erfolgreiche
Exact-Head-Checks, drei erwartete Event-Skips und keine ausstehenden/fehlgeschlagenen
Checks, einschließlich beider vollständiger Hosted-Lint-Läufe und CodeQL.
Sonar-Analyse `2026-10-01T17:39:04+0000` gehört exakt zu diesem Framework-Head:
Gate OK, neue Duplikation 0.0%, duplizierte Zeilen/Blöcke null, offene/bestätigte
Issues null und ausstehende Hotspots null. Framework-eigene 18 HTTPD-, 13 APR-util-
und 20 Downloader-Regressionen bestanden unabhängig, und sein echter
HTTPD2.4.68-/APXS-Diagnosebuild bestand ohne Hoststart. Dies sind externe
Abhängigkeitsfakten, keine Parent-Host-Runtime-Ergebnisse. Die neue Parent-/
Framework-Kombination benötigt nach Veröffentlichung frische Parent-CI, Sonar
und Runtime-Receipts.

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
Last-/Produktionsfreigabe, MRTS-Implementierung oder Merge durchgeführt.
Framework-Implementierung wurde ausdrücklich autorisiert, im eigenen PR #133
geliefert und geprüft; dieser Parent-Commit enthält nur Gitlink und Projektionen,
keine Framework-Source-Dateien.
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
