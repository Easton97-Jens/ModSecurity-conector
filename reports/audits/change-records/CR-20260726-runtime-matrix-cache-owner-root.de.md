# Change Record: Parent-Runtime-Matrix-Cache-Owner-Root-Handoff

**Sprache:** [English](CR-20260726-runtime-matrix-cache-owner-root.md) | Deutsch

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | CR-20260726-runtime-matrix-cache-owner-root |
| Datum (UTC) | 2026-07-26 |
| Basis-Revision | 6ca7e1536ce7e93da68099db9c586b88852ff13e |
| Grenze | Parent-Runtime-Matrix-Shell-Handoff, ein Parent-Regressionstest und dieses englisch/deutsche Change-Record-Paar mit Index. Der mitgeführte Framework-Gitlink ist bereits auf Parent-`master` gemergt; hier werden weder Framework- noch MRTS-Quellen geändert. |
| Finding-Verknüpfung | FND-CROSS-0008; FND-CROSS-0001 bleibt offen, bis frische legitime Runtime-Evidence das strikte Terminal-Gate besteht. |

## Motivation und Problemstellung

Die vollständige Parent-Runtime-Matrix behält ihren Job-spezifischen
`BUILD_ROOT` für Logs, temporäre Dateien, Ergebnisse und isolierte Connector-
Ausführung. Cache-gestützte Apache- und NGINX-Connector-Builds gehören jedoch
nicht zu diesem Job-Root. Der Runner leitet jetzt einen engen Owner Root aus
dem verifizierten Component-Cache ab:

```text
CONNECTOR_COMPONENT_CACHE/builds/connectors
```

Er validiert diesen Root und jeden Apache-/NGINX-Build-Pfad vor dem Connector-
Aufruf. Ein Cache-Build-Pfad außerhalb des abgeleiteten Roots wird abgewiesen,
bevor `make` läuft. Für einen akzeptierten Pfad übergibt der Runner denselben
expliziten Root als `APACHE_BUILD_OWNER_ROOT` beziehungsweise
`NGINX_BUILD_OWNER_ROOT`; er weitet `BUILD_ROOT` nicht auf und deaktiviert den
Framework-Löschguard nicht.

Parent-PR #125 führt bereits Framework-Commit
`a7ebf5a1d9cad2b0a65a7603476a1434fdb16cf6`, der die Framework-NGINX-Owner-
Root-Fähigkeit enthält. Diese Änderung verwendet diese Fähigkeit an der Parent-
eigenen Matrix-Grenze; sie verändert den Gitlink nicht über das normale
Branch-Update von `master` hinaus.

## Akzeptanzkriterien

- Cache-gestützte Apache- und NGINX-Refreshes erhalten denselben expliziten
  Owner Root aus `CONNECTOR_COMPONENT_CACHE/builds/connectors`.
- Ein Connector-Build-Pfad außerhalb dieses engen Roots schlägt fehl, bevor
  `make` aufgerufen wird.
- Der isolierte Job-`BUILD_ROOT` bleibt vom Cache-Owner-Root getrennt.
- Weder Löschguard, striktes Evidence-Gate, SonarQube-Cloud-Policy noch
  Branch-Schutz werden gelockert.
- Der aktualisierte exakte PR-#74-Head benötigt weiterhin vollständige Hosted-
  Producer-, Terminal-Gate-, SonarQube-Cloud-, Review- und Protected-
  Integration-Evidence.

## Implementierungsentscheidung und Begründung

Der betroffene Sink ist der Framework-Refresh-Löschguard. Die erzwungene
Invariante lautet: Ein Refresh-Target muss ein absoluter, sicher generierter
Pfad unter dem expliziten Connector-Cache-Build-Owner-Root sein. Die Parent-
Kontrolle verwendet den Framework-Helper für kanonischen Pfad-Containment vor
dem Dispatch; der Framework-Guard lehnt am Löschpunkt weiterhin unsichere,
relative, symlinked, Sibling- oder Systempfade ab.

Legitime vorbereitete Cache-Builds bleiben refreshbar. Ein Nicht-Cache-Build-
Root wird jetzt abgewiesen, statt einen Connector-Provisioning-Pfad mit nicht
zugehöriger Ownership zu erreichen. Es werden weder Cleanup, `REFRESH`-
Deaktivierung, Suppression, Quality-Gate-Änderung noch ein Branch-Protection-
Bypass verwendet.

## Geänderte Dateien

- `ci/runtime/lifecycle/run-full-matrix-parallel.sh`: leitet den engen
  Connector-Cache-Owner-Root ab, validiert ihn und übergibt ihn an Apache und
  NGINX.
- `tests/test_full_matrix_cache_owner_root.py`: kontrollierte Same-Boundary-
  Positiv- und Outside-Owner-Ablehnungstests.
- `modules/ModSecurity-test-Framework`: der normale Merge von aktuellem
  Parent-Master führt seinen bereits integrierten Gitlink mit.
- `reports/audits/change-records/README.md`, `README.de.md` sowie dieser
  gepaarte Change Record.

## Ausgeführte Befehle

- `sh -n ci/runtime/lifecycle/run-full-matrix-parallel.sh` — bestanden.
- `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest tests.test_full_matrix_cache_owner_root`
  — bestanden (zwei Tests). Die Positivkontrolle führt den echten Matrix-Shell-
  Runner mit einer kontrollierten `make`-Grenze aus und prüft explizite Apache-
  und NGINX-Owner-Roots bei `REFRESH=1`. Die Negativkontrolle verwendet einen
  außerhalb liegenden Build-Root und prüft die Ablehnung vor `make`.
- `git diff --check` — bestanden.

## Security-Auswirkung

Dies ist eine Pfad-Containment-Korrektur am Parent-zu-Framework-Handoff. Sie
hält einen Cache-Build in seinem deklarierten Owner Root und bewahrt den
Framework-Löschguard als finalen fail-closed Sink. Keine Vertrauensgrenze wird
aufgeweitet.

## Runtime-Evidence

Die kontrollierte Regression führt den echten Parent-Matrix-Shell-Runner aus
und beobachtet dessen Connector-Dispatch-Umgebung. Sie ist kein nativer
Connector-Build, Host-Deployment oder vollständiger Runtime-Evidence-Producer;
dies bleibt für den aktualisierten exakten PR-#74-Head erforderlich.

## Bekannte Einschränkungen

Die lokalen Kontrollen ersetzen `make` nur an der finalen Connector-Smoke-
Grenze und behaupten daher keinen Apache- oder NGINX-Build. Die zugehörigen
Framework-Owner-Root-Löschkontrollen wurden separat gemergt und validiert. Das
strikte Parent-Evidence-Gate lief für diesen künftigen #74-Head noch nicht.

## Verbleibende Risiken

FND-CROSS-0008 und FND-CROSS-0001 bleiben offen, bis der Hosted-Exact-Head-
Producer legitime Cache-gestützte Evidence durch das strikte Gate nachweist.
Kein Risiko wird akzeptiert.

## Nicht ausgeführte Prüfungen mit Begründung

Kein lokaler vollständiger Connector-Build oder echte Host-/Runtime-Matrix wird
behauptet. Sie benötigt die autoritative Hosted-Producer-Umgebung und bleibt
für den aktualisierten exakten Parent-PR-#74-Head erforderlich, ebenso das
strikte Terminal-Evidence-Gate, SonarQube-Cloud-Issue-/Duplikations-Readback,
Reviews und geschützte Merge-Voraussetzungen.

Kein Framework- oder MRTS-Source-Test und keine solche Änderung gehört zu
dieser Parent-Änderung. Framework-Owner-Root-Kontrollen wurden unabhängig vor
diesem Handoff gemergt.

## Finaler Diff- und Review-Status

Der lokale Diff ist auf den Parent-Matrix-Handoff, seinen fokussierten
Regressionstest, das normale Master-Gitlink-Update und diesen zweisprachigen
Record/Index begrenzt. Er bestand lokale Syntax-, fokussierte Security-/Pfad-,
CI-Sicherheitsvertrags-, Dokumentationslink- und Whitespace-Checks. Vor einem
geschützten Merge sind weiterhin frische Exact-Head-Hosted-Validierung und
Review erforderlich.
