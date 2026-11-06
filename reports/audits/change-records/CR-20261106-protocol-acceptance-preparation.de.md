# Change Record: CR-20261106-protocol-acceptance-preparation

**Sprache:** [English](CR-20261106-protocol-acceptance-preparation.md) | Deutsch

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | CR-20261106-protocol-acceptance-preparation |
| Datum (UTC) | 2026-11-06 |
| Basis-Revision | `a5f697c35acb5386d2037f91dfed10ad4b469cd9` |

## Motivation und Problemstellung

Die separat implementierten Framework-Vorbereitungstests über konsistenten
Parent-Gitlink, zentralen Versionslock und native Workflowprojektionen auswählen.
Die lokale Policyinventarabweichung ohne Veröffentlichung privater Anweisungen
oder breitere Vererbung klären. Keine Connector-Codekorrektur.

## Akzeptanzkriterien

Der geprüfte Frameworkkandidat muss konsistent ausgewählt werden; MRTS-Revision
und fremde Toolchainpins bleiben erhalten. Native Primary-Publikationsprüfungen
müssen mit der vertrauten Parentbasis übereinstimmen. Policyinventar und geerbte
Digests getrennt ausweisen. Gezielte Hostergebnisse, fehlgeschlagene Pflichten
und Cleanup bleiben sichtbar. Hostprüfung des exakten finalen Commitpaars und
prüfbare Remoteauslieferung stehen aus; Vorbereitung insgesamt NOT_READY.

## Implementierungsentscheidung und Begründung

Framework `fa444236fa3b00c91ba94de49f69f52101087087` auswählen; MRTS
`ee2174431c4edf97e66afe32558ce8454deb2397` erhalten. Native feste Projektionsregistry
mit extrahiertem Kandidaten-`common.sh` und offiziellen Gitobjektdaten verwenden.
Der geschützte Broker-Provenancepin bleibt unverändert; gewöhnliche Framework-
Referenzen seines Workflows ändern sich nur gemäß nativem Projektionsvertrag.
Python 3.15.2, Go 1.27.3 und sämtliche MRTS-Werte bleiben unverändert.

Die ignorierte lokale LLM-Notiz mit 194 Bytes dupliziert bestehende Agentprofile
und ist keine gemeinsame normative Policy. Nach Prüfung lösen byteidentisches
Archiv und lokale Klassifikation ihre Inventarbehandlung. Die vorgeschlagene
versionierte Referenz wurde abgelehnt, da die private Datei in sauberen Klonen
fehlen würde. Die 27 Parentkatalog-, 21 Framework- und 12 MRTS-Vererbungsdigests
bleiben unverändert; keine pauschale Kindvererbung oder Prüfsummenersetzung.

## Geänderte Dateien

- `modules/ModSecurity-test-Framework`: ausgewählter Framework-Gitlink.
- `ci/tooling/project-versions.lock.json`: nur `framework_sha` ändert sich.
- 22 native Workflowprojektionen unter `.github/workflows/`.
- Dieses englisch/deutsche Change-Record-Paar.

Generierte Compilerdokumentation wird bei Bedarf über ihren nativen Generator
aktualisiert; keine manuelle Änderung von Generatorausgaben durch diesen Record.
Lokale Policyklassifikation/Archivierung bleibt lokaler Nachweis, keine
versionierte Policy.

## Ausgeführte Befehle

`P` bezeichnet den eigenen Parentworktree, `F` dessen ausgewähltes verschachteltes
Framework, `PYTHON` den gewählten eigenen Python-3.15.2-Interpreter. Die Parent-
Validierungsumgebung wurde ohne pip oder Paketinstallation erstellt. `COMMON` bezeichnet die geprüfte extrahierte Kandidatenquelle; offizielle
Objektdaten stammen standardmäßig aus dem ausgewählten verschachtelten Framework. Absolute Pfade und vollständige Aufrufbelege bleiben extern.

| RTK-Befehl oder Verfahren | Ergebnis |
| --- | --- |
| `rtk bypass "$PYTHON" ci/tools/sync-framework-component-versions.py --sync --repo-root "$P" --framework-common "$COMMON" --framework-sha fa444236fa3b00c91ba94de49f69f52101087087 --mrts-sha ee2174431c4edf97e66afe32558ce8454deb2397` | PASS; native feste Projektionen synchronisiert |
| Derselbe native Aufruf mit `--check` statt `--sync` | PASS; keine Projektionsabweichung |
| Dieselben nativen Eingaben mit `--verify-primary --base a5f697c35acb5386d2037f91dfed10ad4b469cd9` | PASS; Publikationsrekonstruktion aus vertrauter Basis |
| `rtk bypass "$POLICY_PYTHON" .codex/bin/validate-codex-inheritance.py --check --all` | PASS; aktuelles natives Inventar/Vererbung |
| `rtk bypass "$POLICY_PYTHON" .codex/bin/validate-v32-structure.py` | PASS; V3.2-Struktur |
| Separates Legacy-Auditinventarverfahren | FAIL; 84 Altvertragsbefunde als Rohnachweise erhalten |

`POLICY_PYTHON` bezeichnet den früheren Parent-eigenen Python-3.14.4-Interpreter;
eine finale Wiederholung mit eigenem 3.15.2-Interpreter ist ein separater Nachweis.

Die Dokumentationsprüfung nutzte den bestehenden Framework-eigenen Python-3.15.2-
Interpreter (`FW_PYTHON`) ohne Installation:

| RTK-Befehl oder Verfahren | Ergebnis |
| --- | --- |
| `rtk bypass "$FW_PYTHON" ci/tools/new-change-record.py check` mit explizitem absolutem `TEST_ROOT`, `CONNECTOR_ROOT` und Framework-`PYTHONPATH` | Exit 0; struktureller Change-Record-Vertrag |
| `rtk make check-bilingual-docs check-doc-links FRAMEWORK_ROOT="$F" PYTHON="$FW_PYTHON" FRAMEWORK_PYTHON="$FW_PYTHON"` | Exit 0; Sprachparität, Repositorypfade und Links bestanden |
| `rtk bypass git diff --check` | Exit 0; Whitespace bestanden |

Initiale Recordprüfungen ohne beziehungsweise mit relativem Quellkontext scheiterten;
expliziter absoluter Quellkontext behob diese Aufruffehler.

Aktuelle native Konsistenz und Legacyinventarergebnis sind getrennte Tatsachen;
Letzteres wurde weder unterdrückt noch als Erfolg umgedeutet.

## Security-Auswirkung

Kein Produkt-Security-Fix, keine globale Rechte-/Konfigurationsänderung,
Authentifizierungsänderung, MRTS-Schreibaktion oder Änderung geschützter
Brokerauthorisierung. Keine Prüfpflicht wird abgeschwächt. Lokales Sonar bleibt
ausgesetzt; bestehende GitHub-Sonar-/CodeQL-Pflichten bleiben erhalten. Keine
Zugangsdaten oder sensiblen Rohdaten werden in den Record kopiert.

## Runtime-Evidence

Gezielte Framework-Hostnachweise werteten alle 25 neuen IDs aus: 21 PASS /
4 FAIL; Cleanup 25/25 bestätigt. Fehler: `h2_phase4_strict`, `h2_server_rst_stream`,
`h2_upstream_reset`, `phase4_strict_http2_stream_reset`. Acht angrenzende bestehende
H2-/H3-Aushandlungs-/P2-/P3-/P4-Hostfälle bestanden. Die 15 neuen Vertragsunitmethoden,
29 angrenzenden Unitregressionen und 21 negativen Manipulationen echter
Beobachtungen erfüllten ihre Erwartungen; jede Manipulation wurde abgelehnt.

Diese Beobachtungen binden die dokumentierten Quellbytes und Artefakte; die
Hostprüfung des exakten finalen Parent-/Framework-Commitpaars folgt noch. Sie
belegen weder dieses finale Paar noch alle logischen Profile oder Gesamtabnahme.
Gesamtabnahme NOT_RUN; Vorbereitung NOT_READY.

## Bekannte Einschränkungen

Vier verpflichtende H2-Reseterwartungen scheitern bei erhaltenem
Peerisolationsvertrag. Keine Produktkorrektur enthalten. Erforderliche moderne
ausführbare Pfade für Apache H2, HAProxy HTX H2/SPOE-Begleiter-H2-Streamshutdown
und Envoy ext_proc H2 bleiben offen. Ausgewählte lighttpd-stock-/gepatchte Profile
bleiben gemäß bestehendem Vertrag auf H1 begrenzt; kein neuer Unsupportedmarker.

## Verbleibende Risiken

H2-Resetverhalten und verbleibende Profilrunnerpflichten verhindern
READY_FOR_FULL_ACCEPTANCE. Das Legacyinventar meldet weiterhin 84 Altvertragsbefunde.
Vor Runtimeaussagen über das finale Commitpaar muss dieses exakt geprüft werden.
Frühere quellabgeglichene Nachweise ersetzen diese Prüfung nicht.

## Nicht ausgeführte Prüfungen mit Begründung

Gesamtabnahme ausdrücklich NOT_RUN. Lokale Sonarinstallation/-start/-authentifizierung
und Scans sind vom Benutzer ausgesetzt. Hostwiederholungen des exakten finalen Commitpaars wurden bei Recordaktualisierung
noch nicht beobachtet. Native Compilerleitfadengenerierung endete mit Exit 0
und unveränderten Ausgabebytes im korrekten Quellkontext. Keine Remote-PR-/CI-Prüfungen: Die automatische
Freigabeprüfung lehnte den Framework-Push zweimal ab; diese Egressaktion benötigt
neue Benutzerfreigabe. Kein Merge und keine administrative Regeländerung
autorisiert oder durchgeführt.

## Finaler Diff- und Review-Status

Dies ist der konkrete lokale Reviewrecord für den Parentkandidaten. Exakte lokale
Commit-SHAs, Remotebranchidentitäten und Auslieferungsbelege bleiben in externen
repositorybezogenen Nachweisen. Kein erfundener PR-Link oder erfolgreicher Push-/
CI-Status wird behauptet. Auslieferung bleibt am abgelehnten Framework-Push
blockiert; Ablehnung und erforderliche neue Benutzerfreigabe müssen vor Egress
genannt werden. Die lokale Parentvorbereitung bleibt bis zur Freigabe prüfbar.
