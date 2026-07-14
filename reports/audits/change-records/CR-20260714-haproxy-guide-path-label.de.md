# Change Record: Deutschen HAProxy-Compiler-Leitfadenpfad korrigieren

**Sprache:** [English](CR-20260714-haproxy-guide-path-label.md) | Deutsch

## Identität

| Feld | Wert |
| --- | --- |
| Titel | Deutschen HAProxy-Compiler-Leitfadenpfad korrigieren |
| Change-ID | CR-20260714-haproxy-guide-path-label |
| Datum (UTC) | 2026-07-14T14:44:03Z |
| Autor oder ausführender Agent | Codex |
| Basis-Revision | be0356af96ef582c3a7dbc0169c7c8b27b7b6b34 |
| Zugehöriges Issue oder Pull Request | None bei Erstellung des Records; der autorisierte Draft-PR wird erst nach dem initialen Commit erstellt. |
| Finale Revision | not committed |

## Motivation und Problemstellung

Das deutsche HAProxy-Connector-README zeigte
`docs/build/compilers/haproxy.md`, während sein Markdown-Ziel bereits korrekt
auf `../../docs/build/compilers/haproxy.de.md` zeigte. Beide Compiler-Leitfäden
existieren, und die englische Begleitfassung zeigt und verlinkt ihren
englischen Leitfaden konsistent. Der Widerspruch machte den sichtbaren
deutschen Pfad irreführend, obwohl das Klickziel korrekt war.

## Betroffene Komponenten und Sicherheitsgrenzen

Der Scope umfasst ein sichtbares Markdown-Label in
`connectors/haproxy/README.de.md`, den gepaarten Change Record und seine
gepaarten Indexeinträge. Er ändert nur die Dokumentationsführung: Connector-
Source, Build-Konfiguration, Request-Verarbeitung, Vertrauensgrenze und
Sicherheitsverhalten ändern sich nicht. Der Framework-Worktree und der
Parent-Submodul-Gitlink sind ausgeschlossen. Ignorierte lokale Codex-
Governance-Dateien liegen absichtlich außerhalb des versionierten Diffs.

## Akzeptanzkriterien

| Kriterium | Status | Evidenz |
| --- | --- | --- |
| Der angezeigte deutsche Compiler-Leitfadenpfad ist `docs/build/compilers/haproxy.de.md` und stimmt mit seinem bestehenden Markdown-Ziel überein. | erfüllt | Source-Review, `make check-bilingual-docs` und `make check-doc-links` |
| Der korrekte englische Begleitpfad und sein Ziel bleiben unverändert. | erfüllt | Scoped-Diff-Review |
| Der versionierte Scope enthält nur diese Korrektur, das EN/DE-Change-Record-Paar und die gepaarten Change-Record-Indexeinträge. | erfüllt | Cached-Name-Status-, Stat-, Check- und Full-Diff-Review |
| Der Delivery-Smoke bleibt ausschließlich dokumentarisch und erhebt keinen Runtime-, Release- oder Production-Readiness-Claim. | vor der Auslieferung erfüllt | Abgegrenzter Scope dieses Records und finaler Delivery-Review |

## Untersuchte Alternativen

Das deutsche Ziel auf den englischen Leitfaden zu ändern, wurde verworfen, da
der deutsche Leitfaden bereits existiert und das bestehende Ziel korrekt ist.
Das englische README zu ändern, wurde verworfen, weil sichtbarer Pfad und Ziel
dort bereits konsistent sind. Eine umfassendere HAProxy-Dokumentations-
Überarbeitung liegt außerhalb dieses einzelnen Label-Widerspruchs.

## Implementierungsentscheidung und Begründung

Nur das deutsche sichtbare Link-Label von `haproxy.md` auf `haproxy.de.md`
ändern und das bestehende deutsche Ziel behalten. Damit stimmt der Text, den
Leser sehen, mit der Datei überein, die sie öffnen, ohne Build- oder Runtime-
Dokumentationsinhalt zu verändern.

## Geänderte Dateien

- `connectors/haproxy/README.de.md`
- `reports/audits/change-records/CR-20260714-haproxy-guide-path-label.md`
- `reports/audits/change-records/CR-20260714-haproxy-guide-path-label.de.md`
- `reports/audits/change-records/README.md`
- `reports/audits/change-records/README.de.md`

Lokale `AGENTS.md`- und `.codex/`-Governance-Ergänzungen sind ignoriert und
nicht Teil dieses versionierten Diffs.

## Hinzugefügte oder geänderte Tests

None. Dies ist eine Dokumentations-Label-Korrektur; vorhandene
Dokumentationsprüfungen sind die passende Verifikation.

## Ausgeführte Befehle

| Exakter Befehl | Exit-Code oder Ergebnis | Sanitisierte relevante Zusammenfassung | Kanonischer Evidence-Pfad | Run-ID |
| --- | --- | --- | --- | --- |
| `rtk git blame -L 81,81 -- connectors/haproxy/README.de.md` | `0` | Das widersprüchliche sichtbare Label wurde auf die aktuelle getrackte Zeile zurückgeführt. | None | None |
| `rtk ls -l docs/build/compilers/haproxy.md docs/build/compilers/haproxy.de.md` | `0` | Englische und deutsche Compiler-Leitfadendatei existieren beide. | None | None |
| `rtk make check-bilingual-docs` | `0` | Die bilinguale Dokumentationsprüfung bestand. | None | None |
| `rtk make check-doc-links` | `0` | Repository-Pfadreferenzen und Framework-Dokumentationslinks bestanden. | None | None |
| `rtk git diff --check` | `0` | Im getrackten Worktree-Diff wurden keine Whitespace-Fehler gefunden. | None | None |
| `rtk git diff --cached --name-status` | `0` | Genau fünf scoped Dokumentations- und Change-Record-Pfade wurden gestaged. | None | None |
| `rtk git diff --cached --stat` | `0` | Die staged Änderung ist auf die erwarteten fünf Dateien begrenzt. | None | None |
| `rtk git diff --cached --check` | `0` | Im staged Diff wurden keine Whitespace-Fehler gefunden. | None | None |
| `rtk proxy git diff --cached` | `0` | Der vollständige staged-Diff-Review fand nur die beabsichtigte Link-Label-Korrektur und gepaarte Records/Indizes. | None | None |

## Security-Auswirkung

Keine Änderung des Sicherheitsverhaltens, der Validierung, Defaults, des
Logging-Formats oder der Vertrauensgrenze. Das korrigierte sichtbare
Dokumentationsziel verringert nur Leser-Verwirrung; es belegt keine
Sicherheitseigenschaft.

## Dokumentationsänderungen

`connectors/haproxy/README.de.md` zeigt jetzt sein bestehendes deutsches
Compiler-Leitfadenziel korrekt an. Der gepaarte Change Record und die
gepaarten Indexzeilen zeichnen die abgegrenzte Korrektur auf. Das englische
HAProxy-README wurde geprüft und bleibt unverändert, weil es bereits korrekt
ist.

## Runtime-Evidence

Für diese Änderung wurde keine Runtime-Evidence erhoben oder beansprucht.
Dokumentationsprüfungen, ein Commit, ein Draft-PR und CI sind keine
HAProxy-Runtime-Evidence.

## Bekannte Einschränkungen

Diese Änderung korrigiert nur ein sichtbares Pfadlabel. Sie testet, baut oder
ändert weder HAProxy noch seine SPOA/SPOP-Integration, Compiler-Anforderungen
oder die zugrunde liegenden Leitfäden.

## Verbleibende Risiken

Künftige Verschiebungen oder Umbenennungen des Compiler-Leitfadens müssen
sichtbares Label und Markdown-Ziel zusammen aktualisieren. Die scoped
Dokumentationsprüfungen verringern, können aber künftigen Dokumentationsdrift
nicht ausschließen.

## Nicht ausgeführte Prüfungen mit Begründung

HAProxy-Build-, Konfigurations-, H1/H2/H3-, CRS/MRTS-, Hardening-, Sanitizer-,
statische Analyse-, Smoke- und Lifecycle-Prüfungen sind für eine
Dokumentations-Label-Korrektur nicht anwendbar und würden keine relevante
Runtime-Evidence liefern. Es gibt kein eigenständiges
`make check-repository-path-references`-Target; der bestehende Pfadprüfer lief
innerhalb von `make check-doc-links` und bestand. `make lint` und
`make quick-check` werden nicht ausgeführt, weil ihr breiterer
Build- und Framework-Scope für diese einzelne Label-Änderung nicht angemessen
ist.

## Finaler Diff- und Review-Status

Die lokalen bilingualen, Link-/Pfadreferenz- und Whitespace-Prüfungen bestanden.
Die fünf staged Pfade und ihr vollständiger Cached-Diff wurden manuell geprüft,
und `git diff --cached --check` bestand. Commit, Push, Draft-PR und
CI-Verifikation für die exakte finale SHA stehen noch aus. Dieser Delivery-
Smoke ist keine Release-Freigabe und muss ungemergt bleiben; Auto-Merge bleibt
deaktiviert.
