# Change Record: NGINX-Receipt nur für Konfigurationsprüfung

**Sprache:** [English](CR-20261001-nginx-configtest-receipt.md) | Deutsch

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | `CR-20261001-nginx-configtest-receipt` |
| Datum (UTC) | `2026-10-01` |
| Basis-Revision | `794d16d7d387512213bc2e8d8b2f3199e5dbc6ce` |

## Motivation und Problemstellung

Dem selektierten erforderlichen Record `invalid_boolean` fehlten eine konkrete
Konfigurations-Invocation und ein kanonischer Konfigurations-Evidence-Vertrag.
Eine Behandlung als HTTP-Case oder ein erfundenes Request-Event würde
Testebenen vermischen.

## Akzeptanzkriterien

Den geschlossenen Input `modsecurity maybe;` tatsächlich mit NGINX auf
Konfigurationsebene testen. Nur Exit 1 mit beiden exakten Diagnosen zur
Boolean-Ablehnung akzeptieren. Digestgebundene Operationsartefakte aufbewahren;
FAIL bei fehlender Evidence, falschem Exit, nicht zugehörigen Modulfehlern und
Mismatches erhalten. Auswahl nicht verändern und keine Requests, Starts,
Listener, Worker, Reloads oder vollständige Coverage behaupten.

## Implementierungsentscheidung und Begründung

Der Parent besitzt den tatsächlichen Treiber und das Selected-Invocation-
Wiring. Der separate [Collector-Record](CR-20261001-nginx-configtest-collection.de.md)
beschreibt Artefakt-Verifikation an der Source-Collection-Grenze.
Das begleitende Framework besitzt den expliziten
geschlossenen Konfigurationsvertrag und die Receipt-Validierung. Der Treiber
führt aufbewahrte Snapshots `nginx-binary` und `nginx-module.so` unter einem
frischen externen Root aus und liefert `nginx.conf`, `stdout.log`,
`stderr.log`, `source-result.json` und einen tatsächlichen rohen Record in
`source-result.jsonl`. Die fünf aufbewahrten Operationsdateien sind durch
Receipt-Digests gebunden; kein Native-Event wird synthetisiert. `-e stderr`
verhindert Bootstrap-Logging über einen gecachten Compile-Prefix-Pfad.
Snapshots werden über nicht folgenden Regular-File-Deskriptoren mit je 64 MiB
Grenze gelesen; Captures teilen eine Grenze von 64 KiB und die Operation hat
eine Frist von 10 Sekunden.

## Security-Auswirkung

Symlink-, Checkout- und wiederverwendete Ausgabepfade werden abgewiesen.
Child-Ausführung verwendet einen expliziten Argumentvektor und minimale
Umgebung mit optionalem explizitem Bibliotheksverzeichnis, keine Shell oder
Umgebungs-Dumps. Nur passende allowlistete Diagnosefragmente gelangen in den
Receipt; begrenzte rohe Logs bleiben extern. Erwartete Ablehnung ist keine
pauschale Nonzero-zu-PASS-Konvertierung. Dieser Parent-Slice schwächt keine
Framework-Guardrail oder Native-Event-Validierung und verändert weder
Common-Event-Produzenten noch MRTS-Source.

## Geänderte Dateien

- `ci/runtime/lifecycle/run-nginx-configtest.py`
- `ci/runtime/lifecycle/run-no-crs-baseline.sh` (nur Konfigurations-Wiring;
  zuvor vorbereitete Protokolländerungen sind vom Slice ausgeschlossen)
- `tests/test_nginx_configtest_driver.py`
- `tests/test_nginx_selected_configtest_wiring.py`
- `docs/testing-and-evidence.md` / `.de.md`
- Dieser gepaarte Change Record und das Archivindex-Paar

## Ausgeführte Befehle

Alle Shell-Validierungen verwenden RTK. Der Treiber scheiterte zunächst
dynamisch ohne Implementierung; die Retained-Artifact-Assertion scheiterte
separat vor dem Snapshot-Binding. Die Treiber-Suite besteht 12 Tests zu
erwarteter Ablehnung, falschem Exit/Diagnose, fehlendem/Symlink/zu großem Modul,
Freshness-/Checkout-Guards sowie Capture-Grenze und Timeout. Der finale
kombinierte Treiber-/Collector-Befehl verwendet die vorhandene Framework-
Virtual-Environment:
`rtk proxy env TMPDIR=/var/tmp/codex/ModSecurity-conector/tmp /root/git/ModSecurity-conector/modules/ModSecurity-test-Framework/.venv/bin/python -m unittest tests.test_nginx_configtest_driver tests.test_nginx_configtest_collection -v`.
Dieser finale kombinierte Rerun besteht 18 Tests in 12.304 Sekunden.
Der Task-Koordinator beobachtete zunächst 18 bestandene Selected-Wiring-Tests,
6 Collector-Tests und 58 benachbarte Parent-Tests. Sein anschließender breiterer
Parent-Fokus besteht 186 Tests in 57.106 Sekunden, einschließlich der 12
Treiber-Controls, 6 Collector-Controls, 7 neuen Konfigurations-Wiring-Controls
und benachbarten NGINX-/Pfad-/Lifecycle-Tests. Der begleitende Framework-Fokus
besteht zuletzt 27 Tests in 3.144 Sekunden, einschließlich des Bounded-Secure-
Copy-Controls; unabhängiges Review beobachtet dieselben 27 bestandenen Tests
in 3.651 Sekunden. Die eingefrorene No-CRS-Suite besteht 159 Tests in 112.402
Sekunden mit Exit 0. Vollständiges Framework-`make lint` endet ebenfalls mit
Exit 0 (Session 8526). Python-Kompilierung und Whitespace-Prüfung bestehen für den Treiber-
Slice. RTK-gekapseltes `make PYTHON=/root/git/ModSecurity-conector/modules/ModSecurity-test-Framework/.venv/bin/python check-bilingual-docs check-doc-links`
besteht mit externen `TMPDIR`/`BUILD_ROOT` und unverändertem physischem
Parent-Framework-Pin. Der erste Dokumentationscheck zeigte fehlende exakte
deutsche Record-Überschriften/Metadaten; sie wurden vor dem bestandenen Rerun
korrigiert. Kein unbeobachtetes Ergebnis wird als grün gemeldet.

## Runtime-Evidence

Die echte Retained-Diagnose
`runs/diagnosis/nginx-configtest-retained-jaYdBrvH` unter externem Task-Storage
führt tatsächliches NGINX aus. Der positive Case erzeugt kanonischen
`invalid_boolean`-PASS mit beobachtetem Exit 1 und exakter Boolean-Diagnose.
Die Negativkontrolle verwendet dieses tatsächliche Executable mit einem
kontrollierten Non-ELF-Modul: Exit 1 bleibt Case-FAIL mit
`unexpected_config_error`, keine erwartete Ablehnung. Framework-Finalisierung
erzeugt für jede Kontrolle fünf verwaltete Artefakte; der strikte Check hasht
sie erneut. Beide haben null Native-Events und keinen Daemon-Start oder
Request-Ausführung. Source- und Canonical-Aggregate bleiben FAIL, weil andere
Required-Requests absichtlich nicht ausgeführt wurden. Der strikte Checker für
`analysis/nginx-configtest-retained-check-20261001.json` endet mit Exit 0.
Diese Retained-Build-Diagnose ist kein Exact-Head-Full-Lifecycle-PASS.

## Nicht ausgeführte Prüfungen mit Begründung

Kein Full-E2E, Push, PR-Eingriff, Gitlink-Update, Protokolllauf oder Merge ist
enthalten. Das vollständige Required-Coverage-Gate ist nicht grün; unabhängiges
Source-SHA-/Run-Binding ist vor Exact-
Head-Claims erforderlich. Root-Master-/nobody-Worker-Checks sind für
`nginx -t` nicht anwendbar.
Der Framework-spezifische Change-Record-Checker auf dem Parent ist nicht
anwendbar: Parent-Records verwenden das aktuelle Parent-Template und native
Bilingual-/Pfad-/Link-Checks, nicht die anderen Framework-Überschriften. Keine
historischen Parent-Records oder Validatoren werden verändert, damit dieser
Cross-Owner-Check besteht.

## Bekannte Einschränkungen

Nur `invalid_boolean` wird durch diesen initialen Vertrag implementiert.
Neun weitere konfigurationsbezogene Required-Records bleiben außerhalb des
Slices; HTTP-, Startup-, Reload- und Fault-/Protokollanforderungen werden
durch diesen Receipt nicht erfüllt. Der gesamte Missing-Path-Zähler benötigt
eine separate gemessene Aktualisierung.

## Verbleibende Risiken

Das gecachte Executable, Modul und explizite Bibliotheksverzeichnis müssen
vertrauenswürdig sein. Receipts signieren keine Source-Identitäten: vom
Aufrufer übergebene SHAs benötigen unabhängigen Run-Provenienz-Vergleich.
Snapshots binden ausgeführte Bytes, belegen aber nicht, dass ein aufbewahrter
C-Build aus der aktuellen Parent-Source-Revision erzeugt wurde.

## Finaler Diff- und Review-Status

Dies ist eine lokale begrenzte Implementierung im Review. Vorbereitete
Protokollarbeit bleibt uncommitted und außerhalb des Slices. Framework-
Änderungen haben eigene Ownership; Parent-Framework-/MRTS-Gitlinks bleiben
unverändert. Kein Full-E2E-PASS, Delivery- oder Merge-Ergebnis wird behauptet.
