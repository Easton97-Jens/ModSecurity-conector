# Change Record: Wiederkehrenden Change-Record-Vertragsfehlern vorbeugen

**Sprache:** [English](CR-20260929-change-record-prevention.md) | Deutsch

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | CR-20260929-change-record-prevention |
| Datum (UTC) | 2026-09-29 |
| Basis-Revision | `d62e0427a1cdbe4e4f0f95dec8053187046dfc6e` |

## Motivation und Problemstellung

Der Benutzer hat eine Vorbeugung gegen wiederkehrende Change-Record-CI-Fehler
und die Behebung der SonarQube-Befunde in PR #393 angefordert. Die vorherige reine
Dokumentationskorrektur beseitigte 19 Überschriften-/Identitätsmeldungen; die
Nachvollziehbarkeitsrichtlinie empfahl jedoch weiterhin Synonyme, die der
unveränderte Bilingual-Prüfer nicht akzeptiert. Diese Folgeänderung beseitigt
die Fehlerquelle beim Verfassen, statt den Prüfer abzuschwächen.

## Akzeptanzkriterien

Der neue Generator muss beide Sprachvorlagen aus dem bestehenden Prüfer ableiten,
sie vor dem Schreiben validieren und vorhandene Dateien erhalten. Die Richtlinie
muss die exakt geprüften Überschriften und Identitätsbezeichnungen aufführen.
Eine lesende Archivprüfung samt Regressionen muss in quick-framework-check vor
dem Framework-Setup laufen. Vollständige Prüfungen, Berechtigungen, Pins und
Repository-Grenzen bleiben unverändert. Die gesonderte Behebung der zwei
Sonar-Befunde bleibt blockiert, bis ihre tatsächlichen Regeln und Fundstellen
abgerufen werden können; dieser Record behauptet keine Erfüllung dieses Ziels.

## Implementierungsentscheidung und Begründung

Einen Generator und Frühprüfer allein mit der Standardbibliothek ergänzen.
Der Generator lädt den repository-eigenen Bilingual-Prüfer über seinen festen
benachbarten Pfad, leitet Überschriften und Identitätsbezeichnungen aus dessen
bestehenden Konstanten ab und ruft vor dem Öffnen der Ausgaben dessen vorhandene
Paar-/Strukturprüfungen auf. Namen, Daten und vollständige Basis-SHAs werden
validiert. Vorhandene Archivverzeichnisse werden über Verzeichnisdeskriptoren
und No-Follow-Flags geöffnet; exklusive Dateierzeugung überschreibt keine Records.
Bei einem behandelten Erzeugungsfehler entfernt der Rollback nur Ausgaben, deren
gespeicherte Geräte-/Inode-Identität weiterhin übereinstimmt. Eine absturzatomare
Erzeugung beider Dateien wird nicht garantiert.

Die frühe lesende Prüfung verwendet dieselben Prüferfunktionen und lehnt auch
fehlende Begleitdateien und Symlink-Dateien ab. Sie prüft die Struktur, nicht die
Qualität der beschriebenen Evidence. Die Richtlinie in beiden Sprachen korrigieren
und ihre Literaltabellen gegen dieselben kanonischen Definitionen testen.
Der bestehende Workflow erhält einen lesenden Schritt für Archivprüfung und
beide Testmodule vor make setup-dev. Vollständiger quick-check und vorhandene
Dokumentationsprüfungen bleiben erhalten.

## Geänderte Dateien

- `ci/tools/new-change-record.py`
- `tests/test_change_record.py`
- `docs/change-traceability.md`
- `docs/change-traceability.de.md`
- `.github/workflows/quick-framework-check.yml`
- `reports/audits/change-records/CR-20260929-change-record-prevention.md`
- `reports/audits/change-records/CR-20260929-change-record-prevention.de.md`

## Ausgeführte Befehle

Die In-Process-Validierung unter Python 3.13.5 in einem isolierten Fixture bestand
alle 39 Tests: 20 neue Change-Record-Tests und die 19 unveränderten Tests des
Handoff-Generators. Die neuen Tests verwendeten die aus dem abgerufenen Quelltext
extrahierten einschlägigen unveränderten Prüferdefinitionen, keinen vollständigen
Repository-Checkout. Die ursprünglichen Richtlinien-/Workflow-Dateien und die
unveränderten Handoff-Quell-/Testdateien wurden anhand ihrer Git-Blob-Hashes geprüft.

Vor der Richtlinien-/Workflow-Korrektur fand die Regression 60 fehlende kanonische
Überschriften-/Bezeichnungsliterale in den beiden Richtlinien; der frühe
Workflow-Schritt fehlte ebenfalls. Danach bestanden alle 39 Tests. Negativfälle
prüfen jede Pflichtüberschrift und Identitätsbezeichnung, abweichende Identitäten,
Sprach-/Code-Parität, ungültige Eingaben, vorhandene Ausgaben, Symlink-Pfade,
Rollback, fehlende/leere Archive und Schemaabweichungen. AST-Parsing, Leerzeichen/
abschließende Zeilenumbrüche und die EN/DE-Strukturparität der Richtlinien
bestanden. YAML-Parsing bestätigte, dass nach Entfernen des einzigen zusätzlichen
Schritts exakt die ursprüngliche Workflow-Konfiguration entsteht.

Die folgenden Befehle sind projektnative Validierungspayloads für den echten
Checkout, keine Behauptung ihrer lokalen Ausführung über den fehlenden RTK-Wrapper:

```sh
python3 ci/tools/new-change-record.py check
python3 -m unittest -v tests.test_change_record tests.test_prepare_reviewed_framework_handoff
make check-bilingual-docs
make check-doc-links
git diff --check
```

## Security-Auswirkung

Keine Prüferregel, kein Quality Gate, Ausschluss, Unterdrückung, Berechtigung,
Abhängigkeits-Pin, Framework-/MRTS-Quelltext oder Gitlink wird geändert.
Der Helfer führt weder Shell-/Netzwerkbefehle noch Git aus. Die Erzeugung ist eine
ausdrückliche lokale Schreiboperation auf abgeleitete Record-Dateinamen in einem
vorhandenen vertrauenswürdigen Checkout; die CI ruft ausschließlich die lesende
Prüfung auf. Struktureller Erfolg ist keine Security-, Test-Evidence- oder
Runtime-Freigabe.

## Runtime-Evidence

Keine. Diese Änderung betrifft ausschließlich Verfassen und CI-Struktur.
Weder nativer Connector-Build noch Host-Laufzeit oder ursprüngliche
Framework-Handoff-Reparatur werden behauptet.

## Bekannte Einschränkungen

Der Generator benötigt POSIX-Unterstützung für Verzeichnisdeskriptoren und
No-Follow sowie ein vorhandenes Record-Verzeichnis. Seine Ausgabe enthält
absichtlich offene Texte, die durch tatsächliche Fakten ersetzt werden müssen.
Der Prüfer kann die Richtigkeit dieser Fakten nicht beweisen. Die isolierte
Validierung ist kein projektnativer oder gepinnter Python-3.14.7-Lauf.
Die ursprüngliche Framework-Kandidatenreparatur in PR #393 bleibt nur vorbereitet.

## Verbleibende Risiken

Künftige Autoren können den Generator weiterhin umgehen oder Pflichtüberschriften
ändern; die CI lehnt solche Records ab, statt sie stillschweigend zu normalisieren.
Ein Prozessabbruch zwischen den Erzeugungen kann ein unvollständiges Paar
hinterlassen, das die Frühprüfung ablehnt. Vollständiger Checkout, CI des aktuellen
Heads und Sonar-Ergebnisse benötigen eigene frische Evidence.

## Nicht ausgeführte Prüfungen mit Begründung

Kein lokaler vollständiger Checkout-Lauf, keine vollständige Bilingual-/Link-Suite,
kein gepinnter Python-Lauf und keine Sonar-Analyse wurden ausgeführt.
GitHub-DNS in der lokalen Umgebung, RTK, der kanonische sonar-with-env-Starter
und eine Sonar-CLI/MCP waren nicht verfügbar.

Der GitHub-Sonar-Check 109566898629 meldete an der oben genannten Basis-Revision
ein bestandenes Quality Gate mit zwei neuen Befunden. Die Verbindung lehnte
dessen Annotations-Endpunkt ab; verwertbare Regel-/Datei-/Zeilendetails waren
nicht verfügbar. Deshalb wurden keine spekulative Sonar-Quellkorrektur,
Unterdrückung oder Befund-Disposition vorgenommen. Ein bestandenes Gate beweist
nicht die Behebung dieser beiden Befunde.

## Finaler Diff- und Review-Status

Quelltext, Tests, Richtlinienpaar und der einzelne zusätzliche Workflow-Schritt
wurden vor Veröffentlichung im begrenzten Diff geprüft. Isolierte Tests und
Syntax-/Paritätsprüfungen bestanden. Nachfolgende gehostete Checks lagen beim
Verfassen dieses Records noch nicht vor. Die Sonar-Behebung bleibt blockiert;
die ursprüngliche Handoff-Reparatur bleibt unangewendet. Weder Merge noch
master-Schreibzugriff oder Umschreiben der Historie sind autorisiert.
