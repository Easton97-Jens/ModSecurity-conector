# PR 392 vom NGINX-B09-Fix trennen

**Sprache:** [English](CR-20260929-pr392-scope-separation.md) | Deutsch

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | `CR-20260929-pr392-scope-separation` |
| Datum (UTC) | 2026-09-29 |
| Basis-Revision | `b9208c4cad24a0186e810f25d946f4bca664a278` |
| Lieferziel | Bestehender Parent-Draft-PR #392; kein Merge |

## Motivation und Problemstellung

Der Nutzer hat die Bearbeitung des Merge-Reviews freigegeben. PR #391 trägt
den vollständigeren vorgeschlagenen B09-Klassifizierer- und P2-Fix. PR #392
enthielt eine engere Änderung mit einer widersprüchlichen Assertion für
Fehlerseiten ohne Intervention. Beide Drafts dürfen nicht gegensätzliche
Verträge für dieselbe Funktion festschreiben.

## Akzeptanzkriterien

PR #392 enthält gegenüber seiner ursprünglichen Masterbasis keinen NGINX-
Produktdiff mehr. B13/C07-Produktänderungen und deren Assertions bleiben erhalten.
B09 bleibt offen und bei PR #391; die Trennung behauptet keine Behebung.

## Implementierungsentscheidung und Begründung

Der NGINX-Header wird auf den exakten Basisblob
`889e3c4765da0166f277f9b10c070543d9acdc16` zurückgesetzt. Nur die konkurrierende
B09-Testmethode und ihr ungenutzter Quellpfad entfallen. B13-Grenzwert- und
Aufruferassertions sowie C07-Quellassertions bleiben erhalten. Der veraltete
C07-Kommentar über einen Framework-Normalizerpatch wird korrigiert: Dieser
gehört nicht zu Framework-PR #128. Der bisherige Finding-Record bleibt als
historischer Vorbereitungsnachweis erhalten; dieser Record ersetzt dessen
B09-Lieferumfang, nicht dessen historische Prüfaussagen.

## Geänderte Dateien

- `connectors/nginx/src/ngx_http_modsecurity_common.h`
- `tests/test_reported_security_regressions.py`
- Dieses englisch/deutsche Change-Record-Paar.

## Ausgeführte Befehle

GitHub-API-Quell-/Blobabfragen und begrenzte Quelltransformation wurden ausgeführt.
Die ursprüngliche Testdatei stimmte vor der Änderung mit ihrem aktuellen Gitblob
überein. Python-AST und Erhalt der B13-Assertions wurden als Datenverarbeitung
geprüft. Lokale Projekttests: NOT RUN, da vorgeschriebenes RTK und provisionierte
Repositoryumgebung fehlen. CI am neuen Head steht aus.

## Security-Auswirkung

PR #392 allein liefert keine B09-Reparatur. Der vollständigere Kandidat und
seine Regressionen bleiben in PR #391. Dies trennt Arbeitseinträge und ist
weder Risikoakzeptanz noch Entfernung eines globalen Pflichtgates oder Abschluss.
B13/C07-Verhalten, Dependency-Pins, CI-Rechte und Submodule-Gitlinks bleiben gleich.

## Runtime-Evidence

Diese Nachbesserung erzeugt keinen Live-Host-Nachweis. Grüne Prüfungen des
vorherigen Heads gelten nicht automatisch für den neuen Commit. Die echte
B13-Proxygrenze und C07-Übereinstimmung von Clientantwort und Event benötigen
weiterhin ihre gezielten Laufzeitprüfungen.

## Bekannte Einschränkungen

Keine vollständige Verifikation der Securityfindings wird behauptet.
Der C07-Quellvertrag führt weder den Sidecar noch echte Eventnormalisierung aus.

## Verbleibende Risiken

Nach Integration eines der unabhängigen PRs die kombinierte Fassung erneut prüfen.
Die alte widersprüchliche BYPASS-Assertion darf bei Konflikten nicht gewählt werden.

## Nicht ausgeführte Prüfungen mit Begründung

Native Builds, lokale Suites und Live-Hosts liefen in dieser Bearbeitungsumgebung
nicht, weil Pflichtwrapper und provisionierte Umgebung fehlen. Ausgelassene
oder ausstehende Prüfungen gelten nicht als bestanden.

## Finaler Diff- und Review-Status

Die Änderung beschränkt sich auf die Umfangstrennung. Der bestehende PR bleibt
Draft; kein Merge, Force-Push, gelockertes Gate, Severitywechsel oder Findingabschluss.
