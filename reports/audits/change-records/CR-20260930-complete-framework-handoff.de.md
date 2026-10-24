# Change Record: Framework-Übergabe abschließen

**Sprache:** [English](CR-20260930-complete-framework-handoff.md) | Deutsch

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | CR-20260930-complete-framework-handoff |
| Datum (UTC) | 2026-09-30 |
| Basis-Revision | `bbd74521ee9b1c7544b11c225e399a1c7f8d49da` |

## Motivation und Problemstellung

Der Eigentümer hat die tatsächliche Einspielung der ursprünglichen Framework-Reparatur in PR #393 einschließlich NGINX- und ModSecurity-v3-Wechselabsicherung angefordert. Frühere lokale Läufe wendeten die Änderungen an, stoppten aber bei zwei privilegierten Sandbox-Tests; daher erreichte kein Reparaturcommit den PR.

## Akzeptanzkriterien

Geprüftes Framework-Update und sämtliche zugehörigen Projektionen anwenden; Sicherheitsgrenzen erhalten; betroffene Unit-, Vertrags- und Dokumentationsprüfungen bestehen; normalen Folgecommit auf den bestehenden PR-Branch übertragen. Finale CI und Sonar getrennt bestätigen, bevor der PR als fertig gilt. Kein Merge ist autorisiert.

## Implementierungsentscheidung und Begründung

Die exakten zwölf literalen Änderungen von Framework f9e48b0774b5bdf7aaa8e38ce98eb6c50bf293c8 auf 0290a979ba4bc63a7abed175a53471367b385553 prüfen. Strukturhash 2c3a5774da760981804907a357dc5dafb62f9ba3de1db17a2807ff53fd83c291 nachrechnen und das Parent-NGINX-Tupel auf release-1.31.6, Archiv nginx-1.31.6.tar.gz und SHA-256 974ed5298a5e398e008704ed5db284e655fc270c596493dbccada452448fc9f1 angleichen. Übersehenen Writer-Pin und exakte einzeilige Versionsrückmeldung ergänzen. Leere globale und nur lesende Job-Rechte prüfen, statt globale Rechte wiederherzustellen. Offline-Quell-/Projektionsprüfer und ModSecurity-Cache-/Layout-Regressionen hinzufügen. ModSecurity bleibt v3.0.16 mit 7ea9fefbe0ba409d8733b4d682c8c4c059cd028d.

Die beiden privilegierten Testcallbacks erhalten jetzt den aufgelösten Interpreter statt eines externen virtuellen Alias. Die Kindprozess-Fehlerbehandlung bleibt fehlschlagend und gibt eine begrenzte Diagnose aus. Eine Regression prüft, dass der externe Alias weiter abgelehnt und nur sein bereits erlaubtes aufgelöstes Ziel akzeptiert wird; die produktive Jail-Laufzeitliste bleibt unverändert.

## Geänderte Dateien

Die neunzehn Parent-Textziele des Generators und der Framework-Gitlink; der übersehene NGINX-Writer; dessen Regressionen; Namespace- und Sandbox-Tests; frühe Quick-Prüfung; neuer Versionsprüfer samt Tests; zweisprachige Upgrade-Dokumentation und dieser Record. Die temporäre Hilfe auf dem Validierungsbranch ist vom Reparaturbaum ausgeschlossen.

## Ausgeführte Befehle

Der vorherige Benutzerlauf bestand echten Verifier, Synchronisierer und betroffene Regressionen, scheiterte dann aber bei zwei von 167 CI-Security-Tests. Das sind Basisbeobachtungen, keine Erfolgsbehauptungen. Die direkte Einspielung rekonstruiert und prüft den begrenzten Patch in einem GitHub-Checkout; der verlinkte Validierungsjob und die finalen PR-Checks enthalten die tatsächlichen Endergebnisse. Ein Commit-Objekt wird erst nach erfolgreichen konfigurierten Gates vorbereitet. Der exakt geprüfte Git-Baum wird bei der Veröffentlichung erneut kontrolliert.

## Security-Auswirkung

Keine erweiterte Quell-Allowlist, Freigabe durch Kandidaten-Shellcode, Berechtigungsausweitung, Scanner-Unterdrückung oder Broker-Änderung. Quelltupel und Pfadgrenzen bleiben fail-closed. Die Auswahl des aufgelösten Python korrigiert Testeingaben, ohne externe Hostverzeichnisse einzuhängen. Der Validierungsjob hat nur lesenden Repository-Zugriff; ein getrennter begrenzter Publisher erstellt Git-Objekte und kann weder mergen noch master aktualisieren.

## Runtime-Evidence

Unit- und synthetische Bibliothekslayouttests belegen weder native ABI- noch WAF-Kompatibilität. Der echte NGINX-Exact-Head-Laufzeitjob und benötigte privilegierte Namespace-Ergebnisse müssen getrennt geprüft werden. Keine neue ModSecurity-Version wird ausgewählt oder zertifiziert.

## Bekannte Einschränkungen

Der lokalen ChatGPT-Umgebung fehlen GitHub-DNS und RTK. Gehostete Ausführung liefert projektnative Ergebnisse; lokale Fixture-Ergebnisse ersetzen diese nicht. Ein grüner Vorbereitungscommit genügte nicht und ist erst durch den tatsächlichen Reparaturcommit auf dem PR-Branch abgelöst.

## Verbleibende Risiken

Zukünftige Versionen können öffentliche APIs, SONAME, Ausgabelayout oder WAF-Verhalten ändern. Frühe Abweichungsprüfungen garantieren nicht jedes zukünftige Release. Der unabhängig geschützte NGINX-Broker bleibt eine getrennte Review-Grenze.

## Nicht ausgeführte Prüfungen mit Begründung

Nur wegen dieser Guard-Änderungen wird weder eine neue ModSecurity-Version gebaut noch eine vollständige Multi-Connector-Laufzeitmatrix gestartet. Ausstehende finale CI und Sonar zählen nicht als bestanden. Umgebungsbedingte Skips werden angegeben statt verborgen.

## Finaler Diff- und Review-Status

Nur den begrenzten Reparaturbaum nach Validierung und Prüfung des unveränderten Branches ausliefern. Finalen PR-Head und Checks zurücklesen. Bestehende Sonar-Korrekturen und Dokumentationsabsicherungen erhalten. Kein Force-Push, Master-Push oder Merge.
