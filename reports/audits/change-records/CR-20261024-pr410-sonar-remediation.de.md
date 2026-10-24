# Change Record: CR-20261024-pr410-sonar-remediation

**Sprache:** [English](CR-20261024-pr410-sonar-remediation.md) | Deutsch

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | CR-20261024-pr410-sonar-remediation |
| Datum (UTC) | 2026-10-24 |
| Basis-Revision | `e509db65601057154c184757e2632e65b9dad403` |

## Motivation und Problemstellung

PR #410 enthielt noch eine Sonar-Schwachstelle, zwölf Smells, lokale
Lifecycle-Fehler und Apache-CI-Fixturefehler. Die angesammelte Dokumentations-
und Reporthistorie verdeckte zusätzlich die aktuelle Prüffläche.

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
Prosa/Ergebnisse werden extern archiviert statt im PR erhalten.

## Geänderte Dateien

Die fokussierten Änderungen betreffen HAProxy-Capturehelper,
Envoy-/Apache-/Traefik-Harnesskontrollen, native Observer-Tests, den Apache-
C-Probe, kompakte EN/DE-Dokumentation und einen Change Record. Zehn
maschinenverbrauchte Reporteingaben bleiben aus dem integrierten PR erhalten.

## Ausgeführte Befehle

RTK umhüllte Git-Inspektion, Python-Kompilierung, Go-Format-/Listingprüfung,
C17-Syntaxprüfung, JSON-/Shell-Preflight, den einzigen koordinierten
Abschlussrunner und Dokumentations-/Diffprüfungen. Es gab keinen ungeschützten
Fallback.

## Security-Auswirkung

Der plausible öffentliche Temp-Ausgabepfad ist ohne Ausnahme oder
Unterdrückung geschlossen. Fokussierte statische Prüfung fand keine relevante
Regression. Es gab keinen Deep Scan, keine Policyabschwächung, keine Änderung
der Secretbehandlung und keine neue Vertrauenswurzel.

## Runtime-Evidence

Am eingefrorenen Head `251dc1263a2a67300b13daebd680c42bb8f4130c` wählte der
einzige lokale Lauf 75 aktive Szenarien: 73 PASS, null FAIL, ein ERROR und ein
NOT_REACHED. Python bestand 32/33 Methoden; die Go-Funktion bestand. Der
Apache-Fehler war eine lokale Cross-Worktree-Quellwurzelablehnung. Retryzahl: null.

## Bekannte Einschränkungen

Das lokale Gesamtergebnis ist `FAIL`. Dies ist keine vollständige
I12-/V08–V10-Hostabnahme, belegt keine repositoryweite Durchsetzung des
Default-Suite-Limits und darf nicht zu `verified_pr` hochgestuft werden.

## Verbleibende Risiken

Automatische Final-Head-CI/Sonar kann umgebungsspezifische oder Scannerergebnisse
offenlegen. Vollständige Host-/Protokoll- und blockierte Deploymentnachweise
bleiben außerhalb dieses reduzierten Abschlusses.

## Nicht ausgeführte Prüfungen mit Begründung

Kein zweiter Funktionslauf, keine historische Matrix, Oracle-Kampagne, tiefer
Security-Scan, Veröffentlichung, Bereitstellung oder Zusammenführung lief. Ein
Retry war ausdrücklich verboten; Providerchecks dürfen erst vom gepushten
Final-Head starten.

## Finaler Diff- und Review-Status

Unabhängige statische Reviews fanden nach zwei Dokumentationskorrekturen keine
Quellregression. Der Docs-/Report-Anteil ist von 482 auf 36 geänderte Dateien
reduziert; der PR bleibt Draft, weil der eine lokale Abschlusslauf nicht bestand.
