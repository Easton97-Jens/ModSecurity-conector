# FND-PARENT-0013 — Traefik-Pfad-UDS-Cleanup behält ein finales Same-UID-Unlink-Rennen

## Identity / Identität

| Field / Feld | Value / Wert |
| --- | --- |
| ID | `FND-PARENT-0013` |
| Title / Titel | `Traefik-Pfad-UDS-Cleanup behält ein finales Same-UID-Unlink-Rennen` |
| Category / Kategorie | `security_candidate` |
| Repository / Repository | `parent` |
| Ownership / Ownership | `parent` |
| Priority / Priorität | `P1` |
| Severity / Severity | `medium` |
| Confidence / Confidence | `probable` |
| Status | `blocked` |
| Feasibility status / Machbarkeitsstatus | `blocked_missing_evidence` |
| Release blocker / Release-Blocker | `true` |
| Security relevance / Security-Relevanz | `true` |

## Summary / Zusammenfassung

Der native UDS-Service validiert die Socket-Identität des Pfads vor dem Cleanup
erneut, aber POSIX/Linux hat keine atomare Operation „unlink nur bei dieser
Inode“. Ein bösartiger Prozess mit derselben Service-UID und Änderungsrecht im
Verzeichnis kann den finalen Pfad nach `lstat()` und vor `unlink()` ersetzen.

## Observed behavior / Beobachtetes Verhalten

Die verstärkte Doppelbeobachtung und die `SO_PEERCRED`-Selbstprüfung schließen
die Ersetzungsfenster vor der Ownership-Erfassung. Das finale Cleanup prüft
dennoch Gerät/Inode/Besitzer mit `lstat()` und führt ein separates
pfadbasiertes `unlink()` aus.

## Expected behavior / Erwartetes Verhalten

Eine strikte Foreign-Object-Sicherheitsaussage erfordert entweder keine
automatische Pfadlöschung oder eine verifizierte Trust Boundary, die
Same-UID-Verzeichnisänderungen verhindert. Sie darf keine nicht verfügbare
atomare bedingte Unlink-Semantik behaupten.

## Impact / Auswirkung

Das konfigurierte `0700`-Kind schützt gegenüber anderen UIDs und gewöhnliche
Ersetzung scheitert geschlossen. Es ist keine Isolation gegenüber einem
bösartigen Prozess mit derselben UID; daher ist die verlangte strikte
No-Foreign-Socket-Cleanup-Garantie nicht vollständig bewiesen.

## Affected files and symbols / Betroffene Dateien und Symbole

### Files / Dateien

- `connectors/traefik/src/traefik_engine_service.c`
- `connectors/traefik/scripts/runtime_native_smoke.py`
- `connectors/traefik/build/test-engine-service-runtime.sh`
- `tests/test_traefik_native_local_plugin.py`
- `connectors/traefik/README.md`
- `connectors/traefik/README.de.md`
- `docs/reference/variables.md`
- `docs/reference/variables.de.md`

### Symbols / Symbole

- `traefik_engine_remove_owned_socket`
- `TRAEFIK_ENGINE_SOCKET_PARENT`

## Preconditions / Voraussetzungen

- Ein bösartiger Prozess teilt die effektive Service-UID.
- Er kann das private UDS-Kind-Verzeichnis durchsuchen und ändern.
- Er ersetzt den Pfad nach dem finalen `lstat()` und vor `unlink()`.

## Reproduction / Reproduktion

- `traefik_engine_remove_owned_socket()` prüfen: `lstat()` validiert einen
  Pfadeintrag und `unlink()` konsumiert den Pfad in einer späteren Operation.
- Kein dokumentierter POSIX/Linux-Unlink-API akzeptiert ein Expected-Inode-,
  Descriptor- oder File-Handle-Prädikat.

## Evidence / Evidence

- Run ID: `20260717T114213Z-feasibility-runtime-remediation-838d9adc`
  - Artifact: `logs/058-traefik-uds-final-unlink-static-review.log`; type:
    `source_to_sink_security_review_log`; SHA-256:
    `207b674e7d6842521d6a25b0e0dd4432ba939e5fe6426538636ba12e14e336aa`
  - Command: fokussierte `rg`-Source-to-Sink-Prüfung; working directory:
    `/root/git/ModSecurity-conector`; exit code: `0`; observed:
    `2026-07-17T13:57:53Z`; retention: `retained_task_log`
- Run ID: `20260717T114213Z-feasibility-runtime-remediation-838d9adc`
  - Artifact: `logs/056-traefik-engine-service-double-observation-race-regression.log`;
    type: `native_uds_c17_regression_log`; SHA-256:
    `fd8d6bafee0adf474880625b73c26e719a114e60d44036fb141fc940658b36da`
  - Command: fokussierter nativer C17-Engine-Service-Build- und Lifecycle-Test;
    working directory: `/root/git/ModSecurity-conector`; exit code: `0`;
    observed: `2026-07-17T13:55:00Z`; retention: `retained_task_log`

## Root-cause analysis / Grundursachenanalyse

Pfad-AF_UNIX-Cleanup verwendet eine Check-then-Unlink-Schnittstelle. Dem
OS-API fehlt ein Expected-Object-Prädikat für unlink, und die aktuelle
Architektur hat ein privates Same-UID-Verzeichnis statt einer getrennt
vertrauten Cleanup-Authority.

## Proposed remediation / Vorgeschlagene Remediation

Eine neue Grenze auswählen und nachweisen: Pfad-Sockets nie automatisch
unlinken und `cleanup_incomplete` ausgeben; eine getrennt besessene
vertrauenswürdige Cleanup-Authority verwenden; oder kompatiblen
Abstract-AF_UNIX-Support Ende-zu-Ende etablieren. Bestehende Pre-Bind-
Kollision-, Identitäts- oder Cleanup-Refusal-Kontrollen nicht abschwächen.

## Acceptance criteria / Akzeptanzkriterien

- Der finale Cleanup-Pfad behauptet nie atomare Unlink-if-Inode-Semantik.
- Entweder ist automatische Pfadlöschung fail-closed deaktiviert oder eine
  unabhängig verifizierte Trust Boundary verhindert Same-UID-Pfadersetzung.
- Bestehende Short-Path-, Kollision-, Symlink-, Ersetzung-, Allow-, Blocking-,
  Start-, Shutdown- und Residue-Controls bleiben soweit machbar abgedeckt.

## Validation plan / Validierungsplan

- Die gewählte Grenze mit einem realen bösartigen Same-UID-Ersatztest validieren.
- Nativen C17-Engine-Selbsttest und Protocol-Lifecycle-Controls ausführen.
- Fokussierte Runner-Contracts und bei Verfügbarkeit den echten Host-Lifecycle ausführen.

## Regression tests / Regressionstests

- `connectors/traefik/build/test-engine-service-runtime.sh`
- `tests/test_traefik_native_local_plugin.py`
- Ein zukünftiger realer Same-UID-Final-Unlink-Grenztest nach Architekturauswahl.

## Legitimate control tests / Legitime Kontrolltests

- Normaler fokussierter Native-Engine-Start, Protocol-, Allow- und Blocking-
  Controls bestehen.
- Ein Post-Start-Ersatz-Sentinel bleibt erhalten und der Service meldet
  `socket_cleanup`, statt es zu löschen.

## Dependencies / Abhängigkeiten

- Eine benutzerautorisierte Cleanup-Trust-Boundary-Entscheidung oder kompatible
  Abstract-AF_UNIX-Design-Evidence.

## Blockers / Blocker

- Keine aktuell repository-unterstützte atomare bedingte Pfad-Unlink-Operation
  oder getrennt besessene Cleanup-Authority.

## Related findings / Verwandte Findings

- `FND-FRAMEWORK-0008`
- `FND-PARENT-0014`
- `FND-PARENT-0015`

## Residual risk / Restrisiko

Das Private-Child-Design ist Kollisionsminderung über UIDs hinweg, aber ein
Same-UID-Mutator kann das finale `lstat()`-zu-`unlink()`-Intervall rennen. Der
aktuelle Benutzer hat keine Risikoakzeptanz erteilt.

## History / Historie

- `2026-07-17T13:57:53Z`: `current_task_security_boundary_identified` — die
  Post-Bind- und Post-Probe-Capture-Fenster wurden gehärtet und getestet, aber
  die Source-to-Sink-Prüfung bestätigte die getrennte finale Same-UID-
  Pfadgrenze. Es gibt keine Architekturentscheidung zur Trust Boundary und keine
  Risikoakzeptanz.
- `2026-07-17T14:36:22Z`: `related_same_uid_boundaries_separated` — das
  unabhängige finale Review hält dieses finale Cleanup-Rennen getrennt von der
  Manifest-Leaf-Entfernung (`FND-PARENT-0014`) und der Traefik-Endpoint-
  Umleitung nach Bereitschaft (`FND-PARENT-0015`).
