# Change Record: Parent-Response-Header-Fixture-Containment für SonarQube Cloud S8707

**Sprache:** [English](CR-20260727-sonar-response-header-fixture-containment.md) | Deutsch

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | CR-20260727-sonar-response-header-fixture-containment |
| Datum (UTC) | 2026-07-27 |
| Basis-Revision | 1b0f8825f3510b99b603bb6cd6f0777e1710358e |
| Tracking | SonarQube-Cloud-`pythonsecurity:S8707`-Receipt `AZ9cRyfJHhV2CayPTPxt` bei `ci/runtime/common/response-header-test-backend.py`, Fixture-File-Read-Pfad. |
| Grenze | Parent-Response-Header-Backend, fokussierter Parent-Regressionstest und dieses EN/DE-Change-Record-Paar. Framework/MRTS-Quelle, Gitlinks, Workflows, Report-Generierung, SonarQube-Cloud-Konfiguration, Suppressions, externer Issue-Status und Master bleiben unverändert. |

## Motivation und Problemstellung

Das Backend begrenzte `--body-file` bereits auf eine reguläre Datei in `--safe-root`, las `--fixture-file` jedoch über `Path.read_text` ohne dieselbe Containment-Prüfung. Ein Aufrufer mit Kontrolle über die lokale Backend-Invocation konnte eine lesbare JSON-förmige Datei außerhalb der beabsichtigten Runtime-Root auswählen. Da die Fixture begrenzten Response-Status/Header beeinflusst, ist dies ein realer Broken-Control-Pfad und kein kosmetisches Scanner-Signal.

## Akzeptanzkriterien

- Fixture-Reads lösen vor JSON-Read oder Listener-Start eine existierende reguläre Datei in expliziter Safe-Root oder im bestehenden CWD-Fallback auf.
- Traversal und ein In-Root-Symlink, der außerhalb der Safe-Root auflöst, werden abgewiesen.
- Eine gültige In-Root-Fixture bleibt zulässig und erbt nicht die Ein-Megabyte-Grenze für Body-Dateien.
- Die bestehende Body-File-Größe bleibt begrenzt.
- Header-Validierung, Listener-Reihenfolge, Framework/MRTS-Quelle, Gitlinks, Workflows, Scanner-Konfiguration, Suppressions und Master bleiben unverändert.

## Implementierungsentscheidung und Begründung

`resolve_regular_file` verallgemeinert den bisherigen Body-Resolver und bewahrt strikte Auflösung, Regular-File-, Containment- und optionale Größenprüfung. `resolve_body_file` übergibt weiter `MAX_BODY_BYTES`; `resolve_fixture_file` bewusst nicht. `load_fixture_file` löst vor `read_text` über die Kontrolle auf, und `main` übergibt geparste Safe-Roots. Fehler erreichen weiter `parser.error` vor der Serverkonstruktion.

## Geänderte Dateien

- ci/runtime/common/response-header-test-backend.py
- tests/test_response_header_backend_fixture_paths.py
- reports/audits/change-records/CR-20260727-sonar-response-header-fixture-containment.md
- reports/audits/change-records/CR-20260727-sonar-response-header-fixture-containment.de.md
- reports/audits/change-records/README.md
- reports/audits/change-records/README.de.md

## Ausgeführte Befehle

```sh
rtk proxy env PYTHONDONTWRITEBYTECODE=1 PYTHONNOUSERSITE=1 /root/git/ModSecurity-conector/.venv/bin/python -B -m unittest -v tests.test_response_header_backend_fixture_paths tests.test_response_header_backend.ResponseHeaderBackendTest.test_backend_uses_declarative_status_and_marker_header tests.test_response_header_backend.ResponseHeaderBackendTest.test_invalid_fixture_headers_are_rejected_before_listening tests.test_response_header_backend.ResponseHeaderBackendTest.test_both_host_harnesses_use_the_fixture_for_any_response_headers_rule
rtk proxy git diff --check
```

## Tests und tatsächliche Ergebnisse

| Kommando oder Check | Ergebnis |
| --- | --- |
| Fokus-Fixture-/Backend-Kontrollen | bestanden: 8 Tests. |
| Legitime In-Root-Fixture | bestanden: deklarativer Status und Marker-Header bleiben geliefert. |
| Unsicherer absoluter Fixture-Pfad | bestanden: vor Listener-Start abgewiesen. |
| Parent-Traversal-Fixture-Pfad | bestanden: nach striktem kanonischem Containment abgewiesen. |
| In-Root-Symlink zu Outside-Fixture | bestanden: durch aufgelöstes Containment abgewiesen. |
| Kompatibilität | bestanden: gültige große Fixture bleibt zulässig; Body-Dateien bleiben begrenzt. |
| Vorhandene invalide Header- und Host-Harness-Fixture-Wiring | bestanden. |
| `git diff --check` | bestanden: keine Whitespace-Fehler. |

## Security-Auswirkung

Der Baseline-Source-to-Sink-Pfad ist validiert: CLI-`--fixture-file` floss ohne bestehende Safe-Root-Kontrolle zu `Path.read_text`. Der Kandidat nutzt nun vor dem Sink striktes kanonisches Containment und Regular-File-Test, weshalb relative Traversals und Symlink-Outside-Root-Ziele scheitern. Der Harness ruft das Backend mit harness-eigener `--safe-root` und Fixture unter dieser Runtime-Root auf. Request-Parsing, Header-Validierung, Netzwerkexposition und Body-File-Grenzen werden nicht geändert.

Es bleibt ein pathname-TOCTOU-Aspekt, wenn ein Angreifer eine In-Root-Datei nach Validierung, aber vor dem späteren pathname-Read ersetzen kann. Dieses Modell eines feindlichen gleichzeitigen Schreibers liegt außerhalb des belegten harness-eigenen Runtime-Root-Vertrags und wird nicht als global geschlossene Descriptor-Level-Garantie ausgegeben. Kein Sicherheitsbefund wird vor beobachteter Exact-Head-Analyse geschlossen.

## Dokumentationsstatus

Dieses EN/DE-Change-Record-Paar dokumentiert validierte Baseline, Kandidatenkontrolle, exakte lokale Checks, Kompatibilitätsentscheidung und Residuumsumfang. Beide Change-Record-Indizes sind aktualisiert.

## Runtime-Evidence

Die fokussierten Tests üben nur lokales Python-Backend und statisches Host-Harness-Fixture-Wiring aus. Keine breite Connector-Runtime-Matrix oder Produktion wurde ausgeführt oder behauptet.

## Bekannte Einschränkungen

Das vollständige Modul `tests.test_response_header_backend` enthält Framework-abhängige Metadatenfälle außerhalb dieser engen Path-Control-Änderung und war nicht erforderlich, um die geänderte Read-Grenze auszuüben. Gehostete GitHub- und SonarQube-Cloud-Analyse haben den Kandidaten noch nicht geprüft.

## Verbleibende Risiken

Die Sicherheit des No-`--safe-root`-CWD-Fallbacks hängt weiterhin von einem vertrauenswürdigen engen Working-Directory ab, wie es vor dem Kandidaten für Body-Dateien galt. Ein feindlicher Schreiber der harness-eigenen Runtime-Root benötigte einen getrennten Descriptor-Relative/No-Follow-Entwurf und explizite Lifecycle-/Ownership-Evidence. Der Kandidat trifft keine Aussage über weitere aktuelle S8707-Inventory-Zeilen oder den 1.022-Item-Backlog.

## Nicht ausgeführte Prüfungen mit Begründung

- Vollständige Connector-Builds, Runtime-Matrizen, Framework/MRTS-Tests und Report-Generierung sind für diese enge Parent-Backend-Grenze nicht anwendbar.
- Gehostete GitHub-Checks und die exakte SonarQube-Cloud-Head-Analyse sind offen. Dieser Record gibt weder externes Issue-Closure noch Master-Merge-Autorisierung.

## Finaler Diff- und Review-Status

Der Kandidat enthält nur die kleinste Parent-Path-Control-Reparatur, direkte Negative-/Kompatibilitätsregressionstests und zweisprachige Traceability. Eine unabhängige Securityreview bewertete die Baseline-Control-Lücke als validiert und den Kandidaten unter der Harness-Owned-Root-Annahme als geeignet. Commit-, Push-, PR-, gehostete Checks-, externe Sonar-Disposition- und Merge-Fakten werden erst nach Beobachtung ergänzt.
