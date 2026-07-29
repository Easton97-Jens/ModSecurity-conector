# Change Record: Parent-HAProxy-HTX-Runtime-Artefaktbegrenzung

**Sprache:** [English](CR-20260729-sonar-haproxy-htx-runtime-artifact-containment.md) | Deutsch

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | CR-20260729-sonar-haproxy-htx-runtime-artifact-containment |
| Datum (UTC) | 2026-07-29 |
| Basis-Revision | `9f23ae2c5fe908cef38f203be03f93fda75a8dd7` |
| Tracking | Aktuelle HAProxy-HTX-Harness-Kandidaten aus SonarQube Cloud für Pfade, Localhost-Clients und Komplexität. |
| Grenze | Parent-`connectors/haproxy/`-Harness, fokussierte Parent-Tests und gepaarte Indizes. Keine Framework-, MRTS-, Gitlink-, Workflow-, Sonar-Konfigurations-, Suppression- oder `master`-Änderung. |

## Motivation und Problemstellung

Der lokale HTX-Smoke-Helper akzeptierte Kommandozeilenpfade nach der bloßen Prüfung auf Absolutheit.

Seine Output- und Evidence-Lesezugriffe konnten daher einen anderen Dateisystemort benennen.

Seine Client-Helper akzeptierten zudem beliebige HTTP-Hosts und Ports, obwohl die Harness-Topologie ausschließlich Loopback verwendet.

## Akzeptanzkriterien

- Jeder CLI-Artefakt-Lese- und Schreibzugriff ist absolut, symlink-frei und vor dem Dateisystemzugriff strikt unterhalb eines privaten Runtime-Roots.
- Output-Schreibzugriffe verwenden No-Follow-Deskriptoren und hängen sicher an oder ersetzen atomar; ein Aufrufer kann ein Artefakt nicht über einen Symlink umleiten.
- Client-Verbindungen und Bereitschaftsprobes akzeptieren nur credential-freie `http://127.0.0.1`-Endpunkte mit Ports in `1..65535`.
- Bestehende HTX-Konfiguration, Evidence-Schemas, die No-Body-Payload-Regel und statische Lifecycle-Kontrollen bleiben unverändert.
- Eine spätere Exact-Head-Hosted-Analyse muss null neue Issues und null New-Code-Duplikatzeilen zeigen.

## Implementierungsentscheidung und Begründung

`runtime_artifacts.py` baut auf der bestehenden Parent-Runtime-Pfadpolicy auf, prüft einen privaten Root, öffnet Parent-Verzeichnisse ohne Link-Follow und liest oder schreibt nur reguläre Dateien über Deskriptoren.

Der Helper fordert jetzt für jeden Artefaktbefehl `--runtime-root`; der Shell-Runner prüft diesen Root vor seinem ersten eigenen Schreibzugriff.

Command-Map und ausgelagertes Release-Warten erhalten das Verhalten und entfernen die zwei aktuellen Komplexitätszeilen.

## Geänderte Dateien

- `connectors/haproxy/harness/runtime_artifacts.py` — deskriptorbegrenzte Hilfen für private Root-Artefakte.
- `connectors/haproxy/harness/haproxy_htx_smoke_helper.py` — root-gebundene Pfade, reine Loopback-Client-Endpunkte und weniger komplexes Command-Dispatch.
- `connectors/haproxy/harness/run_haproxy_htx_runtime.sh` — prüft den Runtime-Root vor Schreibzugriffen und übergibt ihn an jeden Artefaktbefehl.
- `connectors/haproxy/harness/test_haproxy_htx_smoke_helper.py` und `tests/test_haproxy_htx_transaction_id.py` — aktualisierter Aufrufvertrag sowie negative Tests für außerhalb des Roots, Symlinks und Nicht-Loopback.
- Dieses englisch/deutsche Change-Record-Paar und seine Indizes.

## Ausgeführte Befehle

| Ausgeführte Kontrolle | Beobachtetes Ergebnis |
| --- | --- |
| `python3 -m unittest tests.test_haproxy_htx_transaction_id` | bestanden: Transaction-ID-Verhalten sowie negative Outside-Root-, Symlink-, Loopback- und Runner-Root-Kontrollen. |
| `python3 -m py_compile` für beide geänderten Helper-Module | bestanden. |
| `sh -n` und `shellcheck` für den Runtime-Shell-Runner | bestanden. |
| `make check-haproxy-htx-overlay` | bestanden: bestehender HTX-Lifecycle- und Host-Action-Source-Contract bleibt erfüllt. |
| `make check-haproxy-common-adoption` | bestanden. |
| HAProxy-GCC-C17-Lint und C23-Advice-Checks | bestanden mit temporärem Output unter `/var/tmp/codex`. |
| `git diff --check` | bestanden. |

## Security-Auswirkung

Der Harness verarbeitet CLI-Pfade und öffnet Loopback-Sockets.

Eine Private-Root-Invariante geht jetzt jedem dynamischen Artefakt-Sink oder -Source voraus; finale Dateien werden mit `O_NOFOLLOW` geöffnet und Writer fordern reguläre Dateien.

Die HTTP-Topologie ist auf lokales `127.0.0.1` begrenzt. Das erhält den absichtlichen Real-Host-Smoke-Transport, ohne dass ein Aufrufer ein Remote-Ziel auswählen kann.

Keine Autorisierungs-, Validierungs-, Isolations-, Evidence-Redaktions-, Quality-Gate- oder CI-Kontrolle wird gelockert.

## Runtime-Evidence

Fokussierte Tests beweisen die Pfad- und URL-Verträge. Statische HTX-Kontrollen beweisen, dass der Harness weiterhin die bestehenden Lifecycle-Anforderungen ausdrückt.

Dies ist kein Live-HAProxy-/libmodsecurity-Runtime-Ergebnis und behauptet keine Promotion.

## Bekannte Einschränkungen

- Der Worktree hat kein initialisiertes Framework-Submodul; deshalb kann der fokussierte HTX-Helper-Test seine Framework-Synchronized-Upstream-Fixture lokal nicht laden. Seine Syntax kompiliert; der unabhängige Parent-Transaction-ID-/Security-Test ist die stärkste ausführbare Kontrolle.
- Der Loopback-Upstream bleibt absichtlich Plain-HTTP für die version-pinned lokale HAProxy-Smoke-Topologie. Der getrennte `python:S5332`-Kandidat braucht eine wirklich konfigurierte TLS-Fixture und wird hier weder unterdrückt noch als behoben dargestellt.
- Hosted-Checks und eine frische Exact-Head-SonarQube-Cloud-Analyse stehen aus.

## Verbleibende Risiken

Der Root ist für den aufrufenden Nutzer privat. Ein künftiger Artefaktproduzent verschiedener Nutzer benötigt ein neues Ownership- und Deskriptorprotokoll-Review statt einer Aufweitung des Roots.

## Nicht ausgeführte Prüfungen mit Begründung

Keine Live-HAProxy-/libmodsecurity-HTX-Runtime und kein vollständiger Framework-gestützter Helper-Test liefen, weil der version-pinned HAProxy-Build und die Framework-Fixture in diesem temporären Worktree fehlen.

Die genannten Source- und fokussierten Parent-Kontrollen sind die stärkste verfügbare lokale Evidence.

## Finaler Diff- und Review-Status

Der Kandidat ist auf Parent-HAProxy-Harness und bilinguale Traceability begrenzt.

Die lokale Validierung ist für die implementierten Pfad-, Loopback-Client- und Komplexitätsreparaturen abgeschlossen.

Zum Zeitpunkt der Record-Erstellung ist er nicht committed, gepusht, veröffentlicht, hosted-verifiziert oder gemergt.
