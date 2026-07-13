# Architektur- und Evidence-Audit

**Sprache:** [English](architecture-and-evidence.md) | Deutsch

## Geltungsbereich

Dieses Audit konsolidiert die aufbewahrten architektur- und evidence-relevanten
Befunde für die sechs ausgewählten Connectoren. Es ist ein Source- und
Contract-Audit; Runtime-PASS-Aussagen bleiben auf den kanonischen Lauf im
[Kernabschluss](../current/core-completion.de.md) begrenzt.

## Gemeinsamer Architekturvertrag

Das Common SDK stellt einen Transaktions-Lifecycle bereit: Begin, Request-
Header, Request-Body Append/Finish, Response-Header, Response-Body
Append/Finish und Transaction Finish/Destroy. Host-Adapter verantworten ihr
Hook-Timing und halten Body-Chunks nur für den Aufruf geliehen; der Common-
Vertrag autorisiert kein connector-eigenes vollständiges Response-Buffering.

Runtime-Roots werden je Connector unter dem vom Aufrufer gewählten
`VERIFIED_RUN_ROOT` abgeleitet. Evidence-, Build-, Run- und Log-Roots sind
isoliert, während der wiederverwendbare Komponenten-Cache unter
`cache-v2/shared` liegt. Das ist Pfad- und Cache-Plumbing, kein eigenständiger
Connector-Runtime-Nachweis.

| Connector | Ausgewählte Hostroute | Audit-relevante Grenze |
| --- | --- | --- |
| Apache | natives httpd-Modul | Hostfilter bestimmen Commit- und EOS-Timing. |
| NGINX | natives HTTP-Modul | Filterreihenfolge und EOS bestimmen den Response-Body-Abschluss. |
| HAProxy | nativer HTX-Filter | Native HTX ist vom SPOP-Compatibility-Pfad getrennt. |
| Envoy | `ext_proc` | Gestreamte Verarbeitung ist von `ext_authz`-Compatibility getrennt. |
| Traefik | native Local-Plugin-Middleware | Native Middleware ist von `forwardAuth`-Compatibility getrennt. |
| lighttpd | gepatchter nativer Entity-Body-Host | Der ausgewählte Response-Body-Pfad ist versionsgebunden und gepatcht. |

## Evidence- und Transportgrenze

Der ausgewählte gemeinsame HTTP/1.1-Kernlauf beobachtete P1--P4-
Regelverarbeitung, Safe-Late-Action, First-Byte-vor-EOS, keinen vollständigen
Response-Buffer, Event-Privacy und Cleanup für jede ausgewählte Hostroute.
Seine vollständige abgegrenzte Aussage steht im
[Kernabschluss](../current/core-completion.de.md); der aktuelle Status und der
verbleibende Umfang stehen in der [Readiness](../current/readiness.de.md).

Für die ausgewählte Safe-Evidence wird ein angefordertes `deny` nach Commit zu
tatsächlichem `log_only`, belässt sichtbares HTTP 200 und bricht die Verbindung
nicht ab. Das Audit macht daraus weder eine Pre-Commit-Deny noch ein Strict-
Transportergebnis. Events enthalten nur Metadaten: Transaktions-/Regel-IDs,
Actions, Timing und Byte-Zähler dürfen aufgezeichnet werden, Request- oder
Response-Body-Payloads sind jedoch keine Evidence-Felder.

## Konfigurations- und Evidence-Governance

- Registrierte Connector-Optionen, Common-Runtime-Keys, ModSecurity-
  Direktiven und Beispielregel-Syntax werden durch das generierte
  [Konfigurationsinventar](../connector-configuration-inventory.json)
  nachverfolgt.
- Generierte Runtime-Berichte bleiben durch die Report-Registry und den
  Layoutcheck `make report-governance` kontrolliert. Generierte Evidence wird
  nicht als Ersatz für einen neuen Runtime-Lauf editiert.
- Compatibility-Routen sind als Compatibility-Routen dokumentiert; sie
  ersetzen weder die ausgewählte native Kernroute noch promoten sie deren
  Capabilities.

## Historischer Kontext

Frühere Common-Adoption-, Local-Build-, Runtime-Root-, Transport-, Promotion-
und Pre-Host-Integration-Audits sind hier konsolidiert. Ihre detaillierten
Pläne, temporären Umgebungsbeobachtungen und Pre-Core-Statusmatrizen sind keine
aktuelle Evidence. Die Git-Historie bewahrt diese Snapshots, ohne parallele
aktuelle Berichte beizubehalten.

## Bewusst nicht erhobene Claims

- Production-Readiness, Production-Hardening, Runtime-Sicherheit oder
  Sicherheitsverifikation;
- CRS-Verifikation oder CRS-Vollständigkeit;
- vollständige Connector-Matrix-, HTTP/2- oder HTTP/3-Verifikation; oder
- Strict-Post-Commit-Enforcement über die ausgewählte Kern-Evidence hinaus.
