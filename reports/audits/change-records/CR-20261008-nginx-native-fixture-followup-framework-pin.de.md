# Change Record: CR-20261008-nginx-native-fixture-followup-framework-pin

**Sprache:** [English](CR-20261008-nginx-native-fixture-followup-framework-pin.md) | Deutsch

Reiner Framework-Folge-Pin; kein Runtime-Erfolg wird behauptet.

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | CR-20261008-nginx-native-fixture-followup-framework-pin |
| Datum (UTC) | 2026-10-08 |
| Basis-Revision | `ca8ac4b0598da65b178f670652047052cda7a531` |

## Motivation und Problemstellung

Die generische Framework-Discovery behandelte die ausschließlich native Reject-
Sourcefixture fälschlich als ausführbaren YAML-Case. Die fehlende generische
Erwartung wurde korrekt abgelehnt; fünf Fehler im bisherigen Parent-Fokus waren
die Folge. Eine separate Extraktion des Regular-File-Validators schließt das
verbleibende Sonar-Komplexitätsfinding.

## Akzeptanzkriterien

Den normal veröffentlichten, sauberen und getesteten Framework-Folgestand
pinnen. Alle 97 selektierten Required-Identitäten, die strikte Ablehnung fehlender
nativer Beweise und den MRTS-Gitlink erhalten. Source-Gates sind keine
Runtime-Akzeptanz.

## Implementierungsentscheidung und Begründung

Nur den Framework-Gitlink von
`61b9f33ad44fa92b916059d2f3e1944c6a4f1bf3` auf
`7db219af6b6e911b73de8b437f82e63efdb06bde` aktualisieren. Die rein native
Fixture wird von generischer Discovery ausgeschlossen, nicht vom Required-
Native-Vertrag. Die Extraktion erhält Eigentümer-, Modus-, Größen-, Byte- und
Digest-Prüfungen der regulären Datei. Beide Framework-Ursachen bleiben separate
Commits; keine Historie wird umgeschrieben.

## Geänderte Dateien

Gitlink `modules/ModSecurity-test-Framework` und dieses EN/DE-Record-Paar.

## Ausgeführte Befehle

Über RTK: Framework `make test-no-crs-contract`: 399 Tests in 178.376s,
Exit 0; vollständiger nativer `make lint`: terminaler Exit 0. Normaler Push und
Remote-Ref-Readback bestätigen den exakten neuen Framework-SHA. Die unabhängige
Analyse dieses SHAs schließt alle 16 verfolgten Findings; keine offenen/neuen
Issues, Duplikation 0.0% und Hotspots 0. Die beiden scaffold-lint-CI-Checks waren
beim letzten Readback noch offen.
Parent `make check-bilingual-docs check-doc-links`, Change-Record-Archivprüfung
und `git diff --check` bestanden mit Exit 0. Der verschachtelte Framework-
Checkout entspricht dem neuen Pin; das tatsächliche MRTS bleibt sauber und
unverändert bei `8a6bb546c4c81d8ffc7be801dceac60c6925685f`.

## Security-Auswirkung

Kein Validator, Evidence-, Ownership-, Containment-, Freshness-, Warnungs- oder
Quality-Gate wird gelockert. Selektierte Required-Native-Cases benötigen weiter
ihren ursprünglichen Runtime-Beweis; generische Fixture-Auslassung ist kein
nativer Erfolg.

## Runtime-Evidence

Keine aus diesem Pin. Alle 45 finalen Runtime-Lücken bleiben offen; das
ursprüngliche Canonical NOT_EXECUTED und die finale Run-Validierungszahl 0 bleiben
unverändert.

## Bekannte Einschränkungen

Der vollständige Parent-Fokus muss nach diesem Pin erneut laufen. Aktuelle
Source-Binary, Modul, echte Requests, Fault-Injection und vollständige kanonische
Evidence sind weiter erforderlich. Framework-CI-Abschluss ist von lokalem Lint
und Sonar getrennt.

## Verbleibende Risiken

Unerwartete Runtime-Artefaktaktualisierung muss im geplanten lokalen Lauf ohne
Egress geschlossen scheitern. Lokale Candidate-Evidence ist keine geschützte
Root-Attestation; unabhängige Trusted-Base-, Workflow-, Runner- und Host-Gate-
Voraussetzungen bleiben blockiert.

## Nicht ausgeführte Prüfungen mit Begründung

Vollständiger Post-Pin-Parent-Fokus, Full-E2E und geschützter Workflow liefen noch
nicht. Ruff bleibt nicht verfügbar; nativer Lint-Erfolg behauptet keine Ruff-
Validierung. Keine MRTS-, administrative Integrations-, Merge-, Retarget- oder
Undraft-Aktion wird vorgenommen.

## Finaler Diff- und Review-Status

Der Framework-Source-Diff wurde unabhängig und vom Koordinator geprüft; seine
vollständigen lokalen Gates sind grün, normale Veröffentlichung ist bestätigt.
Der Parent-Diff ist auf den neuen Gitlink und das Record-Paar begrenzt; die
finale Runtime-Arbeit bleibt offen.
