# Change Record: Parent-Lighttpd-Runtime-Input-Containment

**Sprache:** [English](CR-20260730-sonar-lighttpd-runtime-input-containment.md) | Deutsch

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | CR-20260730-sonar-lighttpd-runtime-input-containment |
| Datum (UTC) | 2026-07-30 |
| Basis-Revision | `caddd86d1eede95de53aa1bc971dd26d875df21c` |
| Tracking | Ein aktueller SonarQube-Cloud-Befund `pythonsecurity:S8707` in `connectors/lighttpd/harness/write_patched_lifecycle_results.py:208`. |
| Grenze | Parent-Lighttpd-Harness-Source und Tests sowie gepaarte Change-Record-Indizes. Keine Framework-, MRTS-, Gitlink-, Workflow-, SonarQube-Cloud-Konfigurations-, Suppression- oder `master`-Änderung. |

## Motivation und Problemstellung

`--entity-fixture-result` erreichte `Path.read_text()`, ohne festzustellen, dass die Datei zum verifizierten privaten Runtime-Root gehört. Der kanonische Shell-Runner erzeugt das Fixture-Ergebnis zwar unter seinem privaten Smoke-Verzeichnis, aber ein direkter Helper-Aufruf konnte einen unabhängigen lesbaren Pfad wählen. Für die übrigen datenführenden Lifecycle-CLI-Inputs fehlte dieselbe Containment-Invariante.

## Akzeptanzkriterien

- Jeder datenführende Lifecycle-Input ist vor dem Lesen oder Verwenden ein absoluter, vorhandener, regulärer Nicht-Symlink-Runtime-Artefaktpfad strikt unterhalb des verifizierten privaten Roots.
- Das Fixture-JSON wird durch den etablierten descriptor-begrenzten, no-follow Runtime-Artefakt-Leser gelesen.
- Escape-Pfade, Symlink-Escapes, fehlende Dateien und nicht-reguläre Fixture-Pfade schlagen fehl, bevor ein Lifecycle-Output, eine Projection oder eine Summary existiert.
- Der bestehende legitime Lifecycle-Control behält Schema, Selected-Case-Ergebnis, Projection und Summary-Verhalten.
- Exact-Head-Hosted-Checks und SonarQube Cloud müssen vor jeder Merge-Betrachtung weiterhin null New Issues und null New-Code-Duplikation beweisen.

## Implementierungsentscheidung und Begründung

`safe_runtime_output.py` stellt nun einen Lighttpd-lokalen Adapter über den bestehenden Parent-Runtime-Path-Primitiven bereit. `safe_input_path()` delegiert an `runtime_artifact_path(..., must_exist=True)` und erhält damit die Anforderungen an absolute Pfade, unterhalb des Roots, keine Symlinks, sichere Parents und reguläre Dateien. `read_runtime_input_text()` delegiert Fixture-Lesezugriffe an den bestehenden descriptor-begrenzten `read_runtime_artifact_text()`-Control. Der Lifecycle-Writer validiert Events, Phase-4-Barrier, First-Byte-Evidence, Content-Length-Events, Chunked-Events und Fixture-Result vor der Verarbeitung; die bestehende atomare Output-Behandlung bleibt unverändert.

## Security-Auswirkung

Die kontrollierte Quelle ist ein lokaler aufruferkontrollierter CLI-Pfad und kein nachgewiesener Remote-HTTP-Input. Der betroffene Sink war der Fixture-Aufruf `Path.read_text()`. Die reparierte Invariante begrenzt alle Lifecycle-Dateninputs auf den privaten Per-Run-Root und weist Symlink- oder Typ-Substitutionen vor der Verarbeitung ab. Der kanonische Runner bleibt kompatibel, weil er diese Artefakte bereits unter diesem Root ablegt. Keine Request-Body-, Rule-, Event-, Autorisierungs-, Runtime-Claim-, Quality-Gate- oder bestehende Output-Schutzkontrolle wird gelockert.

## Geänderte Dateien

- `connectors/lighttpd/harness/safe_runtime_output.py`
- `connectors/lighttpd/harness/write_patched_lifecycle_results.py`
- `connectors/lighttpd/tests/test_patched_event_validation.py`
- Dieses englisch/deutsche Change-Record-Paar und seine gepaarten Indizes.

## Ausgeführte Befehle

| Ausgeführte Kontrolle | Beobachtetes Ergebnis |
| --- | --- |
| Fokussierte Escape-/Symlink-Input-Regression | bestanden: Alle sechs datenführenden Input-Optionen weisen eine Datei außerhalb des Roots und einen In-Root-Symlink, der nach außen zeigt, ab. |
| `python3 connectors/lighttpd/tests/test_patched_event_validation.py -v` mit deaktiviertem Bytecode und task-eigenem temporären Speicher | bestanden: 8 Tests, einschließlich legitimen Lifecycle-Verhaltens, Escape-/Symlink-Pfaden und fehlenden/nicht-regulären Fixture-Controls. |
| `python3 -m py_compile` für die geänderten Python-Module und den Test | bestanden. |
| `python3 connectors/lighttpd/tests/test_patched_host_contract.py -v` mit deaktiviertem Bytecode und task-eigenem temporären Speicher | bestanden: 17 Tests. |
| `git diff --check` | bestanden. |
| `make check-bilingual-docs` | außerhalb dieses Diffs blockiert: Das neue Change-Record-Paar erfüllt die erforderlichen Abschnittsüberschriften, aber im isolierten Worktree fehlt der Parent-gebundene Framework-Checkout, den 20 bereits bestehende lokale Links benötigen. |

## Runtime-Evidence

Die fokussierte Suite ruft die echte Lifecycle-Writer-CLI und dieselben Runtime-Artefakt-Helper wie der gepatchte Lifecycle-Runner auf. Sie beweist die malicious lokalen CLI-Pfadbedingungen und den gültigen In-Root-Control, ohne einen gebauten Lighttpd-Host oder ein HTTP-Runtime-Ergebnis zu behaupten.

## Nicht ausgeführte Prüfungen mit Begründung

Kein Live-gepatchter-Lighttpd/libmodsecurity-Build, Runtime-Smoke, Full-Lifecycle oder Connector-Matrix lief. Diese Python-only Input-Artefakt-Containment-Änderung verändert weder C-Code noch HTTP-Transport, Host-Konfiguration oder Protocol-Logik; die fokussierte echte CLI-Regression ist die proportionale direkte Prüfung. Diese separaten Host-Voraussetzungen waren für diese File-System-Grenze nicht erforderlich.

## Bekannte Einschränkungen

- Der Befund ist ein Befund mit hoher Sicherheit für eine fehlende lokale CLI-Containment-Kontrolle, aber kein validierter Remote-Lighttpd-Arbitrary-File-Read-Exploit.
- Hosted-CI und die Exact-Head-SonarQube-Cloud-Analyse sind noch nicht verfügbar; sie bleiben erforderliche Delivery-Evidence.
- Der Whole-Tree-Checker für bilinguale Dokumentation kann in diesem isolierten
  Worktree nicht bestehen, weil sein Framework-Gitlink-Checkout absichtlich
  fehlt; die gemeldeten fehlenden Link-Targets bestanden bereits vor diesem Diff.

## Verbleibende Risiken

Zukünftige Lighttpd-Lifecycle-Reader müssen denselben verifizierten privaten Root und descriptor-begrenzten Input-Helper verwenden. Ein neuer Reader, der diese Grenze umgeht, benötigt ein fokussiertes Path-Security-Review.

## Finaler Diff- und Review-Status

Der Kandidat ist auf Parent-Lighttpd-Runtime-Input-Containment, fokussierte Tests und bilinguale Traceability begrenzt. Die lokale Verifikation bestand. Zum Zeitpunkt der Record-Erstellung werden kein Commit, Push, Pull Request, Hosted-Check, SonarQube-Cloud-Reanalyse oder Merge behauptet.
