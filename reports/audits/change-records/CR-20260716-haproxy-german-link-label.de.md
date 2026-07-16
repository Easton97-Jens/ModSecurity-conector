# Change Record: Deutsches HAProxy-Compiler-Leitfaden-Linklabel

**Sprache:** [English](CR-20260716-haproxy-german-link-label.md) | Deutsch

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | `CR-20260716-haproxy-german-link-label` |
| Datum (UTC) | `2026-07-16` |
| Basis-Revision | `c8450a9feaef3da9c999586ea60398653601f037` |
| Grenze | Nur Parent-Repository; Framework und MRTS unverändert. |

## Motivation und Problemstellung

`connectors/haproxy/README.de.md` zeigte `docs/build/compilers/haproxy.md`,
während sein bestehendes Markdown-Ziel die deutsche Begleitdatei
`../../docs/build/compilers/haproxy.de.md` war. Das sichtbare Label soll den
tatsächlichen deutschen Leitfaden benennen.

## Akzeptanzkriterien

- Das sichtbare deutsche Linklabel lautet `docs/build/compilers/haproxy.de.md`.
- Das bestehende Ziel bleibt `../../docs/build/compilers/haproxy.de.md`.
- Es sind keine Änderungen an HAProxy-Quellcode, Runtime-Verhalten, Framework,
  MRTS oder Gitlinks enthalten.

## Implementierungsentscheidung und Begründung

Es wird nur das lesersichtbare Label im deutschen HAProxy-README geändert. Die
englische Begleitdatei ist bereits intern konsistent und bleibt absichtlich
unverändert. Dieses knappe Change-Record-Paar dokumentiert nur den tatsächlichen
Umfang dieses Ersatz-PRs und wiederholt keine historischen PR-Records.

## Geänderte Dateien

- `connectors/haproxy/README.de.md`
- `reports/audits/change-records/CR-20260716-haproxy-german-link-label.md`
- `reports/audits/change-records/CR-20260716-haproxy-german-link-label.de.md`

## Ausgeführte Befehle

| Befehl | Ergebnis |
| --- | --- |
| `PYTHONDONTWRITEBYTECODE=1 make check-bilingual-docs` | nur wegen bereits vorhandener fehlender Audit-/Architektur-Indexziele außerhalb dieses Ersatzumfangs fehlgeschlagen; dieses Change-Record-Paar hat keinen Sprachumschalter- oder Change-Record-Fehler. |
| `PYTHONDONTWRITEBYTECODE=1 make check-doc-links` | nur wegen derselben bereits vorhandenen fehlenden Ziele außerhalb dieses Ersatzumfangs fehlgeschlagen. |
| Fokussierter `check_change_record_pair`-Aufruf und HAProxy-Label-Assertion | bestanden. |
| `git diff --check` | bestanden. |

Es wurde kein Runtime-Befehl ausgeführt oder beansprucht.

## Security-Auswirkung

Keine Änderung an Sicherheitskontrollen, Vertrauensgrenzen, Abhängigkeiten,
Credentials, Logging-Verhalten oder ausführbarer Konfiguration. Diese Korrektur
verringert das Risiko, dass Lesende versehentlich den englischen Leitfaden wählen.

## Runtime-Evidence

Nicht anwendbar. Diese Änderung verändert keinen HAProxy-Code, keine
Konfiguration, keine Build-Eingaben und kein Runtime-Verhalten.

## Bekannte Einschränkungen

Die Korrektur prüft nur den Repository-Dokumentationspfad. Sie baut oder testet
nicht HAProxy, SPOA/SPOP, HTTP/1.1, HTTP/2, HTTP/3, CRS oder MRTS.

## Verbleibende Risiken

Der Inhalt des Leitfadens wird durch diese reine Label-Änderung nicht erneut
validiert. Normale Link- und bilinguale Dokumentationsprüfungen bilden die
Evidenzgrenze.

## Nicht ausgeführte Prüfungen mit Begründung

HAProxy-Build/-Konfiguration, Runtime-, Protokoll-, Sanitizer-,
statische-Analyse- und CRS/MRTS-Prüfungen sind für eine sichtbare
Markdown-Labelkorrektur nicht anwendbar. Das breitere `make lint` ist
unverhältnismäßig und kein Dokumentationsnachweis.

## Finaler Diff- und Review-Status

Ausstehend bis zu den fokussierten lokalen Prüfungen, der Exact-SHA-Prüfung des
Ersatz-PRs und der Prüfung des finalen begrenzten Diffs. Dieser Record verwendet
keine Checks des alten PRs als Nachweis für den Ersatz-PR.
