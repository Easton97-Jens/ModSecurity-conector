# Change Record: CR-20261010-r17-pr382-nginx-system-evidence

**Sprache:** [English](CR-20261010-r17-pr382-nginx-system-evidence.md) | Deutsch

Reine Dokumentations-Evidenzreferenz; Runtime-Abnahme gehört zur exakten nachgelagerten getesteten Kombination.

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | CR-20261010-r17-pr382-nginx-system-evidence |
| Datum (UTC) | 2026-10-10 |
| Basis-Revision | `b2622a5d6ca746485c08f4789208299a111f47c7` |

## Motivation und Problemstellung

Den neu veröffentlichten nachgelagerten R17-NGINX-H1-Nachweis und den exakten I09–I12-Restumfang dokumentieren, ohne NGINX-only-Coverage zur vorgelagerten/Connector-übergreifenden Abnahme umzudeuten. Historisches R16 behält seine Messlücke; R17 misst den numerischen generischen Strict-Clientabschluss.

## Akzeptanzkriterien

Vollständige EN/DE-Parität; unveränderte R16-Historie; exakte R17-Identität, Client-/Writer-Abschlüsse und öffentlicher Link; neunspaltige Matrix mit 56 Zeilen für 14 Routenteile; breite I09–I12/V08–V10 bleiben offen und I09f/I10e erledigt; keine Produkt-/Gitlink-/Runtime-Änderung; native Dokumentations-/Archiv-/Regressions-/Diff-Prüfungen wahrheitsgemäß dokumentiert.

## Implementierungsentscheidung und Begründung

Reine Dokumentationsaktualisierung im tatsächlichen #382-Dokumentations-Worktree auf der unten genannten Basis. Unveränderliche b262-Source-/Testlinks dienen als Inventar, nicht als frische bestandene Tests. Bestätigte Apache-void-Sink-Weitergabe und ungeprüftes SPOP-fputs getrennt von unvollständigen Audits und physischen Hostnachweisen. Request-/Response-Companion-Teile bleiben getrennt. Erzeugte Change-Record-Vorlagen verwenden das native Schema, danach ersetzen echte Fakten die Vorlagentexte.

## Geänderte Dateien

- `docs/pr-382-checklist.md`
- `docs/pr-382-checklist.de.md`
- `docs/pr-382-i09-i12-rest-matrix.md`
- `docs/pr-382-i09-i12-rest-matrix.de.md`
- `reports/audits/change-records/CR-20261010-r17-pr382-nginx-system-evidence.md`
- `reports/audits/change-records/CR-20261010-r17-pr382-nginx-system-evidence.de.md`

## Ausgeführte Befehle

Arbeitsverzeichnis: `/var/tmp/codex/ModSecurity-conector/worktrees/pr382-nginx-system-docs-r17`.

```sh
rtk proxy env PYTHONDONTWRITEBYTECODE=1 /var/tmp/codex/ModSecurity-test-Framework/venv/bin/python ci/tools/new-change-record.py create --name r17-pr382-nginx-system-evidence --base-revision b2622a5d6ca746485c08f4789208299a111f47c7 --date 2026-10-10
```

Tatsächliche Vorlagenerzeugung Exit 0. Native `make check-bilingual-docs check-doc-links` bestanden (Exit 0), mit dem exakten lokalen Framework-Dokumentationsworktree und allen temporären Daten im R17-Analyseverzeichnis. EN/DE-Struktur, Repository-Pfade und Dokumentationslinks bestanden. `python -m unittest -v tests.test_change_record tests.test_bilingual_docs tests.test_prepare_reviewed_framework_handoff`: 61 Tests, keine SKIPs, Exit 0. Native Archivvalidierung und `git diff --check` ebenfalls bestanden. Alle Befehle waren RTK-gewrappt; RTK 0.51.0 verifiziert. Finale Remote-CI bleibt separat und wird nicht vorweg behauptet.

## Security-Auswirkung

Keine Änderungen an Guardrails, Autorisierung, Isolation, Validatoren, Required-Auswahl, Sinkpolicy oder Sourcecode. Keine Raw-Payloads/Environment/Secrets veröffentlicht. Diagnosenummern sind keine Client-Exits; echte Direct-Child-Abschlüsse sind explizit begrenzt. Keine Protected- oder Merge-Freigabe abgeleitet.

## Runtime-Evidence

Nachgelagerte getestete Kombination: Parent `2f02370b07149265841411894f1a2cf7f1e978ff`, Framework `9f41f80db7bf53b57429457bce0dda675d2ec5d7`, MRTS `8a6bb546c4c81d8ffc7be801dceac60c6925685f`; Run `nginx_full97_2f02_20261010_r17`. Echter Standard-Full97 Exit 0 / 554.091 Sekunden, originales Canonical PASS, 97 Required PASS (14 YAML / 42 native / 10 Config / 31 Ableitungen), null Required missing/FAIL/BLOCKED/NOT_EXECUTED, leere Schemafehler. Generischer Strict: echter normaler curl-Exit 52 Invocation `669ba1b19fc340618d62148d715e5fc3`, PID 10440; First-Byte-Writer: echter Exit 0 Invocation `1515086ec928494aafd0b0a0fceab107`, PID 12514. 34 curl-Paare, 16 Programmabschlüsse alle normal 0; 79 Nicht-Readiness-HTTP-Operationen einschließlich vier positiver Kontrollen, 61 Lifecycles/Cleanup, 57 frische Projections. Finales Ledger 2589 Einträge, unabhängiger Check 0, SHA256 `b79fbe3e2b7cf2806c8698f2a6fd7f1f1a4c4f06aed8075924311d4d1c27d97a`. [Öffentlicher Bericht](https://github.com/Easton97-Jens/ModSecurity-conector/pull/396#issuecomment-6101794434) ging dieser Änderung voraus. Keine Runtime für diese Dokumentationsrevision ausgeführt.

## Bekannte Einschränkungen

R17 ist lokaler NGINX-H1-Umfang auf Ubuntu 26.04.1 LTS / Kernel 7.0.0-38-generic / x86_64 KVM / NGINX 1.31.6, echter Root UID0/nobody UID65534 in privaten Namespaces. Keine #382-Produkt-, spätere Dokumentations-SHA-, H2/H3-, CRS-, Off-, Produktions-, andere Connector- oder Protected-Abnahme. Curl-HTTP000 ist nicht Producer-/Original200; Native Strict HTTP200 ist ein anderer Beobachter. Originale 42 Source-NOT_EXECUTED-Platzhalter bleiben mit echter spezialisierter Lineage erhalten. Lokale Raw-Evidence ist kein öffentlich herunterladbares Artefakt.

## Verbleibende Risiken

Offene I09–I12/V08–V10 über Routenteile; unvollständiger Aufrufer-/API-Audit und unabhängige physische Sinks/Hoststeuerungen. Erledigte Apache-I09f/I10e nicht wieder geöffnet. Transport-Short-Write/EAGAIN ist kein physischer Event-Sink-Short-Write; Soft-Budget nach Rückkehr kein harter Abbruch. Finale gelieferte Dokumentationshead-CI/Reviews/Sonar und Branch-Abruf bleiben Root-eigen; keine automatische Abnahmeübertragung.

## Nicht ausgeführte Prüfungen mit Begründung

Kein neuer Runtime-Lauf, Full97-Retry, Protected-Dispatch, Connector-übergreifende Tests/Sourcefixes, vollständiger Produktlint, API-Mutation, Git-Lieferung oder Merge durch diese Dokumentationsaufgabe. Nur dokumentationsnative Validierung ist im Umfang. Die nachgelagerte Runtime lief bereits separat; ihr öffentlicher Bericht wird referenziert statt erneut ausgeführt.

## Finaler Diff- und Review-Status

Nur sechs zugewiesene Dokumentationspfade; Root übernimmt finalen unabhängigen Review und normalen Commit/Veröffentlichung. Keine Source, Framework-/MRTS-Pins, Historie oder Runtime-Artefakte geändert. #382 bleibt Draft. Dieser Record behauptet weder künftigen #396-Ready-Übergang, aktuelle Dokumentations-CI noch Merge/Retarget. Native Dokumentations-, Archiv- und 61 Regressionsprüfungen lokal bestanden; finale Head-CI und unabhängige Lieferung bleiben Root-eigen und werden in öffentlichen PR-Metadaten dokumentiert.
