# Change Record: Parent-CI-Provisioning-SonarQube-Cloud-Remediation

**Sprache:** [English](CR-20260801-ci-provisioning-sonar-remediation.md) | Deutsch

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | `CR-20260801-ci-provisioning-sonar-remediation` |
| Datum (UTC) | `2026-08-01` |
| Basis-Revision | `6b4aca18d390363764b96d85cd31969b9bb114a1` |
| Tracking | Aktuelles offenes SonarQube-Cloud-Inventar unter `ci/provisioning`: 21 `python:S3776`, 10 `python:S1192`, 3 `pythonsecurity:S6549`, 2 `python:S3358`, 1 `python:S1066`, 1 `python:S8786` sowie zwei Duplikatblöcke (25 Zeilen). Lokaler Record: `FND-SONAR-0030`. |
| Grenze | Nur Parent `ci/provisioning` und direkte Parent-Regressions-Tests. Framework, MRTS, beide Gitlinks, Workflow-Konfiguration, Scanner-Konfiguration und `master` bleiben unverändert. |

## Motivation und Problemstellung

Das ausgewählte aktuelle SonarQube-Cloud-Verzeichnis meldete 38 offene Source-
Zeilen in `ci/provisioning/components/prepare-runtime-components.py` und zwei
doppelte Report-Formatierungsblöcke. Der Provisioner ist sicherheitsrelevante
Build-Infrastruktur: Er liest Cache-Manifeste, verarbeitet konfigurierte Pfade
und URLs, bereitet Source-Trees und Archive vor, ruft Tools auf und
veröffentlicht Artefakte. Die Remediation entfernt daher die Ursachen für
Komplexität, wiederholte Literale, Bedingungen, reguläre Ausdrücke und
Duplikate, ohne Pfad-, Besitz-, Provenance-, Staging- oder Publish-Controls zu
schwächen.

## Akzeptanzkriterien

- Das aktuelle 38-Zeilen-Source-Inventar und beide Provisioning-seitigen
  Duplikatblöcke werden durch verhaltenserhaltenden, überprüfbaren Code ersetzt,
  nicht durch `NOSONAR`, Exclusions, Regeländerungen, Quality-Gate-Änderungen
  oder bloßes Verschieben von Code.
- Managed-Cache-Containment, Marker-Besitz, reine Legacy-Löschung, frisches
  Staging, atomare Veröffentlichung, HTTPS-/Provenance-Prüfungen,
  Framework-V3-Provenance-Validierung und connectorspezifische Runtime-Semantik
  bleiben wirksam.
- Fokussierte normale und negative Controls bestehen, einschließlich aller drei
  unabhängig konfigurierbaren Expat-Override-Pfade.
- Vor der Behauptung, dass das Inventar behoben ist oder das Verzeichnis keine
  neuen Issues oder Duplikatblöcke hat, wird eine frische SonarQube-Cloud-
  Analyse des exakten Draft-PR-Heads eingeholt.

## Implementierungsentscheidung und Begründung

Der große Provisioner wird an seinen bestehenden semantischen Grenzen zerlegt.
Kleine private Helper machen Cache-Manifest-Abgleich, Cache-Entry-Vorbereitung,
Archivvalidierung, Source-Hashing, Expat-Override-Behandlung,
ModSecurity-Vorbereitung, Connector-Planung, Report-Erzeugung und CLI-
Komposition einzeln lesbar. Wiederholte operative Dateinamen und Statuslabels
haben einen privaten Besitzer. Verschachtelte Connector-Ausdrücke sind
explizite Verzweigungen, während die Apache-Fehlerdiagnose begrenztes,
zeilenlokales Matching statt der früheren breiten Regex-Form verwendet.

Die Report-Darstellung wird mit privaten Formatierungs-Helpern zusammengesetzt,
bleibt aber für einen vollständigen repräsentativen Payload byteidentisch.
Damit werden die zwei Provisioning-seitigen Duplikatblöcke entfernt, ohne die
eigenständig verantwortete Evidence-Report-Implementierung zu verändern. Ein
stiller nichtnull Git-Submodule-Rückgabecode trägt jetzt einen expliziten
Fehlerstatus statt sich auf Diagnosetext zu verlassen; der Caller scheitert
auch bei leeren beiden Output-Streams geschlossen.

Die erste Exact-PR-Head-Analyse nach diesem größeren Refactoring meldete acht
weitere Source-seitige Maintainability-Issues im neu zerlegten Provisioner:
vier wiederholte Literale, zwei unbenutzte private Parameter, eine
verschachtelte Bedingung und einen redundanten NGINX-Protokollprofilparameter.
Der gleiche Kandidat gibt diesen Literalen nun jeweils einen privaten Besitzer,
entfernt die unbeobachteten Parameter, beendet einen fehlgeschlagenen Expat-
`autoreconf`-Schritt ohne Änderung der Verzweigungsreihenfolge und leitet das
NGINX-Buildprofil aus den bereits aufgelösten Protokollinputs ab. Diese
Nachbesserung erhält alle Cache-, Provenance- und Build-Contracts; sie ändert
weder Sonar-Regeln, Quality Gate, Exclusions noch Suppressions.

Der nächste SonarQube-Cloud-Readback für den exakten PR-Head meldete zwei
S3415-Testdiagnosen in den zwei neu ergänzten Assertions: Sie übergaben den
Sollwert vor dem Istwert. Beide Aufrufe verwenden jetzt die frameworkübliche
Reihenfolge Istwert, Sollwert. Das korrigiert nur Diagnose- und
Reporting-Semantik; der getestete Expat-Fehler- beziehungsweise NGINX-
Profilvertrag bleibt unverändert. Der Hosted-Rerun für den exakten Head bleibt
vor einer Verifikationsaussage erforderlich.

## Security-Auswirkung

Keine Vertrauensgrenze wird gelockert. Manifest-Pfadwerte werden nur als Daten
verglichen; Dateisystem-Löschung, Veröffentlichung, Kopie,
Verzeichniserzeugung und Build-Sinks erfordern weiterhin Managed-Root-
Containment und Besitzmarker. Git- und Archiv-Eingaben behalten URL-, Ref-,
Digest-, Lock-, Staging-, Clean-Tree-, Submodule- und `git fsck`-Prüfungen vor
der Veröffentlichung. Der Framework-V3-Provenance-Guard läuft weiterhin vor
allen ModSecurity-Build-Sinks, und die Veröffentlichung des normalen Prefix
geht weiterhin der Build-Root-Veröffentlichung voraus.

Die Expat-Controls belegen jetzt `EXPAT_PREFIX`, `EXPAT_BUILD_DIR` und
`EXPAT_SOURCE_COPY` getrennt: Ein legitimes markiertes Managed-Child wird
akzeptiert, während ein externer Pfad, kanonische Traversal und Symlink-Escape
vor Build oder Veröffentlichung abgewiesen werden. Ein abgeschlossener
Baseline-Scoped-Security-Scan fand kein reportbares Issue; der erforderliche
Post-Change-Security-Diff-Review bleibt als separate Exact-Diff-Verifikation
bestehen.

## Geänderte Dateien

- `ci/provisioning/components/prepare-runtime-components.py`
- `tests/test_prepare_runtime_components.py`
- `tests/test_runtime_component_cache_contract.py`
- `reports/audits/change-records/README.md` und `README.de.md`
- dieses englische/deutsche Change-Record-Paar

## Ausgeführte Befehle

| Befehl | Ergebnis |
| --- | --- |
| `PYTHONDONTWRITEBYTECODE=1 PYTHONNOUSERSITE=1 /root/git/ModSecurity-conector/.venv/bin/python -m unittest -v tests.test_prepare_runtime_components tests.test_runtime_component_cache_contract tests.test_runtime_component_cache_identity tests.test_runtime_env_snapshot_contract tests.test_runtime_artifact_utils tests.test_runtime_path_policy` | bestanden: 90 fokussierte Provisioner-, Cache-, Environment-, Artefakt- und Path-Policy-Tests. |
| `PYTHONDONTWRITEBYTECODE=1 PYTHONNOUSERSITE=1 /root/git/ModSecurity-conector/.venv/bin/python -m py_compile ci/provisioning/components/prepare-runtime-components.py` | bestanden. |
| `make check-runtime-path-policy PYTHON=/root/git/ModSecurity-conector/.venv/bin/python` | bestanden. |
| `git diff --check` | vor Dokumentations-Autorenschaft bestanden; nach finalem Dokumentations-/Security-Review wiederholt. |

## Runtime-Evidence

Die Parent-gepinnte Framework-Revision wurde nur im isolierten Task-Worktree
als Test-Fixture initialisiert, sodass die fokussierten Parent-Tests die
normalen Cache-/Provisioning-Contracts ausführen können. Das änderte weder
Framework-Source noch MRTS-Source oder einen Gitlink. Kein echter
Netzwerk-Download, keine Paketinstallation und kein nativer Connector-Build
wurde in dieser Aufgabe ausgeführt; diese Schritte liegen außerhalb der
deterministischen lokalen Regression-Suite und benötigen eigene kontrollierte
Environment-Evidence.

## Exact-PR-Head-Delivery-Evidence

Zum Zeitpunkt der Record-Autorenschaft wird kein Commit, Push, Draft-PR,
Hosted-CI-Ergebnis oder Hosted-SonarQube-Cloud-Ergebnis behauptet. Die Aufgabe
ist auf einem isolierten Branch von der angegebenen Basis-Revision vorbereitet.
PR-Beschreibung und finale Delivery-Evidence müssen den exakten lokalen,
Remote- und PR-Head-SHA benennen und anschließend das frische Hosted-Ergebnis
für genau diesen Head festhalten.

## Nicht ausgeführte Prüfungen mit Begründung

- Ein vollständiger echter Provisioning-Build wurde nicht ausgeführt, weil er
  Third-Party-Runtime-Komponenten herunterlädt und baut; das wäre breiter als
  die geforderte statische Remediation und ist für die veränderten lokalen
  Contracts nicht erforderlich.
- Das breite `make lint`-Aggregat bestand lokal nicht. Mit beschreibbaren,
  task-eigenen Output-Roots erreicht es den unveränderten Apache-C17-Lintpfad
  und scheitert an bestehenden Warnings-as-Errors in
  `connectors/apache/src/mod_security3.c` und `connectors/apache/src/msc_config.h`.
  Derselbe Befehl erzeugt auf dem aktuellen Root-`master` dieselben Fehler,
  und diese drei Apache-Pfade haben keinen Diff zur Task-Basis. Das wird als
  externe Baseline-Einschränkung dokumentiert, nicht als bestandenes
  Provisioner-Lint-Ergebnis und nicht durch Schwächung von `-Werror` behoben.

## Bekannte Einschränkungen

Fokussierte lokale Tests und Source-Review belegen die geänderten Control-
Pfade, sind aber keine Hosted-SonarQube-Cloud-Analyse. Der finale
Post-Change-Security-Diff-Scan, der Bilingual-Dokumentationscheck, Commit,
Draft-PR und die Exact-Head-Hosted-Verifikation bleiben erforderlich, bevor
die Remediation als vollständig verifiziert gemeldet werden kann.

## Verbleibende Risiken

Der aktuelle projektweite SonarQube-Cloud-Backlog außerhalb von
`ci/provisioning` ist nicht Teil dieser Änderung. Die drei bestehenden
S6549-Alerts werden durch diesen Record nicht verworfen: Ihr behauptetes
Path-Escape-Ergebnis wird durch Source-/Sink-Review und dedizierte negative
Controls abgedeckt, während die Exact-PR-Head-Analyse noch ihre aktuelle
Hosted-Disposition bestimmen muss. Dieser Change Record autorisiert keine
Master-Integration.

## Finaler Diff- und Review-Status

Dies ist ein Pre-Delivery-Record für den isolierten Remediation-Kandidaten.
Sein finaler Status hängt von einem Exact-Head-Security-Review, finalem
scoped Diff-Check, lokaler Dokumentationsvalidierung und einer wahrheitsgemäßen
Draft-PR-Delivery ab. Er behauptet keine Merge-Bereitschaft und autorisiert
keinen Merge.
