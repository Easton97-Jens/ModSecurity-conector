# Change Record: Behebung der SonarQube-Cloud-Reliability-Bugs

**Sprache:** [English](CR-20260720-sonar-reliability-remediation.md) | Deutsch

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | `CR-20260720-sonar-reliability-remediation` |
| Datum (UTC) | `2026-07-20` |
| Basis-Revision | `5a22cbf5206dbc2b7f53a9f961d72e37d567e188` |
| Tracking | Aktuelle Parent-Master-SonarQube-Cloud-Bug-Records: `python:S5779`, `python:S1751`, drei `c:S2637`-Stellen, `c:S5489`, `c:S836` und `c:S3519`. |
| Grenze | Nur Parent-Provisioning, Envoy-Smoke-Helper, Traefik-Engine-Service, Common-Authorization-Service, Native Oracle und HAProxy-SPOP-Diagnostik; Framework und MRTS bleiben unverändert. |

## Motivation und Problemstellung

Die aktuelle Parent-SonarQube-Cloud-Analyse auf der Basis-Revision meldet neun
offene Bug-Records. Zwei Python-Records verwenden einen fragilen
Assertion-/Fehlerpfad und eine Ein-Iterations-Schleife. Die nativen Records
betreffen optionale Zeigerkopien, deren Nullsicherheit nur durch einen
Size-Helper impliziert ist, ein durch Wrapper verdecktes Lock-Paar, einen
uninitialisierten Socket-Address-Analysepfad, einen nullable JSON-String-
Fallback und Diagnostik, die den Standard-Error-Stream ohne expliziten Guard
übergibt.

## Akzeptanzkriterien

- Erfolgreiche Cache-Veröffentlichung, gültige nicht-gechunkte Envoy-Body-Reads,
  Traefik-Result-Serialisierung, Authorization-Listener-Verhalten, native
  JSON-Escapes und HAProxy-Startdiagnostik bleiben erhalten.
- Null-, Lock- und Socket-Zustand werden ohne Sonar-Suppression,
  Regel-Deaktivierung, Exclusion, Hotspot-Disposition oder Quality-Gate-
  Änderung explizit gemacht.
- Fokussierte Regression-/Contract-Abdeckung wird ergänzt und alle berührten
  C-Translation-Units werden mit C17-Warnungen als Fehler kompiliert.
- Vor der Behauptung, dass die ursprünglichen neun Bug-Keys behoben sind, wird
  eine frische SonarQube-Cloud-Analyse für den exakten PR-Head eingeholt.

## Implementierungsentscheidung und Begründung

Der Cache-Publisher ersetzt drei `assert`-Statements durch einen privaten
`require_staging_path`-Guard, der auch bei optimierter Python-Ausführung
wirksam bleibt. Der Envoy-Helper führt den einen erforderlichen First-Body-Byte-
Receive direkt aus. Traefik kopiert optionale Felder erst nach nicht-null
Zeiger und positiver begrenzter Größe; seine direkten Mutex-Paare machen die
Lock/Unlock-Beziehung an jeder Call-Site sichtbar. Common initialisiert
akzeptierte und lokale
Socket-Address-Objekte. Der Native Oracle gibt für einen null optionalen Wert
einen leeren JSON-String aus, bevor er einen Byte-Cursor bezieht, und die
HAProxy-Diagnostik prüft den Standard-Error-Stream explizit.

Dies sind enge, verhaltenserhaltende Änderungen an den vorhandenen
Enforcement- oder Diagnostik-Grenzen; weder öffentliche API noch
Connector-Protokoll, Framework-Source, MRTS-Source, Scanner-Konfiguration oder
Quality Gate werden verändert.

## Security-Auswirkung

Die betroffenen Pfade verarbeiten native Connector-Ergebnisse,
Socket-Peer-Informationen und Runtime-/Evidence-Diagnostik. Die Änderungen
behandeln fehlende optionale Werte und uninitialisierten Zustand sicher,
während legitime nicht-null und begrenzte Eingaben erhalten bleiben. Sie
akzeptieren keine fehlerhaften Eingaben, senken kein Ressourcenlimit, schwächen
keine Validierung und verbergen kein Scanner-Ergebnis.

## Geänderte Dateien

- `ci/provisioning/components/prepare-runtime-components.py`
- `connectors/envoy/harness/envoy_smoke_helper.py`
- `connectors/traefik/src/traefik_engine_service.c`
- `common/runtime/http_authorization_service.c`
- `ci/tools/native_modsecurity_oracle.c`
- `connectors/haproxy/src/haproxy_spop_diagnostic_runtime.c`
- `tests/test_prepare_runtime_components.py`
- `tests/test_envoy_transport_hardening_contract.py`
- `tests/test_sonar_reliability_contract.py`
- `reports/audits/change-records/README.md` und `README.de.md`
- dieses englische/deutsche Change-Record-Paar

## Ausgeführte Befehle

| Befehl | Ergebnis |
| --- | --- |
| `rtk env PYTHONDONTWRITEBYTECODE=1 PYTHONNOUSERSITE=1 /root/git/ModSecurity-conector/.venv/bin/python -m unittest -v tests.test_sonar_reliability_contract` | bestanden: 5 fokussierte Source-Contract-Tests. |
| `rtk env PYTHONDONTWRITEBYTECODE=1 PYTHONNOUSERSITE=1 /root/git/ModSecurity-conector/.venv/bin/python -m unittest -v tests.test_envoy_transport_hardening_contract` | bestanden: 8 Envoy-Transport-Controls. |
| `rtk env PYTHONDONTWRITEBYTECODE=1 PYTHONNOUSERSITE=1 /root/git/ModSecurity-conector/.venv/bin/python -m unittest -v tests.test_traefik_native_local_plugin` | bestanden: 16 Traefik-Native-Plugin-/UDS-Controls. |
| `rtk env PYTHONDONTWRITEBYTECODE=1 PYTHONNOUSERSITE=1 /root/git/ModSecurity-conector/.venv/bin/python -m unittest -v tests.test_prepare_runtime_components.PrepareRuntimeComponentsTest.test_require_staging_path_rejects_absence_and_preserves_path` | bestanden. |
| `rtk proxy cc -std=c17 -Wall -Wextra -Werror -fsyntax-only ...` für jede berührte C-Translation-Unit | bestanden für Traefik-Engine-Service, Common-Authorization-Service, Native Oracle und HAProxy-SPOP-Diagnostik. |
| `rtk git diff --check` | nach dem Dokumentationspaar bestanden. |

## Runtime-Evidence

In diesem isolierten Worktree wurde keine vollständige native Connector-Runtime
ausgeführt. Die aufbewahrte lokale Evidence besteht aus C17-Syntaxvalidierung
aller vier berührten C-Translation-Units sowie fokussierten Contracts für die
Envoy-Receive-Grenze, Traefik-Mutex-/Serialisierungsgrenzen, den
Provisioning-Guard und die zweisprachige Dokumentation. Frische GitHub- und
SonarQube-Cloud-Evidence für den PR-Head ist weiterhin erforderlich, bevor die
ursprünglichen Bug-Keys als behoben behauptet werden.

## Nicht ausgeführte Prüfungen mit Begründung

- Ein breiterer Lauf von `tests.test_prepare_runtime_components` führte 38
  Tests aus; 35 bestanden und drei HAProxy-Cache-Tests scheiterten vor dem
  geänderten Code, weil dieser isolierte Parent-Worktree kein initialisiertes
  `modules/ModSecurity-test-Framework/ci/provisioning/prepare-haproxy-runtime.sh`
  enthält. Die drei Fehler werden als externer Framework-Worktree-
  Prerequisite-Gap dokumentiert, nicht als bestandenes Ergebnis.
- Vollständige native Connector-Builds und Runtime-Harnesses benötigen eine
  linkbare lokale libmodsecurity-Installation und/oder Host-Source; verfügbar
  war nur die C17-Syntaxvalidierung.
- Der repositoryweite Bilingual-Checker erreichte die Link-Phase ohne
  Change-Record-Heading-Fehler und stoppte dann an unabhängigen fehlenden
  Framework-Link-Targets, weil dieser isolierte Parent-Worktree keinen
  initialisierten Framework-Checkout besitzt. Der CI-Checker für den exakten
  PR-Head bleibt die ausstehende Full-Scope-Evidence.
- Frische GitHub-Actions-, CodeQL-, SonarQube-Cloud-, Review- und PR-Evidence
  bleiben Delivery-Prüfungen und wurden für diese lokalen Änderungen noch nicht
  beobachtet.

## Bekannte Einschränkungen

Die C17-Prüfungen und fokussierten Contracts belegen Source-Level-Sicherheit
und Kompatibilität an den berührten Grenzen, sind aber kein frisches
SonarQube-Cloud-Ergebnis.

## Verbleibende Risiken

Der aktuelle Master enthält außerdem unabhängige unreviewte Security-Hotspots
und einen getrennt getrackten Vulnerability-Backlog; dieser Record behauptet
nicht, sie zu lösen. Die Delivery ist ein offener Draft-PR (#66), dessen
exakter aktueller Head, GitHub-Checks, CodeQL-Ergebnis, Review und
SonarQube-Cloud-Analyse weiterhin erforderlich sind, bevor diese Arbeit
`verified_pr` erreichen kann.

## Finaler Diff- und Review-Status

Der erste lokale Commit ist
`d1ec42d0ebf713b3e898538ea125c8d6e5b8bf6d`; er wird über Draft-PR #66
ausgeliefert. Das Change-Record-Paar benennt die fehlende
Framework-Prerequisite und ausstehende Remote-Checks bewusst explizit. Dieser
Record autorisiert keinen Merge.
