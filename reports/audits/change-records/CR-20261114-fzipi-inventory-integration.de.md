# Change Record: CR-20261114-fzipi-inventory-integration

**Sprache:** [English](CR-20261114-fzipi-inventory-integration.md) | Deutsch

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | CR-20261114-fzipi-inventory-integration |
| Datum (UTC) | 2026-11-14 |
| Basis-Revision | `80334858a1a1e1ad1ff65e647716584a18cf3e9c` |

## Motivation und Problemstellung

Parent `80334858a1a1e1ad1ff65e647716584a18cf3e9c` wählte Framework `3ff8b75c9f4d2cb3614a4dcb7afd2e5360e074d8`; dessen Inventar lehnte geprüfte Testinhalte vor Ausführung ab, weil sieben Schema-5-Hash-Bindungen noch ältere Bytes beschrieben. Die notwendige zweite Pin-Integration wählt den gemergten Framework-Master `2cc331d8bc4c86592afd7219ddeaba1e60dc0ced` aus [Framework PR 172](https://github.com/Easton97-Jens/ModSecurity-test-Framework/pull/172).

## Akzeptanzkriterien

Die verifizierte Framework-Inventarreparatur integrieren, ohne Produktverhalten, Test-Source-Inhalte, Inventarmitgliedschaft oder Validierungsstärke zu ändern. Alle anderen Komponenten-/Tool-/Runtime-Versionen und MRTS erhalten. Parent-Prüfungen und erforderliche CI für den neuen Pin müssen vor autorisierter Parent-Master-Integration bestehen; Evidenz früherer Heads wird nicht übertragen.

## Implementierungsentscheidung und Begründung

Der bestehende native Schema-5-Updater aktualisierte exakt sieben Hash-Felder: zwei Envoy-Tests und jeweils einen für Traefik, Apache-Lifecycle, HAProxy-Binding, Runtime-Event-Sink und NGINX-Body-Buffer-Fixture. Alle 529 gebundenen Framework-Source-Dateien und alle übrigen Inventardaten bleiben gemäß Framework-Vergleich byteidentisch/semantisch unverändert. Den tatsächlichen Squash-Master statt seines abweichenden geprüften PR-Heads `f2a44adbcaa9fee093093b21186e7e305b78a02c` auswählen.

## Geänderte Dateien

Der Koordinator besitzt Parent-Komponenten-Lock, 22 Workflow-Projektionen und Framework-Gitlink-Update vom vorherigen Pin auf den ausgewählten Master. Dieses neue EN/DE-Change-Record-Paar dokumentiert die gemeinsame Pin-Aktualisierung. Produkt-Source, Framework-Testimplementierung und MRTS-Inhalte bleiben unverändert.

## Ausgeführte Befehle

Das native Parent-Scaffold wurde über RTK mit explizitem Parent-/Framework-Kontext und den Argumenten `create --name fzipi-inventory-integration --base-revision 80334858a1a1e1ad1ff65e647716584a18cf3e9c --date 2026-11-14` erfolgreich ausgeführt. Der beobachtete Framework-Einstieg war `rtk bypass python3 -B -` und startete Child-Prozesse mit explizitem Kontext: nativer Updater-Check Exit 1 vorher / 0 nachher, vollständiger Inventar-Verifier Exit 2 vorher / 0 nachher, Updater-Apply Exit 0, sechs Maintenance-Regressionen PASS und Framework-Dokumentation PASS. Exakte Child-argv und Kontext stehen im [Framework-Record](https://github.com/Easton97-Jens/ModSecurity-test-Framework/blob/2cc331d8bc4c86592afd7219ddeaba1e60dc0ced/reports/audits/change-records/20261114-01-fzipi-inventory-bindings.de.md); sie werden nicht als direkte RTK-Child-Aufrufe umetikettiert. Die Parent-Orchestrierung über `rtk bypass python3 -` startete die konfigurierten Framework-Python-Kindbefehle ebenfalls über RTK. Native Kandidatenprüfung vor/nach Synchronisierung, Synchronizer `--sync`/`--check` und `--verify-primary --base 80334858a1a1e1ad1ff65e647716584a18cf3e9c` bestanden. Der kanonische Inventarcheck sowie `modsecurity_connector_ci.lib.active_test_inventory --check` bestanden mit explizitem Parent-/Framework-Kontext und Profil `h1`. Ein anfänglicher Exit 2 wegen fehlenden externen Ausgabeverzeichnisses war ein Setupfehler; nach dessen Anlage bestand die vollständige Zulassung mit 100 aktiven Fällen bei Grenze 100. Die drei ausgewählten Runtime-Event-Sink-, Host-Action- und HAProxy-Regressionsmodule bestanden mit 26 Methoden in 6.678 Sekunden. Native EN/DE-/Repositorypfad-/Link-Prüfungen bestanden ebenfalls.

## Security-Auswirkung

Die Reparatur stellt die Provenienz geprüfter Source wieder her; sie schwächt weder Hash-, Pfad-, Symlink-, Schema-, Auswahl- noch Fallbudget-Kontrollen. Die frühere exakte Operator-Freigabe `f94` wird nicht auf den neuen Gitlink übertragen. Ein neuer exakter Operatorplan/eine Zulassung kann erforderlich sein; dieser Record installiert, erteilt oder umgeht nichts davon.

## Runtime-Evidence

Framework PR 172 bestand vor Squash-Merge alle sieben erforderlichen Checks und Sonar mit null offenen/unaufgelösten Issues und null Hotspots am exakten Head `f2a44adbcaa9fee093093b21186e7e305b78a02c`. Der ausgewählte Framework-Master ist `2cc331d8bc4c86592afd7219ddeaba1e60dc0ced`. Für diese reine Hash-Reparatur wird keine neue Host-Runtime ausgeführt. Parent-Hauptanalyse und alle 12 nativen Sonar-Ziele bei `80334858a1a1e1ad1ff65e647716584a18cf3e9c` bleiben datierte historische Evidenz bestandener Gates, null unaufgelöster Issues und null Hotspots; sie qualifizieren keinen künftigen Parent-Pin-Commit.

## Bekannte Einschränkungen

Inventarzulassung belegt die Bindungsreparatur, nicht die Ausführung jedes Katalogfalls. Die genannten lokalen Parent-Prüfungen für den neuen Pin sind bestanden; CI des neuen Heads benötigt späteren normalen Commit/Push. Kein zukünftiges Ergebnis wird als beobachtete Evidenz dargestellt.

## Verbleibende Risiken

Neue Source-Edits würden eine weitere geprüfte Bindungsaktualisierung benötigen. Parent-Merge bleibt an grüne erforderliche Tests, finale Prüfungen gestagter Bytes und jede anwendbare exakte Operator-Zulassung gebunden. Bestandene Framework-Prüfungen allein belegen keine Parent-Auslieferungsbereitschaft.

## Nicht ausgeführte Prüfungen mit Begründung

Weder Parent-CI für den neuen Pin noch Parent-Commit oder Parent-Master-Merge werden behauptet. Finale Prüfung der gestagten Bytes, die erforderliche exakte Operator-Zulassung sowie aktuelle CI-Evidenz folgen als getrennte Auslieferungsschritte. MRTS bleibt read-only bei `ee2174431c4edf97e66afe32558ce8454deb2397`; weder MRTS-Mutation noch vollständige Materialized-Pin-Prüfung wird behauptet.

## Finaler Diff- und Review-Status

Native Scaffold-Identität, UTC-Datum und Parent-Basis bleiben erhalten. Die abgegrenzten Schema-/EN-DE-/Link-/Whitespace- und Secrets-Prüfungen bestanden. Die aufgeführten lokalen Resultate sind beobachtet; der finale Index muss vor normalem Commit/Push nativ geprüft und exakt zugelassen werden. Parent-Merge bleibt an die anschließenden aktuellen CI-Gates gebunden.
