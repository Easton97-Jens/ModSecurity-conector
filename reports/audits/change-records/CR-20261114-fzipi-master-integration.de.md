# Change Record: CR-20261114-fzipi-master-integration

**Sprache:** [English](CR-20261114-fzipi-master-integration.md) | Deutsch

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | CR-20261114-fzipi-master-integration |
| Datum (UTC) | 2026-11-14 |
| Basis-Revision | `43baefa2d3a6ce66876aca1a2cd0d7b50e2a412a` |

## Motivation und Problemstellung

Parent wählte noch Framework `31531f74cfe26c2a40d4bb5f6eaae4c0920127e1`, dessen Fixtures nicht zum abgeschlossenen Connector-Followup passen. [Framework PR 171](https://github.com/Easton97-Jens/ModSecurity-test-Framework/pull/171) ist nun per Squash gemergt; diese Integration wählt dessen Master-Commit `3ff8b75c9f4d2cb3614a4dcb7afd2e5360e074d8` über die nativen Kandidaten- und Publikationsverträge.

## Akzeptanzkriterien

Den gemergten, geprüften Framework-Tree auswählen; ausschließlich dessen Lock-/Workflow-Projektionen und Parent-Gitlink synchronisieren; andere Komponenten-/Tool-/Runtime-Versionen und MRTS erhalten. Parent-Master-Integration ist nur bei grünen erforderlichen Tests autorisiert. Kandidatenprüfung ersetzt weder Parent-CI für den neuen Pin noch finale Hook-Zulassung oder Merge-Autorität.

## Implementierungsentscheidung und Begründung

Nativen Verifier und Synchronisierer statt manueller Änderungen generierter Referenzen verwenden. Das extrahierte Framework-Common-Skript ist Eingabedaten und wird niemals gesourct. Der ausgewählte Master-Tree ist identisch zum geprüften `f3813dad`; seine abweichende Squash-Commit-Identität wird ausdrücklich dokumentiert. MRTS bleibt `ee2174431c4edf97e66afe32558ce8454deb2397`.

## Geänderte Dateien

Komponenten-Lock plus 22 Workflow-Projektionen, Parent-Framework-Gitlink und dieses EN/DE-Record-Paar. Der Koordinator besitzt die 23 generierten Dateien und das geplante Gitlink-Staging; dieser Record-Autor ändert ausschließlich dieses Paar. Diese Integration ändert weder Produkt-Source-Verhalten noch MRTS-Inhalte oder andere Versionsauswahl.

## Ausgeführte Befehle

Aliase bezeichnen die tatsächlich ausgewählten Orte: `P` ist der Parent-Worktree, `F` der Framework-Task-Worktree mit Git-Objekten, `E` das zulässige externe Run-Verzeichnis, `C=$E/master-integration/framework-common.data` und `PY` der kanonische Framework-Interpreter. `O=31531f74cfe26c2a40d4bb5f6eaae4c0920127e1`, `S=3ff8b75c9f4d2cb3614a4dcb7afd2e5360e074d8`, `B=43baefa2d3a6ce66876aca1a2cd0d7b50e2a412a`. Alle folgenden Befehle verwendeten `rtk bypass env RUNNER_TEMP=$E/master-integration FRAMEWORK_ROOT=$F TEST_ROOT=$F CONNECTOR_ROOT=$P CONNECTOR_REVISION=$B PYTHONDONTWRITEBYTECODE=1 $PY -I`:

| Befehl nach Prefix | Vom Koordinator beobachtetes Ergebnis |
| --- | --- |
| `$P/ci/tools/verify-framework-candidate-contract.py --candidate-sha $S --framework-common $C --candidate-framework-root $F --expected-parent-framework-sha $O` | PASS nach Wiederherstellung des Zugriffs auf die gepinnte Git-Source. |
| `$P/ci/tools/sync-framework-component-versions.py --framework-common $C --framework-object-root $F --framework-sha $S --sync` | PASS; Komponenten-Lock und 22 Workflow-Referenzen synchronisiert. |
| `$P/ci/tools/sync-framework-component-versions.py --framework-common $C --framework-object-root $F --framework-sha $S --check` | PASS; Änderungsliste `[]`. |
| `$P/ci/tools/verify-framework-candidate-contract.py --candidate-sha $S --framework-common $C --candidate-framework-root $F --expected-parent-framework-sha $S` | PASS gegen den synchronisierten Lock. |
| `$P/ci/tools/sync-framework-component-versions.py --framework-common $C --framework-object-root $F --framework-sha $S --verify-primary --base $B` | PASS für Publikationsbytes im Worktree. |

Der erste Kandidatenaufruf scheiterte, weil die alte gepinnte Framework-Git-Source über den Export ohne Git nicht verfügbar war. Dieser Export blieb extern erhalten; ein verknüpfter Framework-Git-Worktree wurde beim alten Pin registriert und danach ohne rekursive MRTS-Initialisierung auf den ausgewählten neuen Pin ausgecheckt. Die folgenden Ergebnisse oben löschen diesen anfänglichen Fehler nicht aus.

## Security-Auswirkung

Der Framework-Pin ist eine Test-Supply-Chain-Grenze. Native Verifikation prüft Git-gestützte Source-Identität und zulässige Projektionen; weder Source-Daten-Skriptausführung noch Validierungsumgehung wird eingeführt. Eine neue exakte Operator-Gitlink-Zulassung kann durch den Hook weiterhin erforderlich sein; sie ist zu diesem Zeitpunkt weder installiert noch freigegeben. Eine Umgehung wird nicht behauptet.

## Runtime-Evidence

Vor dem Framework-Merge bestand der geprüfte `f3813dad` 19 Runner-Methoden, alle neun tatsächlichen nativen NGINX-Szenarien und sieben CI-Workflows, mit null gemeldeten Issues/Hotspots. Der gemergte Framework-Master hat denselben Tree. Zum Record-Snapshot umfassen fünf Framework-Läufe nach Master drei Erfolge und zwei noch offene Läufe. Diese Fakten belegen weder Parent-CI für den neuen Pin noch einen anderen Host/ein anderes Profil.

## Bekannte Einschränkungen

Der neue Framework-Worktree hat keinen initialisierten MRTS-Checkout; das tatsächliche bestehende MRTS-Repository bleibt an seinem dokumentierten Pin unverändert. Keine vollständige Materialized-Pin-Verifikation wird behauptet. Der extern erhaltene Export ohne Git-Metadaten ersetzt nicht die vom nativen Verifier benötigte Git-Source.

## Verbleibende Risiken

Parent-Master-Merge hat nicht stattgefunden. Verbleibende erforderliche CI, finales Review der gestagten Bytes und jede exakte Hook-Zulassung müssen vor autorisierter Integration erfolgreich sein. Bestandene Kandidaten-/Publikationsprüfungen allein können weder Runtime- noch finalen Auslieferungserfolg belegen.

## Nicht ausgeführte Prüfungen mit Begründung

Parent-CI für den neuen Pin benötigt normalen Commit/Push und ist noch nicht gelaufen. Die zwei offenen Framework-Läufe nach Master und finale gestagte Dokumentations-/Indexprüfungen werden nicht als bestanden behauptet. Der Koordinator wird diese Prüfungen vor Commit/Integration ausführen und dokumentieren; kein zukünftiges Ergebnis wird als beobachtete Evidenz dargestellt.

## Finaler Diff- und Review-Status

Dieses Paar füllt das native Scaffold ohne Änderung von Identität/Datum/Basis. Der Koordinator behält die Verantwortung für generiertes Projektionsreview, Gitlink-Staging, finale Prüfungen und Parent-Master-Lifecycle. Dieser Autor führt weder Git-Aktion noch Source-Edit oder MRTS-Schreibzugriff aus; finaler Commit, vollständig grüner Parent-Status oder abgeschlossener Parent-Merge werden nicht behauptet.


Abschließende lokale Pre-Commit-Evidenz: Vollständige Parent-EN/DE-/Pfadreferenz-/Link-Prüfungen und gestagter Whitespace bestanden; der native Synchronisierer `--verify-primary --base 43baefa2d3a6ce66876aca1a2cd0d7b50e2a412a --staged` meldete `FRAMEWORK_PRIMARY_VERIFIED`. Das gewählte gemergte Framework unter `modules/ModSecurity-test-Framework` bestand anschließend `python -m unittest -v modsecurity_connector_tests.test_runtime_event_sink_failures modsecurity_connector_tests.test_runtime_host_action_validation modsecurity_connector_tests.test_haproxy_binding_refactor`: 26 Methoden in 6.679 Sekunden, Exit 0. Diese prüfen unmittelbar die zuvor fehlgeschlagenen Extraktions-/Mock-Schnittstellen. Gehostete Parent-Checks benötigen weiterhin normalen Commit und Push; kein zukünftiger Merge- oder Admission-Erfolg wird behauptet.
