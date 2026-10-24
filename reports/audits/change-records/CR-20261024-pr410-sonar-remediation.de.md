# Change Record: CR-20261024-pr410-sonar-remediation

**Sprache:** [English](CR-20261024-pr410-sonar-remediation.md) | Deutsch

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | CR-20261024-pr410-sonar-remediation |
| Datum (UTC) | 2026-10-24 |
| Basis-Revision | `e509db65601057154c184757e2632e65b9dad403` |
| Start der letzten Reparatur | `a1edb5c9b3722eec8c6911345d3315dd82eb145a` |

## Motivation und Problemstellung

PR #410 enthielt noch eine Sonar-Schwachstelle, zwölf Smells, lokale
Lifecycle-Fehler und Apache-CI-Fixturefehler. Die angesammelte Dokumentations-
und Reporthistorie verdeckte zusätzlich die aktuelle Prüffläche. Nach der
vorherigen Reparatur verblieben für diese letzte gezielte Runde ein MINOR-Smell,
ein lokaler Apache-Guard-ERROR und ein davon abhängiger NOT_REACHED-Fall.

## Akzeptanzkriterien

Die benannten Ursachen ohne schwächere Kontrollen reparieren; eine vorab
deklarierte Auswahl von höchstens 100 aktiven Szenarien ohne Retry ausführen;
den tatsächlichen PR-Diff reduzieren; Framework/MRTS erhalten; nur
wahrheitsgetreue Exact-Head-Nachweise veröffentlichen.

## Implementierungsentscheidung und Begründung

Private HAProxy-Captureausgabe nutzt jetzt eine feste externe Grenze,
vertrauenswürdige Vorfahren, ein exklusives 0700-Blatt und deskriptorgebundene
0600-Receipts. Fokussierte Refactorings beseitigen die zwölf Smell-Ursachen.
Testwurzeln und SDK-Includeauswahl sind an ihren Ownern korrigiert. Historische
Prosa/Ergebnisse werden extern archiviert statt im PR erhalten. Der letzte Smell
wird mit einer verhaltensgleichen Dictionary-Comprehension beseitigt. Der
Apache-Guard kopiert den exakten Registry-hashgebundenen Framework-Fall in seine
private Testwurzel; produktive Pfadfreigaben bleiben unverändert, und negative
Assertions benennen nun ihre vorgesehenen Ablehnungszweige.

## Geänderte Dateien

Die fokussierten Änderungen betreffen HAProxy-Capturehelper,
Envoy-/Apache-/Traefik-Harnesskontrollen, native Observer-Tests, den Apache-
C-Probe, kompakte EN/DE-Dokumentation und einen Change Record. Die letzte
Reparatur ändert zusätzlich nur
`connectors/apache/harness/apache_oracle_overrides.py`,
`tests/test_apache_header_semantics.py`, dieses kompakte EN/DE-Abschlusspaar und
dieses Change-Record-Paar. Zehn maschinenverbrauchte Reporteingaben bleiben aus
dem integrierten PR erhalten.

## Ausgeführte Befehle

RTK umhüllte Git-Inspektion, Python-Kompilierung, Go-Format-/Listingprüfung,
C17-Syntaxprüfung, JSON-/Shell-Preflight, den einzigen koordinierten
Abschlussrunner und Dokumentations-/Diffprüfungen. Es gab keinen ungeschützten
Fallback. Die letzte Reparatur nutzte RTK-umhüllte Sonar-Auslesung,
Python-Kompilierung, JSON-/Shell-/Hash-/Zähl-Preflight und genau einen
Vier-Methoden-unittest-Aufruf über
`rtk bash /var/tmp/codex/ModSecurity-conector/pr410-last-repair-20261024/run-closeout.sh`.

## Security-Auswirkung

Der plausible öffentliche Temp-Ausgabepfad ist ohne Ausnahme oder
Unterdrückung geschlossen. Fokussierte statische Prüfung fand keine relevante
Regression. Es gab keinen Deep Scan, keine Policyabschwächung, keine Änderung
der Secretbehandlung und keine neue Vertrauenswurzel. Die letzte Test-Fixture
bleibt unter einer privaten testeigenen Wurzel und prüft die echten
Framework-Bytes vor Nutzung gegen die bestehende Registry-SHA.

## Runtime-Evidence

Der frühere erhaltene Lauf bleibt bei 73/75 PASS mit einem ERROR und einem
NOT_REACHED. Der separat autorisierte letzte Reparaturlauf
`pr410-last-repair-20261024-final-001` band Start-Head
`a1edb5c9b3722eec8c6911345d3315dd82eb145a` an den ausführbaren Patch mit SHA-256
`2e3681297d924921b82449b82da7675ce4dee0f35d3f968989af0401ec683057`.
Alle vier Methoden / 13 expandierten aktiven Szenarien bestanden, ohne Retry.
Ergebnis-SHA-256:
`f6d02a742713a9d1ec8cab5e399cdb52b32e198b798eaae00795940c20ec0fbf`.

## Bekannte Einschränkungen

Das letzte gezielte lokale Gesamtergebnis ist `PASS`. Dies ist keine vollständige
I12-/V08–V10-Hostabnahme und belegt keine repositoryweite Durchsetzung des
Default-Suite-Limits. `verified_pr` hängt weiterhin von automatischer
Exact-Head-CI/Sonar- und Review-Auslesung ab.

## Verbleibende Risiken

Automatische Final-Head-CI/Sonar kann umgebungsspezifische oder Scannerergebnisse
offenlegen. Vollständige Host-/Protokoll- und blockierte Deploymentnachweise
bleiben außerhalb dieses reduzierten Abschlusses.

## Nicht ausgeführte Prüfungen mit Begründung

Kein zweiter letzter Reparaturlauf, keine historische Matrix, Oracle-Kampagne,
tiefer Security-Scan, Veröffentlichung, Bereitstellung oder Zusammenführung lief.
Die Retryzahl ist null; Providerchecks starten erst vom gepushten Final-Head.

## Finaler Diff- und Review-Status

Unabhängige statische Reviews fanden nach den Dokumentationskorrekturen keine
Quellregression. Gegenüber der tatsächlichen PR-Basis ist der
Docs-/Report-Anteil von 193 auf 25 geänderte Dateien reduziert. Der letzte
gezielte lokale Lauf besteht; der PR bleibt Draft, solange die automatische
Exact-Head-Prüfung aussteht.
