# Change Record: CR-20261102-master-reconcile

**Sprache:** [English](CR-20261102-master-reconcile.md) | Deutsch

Geprüfte Teiländerung mit ausdrücklich erfassten offenen Nachweisen.

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | CR-20261102-master-reconcile |
| Datum (UTC) | 2026-11-02 |
| Basis-Revision | `430d3194fa04ca4aafcdaef6aeb256d21dc18f0c` |

## Motivation und Problemstellung

Veraltete Framework-Anbindungsidentität, Apache-Dokumentation und vererbte Policy-Metadaten abgleichen sowie aktuelle Nachweislücken prüfbar machen. Der Quellenabgleich trennt tatsächliches Verhalten von Zielrichtlinien und historischen Runtime-Belegen.

## Akzeptanzkriterien

Einen geprüften, bereits integrierten Framework-Commit konsistent in Gitlink, Lock und festen Workflow-Projektionen verwenden; Apache-Verhaltensaussagen EN/DE korrigieren; geprüfte Inheritance-Änderungen validieren; echte Coverage, begrenztes Dependency-Inventar und unangewendete Regelvorlagen liefern. Die PR440-Korrektur übernimmt nach den getrennten Framework-/MRTS-Merges eine tatsächliche integrierte Framework-Revision; neue gehostete CI am Head muss das entstandene Paar qualifizieren.

## Implementierungsentscheidung und Begründung

Ursprüngliche Auswahl war Framework91145b7. Die CI-Korrektur für PR440 wählt integriertes Framework03fa02bacfc327863d91723fdc77a4888a33f0a8 einschließlich separat gemergter155/159/162/158/163 und MRTS75394f9a687ca2f09fd7623b23ac527bba10d7d9 mit gemergtemMRTS5. Parent-Master1a1023b92eb30ef73546cd2a2c3e84b39d34a153 wird regulär in den PR-Branch übernommen. Sein irrtümlicher Framework158-Head vor dem Squasha26b028104b28ddd980290b5af7b3fb195c43f9a scheitert am unveränderten Ancestry-Guard; stattdessen wird die integrierte Identität gewählt. Framework164 an1b0885 bleibt ausgeschlossen, weil NGINX1.31.8 mit der unabhängig geprüften1.31.6-Übergabe kollidiert. sync-framework-component-versions.py mit festem Zielregister statt pauschaler Stringersetzung verwenden. Parent-Python3.15.1 und Framework-Python3.15.2 behalten ihre unabhängig gepinnten Interpreterverträge. Policy-Quelltexte nach inhaltlicher Vererbungsprüfung erhalten; ausschließlich geprüfte Digests/Templates aktualisieren und die Host-Kontextanleitung korrigieren. Die getrennten Wartungsintegrationen werden ohne erneute Implementierung ihrer Quelländerungen übernommen;157 bleibt ungemergt geschlossen.

## Geänderte Dateien

Framework-Gitlink, ci/tooling/project-versions.lock.json und generatorverwaltete Framework-Action-/Workflow-Referenzen; docs/architecture.md und docs/connectors/apache.md mit deutschen Begleitdateien; .codex/context/security-runtime-preflight.md, Vererbungskatalog/Templates; reports/audits/master-reconcile-20261102/* und dieses Change-Record-Paar. Kein Connector-Runtime-Produktquelltext geändert.

## Ausgeführte Befehle

RTK-verpackte native Operationen: sync-framework-component-versions.py --sync/--check mit exakt ausgewähltem SHA und git-extrahierter common.sh unter RUNNER_TEMP; --check meldete keine Änderungen. Explizite On-Demand-Tests test_update_framework_versions und test_project_toolchain_pins:55 Tests bestanden. make check-bilingual-docs check-doc-links bestand vor letzten Berichtsdateien; abschließende Prüfungen sind im Abschlussnachweis erfasst. Parent-validate-codex-inheritance.py --check --repository parent bestand. Für die neu gewählte Revision meldet der native Projektionsgeneratorcheck keine Änderungen und die Kandidatenprüfung besteht; check-python-version-contract besteht (Python3.15.1,53 Jobs),94 bestehende Pin-/Toolchain-/Projektions-/Kandidatenregressionen bestehen (133,158s) und der aktualisierte Parent-Inheritance-Validator besteht. Alle aktiven gehosteten Checks und SonarCloud für gewähltes Framework03fa02b bestanden; neue gehostete CI am Parent-Head steht bei dieser Aktualisierung aus. Tatsächlich gemessene Werte/Herkunft stehen in coverage-summary.json; kein gesamter Python-PASS wird behauptet.

## Security-Auswirkung

Alle bestehenden Zulassungs-, Identitäts-, Socket-, Artefakt-, Compiler- und CI-Kontrollen erhalten. Die Sonar-Ausnahme ändert keine allgemeine Repository-Regel und kein GitHub-Workflow-Verhalten. Regel-JSONs sind ausschließlich Vorschläge. Quellen-/Advisory-Bewertung erfasst ungeklärte NGINX-/Envoy-/Python-Updatebetroffenheit und unvollständige native transitive Verlinkung statt Befundfreiheit zu behaupten. Keine Zugangsdatenwerte oder unbeschränkten Logs erfasst.

## Runtime-Evidence

Keine frische Connector-Host- oder H2/H3-Kampagne. Common-/gcov- und Go-Coverage belegen ausschließlich ausgewählte Testausführung. Die Host-Kontextanleitung benennt integrierten Preflight und echte Voraussetzungen desselben Kontexts; Belege vom2026-11-01 bleiben historisch.

## Bekannte Einschränkungen

Der Benutzer wählte gezielte Coverage-Messung mit dokumentierten Grenzen.
Die116 benannten Python-Tests und tatsächlichen Go-/Common-Messungen erfüllen
diesen Messumfang; Abschluss oder Wiederholung des vollständigen
Spezialassessments mit977 Ausführungen ist nicht erforderlich. Sein historischer
Abbruch und unabhängige Broker-, Runtime- und Dependency-Befunde bleiben
dokumentiert; CI-Prüfungen bleiben unverändert.

Gehostete Parent440-CI an38ebc633 lehnt vor ausgewählter Ausführung die
common.sh-Bindung des gewählten Framework91145 ab:156 änderte den Python-
Patchpin ohne Aktualisierung dieses Digests. Alle28 untersuchten einzeln
fehlgeschlagenen Jobs haben diese Zulassungsursache; das Fünf-Zellen-Aggregat
scheitert zusätzlich nach unvollständiger Aufbewahrung der Fehlerbelege.
Headgebundenes JSON und EN/DE-Abschlussnachweis erhalten Diagnosen und
Quelldigests. Framework159 regenerierte die Bindung mit dem bestehenden Werkzeug und ist
inzwischen separat gemergt sowie in gewähltem03fa02b enthalten; kein Guard wird
abgeschwächt. Der gemeldete Master-Run41470651827/Job125363368715 lehnt dagegen
korrekt die158-Identität vor dem Squash ab. Die PR440-Korrektur übernimmt
integriertes03fa02b und muss ihren neuen eingecheckten Head qualifizieren;
historische Nachweise bleiben unverändert.

Die vollständige Traefik-Auth-Vorbereitung scheitert weiterhin geschlossen an einem versiegelten Profil;10/19 historische Registry-Repository-Objekte weichen ab. Die vollständige Python-Spezialmessung scheiterte nach 56 abgeschlossenen Fällen am geschützten Aufrufervertrag; Timing wurde nicht erreicht. Der aktuelle dünne Parent-Wrapper ist mit dem historischen Inline-Zulassungsvertrag des unveränderlich gepinnten Brokers inkompatibel. Aktuelle Inheritance-Qualifikation der integrierten Kinder ist getrennt von der historisch fehlgeschlagenen Prüfung zu bewerten.

## Verbleibende Risiken

Aktuelle Hostqualifikation, vollständige native/Container-SBOM und Advisory-Analyse von Distributionspatches, geprüfte Runtime-Tupel-Builds, Sicht auf klassische Branch-Protection (HTTP 403) und neue gehostete CI-Qualifikation am Head bleiben offen. Bestehende grüne allgemeine CI schließt diese Lücken nicht.

## Nicht ausgeführte Prüfungen mit Begründung

Lokale Sonar-Secrets-Prüfung aufgrund ausdrücklicher Benutzeranweisung nicht ausgeführt. Keine lokale Sonar-Reparatur und keine verpflichtende Ersatzprüfung. Sonar-Analyseimport, vollständige H2/H3-Abnahme und frischer Hostlauf des endgültigen Merge-Paars wurden nicht ausgeführt; historische Messungen qualifizieren das neu gewählte Paar nicht. Administrative Vorlagen wurden wegen nötiger gesonderter Freigabe nicht angewendet.

## Finaler Diff- und Review-Status

Taskänderungen sind von bestehenden Checkouts/Worktrees isoliert. ParentPR440 bleibt ungemergt. Framework159 und der minimale reine MRTS-Test-PR5 wurden getrennt geliefert und anschließend durch andere Arbeiten integriert; ihre ursprünglichen Lieferidentitäten bleiben im Abschlussnachweis erhalten. Dieser Task führt keinen PR-Merge, Force-Push, direkten Master-/Main-Push oder Schutzregelwechsel aus; die reguläre Master-in-PR-Branch-Integration erhält die Historie. Gesamtergebnis bleibt partial bis zur Auflösung der erfassten Pflichtlücken.
