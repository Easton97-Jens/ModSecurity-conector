# ADR-003: Gemeinsame P1--P4-Lifecycle-Semantik

**Sprache:** [English](ADR-003-shared-p1-p4-lifecycle-semantics.md) | Deutsch

## ID

ADR-003

## Status

accepted

## Date

2026-08-25

## Context

Die zehn benannten Connectorlösungen stellen unterschiedliche Host-Callbacks und
Protokollgrenzen bereit. Das Produkt benötigt dennoch eine einzige
quellengestützte Bedeutung für P1, P2, P3 und P4, eine Entscheidungstaxonomie,
begrenzten gehaltenen Zustand und deterministisches Lifecycle-Cleanup. Diese
Entscheidung ist auf Parent-Quellcode, lokale Tests und Dokumentation beschränkt.
CI, Branch-Governance, Rulesets und Required Checks liegen außerhalb des Scopes.

Die Implementierungsevidenz bestimmt P1 als Request-Header nach den
Connection/URI-Voraussetzungen und vor dem Request-Commit; P2 als begrenzte
Request-Body-Aufnahme mit genau einer Request-EOS-Entscheidung; P3 als
Response-Header vor dem Response-Commit, solange der ursprüngliche Status
veränderbar ist; und P4 als begrenzte Response-Body-Aufnahme mit genau einer
Response-EOS-Entscheidung. Connection, URI und Logging bleiben
Host-Lifecycle-Voraussetzungen oder Epiloge, keine zusätzlichen Fachphasen.

Derzeit ist kein versionierter Change Record zugeordnet: Die Repository-
Archivrichtlinie verlangt eine explizite Record-Entscheidung, und solange die
Akzeptanzkriterien für alle zehn Lösungen unvollständig sind, ist keine
Auslieferung möglich.

## Decision

`msconnector_transaction_contract` ist der einzige kanonische Common-
Transaktionsdatensatz fester Größe und endliche Zustandsautomat für jede
benannte Connectorlösung. Er besitzt validierte Transaktions- und
Hostidentitäten, P1--P4-Reihenfolge, begrenzte Request-/Response-Metadaten und
Body-Zähler, Entscheidungs-/Rule-ID-/Aktions-/Modus-/Fehlerkorrelation,
Zeitfelder, Response-Commit und Cleanupstatus. Gehaltener Contract-/Event-
Zustand enthält ausschließlich Metadaten, niemals Request- oder
Response-Payload-Bytes.

Jeder Hostadapter wählt ein explizites Connectorprofil. Ein Profil ordnet eine
Phase entweder direkt über einen Host-Callback zu oder markiert P3/P4 als
`COMPANION_REQUIRED`. Ein Request-only-Protokoll darf Letzteres nur mit einer
verpflichtenden privaten Response-Komponente erfüllen, die eine
servergenerierte opaque Capability genau einmal übergibt und claimt. Die
Response-Komponente ist Teil der logischen Connectorlösung und kein optionaler
Capability-Fallback.

Der gemeinsame MRC1-Response-Companion-Transport bleibt die Autorität für
begrenztes Framing, private UDS-Identität, Timeout, Cleanup und die Reihenfolge
der Response-Operationen. Die HAProxy-SPOE/SPOP-Bridge verwendet den
Common-Protokoll-/Parserkern plus ein owner-erhaltendes SPOP-Backend; sie kopiert
weder MRC1-Framing noch legt sie einen nativen Transaktionspointer dem
HTX-Prozess offen. Die ausgewählte Stock-lighttpd-Lösung ist das
traffic-owning `stock-lighttpd-sidecar`: Ein privates Sidecar mit wörtlichem
Loopback und HTTP/1.1 besitzt einen begrenzten Austausch und führt P1--P4
direkt aus. Die native `stock-lighttpd`-Modulroute bleibt eine ausdrücklich
nichtkanonische P1/P3-Kompatibilitätsübersetzung und niemals ein impliziter
Fallback. Die gepatchte lighttpd-Route bleibt eine eigene Connectorlösung.

## Alternatives

1. Unabhängige host-spezifische Phasenbedeutung und Entscheidungspolitik
   beibehalten. Abgelehnt: Dies erlaubt abweichende Fachsemantik und
   inkonsistentes Cleanup.
2. P3/P4 für Request-only-Protokolle als `not_applicable` deklarieren.
   Abgelehnt: Dies entfernt erforderlichen Response-Schutz, statt die
   Protokollgrenze zu lösen.
3. Einen Traffic-besitzenden generischen Sidecar für Stock lighttpd ergänzen.
   Für die kanonische Stock-Lösung ausgewählt: Das Sidecar ist ein bewusst
   begrenzter privater Loopback-HTTP/1.1-Traffic-Eigentümer, während das native
   Stock-Modul eine ausdrückliche P1/P3-Kompatibilitätsübersetzung und kein
   Fallback bleibt.
4. MRC1 in einem HAProxy-lokalen UDS-Server duplizieren. Abgelehnt: Framing,
   Limits, Peer-Authentifizierung, Capability-Behandlung, Timeout und Cleanup
   würden von Common abweichen.

## Consequences

Direkte Adapter müssen jede Phase genau einmal beginnen und abschließen,
begrenzte Metadaten-/Body-Zähler erfassen, Entscheidungen über die
Common-Taxonomie abbilden und vor dem Cleanup abschließen oder canceln.
Companion-Adapter dürfen keinen unbeschränkten transaktionsübergreifenden
Zustand halten, müssen opaque Single-Claim-Korrelation mit begrenzter Kapazität
und TTL verwenden und bei fehlender, abgelaufener, wiederholter oder
fehlerhafter Korrelation fail-closed sein.

Hostaktionen bleiben host-spezifische Übersetzungen. Ein Pre-Commit Block oder
Redirect kann zu einer veränderbaren HTTP-Antwort werden; eine Post-Commit
Strict-Entscheidung kann zu einem dokumentierten Connection-Abort werden, wenn
der Host Bytes nicht sicher umschreiben kann. Dies ist ein
Übersetzungsunterschied und keine Änderung der kanonischen
Entscheidungsbedeutung.

Die Entscheidung hält aktuelle Evidenzlücken absichtlich sichtbar. Sie stuft
Source-Wiring nicht zu einem nativen Stock-Modul-Host-Runtime-Pass hoch:
P2/P4 kommen aus dem separat ausgewählten traffic-owning Sidecar, nicht aus
dem unveränderten Stock-Modul. Ein nicht integrierter HAProxy-Companion gilt
weiterhin nicht als vollständige P1--P4-Route. Das Sidecar bindet nur an
wörtliches Loopback, besitzt Cleanup in einem Worker und benötigt daher keine
prozessübergreifende Korrelation oder TTL-Registry; sein Event-JSONL bleibt
metadaten-only.

## Security impact

Der Vertrag erzwingt Header-, Body-, Event-, Frame-, Kapazitäts- und TTL-Limits;
lehnt ungültige, doppelte, übersprungene, verspätete, terminale und bereinigte
Phasenübergänge ab; und macht Cancel, Timeout, Engine-/Protokollfehler und
unvollständiges Cleanup zu expliziten terminalen Ergebnissen. MRC1 erfordert ein
ausschließlich vom Owner nutzbares Parent-Verzeichnis, einen privaten Socket,
unterstützte Peer-Credentials, begrenzte Frames und eine opaque Capability, die
keine clientgesteuerte Transaktionsidentität ist.

Event JSONL enthält ausschließlich Metadaten. Auf der Response-Observer-
Protokollgrenze befinden sich weder Body-Payload, nativer Transaktionspointer,
Hostidentität noch ein unbeschränkter Request-Key. Kein stiller Versions- oder
Capability-Fallback ist zulässig.

## Test and evidence impact

Die verpflichtende lokale Contract-Suite deckt gültige/ungültige Reihenfolge,
doppelte und fehlende Phasen, Limits, alle kanonischen Entscheidungsarten in
Safe/Strict-Modi, Timeouts, Cancel, Cleanup, Kapazitätsrückgewinnung, parallele
Transaktionen und zwei sequenzielle Transaktionen auf einer MRC1-Verbindung ab.
Adapter-Source-/Komponententests decken ihre engen Hostübersetzungen ab.
Isolierte Envoy-`ext_authz`- und Traefik-`forwardAuth`-Runtime-Receipts
prüfen ihre Response-Companions.

Dieser ADR beansprucht keinen vollständigen Production-Runtime-Pass für alle
zehn Lösungen. Insbesondere bleiben native Apache/NGINX/lighttpd-Host-Receipts
separat zu belegen; die kanonische Stock-P2/P4-Evidence gilt für das Sidecar,
während das unveränderte native Stock-Modul P1/P3-only bleibt. Die kombinierte
HAProxy-MRC1-v2-Evidence ist lokal und qualifiziert, keine pauschale
Produktionsreifebehauptung.

## Affected documentation

- `common/docs/transaction-phase-contract.md`
- `common/docs/transaction-phase-contract.de.md`
- `common/docs/design.md`
- `common/docs/design.de.md`
- `docs/architecture.md`
- `docs/architecture.de.md`
- `connectors/*/capabilities.json`
