# Change Record: CI-Connector-Profil-Literal-Deduplizierung für SonarQube Cloud

**Sprache:** [English](CR-20260723-sonar-ci-connector-profile-literals.md) | Deutsch

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | CR-20260723-sonar-ci-connector-profile-literals |
| Datum (UTC) | 2026-07-23 |
| Basis-Revision | Current integration base ec57576814a3f75c5e153d51c945bd1dd341a916; original source base a308d7b414f0859490fe7253e0683a4bde80b563. |
| Tracking | FND-SONAR-0021; drei aktuelle SonarQube-Cloud-python:S1192-Befunde AZ9cRyWgHhV2CayPTPuj, AZ9cRyWgHhV2CayPTPuk und AZ9cRyWgHhV2CayPTPul. |
| Grenze | Parent-CI-Dokumentationslayout-Checker, dieses englisch/deutsche Change-Record-Paar und seine Indizes. Framework, MRTS, Gitlinks, Profilmitgliedschaft, Runtime-Code, Scanner-Konfiguration, Quality Gates, Suppressions, Exclusions, Issue-Status und Default-Branch bleiben unverändert. |

## Motivation und Problemstellung

Der Connector-Profil-Layout-Checker wiederholte dieselben README-, Detection-
Only-Rule- und Engine-Off-Rule-Pfade für alle sechs Connector-Tupel. Die daraus
entstehenden S1192-Befunde sind Maintainability-Issues, während die Profilsets
selbst beabsichtigte connector-spezifische Validierungsverträge sind.

## Akzeptanzkriterien

- Die drei wiederholten Pfadliterale sind an eng benannte unveränderliche
  Modulkonstanten gebunden und nicht mehr über Connector-Tupel wiederholt.
- Jedes Required-File-Tupel für Apache, NGINX, HAProxy, Envoy, Traefik und
  lighttpd löst zu exakt denselben Werten wie in der Basisrevision auf.
- Direkte Detection-Only-, Engine-Off- und Strict-Reference-Checks verwenden
  dieselben Konstantenwerte.
- Connector-Konfigurationsgenerator und Checker bestehen weiterhin.
- Keine Profilmitgliedschaft, Validation-Message, Rule, kein Quality Gate,
  keine Exclusion, Suppression, kein NOSONAR und kein Issue-Status werden
  geändert.
- Frische Exact-Head-SonarQube-Cloud- und Hosted-Evidence ist erforderlich,
  bevor die drei Befunde für die geschützte Integration als verifiziert gelten.

## Implementierungsentscheidung und Begründung

Das Modul bindet jetzt PROFILE_README, DETECTION_ONLY_RULES und ENGINE_OFF_RULES
einmal und verwendet sie in allen sechs Profil-Tupeln sowie den direkten Checks.
Die Werte bleiben README.md, rules/detection-only.conf und rules/engine-off.conf.

Ein AST-Mapping von Base zu Kandidat vergleicht das vollständige Required-File-
Dictionary statt nur Textvorkommen zu zählen. Es beweist, dass alle sechs
Connector-Tupel vor und nach dem Refactoring dieselben aufgelösten Pfadwerte
haben.

## Geänderte Dateien

- ci/checks/documentation/check-connector-config-reference.py
- reports/audits/change-records/README.md und README.de.md
- dieses englisch/deutsche Change-Record-Paar

## Security-Auswirkung

Dies ist als Runtime-Security-Modifikation nicht anwendbar. Der statische
Checker löst weiterhin dieselben repository-relativen Profilpfade auf und führt
dieselben Datei-/Content-Validierungen durch. Kein Parser, Runtime-Path-Sink,
Befehl, Permission-, Authentisierungs-, Isolations- oder Scanner-Control ändert
sich.

## Ausgeführte Befehle

- Fokussiertes make check-connector-config-reference: vor und nach dem
  Constants-only-Change bestanden; der Generator meldet 21 aktuelle generierte
  Dateien und der Checker alle sieben Vertragsbereiche bestanden.
- In-Memory-Profil-Mapping von Base zu Kandidat: für alle sechs Connector-Tupel
  und die drei Konstantenwerte bestanden.
- git diff --check: für den Source-only-Kandidaten vor dem Hinzufügen dieses
  Record-Paars bestanden.

## Runtime-Evidence

Das Target ist ein statischer CI-Dokumentationslayout-Checker. Es validiert
committete Profildateien und Rule-Contents; keine Live-Connector-, Framework-,
MRTS- oder Production-Runtime wird beansprucht.

## Validierungsstatus

Der fokussierte Checker und das Profil-Mapping bestehen auf dem aktuellen
Integrations-Head. Das Mapping beweist, dass alle sechs Required-File-Tupel und
die drei direkten Pfadprüfungen nach der Konstantensubstitution ihre exakten
Werte behalten. Gezielte bilinguale Dokumentation, finaler Scoped-Diff und
Exact-Head-Hosted-Delivery-Evidence bleiben vor der geschützten Integration
erforderlich.

## Bekannte Einschränkungen und Follow-up

Dieser Record deckt nur drei aktuelle Parent-S1192-Befunde in einem CI-Checker
ab. Er beansprucht nicht, dass die projektweite 1.474-Item-Inventur oder andere
CI-, Common-, Scripts-, Tests- oder Connector-Befunde behoben sind.

## Verbleibende Risiken

Die Werte bleiben absichtlich unverändert. Das verbleibende Delivery-Risiko ist
extern: Eine frische Exact-Head-SonarQube-Cloud-Analyse und Hosted-Checks müssen
den aktualisierten PR verifizieren, bevor die Befunde als verified markiert
werden.

## Nicht ausgeführte Prüfungen mit Begründung

- Kein Framework- oder MRTS-Test und keine -Änderung: Beide liegen außerhalb
  des Scopes.
- Keine Live-Connector-Runtime: Das Verhalten des statischen Checkers wird
  direkt durch sein fokussiertes Target ausgeübt.
- Exact-Head-Hosted-Checks und SonarQube-Cloud-Analyse: nach dem Push des
  normalen Parent-Branch-Updates und vor der geschützten Integration
  erforderlich.

## Delivery-Status

Der Kandidat wurde auf einem isolierten Parent-Task-Branch normal aus der
festgehaltenen aktuellen Integrationsbasis aktualisiert. Er darf für frische
Exact-Head-Validierung zu seinem bestehenden Draft-PR gepusht werden. Eine
geschützte Squash-Integration ist erst nach erfolgreichen anwendbaren
Exact-Head-Checks, SonarQube-Cloud-Ergebnis, Review-Status und aktueller
Basisverifikation autorisiert. Direkte Default-Branch-Updates, Rebase,
Force-Push und Framework-/MRTS-Changes bleiben verboten.

## Finaler Diff- und Review-Status

Der finale Current-Base-Diff führt drei unveränderliche Konstanten ein und
ersetzt ihre passenden Verwendungen; er ändert weder Profilwerte noch
Validation-Flow. Der fokussierte Checker, das statische Profil-Mapping und der
lokale Diff-Review bestanden. Frische Exact-Head-Hosted-Delivery-Evidence
bleibt erforderlich; dieser Record behauptet keinen vorzeitigen Quality-Gate-
oder PR-Status.
