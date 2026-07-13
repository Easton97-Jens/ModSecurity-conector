# Connector-Readiness

**Sprache:** [English](readiness.md) | Deutsch

## Aktuelle Evidenzgrenze

Die ausgewählten echten HTTP/1.1-Hostpfade schlossen den gemeinsamen
kanonischen Lauf `six-connectors-core-final-20260712T164725Z-e16e7f1` ab.
Jeder ausgewählte Runner und das Aggregat-Target
`full-lifecycle-all-connectors` endeten mit `0`; das read-only Gate
`make check-six-connector-core-completion` bestand.

Dies ist abgegrenzte Common-/libmodsecurity-Host-Evidence für den ausgewählten
Kern. Sie ersetzt keine lauflokalen Artefakte und belegt weder eine
vollständige Connector-Matrix noch eine Capability-Promotion oder ein
Production-Ergebnis.

| Connector | Ausgewählte Integration | Ausgewählter HTTP/1.1-Kern | Erweiterter Katalog | Geltungsgrenze |
| --- | --- | --- | --- | --- |
| Apache | `native-httpd-module` | PASS | NOT EXECUTED | Nur ausgewählter P1--P4-Kern |
| NGINX | `native-nginx-http-module` | PASS | NOT EXECUTED | Nur ausgewählter P1--P4-Kern |
| HAProxy | `native-htx-filter` | PASS | NOT EXECUTED | Nur ausgewählter P1--P4-Kern |
| Envoy | `ext_proc` | PASS | NOT EXECUTED | Nur ausgewählter P1--P4-Kern |
| Traefik | `native-traefik-middleware` | PASS | NOT EXECUTED | Nur ausgewählter P1--P4-Kern |
| lighttpd | `patched-native-lighttpd` | PASS | NOT EXECUTED | Nur ausgewählter P1--P4-Kern |

Der Kern umfasst die ausgewählten P1-, P2-, P3-, P4-Regel-1100301-, Safe-
Late-Action-, First-Byte-vor-EOS-, No-Full-Response-Buffer-, Event-Privacy-
und Cleanup-Beobachtungen. Die genauen Evidence-Zeilen und Hostpfaddetails
stehen im [Kernabschluss](core-completion.de.md).

## Aktuelle technische Grenzen

- Ein ausgewähltes P4-Safe-Ergebnis ist nach Commit ein angefordertes `deny`
  mit tatsächlichem `log_only`, sichtbarem HTTP 200, gesendeten Headern/Body
  und ohne Connection-Abort.
- Response-Body-Chunks werden inkrementell ingestiert; die ausgewählte
  Phase-4-Regel wird bei End of Stream ausgewertet. Das ist kein Claim über
  Entscheidungen pro Chunk.
- Strict-Post-Commit-Enforcement, HTTP/2, HTTP/3, Compression-Verarbeitung
  und der erweiterte Katalog bleiben getrennte Hardening- oder Evidence-Arbeit.
- Capability-Deklarationen bleiben im generierten
  [Connector-Capability-Katalog](../testing/generated/canonical/connector-capabilities.generated.de.md)
  maschinenlesbar. Sie werden nicht durch Statusprosa ersetzt.

## Aktuelle Sources of Truth

| Thema | Kanonische Quelle |
| --- | --- |
| Ausgewählte Sechs-Connector-Kern-Evidence | [Kernabschluss](core-completion.de.md) |
| Architektur-, Runtime-Root-, Transport- und Evidence-Audit | [Architektur- und Evidence-Audit](../audits/architecture-and-evidence.de.md) |
| Generierte Capability-Deklarationen | [Connector-Capability-Katalog](../testing/generated/canonical/connector-capabilities.generated.de.md) |
| Connector-Konfigurationsoptionen | [Konfigurationsinventar](../connector-configuration-inventory.json) und die verlinkten Beispielreferenzen |

Historische Planung, Pre-Core-Snapshots und Connector-spezifische No-CRS-
Prosa-Snapshots wurden in diese aktuellen Quellen konsolidiert. Die Git-
Historie bewahrt ihre Chronologie, ohne konkurrierende aktuelle
Statusdokumente zu behalten.

## Bewusst nicht erhobene Claims

- Production-Readiness, Production-Hardening, Runtime-Sicherheit oder
  Sicherheitsverifikation;
- CRS-Verifikation, CRS-Vollständigkeit oder vollständige Full-Matrix-
  Verifikation;
- vollständige HTTP/2- oder HTTP/3-Verifikation; oder
- Strict-Post-Commit-Enforcement außerhalb des ausgewählten kompakten Kerns.
