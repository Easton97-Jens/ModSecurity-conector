# Change Record: CR-20261103-runtime-readiness-prerequisites

**Sprache:** [English](CR-20261103-runtime-readiness-prerequisites.md) | Deutsch

Scoped readiness prerequisites.

## Identität

| Field | Value |
| --- | --- |
| Change-ID | CR-20261103-runtime-readiness-prerequisites |
| Datum (UTC) | 2026-11-03 |
| Basis-Revision | `11fab78a5447f75cb254ddf963eca770fa04ba04` |

## Motivation und Problemstellung

Der aktuelle delegierte NGINX-Caller mit einem Job wird vom unveränderlichen Brokervertrag mit fünf Inlinejobs abgewiesen. Der erfolgreiche gewöhnliche Hosted-NGINX-Smoke qualifiziert diesen geschützten Pfad nicht. Parent-Python stand außerdem noch auf3.15.1; der geprüfte stabile Patch ist3.15.2.

## Akzeptanzkriterien

Den tatsächlichen Inlinecaller aus dem exakten ausgewählten Framework-Gitblob erzeugen, alle Master-/Non-Fork-/Dispatch-Gates und geschützten Identitäten erhalten und diese typisierte Projektion in die gewöhnliche Framework-Revisionssynchronisierung einbinden. Den Python-Patch über den nativen atomaren Updater anwenden. Beide übergeordneten Revisionsauswahlen bis zur gesonderten Mergefreigabe erhalten.

## Implementierungsentscheidung und Begründung

Der kanonische Framework-Caller erfüllt den unveränderlichen Brokerparser bereits. Seine exakten geprüften Bytes werden projiziert; nur Aufruftrigger und Herkunftskommentare ändern sich. framework-inline-caller erweitert den bestehenden transaktionalen Parent-Synchronisierer: begrenzte Gitdaten mit festem Pfad, geprüfter Quellhash, Prüfung der vorherigen Ausgabe und genau ein historischer Migrationseingang. Kandidaten-Python wird nie importiert. Eine neue Brokerveröffentlichung ist nicht nötig. Der native Python-Updater änderte .python-version und zentralen Lock gemeinsam; die offiziellen Python3.15.2-Releasenotes belegen einen Sicherheitspatch. Versionsalter wird nicht als Schwachstellenbefund gewertet.

## Geänderte Dateien

Die erzeugte .github/workflows/run-protected-nginx-root-broker.yml, ci/tools/sync-framework-component-versions.py, .python-version, ci/tooling/project-versions.lock.json, gepaarte docs/build/README, docs/security/ci-security-tooling und docs/reference/version-pins sowie dieses Recordpaar. Der gepaarte rules-review-Bericht und seine Vorher-/Nachher-JSON aktualisieren den unangewendeten Merge-Regel-Vorschlag anhand aktueller Checks; ihr Umfang wird hier erfasst. Framework-Runner, Fixtures, Capture-Erzeugung, Coverage-Bindung und Teil-SBOM-Export werden im getrennten Framework-Draft geliefert; MRTS-Inheritance-Korrekturen stehen in MRTS-PR #6.

## Ausgeführte Befehle

RTK-gekapselte native scripts/update-python-version.py --check --json und --update --expected-version3.15.2 --json wählten den stabilen Patch. Die exakten privaten Parent-/Framework-Interpreter sind reguläres CPython3.15.2. Framework-Tests gegen die tatsächliche unveränderliche Brokerquelle bestanden9 neue Projektions-/Negativ-/Atomizitätschecks und6 ausgewählte vorhandene Fixture-/Pinchecks. Der Parent-Synchronisierer --check mit dem exakten bb6c758-common.sh-Blob und explizitem bestehendem Framework-Objektrepository lieferte changed=[]. Der Framework-Callergenerator --check bestand. Dokumentations-, Interpretervertrags- und finale Whitespaceprüfungen werden mit der finalen PR-Validierung erfasst; unausgeführte Ergebnisse werden hier nicht behauptet.

## Security-Auswirkung

Deny-Default-Rechte, exakte geschützte Master-/Non-Fork-/Dispatch-Gates, Concurrency, unveränderlicher Broker8ae707d72f1a8acb25d239e55e28a73cbc7522b1 und geschütztes Framework99a7985c1be92a2297b1b59208f64df6768f2cbf bleiben erhalten. Feste Gitquellbytes sind ausschließlich Daten. Kein Broker, Publisher, Root-Lifecycle oder administratives Regelanwenden wird ausgelöst. Zum Interpreterpatch siehe den offiziellen [Python3.15.2-Sicherheitsrelease](https://www.python.org/downloads/release/python-3152/).

## Runtime-Evidence

Dieser Parent-Diff ändert Orchestrierung und Werkzeuge. Tatsächliche gezielte NGINX-Protokollnachweise werden getrennt mit dem Framework-Kandidatenrunner und zugelassenen Baseline-Produktartefakten erzeugt; sie qualifizieren diesen geschützten Master-Broker-Lifecycle nicht. Parsererfolg belegt ausschließlich Callerkompatibilität.

## Bekannte Einschränkungen

Parent basiert weiter auf11fab78a5447f75cb254ddf963eca770fa04ba04 und pinnt Frameworkbb6c7580208a05c17d6d6674571731b6a71028cb/MRTS75394f9a687ca2f09fd7623b23ac527bba10d7d9. Der Caller-Herkunftskommentar nennt wahrheitsgemäß diesen vorhandenen exakten Framework-Quellblob. Neue Framework-/MRTS-Änderungen sind noch nicht gemergt oder durch diese Gitlinks ausgewählt. Erst nach gesonderter Freigabe die tatsächlichen Mergecommits pinnen, dann regenerieren und das endgültige Paar prüfen.

## Verbleibende Risiken

Hosted-Checks des aktuellen Heads und endgültige Paarprüfung bleiben getrennte Liefergates. Eine geschützte Brokerlaufzeit benötigt einen gesondert autorisierten Dispatch vom geschützten Master. Keine umfassende Profil-/Protokollabnahme oder vollständige Schwachstellenprüfung wird behauptet.

## Nicht ausgeführte Prüfungen mit Begründung

Keine vollständige Standardsuite, komplette Laufzeitmatrix, privilegierter Broker, Publisher, administratives Anwenden oder Merge. Lokales Sonar ist durch die ausdrückliche aktuelle Benutzeranweisung ausgesetzt; bestehende Hosted-Sonar-/CodeQL-Prüfungen bleiben unverändert. Kein verpflichtender Ersatzscanner wurde eingeführt.

## Finaler Diff- und Review-Status

Gezielter Review der Erzeugung und Transaktionsgrenzen abgeschlossen. Die getrennte Draftlieferung erhält Quellen und Nachweise. Der finale PR nennt terminale Prüfungen und exakte Commitidentitäten; diese Vorbereitung autorisiert keinen Merge oder Masterupdate.
