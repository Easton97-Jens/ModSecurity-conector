# Change Record: CR-20261028-sonar-connectors-followup

**Sprache:** [English](CR-20261028-sonar-connectors-followup.md) | Deutsch

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | CR-20261028-sonar-connectors-followup |
| Datum (UTC) | 2026-10-28 |
| Basis-Revision | `c5993ed9a7b59fc0bd58f105595ec79f596c88d6` |

## Motivation und Problemstellung

Der Nutzer bat um einen neuen PR zur Sonar-Verzeichnistabelle und nahm anschließend `tests/` und `ci/` ausdrücklich aus. Die aktuelle Hauptanalyse an der Basis enthält 35 Connector-Befunde: 34 API-Const-Vorschläge `c:S995` und eine Operator-Eingabepfadmeldung `pythonsecurity:S8707`. Dies sind die bereits geprüften Kandidaten nach dem gemergten PR #430. Der Nutzer hatte zunächst ausschließlich Dokumentation bestimmt und anschließend ausdrücklich verlangt, diese geprüften Connector-Befunde aus der Bewertung zu nehmen. Diese neuere Anweisung autorisiert einzelne False-Positive-Umstufungen für exakt diese 35 Hauptprojektbefunde; ci/ und tests/ bleiben ausgenommen.

## Akzeptanzkriterien

Alle 35 authentifizierten aktuellen Positionen einzeln abgleichen; ABI und unterstütztes CLI-Verhalten erhalten. Beide Nutzerausnahmen erfassen, ohne den Analyseumfang zu ändern. Produktquellcode unverändert lassen; nur die 35 einzeln geprüften Connector-Befunde mit technischen Kommentaren als FALSE_POSITIVE einstufen. Null verbleibende Connector-Befunde und unveränderte andere Befundstatus prüfen. Den ursprünglichen und verbleibenden Master-Gate-Fehler korrekt angeben. Bericht und gepaarte Records validieren, anschließend einen neuen Draft-PR mit wahrheitsgemäß gemeldeten Prüfungen am aktuellen Head liefern. Dies ist eine autorisierte Fehlalarmeinstufung und keine Behauptung 35 behobener Codefehler oder als Risiko akzeptierter Schwachstellen.

## Implementierungsentscheidung und Begründung

Frische unabhängige Quellcode-/Header-/Registrierungsprüfung bestätigt, dass 18 Apache-, sieben NGINX- und neun HAProxy-Parameterpositionen die vorhandenen veränderbaren Host-Callbacktypen benötigen. Pointee-Const würde diese Signaturen verletzen. Die neue HTX-Master-Befund-ID bezeichnet die bereits geprüfte Funktion `haproxy_modsecurity_htx_filter_http_payload/msg`, keine neue Ursache.

Der lighttpd-First-Byte-Helfer akzeptiert bewusst separat gewählte Event-Eingabe. Sein vorhandener positiver Test `connectors/lighttpd/tests/test_patched_event_validation.py::test_first_byte_writer_accepts_phase_aliases_and_preserves_schema` legt die Eingabe außerhalb von `--runtime-output-root` ab und erwartet Erfolg. Der tatsächliche Hosted-Runner übergibt einen festen privaten Snapshot. Sonar beschreibt lokales `argparse.parse_args()` als HTTP-Quelle; es wurde keine neue ausnutzbare Grenze belegt. Verpflichtendes Output-Root-Containment würde den nachgewiesenen Vertrag verletzen. Optionales neues Input-Root-Verhalten wäre eine separate Funktion und würde den generischen Eingabezweig nicht entfernen; daher wird es nicht ergänzt.

Nach der neueren Nutzerfreigabe wurden alle 35 Befunde mit der vorhandenen authentifizierten API und ihren spezifischen technischen Gegenbelegen einzeln umgestuft. Unabhängiger Abruf bestätigte exakt 35 FALSE_POSITIVE-Statuswerte und exakte Kommentare. Produktquellcode bleibt unverändert.

## Geänderte Dateien

`reports/audits/sonar-connectors-followup-20261028.json`, dieser deutsche Record und sein englischer Begleiter. Das JSON erhält den ursprünglichen Snapshot mit 35 Positionen und ergänzt die autorisierte Einstufung/Readback. Keine Änderungen an Connector-, CI- oder Testquellen, Quellbindungen, generiertem Testarchiv, Gitlinks, Abhängigkeiten, Regeln, Gates, Unterdrückungen oder Analyseausschlüssen.

## Ausgeführte Befehle

PASS: authentifizierter Read-only-Snapshot von Befunden/Hotspots/Metriken/Analyse/Gate durch RTK und `/usr/local/bin/sonar-with-env`, gebunden an die exakte Basis. Das vollständige Hauptinventar enthält 59 offene Befunde; die Connector-Auswahl umfasst 35 bei null Hotspots. PASS: `rtk bypass python3.15 /var/tmp/codex/ModSecurity-conector/analysis/sonar-directory-followup-20261028/connector-only/verify-connector-report.py` bestätigt jede ID/Regel/Typ/Pfad/Zeile/Meldung, 34 API- plus einen CLI-Fall, beide Ausnahmen, null Quellcodeänderungen und exakt 35 autorisierte Servereinstufungen. Unabhängige Quellcode-/Vertragsprüfung ist abgeschlossen. PASS: `rtk bypass python3.15 ci/tools/new-change-record.py check`, `rtk make check-bilingual-docs PYTHON=/usr/local/bin/python3.15`, `rtk make check-doc-links PYTHON=/usr/local/bin/python3.15 FRAMEWORK_ROOT=/var/tmp/codex/ModSecurity-conector/worktrees/sonar-directory-followup-20261028/modules/ModSecurity-test-Framework`, vorgemerktes `git diff --check` und Standard-Gitleaks8.30.1-Scan der vorgemerkten Änderungen mit `--redact=100`. PASS: 35 sequenzielle `/api/issues/do_transition`-Aufrufe mit `transition=falsepositive` durch RTK und `/usr/local/bin/sonar-with-env`, jeweils mit technischem Einzelkommentar. Unabhängiger Abruf/Peer-Prüfung bestätigt alle 35 FALSE_POSITIVE, null offene Connector-Befunde, null Bugs/Vulnerabilities/Code Smells/Hotspots und alle Connector-Ratings 1.0 (A). Exakt 24 andere offene Statuswerte bleiben unverändert: ci/ 15, tests/ 6, common/ 3. Neues CI/Cloud am aktuellen Head wird noch nicht behauptet.

## Security-Auswirkung

Keine Änderung an Security-Kontrollen oder Runtime-Verhalten. Review-Evidence ist auf die ausgewählten Befunde begrenzt. Das fehlgeschlagene Master-Gate bleibt als ERROR erfasst: `new_security_rating=5`, erforderlicher Höchstwert `1`, New-Code-Zeitraum ab `2026-05-14T18:30:31+0000`. Die autorisierte Fehlalarmeinstufung entfernt diese Meldungen aus der Connector-Bewertung. Sie ist weder Quellcode-Security-Fix, Risikoakzeptanz noch bestandene Master-Analyse. Keine Regeln oder Gates wurden geändert.

## Runtime-Evidence

Für diesen reinen Dokumentations-PR wurde keine Runtime-Evidence erhoben oder beansprucht. Quellcode und vorhandene Tests wurden ausschließlich als Vertragsevidence gelesen.

## Bekannte Einschränkungen

Alle 35 geprüften Befunde sind nach der neueren ausdrücklichen Nutzeranweisung jetzt FALSE_POSITIVE. Offene Connector-Befundmetriken sind null; andere Hauptprojektkomponenten und separate Native-/Advisory-Projekte wurden nicht umgestuft. Es wurde keine sichere reine Quellcodekorrektur gefunden, die die nachgewiesenen APIs und das CLI-Verhalten erhält. Ein gegebenenfalls grünes neues Changed-Code-PR-Gate bereinigt das unveränderte Master-Inventar nicht. Der Analysesnapshot ist revisionsgenaue Evidence, keine Zusage für spätere Analysen.

## Verbleibende Risiken

Nicht unterstützte Callbackänderungen oder willkürliche Einschränkungen separat gewählter Operator-Eingaben würden Kompatibilitätsregressionen verursachen. Diese Ansätze werden nicht implementiert. Nur die 35 geprüften Hauptprojekt-Connector-Statuswerte änderten sich. Die übrigen 24 offenen anderen Statuswerte wurden unabhängig als unverändert geprüft. Befunde in `ci/` und Root-`tests/` bleiben außerhalb dieser Aufgabe und werden nicht aus der Analyse entfernt.

## Nicht ausgeführte Prüfungen mit Begründung

Keine Produkttests, Builds, zusätzliche I12-Kampagne, Runtime-Matrix, Deployment oder Merge: es ändert sich kein Produktcode. Vorhandene positive Tests wurden als Vertragsevidence gelesen, nicht ausgeführt oder neu als bestanden gewertet. Beide konfigurierten Sonar-Workflows gelten weiterhin für reine Dokumentations-PRs; Ergebnisse am exakten Head sind nach Erstellung abzurufen. Framework bleibt am vorhandenen exakten Gitlink für Parent-Linkprüfungen, ohne Framework-/MRTS-Änderung.

## Finaler Diff- und Review-Status

Der angeforderte Umfang besteht ausschließlich aus Connector-Befunden. Dieser PR liefert den aktuellen Abgleich der 35 Positionen und die Auditspur der neueren autorisierten Fehlalarmumstufungen. Quellcodekorrekturen bleiben null; die Connector-Bewertung ist bereinigt, während das globale Master-Gate ERROR bleibt. Lokale Daten-, Struktur-, zweisprachige/Link-, vorgemerkte Whitespace- und Secret-Prüfungen bestehen; unabhängiges EN/DE-/Datenreview fand keine wesentlichen Ungenauigkeiten. Neue Draft-PR-/CI-Ergebnisse am aktuellen Head sind im PR abzurufen. Kein Merge ist autorisiert.
