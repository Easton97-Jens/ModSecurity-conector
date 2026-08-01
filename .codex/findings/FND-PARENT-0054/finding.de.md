# FND-PARENT-0054 — Der Runtime-Matrix des exakten PR #74 fehlte kausale Hosted-Ausgabe

## Identität

| Feld | Wert |
| --- | --- |
| ID | FND-PARENT-0054 |
| Kategorie | evidence_gap |
| Repository / Ownership | parent / parent |
| Priorität / Schweregrad / Konfidenz | P1 / not_applicable / validated |
| Status / Machbarkeit | in_progress / blocked_missing_evidence |
| Release-Blocker / sicherheitsrelevant | false / true |

## Beobachtung, Auswirkung und Evidenz

Am Parent-PR-#74-Head `7238c9d0a0902affbf7dfae1d7f96d6603d80f89` bestanden im Hosted-Run `30196090664`, Job `89777788658`, Komponenten-Vorbereitung und Readiness einschließlich des reparierten PCRE2-/Apache-Pfads, danach schlug `make runtime-matrix-all-runtime` mit `rc=2` fehl.

Parallele Matrix- und abhängige Report-/Layout-/Lint-/Quick-Check-Consumer schlugen deshalb fehl oder wurden ungültig, und das terminale strikte Evidence-Gate wurde übersprungen.

Der äußere Log legt nur `$BUILD_ROOT/verified-runs/<validated-run-id>/logs/04-make-runtime-matrix-all-runtime.log`, nicht den kausalen Inhalt offen. Die aufbewahrte Evidenz ist `.codex/runs/20260726T093511Z-pr74-runtime-matrix-blocker/evidence/hosted-runtime-matrix-failure.md` mit SHA-256 `058e7f6654014df476a7ae375c1a938d1cf04ccaf5a4996884919d222c243757`.

Die begrenzte Diagnostik des nächsten historischen exakten Heads
`6809e348ad043bf3fcfd9b90d963882cc2fb2cb2` legte die Ursache im Hosted-Run
`30197684223`, Job `89782035387`, offen: Apache- und NGINX-cache-gestützte
Refreshes lehnten korrekt einen abweichenden Owner-Root ab. Dieses
historische Observability-Ergebnis bleibt erhalten; die getrennte Remediation
liegt bei `FND-CROSS-0008`, und keine fehlgeschlagene Evidence wurde akzeptiert.

## Ursache, Remediation und Validierung

Die begrenzte Parent-Diagnostik stellte die Matrix-Ursache fest, ohne den
strikten Producer oder das terminale Gate zu schwächen. Dies ist weder ein
Duplikat von `FND-PARENT-0053`, dessen PCRE2-Provenance-Defekt sich im selben
Lauf nicht mehr reproduziert, noch von `FND-CROSS-0008`, das die
Parent-/Framework-Cache-Owner-Root-Remediation besitzt.

Die historische Parent-only-Remediation tailte genau den festen von der Run-ID
abgeleiteten `04`-Matrix-Log erst nach vorhandener Run-ID-Validierung, verlangte
einen regulären Nicht-Symlink-Log, begrenzte auf 300 command-geschützte Zeilen
und ließ das terminale Gate unverändert.

Keine Rekursion, kein Glob, keine breite Log-Suche sowie keine Framework-/MRTS-/Gitlink- oder Risikoakzeptanz-Aktion sind autorisiert.

Fokussierte Workflow-Security- und Dokumentationsvalidierung bestand vor der
Publikation. Der frische exakte Hosted-Producer legte die echte Ursache offen
und bewahrte die Ablehnung. Zugehörige/abhängige Records sind
`FND-CROSS-0001`, `FND-PARENT-0053`, `FND-FRAMEWORK-0056` und
`FND-CROSS-0008`.

## Historie

- 2026-07-26 — Der exakte Hosted-Producer bestand PCRE2-/Apache-Vorbereitung, schlug aber in der verpflichtenden Matrix fehl, ohne seinen kausalen festen Log offenzulegen.
- 2026-07-26 — Die begrenzte Next-Head-Diagnostik legte die Cache-Owner-Root-Ursache offen; dieses Observability-Finding ist `verified`, die getrennte Reparatur wird als `FND-CROSS-0008` verfolgt.

## Aktueller Abstimmungsstatus — 2026-08-01

Die frühere vorgeschlagene Archivdisposition wird zurückgezogen. Zwar wurde
[PR #74](https://github.com/Easton97-Jens/ModSecurity-conector/pull/74) als
`0b278f7ef952d5d47a2109ea265a95bf4d887772` gemergt, aber der einzige Commit mit
der begrenzten Diagnose, `b28b8744765a2cac6e3cf91f7bd3070d49d7774d`, ist **kein**
Vorfahr des aktuellen `origin/master` `59aba762f2d852fd917079ca8519e4ea7f49169c`.
Die heutige `verified-report-governance.yml` ist bewusst der leichte Pfad
`make report-governance`, und `test_verified_report_governance_stays_lightweight`
verlangt die Abwesenheit von `verified-report-run`, dem strikten Evidence-Gate
und den Runtime-Matrix-Begriffen.

Historische PR-Checks, CodeQL und SonarCloud beweisen deshalb kein aktuelles
gleichwertiges Control. Dieser Record bleibt als `in_progress` aktiv, bis
entweder Current-Source-Evidence für ein gleichwertiges begrenztes Fail-Closed-
Control oder eine autorisierte, evidenzgestützte Retirement-/Replacement-
Entscheidung vorliegt. Diese Abstimmung ändert keinen Produkt-Workflow, kein
Framework, MRTS, Gitlink, Scanner, Gate oder Risikocontrol; `FND-CROSS-0008`
bleibt getrennt aktiv.
