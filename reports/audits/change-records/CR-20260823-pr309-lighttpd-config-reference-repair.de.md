# Change Record CR-20260823: PR-#309-Lighttpd-Config-Reference-Reparatur

**Sprache:** [English](CR-20260823-pr309-lighttpd-config-reference-repair.md) | Deutsch

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | `CR-20260823-pr309-lighttpd-config-reference-repair` |
| Datum (UTC) | `2026-08-23` |
| Basis-Revision | `7c403fada21de4547259fef1dc4a1b079cb0cb25` |
| Scope | Nur Parent-Repository: geschlossene Lighttpd-Config-Reference-Extraktion, ein fokussierter Regressionstest, generiertes englisches/deutsches Referenzmaterial und gekoppelte Nachvollziehbarkeit. Keine Framework-, MRTS-, Gitlink-, Connector-Runtime-Source-, Workflow-, Dependency-, Toolchain-, NGINX- oder Quality-Gate-Konfigurationsänderung. |

## Motivation und Problemstellung

Nachdem Parent-PR [#309](https://github.com/Easton97-Jens/ModSecurity-conector/pull/309)
auf der Basis-Revision per Squash gemergt wurde, stoppten seine gemeinsamen
`test-common`- und `test-apache`-Pfade, bevor ein Host starten konnte. Der
erste Fehler kam aus `extract_lighttpd()`: Sein geschlossenes erwartetes
Inventory führte noch zwei native Plugin-Direktiven, während
`connectors/lighttpd/module/mod_msconnector.c` jetzt genau drei deklariert.

Die fehlende Direktive ist `msconnector.expose-host-transaction-id`. Sie ist
eine bestehende, standardmäßig deaktivierte, serverspezifische Evidence-Option.
Diese Reparatur stellt den quellbasierten Dokumentationsvertrag wieder her,
ohne den Extractor zu erweitern oder die native Lighttpd-Runtime zu ändern.

## Akzeptanzkriterien

- Genau die drei nativen Lighttpd-Direktiven mit ihren Source-Typen und
  Server-Scopes verlangen; einen unerwarteten Schlüssel, Typ oder Scope
  ablehnen.
- Die bestehende Transaction-ID-Evidence-Option in generierten englischen und
  deutschen Config-References sowie im maschinenlesbaren Inventory dokumentieren.
- Ihre standardmäßig deaktivierte, servergenerierte und nicht Request-
  reflektierende Semantik erhalten.
- Einen fokussierten Regressionstest für das geschlossene Inventory und die
  Optionssemantik ergänzen.
- Framework/MRTS/Gitlinks, Workflows, Dependencies, Toolchains und
  Quality-Controls erhalten.
- Nach Commit und Push dieses Traceability-Records eine frische Exact-Head-
  Hosted-Validierung erhalten; kein historisches Check-Ergebnis gilt als
  Evidence für einen neuen Head.

## Implementierungsentscheidung und Begründung

- `extract_lighttpd()` behält den geschlossenen geordneten Tuple-Vergleich für
  `msconnector.enabled`, `msconnector.config-file` und
  `msconnector.expose-host-transaction-id`; es verwendet weder Wildcard noch
  permissiven Parser.
- Die neue Dokumentationszeile wird aus der bestehenden nativen Source erzeugt.
  Ihr P3-Response-Header trägt nach der Response-Header-Verarbeitung eine
  servergenerierte Host-Transaction-ID und verändert keine Common-Runtime-
  Transaction-ID-Eingabe.
- Wiederholte Lighttpd-Metadatenliterale sind nur benannte Konstanten; ihre
  Werte und die Semantik der generierten Ausgabe bleiben unverändert.
- Der Generator und nicht nur generierte Dateien ist die Quelle des
  Dokumentationsupdates.

## Alternativen

- Ein permissiver Extractor oder ein Wildcard-Inventory wurde abgelehnt, weil
  es künftigen Drift nativer Direktiven verdecken würde, statt fail closed zu
  reagieren.
- Generiertes Markdown und JSON ohne Generatoränderung zu editieren wurde
  abgelehnt, weil Generierungschecks dies sofort überschreiben oder ablehnen
  würden.
- Native Lighttpd-Runtime-Source zu ändern war nicht nötig: Die Option besteht
  bereits, und der Defekt lag ausschließlich im veralteten
  Dokumentationsvertrag.

## Kompatibilitätsauswirkung

Die generierte Reference und das Inventory weisen jetzt eine bestehende
standardmäßig deaktivierte Direktive aus. Es ändern sich keine Runtime-
Konfigurationssyntax, kein Default, kein Request-Verhalten, kein Response-
Verhalten, keine Connector-ABI, Dependency, Toolchain oder Repository-Grenze.

## Security-Auswirkung

Der korrigierte Vertrag ist sicherheitsrelevant, weil er einen opt-in
Response-Header beschreibt. Die Reparatur erhält das geschlossene
Source-Inventory und dokumentiert, dass der Wert servergeneriert,
standardmäßig deaktiviert und niemals ein Request-Header-Reflex ist. Sie ändert
keinen Request-Parser-, Header-Emissions-, Privileg-, Datei-, Namespace- oder
Runtime-Entscheidungspfad. Ein fokussiertes Security-Review fand keine
berichtspflichtige Regression.

## Geänderte Dateien

- `ci/checks/documentation/connector_config_reference.py`
- `tests/test_connector_config_reference.py`
- `examples/lighttpd/configuration-reference.md`
- `examples/lighttpd/configuration-reference.de.md`
- `reports/connector-configuration-inventory.json`
- `reports/audits/change-records/CR-20260823-pr309-lighttpd-config-reference-repair.md`
- `reports/audits/change-records/CR-20260823-pr309-lighttpd-config-reference-repair.de.md`
- `reports/audits/change-records/README.md`
- `reports/audits/change-records/README.de.md`

## Ausgeführte Befehle

### Tests und tatsächliche Ergebnisse

| Check | Tatsächliches Ergebnis |
| --- | --- |
| `python -m unittest -v tests/test_connector_config_reference.py` | Bestanden: 2 Tests. |
| `make check-connector-config-reference` | Bestanden; quellbasierte Generierung und semantische Inventory-Validierung abgeschlossen. |
| `python -m unittest -v connectors.lighttpd.tests.test_patched_host_contract` | Bestanden: 35 Tests, 2 übersprungen. |
| `make check-doc-links` | Bestanden. |
| `make check-bilingual-docs` | Bestanden. |
| `make check-variable-documentation` | Bestanden. |
| Fokussierte Python-Kompilierung | Bestanden. |
| Fokussiertes Security-Diff-Review | Bestanden: kein berichtspflichtiger Fund und keine sicherheitsrelevante Regression. |
| `git diff --check` | Auf dem finalen Delivery-Diff vor dem Staging bestanden; erneuter Lauf für den gestagten Commit erfolgt. |

## Runtime-Evidence

Diese Reparatur ändert einen Source-zu-Dokumentation-Vertrag, keinen
Connector-Runtimepfad. Der ursprüngliche Fehler trat in der gemeinsamen
Config-Reference-Validierung auf, bevor Apache oder Lighttpd starteten. Die
Regressionstests liefern daher die relevante Evidence: Sie führen den
geschlossenen Extractor gegen die native Source aus und prüfen die generierten
Vertragsmetadaten.

## Nicht ausgeführte Prüfungen mit Begründung

- Vollständiges lokales `make lint` kann in dieser Umgebung nicht enden, weil
  seine gemeinsame Provisionierung nicht verfügbare gepinnte NGINX-/HAProxy-
  Eingaben benötigt. Kein Check wurde abgeschwächt und kein Environment-
  Fallback verwendet.
- Das Projekt pinnt Go `1.26.7`, lokal waren nur Go `1.26.6` und `1.26.5`
  aufrufbar. Es wurde keine Toolchain akquiriert; Hosted-Go-Checks sind auf
  dem finalen PR-Head erforderlich.
- Frische Hosted-, SonarCloud- und Master-Checks für den durch diesen Record
  erzeugten Head waren beim Schreiben dieses Dokuments ausstehend und werden
  hier nicht behauptet.

## Bekannte Einschränkungen

Dieser Record kann die fehlgeschlagene Post-Merge-Check-Historie von PR #309
nicht rückwirkend ändern. Er dokumentiert den Lifecycle des korrigierenden PR
und verlangt Exact-Head-Erfolg für den Successor-Head und die resultierende
`master`-Revision.

## Verbleibende Risiken

Eine zukünftige Änderung nativer Lighttpd-Direktiven wird korrekt fail closed,
bis das quellbasierte Inventory und sein Regressionstest gemeinsam aktualisiert
sind. Die aktuelle Reparatur erzeugt oder beansprucht keine neue Lighttpd-
Runtime-Evidence.

## Finaler Diff- und Review-Status

Die Parent-only-Korrektur ist für einen frischen normalen Commit, Exact-Head-
Review und geschützten PR-Merge vorbereitet. Dieser Change Record autorisiert
selbst keinen Merge, keine Framework-/MRTS-Änderung, kein Gitlink-Update,
keinen direkten `master`-Push und keine Quality-Control-Änderung.

## Auslieferungsstatus

Dieser Record wird als fokussierte Fortsetzung von Parent-PR #334 committed.
Sein neuer Head benötigt eine vollständige frische Hosted- und SonarCloud-
Validierungsrunde, bevor die aktuelle explizite Master-Autorisierung ausgeübt
werden darf. Dieser Record behauptet kein Merge-Ergebnis.
