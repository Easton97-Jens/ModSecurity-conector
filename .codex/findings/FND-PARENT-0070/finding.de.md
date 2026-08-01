# FND-PARENT-0070 — Apache-APXS-Wrapper lässt einen privaten Common-Header bei frischer DSO-Materialisierung aus

## Identität

- Kategorie: build_defect
- Repository / Ownership: parent / parent
- Priorität / Schweregrad / Konfidenz: P1 / not_applicable / validated
- Status / Machbarkeit: fixed / feasible_now
- Release-Blocker / Candidate-Integration-Blocker / Sicherheitsrelevanz: true / false / true
- Scope: Resulting Parent-master 154ee724eba4653fa6378fc3c8729ae433e65697, tree-identical to final PR #183 head 4e4dfb36e1b05f7eda38450fd3710e3a04905118

## Zusammenfassung

**Aktuelle Resulting-Master-Disposition — 2026-07-29T11:27:25Z.** PR #183
mergte als Master `154ee724eba4653fa6378fc3c8729ae433e65697`; Tree
`c4d08e66d9b1929f4a56c81f3d5a021ea6ce4ef0` entspricht finalem Head
`4e4dfb36e1b05f7eda38450fd3710e3a04905118`, und alle 14 Master-SHA-Workflows
waren erfolgreich. Detached-Master-fokussierte Apache/MIME-Unit-Checks und
`make check-apache-common-adoption` bestanden. Diese Fakten ersetzen die
historische Kandidat-only-Formulierung unten, aber keinen frischen
Resulting-Master-APXS-/DSO-/HTTP-Lauf; das Finding bleibt `fixed`, nicht
`verified` oder `closed`.

Eine frische Apache-Connector-DSO-Materialisierung stagte request_helpers.c,
ließ aber seinen quoted private Header header_validation_internal.h aus. Der
zurückgehaltene Pre-Fix-Tree bestätigt, dass der Header fehlte, während der
Source-Header existiert, und der APXS-Wrapper die C-Source-Liste ohne diesen
Header kopierte.

Eine mutierbare Task-Worktree-Reparatur ergänzt den Header nun in dieser
Copy-Liste. Ihr frisch materialisierter Tree enthält den Header und erzeugte ein
DSO mit SHA-256 `fdaf666fccde82299a028f7c593412c379a61ea0e5a2074398d5a6994656919b`;
der Parent-Task meldet, dass der zugehörige saubere DSO-make erfolgreich war.
Dies ist daher **nur lokal fixed**, nicht verified oder closed: Die Reparatur
benötigt weiterhin einen unabhängig committeten PR-Exact-Head und eine
Reproduktion auf dem resultierenden Master.

Das P1-Release-Blocker-Flag bleibt für normale Apache-Connector-Builds aktiv,
bis diese Delivery-Evidence vorliegt. Der Defekt bestand bereits, wurde nicht
von selektivem #94A eingeführt und ist daher nicht dessen Integration-Blocker.

## Evidence und Grenze

| Artefakt | SHA-256 oder Ergebnis | Evidence |
| --- | --- | --- |
| Materialized-Source-Manifest | 65523487c8135066604a68c283217b34f00f241fe67ce241db1d8b65ecdaf4ff | Wrapper ist adapter-owned aus Parent-apxs-wrapper.in. |
| Materialisiertes Wrapper-Template | 35103aa90e4dea20a36ef8e84b659ebdde28f9bd68456ecf1460bc47be9a8d02 | Copy-Schleife staged request_helpers.c, lässt header_validation_internal.h aber aus. |
| Gestagtes request_helpers.c | e7c5473ce0228084bc2407548af20dbdb93f7ca2ba9c7757b60bbd93f2511659 | Inkludiert header_validation_internal.h bei Zeile 4. |
| Parent-Source-Header | b9ca7130e184913c10b3b24cfae18415eef411a908b1af5f926af6b695ed11e7 | Benötigter Header existiert in common/src. |
| Gestagter privater Header | fehlt; test -e endet 1 | Benötigter Sibling-Header fehlt in build/common-src. |
| Mutierbarer reparierter Wrapper | 723148f1b635b4d33c80b13860e1c8d3b6be4c984bde2400ad086b9c7501ed1f | Uncommitteter Task-Worktree-Snapshot ergänzt header_validation_internal.h. |
| Reparierter gestagter Header | b9ca7130e184913c10b3b24cfae18415eef411a908b1af5f926af6b695ed11e7 | Frischer reparierter Tree enthält den benötigten Header. |
| Repariertes DSO | fdaf666fccde82299a028f7c593412c379a61ea0e5a2074398d5a6994656919b | Frischer reparierter Tree erzeugte mod_security3.so. |

Der ausgewählte Kandidatencommit ist für den ursprünglichen betroffenen
Pfadvergleich exakt 9f23ae2c5fe908cef38f203be03f93fda75a8dd7, mit leerem
Base-zu-HEAD-Diff. Die Reparatur ist ein uncommitteter Working-Tree-Delta auf
diesem Checkout und daher kein exakter committeter PR-Head. Parent-Task-Evidence
meldet den ursprünglichen make-Fehler und den reparierten make-Erfolg; an einen
committeten PR-Head gebundene Raw-Command/stdout/stderr-Receipts bleiben
erforderliche Verifizierungsartefakte.

## Grundursache und Remediation-Richtung

Der Parent-APXS-Wrapper kopiert eine kuratierte Common-C-Source-Liste in ein
frisches build/common-src-Verzeichnis, kopiert aber nicht die privaten lokalen
Header, die diese Sources quoten. Framework-Materialisierung besitzt oder
entfernt diesen Wrapper-Vertrag nicht. Die nachgewiesene Reparatur gehört in den
Parent-Wrapper: den privaten Header stagen und einen fokussierten
Vollständigkeitsvertrag für jeden von einer gestagten Common-Source benötigten
quoted local Header ergänzen. Sie über einen unabhängigen committeten PR
promoten, danach einen sauberen frischen APXS-DSO-make mit Raw-Command/stdout/
stderr/Exit-Evidence sowie Apache-Konfigurations-/Load- und ausgewählte
HTTP-Legitimate-Controls auf dem exakten Head und dem resultierenden Master
ausführen. Den Fehler weder unterdrücken noch einen vorbestehenden Source-Tree-
Header als Fallback verwenden.

## Akzeptanz und Abgrenzung

Akzeptanz verlangt, dass der private Header in frischem build/common-src
erscheint, der saubere DSO-make mit Exit 0 endet, Apache normal lädt/
konfiguriert und ein negativer Contract die Auslassung eines benötigten lokalen
Headers zurückweist. Die nachgewiesene lokale Reparatur benötigt weiterhin einen
eigenen committeten exakten Head, frische Evidence und eine Reproduktion auf dem
resultierenden Master.

Dieser Record ist von FND-PARENT-0008 (historischer Clang-Initializer),
FND-PARENT-0064 (RulesSet-Lifecycle-Cleanup), FND-PARENT-0068
(Cleanup-Runner-TOCTOU) und FND-PARENT-0069 (GCC-C17-Warnungsgruppe) getrennt.
Er etabliert keinen attacker-kontrollierten Exploit-Pfad, blockiert aber bis
zur Remediation die normale Apache-Connector-Build-Delivery.

## Historie

- 2026-07-29T11:27:25Z: Die oben genannten Resulting-Master-Delivery-Fakten
  wurden abgeglichen; frische Master-APXS-/DSO-/HTTP-Validierung bleibt nötig.

- 2026-07-29T10:25:19Z: zurückgehaltene post-sentinel-Materialisierungs-
  Evidence erzeugte den kanonischen Parent-Build-Defekt-Record.
- 2026-07-29T10:33:55Z: die mutierbare Wrapper-Reparatur wurde frisch
  materialisiert; der gestagte Header und das resultierende DSO sind
  zurückgehalten, und der Parent-Task meldet einen erfolgreichen sauberen
  DSO-make. Status ist nur lokal fixed, bis committed-Exact-Head- und
  resulting-master-Validierung vorliegt.
