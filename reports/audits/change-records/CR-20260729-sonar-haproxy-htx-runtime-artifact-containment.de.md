# Change Record: Parent-HAProxy-HTX-Runtime-Artefaktbegrenzung

**Sprache:** [English](CR-20260729-sonar-haproxy-htx-runtime-artifact-containment.md) | Deutsch

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | CR-20260729-sonar-haproxy-htx-runtime-artifact-containment |
| Datum (UTC) | 2026-07-29 |
| Basis-Revision | Original change base `9f23ae2c5fe908cef38f203be03f93fda75a8dd7`; synchronized candidate base `200712b4dcede1caccc753a572e1e754a5de3e8b` |
| Tracking | Aktuelle HAProxy-HTX-Harness-Kandidaten aus SonarQube Cloud für Pfade, Localhost-Clients und Komplexität. |
| Grenze | Parent-`ci/lib/`, HAProxy- und Envoy-Harness-Fassaden, fokussierte Parent-Tests und gepaarte Indizes. Keine Framework-, MRTS-, Gitlink-, Workflow-, Sonar-Konfigurations-, Suppression- oder `master`-Änderung. |

## Motivation und Problemstellung

Der lokale HTX-Smoke-Helper akzeptierte Kommandozeilenpfade nach der bloßen Prüfung auf Absolutheit.

Seine Output- und Evidence-Lesezugriffe konnten daher einen anderen Dateisystemort benennen.

Seine Client-Helper akzeptierten zudem Klartext-HTTP, obwohl die Harness-Topologie ausschließlich lokal ist und einen temporären TLS-Endpunkt authentisieren kann.

## Akzeptanzkriterien

- Jeder CLI-Artefakt-Lese- und Schreibzugriff ist absolut, symlink-frei und vor dem Dateisystemzugriff strikt unterhalb eines privaten Runtime-Roots.
- Output-Schreibzugriffe verwenden No-Follow-Deskriptoren und hängen sicher an oder ersetzen atomar; ein Aufrufer kann ein Artefakt nicht über einen Symlink umleiten.
- Client-Verbindungen akzeptieren nur credential-freie `https://127.0.0.1`-Endpunkte mit Ports in `1..65535` und prüfen eine reguläre Zertifikatsdatei unter dem privaten Runtime-Root.
- Bestehende HTX-Konfiguration, Evidence-Schemas, die No-Body-Payload-Regel und statische Lifecycle-Kontrollen bleiben unverändert.
- Eine spätere Exact-Head-Hosted-Analyse muss null neue Issues und null New-Code-Duplikatzeilen zeigen.

## Implementierungsentscheidung und Begründung

Die gemeinsame Parent-Schicht `runtime_path_utils.py` prüft einen privaten Root, öffnet Parent-Verzeichnisse ohne Link-Follow und liest oder schreibt nur reguläre Dateien über Deskriptoren. HAProxy und Envoy behalten kleine Connector-lokale Fassaden einschließlich ihrer bestehenden JSON-Serialisierung und Evidence-Formate, statt das Deskriptorprotokoll zu kopieren.

Der gemeinsame atomare Writer erzeugt `0600`-temporäre Dateien über den geöffneten Parent-Deskriptor, prüft das Ziel unmittelbar vor `replace` erneut als regulär und entfernt nur einen temporären Namen, den er selbst erfolgreich erzeugt hat. Eine Kollision mit einem vorhandenen temporären Namen wird wiederholt, ohne diese vorhandene Datei zu löschen.

Der Helper fordert jetzt für jeden Artefaktbefehl `--runtime-root`; der Shell-Runner prüft diesen Root vor seinem ersten eigenen Schreibzugriff.

Der Runner erstellt für jeden Lauf ein kurzlebiges Zertifikat für `127.0.0.1` und ein Private-Key-Bundle ausschließlich unter diesem Root. HAProxy bindet sein TLS-Frontend an das Bundle, während der Client die separate reguläre Zertifikatsdatei über einen expliziten Python-TLS-Client-Kontext mit Zertifikatsprüfung und TLS 1.2 oder neuer vertraut.

Command-Map und ausgelagertes Release-Warten erhalten das Verhalten und entfernen die zwei aktuellen Komplexitätszeilen.

## Geänderte Dateien

- `ci/lib/runtime_path_utils.py` — gemeinsame deskriptorbegrenzte Primitive für private Root-Artefakte der Parent-Harnesses.
- `connectors/haproxy/harness/runtime_artifacts.py` — HAProxy-kompatible Fassade über den gemeinsamen Artefakt-Primitiven.
- `connectors/envoy/harness/envoy_smoke_helper.py` — Envoy-kompatible Fassade über den gemeinsamen Primitiven bei Erhalt der JSON-/Event-Serialisierung.
- `connectors/haproxy/harness/haproxy_htx_smoke_helper.py` — root-gebundene Pfade, reine TLS-Loopback-Client-Endpunkte mit Zertifikatsprüfung und weniger komplexes Command-Dispatch.
- `connectors/haproxy/harness/run_haproxy_htx_runtime.sh` — prüft den Runtime-Root vor Schreibzugriffen, erstellt ein privates TLS-Zertifikat/-Bundle je Lauf und übergibt ihn an jeden Artefaktbefehl.
- `connectors/haproxy/harness/test_haproxy_htx_smoke_helper.py`, `tests/test_haproxy_htx_transaction_id.py` und `tests/test_runtime_artifact_utils.py` — aktualisierter Aufrufvertrag sowie negative Tests für außerhalb des Roots, Symlinks, No-Follow, nichtreguläre Ziele, atomare Rechecks, Kollisions-Cleanup und Nicht-Loopback; der Metadaten-Event-Test bindet seinen temporären privaten Root jetzt vor dessen Verwendung.
- Dieses englisch/deutsche Change-Record-Paar und seine Indizes.

## Ausgeführte Befehle

| Ausgeführte Kontrolle | Beobachtetes Ergebnis |
| --- | --- |
| `/root/git/ModSecurity-conector/.venv/bin/python -B -m unittest -v tests.test_haproxy_htx_transaction_id` | bestanden: 3 Transaction-ID-, Outside-Root-, Symlink-, Loopback-TLS- und Runner-Root-Kontrollen. |
| `/root/git/ModSecurity-conector/.venv/bin/python -B -m unittest -v tests.test_runtime_artifact_utils tests.test_haproxy_htx_transaction_id tests.test_envoy_transport_hardening_contract tests.test_runtime_path_security` | bestanden: 42 Kontrollen für gemeinsame Helper, HAProxy, Envoy, Loopback-TLS, private Roots, Deskriptoren, atomare Rechecks und Kollisions-Cleanup. |
| `/root/git/ModSecurity-conector/.venv/bin/python -m py_compile` für die geänderten Helper und fokussierten Tests | bestanden. |
| Fokussierter direkter Metadaten-Event-Control mit temporärem Root über `haproxy_htx_smoke_helper.py` | bestanden: Metadaten-Event und Host-Evidence werden unter dem gebundenen privaten Root geschrieben. |
| Statischer AST-Bindungs-Control für `test_event_contains_only_metadata` | bestanden: sein geladener `root` ist vor der Verwendung lokal gebunden. |
| Fokussierte temporäre TLS-Server-/Helper-Client-Regression | bestanden: eine verifizierte `https://127.0.0.1`-Zertifikatskette funktioniert; `http` wird vor einer Client-Verbindung abgewiesen. |
| `sh -n` und `shellcheck` für den Runtime-Shell-Runner | bestanden. |
| `make check-haproxy-htx-overlay` | bestanden: bestehender HTX-Lifecycle- und Host-Action-Source-Contract bleibt erfüllt. |
| `make check-haproxy-common-adoption` | bestanden. |
| `make check-envoy-common-adoption` | bestanden. |
| HAProxy-GCC-C17-Lint und C23-Advice-Checks | nach der einzeiligen Python-Testreparatur nicht erneut ausgeführt; kein C-Quellcode wurde geändert. |
| `git diff --check` | bestanden. |
| `/root/git/ModSecurity-conector/.venv/bin/python -B -m unittest -v tests.test_bilingual_docs` | bestanden: 21 Tests des Bilingual-Dokumentationscheckers. |
| `make check-bilingual-docs` | blocked_environment: der Change-Record-Identitätsunterschied ist repariert; verbleibende Fehler sind ausschließlich Links in das bewusst nicht initialisierte Framework-Submodul. |
| `make check-doc-links` | blocked_environment: jedes gemeldete fehlende Ziel liegt im bewusst nicht initialisierten Framework-Submodul. |
| `tests.test_runtime_path_policy` | blocked_environment: sein Shell-Selftest sourced das bewusst nicht initialisierte Framework-`ci/lib/common.sh`; dies ist kein Fehler des gemeinsamen Parent-Artefakt-Helpers. |
| `ruff` und `pyright` | not_run: im ausgewählten Parent-Virtualenv sind weder Executable noch Modul vorhanden; für diese Remediation ist kein Tool-Provisioning autorisiert. |

## Security-Auswirkung

Der Harness verarbeitet CLI-Pfade und öffnet Loopback-Sockets.

Eine Private-Root-Invariante geht jetzt jedem dynamischen Artefakt-Sink oder -Source voraus; finale Dateien werden mit `O_NOFOLLOW` geöffnet und Writer fordern reguläre Dateien. Das gemeinsame Primitiv erhält deskriptorrelatives Anhängen, `0600`-Modi, atomaren Ersatz im selben Verzeichnis und Cleanup begrenzt auf erfolgreich erzeugte temporäre Namen.

Envoy prüft jetzt ebenfalls ein vorhandenes Ziel unmittelbar vor seinem deskriptorrelativen Ersatz erneut als regulär, entsprechend dem stärkeren HAProxy-Vertrag. Die Änderung behauptet keine Crash-Dauerhaftigkeit durch Directory-`fsync`.

Der Smoke-Client erlaubt jetzt nur lokales `https://127.0.0.1` und prüft das Zertifikat pro Lauf, bevor er HTTP-Daten mit HAProxy austauscht. Ein Aufrufer kann weder ein Remote-Ziel noch Klartexttransport auswählen.

Keine Autorisierungs-, Validierungs-, Isolations-, Evidence-Redaktions-, Quality-Gate- oder CI-Kontrolle wird gelockert.

## Runtime-Evidence

Fokussierte Tests beweisen die Pfad- und URL-Verträge. Statische HTX-Kontrollen beweisen, dass der Harness weiterhin die bestehenden Lifecycle-Anforderungen ausdrückt.

Dies ist kein Live-HAProxy-/libmodsecurity-Runtime-Ergebnis und behauptet keine Promotion.

## Bekannte Einschränkungen

- Der Worktree hat kein initialisiertes Framework-Submodul; deshalb kann der vollständige fokussierte HTX-Helper-Test seine Framework-Synchronized-Upstream-Fixture lokal nicht laden. Seine Syntax kompiliert; der unabhängige Parent-Transaction-ID-/Security-Test und der direkte Metadaten-Event-Control sind die stärksten ausführbaren Kontrollen.
- Der HAProxy-zu-Python-Upstream bleibt ein separater privater lokaler Backend-Kanal. Dieser Record beansprucht nur die reparierte Client-zu-HAProxy-TLS-Grenze; eine andere Deployment-Topologie benötigt ein eigenes Upstream-Transport-Review.
- Der vorherige Exact-Head war ausschließlich durch SonarQube-Cloud-New-Code-Duplikation blockiert; die gemeinsame Extraktion und ihre neuen direkten Kontrollen benötigen vor jeder Merge-Aussage eine frische Exact-Head-Hosted-Analyse.

## Verbleibende Risiken

Der Root ist für den aufrufenden Nutzer privat. Ein künftiger Artefaktproduzent verschiedener Nutzer benötigt ein neues Ownership- und Deskriptorprotokoll-Review statt einer Aufweitung des Roots.

## Nicht ausgeführte Prüfungen mit Begründung

Keine Live-HAProxy-/libmodsecurity-HTX-Runtime und kein vollständiger Framework-gestützter Helper-Test liefen, weil der version-pinned HAProxy-Build und die Framework-Fixture in diesem temporären Worktree fehlen.

Die HAProxy-GCC-C17-Lint- und C23-Advice-Checks wurden nach der einzeiligen Python-Testreparatur nicht erneut ausgeführt, weil kein C-Quellcode geändert wurde.

Die genannten Source- und fokussierten Parent-Kontrollen sind die stärkste verfügbare lokale Evidence.

## Finaler Diff- und Review-Status

Der Kandidat ist auf Parent-Common-Pfad- sowie HAProxy-/Envoy-Harness-Code und bilinguale Traceability begrenzt.

Der ursprüngliche Kandidat wurde committed und als PR #182 veröffentlicht. Dieses lokale Follow-up synchronisiert ihn mit `200712b4dcede1caccc753a572e1e754a5de3e8b`, repariert die Metadaten-Event-Testbindung und führt die oben genannten fokussierten lokalen Kontrollen erneut aus.

Der vorherige aktualisierte Kandidat wurde als PR-#182-Head `85995befd19dcac4ab159ec05ee511b891981296` gepusht; seine GitHub-Actions bestanden, aber SonarQube Cloud lehnte 36 doppelte New-Code-Zeilen im neu hinzugefügten HAProxy-Artefaktmodul ab. Dieses lokale Shared-Helper-Follow-up ist noch nicht gepusht, hosted-verifiziert, reviewed oder gemergt. Vor der Integration bleiben ein neuer Exact-Head-GitHub-Actions- und SonarQube-Cloud-Zyklus erforderlich.
