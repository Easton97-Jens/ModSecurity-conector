# FND-FRAMEWORK-0057 — Connector-neutrale Security-Data-Flow-Deskriptoren werden als ausführbare Runtime-Fälle behandelt

## Identität

| Feld | Wert |
| --- | --- |
| ID | FND-FRAMEWORK-0057 |
| Kategorie | ci_failure |
| Repository / Ownership | framework / framework |
| Priorität / Schwere / Konfidenz | P1 / not_applicable / reproduced |
| Status / Machbarkeit | fixed / blocked_external_dependency |
| Release-Blocker / sicherheitsrelevant | true / true |
| Betroffene Revision | `a7ebf5a1d9cad2b0a65a7603476a1434fdb16cf6` |
| Parent-/MRTS-Disposition | Framework-PR #51 ist gemergt und über Parent #126 übernommen; Parent #74 benötigt einen frischen Exact-Head-Producer und ein striktes Gate; MRTS bleibt unverändert |

## Zusammenfassung, beobachtetes Verhalten und Auswirkung

## Framework-Revalidierung und verbleibender Blocker vom 2026-07-26

Der aktuelle Framework-master `47e50e7bc43ba7a3b5bad1a9448111794f664cc0`
besteht die Framework-eigenen Case-Schema-, Matrix-Report- und
Security-Data-Flow-Checker-Controls. Damit ist dies kein verbleibender
Framework-Source-Defekt. Der Record bleibt `blocked` statt `verified`, bis
Parent-PR #74 einen frischen Exact-Head-Producer, striktes Terminal-Gate,
SonarQube-Cloud-, Review- und Protected-Integration-Evidence liefert. Parent
und MRTS wurden in diesem Task nicht geändert.

Der Exact-Head-Runtime-Producer von Parent-PR #74 bei
`c6db0f8ab5b95be67a92ba925a1f4caa3d3d0a1d` bereitete Apache und NGINX nativ
erfolgreich vor und scheiterte anschließend in der Framework-Force-All-
Falldiscovery mit `ValueError: case requires rules` für einen
Framework-eigenen `security-data-flow`-Deskriptor.

Alle 15 Deskriptoren unter `tests/cases/security-data-flow/**` sind
connector-neutrales Former-XFAIL-Connector-Gap-Inventar mit
`capabilities.runtime_verified: false`; keiner enthält eine connector-eigene
ModSecurity-Regel. Der Runner normalisiert zudem die deklarierte Capability
`security_data_flow` zu `security-data-flow`, kannte dieses normalisierte
Token aber nicht. Der Schema-Contract kann damit einen explizit nicht
ausführbaren Deskriptor nicht von einem unvollständigen aktiven Runtime-Fall
unterscheiden.

Der Defekt blockiert frische legitime Runtime-Evidence für Parent #74. Eine
Platzhalterregel oder weit gefasste Ausnahme könnte Connector-Runtime-Verhalten
erfinden und nicht unterstützte Security-Ergebnisse hochstufen. Ein
Produktions-Exploit wird nicht behauptet.

## Reproduktion und Ursache

Die Hosted-Evidence ist GitHub-Actions-Parent-PR-#74-Lauf `30205593649`, Job
`89802976898`. Eine direkte Framework-Force-All-`case_cli.py list-cases`-
Kontrolle reproduzierte das frühere Verhalten; nach der vorbereiteten Reparatur
endet sie ohne Auswahl dieser Deskriptoren erfolgreich.

Der Runner nimmt jedes YAML als materialisierbar an und verlangt daher
`rules`, Request- und Expectation-Daten. Außerdem fehlt dem
Capability-Allowlist das normalisierte Token `security-data-flow`. Diese
Deskriptoren enthalten absichtlich keine Connector-Implementierungsregeln und
dürfen nicht in eine Connector-Runtime gelangen.

## Remediation und Akzeptanzkriterien

Die Remediation führt `runtime_materializable: false` ein. Dies wird nur
akzeptiert, wenn alle folgenden Bedingungen erfüllt sind:

1. `status` ist `connector-gap`;
2. `former_xfail` ist exakt true; und
3. `capabilities.runtime_verified` ist exakt false.

Der Runner schließt solche Fälle auch bei Force-All-Discovery aus, direkte
Materialisierung weist sie ab, und der Report-Generator gibt
`NOT_EXECUTABLE` / nicht hochstufbare Metadaten aus. Die normale nichtleere
`rules`-Pflicht bleibt für materialisierbare Fälle bestehen; die normalisierte
Capability wird registriert, ohne beliebige Capability-Strings zu akzeptieren.

Für die Akzeptanz müssen die 15 Deskriptoren den eingeschränkten Contract
bestehen; fokussierte Runner-/CLI- und Reporttests bestehen; Force-All-Discovery
darf die Deskriptoren nicht auswählen; direkte Materialisierung muss scheitern;
Framework-PR #51 muss Hosted-CI, SonarQube Cloud, Review und geschützte
Integration erfüllen; danach müssen der übernommene Exact-Head-Producer und
das strikte Terminal-Gate von Parent #74 bestehen.

## Evidence, Validierung und Restrisiko

Aufbewahrte begrenzte Evidence:
`/var/tmp/codex/runs/framework/20260726T145000Z-security-data-flow-case-schema/evidence/security-data-flow-case-schema-summary.md`
(SHA-256 `72c36838d9d868f50df8cc7e6dfe35fd0e72c59928415b9da1c84e828ad2ee90`).
Sie enthält Fehler-IDs, Contract und lokale Resultate, aber keine ungekürzten
Hosted-Logs oder Runner-Umgebungen.

Fokussierte Runner-/CLI- und Report-Generator-Suites bestanden mit 22 Tests.
Force-All-Discovery, Syntax-Kompilierung, der 15-Fälle-Security-Data-Flow-
Checker und Dokumentations-/Change-Record-Checks bestanden. Ruff und Pyright
sind nicht verfügbar und wurden nicht installiert. Ein isolierter No-MRTS-
Generator-Smoketest endete mit 0, hatte aber kein kanonisches Inputinventar;
seine generierte Ausgabe wurde verworfen.

Das Restrisiko bleibt sichtbares Connector-Gap-Inventar, bis eine
connector-eigene Implementierung Regeln und Live-Evidence liefert. Es werden
weder Runtime-Ergebnis, Hochstufung, Testschwächung noch Risikoakzeptanz
behauptet. Framework-PR #51 ist als `de705a5` gemergt; Parent #126 hat den
Gitlink bereits übernommen. Die verbleibende Evidenzlücke ist der frische
Parent-#74-Producer mit strengem Terminal-Gate, nicht eine Framework- oder
MRTS-Änderung.

## Verlauf

- 2026-07-26 — Aus Exact-Parent-#74-Hosted-Fehler und direkter Framework-
  Force-All-Discovery reproduziert; der vollständige 15-Fälle-Audit erkannte
  den fehlenden expliziten Deskriptorzustand und die Lücke im normalisierten
  Capability-Allowlist.
- 2026-07-26 — Die enge Framework-Reparatur wurde in einem isolierten
  Worktree implementiert und lokal validiert; Framework-Draft-PR
  [#51](https://github.com/Easton97-Jens/ModSecurity-test-Framework/pull/51)
  ist bei Exact Head `792bbffb1eefc7be0a9f76911729917d606eb00b` offen. Sein
  Hosted-Check-Zyklus läuft; ein Framework-Merge ist nicht autorisiert.
- 2026-07-26 — Alle sichtbaren Exact-Head-GitHub-Actions-Checks bestanden.
  SonarQube Cloud hat noch keine PR-Analyse erzeugt: Quality Gate ist `NONE`
  und New-Code-Measures sind leer. Der leere Issues-Endpoint wird nicht als
  Null-Issues-/Null-Duplikationsresultat behandelt; der Draft benötigt echte
  Sonar-Analyse, bevor Review-/Integrations-Evidence vollständig sein kann.
- 2026-07-26 — Framework-PR #51 erhielt später eine abgeschlossene
  SonarQube-Cloud-Analyse und wurde normal als
  `de705a5efb872f95f010346fe2e6143c88876ad4` gemergt. Die finalen sichtbaren
  PR-Checks einschließlich SonarQube Cloud Code Analysis bestanden. Direkter
  PR-#51-Readback meldet null offene/bestätigte Issues und null New-Code-
  Duplikation. Parent #126 hat den resultierenden Gitlink bereits übernommen;
  ein aufgefrischter Exact-Head-Producer und ein striktes Gate von Parent #74
  sind die einzigen ausstehenden Akzeptanzkontrollen.
