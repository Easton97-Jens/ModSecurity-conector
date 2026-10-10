# Change Record: CR-20261010-r17-strict-client-full97

**Sprache:** [English](CR-20261010-r17-strict-client-full97.md) | Deutsch

Dokumentationsabschluss für den tatsächlichen lokalen R17-Nachweis; kein Produktfix oder Protected-PASS.

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | CR-20261010-r17-strict-client-full97 |
| Datum (UTC) | 2026-10-10 |
| Basis-Revision | `2f02370b07149265841411894f1a2cf7f1e978ff` |

## Motivation und Problemstellung

R16 hatte bereits Canonical PASS und97 Required-PASS, aber der präzise numerische Abschluss des generischen Strict-Clients war nicht persistiert. R17 schließt diese Messlücke durch externe direkte Child-Instrumentierung und genau einen neuen Standard-Full97. Diese versionierte Änderung dokumentiert den abgeschlossenen Nachweis; Produkt, Framework-/MRTS-Pins und Required-Vertrag bleiben unverändert.

## Akzeptanzkriterien

Alle97 Required-Records und Originalvalidatoren unverändert halten; normale Exits, Signale und Startfehler direkt unterscheiden; Curl-Argumente/Streams/Timeouts bewahren; First-Byte-Writer-Messung erhalten; begrenzte Controls/Fokusprobe und genau einen neuen Standard-Full97 ausführen; echte Operations-/Identitäts-/Cleanup-Evidence, originalen Canonical PASS und geprüfte Hashes verlangen. Der tatsächliche Ready-Übergang bleibt eine separate Root-Aktion nach finalen Dokumentationsprüfungen und Veröffentlichung.

## Implementierungsentscheidung und Begründung

Bestehendes direktes Popen/wait-Verfahren in externem CURL-Override wiederverwenden, gebunden an /usr/bin/curl und den Hash der tatsächlichen Case-Quelldatei. Exklusive UUID-gebundene owner-only Start-/Abschlussreceipts werden dauerhaft fsync-gesichert. TERM/INT/HUP werden an den echten Child weitergegeben; normal 143 wird nicht als Signal ausgelegt. Keine Ableitung aus stderr/HTTP/Make-Erfolg, kein Argument-/Environment-Dump, kein neuer Timeout, keine Required-Verkleinerung oder Validatorabschwächung. Instrument-SHA256: `c4606c146fe0a47ebeb03564505082ee58c075889eae8b8dea4ff6ed401833b5`. Der Frozen-Plan-Audit bindet Case und Log exakt; ein Basename allein beweist keine Katalogidentität.

## Geänderte Dateien

`docs/pr-396-full97-followup-checklist.md`, `docs/pr-396-full97-followup-checklist.de.md`, `reports/audits/change-records/CR-20261010-r17-strict-client-full97.md`, `reports/audits/change-records/CR-20261010-r17-strict-client-full97.de.md`. Externe Recorder-/Test-/Auditdateien bleiben unter `/var/tmp/codex/ModSecurity-conector/analysis/nginx-strict-client-full97-r17-20261010T193127Z`; diese Dokumentationsaufgabe änderte keine funktionalen Checkout-Dateien.

## Ausgeführte Befehle

Alle lokalen Befehle liefen RTK-gekapselt. Natives Scaffold: `python ci/tools/new-change-record.py create --name r17-strict-client-full97 --base-revision 2f02370b07149265841411894f1a2cf7f1e978ff --date 2026-10-10`, Exit 0. Recorder-RED vor Implementierung: ein fehlender Messnachweis, Exit 1. Finale direkte Recorder-Controls:14 Tests, Exit 0; dazu8 bestandene Python-Meter-Controls. Roots R17-Receipts belegen 71 Fokustests und61 Namespace-Tests ohne SKIPs, Exit 0. Der freigegebene Standard `make full-lifecycle-nginx` endete tatsächlich mit Make-/Supervisor-Exit 0,554.091s; Originalvalidator-Exit 0. Native `make check-bilingual-docs check-doc-links` bestanden, Exit 0 nach Korrektur eines anfänglichen deutschen Überschriftsfehlers. `python -m unittest -v tests.test_change_record tests.test_bilingual_docs tests.test_prepare_reviewed_framework_handoff`: 61 Tests, keine SKIPs, Exit 0. Tatsächliche Captures bleiben im R17-Analyseverzeichnis erhalten; temporäre Daten liegen dort und der exakte Framework-Worktree wurde ausdrücklich gewählt. Diese Aufgabe wiederholte weder Runtime noch vollständigen lokalen Lint.

## Security-Auswirkung

Keine Secrets oder vollständigen Environments/Argumente gespeichert. Festes Binary/Hash, root-owned symlinkfreie Case-Datei und Ausgabeverzeichnis-Hierarchie, O_NOFOLLOW, exklusive Receipts und separater Control-Scope bewahren die bestehenden Grenzen. Runtime bleibt isolierte Loopback-Umgebung mit Root-Master/nobody-Worker. Externe Messung ist lokale Instrumentierung, kein unabhängig vertrauenswürdiger Protected-Root-Prüfer. Bestehende Source-/Runtime-Artefakte bleiben unverändert.

## Runtime-Evidence

[Öffentlicher R17-Bericht](https://github.com/Easton97-Jens/ModSecurity-conector/pull/396#issuecomment-6101794434), veröffentlicht 2026-10-10T20:21:11Z vor dieser Dokumentationsänderung. Getesteter Parent `2f02370b07149265841411894f1a2cf7f1e978ff`, Framework `9f41f80db7bf53b57429457bce0dda675d2ec5d7`, MRTS `8a6bb546c4c81d8ffc7be801dceac60c6925685f`, NGINX 1.31.6; Run `nginx_full97_2f02_20261010_r17`. Ubuntu 26.04.1 LTS/Kernel 7.0.0-38/KVM. OriginalCanonical PASS;97/97 Required-PASS, Routen14 YAML/42 native/10 config/31 derived. Inventar 166:97 PASS/34 nicht ausgewählte NOT_EXECUTED/35 NOT_APPLICABLE. Collector-Source separat PASS31/NOT_EXECUTED42-Platzhalter; spezialisierte Originalreceipts unverändert. Tatsächlich 79 HTTP-Operationen ohne Readiness einschließlich vier positiver Controls;17 Readiness;61 Lifecycles/Cleanup;57 frische direkte root-owned Projections. Direkte Curl 34 Paare:16 primary/1 First-Byte/17 readiness. Generischer Strict normaler Exit 52, kein Signal, UUID `669ba1b19fc340618d62148d715e5fc3`, PID 10440, Rule 1100301/Phase 4/Strict-Abort; Curl-HTTP 000 und Producer-HTTP 200 getrennt. First-Byte-Writer Exit 0, UUID `1515086ec928494aafd0b0a0fceab107`, PID 12514. Alle16 vereinbarten Programmreceipts über 11 Klassen normal 0. Runtime 2589 Prüfsummen, Verifikation0; Ledger `b79fbe3e2b7cf2806c8698f2a6fd7f1f1a4c4f06aed8075924311d4d1c27d97a`. Echter frischer NGINX-Binary-/Modulbuild, Engine-Cache-Wiederverwendung identitätsgeprüft. Erster eingefrorener Analyzer-Exit 1 erhalten; neue Read-only-v2/v3 nutzen nach absichtlichem Scrubbing der raw phase4.log den originalen Normalized-TX und Scrublog. Historische R15/R16 unverändert.

## Bekannte Einschränkungen

Lokaler H1-only-No-CRS-Nachweis, nicht H2/H3, Off, CRS, Produktion, andere Connectoren oder Protected. Ableitungen sind keine zusätzlichen HTTP-Operationen. Transport-EAGAIN/Short-Write beweist keinen physischen Event-Log-Sink-Short-Write; kein universeller per-Case-Loaded-Inode-Nachweis. Zusätzlicher Produkt-ShellCheck 7 Warnungen/7 Infos unverändert; historische16 Apache/MRTS-Diagnosen nicht erneut getestet. Vollständiger zusätzlicher lokaler Lint nicht erneut ausgeführt. Tatsächliche CI am getesteten Head22 SUCCESS/2 absichtliche H2/H3-SKIPs; frischer Sonar-GateOK/alle fünf Bedingungen bestanden. Späterer Docs-only-Head benötigt eigene frische Quality/Readbacks und erbt keinen Runtime-PASS.

## Verbleibende Risiken

Root muss die Dokumentationspaare prüfen/veröffentlichen, finalen Dokumentations-Head/CI zurücklesen und den bedingt freigegebenen tatsächlichen Ready-Übergang durchführen/zurücklesen. Kein zukünftiger Ready-Status oder eigene Approval wird behauptet. PR #382 bleibt OPEN/DRAFT; übergreifende I09–I12 bleiben offen. Framework PR #137 ist CLOSED/MERGED, getesteter 9f-Pin bleibt. Ready ist keine Merge-Freigabe.

## Nicht ausgeführte Prüfungen mit Begründung

Kein zweiter Full97, Protected-Dispatch, master-/Trusted-Base-/Runner-/sudoers-/Host-Gate-Änderung, Merge, Retarget, Framework-Repinning oder CrossConnector-Umbau. Diese sind nicht freigegeben oder separate Scopes. Funktionale Sourceänderungen waren unnötig, da externe Messung den bestehenden echten CURL-Aufruf erreicht. Zusätzlicher vollständiger lokaler Lint und historische Apache/MRTS-Diagnosen wurden nicht erneut ausgeführt; finale Dokumentationschecks/CI gehören Root und müssen anhand tatsächlicher Ergebnisse berichtet werden.

## Finaler Diff- und Review-Status

Die Änderung betrifft nur Dokumentation; historische Bindungen und Checkbox-IDs bleiben erhalten. Öffentlicher/lokaler Bericht geht diesen Edits voraus. Bestehende Sourcetests, originale Runtime-Status und Instrumentierung bleiben unverändert. Native EN/DE-/Pfad-/Linkprüfungen und 61 Regressionstests bestanden. Unabhängiger Review bestätigte gleiche IDs und korrigierte die Formulierung zu beobachtetem versus erforderlichem Exit52; keine numerische52-Vorgabe wurde eingeführt. Gitveröffentlichung, frische Nachfolger-CI und tatsächlicher PR-Ready-Übergang/Readback bleiben separate Root-Lieferaktionen, dokumentiert in öffentlichen PR-Metadaten. Hier wird kein Dokumentationsnachfolger-SHA oder CI-Ergebnis erfunden.
