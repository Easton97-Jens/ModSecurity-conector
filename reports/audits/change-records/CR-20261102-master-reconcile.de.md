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

Einen geprüften, bereits integrierten Framework-Commit konsistent in Gitlink, Lock und festen Workflow-Projektionen verwenden; Apache-Verhaltensaussagen EN/DE korrigieren; geprüfte Inheritance-Änderungen validieren; echte Coverage, begrenztes Dependency-Inventar und unangewendete Regelvorlagen liefern. Die endgültige Übernahme neu korrigierten Framework-Codes erfordert dessen separat freigegebenen Merge und einen anschließenden Pin auf den exakten Merge-SHA.

## Implementierungsentscheidung und Begründung

Framework 91145b7ba721bdec4e89af754cf40bf496fd2a08 einschließlich integrierter TLS-Untergrenze#154 und Python-Patch#156 auswählen. sync-framework-component-versions.py mit festem Zielregister statt pauschaler Stringersetzung verwenden. Parent-Python 3.15.1 bleibt unabhängig von Framework 3.14.10. Policy-Quelltexte nach inhaltlicher Vererbungsprüfung erhalten; ausschließlich geprüfte Digests/Templates aktualisieren und die Host-Kontextanleitung korrigieren. Bestehende Wartungsarbeiten#155/#157/#158 bleiben getrennt.

## Geänderte Dateien

Framework-Gitlink, ci/tooling/project-versions.lock.json und generatorverwaltete Framework-Action-/Workflow-Referenzen; docs/architecture.md und docs/connectors/apache.md mit deutschen Begleitdateien; .codex/context/security-runtime-preflight.md, Vererbungskatalog/Templates; reports/audits/master-reconcile-20261102/* und dieses Change-Record-Paar. Kein Connector-Runtime-Produktquelltext geändert.

## Ausgeführte Befehle

RTK-verpackte native Operationen: sync-framework-component-versions.py --sync/--check mit exakt ausgewähltem SHA und git-extrahierter common.sh unter RUNNER_TEMP; --check meldete keine Änderungen. Explizite On-Demand-Tests test_update_framework_versions und test_project_toolchain_pins:55 Tests bestanden. make check-bilingual-docs check-doc-links bestand vor letzten Berichtsdateien; abschließende Prüfungen sind im Abschlussnachweis erfasst. Parent-validate-codex-inheritance.py --check --repository parent bestand. Tatsächlich gemessene Werte/Herkunft stehen in coverage-summary.json; kein gesamter Python-PASS wird behauptet.

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
Quelldigests. Framework159 regeneriert die Bindung mit dem bestehenden Werkzeug;
kein Guard wird abgeschwächt. Nach genehmigter Framework-Integration dessen
tatsächlichen Merge-Commit pinnen und das endgültige eingecheckte Paar qualifizieren.

Die vollständige Traefik-Auth-Vorbereitung scheitert weiterhin geschlossen an einem versiegelten Profil;10/19 historische Registry-Repository-Objekte weichen ab. Die vollständige Python-Spezialmessung scheiterte nach 56 abgeschlossenen Fällen am geschützten Aufrufervertrag; Timing wurde nicht erreicht. Der aktuelle dünne Parent-Wrapper ist mit dem historischen Inline-Zulassungsvertrag des unveränderlich gepinnten Brokers inkompatibel. Vollständige native Vererbungsprüfung gegen derzeit eingebettetes Framework/MRTS bleibt offen.

## Verbleibende Risiken

Aktuelle Hostqualifikation, vollständige native/Container-SBOM und Advisory-Analyse von Distributionspatches, geprüfte Runtime-Tupel-Builds, Sicht auf klassische Branch-Protection (HTTP 403) und endgültiger Merge/Pin des korrigierten Frameworks bleiben offen. Bestehende grüne allgemeine CI schließt diese Lücken nicht.

## Nicht ausgeführte Prüfungen mit Begründung

Lokale Sonar-Secrets-Prüfung aufgrund ausdrücklicher Benutzeranweisung nicht ausgeführt. Keine lokale Sonar-Reparatur und keine verpflichtende Ersatzprüfung. Sonar-Analyseimport, vollständige H2/H3-Abnahme und frischer Hostlauf des endgültigen Merge-Paars wurden nicht ausgeführt; dieses Paar existiert noch nicht. Administrative Vorlagen wurden wegen nötiger gesonderter Freigabe nicht angewendet.

## Finaler Diff- und Review-Status

Taskänderungen sind von bestehenden Checkouts/Worktrees isoliert. Framework- und Parent-Lieferung bleiben getrennte Draft-PRs; der minimale reine MRTS-Test-DraftPR#5 wurde unabhängig freigegeben und mit bf756a403ead39863cc15a81b5608e2b6062435d geliefert. Kein Merge, Force-Push, direkter Master-/Main-Push oder Schutzregelwechsel ist freigegeben oder ausgeführt. Gesamtergebnis bleibt partial bis zur Auflösung der erfassten Pflichtlücken.
