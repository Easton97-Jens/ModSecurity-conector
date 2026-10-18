# Change Record: CR-20261018-haproxy-bounded-host-batches

**Sprache:** [English](CR-20261018-haproxy-bounded-host-batches.md) | Deutsch

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | CR-20261018-haproxy-bounded-host-batches |
| Datum (UTC) | 2026-10-18 |
| Basis-Revision | `7ad1d7b1c6d88c7430213d408f1f184f2442314c` |

## Motivation und Problemstellung

Unabhängige HAProxy-Fälle tragen wiederholt die Setup-Kosten des privaten Controllers. Ein unveränderter privater Namespace wird für eine begrenzte Folge frischer vorhandener Capture-Driver genutzt; Original-IDs, Prozesslebenszeiten und Messungen bleiben getrennt.

## Akzeptanzkriterien

Pro Queue höchstens sechs Fälle einer Route vorbereiten. Original-JSON, Oracles und Payloadbytes erhalten. Alle Eingaben per Hash binden, explizite Laufzeitpfad-/Port-Relokationsdiffs speichern und veränderliche oder ungeprüfte Eingaben ablehnen. Jeden echten Driver abwarten, seinen Exit unverändert erhalten und vor dem nächsten Fall bei Prozess-/Descriptor-/Socket-Leaks, Timeout, fehlendem/fehlgeschlagenem Cleanup oder Ausgabe-/Laufzeitbudgetbruch stoppen. Ein abgeschlossener Batch und Controller-Exit 0 dürfen niemals Lifecycle-PASS vergeben.

## Implementierungsentscheidung und Begründung

`i12_batch.py` als HAProxy-spezifischen Koordinator ergänzen. Native- und SPOP-Fixture-Kopien relokieren ausschließlich die bekannten Python-Driver von `/task` und `/mnt/fixtures` in Fall-Unterverzeichnisse und nutzen vollständige unterschiedliche Portblöcke. Companion verwendet sein vorhandenes `--root` und dynamische Ports ohne Quelländerung. Jeder Fall startet frische Driver-/Host-/Agent-Prozesse. Prozess-PID/Startzeit, Koordinator-Descriptoren und tatsächliche Kernel-Sockettabellen werden vorher/nachher verglichen; TCP TIME_WAIT bleibt die dokumentierte Ausnahme ohne lebenden Besitzer, und eindeutige Ports vermeiden Wiederverwendungsverzögerungen. Vorhandene Driver-Cleanup-Receipts bleiben von HTTP-/nativer Qualifikation getrennt. HOME wird unverändert geerbt; fallbezogene TMPDIR- und XDG-Verzeichnisse trennen temporäre und Cache-Ausgaben. Tatsächliche TCP-TIME_WAIT-Zeilen bleiben separat in jedem Vorher-/Nachher-Snapshot erhalten. Ein fehlgeschlagener /proc-Identitätszugriff lässt starttime null und wartet trotzdem das tatsächliche Kind ab, bevor gestoppt wird. Der unveränderte Controller verantwortet weiterhin Admission, Capability-Drop, Namespace-Überwachung sowie aggregierte Speicher-/Prozessbudgets.

## Geänderte Dateien

Neu: `connectors/haproxy/harness/i12_batch.py`, `tests/test_haproxy_i12_batch.py` und dieses EN/DE-Change-Record-Paar. Diese Arbeit ändert keine vorhandenen Driver-, Controller-, Produkt-, gemeinsamen Capture-, zentrale Matrix-, Framework- oder MRTS-Dateien.

## Ausgeführte Befehle

`rtk proxy <run>/test-env/bin/python -m pytest -q tests/test_haproxy_i12_batch.py`: 22 Tests bestanden unter CPython 3.14.7, Exit 0. Die Tests umfassen echte harmlose Kindprozess-Exits, einen begrenzten schlafenden Prozess, einen tatsächlichen Loopback-Listener, tatsächliche Descriptor-Änderungen, Timeout/Reaping, Ausgabe-Budgetfehler sowie Queue-/Quellmanipulation. Diese Komponentenprozesse sind keine HAProxy-Hostläufe. Exakte umhüllte argv/cwd/Zeiten/Ausgabehashes: `<run>/commands/haproxy-batch-components-v6-20261018.json`. Drei Vorbereitungen endeten mit Exit 0: `<run>/commands/haproxy-batch-pilot-prepare-{native,spop,companion}-v2-20261018.json`. `<run>` bezeichnet `/var/tmp/codex/ModSecurity-conector/runs/i12-haproxy-415-acceptance-20261015`. Die Pilotquellen für Native, SPOP und Companion sind jeweils `native/original-fixtures-v7`, `spop/source-fixtures-v4` und `companion/source-fixtures-v5`.

## Security-Auswirkung

Keine Änderung des produktiven Security-Verhaltens. Versiegelte Queues binden den exakten Koordinator, Quell-Fixtures, Driver und Relokationsreceipts; ausführbare argv werden aus zugelassener Route und Fall abgeleitet, statt beliebigen Shelltext anzunehmen. Physische Pfade lehnen Traversal, Symlinks und fremde Eigentümer ab. Die Laufzeit verlangt die originale Nonroot-Controller-Admission und passende tatsächliche Namespace-Identitäten. Ein Cleanup-Defekt verhindert weitere Fallausführung. Das finale Artefakt-Binding bleibt eine separate, von Root geprüfte Controller-Eingabe.

## Runtime-Evidence

Drei Pilotkandidaten mit je zwei Fällen liegen unter `<run>/batches/20261018-pilot-v2`. `root-review.json` und die drei `*-relocations.diff`-Dateien enthalten exakte vorgeschlagene argv, Hashes, Änderungen und Grenzen. Root prüfte und versiegelte ausschließlich den SPOP-Kandidaten und dokumentierte `spop-root-approval.json` sowie das exakte `spop-root-spec.json` (SHA-256 `e471578a2db9e3bbfe4f52d9ee6bf1a2038aada7c929f2d0519b6fa60c5b650e`). Der Koordinator-SHA-256 lautet `2e2f10191bd8729dbc5beed1ee345663d7eafd87557159b7b77a3b06fd220ce9`. Native- und Companion-Kandidatenverzeichnisse bleiben unversiegelt.

Root führte den SPOP-Piloten `attempt-1792320861376221286` aus: zwei frische SPOP-Fälle, jeweils Driver-Exit 0, mit Hauptrequest-ACK-Status 200 und 403, zugehörigen Backend-Requestzahlen 1 und 0 sowie gesunden Nachbarn. Der Batch beendete beide Fälle ohne Cleanup-Fehler; Controller-Exit 0, kein Timeout, keine überlebenden Namespace-PIDs und keine äußeren Mount-Leaks. Rohevidence bleibt unter `<run>/isolation/attempt-1792320861376221286` erhalten, einschließlich `controller-result.json`, `data/batch-result.json` und der Client-/Frame-/Backend-/Native-Dateien jedes Falls. Diese zwei SPOP-Fälle sind keine separaten Native- oder Companion-Läufe. Hauptclient-Zeitstempel fehlen in diesem Snapshot und verhindern eine unabhängige Lifecycle-Zuordnung; Messreparatur und frische Ausführung bleiben erforderlich. Kein Lifecycle-PASS wird behauptet. Dieser Worker startete keinen HAProxy-Host oder Agenten.

## Bekannte Einschränkungen

Fälle teilen eine tatsächliche Namespace-Admission, nicht eine HTTP-Transaktion oder Engine-Instanz. Die Qualifikation muss diese Beziehung ausdrücklich erhalten und die getrennten echten Prozessidentitäten und Rohdateien jedes Falls verwenden. Der vorhandene native Einzelcase-Observer benötigt eine unabhängig geprüfte optionale Datenverzeichnis-Anpassung, bevor er verschachtelte Batch-Ausgaben verarbeitet. Ein Kernel-TCP-TIME_WAIT-Eintrag gilt nicht als lebender Listener-/Prozess-Leak.

## Verbleibende Risiken

Native-/Companion-Privathost-Piloten, reparierte SPOP-Clientzeitstempel mit frischer Ausführung, vollständige Artefakt-/SDK- und Loaded-Image-Bindings, alle Original-Oracle-Vergleiche, Lifecycle-Review und finales CI/Sonar bleiben erforderlich. Der oben beschriebene SPOP-Pilot belegt ausschließlich Capture-Ausführung und Cleanup; weder gemessene Beschleunigung durch Batching noch Host-Vollständigkeit wird behauptet. Vollständiger Quellreview bestätigt, dass der vorhandene Candidate bereits `/task/isolation-admission.json` schreibt; v2 erhält dieses Originalreceipt und prüft zusätzlich das unveränderliche `/opt/controller/admission.json`, tatsächliche Capabilities/NoNewPrivs und Trennung von äußeren Namespaces. Frühere Review-Unsicherheit über ein fehlendes Receipt ist kein tatsächlicher Runtime-Defekt. V1 bleibt erhalten und unausgeführt.

## Nicht ausgeführte Prüfungen mit Begründung

Dieser Worker führte keinen privaten HAProxy-Host, CI oder serverseitige Sonar-Analyse aus. Root gab den oben beschriebenen SPOP-Piloten separat frei, versiegelte ihn und führte ihn aus. Native- und Companion-Pilotversiegelung/-ausführung bleiben zurückgestellt. Root verantwortet die Git-Lieferung.

## Finaler Diff- und Review-Status

Das eigene neue Modul, Tests und Change-Record-Paar sind vorbereitet. Komponententests bestanden; Root prüfte die Relokationsdiffs und gab ausschließlich den SPOP-Piloten frei, versiegelte ihn und führte ihn aus. Native- und Companion-Kandidaten bleiben zurückgestellt und unversiegelt. Der Koordinator ist mit dem oben angegebenen SHA-256 eingefroren. Frühere strukturelle Dokumentationsprüfungen belegten keine deutsche Inhaltsvollständigkeit; das erhaltene deutsche Gerüst wurde jetzt durch eine vollständige Begleitfassung ersetzt, und alle 12 Abschnitte wurden manuell mit den englischen Fakten abgeglichen. Kein Merge, Push, neuer PR oder Lifecycle-Abnahmeergebnis wird behauptet.
