# Change Record: Traefik-Runtime-Binär-Provenance und Root-Containment

**Sprache:** [English](CR-20260723-sonar-traefik-runtime-root-confinement.md) | Deutsch

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | CR-20260723-sonar-traefik-runtime-root-confinement |
| Datum (UTC) | 2026-07-23 |
| Basis-Revision | a308d7b414f0859490fe7253e0683a4bde80b563 |
| Tracking | `AZ9MwiwM-bUaKQ_zSGAq` und `AZ9cRyuTHhV2CayPTP1Q` (`python:S5443`); Pending-Canonical-Finding-Import `FND-SONAR-0012`. |
| Grenze | Nur Parent: Traefik-Helper, Parent-Test, gepaarte Traefik-Dokumentation und dieses Change-Record-Paar. Framework, MRTS, Gitlinks, Abhängigkeiten, Scanner-Konfiguration, Quality Gates, Suppressions, False-Positive-State und Host-Protokollverhalten bleiben unverändert. |

## Motivation und Problemstellung

Der direkte Traefik-forwardAuth-Runtime-Smoke leitete `BUILD_ROOT` und `CONNECTOR_COMPONENT_CACHE` aus vorhersehbaren gemeinsamen `/var/tmp`-Defaults ab. Danach leitete er Connector- und Traefik-Binärpfade aus diesen Wurzeln ab und übergab sie nach einer Prüfung nur auf absoluten Pfad, Nicht-Systempfad, Existenz und Ausführbarkeit an `subprocess`. Ein anderer lokaler Benutzer konnte den gemeinsamen temporären Baum vor einer direkten Ausführung vorbereiten und damit vom Angreifer ausgewählte ausführbare Dateien zu den Prozess-Sinks bringen.

Das Problem ist eine lokale Cross-User-Executable-Integrity-Grenze. Diese Remediation ändert keinen Remote-Request-zu-Process-Pfad, kein Framework-Verhalten, kein MRTS-Verhalten und keinen Production-Capability-Claim.

## Akzeptanzkriterien

- Fehlende, gruppen-/weltbeschreibbare oder symlinkte Runtime-Wurzeln werden vor der Prozessausführung zurückgewiesen.
- Eine symlinkte Binärdatei, eine Binärdatei außerhalb ihrer vorgesehenen Wurzel oder ein gruppen-/weltbeschreibbares Verzeichnis zwischen Wurzel und Binärdatei wird zurückgewiesen.
- Eine legitime reguläre ausführbare Datei, die dem aktuellen Benutzer gehört, nicht gruppen-/weltbeschreibbar und enthalten ist, bleibt akzeptiert.
- Die zwei ausgewählten Keys werden auf einer frischen Exact-Head-SonarQube-Cloud-Analyse ohne Suppression, False-Positive-Disposition, Exclusion, Regeländerung oder Quality-Gate-Änderung geprüft.
- Fokussierte Tests, Syntax-/Import-Validierung, Direct-Caller- und Alternate-Bypass-Review, ein Security-Diff-Review und Hosted-Exact-Head-Checks werden vor einer Delivery wahrheitsgemäß festgehalten.

## Implementierungsentscheidung und Begründung

Die Python-Grenze unmittelbar vor den Connector- und Traefik-`subprocess`-Sinks ist der schmalste vollständige Enforcement-Point. Der Helper verlangt jetzt explizite `BUILD_ROOT`- und `CONNECTOR_COMPONENT_CACHE`-Werte. Jede ausgewählte Wurzel muss ein vorhandenes absolutes Verzeichnis außerhalb des Checkouts sein, dem aufrufenden Benutzer gehören, symlinkfrei und nicht gruppen-/weltbeschreibbar sein sowie gegen Cross-User-Ancestor-Replacement geschützt sein.

Jede ausgewählte Binärdatei muss eine reguläre, dem aktuellen Benutzer gehörende, nicht gruppen-/weltbeschreibbare ausführbare Datei sein, die unter ihrer korrespondierenden validierten Wurzel enthalten ist. Jeder Verzeichniseintrag zwischen dieser Wurzel und der Binärdatei muss ebenfalls gegen Cross-User-Replacement geschützt sein. Das entfernt nur den unsicheren impliziten gemeinsamen `/tmp`- und `/var/tmp`-Fallback, bewahrt vertrauenswürdige explizite Lifecycle-Wurzeln, das `BLOCKED`- / Exit-77-Fehlerverhalten und `--help` ohne Runtime-Eingaben.

## Geänderte Dateien

- connectors/traefik/scripts/runtime_smoke.py
- tests/test_traefik_runtime_smoke_security.py
- connectors/traefik/README.md und connectors/traefik/README.de.md
- dieses englische/deutsche Change-Record-Paar

Die etablierten Change-Record-Indizes werden bewusst nicht geändert, weil beide bereits durch den unabhängigen offenen Draft-PR #74 verändert sind; diese Aufgabe beansprucht keine Ownership dieser Pfade.

## Ausgeführte Befehle

- `python -m unittest -v tests.test_traefik_runtime_smoke_security`: bestanden; fünf fokussierte bösartige und legitime Kontrolltests übten die geänderte Helper-Grenze aus, darunter ein beschreibbarer Binär-Vorfahre und eine legitime `0755`-Wurzel unter Kontrolle des aktuellen Benutzers.
- `python -m compileall -q connectors/traefik/scripts/runtime_smoke.py tests/test_traefik_runtime_smoke_security.py`: bestanden mit außerhalb des Checkouts umgeleitetem Bytecode.
- `python connectors/traefik/scripts/runtime_smoke.py --help`: bestanden ohne Runtime-Eingaben.
- Eine direkte Ausführung mit allen nicht gesetzten Runtime-Root-Umgebungsvariablen und einem absoluten entbehrlichen Result-Root lieferte `BLOCKED` / Exit 77 mit `BUILD_ROOT must be set to a trusted runtime root`; es wurde kein Runtime-Artefakt erzeugt.

## Security-Auswirkung

Der geänderte Source-to-Sink-Pfad ist ausgewähltes `BUILD_ROOT` oder `CONNECTOR_COMPONENT_CACHE` zu abgeleitetem Binärpfad zu `subprocess`. Die Invariante wird vor der Akzeptanz jeder Binärdatei erzwungen: Current-User-Provenance, nicht gemeinsam beschreibbare Rechte, Non-Symlink-Identity, Cross-User-Ancestor-Protection und Expected-Root-Containment. Dies blockiert Preseeded-Root-, Symlink-, Outside-Root- und Writable-Descendant-Bypässe, ohne vertrauenswürdiges explizites Lifecycle-Root-Verhalten zu ändern. Kein Security-Control wird geschwächt und es werden weder Suppression, `NOSONAR`, Scanner-Konfiguration noch Quality-Gate-Änderung verwendet.

## Runtime-Evidence

Die deterministische Parent-Regression-Suite übt die echten Helper-Funktionen aus, die die zwei Prozesspfade begrenzen. Sie beweist sicher die Zurückweisung von Wurzeln und Binärdateien, bevor ein subprocess startet, und die Akzeptanz einer enthaltenen regulären Binärdatei. Sie ist kein Host-Runtime-Claim: Es wurde kein echter Traefik-, Connector- oder libmodsecurity-Prozess gestartet.

## Bekannte Einschränkungen

Der lokale kanonische `.codex/findings`-Store ist read-only gemountet. Das vollständige EN/DE/JSON-`FND-SONAR-0012`-Bundle bleibt deshalb als importbereites Artefakt im privaten Task-Run erhalten. Das Change-Record-Indexpaar wird bewusst wegen der Überschneidung mit dem offenen Draft-PR #74 zurückgestellt. Keine dieser Bedingungen ändert Product-Source-Verhalten.

## Verbleibende Risiken

Bis ein neuer exakter PR-Head analysiert ist, akzeptieren direkte Ausführungen des ungepatchten Master weiterhin die vorhersehbaren Wurzeln. Same-UID-Races bleiben außerhalb des Cross-User-Protection-Claims. Frische Hosted-CI- und SonarQube-Cloud-Evidence sind erforderlich, bevor einer der ausgewählten Keys als behoben gilt. Es ist keine Risikoakzeptanz erfasst.

## Nicht ausgeführte Prüfungen mit Begründung

- `tests.test_collect_no_crs_source` ist im isolierten Task-Worktree blocked, weil es den fehlenden Framework-Submodule-Checker `modules/ModSecurity-test-Framework/ci/checks/catalog/no_crs_baseline.py` importiert. Es wurde keine Framework-Änderung, kein globaler Interpreter und keine Abhängigkeits-Substitution versucht.
- Ein echter Traefik-Runtime-Smoke ist nicht ausgeführt, weil dokumentierte lokale Connector-/Traefik-/libmodsecurity-Voraussetzungen nicht festgestellt wurden. Die fokussierten Helper-Tests ersetzen keine Host-Runtime-Evidence.
- Der repository-weite Bilingual-Checker kann durch Framework-Linkziele blockiert sein, wenn das isolierte Worktree das Framework-Submodul nicht enthält; er wird vor der Delivery ausgeführt und wahrheitsgemäß berichtet.
- Hosted-Checks und Exact-Head-SonarQube-Cloud-Analyse können nicht vor einem Commit und Draft PR laufen.

## Finaler Diff- und Review-Status

Die lokale Parent-only-Implementierung und fokussierten Security-Controls sind auf Branch `codex/sonar-traefik-runtime-root-20260723-master-a308d7b` auf der aktuell beobachteten `master`-Revision. Es werden kein Commit, Push, Pull Request, Review-Freigabe, Merge, Default-Branch-Update oder Hosted-Ergebnis behauptet. Final-Diff, Security-Diff-Review, Exact-Head-Checks, SonarQube-Cloud-Ergebnis und Draft-PR-Status müssen abgeglichen werden, bevor eine Delivery als verifiziert berichtet wird.
