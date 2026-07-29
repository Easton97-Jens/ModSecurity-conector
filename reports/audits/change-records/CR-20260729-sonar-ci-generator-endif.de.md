# Change Record: Parent-CI-Block-Status-Generator-Preprocessor-End-Literal für SonarQube Cloud S1192

**Sprache:** [English](CR-20260729-sonar-ci-generator-endif.md) | Deutsch

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | `CR-20260729-sonar-ci-generator-endif` |
| Datum (UTC) | `2026-07-29` |
| Basis-Revision | `dbbc9c6aa2bca22fcd0385fa76b878873ccab2cc` |
| Grenze | Ausschließlich Parent `ci/tools/generate-block-status-config.py`, dieses englische/deutsche Change-Record-Paar und die gepaarten Indizes. Keine `.github/`, keine Test-Source, kein Framework, kein MRTS, kein Gitlink, keine Scanner-Konfiguration, kein Quality Gate, keine Exclusion, keine Suppression und keine Default-Branch-Änderung sind enthalten. |
| SonarQube-Cloud-Verknüpfung | Aktueller `python:S1192`-Befund `AZ8d8_sBE36x1qGA4xhX` für die drei identischen generierten Header-Literale `"#endif"`. |

## Motivation und Problemstellung

Der connector-neutrale Block-Status-Generator gibt dasselbe C-Preprocessor-End-
Token beim Extern-C-Abschluss, C++-Guard-Abschluss und Include-Guard-Abschluss
aus. SonarQube Cloud meldet dieses wiederholte Generated-Output-Literal als
`python:S1192`.

## Implementierungsentscheidung und Begründung

`PREPROCESSOR_ENDIF = "#endif"` liefert jetzt diese drei unveränderten
Positionen. Status-Allowlist, Connector-Allowlist, numerisches Parsing,
deterministische Sortierung, CLI-Parameter, Ausgabeorte und die Reihenfolge
des generierten Textes bleiben unverändert.

## Akzeptanzkriterien

- Ausschließlich die drei äquivalenten Generated-Header-End-Token-Referenzen
  ändern sich.
- Bestehende generierte Ausgabe bleibt für repräsentative leere, normale,
  umsortierte und vollständige Allowlist-Statusauswahlen bytegenau äquivalent.
- Alle unterstützten Connectors sowie die Fälle für ungültige Duplikate,
  Bereiche, nicht unterstützte/nicht numerische/unknown Connectors bewahren
  ihr bisheriges Ergebnis.
- Ein zukünftiger exakter PR-Head muss null neue SonarQube-Cloud-Issues und
  `0.0%` New-Code-Duplizierung erhalten, ohne Regeln oder Kontrollen zu
  schwächen.

## Geänderte Dateien

- `ci/tools/generate-block-status-config.py`
- `reports/audits/change-records/CR-20260729-sonar-ci-generator-endif.md`
- `reports/audits/change-records/CR-20260729-sonar-ci-generator-endif.de.md`
- `reports/audits/change-records/README.md`
- `reports/audits/change-records/README.de.md`

## Ausgeführte Befehle

| Befehl oder Kontrolle | Ergebnis |
| --- | --- |
| `python -B ci/checks/common/check-block-status-generator.py` mit task-eigenem temporärem Speicher | bestanden: alle Connectors, vollständige Allowlist, Ablehnung ungültiger Eingaben, deterministische Ausgabe und HAProxy-Mappings. |
| Reiner Output-Vergleich mit dem aktuellen `origin/master`-Generator | bestanden: Header-, C- und HAProxy-Text stimmten für leere, normale, umsortierte und vollständige Allowlist-Statussets überein. |
| `python -P -m py_compile ci/tools/generate-block-status-config.py` mit task-eigenem Bytecode-Cache | bestanden. |
| `git diff --check` | bestanden. |
| Fokussierter Full-File-Security-Review von Generator, Diff, Security-Guidance und nativem Smoke-Checker | bestanden: kein plausibler Candidate; bestehende CLI-Input-, Allowlist-, Deterministic-Output- und Write-Grenzen bleiben unverändert. |

## Security-Auswirkung und Restrisiko

Der Generator akzeptiert Operator-/CI-CLI-Werte und schreibt generierte
Artefakte. Seine bestehende sicherheitsrelevante Invariante lautet, dass nur
unterstützte Connectors und global erlaubte HTTP-Status diese Outputs
beeinflussen. Die Konstante ersetzt alle drei früheren Literale unveränderlich
und exakt; sie ändert weder Source-to-Sink-Pfad noch Validierung, Branch,
Ziel oder generiertes Byte.

Das `--out-dir` eines autorisierten Aufrufers bleibt eine bereits bestehende
Ausgabefähigkeit; diese enge Literalrefaktorierung erweitert oder behebt sie
nicht. Dieses Record beansprucht keine Security-Finding, Suppression oder
Behebung.

## Runtime-Evidence

Es werden keine Connector-Runtime, keine netzwerkgestützte Komponenten-
Vorbereitung und keine Host-Matrix beansprucht. Der fokussierte Generator-
Contract übt alle unterstützten Connectors, die vollständige Status-Allowlist,
Fehlerfälle, generiertes Dateilayout und Determinismus ohne Connector-Runtime
aus.

## Bekannte Einschränkungen

Der fokussierte Output-Vergleich deckt repräsentative leere, normale,
umsortierte und vollständige Allowlist-Eingaben ab, aber nicht jeden möglichen
von einem Aufrufer gewählten `--out-dir`. Die repositoryweiten bilingualen und
Link-Checks bleiben nach Korrektur der erforderlichen Überschriften dieses
Records `blocked_external_dependency`: Sie melden ausschließlich die bereits
fehlenden Framework-Gitlink-Targets, die diese Parent-only-Aufgabe weder
befüllt noch ändert.

## Verbleibende Risiken

Der exakte Hosted-PR-Head muss noch belegen, dass SonarQube Cloud den
ausgewählten S1192-Befund entfernt und zugleich null neue Issues sowie 0.0%
New-Code-Duplizierung meldet. Kein lokaler Check kann dieses Hosted-
Exact-Head-Ergebnis ersetzen.

## Nicht ausgeführte Prüfungen mit Begründung

- Kein netzwerkgestützter Connector-Build, Package-Download oder Runtime-
  Matrixlauf: Die Änderung ist eine byte-erhaltende Generator-
  Literalrefaktorierung, und der fokussierte Generator-Contract deckt ihr
  legitimes Verhalten ab.
- Kein Framework, MRTS, Gitlink, `.github/` oder unverbundene Parent-Source
  wurde ausgeführt oder geändert, weil der Nutzer die Remediation auf Parent
  `ci/` und `scripts/` eingeschränkt hat.
- Hosted-SonarQube-Cloud-, GitHub-Actions-, Review- und Merge-Evidence werden
  nicht lokal hergeleitet und benötigen den späteren exakten PR-Head.

## Finaler Diff- und Review-Status

Dieses Record beansprucht absichtlich keinen Commit, Push, Pull Request,
Hosted-Check, Review, SonarQube-Cloud-Analyse oder Merge. Diese Fakten müssen
am späteren exakten PR-Head beobachtet werden. Es wurden kein netzwerkgestützter
Connector-Build und keine Runtime-Matrix ausgeführt, weil das Generated-Output-
Literal vollständig durch den fokussierten Generator-Contract ausgeübt wird.
