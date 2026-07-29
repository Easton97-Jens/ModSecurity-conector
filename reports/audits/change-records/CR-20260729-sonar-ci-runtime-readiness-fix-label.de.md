# Change Record: Parent-CI-Runtime-Readiness-Deduplizierung des Remediation-Labels für SonarQube Cloud S1192

**Sprache:** [English](CR-20260729-sonar-ci-runtime-readiness-fix-label.md) | Deutsch

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | `CR-20260729-sonar-ci-runtime-readiness-fix-label` |
| Datum (UTC) | `2026-07-29` |
| Basis-Revision | `dbbc9c6aa2bca22fcd0385fa76b878873ccab2cc` |
| Grenze | Ausschließlich Parent `ci/checks/evidence/check-runtime-producer-readiness.py`, dieses englische/deutsche Change-Record-Paar und die gepaarten Indizes. Keine `.github/`, keine Test-Source, kein Framework, kein MRTS, kein Gitlink, keine Scanner-Konfiguration, kein Quality Gate, keine Exclusion, keine Suppression und keine Default-Branch-Änderung sind enthalten. |
| SonarQube-Cloud-Verknüpfung | Aktueller `python:S1192`-Befund `AZ7POyUhBW70q7L2nMJN` für neun gleiche Component-Remediation-Labels `"run make prepare-runtime-components"`. |

## Motivation und Problemstellung

Der Runtime-Producer-Readiness-Report zeigt für neun erforderliche NGINX-,
Apache- und HAProxy-Component-Zeilen dasselbe feste Remediation-Label.
SonarQube Cloud meldet dieses wiederholte Source-Literal als `python:S1192`.

## Implementierungsentscheidung und Begründung

`RUNTIME_COMPONENT_PREPARATION_FIX` besitzt jetzt das exakte bestehende Label
und liefert es nur für diese neun Component-`fix`-Felder. Der abweichende Wert
`"make prepare-runtime-components"` in der NGINX-Readiness-Zusammenfassung
ist nicht Teil der Änderung. Component-Namen, Reihenfolge, Pfade,
`required`-Flags, Pfadvalidierung, Runtime-Environment-Verarbeitung,
`BLOCKED`-Berechnung und Exit-Codes bleiben unverändert.

## Akzeptanzkriterien

- Ausschließlich die neun gleichen Component-Remediation-Label-Referenzen
  ändern sich.
- Ein kontrollierter vollständiger Readiness-Payload bleibt mit der aktuellen
  `master`-Implementierung bytegenau äquivalent.
- Der bestehende sichere externe Source-Root-Control sowie die Ablehnung von
  `/etc` und fremden Roots behalten ihre Ergebnisse.
- Ein zukünftiger exakter PR-Head muss null neue SonarQube-Cloud-Issues und
  `0.0%` New-Code-Duplizierung erhalten, ohne Regeln oder Kontrollen zu
  schwächen.

## Geänderte Dateien

- `ci/checks/evidence/check-runtime-producer-readiness.py`
- `reports/audits/change-records/CR-20260729-sonar-ci-runtime-readiness-fix-label.md`
- `reports/audits/change-records/CR-20260729-sonar-ci-runtime-readiness-fix-label.de.md`
- `reports/audits/change-records/README.md`
- `reports/audits/change-records/README.de.md`

## Ausgeführte Befehle

| Befehl oder Kontrolle | Ergebnis |
| --- | --- |
| Python `3.14.4` `-m py_compile` des geänderten Checkers mit task-eigenem Bytecode-Cache-Root | bestanden. |
| `python -B -m unittest -v tests.test_runtime_producer_readiness_path_policy` mit task-eigenem temporärem Speicher | bestanden: 4 Tests, einschließlich sicherem kanonischem Source-Root-Control sowie Runtime-Environment-`/etc`- und Foreign-Root-Ablehnung. |
| Kontrollierter Base-versus-Head-`build_payload()`-Paritäts-Harness | bestanden: vollständige Payload-Gleichheit und unveränderte Required-Component-Remediation-Labels. |
| `make check-runtime-producer-readiness` mit demselben ausgewählten Python und task-eigenem temporärem Speicher | blocked_external_dependency: Der Checker gab korrekt `BLOCKED`/77 zurück, weil NGINX-, Apache- und HAProxy-Runtime-Artefakte nicht vorbereitet sind. Keine Component-Vorbereitung wurde gestartet. |
| `git diff --check` | bestanden. |
| Fokussierter Full-File-Security-/Control-Review | bestanden: kein plausibler Security-Candidate. Das feste Label erreicht nur Report-Text, niemals Command-, Pfad-, Autorisierungs-, Status- oder Exit-Code-Sink. |

## Security-Auswirkung und Restrisiko

Der Checker erhält CLI-Roots, Environment-Werte, gecachte Runtime-Environment-
Werte und Framework-Common-Shell-Output. Seine sicherheitsrelevante Invariante
lautet, dass fehlende Components oder unsichere Runtime-Pfade `BLOCKED`
bleiben und keine System-Write-Pfade autorisieren können. Der gemeinsame Wert
ist Source-authored, wird nicht externalisiert und nur in Report-Content
gerendert; er kann Validierung oder Control-Flow des Checkers nicht ändern.

Dieses Record beansprucht keine Security-Finding, Suppression oder Behebung.
Das Restrisiko ist auf Implementierungstippfehler oder versehentliche
Scope-Ausweitung begrenzt; beide werden vom fokussierten Diff-Review und
Payload-Paritätscheck abgedeckt.

## Runtime-Evidence

Es werden keine Connector-Runtime, keine Component-Provisionierung, kein
Netzwerkzugriff, keine Package-Installation und keine Host-Matrix beansprucht.
Der direkte native Readiness-Befehl wurde korrekt blockierend beobachtet, als
erforderliche Runtime-Artefakte fehlten; das fokussierte Unit-Modul übt die
relevanten legitimen und negativen Pfadkontrollen ohne Provisionierung aus.

## Bekannte Einschränkungen

Das fokussierte Unit-Modul verifiziert Path-Policy-Verhalten, nicht eine
vollständig vorbereitete NGINX-/Apache-/HAProxy-Installation. Das Bestehen des
nativen Readiness-Befehls braucht separat vorbereitete Artefakte und ist keine
Voraussetzung für diese Equal-String-Refaktorierung.

## Verbleibende Risiken

Der exakte Hosted-PR-Head muss noch belegen, dass SonarQube Cloud den
ausgewählten S1192-Befund entfernt und zugleich null neue Issues sowie `0.0%`
New-Code-Duplizierung meldet. Kein lokaler Check kann dieses Exact-Head-
Ergebnis ersetzen.

## Nicht ausgeführte Prüfungen mit Begründung

- Kein `make prepare-runtime-components`, netzwerkgestützter Build,
  Package-Download oder Runtime-Matrixlauf: Diese würden unverbundene
  Runtime-Artefakte provisionieren statt diesen festen Report-Textwert zu
  validieren.
- Kein Framework, MRTS, Gitlink, `.github/` oder unverbundene Parent-Source
  wurde ausgeführt oder geändert, weil der Nutzer die Remediation auf Parent
  `ci/` und `scripts/` eingeschränkt hat.
- Hosted-SonarQube-Cloud-, GitHub-Actions-, Review- und Merge-Evidence werden
  nicht lokal hergeleitet und benötigen den späteren exakten PR-Head.

## Initialer Delivery-Status

Der initiale Source-und-Traceability-Commit
`491367f4708d9f2f67cfa8ec418032e1767a0f67` wurde auf
`agent/parent-ci-runtime-readiness-remediation-20260729` gepusht, und Draft
PR [#171](https://github.com/Easton97-Jens/ModSecurity-conector/pull/171)
wurde gegen `master` eröffnet. Bei der PR-Erstellung stimmten lokaler,
Remote- und PR-Head auf diesen Commit überein. Dieses Delivery-Metadaten-
Follow-up ändert nur Dokumentation; daher ist weiterhin ein frischer
Exact-Head-Zyklus für GitHub Actions und SonarQube Cloud nötig. Es ist kein
Merge autorisiert oder beansprucht.

## Finaler Diff- und Review-Status

Der finale Source-Diff bleibt auf den einen Parent-CI-Readiness-Checker
begrenzt: Eine Source-authored-Konstante liefert dieselben neun festen
Report-Labels. Dieses bilinguale Change-Record-Paar und seine Indizes liefern
nur die erforderliche Delivery-Traceability. Die fokussierten Payload-Paritäts-,
Path-Policy-, Syntax-, Diff- sowie Security-/Control-Prüfungen bestanden; der
native Readiness-Befehl blieb wegen fehlender externer Runtime-Artefakte
korrekt blockiert. Bei diesem Record-Stand hat Draft-PR #171 seine frische
Exact-Head-Hosted-Verifikation noch nicht abgeschlossen; es ist kein Merge
autorisiert oder beansprucht.
