# Change Record CR-20260809: Fünf-Connector-No-CRS-Capability-Audit

**Sprache:** [English](CR-20260809-five-connector-no-crs-capability-audit.md) | Deutsch

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | `CR-20260809-five-connector-no-crs-capability-audit` |
| Datum (UTC) | `2026-08-09` |
| Basis-Revision | `ef88a616498e0a2893cd3da54003dd7cdea57015` |
| Umfang | Nur Parent; der Framework-Gitlink bleibt `a7a8dcdd62da8d0e4d7ea36549f7c54c5d614e68` und MRTS wurde nicht geändert. Die Basis wurde lokal als `d9f73ca0558ca499d92ae2736d1be642b9005ee7` gemergt. |
| Lieferstatus | Entwurfsrecord. Die lokalen Source- und Test-Commits gehen diesem Dokumentationsupdate voraus; kein Push, gehostetes Workflow-Ergebnis, Review-Ergebnis oder Merge ist hier dokumentiert. |

## Motivation und Problemstellung

PR #243 benötigt eine Least-Privilege-zeitgesteuerte/manuelle No-CRS-Baseline,
deren Scope ohne impliziten weitergehenden Connector-, Protokoll-, CRS-, MRTS-
oder Produktions-Claim auditierbar ist.

## Akzeptanzkriterien

- Der sichtbare Aufrufer wählt nur das geschlossene Profil `no-crs` und
  delegiert an einen wiederverwendbaren Workflow mit der Berechtigung
  `contents: read`.
- Das Profil enthält genau Apache, HAProxy, Envoy, Traefik und lighttpd;
  unbekannte Profile und Zeilen außerhalb dieser Zuordnung schlagen geschlossen
  fehl.
- Jede Aggregate-Eingabe ist an Connector, Profil, Run-ID, Parent- und
  Framework-Commit sowie Cleanup-Status gebunden; das Aggregate verlangt genau
  die fünf erwarteten Eingaben.
- PR-eigene privilegierte NGINX-Handoff-, Owner-Override- und Projektions-
  Änderungen werden entfernt, ohne den geschützten NGINX-Broker des aktuellen
  Masters zu verändern.
- Englische/deutsche Dokumentation und dieser Change Record bleiben äquivalent.

## Implementierungsentscheidung und Begründung

Der Aufrufer verdrahtet `no-crs`; der wiederverwendbare Workflow erhält seine
Matrix von einem Parent-eigenen geschlossenen Profilauflöser. Der Runner nutzt
unprivilegierte private externe Roots und zeichnet einen Profile-Receipt über
den bestehenden Framework-Result-Artefaktmechanismus auf. Ein Parent-eigener
Fünf-Ergebnis-Verifier wird verwendet, weil der geprüfte Framework-Summarizer
eine generische Sechs-Connector-Steuerung ist und die Aufgabe keine
Framework- oder MRTS-Source-/Gitlink-Änderungen autorisiert.

Der Scope bewahrt die generischen Sechs-Connector-Make-Targets und das
geschützte NGINX-Broker-/Caller-Verhalten des aktuellen Masters. Keines davon
ist Evidence dafür, dass NGINX Teil dieses Fünf-Connector-Profils ist.

### Capability-Audit

Diese Tabelle ist ein Source-/Contract-Audit der fünf ausgewählten
Connector-Zeilen, keine gehostete Evidence. `implemented` für No-CRS bedeutet,
dass das Profil nur in Source und Contracts implementiert ist; gehostete
Evidence bleibt ausstehend. Die anderen Werte werden absichtlich nicht aus
generischen Source-Targets oder Capability-Metadaten hochgestuft.

| Connector | No-CRS | With-CRS | No-MRTS | With-MRTS | Full lifecycle |
| --- | --- | --- | --- | --- | --- |
| Apache | `implemented` (source/contract only, hosted evidence pending) | `not_implemented` | `unknown_pending_audit` | `unknown_pending_audit` | `partially_implemented` (generic existing source targets, not activated/claimed by this profile) |
| HAProxy | `implemented` (source/contract only, hosted evidence pending) | `not_implemented` | `unknown_pending_audit` | `unknown_pending_audit` | `partially_implemented` (generic existing source targets, not activated/claimed by this profile) |
| Envoy | `implemented` (source/contract only, hosted evidence pending) | `not_implemented` | `unknown_pending_audit` | `unknown_pending_audit` | `partially_implemented` (generic existing source targets, not activated/claimed by this profile) |
| Traefik | `implemented` (source/contract only, hosted evidence pending) | `not_implemented` | `unknown_pending_audit` | `unknown_pending_audit` | `partially_implemented` (generic existing source targets, not activated/claimed by this profile) |
| lighttpd | `implemented` (source/contract only, hosted evidence pending) | `not_implemented` | `unknown_pending_audit` | `unknown_pending_audit` | `partially_implemented` (generic existing source targets, not activated/claimed by this profile) |

## Geänderte Dateien

Die laufende Implementierung ändert Caller und wiederverwendbaren Workflow,
Profilauflöser/-aggregator, Lifecycle- und Collector-Verkabelung, fokussierte
Vertragstests sowie die folgenden Reader-Dokumentationspaare:

- `docs/build/README.md` und `docs/build/README.de.md`
- `docs/testing-and-evidence.md` und `docs/testing-and-evidence.de.md`
- `ci/README.md` und `ci/README.de.md`
- dieses Change-Record-Paar

Das finale Datei-Inventar muss vor der Lieferung mit dem finalen Diff
abgeglichen werden.

## Ausgeführte Befehle

### Tests und tatsächliche Ergebnisse

| Prüfung | Tatsächliches Ergebnis |
| --- | --- |
| Fokussierte Suite | Bestanden: 225 Tests |
| `make check-ci-security-contract` | Bestanden |
| `make check-runtime-path-policy` | Bestanden |
| `make check-bilingual-docs` | Bestanden |
| `make check-doc-links` | Bestanden |
| `make check-no-crs-doc-consistency` | Bestanden |
| actionlint | Bestanden |
| zizmor | Bestanden |
| Shell-Syntax und Python-AST | Bestanden |
| `git diff --check` | Bestanden |
| Python-Version-Contract | Der neue Caller-/Callee-Contract bestand seine 24 fokussierten Tests; das repositoryweite Target bleibt durch die identischen unabhängigen Inventarfehler auf `origin/master` blockiert |

Dies sind während der Implementierung beobachtete lokale Ergebnisse.
Gehostete Workflow-, Pull-Request-, Review- und SonarQube-Ergebnisse bleiben
ausstehend; dieser Record behauptet keinen Commit oder Push.

## Security-Auswirkung

Diese Änderung betrifft CI-Berechtigungen, nicht vertrauenswürdige Workflow-
Eingaben, externe Pfade, Artefaktprovenienz und Prozess-Cleanup. Das Profil ist
geschlossen, nutzt nur die Contents-Leseberechtigung, enthält keinen
privilegierten Handoff und weist unbekannte Profil-/Connector-Werte zurück,
bevor Profilevidence akzeptiert wird. Vor der Lieferung bleibt ein finaler
fokussierter Sicherheitsreview erforderlich.

## Runtime-Evidence

Es wird kein gehosteter Runtime-Lauf dokumentiert. Statische Workflow-/Profil-
Verträge und lokale Fixtures belegen kein gehostetes Connector-Runtime-Ergebnis.

## Nicht ausgeführte Prüfungen mit Begründung

Gehostete GitHub-Actions-, Review-Thread-, Required-Check- und SonarQube-
Ergebnisse liegen in diesem Entwurf nicht vor. Sie dürfen nicht aus lokalen
Änderungen hergeleitet werden.

## Bekannte Einschränkungen

Das Profil ist absichtlich No-CRS- und HTTP/1.1-begrenzt. Es belegt weder CRS,
MRTS, HTTP/2, HTTP/3, Full-Matrix-Abdeckung, Produktionsreife noch nicht
beobachtetes Response-Verhalten.

## Verbleibende Risiken

Zukünftige Profile erfordern eine neue geschlossene Zuordnung, Capability- und
Receipt-Validierung, Aggregations-Erwartungen, Tests und vollständige
englische/deutsche Dokumentation. Alleinige Wiederverwendung dieses Profils
kann diese nicht unterstützten Claims nicht promoten.

## Finaler Diff- und Review-Status

In Arbeit. Der finale Abgleich muss die genaue Branch-/Commit-/PR-Head-
Beziehung, tatsächliche lokale und gehostete Check-Ergebnisse, Review-Status
und Lieferdisposition enthalten.
