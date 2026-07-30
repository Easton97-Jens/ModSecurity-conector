# Change Record: Parent-Lighttpd-Runtime-Output-Containment

**Sprache:** [English](CR-20260729-sonar-lighttpd-runtime-output-containment.md) | Deutsch

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | CR-20260729-sonar-lighttpd-runtime-output-containment |
| Datum (UTC) | 2026-07-29 |
| Basis-Revision | `5a345e3ff90cf5405caea5ff7ae4536b52f826c9` |
| Tracking | Sechs aktuelle SonarQube-Cloud-Befunde `pythonsecurity:S8707`: Fixture-Ready/Result, First-Byte-Metadaten und Lifecycle-Projection/Summary/Results-Outputs. |
| Grenze | Parent-Lighttpd-Harness-Source und Tests sowie gepaarte Change-Record-Indizes. Keine Framework-, MRTS-, Gitlink-, Workflow-, Sonar-Konfigurations-, Suppression- oder `master`-Änderung. |

## Motivation und Problemstellung

Die drei Helper akzeptierten Kommandozeilen-Output-Pfade und schrieben sie nach bloßer Parent-Erstellung. Der Full-Lifecycle-Shell-Runner akzeptierte ein absolutes Smoke-Verzeichnis, stellte jedoch vor Create-, Remove- und Weitergabe-Operationen keinen privaten symlink-freien Write-Root her. Ein Aufrufer konnte so einen unbeabsichtigten Dateisystemort wählen oder einen Pfad mit einem symbolischen Link umleiten.

## Akzeptanzkriterien

- Jeder generierte Fixture-, First-Byte-, Projection-, Summary- und Lifecycle-Output ist ein absoluter Nicht-Symlink-Pfad strikt unterhalb eines verifizierten privaten Runtime-Output-Roots.
- Der Root wird mit der bestehenden Runtime-Path-Policy vor Shell-Cleanup, Erstellung, Fixture-Start oder Übergabe an Downstream-Helper geprüft.
- Generierte Dateien nutzen private `O_NOFOLLOW|O_EXCL`-Temp-Erstellung und atomaren Ersatz; JSON/JSONL-Schemata bleiben unverändert.
- Legitime verschachtelte temporäre Outputs funktionieren; Escape- und Symlink-Output-Pfade werden vor einem Artifact-Write abgewiesen.
- Exact-Head-Hosted-Checks und SonarQube Cloud müssen vor jeder Merge-Betrachtung null New Issues und null New-Code-Duplikation beweisen.

## Implementierungsentscheidung und Begründung

`safe_runtime_output.py` ist ein lokaler Lighttpd-Harness-Adapter über der bestehenden Parent-Runtime-Path-Policy. Er prüft einen schmalen privaten Root, fordert jeden Output und Parent darunter und verwendet vor `os.replace` eine nicht verfolgende exklusive Temp-Datei. Jeder Writer erhält `--runtime-output-root`; der Shell-Runner prüft Smoke-Root und First-Byte-Evidence-Pfad vor dem ersten Write und übergibt anschließend denselben Root an alle betroffenen Helper. Der Adapter verändert nicht den gemeinsamen `ci/lib`-Vertrag, sondern wendet dessen etablierte Kontrollen auf Lighttpd-spezifische Outputs an.

## Geänderte Dateien

- `connectors/lighttpd/harness/safe_runtime_output.py` — verifizierter Root, Containment und atomarer No-Follow-Writer.
- Die drei betroffenen Writer/Fixture-Helper und ihr Shell-Aufrufer.
- Fokussierte Event-Validation- und Host-Contract-Tests.
- Dieses englisch/deutsche Change-Record-Paar und seine gepaarten Indizes.

## Ausgeführte Befehle

| Ausgeführte Kontrolle | Beobachtetes Ergebnis |
| --- | --- |
| Python-Bytecode-Kompilierung der vier geänderten Harness-Module | bestanden. |
| `sh -n connectors/lighttpd/harness/run_patched_full_lifecycle.sh` | bestanden. |
| Fokussierte Lighttpd-Event-Validation- und Host-Contract-Tests | bestanden: 23 Tests, einschließlich normaler verschachtelter Outputs, Escape-Output-Abweisung, Symlink-Escape-Abweisung und beider Fixture-Control-Escape-Fälle. |
| `make check-lighttpd-common-adoption` | bestanden. |
| Lighttpd-Host-Integration- und Build-Wiring-Checks | bestanden. |
| `git diff --check` | bestanden. |

## Security-Auswirkung

Die attacker-kontrollierte Quelle ist der CLI-/Environment-abgeleitete Output-Ort. Frühere Sinks waren `mkdir` plus direkte Text-/Stream-Writes in drei Helpern sowie Shell-Cleanup/Create-Operationen unter dem konfigurierten Smoke-Root. Die neue Invariante prüft Root und jeden Output vor diesen Sinks. Negative Tests zeigen, dass Pfade außerhalb des Roots und Symlink-Descendants vor einem Artifact abgewiesen werden; positive Tests zeigen, dass gültige temporäre verschachtelte Outputs begrenzte Metadaten erhalten. Keine Request-Body-, Rule-, Event-, Autorisierungs-, Runtime-Claim- oder Quality-Gate-Kontrolle wird gelockert.

## Runtime-Evidence

Die fokussierten Tests führen die echten Writer-CLIs und dieselben File-System-Helper aus, die der gepatchte Lifecycle-Runner nutzt. Sie benötigen keinen gebauten Lighttpd-Host. Der Shell-Contract beweist, dass der Runner den verifizierten Root an jeden betroffenen Helper übergibt.

## Bekannte Einschränkungen

- Eine vollständige gepatchte Lighttpd-/libmodsecurity-Host-Runtime und Connector-Matrix liefen nicht, weil der version-festgeschriebene Host-Build und die Fixtures in diesem temporären Task-Worktree fehlen.
- Vor der Delivery benötigt der synchronisierte exakte Kandidat einen vollständigen Codex-Security-Diff-Scan; dieses Change Record ersetzt dessen versiegelte Evidence nicht.
- Hosted-Checks und frische Exact-Head-SonarQube-Cloud-Analyse stehen aus.

## Verbleibende Risiken

- Neue Lighttpd-Harness-Writer müssen diesen Adapter benutzen und einen verifizierten Root erhalten; ein Umgehen benötigt eine neue fokussierte Path-Security-Prüfung.

## Nicht ausgeführte Prüfungen mit Begründung

Keine Live-gepatchte-Lighttpd-Runtime und keine vollständige Connector-Matrix liefen, weil der erforderliche Host-Build und die Fixtures in diesem temporären Worktree fehlen. Die CLI-Level-malicious/legitimate-Kontrollen sind für diese File-System-Sinks die stärkste verfügbare direkte Evidence; der separate vollständige Security-Diff-Scan des synchronisierten Kandidaten bleibt vor der Delivery erforderlich.

## Finaler Diff- und Review-Status

Der Kandidat ist auf Parent-Lighttpd-Harness-Security und bilinguale Traceability begrenzt. Er deckt alle sechs ausgewählten S8707-Locations mit einer gemeinsamen Verified-Root-Grenze ab. Der synchronisierte exakte Head benötigt frische lokale, vollständige Security-Diff- und Hosted-Verifikation vor jeder Delivery- oder Merge-Behauptung.
