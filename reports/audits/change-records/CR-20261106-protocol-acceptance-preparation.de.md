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
und Cleanup bleiben sichtbar. Hostprüfung des dokumentierten 5093/fa-Paars und beide Draft-PRs sind vorhanden;
Vorbereitung insgesamt NOT_READY.

## Implementierungsentscheidung und Begründung

Framework `d0c8bdf508f5c335736bcd442274d8db62a818c4` auswählen; MRTS
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
| `rtk bypass "$PYTHON" ci/tools/sync-framework-component-versions.py --sync --repo-root "$P" --framework-common "$COMMON" --framework-sha d0c8bdf508f5c335736bcd442274d8db62a818c4 --mrts-sha ee2174431c4edf97e66afe32558ce8454deb2397` | PASS; native feste Projektionen synchronisiert |
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

Finale Hostnachweise am dokumentierten Paar 5093/fa: alle 25 neuen IDs
real ausgewertet (21 PASS / 4 FAIL), acht angrenzende Hostfälle PASS; 33/33 Cleanup
bestätigt. Vollständige SHAs stehen im abschließenden Reviewabschnitt. Die vier
Fehler sind `h2_phase4_strict`, `h2_server_rst_stream`, `h2_upstream_reset`,
`phase4_strict_http2_stream_reset`. Die 15 neuen Vertragsunitmethoden plus 29
angrenzenden Unitregressionen bestanden; 21 Manipulationen echter Beobachtungskopien
wurden abgelehnt. Kein Nachweis einer umfassenden Abnahme oder eines späteren
Folgecommitpaars. Gesamtabnahme NOT_RUN; Vorbereitung NOT_READY.

## Bekannte Einschränkungen

Vier verpflichtende H2-Reseterwartungen scheitern bei erhaltenem
Peerisolationsvertrag. Keine Produktkorrektur enthalten. Erforderliche moderne
ausführbare Pfade für Apache H2, HAProxy HTX H2/SPOE-Begleiter-H2-Streamshutdown
und Envoy ext_proc H2 bleiben offen. Ausgewählte lighttpd-stock-/gepatchte Profile
bleiben gemäß bestehendem Vertrag auf H1 begrenzt; kein neuer Unsupportedmarker.

## Verbleibende Risiken

H2-Resetverhalten und verbleibende Profilrunnerpflichten verhindern
READY_FOR_FULL_ACCEPTANCE. Das Legacyinventar meldet weiterhin 84 Altvertragsbefunde.
Ein späteres Folgepaar benötigt eigene Verifikation; die dokumentierten
5093/fa-Nachweise qualifizieren kein neueres Paar.

## Nicht ausgeführte Prüfungen mit Begründung

Gesamtabnahme bleibt ausdrücklich NOT_RUN. Lokale Sonarinstallation, Start,
Authentifizierung und Scans bleiben ausgesetzt. Kein Produktfix und kein Merge.
GitHubprüfungen laufen beziehungsweise werden untersucht; die generierte
Archivkorrektur benötigt Folge-CI am exakten Head und Hostprüfung des späteren
Paars. Der native Compilerleitfadengenerator bestand mit unveränderten Ausgabebytes.

## Finaler Diff- und Review-Status

Der ausdrücklich freigegebene Framework-[PR #169](https://github.com/Easton97-Jens/ModSecurity-test-Framework/pull/169)
und Parent-[PR #445](https://github.com/Easton97-Jens/ModSecurity-conector/pull/445)
existieren. Neue Benutzerfreigabe ersetzte die frühere Pushablehnung; beide
ursprünglichen Commits wurden gepusht. GitHub-CI wird weiter ausgewertet;
finale Ergebnisse am exakten Head bleiben extern dokumentiert. Kein Merge.

Alle 33 gezielten Hostwiederholungen wurden an Parent
`5093a7aa349372279fb2c76974da6423de511332` / Framework
`fa444236fa3b00c91ba94de49f69f52101087087` / MRTS
`ee2174431c4edf97e66afe32558ce8454deb2397` abgeschlossen: neue Fälle
21 PASS / 4 FAIL, angrenzende Fälle 8 PASS; alle 33 Cleanups bestätigt. Diese
Ergebnisse qualifizieren genau dieses Paar und seine zugelassenen Artefakte.
Vier H2-Pflichten und weitere moderne Profilpfade bleiben offen; NOT_READY und
Gesamtabnahme NOT_RUN bleiben unverändert.

Parent-CI deckte eine ausgelassene generierte Testarchivprojektion auf: Natives
`update-test-archive --check` scheiterte in Lint-, Quick-, NGINX- und Commonprüfungen.
Der native Frameworkgenerator ergänzt ausschließlich die neue Testquelldatei
mit 15 Methoden im Archiv; der Bestand steigt von 8096 auf 8111. Diese Folgeänderung
betrifft Archivprojektion und Dokumentation ohne Runtimecode- oder
Erwartungsänderung. Die Verifikation eines späteren Commitpaars bleibt separat;
sie wird nicht aus den 5093/fa-Hostläufen abgeleitet. Exakte Folge-SHAs und
CI-Belege bleiben extern erhalten.

Die Framework-PR-CI lehnte danach den neu versionierten C-Client vor dem
Scannerstart ab: Seine Quelle fehlte im geschlossenen nativen Compileinventar.
Ausschließlich `tests/runners/protocol_acceptance_client.c` in die geprüften
Rezepte aufnehmen und die exakte Offlineinventarassertion von 81 auf 82 Einheiten
anpassen. Vollständige Mengengleichheit, Warnflags, Zugangsdatenabgrenzung und
alle Analysegates bleiben erhalten. Generiertes Spezialtestarchiv wegen der
geänderten Offlinetestquelle aktualisieren. Kein lokaler Scanner, keine
Sonarinstallation oder Authentifizierung. Finale Folge-SHAs, gezielte
Hostwiederholungen und aktuelle Head-CI-Ergebnisse bleiben extern dokumentiert.
