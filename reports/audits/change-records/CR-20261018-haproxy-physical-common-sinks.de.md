# Change Record: CR-20261018-haproxy-physical-common-sinks

**Sprache:** [English](CR-20261018-haproxy-physical-common-sinks.md) | Deutsch

Produkt-Follow-up im bestehenden #382; integrierte Hostabnahme in #415.

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | CR-20261018-haproxy-physical-common-sinks |
| Datum (UTC) | 2026-10-18 |
| Basis-Revision | `29b42a469d4273661bcda5e917db62d9de21a06b` |

## Motivation und Problemstellung

Native HTX hatte keinen konfigurierten physischen Common-Entscheidungssink. Stdio-Close-/Schreibfehler und die Herkunft von Companion-OUTCOME-Events brauchten explizite gemeinsame Behandlung. Einer CI-Binding-Fixture fehlte außerdem das neu erforderliche Feld der Request-HTTP-Version.

## Akzeptanzkriterien

Begrenzte physische native Metadaten über sichere private Deskriptoren schreiben; Serialisierung und sämtliche stdio-Stufen prüfen; erste Ursache und exakte beobachtete Phase erhalten; unpassende Companion-Events abweisen; natives Allow sowie einmaliges Close/Free erhalten. Frische Host-Lifecycle-Abnahme bleibt getrennt.

## Implementierungsentscheidung und Begründung

Drei geprüfte Common-FILE-Helfer und optionales HTX events-file mit Mutex und dauerhaftem Erstfehler ergänzen. Den bestehenden privaten No-Follow-Dateiopener für SPOP-Logs wiederverwenden. Companion-Events nach akzeptiertem OUTCOME und vor RELEASE mit Owner-Snapshot und kopierten Queue-Metadaten erzeugen. Gültiges P4-Allow in COMPLETED wird ohne Event akzeptiert; Nicht-Allow mit falschen Disruptive-Flags wird abgewiesen. Unbekanntes Companion late_intervention_mode auslassen, statt den Engine-Standard des Owners zu kopieren.

## Geänderte Dateien

common/include/msconnector/event_jsonl.h, common/src/event_jsonl.c; HAProxy-Filter/Binding/Header/SPOP-Runtime; native Common-Stream-/Physical-Event-/Companion-Event-Tests und bestehende I10-/Sink-Fixtures. Root ergänzt tests/test_haproxy_binding_refactor.py um http_version und die Assertion, dass native URI-Verarbeitung 1.1 erhält. Dokumentation: connectors/haproxy/README.md und README.de.md sowie dieses Change-Record-Paar.

## Ausgeführte Befehle

RTK-verpackte fokussierte CPython3.14.7-Tests, kompilierte Fehler-Cookies, ASan/UBSan, native SDK-P3/P4-Eventauslese, sieben Owner-Mutationen, vier Shared-Helper-Mutationen, eine Omitted-Native-Write-Mutation und HAProxy3.2.25-/Binding-/SPOP-Builds bestanden. Exakte argv, Exits, Rohhashes und erhaltene Failing-before-Versuche sind im externen Lauf i12-haproxy-415-acceptance-20261015/product-spop/physical-sink-review.json indiziert. Die Root-Binding-Refactor-Regression bestand in commands/binding-refactor-current-version-20261018. Spätere integrierte Suite-Ergebnisse werden getrennt erfasst.

Breitere Root-Regression: 276 Tests und 249 Subtests bestanden, 12 übersprungen, vier Fehler. Zwei veraltete extrahierte/native Security-Fixtures wurden korrigiert; ihre 14-Test-Suite bestand. Die zwei weiteren Fehler betreffen den alten upload-artifact-Pin, der bereits in #410 korrigiert ist; die Prüfung nach normaler Integration muss diesen aktuellen Test verwenden, ohne den Workflow-Pin zu ändern. Die Prüfungen der gepaarten README-/Change-Record-Dateien und Dokumentationslinks bestanden.

## Security-Auswirkung

Keine Payload-/Header-/URI-/nativen Logdaten gelangen in Common-Metadaten. Sichere Pfadannahme, Eigentums- und Modusprüfungen bleiben aktiv; kein Symlink- oder stdout-Fallback. Ein fehlerhafter konfigurierter Sink weist späteres Allow ab. Queue-Metadaten haben begrenzte eigene Lebensdauer. Keine Änderung an Abhängigkeiten, Framework-/MRTS-Gitlink, Gates, Warnungen oder Security-Policy.

## Runtime-Evidence

Echtes libModSecurity3.0.14 erzeugt physische P3/P4-Entscheidungsdatensätze; Parallelkontrollen erhalten 32 korrelierte native Datensätze. Stdio-Kontrollen prüfen bestehendes ferror, Serialisierung ohne Schreibvorgang, fputs-/fflush-/fclose-Fehler, verhinderte Wiederholungen nach Sinkfehler und verbrauchtes Eigentum. Dies sind tatsächliche Komponentenausführungen und keine vollständigen HAProxy-Host-Lifecycle-PASS.

## Bekannte Einschränkungen

Flush ist keine dauerhafte Speicherung oder Clientzustellung. Native Filter-Deinitialisierung ist void und kann keinen Prozessexitfehler melden. Companion-Host-phase4-mode bleibt im physischen Event unbekannt, da aktuelles OUTCOME keinen Modus trägt; das optionale Feld fehlt. Eine Sandbox-UID-Mapping-abhängige Opener-Kontrolle wurde explizit übersprungen; der normale Private-File-Smoke bestand.

## Verbleibende Risiken

Frische Direct-/SPOP-/Companion-Builds und isolierte Hosttests müssen die integrierte Revision binden. Anforderungen an physisch beobachtete Hostmodus-Metadaten bleiben bis zur getrennten Umsetzung und Messung offen. Historische Rohbelege und Fehler bleiben unverändert.

## Nicht ausgeführte Prüfungen mit Begründung

Vollständige aktuelle integrierte I12-Hostqualifikation und Final-Head-CI/Sonar folgen Veröffentlichung über #382→#410→#415 und frischen Builds. Historisches #382 Gitleaks ist ein unabhängiger Release-Blocker ohne Ausnahme oder History-Umschreibung.

## Finaler Diff- und Review-Status

Unabhängiger Quellreview fand falsche P1/P3-Zuordnung bei Sinkfehlern; die zuständige Korrektur verwendet die tatsächliche Entscheidungsphase und erhält frühere Ursachen. Finale eingefrorene Quellidentität und fokussierte Regressionsergebnisse bleiben im externen Reviewpaket erhalten. Root-Integrationsreview, Dokumentationsprüfungen und Lieferung sind vor Veröffentlichung dieses Follow-ups erforderlich.
