# Change Record: Parent-Traefik-Runtime- und Lifecycle-Remediation

**Sprache:** [English](CR-20260730-sonar-traefik-runtime-lifecycle.md) | Deutsch

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | `CR-20260730-sonar-traefik-runtime-lifecycle` |
| Datum (UTC) | 2026-07-30 |
| Basis-Revision | `caddd86d1eede95de53aa1bc971dd26d875df21c` |
| Tracking | `FND-SONAR-0027`; das aktuelle Master-Traefik-Inventar enthält 36 offene Items. |
| Grenze | Nur Parent `connectors/traefik/` und direkte Parent-Tests. |

## Motivation und Problemstellung

Der ForwardAuth-Runner löscht und erzeugt Ergebnis-Pfade jetzt nur noch als
Nicht-Root-Nachfolger des verifizierten `BUILD_ROOT`. Der Native-Runner
validiert einen besitzergesteuerten, nicht ersetzbaren Output-Vorfahren.
Native Literal-/Parser-, Go-Stream-/UDS- und C17-Engine-Kontrollfluss wurden
ohne Änderung des Wire- oder Lifecycle-Vertrags zerlegt. Framework, MRTS,
Gitlinks, Workflows, Sonar-Regeln, Exclusions, Suppressions und Quality Gates
bleiben unverändert.

## Implementierungsentscheidung und Begründung

Die Reparatur erzwingt bestehende Private-Root-Trust-Boundaries vor
zustandsändernden Operationen und extrahiert unabhängige Lifecycle-Aufgaben in
kleine Helper. Dies bewahrt Output und Protokoll ohne Suppressions.

## Akzeptanzkriterien

Unsichere Output-Roots scheitern vor Zustandsänderungen, legitime private Roots
bleiben gültig und der exakte PR-Head muss null New Issues und Duplikatzeilen
haben.

## Geänderte Dateien

`runtime_smoke.py`, `runtime_native_smoke.py`, native Middleware-Go-Quellen und
Tests, `traefik_engine_service.c`, direkte Python-Tests sowie dieses gepaarte
Record/Index änderten sich; keine andere Repository-Grenze änderte sich.

## Ausgeführte Befehle

| Befehl | Ergebnis |
| --- | --- |
| Fokussierte Python-Runtime-Root-Controls | bestanden: 7 Tests. |
| Fokussierte Go-Middleware- und UDS-Wire-Format-Controls im task-eigenen Go-1.26.5-Cache | bestanden. |
| `git diff --check` | bestanden; erneute Ausführung vor Delivery erforderlich. |
| Vollständige native Python-/Go-UDS-Suites | blockiert: Sandbox-AF_UNIX-Setup liefert `Operation not permitted`. |
| C17-Engine-Build | blockiert (`77`): libmodsecurity-Header/-Library fehlen lokal. |

## Security-Auswirkung

Die Output-Root-Änderungen begrenzen Pfade vor rekursivem Löschen, Plugin-Kopie,
Evidence-Erzeugung und Builds; private legitime Roots bleiben zulässig. Es
werden keine Host-Runtime, CI, Review, Sonar-Reanalyse, PR-Delivery oder Merge
behauptet. Exact-PR-Head-Actions und SonarQube Cloud müssen vor jeder
Integrationsentscheidung null New Issues und null New-Code-Duplikatzeilen
zeigen.

## Runtime-Evidence

Fokussierte Controls liefern nur Source-Level-Evidence; kein Host-Runtime-
Ergebnis wird behauptet, weil die nötigen lokalen Voraussetzungen fehlen.

## Bekannte Einschränkungen

AF_UNIX und libmodsecurity sind in dieser Sandbox nicht verfügbar.

## Verbleibende Risiken

Das ursprüngliche Sonarqube-Inventar bleibt bis zur frischen Exact-Head-Analyse
offen.

## Nicht ausgeführte Prüfungen mit Begründung

Der vollständige Host-Lifecycle benötigt AF_UNIX und libmodsecurity; beides
ist in dieser Sandbox nicht verfügbar. Hosted-Verifikation steht bis zum
Draft-PR aus.

## Finaler Diff- und Review-Status

Draft-PR [#203](https://github.com/Easton97-Jens/ModSecurity-conector/pull/203)
wurde aus `agent/traefik-sonar-remediation-20260730` bei Commit
`e5fa1aa8f69fe9d088b661eba80b296bc845870a` eröffnet. Hosted-Review,
Exact-Head-Checks und SonarQube-Cloud-Reanalyse stehen aus; kein Merge und
keine `master`-Änderung werden behauptet.
