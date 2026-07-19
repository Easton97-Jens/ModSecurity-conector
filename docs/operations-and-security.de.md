# Betrieb und Sicherheit

**Sprache:** [English](operations-and-security.md) | Deutsch

## Geltungsbereich

Dieser Guide fasst repositoryweite Betriebs- und Sicherheitsgrenzen zusammen.
Er ist keine Produktions-Deployment-Anleitung und behauptet nicht, dass ein
Connector produktionsreif, laufzeitsicher, sicherheitsverifiziert,
CRS-verifiziert oder für jedes Protokoll beziehungsweise jeden Testcase
vollständig ist.

## Deployment-Grenze

Ein ausgewählter Connector wird nur mit seinem dokumentierten Host-Build,
seiner Konfiguration, seinen Regeln und Runtime-Voraussetzungen betrieben.
Build-, Cache-, Runtime-, Log- und Evidence-Verzeichnisse müssen außerhalb des
Checkouts beschreibbar sein. Das Repository schreibt keinen
entwicklerspezifischen absoluten Pfad vor.

| Bereich | Erforderliche Praxis | Grenze |
| --- | --- | --- |
| Build/Cache | Dokumentierte extern beschreibbare Roots und festgelegte/ausgewählte Inputs verwenden | Ein erfolgreicher Build ist kein Hostverkehrsnachweis |
| Runtime | Nur den ausgewählten Host/das Profil mit expliziten Inputs starten | Eine Startprüfung ist kein Request-/Response-Test |
| Evidence | Nicht geheime Run-ID und begrenzten Evidence-Root verwenden | Ein Lauf verallgemeinert nicht auf ein anderes Profil |
| Konfiguration | Nur geprüfte Host-, Runtime- und Regelinputs laden | Eine Konfigurationsprüfung ist kein Lifecycle-Ergebnis |

## Logs, Artefakte und Datenschutz

Logs und Artefakte sollen die minimal nötigen Metadaten enthalten, um eine
ausgewählte Beobachtung zu erklären. Result- und Eventdatensätze bleiben
payload-sicher. Zugangsdaten, Session-Material, Cookies, Authorization-Header,
private Schlüssel, Zertifikate, Request-Bodies, Response-Bodies oder
host-private Pfade gehören nicht in eingecheckte Dokumentation oder Artefakte.

Logausgabe wird in der Betriebsumgebung rotiert oder begrenzt. Behalten werden
die Run-ID, das ausgewählte Profil, die effektive nicht geheime Konfiguration,
die Connector-Identität und die Artefaktprovenienz, die der passende Validator
erfordert.

## Limits, Timeouts und Buffering

| Kontrolle | Betriebszweck | Sicherheitsgrenze |
| --- | --- | --- |
| Header- und Body-Limits | Ressourcenverbrauch vor der Verarbeitung begrenzen | Ein höheres Limit ist kein Nachweis für sicheres Buffering |
| Request-/Response-Timeouts | Host- oder Bridge-Wartezeit begrenzen | Eine Timeout-Einstellung beweist keine Cancellation-Semantik |
| Response-Body-Scope | Engine-Inspektion und Bytes beschränken | Keinen connector-eigenen vollständigen Response-Puffer einführen, außer ein dokumentiertes Host-Sicherheitsgate erfordert ihn; Apache hält normalisierte Ausgabe unter einem endlichen fail-closed Limit bis EOS zurück |
| Event-/Log-Limits | Diagnostik begrenzt und payload-sicher halten | Trunkierung muss wahrheitsgemäß dargestellt werden |

Exakte Parser-Defaults und Hostkontexte stehen in den vollständigen
Connector-Konfigurationsreferenzen, nicht in diesem Betriebsüberblick.

## Updates, Origin und Dependency-Behandlung

Quellattribution, Lizenzen, Origin-Metadaten, festgelegte Komponenteninputs und
Adaptermetadaten bleiben mit den eingecheckten Quellen konsistent. Eine
Komponente wird nur über ihren dokumentierten Source-/Buildprozess aktualisiert;
danach laufen die passenden Konfigurations-, Vertrags- und Evidence-Prüfungen.
Eine geänderte Source-Revision befördert kein historisches Ergebnis.

Repository und Framework unterscheiden eine fehlende optionale Voraussetzung
von einem stillen Fallback. Globale Komponenten werden nicht installiert,
beliebige System-Binaries nicht als Ersatz verwendet und Runtime-Abhängigkeiten
nicht heruntergeladen, sofern der aufgerufene dokumentierte Workflow dies nicht
ausdrücklich erlaubt und aufzeichnet.

Connector-lokale <code>ORIGIN.md</code>, Source-Maps, Lizenzmaterial und
Adaptermetadaten bleiben die detaillierten Provenienzdatensätze. Hier bleibt
genug repositoryweiter Kontext erhalten, um zu erklären, dass ein
importierter/Upstream-Pfad kein Implementierungs- oder Laufzeitclaim ist.

| Komponente | Source-URL | Beobachteter Commit | Beobachtete Version | Lizenz |
| --- | --- | --- | --- | --- |
| ModSecurity-apache | https://github.com/owasp-modsecurity/ModSecurity-apache | <code>0488c77f69669584324b70460614a382224b4883</code> | <code>v0.0.9-beta1-26-g0488c77</code> | Apache-2.0 |
| ModSecurity-nginx | https://github.com/owasp-modsecurity/ModSecurity-nginx | <code>9eb44fd9ab0988756e1ab8ce5aa5548ddbe57846</code> | <code>v1.0.4-14-g9eb44fd</code> | Apache-2.0 |

Apache-Attribution bleibt unter <code>licenses/apache/</code> und
<code>connectors/apache/ORIGIN.md</code>; produktive Apache-Quellen und
Autotools/APXS-Inputs sind adapter-eigen. NGINX-Attribution bleibt unter
<code>licenses/nginx/</code> und <code>connectors/nginx/ORIGIN.md</code>;
produktive Modulquellen und Konfiguration sind adapter-eigen. Die aufgezeichnete
NGINX-Phase-4-Source-Änderung aus
https://github.com/owasp-modsecurity/ModSecurity-nginx/pull/377 bei
<code>3d72b004ff27a78ea19c6b945870e2cae62a97ac</code> befördert
<code>RESPONSE_BODY</code> nicht.

| Engine-Referenz | Source-URL | Beobachteter Commit | Beobachtete Version | Lizenz |
| --- | --- | --- | --- | --- |
| ModSecurity v2 | https://github.com/owasp-modsecurity/ModSecurity | <code>02eed22d74667b32091eece088a8ebdf64b6ba67</code> | <code>v2.9.13</code> | Apache-2.0 |
| ModSecurity v3 | https://github.com/owasp-modsecurity/ModSecurity | <code>0fb4aff98b4980cf6426697d5605c424e3d5bb60</code> | <code>v3.0.15</code> | Apache-2.0 |

Upstream-Git-Verzeichnisse oder generierte Build-Artefakte werden nicht
importiert. Origin-Maps und Lizenzkopien werden bei Änderungen importierter
Dateien aktualisiert. Jede künftige Source-Reduktion erfordert erhaltene
Attribution und passende isolierte Build-/Smoke-Evidence; die Git-Historie
bewahrt die entfernte Planungschronologie.

## Fehlerbehebung

| Symptom | Erste Prüfung | Nicht folgern |
| --- | --- | --- |
| Build- oder Konfigurationsfehler | Ausgewählter Compiler-/Build-Guide und Host-Config-Check-Ausgabe | Einen Source-Fehler ohne die gemeldete Stufe zu prüfen |
| Fehlende Runtime-Komponente | Deklarierte Komponenten-/Root-Variable und Blocked-Prerequisite-Ausgabe | Dass eine nicht zusammenhängende System-Binary gleichwertig ist |
| Unerwartetes P4-Ergebnis | Connector-Guide, Phase-Event, Commit-/EOS-Metadaten und ausgewähltes Profil | Eine Strict-Client-Aktion allein aus einem Regelmatch |
| Report-/Statusabweichung | Run-ID, effektive Konfiguration, normalisierte Records und Validator-Ausgabe | Dass eine generierte Zusammenfassung roher Laufzeitbeweis ist |

## Hardening-Backlog und Nicht-Claims

Transport-Hardening, Cancellation-Verhalten, Strict Late Intervention,
Performance, Protokollabdeckung, CRS-Vergleich, Restart-Verhalten und
erweiterte Katalogabdeckung bleiben getrennt evidence-gesteuert. Sie werden als
begrenzte Arbeitspunkte in aktuellen Reports oder Connector-Guides geführt,
statt historische Status-Snapshots in diesem Dokument zu bewahren.

## Verwandte Referenzen

- [Architektur](architecture.de.md)
- [Konfiguration](configuration.de.md)
- [Tests und Nachweise](testing-and-evidence.de.md)
- [Build-Dokumentation](build/README.de.md)
- [CI-Sicherheitswerkzeuge](security/ci-security-tooling.de.md)
- Connector-lokale <code>ORIGIN.md</code> und Source-Maps
