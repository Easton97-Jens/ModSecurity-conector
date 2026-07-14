# Architekturentscheidungsrecords

**Sprache:** [English](README.md) | Deutsch

## Zweck und Geltungsbereich

Dieses Verzeichnis ist der schlanke Ort für Architecture Decision Records
(ADRs) des Connector-Produkt-Monorepos. Es hält dauerhafte Entscheidungen fest,
deren Alternativen, Sicherheitsauswirkung, Test-/Evidence-Auswirkung und
Dokumentationsauswirkung überprüfbar bleiben müssen. Es ist kein Ort für
generierte Berichte, Runtime-Artefakte oder eine rückwirkende Umschreibung der
Historie.

Beim Anlegen dieses Verzeichnisses gab es weder einen versionierten ADR-Prozess
noch einen einzelnen ADR. Dieses README etabliert den Prozess; es ist selbst
kein ADR.

## Wann ein ADR anzulegen ist

Ein ADR ist vor oder zusammen mit einer wesentlichen Entscheidung anzulegen,
die eine Repository-Grenze, einen gemeinsamen Produktvertrag, eine Lifecycle-
Invariante, eine Sicherheitsgrenze oder Ort/Bedeutung wiederverwendbarer Tests
und Evidence ändert. Ein kleines Implementierungsdetail bleibt in seinem
zugehörigen Change Record, sofern seine Begründung keine spätere
connectorübergreifende Arbeit leiten wird.

Jeder ADR wird in diesem Verzeichnis als englisch-deutsches Paar namens
`ADR-<number>-<short-slug>.md` und `ADR-<number>-<short-slug>.de.md`
versioniert. Technische Literale, Status, Datum, Links, Codeblöcke und Tabellen
bleiben in beiden Dateien gleich. Den zugehörigen Change Record festhalten und
betroffene Konzept-, Architektur-, Konfigurations-, Sicherheits- und
Connector-Dokumentation aktualisieren.

## Verpflichtende Vorlage

Für jeden neuen ADR diese Vorlage verwenden. Jeden Platzhalter in
Winkelklammern ersetzen.

~~~text
# ADR-<number>: <title>

## ID
ADR-<number>

## Status
proposed | accepted | superseded | deprecated

## Date
YYYY-MM-DD

## Context
<problem, constraints, and evidence boundary>

## Decision
<decision and scope>

## Alternatives
<alternatives and why they were not selected>

## Consequences
<positive, negative, migration, and ownership consequences>

## Security impact
<trust, data, limits, failure, and residual-risk impact>

## Test and evidence impact
<required contract tests, runtime evidence, and non-claims>

## Affected documentation
<paths that must be updated>
~~~

## Empfohlene erste ADRs

Dies sind nur Empfehlungen. Sie gelten nicht als angenommene Entscheidungen,
bevor ihre eigenen ADR-Dateien geprüft und angenommen sind.

| Vorgeschlagene ID | Festzuhaltende Entscheidung | Warum sie dauerhaft sein sollte |
| --- | --- | --- |
| `ADR-001` | Parent-Produkt-Monorepo und unabhängiges Framework-Repository | Fixiert die Produkt-/Test-Ownership-Grenze. |
| `ADR-002` | Host-neutraler `common/`-Vertrag | Verhindert Server-/Proxy-SDK-Kopplung in Shared Code. |
| `ADR-003` | Geteilte P1--P4-Lifecycle-Semantik | Hält die beobachtbare Phasenbedeutung über Adapter hinweg konsistent. |
| `ADR-004` | Connector-Selbstständigkeit für Build, Packaging und Installation | Definiert, was für ein host-spezifisches Produkt vorhanden sein muss. |
| `ADR-005` | Parent-Produktvertragstests gegenüber wiederverwendbaren Framework-Tests | Macht künftige Testablage und Evidence-Ownership überprüfbar. |

## Evidence-Grenze

Ein ADR darf Code, Konfiguration, Tests, Berichte oder einen Change Record
zitieren, muss aber `verified`, `documented_not_runtime_verified`,
`compatibility_only`, `unknown` und `out_of_scope` wie im
[Repository-Konzept](../repository-concept.de.md) unterscheiden. Ein ADR macht
ohne abgegrenzte kanonische Evidence keinen Runtime-PASS- oder
Production-Ready-Claim.
