# Versionierte Konfiguration

**Sprache:** [English](README.md) | Deutsch

## Zweck und Grenze

\`config/\` enthält kleine, versionierte maschinenlesbare Inputs für
Repository-Checks, Harnesses und Report-Generatoren. Es ist für deklarative
Test- und Contract-Konfiguration bestimmt, nicht für umgebungsspezifische
Host-Konfiguration oder Runtime-Ausgabe.

Vorhandensein oder JSON-Validität einer Konfiguration ist keine Runtime-Evidence.
Insbesondere macht dieses Verzeichnis keinen Production-, CRS-Vollständigkeits-,
HTTP/2-, HTTP/3-, Full-Matrix- oder Strict-für-alle-Connectoren-Claim.

## Struktur und Source of Truth

| Pfad | Zweck | Source of Truth / Consumer |
| --- | --- | --- |
| \`testing/capability-contract.json\` | Connector-neutraler Capability-Contract für Contract-/Evidence-Checks | Das eingecheckte JSON ist Source of Truth für diesen Contract; sein Wert \`runtime_claim\` ist bewusst keine Runtime-Promotion. |
| \`testing/import-status.json\` | Klassifikation importierten, gemappten, blockierten und connector-spezifischen Testmaterials | Das eingecheckte JSON wird von Apache-, NGINX- und HAProxy-Harness-/Report-Pfaden konsumiert. Es muss den geprüften Repository-Status statt eines optimistischen Runtime-Ergebnisses abbilden. |

Der Consumer-Code und das Root-[Makefile](../Makefile) definieren Validation
und Target-Verhalten. Generierte Reports sind abgeleitete Artefakte, kein Ersatz
für diese Source-Dateien.

## Konfiguration hinzufügen oder ändern

Einen neuen versionierten Input in einem benannten Domain-Verzeichnis wie
\`config/testing/\` ablegen und im selben Change einen Validator oder bestehenden
Consumer ergänzen. Explizite JSON-Werte und stabile Schema-Keys verwenden.
Source-Contract, Tests und jeden Generator aktualisieren, der daraus
Dokumentation oder Reports ableitet.

Keine rechner-spezifische Host-Konfiguration, generiertes JSON, Build-/Cache-
Pfade, Runtime-Logs, Result-Dateien, Source-Downloads, Passwörter, Tokens,
private Schlüssel, Zertifikate, Cookies oder Authorization-Header unter
\`config/\` ablegen. Keine nicht implementierte Einstellung hinzufügen, nur weil
ein anderer Connector eine ähnlich benannte Capability ausweist.

## Variablen und Platzhalter

Das versionierte JSON in diesem Verzeichnis ist absichtlich literal: Es
expandiert weder Shell-Variablen noch Dokumentationsplatzhalter. Die es
konsumierenden Kommandos können die folgenden Root-Inputs erhalten. Vollständige
Definitionen stehen in der [Variablen- und Platzhalterreferenz](../docs/reference/variables.de.md).

| Name | Lokale Bedeutung | Pflicht, Format und Beispiel |
| --- | --- | --- |
| \`NO_CRS_RULES_FILE\` | Rule-Datei, die No-CRS-Lifecycle-Kommandos auswählen, welche auch konfigurationsabgeleitete Contracts konsumieren | Für Konfigurationsvalidierung optional; Root-Default ist die Framework-Baseline. Ein Override muss eine vorhandene absolute Rule-Datei sein, etwa \`/srv/modsecurity-work/rules/no-crs-baseline.conf\`. Kein JSON-Feld. |
| \`NO_CRS_CONNECTORS\` | Begrenzte Connector-Auswahl für Aggregate-Targets | Optional; Repository-Default ist \`apache nginx haproxy envoy traefik lighttpd\`. Nur diese leerzeichengetrennten Namen nutzen, soweit ein Target keinen anderen Scope dokumentiert. |
| \`NO_CRS_RUN_ID\` | Aggregate-Evidence-Namespace für Lifecycle-/Report-Kommandos | Für einen aggregierten Evidence-Lauf erforderlich, kein Default, dateisystemsicheres Token wie \`six-core-20260712T120000Z\`. Darf weder Secrets noch personenbezogene Information enthalten. |
| \`<repository-root>\` | Reiner Dokumentationsplatzhalter für den Checkout mit \`config/\` | Nur wenn ein Kommando ihn verlangt durch einen realen absoluten Root wie \`/srv/src/ModSecurity-conector\` ersetzen; Winkelklammern sind keine ausführbare Eingabe. |
| \`<external-source-root>\` | Reiner Dokumentationsplatzhalter für einen vertrauenswürdigen Checkout außerhalb dieses Repositorys | \`/srv/src/ModSecurity-test-Framework\` ist ein Beispiel. Kein Output-/Cache-Pfad und keine Evidence, dass externe Inputs verifiziert sind. |

Niemals \`REPLACE_ME\`, \`CHANGE_ME\`, \`$VAR\` oder einen anderen informellen Token
in JSON einsetzen. Es gibt keine Interpolationsphase; stattdessen einen
dokumentierten konkreten Schema-Wert verwenden oder einen geprüften
Consumer-Contract ergänzen.

## Relevante Targets

| Target | Zweck und Ergebnisgrenze |
| --- | --- |
| \`make check-common-sdk-contract\` | Prüft, dass der Capability-Contract vorhanden und mit SDK-/Common-Erwartungen strukturell konsistent ist. |
| \`make lint\` | Validiert \`config/testing/import-status.json\` als JSON und führt breitere Contract-Consumer aus. Ein erfolgreicher Lint beweist keinen Host-Lauf. |
| \`make report-governance\` | Prüft Governance generierter Reports und Source-/Derived-Grenzen. Aktualisiert keine Runtime-Evidence. |
| \`make refresh-all-reports\` | Regeneriert Report-Artefakte aus ihren dokumentierten Quellen; Änderungen prüfen, statt generierte Ausgabe manuell zu editieren. |
| \`make full-lifecycle-all-connectors\` | Nutzt Lifecycle-Inputs und schreibt laufbezogene Evidence; für einen aggregierten Kandidaten eine sichere \`NO_CRS_RUN_ID\` angeben. |

Vor Änderung eines Status- oder Capability-Begriffs [Testing](../docs/testing-and-evidence.de.md),
[Evidence](../docs/testing-and-evidence.de.md) und das
[Glossar](../docs/reference/glossary.de.md) lesen.
