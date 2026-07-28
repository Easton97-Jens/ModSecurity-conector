# Change Record: Parent-Testfixture-Duplikatreduzierung für SonarQube Cloud

**Sprache:** [English](CR-20260727-sonar-parent-test-duplication.md) | Deutsch

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | CR-20260727-sonar-parent-test-duplication |
| Datum (UTC) | 2026-07-27 |
| Basis-Revision | 1b0f8825f3510b99b603bb6cd6f0777e1710358e |
| Tracking | Parent-Duplikatbaseline: 2.013 Zeilen und 0,4 Prozent. Kandidatenkomponenten: `tests/test_runtime_component_cache_contract.py` (187) und `tests/test_connector_capabilities.py` (38); Komponentenanzahlen können sich überlappen. |
| Grenze | Die beiden Parent-Testmodule und dieses EN/DE-Change-Record-Paar. Produktquelle, Tests/Assertions, Framework/MRTS-Quelle, Gitlinks, Workflows, generierte Reports, Sonar-Konfiguration, Suppressions, externer Issue-Status und Master bleiben unverändert. |

## Motivation und Problemstellung

Die aktuelle SonarQube-Cloud-Baseline meldet 0,4 Prozent Duplikatdichte. Die zwei gewählten Parent-Testmodule enthalten wiederholtes lokales Fixture-Setup, das Cache-Integritäts- und Framework-Provenance-Assertions verdeckt. Der Kandidat entfernt nur dieses wiederholte Setup; er entfernt, vereinigt oder schwächt keine Tests.

## Akzeptanzkriterien

- Jeder Test, jede Assertion, jeder Negativfall und jede Temporary-Root-Isolierung bleibt semantisch gleichwertig.
- Gemeinsame private Helfer bleiben in ihrer Testklasse und erhalten lokale Git-, erwartete Remote-, Clone/Fetch-, Cache- und Framework-Gitlink-Verträge.
- Produktimplementierung, Framework/MRTS-Quelle, Gitlinks, Workflows, generierte Reports, Sonar-Konfiguration, Suppressions und `master` bleiben unverändert.
- Die zwei vollständigen fokussierten Module, Dokumentationschecks und Diff-Hygiene bestehen.
- Eine neue exakte SonarQube-Cloud-Head-Analyse bestimmt die tatsächliche globale Duplikatreduktion.

## Implementierungsentscheidung und Begründung

`RuntimeComponentCacheContractTest` besitzt private Helfer für wiederholtes Expat-Fixture, lokales Upstream-Repository und Clone/Fetch-Interception. Einzelne Tests behalten Expected-Ref-, Fehler-, Mutations- und Assertion-Logik. `ConnectorCapabilitiesTest` besitzt einen lokalen Framework-Checkout-plus-Gitlink-Helfer; Matching-, Mismatch- und Stale-Record-Tests behalten ihre eigene Outcome-Einrichtung.

Es wird nur identisches Testgerüst extrahiert. Cache-Production, Source-Provenance, Framework-Validierung und Kontrollfallinhalt bleiben unverändert.

## Geänderte Dateien

- tests/test_runtime_component_cache_contract.py
- tests/test_connector_capabilities.py
- reports/audits/change-records/CR-20260727-sonar-parent-test-duplication.md
- reports/audits/change-records/CR-20260727-sonar-parent-test-duplication.de.md
- reports/audits/change-records/README.md
- reports/audits/change-records/README.de.md

## Ausgeführte Befehle

```sh
rtk proxy env PYTHONDONTWRITEBYTECODE=1 PYTHONNOUSERSITE=1 /root/git/ModSecurity-conector/.venv/bin/python -B -m unittest -v tests.test_runtime_component_cache_contract
rtk proxy env PYTHONDONTWRITEBYTECODE=1 PYTHONNOUSERSITE=1 /root/git/ModSecurity-conector/.venv/bin/python -B -m unittest -v tests.test_connector_capabilities
rtk proxy make check-bilingual-docs
rtk proxy make check-doc-links
rtk proxy git diff --check
```

## Tests und tatsächliche Ergebnisse

| Kommando oder Check | Ergebnis |
| --- | --- |
| `tests.test_runtime_component_cache_contract` | bestanden: 27 Tests. |
| `tests.test_connector_capabilities` | bestanden: 13 Tests. |
| Cache-/Provenance-Negativkontrollen | bestanden: clean/dirty/corrupt/moving Git-Checkout, vollständiges Manifest, Cache-Identität, Framework-Matching/Mismatch und Stale-Record-Verträge bleiben abgedeckt. |
| `git diff --check` | bestanden: keine Whitespace-Fehler. |

## Security-Auswirkung

Der Patch verändert nur Test-Fixture-Setup rund um Cache- und Provenance-Kontrollen. Er ändert weder Produkt-Command-Ausführung, Netzwerkzugriff, Safe-Root-/Pfadbehandlung, Cache-Validierungscode, Framework-/MRTS-Quelle noch eine Sicherheitskontrolle. Die fokussierten Module führen die erhaltenen lokalen Git- und negativen Provenance-/Cache-Verträge aus. Es wurde kein neuer Sicherheitsbefund identifiziert; gehostete Analyse ist noch offen.

## Dokumentationsstatus

Dieses EN/DE-Change-Record-Paar hält Umfang, tatsächliche Validierung und die Einschränkung fest, dass lokale Duplikatanzahlen nicht die globale SonarQube-Cloud-Kennzahl beweisen. Die Indizes sind in beiden Sprachen aktualisiert.

## Runtime-Evidence

Es wurde kein Runtime-Connector-, Protokoll-, Host-, Reportgenerator- oder Produktionsverhalten verändert oder behauptet. Die fokussierten Tests sind Testvertrags-Evidence, keine Connector-Runtime-Evidence.

## Bekannte Einschränkungen

Der isolierte Parent-Worktree initialisierte den bestehenden Parent-festgeschriebenen Framework-Gitlink `47e50e7bc43ba7a3b5bad1a9448111794f664cc0` nur, damit der Framework-abhängige Test laufen konnte. Framework-/MRTS-Quelle und Gitlinks blieben unverändert. SonarQube Cloud hat den Kandidaten nicht analysiert; eine beobachtete Reduktion gegenüber 0,4 Prozent darf daher nicht behauptet werden.

## Verbleibende Risiken

Ein künftiger Test könnte von einem Fixture-Detail abhängen, das die aktuellen fokussierten Module nicht abdecken. Private Helfer, pro Test erhaltene Outcome-Einrichtung und beide vollständigen Modulläufe mindern dieses Risiko. Der Kandidat trifft keine Aussage über andere Duplikatblöcke oder den 1.022-Item-Backlog.

## Nicht ausgeführte Prüfungen mit Begründung

- Connector-Builds, vollständige Runtime-Matrizen und MRTS-Tests sind nicht anwendbar: keine Produkt-/Runtime- oder Cross-Repository-Quelle änderte sich.
- Gehostete GitHub-Checks und die exakte SonarQube-Cloud-Head-Analyse sind noch nicht erfolgt. Dieser Record liefert weder ein globales Duplikatergebnis noch Master-Merge-Autorisierung.

## Finaler Diff- und Review-Status

Der Kandidat ist auf zwei Parent-Testmodule und zweisprachige Traceability begrenzt. Eine unabhängige Semantikreview ist vor Delivery erforderlich; Fakten zu Commit, Push, PR, Checks, Sonar-Analyse oder Merge werden erst nach Beobachtung dokumentiert.
