# B09-Integration mit echtem NGINX-Fehlerseitenrouting

**Sprache:** [English](CR-20260929-nginx-b09-host-integration.md) | Deutsch

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | `CR-20260929-nginx-b09-host-integration` |
| Datum (UTC) | 2026-09-29 |
| Basis-Revision | `f490ba693d2a014ead7b6b477cc7933a0f3e4bc6` |
| Lieferziel | Bestehender Parent-Draft-PR #391; kein Merge |

## Motivation und Problemstellung

Im Merge-Review fehlte echtes Fehlerseitenrouting als B09-Nachweis. Die
isolierten Klassifizierertests zeigen weder das tatsächliche NGINX-Phasenscheduling
noch, ob der Contenthandler des geschützten Ziels erreicht wird.

## Akzeptanzkriterien

Die bereits provisionierten Exact-Head-Artefakte von NGINX, Modul und
libmodsecurity sowie der getrennte Non-Root-Worker werden verwendet. Ein Ursprung
antwortet mit 418 und leitet intern zum geschützten Ziel. Mit harmlosem P2-Deny-
Marker muss der Client 403 erhalten, das native Log die P2-Regel nennen und der
Zielbackendaufruf ausbleiben. Ohne Marker muss das Ziel seinen Kontrollbody liefern
und genau einmal aufgerufen werden. Deaktivierten und aktiv erlaubenden Ursprung,
wiederholte Ablehnungen, anschließende erlaubte Requests und geordnetes Ende prüfen.

## Implementierungsentscheidung und Begründung

Eine begrenzte Loopback-HTTP/1-Fixture ergänzt den vorhandenen Hosted-Functional-A-
Einstieg. Root-Launcher, Provisionierung, Workeraccount, private Verzeichnisse,
bisherige Kontrollen und Evidencewriter bleiben unverändert. Das Shellskript
bekommt nach der bisherigen Evidenceprojektion einen festen Python-Aufruf.
Die Fixture prüft Head und Worker-UID/GID, bindet Artefakthashes, verwendet private
Testregeln und beobachtet den Backendaufruf statt nur den Clientstatus. Beliebige
rekursive Fehlerseitenkonfigurationen oder vollständige Profilabdeckung werden
nicht als geprüft behauptet.

## Geänderte Dateien

- `connectors/nginx/harness/run_error_page_intervention.py`
- `connectors/nginx/harness/run_exact_head_use_error_log.sh`
- Dieses englisch/deutsche Change-Record-Paar.

## Ausgeführte Befehle

Die vollständige ursprüngliche Shelldatei wurde vor der einzelnen Ergänzung
rekonstruiert und gegen Gitblob `b90c8d90364d4a6330ded43cbc8a2fadde9eb644` geprüft.
Die Python-Fixture wurde als AST geparst. Lokale Projektausführung unterblieb,
weil RTK und provisionierte native Artefakte fehlen. Tatsächliche Integration
und CI-Ergebnisse stehen für den neuen veröffentlichten Head aus.

## Security-Auswirkung

Keine Änderung an Connector-Produktcode, Gates, Tokenrechten, Root-Broker,
Worker-Identitätsvorgaben, Dependency-Pins oder Gitlinks. Loopbackverkehr und
Dateien gehören ausschließlich zum frischen Testlauf. Root-Master und Non-Root-
Worker bleiben getrennt; Identitäten und Prozessende werden ausdrücklich beobachtet.

## Runtime-Evidence

Bei Erfolg druckt der Job NGINX_B09_RESULT mit Parent-SHA, Artefakt-/Regelhashes,
einzelnen Status-/Backendbeobachtungen, Workertrennung und Cleanup. Private Rohlogs
bleiben unter der Functional-A-Laufwurzel. Bisherige Functional-A-Ergebnisse
zertifizieren B09 nicht automatisch; der ausdrückliche neue Nachweis ist nötig.
Dies ist begrenzte Integration, keine unabhängige geschützte Attestierung.

## Bekannte Einschränkungen

Der Test umfasst HTTP/1, einen internen Fehlerseitenschritt und ein P2-
Headerprädikat. Nicht alle Rekursionsregeln, Responseinterventionen, Bodymodi oder
Deployments sind damit bewiesen. Kein Finding wird automatisch geschlossen.

## Verbleibende Risiken

Fehler müssen an der echten Hostgrenze diagnostiziert und dürfen nicht durch
schwächere Assertions versteckt werden. Kombinationen mit anderen NGINX-PRs
benötigen neue Checks. PR #392 trägt nur B13/C07 und keinen Konkurrenzklassifizierer.

## Nicht ausgeführte Prüfungen mit Begründung

Lokale native Builds und Laufzeittests liefen mangels Pflichtwrapper und
provisionierter Umgebung nicht im Editor. Der neue Hosted-Aufruf muss vor der
Abnahme tatsächlich durchlaufen und sein Ergebnis ausgewertet werden.

## Finaler Diff- und Review-Status

Nur Fixture, ein fester Aufruf und dieses Record-Paar werden ergänzt. Vorhandene
Checks und Assertions bleiben erhalten. Draftstatus, offene Findings und
Repositorygrenzen bleiben bestehen; kein Merge und kein Force-Push.
