# FND-PARENT-0053 — Der exakte #74-Runtime-Producer ist bei der Apache-HTTPD-Vorbereitung blockiert

## Identität

| Feld | Wert |
| --- | --- |
| ID | FND-PARENT-0053 |
| Kategorie | ci_failure |
| Repository / Ownership | parent / parent |
| Priorität / Schweregrad / Konfidenz | P1 / not_applicable / confirmed |
| Status / Machbarkeit | fixed / feasible_now |
| Release-Blocker / sicherheitsrelevant | true / true |
| Betroffene Delivery | Parent-PR #74 am exakten Head `d93446a1b53be344f5599c48272060e2c664ae86` |
| MRTS-Auswirkung | keine; MRTS bleibt read-only |

## Beobachtung und Auswirkung

Beide Exact-Head-`verified-report-governance`-Läufe schlagen im
verpflichtenden Runtime-Producer bei `prepare-runtime-components: FAILED
apache_httpd: missing_local_httpd_build` fehlgeschlossen fehl. Ihre
Readiness-, Matrix-, Report-, Lint- und Terminal-Gate-Consumer können nach
diesem Producer-Fehler nicht erfolgreich ausgeführt werden.

Die beobachtete Klassifikation beweist einen Parent-owned
Apache-Runtime-Preparation-Blocker, aber keine Apache-Source-Root-Cause,
keinen Integrity-Bypass, keine Secret-Exposure und keine erfolgreiche hostile
Input-Ausnutzung. Parent PR #74 darf nicht integriert werden, solange der
frische strikte/vollständige Producer fehlschlägt.

## Scope und Constraints

Der aktuell beobachtete Pfad liegt in Parent-CI/Runtime-Orchestrierung und der
Parent-Apache-Komponenten-Vorbereitung. Framework-Source, Parent/Framework-
Gitlink und MRTS-Source liegen außerhalb des Remediation-Scopes dieses
Findings. Der strikte Producer und das terminale Evidence-Gate müssen
fehlgeschlossen bleiben.

## Evidenz und Einschränkung

Das aufbewahrte Exact-Head-Artefakt dokumentiert beide GitHub-Run/Job-IDs und
die gemeldete Klassifikation. Sein äußerer Producer-Log enthält nicht den
internen Apache-Source-Build-Fehler; eine Paket-, Konfigurations-, Source- oder
Code-Remediation jetzt auszuwählen wäre daher spekulativ. Follow-up `d93446a`
ist lokal validiert und normal publiziert; es legt nur den Preparation-Log des
aktuellen Runs und den festen Apache-Build-Log über Regular-File-,
Nicht-Symlink-, 300-Zeilen- und Command-Shielded-Pfade offen. Sein frisches
gehostetes Ergebnis bleibt erforderlich, bevor diese Diagnose oder eine
Apache-Remediation akzeptiert wird.

## Akzeptanzkriterien

1. Eine frische Exact-Head-Fehlerdiagnose legt ausschließlich den festen,
   task-owned Apache-Build-Log über einen begrenzten, command-shielded Pfad
   offen.
2. Der zugrundeliegende Apache-Preparation-Fehler wird aus dieser Evidence
   reproduziert und klassifiziert.
3. Die kleinste Parent-owned-Korrektur bewahrt Cache-/Pfad-Containment,
   Source-Provenance und das strikte Producer-Verhalten.
4. Fokussierte lokale Tests sowie ein frischer Exact-Head-strikter/vollständiger
   Producer und sein terminales Evidence-Gate bestehen, bevor dieses Finding
   geschlossen wird.

## Validierungsplan

- Das frische Exact-Head-gehostete Ergebnis des publizierten `d93446a`
  inspizieren und den inneren
  Apache-Fehler ohne Abschwächung von Producer oder Gate klassifizieren.
- Nur die belegte Parent-Remediation implementieren und testen; dann
  Exact-Head-CI, SonarCloud-, Review-/Thread- und geschützte
  Integrations-Checks wiederholen.

## Evidenz

- Artefakt: `.codex/runs/20260726T073000Z-pr74-apache-runtime-blocker/evidence/exact-head-ci-failure.md`
- Run-IDs: `30192356697`, `30192358331`
- Exakter Head: `28a4a1af5e764860d27ecb670bd82283e7b1aa74`
- Publiziertes Follow-up: `d93446a1b53be344f5599c48272060e2c664ae86`
- Lokale Follow-up-Controls: 19 Workflow-Sicherheits-Tests,
  `make check-ci-security-contract`, `make check-bilingual-docs` und
  `git diff --check` bestanden; sie sind keine gehostete Runtime-Evidence.

## Restrisiko

Aus dem fehlgeschlagenen Producer wird weder Runtime-Evidence noch Merge-
Assurance akzeptiert. Das strikte terminale Gate bleibt intakt; keine
Risikoakzeptanz ist dokumentiert.

## Historie

- 2026-07-26 — Aus zwei terminalen Exact-Head-#74-Hosted-Failures erstellt.
  Die begrenzte äußere Diagnose identifizierte `missing_local_httpd_build`,
  doch die innere Apache-Source-Build-Ursache wartet auf frische begrenzte
  Evidence.
- 2026-07-26 — `d93446a` mit einer Two-Path-, Command-Shielded-,
  Regular-File-only-Diagnose publiziert. Der neue Exact-Head-Producer-Lauf
  steht aus; weder Finding noch Delivery werden durch statische/lokale Controls
  geschlossen.

## Root-Cause-Update und aktuelle Remediation (2026-07-26)

Der frische Hosted-Run von `d93446a1b53be344f5599c48272060e2c664ae86`
erreichte die begrenzte Diagnose. Run `30193495484`, Job `89770795068`, gab
die innere Ursache aus:

```text
apache_poc: blocked missing required SHA256 digest for pcre2
```

Das bedingungslose Parent-`export PCRE2_SHA256` wandelte seinen fehlenden Wert
in einen explizit leeren Environment-Override um. Framework unterscheidet
absichtlich zwischen einem nicht gesetzten Wert (der sein überprüftes
Default-Pin erhält) und einem explizit leeren Wert (der fehlgeschlossen
scheitert). Die im Artefakt
`.codex/runs/20260726T083803Z-pr74-pcre2-digest-remediation/evidence/exact-head-pcre2-digest-blocker.md`
aufbewahrte schreibfreie Make-Reproduktion beobachtete `PCRE2_SHA256=<>`; die
Artefakt-SHA-256 lautet
`f226e3d727c384c55abc80cea24aec506341e831d52c9e695892ecad617e29a5`.

Dieselbe Source-Prüfung bestätigte eine Parent-Cache-Integritätslücke: Vor dem
Framework-Extraction-Time-Verifier konnte `prepare_archive` eine leere
PCRE2-Prüfsumme akzeptieren, seine Checksum-URL als Fallback verwenden,
Archivinhalt herunterladen und parsen und einen Cache-Eintrag als vollständig
markieren. Framework verhinderte weiterhin einen nachgewiesenen
Extraction-Bypass, aber Parent darf diesen unbestätigten Cache-Zustand weder
verarbeiten noch publizieren.

Die aktive Parent-only-Korrektur exportiert `PCRE2_SHA256` deshalb nur, wenn
GNU Make einen tatsächlich vom Caller bereitgestellten Wert meldet, und
erzwingt vor Parent-Archiv-/Cache-Zustand eine literale 64-hex-PCRE2-Prüfsumme.
Eine gültige Prüfsumme wird kleingeschrieben; leere, nur aus Whitespace
bestehende, fehlerhafte und nicht passende Eingaben werden abgelehnt.
`PCRE2_SHA256_URL` kann keine fehlende literale PCRE2-Prüfsumme ersetzen.
Framework bleibt die alleinige Default-Pin-Autorität und sein
Extraction-Verifier bleibt unverändert.

Die aktualisierten Akzeptanzkriterien sind: (1) fehlende, explizit leere und
gültige Caller-Werte behalten diese exakten Make-Grenzsemantiken; (2) ungültige
PCRE2-Eingabe erreicht keinen Parent-Download, Parser, Checksum-URL-Fallback
oder Cache-Publikation; (3) passende Eingabe bleibt eine legitime
`checksum_status`-`PASS`-Kontrolle und nicht passende Eingabe hinterlässt
keinen vollständigen Marker; (4) die fokussierten Parent-Make-, Cache-Contract-,
Cache-Identity-, CI-Security-, Komponenten-, Dokumentations- und Diff-Checks
bestehen; und (5) ein frischer gehosteter Exact-Head-strikter/vollständiger
Producer plus terminales Evidence-Gate besteht, bevor dieser Befund verifiziert
oder PR #74 integriert wird.

Der einzige verbleibende Finding-Level-Blocker ist frische gehostete
Exact-Head-Producer- und Terminal-Gate-Evidence nach normaler
Parent-Branch-Veröffentlichung. Verwandte Records sind `FND-CROSS-0001`,
`FND-PARENT-0052`, `FND-FRAMEWORK-0005` und die separate
Framework-Fixture-Regression `FND-FRAMEWORK-0056`. Keine fehlgeschlagene
Runtime-Ausgabe wird als Evidence akzeptiert und kein Risiko wird akzeptiert.
