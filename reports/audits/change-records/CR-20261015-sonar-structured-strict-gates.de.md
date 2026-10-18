# Change Record: CR-20261015-sonar-structured-strict-gates

**Sprache:** [English](CR-20261015-sonar-structured-strict-gates.md) | Deutsch

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | CR-20261015-sonar-structured-strict-gates |
| Datum (UTC) | 2026-10-15 |
| Basis-Revision | `a311c725c44a7a4da95acb1a4818f66bd56c462a` |

## Motivation und Problemstellung

Die Provider-Zusammenfassung kann selbst bei erfolgreicher Analyse ausdrückliche Befundzahlen auslassen. Darstellungstext belegt keinen strengen Nullstand. Der bisherige Parser lehnte diese Form ab, ohne die offiziellen strukturierten PR-Belege auszuwerten.

## Akzeptanzkriterien

Aktueller GitHub-PR-Head, abgeschlossener erfolgreicher Sonar-Provider-Check und Commit der Sonar-PR-Analyse müssen vor und nach dem Abruf übereinstimmen. Erforderlich sind Quality Gate OK ohne ignorierte oder fehlgeschlagene Bedingungen, Security Rating A insgesamt und für neuen Code, null neue aktive/akzeptierte Issues, ein ausdrücklicher PR-Hotspot-Messwert null sowie alle drei exakten neuen Duplikationsmesswerte null. Fehlende, veraltete, unvollständige, mehrdeutige oder widersprüchliche Belege müssen scheitern.

## Implementierungsentscheidung und Begründung

Beide Gates nutzen denselben strengen strukturierten Verifier. Die offizielle Projekt-PR-Inventur liefert Commit-SHA und Analysedatum; PR-bezogenes Quality Gate, Messwerte und vollständig paginierte Issue-Inventuren liefern unabhängige Zahlen. Der unterstützte Issue-Filter lautet `sinceLeakPeriod=true`. Der veröffentlichte Hotspot-Suchvertrag bietet keinen PR-Bezug und wird deshalb nicht ersatzweise benutzt: Der ausdrückliche PR-Komponentenmesswert `new_security_hotspots` ist Pflicht; jeder positive Wert scheitert. Fehlende Messwerte werden niemals null.

JSON-Felder, Zahlenwerte, Seitensummen und Datensatzidentitäten werden geprüft. HTTP-Weiterleitungen werden abgelehnt; Antworten, Zeitlimits, Seitenzahlen und Diagnoseausgaben sind begrenzt. Duplikationsdiagnosen behalten Datei-/Blockbelege über denselben Client. Ein zweiter Provider-Abruf verwirft auch eine geänderte Conclusion bei unveränderter Check-ID und Ausgabe. Der Workflow übergibt beiden Gates die PR-Nummer.

## Geänderte Dateien

- `ci/checks/common/check-sonar-zero.py` und `check-sonar-duplication.py`.
- `tests/test_sonar_zero_gate.py` und `test_sonar_duplication_gate.py`.
- `.github/workflows/lint.yml`: ausdrückliche PR-Nummer für das Zero-Gate.
- Dieses EN/DE-Change-Record-Paar.

## Ausgeführte Befehle

Alle Shellbefehle im isolierten Shared-Gates-Worktree liefen über RTK. Mit Parent-Virtualenv und `PYTHONNOUSERSITE=1`, `PIP_REQUIRE_VIRTUALENV=true`, `PIP_DISABLE_PIP_VERSION_CHECK=1`:

- `rtk proxy .../.venv/bin/python -m unittest tests.test_sonar_zero_gate tests.test_sonar_duplication_gate`: 38 Tests PASS am 2026-10-18.
- Die neue Regression für einen Conclusion-Wechsel scheiterte vor der ergänzten Abschlussprüfung und bestand anschließend in der vollständigen fokussierten Suite.
- `tests.test_bilingual_docs tests.test_change_record`: 42 Tests PASS. Change-Record-Strukturprüfung, AST-Syntax für vier Python-Dateien und `git diff --check`: PASS. Die kombinierte Sonar-/Lint-/Workflow-/CI-Security-Suite bestand mit 67 Tests in 296,897 Sekunden, einschließlich der intern aufgerufenen Repository-Prüfung `make check-ci-security-contract`. Die separate Lint-/Workflow-Security-Kontrolle bestand mit 16 Tests.
- `rtk --version`, `rtk gain`, `rtk proxy which rtk`: PASS; RTK 1.0.1.

## Security-Auswirkung

Keine Quality Gates, Regeln, Ausschlüsse, Befundzustände oder Zugangseinstellungen werden gelockert. Nur offizielle Leseendpunkte mit festem Ursprung sind zugelassen. Clientfehler geben keine Zugangswerte, Header oder Antwortinhalte aus. Lokaler zugangsabhängiger Sonar-Zugriff unterliegt weiterhin dem kanonischen Wrapper `sonar-with-env`. Der Patch verändert keine Sonar-Zustände.

## Runtime-Evidence

Offline-Tests verwenden ausdrückliche strukturierte API-Formen und unabhängig gesteuerte Fehler. Sie prüfen veraltete Heads, gewechselte Analysen/Checks/Conclusions, fehlende und positive Messwerte, mehrdeutige Perioden, fremde Identitäten, unvollständige und doppelte Seiten, Annotationen, nicht unterstützte Filter, Weiterleitungen und Antwortgrenzen. Offizielle API-Vertragsbelege bleiben im externen Aufgabenverzeichnis `shared-gates` erhalten. Diese Prüfungen validieren Gateverhalten; sie belegen keine erfolgreiche gehostete Produktanalyse.

## Bekannte Einschränkungen

Der öffentliche Abruf setzt das konfigurierte öffentliche SonarCloud-Projekt voraus. Nicht unterstützte oder fehlende Belege scheitern geschlossen. Inventuren über 2.000 Datensätzen oder Antworten über 1 MiB erfordern gezielte Prüfung statt Teilabnahme. Der Hotspot-Beleg ist die ausdrückliche PR-bezogene Gesamtsumme null, da der veröffentlichte Suchendpunkt PR-Hotspots nicht unabhängig auflisten kann.

## Verbleibende Risiken

Der exakte endgültige veröffentlichte PR-Head benötigt weiterhin frische erfolgreiche GitHub- und Sonar-Abrufe. Eine historische erfolgreiche Zusammenfassung oder ein lokales Testergebnis erfüllt diese Abnahme nicht.

## Nicht ausgeführte Prüfungen mit Begründung

Dieser Quellpatch behauptet weder Scanner-Upload noch Live-Abnahme des endgültigen Heads. Produkt-Hosttests gehören zum integrierten Traefik-Evidenzlauf und liegen außerhalb dieser gemeinsamen Gateänderungen.

## Finaler Diff- und Review-Status

Beide Gateimplementierungen, Workflowbindung und fokussierte Tests wurden gegen den strengen Vertrag für den endgültigen Head geprüft. Der Conclusion-Wechsel bei gleicher Provider-ID wurde beim Abschlussreview reproduziert und behoben. Veröffentlichung und abschließende gehostete Prüfung verantwortet die übergeordnete Aufgabe.
