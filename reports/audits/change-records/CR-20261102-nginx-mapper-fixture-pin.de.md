# Change Record: CR-20261102-nginx-mapper-fixture-pin

**Sprache:** [English](CR-20261102-nginx-mapper-fixture-pin.md) | Deutsch

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | CR-20261102-nginx-mapper-fixture-pin |
| Datum (UTC) | 2026-11-02 |
| Basis-Revision | `97dfcaddb698d5b95c3f78531eb81803699ffbe1` |

## Motivation und Problemstellung

Bestehender Connector-Draft [#348](https://github.com/Easton97-Jens/ModSecurity-conector/pull/348)
pinnt Framework b852802. Der eigenständigen NGINX-Mapper-Status-Fixture fehlt der
echte Header-Authority-Helper, den der echte Mapper jetzt aufruft. Vorher:
C17/-Wall/-Wextra/-Werror meldet implizite Deklaration und inkompatibles
ngx_str_t-aus-int in setUpClass; keine Methode läuft.
Externer Framework-[#153](https://github.com/Easton97-Jens/ModSecurity-test-Framework/pull/153)
korrigiert nur Fixture-Abhängigkeiten und notwendige generierte Beschreibungen/EN-DE-Record.
Basis ist aktueller masterbc08ee7 unter Erhalt des unabhängig gemergten#151.
Dieser Parent-Change pinnt den lokal geprüften Remotecommit
`34dc7f9e7f9f9b1de42b5a19a491e804f7c7d747`, keinen alten Snapshot oder uncommittete Arbeit.

## Akzeptanzkriterien

Gleichen geprüften Remote-SHA in Gitlink, Lock und jeder registrierten Action-/
Workflow-Projektion pinnen. MRTS und unabhängige Versionen erhalten. Alle fünf
Mappermethoden mit vorhandenen Unterfällen und null Skips am finalen Commitpaar
erneut ausführen; relevante Projektions-/Provenienz-/Generator-/Doc-/Secret-/
angrenzende NGINX-Prüfungen. Nur normalen additiven Commit auf bestehendem#348
veröffentlichen. New-Head-CI/CodeQL/Sonar separat bewerten; kein altes Grün wiederverwenden.

## Implementierungsentscheidung und Begründung

Der aktuelle Abhängigkeitsvertrag in `docs/test-ownership-migration.md`
erlaubt einen veröffentlichten Framework-PR-SHA als vorläufigen Pin und verlangt
Framework-Integration vor späterer Connector-Integration. Hier kein Merge erlaubt.
Nativen Kandidatenprüfer und Komponentenversionssynchronisierer verwenden,
keine manuellen Hashänderungen. Nur exaktes committetes Framework-`ci/lib/common.sh`
per `git archive` in externes RUNNER_TEMP extrahieren; Shell-Daten nicht ausführen.
Alter gepinnter Kontext prüft vor, neuer gepinnter Kontext nach der Umstellung.
Keine Produktkorrektur oder Integration des Kontext-PR#436.

## Geänderte Dateien

Framework-Gitlink; `ci/tooling/project-versions.lock.json`;22registrierte Workflows
mit54Framework-Identitätsreferenzen; dieser EN/DE-Change-Record. Geänderte
Workflowbytes sind nur b852802→34dc7f9-Revisionsersetzungen.
MRTS bleibt `8a6bb546c4c81d8ffc7be801dceac60c6925685f`,
Python3.15.1 und Go1.27.3 im Lock unverändert. Produktcode, unabhängige
Abhängigkeitsversionen und vertrauenswürdige Brokerzuständigkeit ändern sich nicht.
Compiler-Guide-Generator ausgeführt; bestehende generierte Guides unverändert.

## Ausgeführte Befehle

Durchgehend RTK. Parent-Python ist `$PARENT_PYTHON`, vorhandenes Framework-Python
ist `$FRAMEWORK_PYTHON`, beide lokal3.14.4; kein Nachweis einer Ausführung mit
den unabhängig gepinnten Hosted-Python-Versionen.
Explizites TEST_ROOT/FRAMEWORK_ROOT wählt verschachteltes gepinntes Framework,
CONNECTOR_ROOT/CONNECTOR_REVISION diesen exakten Task-Checkout/HEAD, Profil
protocol-integrity; RUNNER_TEMP/Output/Temp/Cache liegen extern.
Run: `nginx-mapper-fixture-20261102`.

| Tatsächlicher Befehl / Verfahren | Exitcode | Beobachtetes Ergebnis |
| --- | --- | --- |
| `ci/tools/new-change-record.py create --name nginx-mapper-fixture-pin --base-revision 97dfcaddb698d5b95c3f78531eb81803699ffbe1 --date 2026-11-02` mit explizitem Framework-Importkontext | 0 | Native EN/DE-Scaffolds erstellt |
| `ci/tools/verify-framework-candidate-contract.py --repo-root "$CONNECTOR_ROOT" --candidate-sha 34dc7f9e7f9f9b1de42b5a19a491e804f7c7d747 --framework-common "$EXACT_COMMON" --candidate-framework-root "$CANDIDATE_FRAMEWORK" --expected-parent-framework-sha b85280278310f4034af78149ac13671438965c7b` | 0 | Vor Umstellung mit altem gepinntem Kontext verifiziert |
| `ci/tools/sync-framework-component-versions.py --sync --repo-root "$CONNECTOR_ROOT" --framework-common "$EXACT_COMMON" --framework-sha 34dc7f9e7f9f9b1de42b5a19a491e804f7c7d747` | 0 |23native Projektionspfade geändert |
| Gleicher Synchronisierer `--check` | 0 | changed=[] |
| Kandidatenprüfer mit neuem Kontext und `--expected-parent-framework-sha 34dc7f9e7f9f9b1de42b5a19a491e804f7c7d747` | 0 | Neues Paar verifiziert |
| Synchronisierer `--verify-primary --base 97dfcaddb698d5b95c3f78531eb81803699ffbe1` mit gleichem Repo/Common/SHA | 0 | FRAMEWORK_PRIMARY_VERIFIED |
| `scripts/generate_compiler_guides.py` | 0 | Kein Guide-Drift |
| Framework `-m unittest -v modsecurity_connector_tests.test_nginx_request_mapper_status` mit verschachteltem Fixpin | 0 |5PASS vor Parent-Commit |

Initiale Setupfehler bleiben sichtbar: Record-Erzeugung ohne expliziten
Framework-Import scheiterte1; Kandidatenkontext gegen alte Action-Pins scheiterte2;
Synchronisierer verwarf common.sh außerhalb des erlaubten RUNNER_TEMP-Roots mit2.
Alle scheiterten vor Produktprojektionsänderungen. Korrekte Imports/Kontexte und
nativer Archivinput lösten sie ohne Validierungsabschwächung. Externe exakte
Befehle und finale Paarreceipts bleiben im genehmigten Run; beobachtete Liefer-/
Current-Head-Fakten werden separat erfasst.

## Security-Auswirkung

Integritätswartung, keine Behebung einer validierten Produktlücke.
Externe Fixture übernimmt echte next_header-/Authority-Bodies mit korrekten
Signaturen, Abhängigkeitsreihenfolge, Hosttypen/Makros und beiden bedingten
HTTP/3-Kompilierungszweigen. Ihre fünf Methoden-/probe-ASTs,14Probes,10benannten
Unterfälle, Fehlerinjektionen, Headergrenzen und strengen Compilerflags bleiben.
Kein Quellstub, Collector-Ausnahme, Gate-/Schutzabschwächung oder MRTS-Schreibzugriff.

## Runtime-Evidence

Keine neue. Eigenständige C17-Fixture-/Vertragsprüfungen belegen nur ihre Ebene,
keine Hosted-NGINX-/TLS-/H2-/H3-Qualifikation. Keine vollständige Kampagne im Auftrag.

## Bekannte Einschränkungen

Framework153 bleibt Draft/ungemergt. Vor späterem Connector348-Merge integrieren,
nicht automatisch in diesem Auftrag. Finales eingechecktes Parent-Paar und
New-Head-Hosted-Prüfungen bleiben getrennte Lieferschritte.
Verschachteltes MRTS ist lokal uninitialisiert; strenge unabhängige MRTS-HEAD-
Provenienz hier nicht als bestanden melden. Grenze erhalten, gegebenenfalls
echte frische Hosted-Evidenz verwenden, ohne MRTS lokal zu ändern.

## Verbleibende Risiken

Spätere Masterintegration ändert Commitidentität und braucht eigenen verifizierten
Pin-Follow-up. Verbindliche New-Head-CI/CodeQL/Sonar-Findings können fokussierte
Folgecommits erfordern; keine Vorabfreigabe oder Unterdrückung.

## Nicht ausgeführte Prüfungen mit Begründung

Keine breite Standard-/historische Suite, MRTS-Ausführung, installierte Hostkampagne
oder H2-/H3-Vollqualifikation. Finale Commitpaar-/New-Head-Hosted-Gates stehen an
diesem Vorbereitungspunkt aus; frühere Heads ersetzen sie nicht.

## Finaler Diff- und Review-Status

Nur task-eigene Projektions-/Record-Vorbereitung. Abschließendes Staged-Whitespace-,
unabhängiges Diff-/EN-DE-Review, Secret-Scan, finales Paar und normaler additiver
Push sind vor dem Lieferendpunkt erforderlich.
Keine Zugangsdaten, privaten Payloads, geerbten Umgebungsdumps oder unbeschränkten
Logs enthalten. Hauptcheckout/fremde Arbeit und separater KontextPR436 unverändert.

### Lokale Vorbereitungsverifikation

Natives `new-change-record.py check`, `make check-project-versions check-bilingual-docs check-doc-links`,
Staged-`--verify-primary`, öffentliche Inventar-Admission und natives Archiv-`--check`
bestanden (jeExit0). Admission bleibt100aktiv/Limit100 und2586On-Demand,
Inventar-SHA-256 `fc007bdea733980700a74609acb41e5332977516b19f2f6e2823ecb5860557fd`.
Die erste Archivstrukturprüfung verwarf das neue deutsche Sprachumschaltformat;
Wiederherstellung des exakten nativen Formats korrigierte nur diesen Record.
Redigierter Staged-Diff-Gitleaks bestanden (40444Bytes,keine Funde), Whitespace
bestanden. Unabhängiges Staged-Diff-/EN-DE-Review bestätigt nur22Workflow-/
54Identitätsersetzungen, nur framework_sha im Lock, exakten Remotegitlink und
Records. Finale Commitpaarreceipts und frische Hosted-Analyse bleiben erforderlich.

### Separat autorisierte finale Integration

Vorstehende Abschnitte beschreiben den ursprünglichen vorläufigen Pin-Stand.
Der aktuelle Benutzer autorisiert separat reguläre Framework153-/Parent348-
Integration in dieser Reihenfolge mit exakter Head-Bindung, nur nach allen
Pflichtprüfungen. Framework153 wurde tatsächlich am `2026-11-02T06:11:26Z` per
Squash in `f11d4617ff98ad615c72c1b6672fc386394db41e` integriert; sein Baum entspricht
exakt geprüftem64e53d3. Finale PR-Head-Methoden beideV3 (14 beobachtete Probes/zehn
benannte Unterfälle je Modus, keine Skips), elf angrenzende Methoden, native
Prüfungen, neun Workflows, CodeQL und fünf Sonar-Bedingungen bestanden;
PR-Issues/Hotspots0. Masterprüfungen bleiben separat.

Parent-mastere6b36f7 normal in3d1ab620 übernommen; nur fünf unabhängige
Policy-/Record-Dateien geerbt. Produktänderungen erhalten; KontextPR436 ausgeschlossen.
Exakte eingecheckte Framework-Common-Daten per git archive unter RUNNER_TEMP
speisen nativen Verifier/Synchronizer. Pre-Kandidat34dc7f9->f11d461 bestand;
nativer Sync aktualisierte23Projektionsdateien: nur framework_sha und54Referenzen
in22Workflows. Gitlink wählt denselben tatsächlichen Framework-Merge.
MRTS8a6bb546, Python3.15.1 undGo1.27.3 unverändert. Historische Pin-Aussage im
MRTS-Guide datiert; aktuelle Autorität bleiben Gitlink/Lock. Keine manuelle Digestkorrektur.

Frische finale Commitpaar-Methoden/-Verträge/-Generatoren/-Docs/-Secrets/-Pins,
strenge frische Hosted-Provenienz, alle ParentCI-/CodeQL-/Sonar-Scopes/-Issues/
-Hotspots, Review-/Regel-/Basisprüfungen und Post-Merge-Master-/Baumevidenz bleiben
verpflichtend. Lokal uninitialisiertes MRTS ist fehlende Voraussetzung, kein
lokales ProvenienzPASS oder Initialisierungserlaubnis. Historisches Traefik-
Feedback einzeln quellengeprüft: erhaltener Terminalfehler verhindert ReaderFrom-
Bypass; nativeMSE1/op7 nutzen monotonen C-Peer, nicht compositeMSC2/op5.
Frische verwandte vorhandene Prüfungen und konkrete Antworten gehen Auflösung
voraus. Exakte finale Receipts bleiben extern unter
`nginx-mapper-integration-20261102` und in geschützten PR-Metadaten erhalten.
Kein altes Grün, neue Protokollkampagne, Risikoakzeptanz, abgeschwächter Check,
Bypass, direkter Master-Push, Force-Push, MRTS-Edit oder Vollqualifikation.
