# Change Record: CR-20261018-i12-apache-evidence-boundaries

**Sprache:** [English](CR-20261018-i12-apache-evidence-boundaries.md) | Deutsch

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | CR-20261018-i12-apache-evidence-boundaries |
| Datum (UTC) | 2026-10-18 |
| Basis-Revision | `ad510c3b4168ff0e11fc36803e2ce4127a0689ad` |

## Motivation und Problemstellung

Die Cloud-Analyse dieser Basis-Revision meldete 59 offene neue Findings: 35 Schwachstellen und 24 Code Smells, Security-Rating E, 62 neue duplizierte Zeilen, null akzeptierte Findings und null neue Hotspots; das Quality Gate war ERROR. Analysis-ID: `fb98417b-c9eb-4f0f-ba1d-e94e5b868a0a`; CE-Task: `AaFAC4JUzCyA98lidsk1`. Dies sind historische Serverergebnisse, keine Ergebnisse für die hier beschriebenen unveröffentlichten Änderungen.

Diese Änderung begrenzt bestehende Apache-Evidence-Werkzeuge auf zugelassenen privaten Speicher und wörtliche Loopback-Clientargumente, vereinfacht bestehende Extraktions- und Paketierungspfade und kennzeichnet die Herkunft des öffentlichen Readbacks ausdrücklich. Neue Abnahmetreiber, neue Host-Observer und deren spätere Runtime-Läufe liegen außerhalb dieses Records.

## Akzeptanzkriterien

Private Pfad- und Clientargumentprüfungen weisen unsichere Eingaben zurück; tatsächliche APR-Aufrufe und Rückgaben bleiben erhalten. Extraktion, vollständige Ledger mit 155 Zeilen und Pakete behalten Beobachtungen, Original-Oracles, unbekannte Werte und Freigabegrenzen bei. Die physische Quelle einer öffentlichen Projektion bleibt unabhängig abrufbar. Vor einer Gesamtabnahme bleiben CI und Cloud-Analyse des endgültig veröffentlichten Heads erforderlich.

## Implementierungsentscheidung und Begründung

`paths.py` prüft konfigurierten externen Speicher, Eigentümer und Modi der übergeordneten Verzeichnisse, kanonische Eingabedateien ohne Symlinks, Fixture-Auswahl und private Ausgabeziele. Beide Vorbereiter versiegeln dieses Hilfsmodul und `process_capture.py`; Letzteres teilt bestehende Snapshots desselben Prozesses, ohne Cleanup-Beobachtungen zu erfinden. `observed_curl.py` lässt eine wörtliche Menge von Optionen und Werten, genau eine HTTP-Loopback-URL ohne Zugangsdaten an einem hohen Port sowie private Body-/Ausgabepfade zu; echtes Readiness-curl deaktiviert implizites Laden von Konfiguration.

Der APR-Fehlerhelfer verlangt das Opt-in `I12_SINK_ROOT`, kanonischen nicht gemeinsam beschreibbaren Speicher der aktuellen UID und den bestehenden exakten privaten Marker. Typisierte Funktionszeiger, eine Beobachtungsstruktur und ein Helfer für physische Operationen ersetzen komplexe Deklarationen und Verzweigungen; echte Descriptor-Operationen und APR-Rückgaben werden weitergereicht. Benannte Kollektoren teilen Extraktion, Ledger, Paketierung und Vorbereitung auf. Eine Äquivalenzprüfung zeigte während des Refactorings eine falsche Kandidatenauswahl und das Überschreiben des akzeptierten Pakets; beides wurde korrigiert, und Regressionstests sichern die übergebene Eingabe und das akzeptierte Paket.

`public_projection.py` benennt 18 aus Zeitstempeln abgeleitete numerische Client-Verknüpfungen von `client_token` in `client_process_correlation_id` um. Die Metadaten setzen ausdrücklich `is_physical_capture: false`, listen jede Umbenennung und binden den unveränderten Quellhash. Geändert wird der öffentliche Feldname, nicht die physische Beobachtung oder ihre Bedeutung.

## Geänderte Dateien

Das Apache-spezifische Verzeichnis `ci/runtime/lifecycle/apache-i12/` enthält Änderungen an `apr_sink_fault.c`, `launch.py`, `ledger.py`, `observed_curl.py`, `package.py`, `prepare.py`, `prepare_sinks.py`, `review.py` und `sink_launch.py` sowie `paths.py`, `process_capture.py` und `public_projection.py`.

Zugehörige Änderungen betreffen `tests/test_apache_i12_boundaries.py`, `tests/test_apache_i12_launch.py`, `tests/test_apache_i12_package.py` und `tests/test_apache_i12_sink_fault.py`; die historischen Reproduktionshelfer `root-review-duplicate.py`, `root-review-supported.py` und `rule-equivalence-probe.py`; das öffentliche `sink-positive-control.json`; sowie dessen erhaltene Rohquelle und Manifest. Dieses EN/DE-Change-Record-Paar dokumentiert diesen Umfang. Dieser Arbeitsschritt ändert keinen produktiven Connector-Code, gemeinsamen Observer, Workflow, Scanner-Ausschluss, Framework-/MRTS-Gitlink oder die zentrale Matrix.

## Ausgeführte Befehle

Der frühere fokussierte Lauf verwendete:

```sh
rtk proxy /root/git/ModSecurity-conector/.venv/bin/python -m unittest -q tests.test_apache_i12_mapper tests.test_apache_i12_sink_fault tests.test_apache_i12_review tests.test_apache_i12_ledger tests.test_apache_i12_package tests.test_apache_i12_launch tests.test_apache_i12_boundaries
```

Ergebnis: 48 Tests, Exit 0, einschließlich acht Tests mit echten APR-Operationen. Das Deaktivieren der physischen Fehleroperation in einem separaten Quellmutanten führte acht native Tests aus und ergab zwei erwartete Fehler, null Errors; der Mutationsdetektor endete mit Exit 0. Vergleiche aller Felder waren für acht tatsächliche unsignierte Pakete, alle 155 Ledger-Zeilen und alle 155 Paketzeilen gleich. Drei Vorbereitungsprüfungen versiegelten ihre Eingaben; sie führten keine Hosts aus. Das frühere `rtk proxy git diff --check` endete mit Exit 0. Nach dem Ausfüllen dieses Paars endeten `rtk proxy /root/git/ModSecurity-conector/.venv/bin/python ci/tools/new-change-record.py check` und `rtk proxy git diff --check` beide mit Exit 0. Die Change-Record-Prüfung validiert nur die Struktur, nicht die Richtigkeit der Evidence.

Laufbezogene Belege liegen unter `/var/tmp/codex/ModSecurity-conector/runs/i12-apache-414-acceptance-20261015/analysis/`: `sonar-checks/receipt.json`, `sonar-checks/mutation-receipt.json`, `sonar-extraction-equivalence.json`, `sonar-ledger-package-equivalence.json`, `sonar-preparation-checks.json` und `sonar-fix-summary.json`. Diese lokalen Belege beschreiben den erfassten Worktree-Stand; sie belegen weder Lieferung noch Prüfungen des finalen Heads.

## Security-Auswirkung

Angriffsvoraussetzungen sind vom Angreifer kontrollierte CLI-Pfade, Fixture-Auswahl oder Clientargumente, die diese privaten Testwerkzeuge erreichen, oder unsichere Substitutionen beschreibbaren Speichers. Die Prüfungen begrenzen diese Eingaben und lehnen unsichere Zustände ab. Numerische Prozessverknüpfungen vermitteln keine Authentifizierungsrechte. Es gibt keinen Scanner-Ausschluss, kein akzeptiertes Finding, keine Ausnahme, keinen Validierungsbypass, keine erfundene Fehlerrückgabe, keine gelockerten Warnungen und kein abgeschwächtes Gate.

## Runtime-Evidence

Die Tests üben echte APR-Operationen und Negativkontrollen aus; die Äquivalenzprüfung verwendet acht vorhandene tatsächliche Hostpakete. Dieser Record behauptet keine zusätzliche native Hostausführung und keinen neu qualifizierten I12-PASS.

Das historische Fallledger bleibt bytegleich mit SHA256 `927a0c809e7c26bcdb4ffed2f87370c23c6a21a066d6bb7bc217a626be7ea746`. Das erhaltene [Rohdatenmanifest](../apache-i12-20261015/raw/manifest.json) adressiert [sink-positive-control.json.gz](../apache-i12-20261015/raw/sink-positive-control.json.gz): komprimiertes SHA256 `22f8ba1e53be10ce9b2cb92fa3849877889f08fd65f086f2acc830df93e57e59`, dekodiertes SHA256 `e52c51888736e9f252d1eff738e75cd7f8dd784045926ec12fad2df85439772f`. Dasselbe Original ist in Commit `68e3c34a780e26cfb714155b4f7652ca059a8572` erhalten. Die öffentliche Projektion ist ausdrücklich von dieser physischen Quelle getrennt.

## Bekannte Einschränkungen

Die 59 Quellkorrekturen sind Kandidaten, bis der veröffentlichte Head eine neue Cloud-Analyse erhält. Lokales Vortex lieferte HTTP 403; authentifizierte Cloud-Readbacks waren erfolgreich. Weder dieser Fehler noch lokale Quellprüfung belegt null Findings. Vorbereitung und Paketäquivalenz belegen keine Ausführung der verbleibenden Apache-Verträge. Fehlende Messungen bleiben unbekannt.

## Verbleibende Risiken

Regressionen im integrierten Quellstand und neu gemeldete Scanner-Findings erfordern abschließende integrierte Prüfungen. Bestehende Runtime-Lücken, Original-Oracle-Konflikte und die Abnahmeentscheidung über 155 Fälle bleiben gesonderte Arbeit. Es gibt keine Release-Freigabe und keine Behauptung `I12_COMPLETE`.

## Nicht ausgeführte Prüfungen mit Begründung

Cloud-Analyse des endgültig veröffentlichten Heads, strikte Abnahme von null Duplikation/Security-Findings, GitHub-CI für den exakten Head und die finale integrierte Hostkampagne sind durch diesen Arbeitsschritt nicht belegt, da er vor Veröffentlichung und Integration liegt. Repository-weite Zweisprachigkeits- und Linkprüfung übernimmt die integrierende Aufgabe nach dem Ausfüllen dieses Paars. Für diesen Record erfolgten weder Merge noch Deployment oder Produktrelease.

## Finaler Diff- und Review-Status

Der dokumentierte Umfang ist ein uncommitteter Apache-Evidence-Werkzeugkandidat auf Basis der obigen Revision; dies ist kein Liefer-SHA. Die integrierende Aufgabe übernimmt die finale Diff-Prüfung, frische Validierung, normale Commits/Push und Aktualisierungen von PR #414. Quellkorrekturen werden nicht als Cloud-Auflösung gemeldet.
