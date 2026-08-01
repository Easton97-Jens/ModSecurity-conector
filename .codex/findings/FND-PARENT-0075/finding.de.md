# FND-PARENT-0075 — PR #202 Secret Scanning kann eine historische Dokumentations-Token-Heuristik nicht bereinigen

## Klassifikation

| Feld | Wert |
| --- | --- |
| ID | FND-PARENT-0075 |
| Kategorie | ci_failure |
| Repository / Ownership | parent / parent |
| Priorität / Schweregrad / Konfidenz | P1 / not_applicable / reproduced (0.95) |
| Status / Umsetzbarkeit | not_applicable / not_applicable |
| Release-Blocker / Kandidat für Integrationsblocker / sicherheitsrelevant | false / false / true |
| Protokoll / Profil | GitHub Actions pull-request Secret scanning und checksum-verifizierte Gitleaks-Commit-Range-Grenze / historischer Parent-PR #202 ist geschlossen; frischer Parent-PR #213 bestand seine exakte Range und wurde bei `f335965fd5f7b9640fc39a1dd7873d46d7c989c5` nach `master` gemergt |

## Zusammenfassung

Der exakte Secret-Scanning-Job von PR #202 scannt die vollständige
Merge-Base-Commit-Range statt nur des finalen Trees. Der finale bilinguale
Change Record rendert öffentliche opake Sonar-Identifier jetzt als
rekonstruierbare Fragmente, aber der ursprünglich veröffentlichte Task-Commit
bleibt in der PR-Historie. Der Detector liefert deshalb zwei
`generic-api-key`-Heuristiktreffer, obwohl die begrenzte Triage einen
öffentlichen Nicht-Credential-Dokumentations-Identifier je Sprache und keine
Credential-Quelle oder keinen Sink belegt.

Dies ist kein Beleg für eine Credential-Exposition. Es ist dennoch ein
anwendbarer, fail-closed Security-Control-Fehler; PR #202 kann daher ohne
aktuelle Benutzerentscheidung weder vollständig verifiziert noch sicher
gemergt werden. Kein roher Match, Token oder Scanner-Wert wird in diesem Record
aufbewahrt.

## Aktuelle Disposition nach verifiziertem Ersatz

Der aktuelle Benutzer autorisierte einen Ersatz mit frischer Historie. PR #213
bestand seine exakten erforderlichen Head-Checks, `pull-request-range` Secret
Scanning, das SonarQube-Cloud-Quality-Gate, null OPEN/CONFIRMED-PR-Issues,
null neue duplizierte Zeilen und `0.0%` New-Code-Duplizierung. Er wurde danach
über den normalen geschützten SHA-gebundenen Squash-Pfad nach `master` bei
`f335965fd5f7b9640fc39a1dd7873d46d7c989c5` gemergt; auch die Post-Merge-
Master-Checks bestanden. Erst nach dieser Verifikation wurde PR #202 als
abgelöst geschlossen.

Die historische #202-Range bleibt als Evidence erhalten und würde bei einer
erneuten Auswertung weiterhin die historische Heuristik enthalten. Sie ist
jedoch kein aktiver Delivery-Kandidat oder Integrationsblocker mehr. Dieser
Record ist deshalb `not_applicable`; das ist keine Behauptung, die historische
Beobachtung sei umgeschrieben, unterdrückt oder fälschlich grün erklärt worden.

## Beobachtetes und erwartetes Verhalten

| Aspekt | Beobachtet | Erwartet |
| --- | --- | --- |
| Exakter Scan | GitHub-Actions-Run `30689182074`, Job `91340747868`, scannte `651834ef577095a48b7f54d5bd7ffcc76d9c388a..ecccaa0adf16b329162167eb1abe8a0003dc0052`, lieferte Exit `1` und zwei redigierte Treffer. Der checksum-pinned lokale Range-Scan lieferte dieselbe Anzahl und denselben Exit. | Secret Scanning bleibt fail-closed und es wird kein echtes Credential committed. Ein Delivery-Kandidat hat eine scan-passende Commit-Range ohne Änderung von Gitleaks-Regeln, Workflows, Ignores, Allow-Lists oder Redaction. |
| Finaler Tree | Der aktuelle englische/deutsche Change Record vermeidet das bekannte zusammenhängende Detector-förmige Rendering und bewahrt die Rekonstruierbarkeit. | Der finale Inhalt bleibt prüfbar und bilingual, ohne den historischen Detector-förmigen Wert erneut einzuführen. |
| PR-Historie | Der ursprüngliche veröffentlichte Commit liegt in der Merge-Base-bis-Head-Range; ein normaler neuer Commit kann daher das frühere Detector-Ergebnis nicht bereinigen. | Einen frischen autorisierten Kandidaten verwenden oder eine aktuelle explizite Risikoentscheidung aufzeichnen; niemals veröffentlichte Historie umschreiben, um das Ergebnis zu verbergen. |

## Auswirkung und betroffener Scope

PR #202 schlägt in einem anwendbaren Security-Control fehl, obwohl Final Tree
und SonarQube-Cloud-Analyse sauber sind. Das Ergebnis als grün zu behandeln
würde die Secret-Scanning-Evidence irreführend machen. Der Bericht belegt eine
Token-förmige historische Dokumentations-Heuristik, keine Credential-Quelle,
keinen Sink und kein exponiertes Secret. Er ist Kandidat für einen
Integrationsblocker, kein Projekt-Release-Blocker.

- `reports/audits/change-records/CR-20260730-sonar-ci-runtime-security-root-remediation.md`
- `reports/audits/change-records/CR-20260730-sonar-ci-runtime-security-root-remediation.de.md`
- `CR-20260730-sonar-ci-runtime-security-root-remediation` Tracking-Zeile
- `Secret scanning / pull-request-range`

Kein Framework, MRTS, Gitlink, Scanner-Konfiguration, Secret Store oder
Default-Branch-Inhalt wird durch dieses Finding geändert.

## Voraussetzungen und Reproduktion

1. PR #202 behält seinen ursprünglichen veröffentlichten Commit mit
   zusammenhängendem öffentlichem opaken Dokumentationstext.
2. Der Secret-Scanning-Workflow ruft Gitleaks mit
   Merge-Base-bis-Head-Commit-Range-Semantik auf.
3. Der Benutzer hat nur die Integration von PR #202 autorisiert, nicht einen
   Ersatz-PR, Force-Push, Rewrite veröffentlichter Historie,
   Scanner-Policy-Änderung oder Risikoakzeptanz.

Reproduktion ohne einen Match-Wert aufzubewahren: Run `30689182074` und Job
`91340747868` am exakten Head `ecccaa0adf16b329162167eb1abe8a0003dc0052`
prüfen und checksum-pinned Gitleaks mit `--redact=100` gegen
`651834ef577095a48b7f54d5bd7ffcc76d9c388a..ecccaa0adf16b329162167eb1abe8a0003dc0052`
ausführen. Der redigierte Job und der lokale Range-Scan liefern jeweils zwei
Findings und Exit `1`. Das finale Fragment-Rendering mit der ursprünglichen
Historie vergleichen, ohne einen Detector-Wert auszugeben oder zu speichern:
Ein normaler Follow-up-Commit kann ein historisches Range-Ergebnis nicht
ändern.

## Evidence

| Run | Artefakt | SHA-256 | Ergebnis |
| --- | --- | --- | --- |
| `pr-202-head-eccc-secret-scan-recurrence-20260801` | `/var/tmp/codex/ModSecurity-conector/runs/ci-runtime-sonarqube-remediation-20260730/evidence/pr-202-head-eccc-secret-scan-recurrence.md` | `86a3b7d2c45da8f150e6898ec364d3cf3353b7e333e30fbc68a92f500faef0c5` | Sanitized GitHub- und lokale Exact-Range-Receipt: zwei redigierte generic-api-key-Heuristiktreffer, Exit `1`; kein roher Match aufbewahrt. |
| `pr-202-head-eccc-sonar-clean-20260801` | `/var/tmp/codex/ModSecurity-conector/runs/ci-runtime-sonarqube-remediation-20260730/evidence/pr-202-head-eccc-sonar-clean.md` | `8cea3f6df1afb3b33b4f84acfbf91373282d7d1b8477d96ec975fd2060e002c3` | SonarQube Cloud Quality Gate `OK`, null offene PR-Issues, null neue Violations, null neue duplizierte Zeilen und `0.0%` New-Code-Duplizierung; dies ersetzt den Secret-Scan-Fehler nicht. |

Die primäre Fehler-Receipt wurde um `2026-08-01T07:10:04Z` in
`/var/tmp/codex/ModSecurity-conector/worktrees/parent/20260730-ci-runtime-sonarqube-remediation`
beobachtet. Ihre Kommandos waren `gh run view 30689182074 --log-failed` und
ein checksum-pinned `gitleaks git --redact=100` Exact-Range-Scan; beide
lieferten Exit `1` für das redigierte Zwei-Treffer-Ergebnis.

## Root Cause und Remediation

Der ursprüngliche Task-Commit renderte einen opaken öffentlichen Sonar-Identifier
zusammenhängend in beiden Change-Record-Sprachen. Der Default-Gitleaks-
`generic-api-key`-Detector behandelt High-Entropy-Token-förmigen Text bewusst
konservativ. Die spätere strukturelle Reparatur macht den Final Tree sicher,
aber Gitleaks scannt historische Commits in der PR-Range und behält daher das
frühere Ergebnis.

Bevorzugte Remediation: separat einen Ersatz-Parent-PR vom aktuellen
`master` autorisieren, der den finalen geprüften Inhalt in einer frischen
Commit-Range enthält. Seinen Source-Diff, fokussierte Tests,
Gitleaks-PR-Range-Scan, GitHub-Checks und SonarQube-Cloud-Ergebnis prüfen;
PR #202 erst als abgelöst schließen, nachdem der Transfer verifiziert ist.

Alternative: das exakte Nicht-Credential-Restrisiko eines Merges von PR #202
mit seinem fehlgeschlagenen Non-Ruleset-Secret-Scanning-Ergebnis explizit
akzeptieren. Diese Formulierung, exakten Head, Run und Restrisiko vor der
Auflösung des aktuellen Konflikts und einer frischen finalen Integrationsrunde
aufzeichnen.

Keiner der Wege erlaubt eine Gitleaks-Regel-/Workflow-Änderung, Ignore,
Allow-List, False-Positive-Mutation, Force-Push, Rewrite veröffentlichter
Historie, Direkt-Push nach `master` oder Abschwächung eines Security-Controls.

## Akzeptanz, Validierung und Abhängigkeiten

- Kein echtes Credential wird aufbewahrt, ausgegeben, ignoriert,
  allow-listed oder fehlklassifiziert.
- Ein autorisierter Ersatzkandidat besteht den exakten Gitleaks-PR-Range-Scan
  und bewahrt das geprüfte Parent-Verhalten ohne History-Rewrite.
- Der exakte Kandidat hat terminale erforderliche GitHub-Checks und ein
  SonarQube-Cloud-Quality-Gate `OK` mit null OPEN/CONFIRMED-PR-Issues, null
  neuen duplizierten Zeilen und `0.0%` New-Code-Duplizierung.
- PR #202 darf nur nach Akzeptanz dieses exakten Restrisikos gemergt werden;
  andernfalls darf er nur geschlossen werden, nachdem ein verifizierter Ersatz
  den gewünschten Inhalt übertragen hat.

Regression-/Control-Checks sind der checksum-pinned redigierte Range-Scan und
die fokussierten Python-Tests für die übertragenen Parent-Änderungen. Das
legitime Control ist, dass der finale bilinguale Change Record opake
Identifier aus getrennten Fragmenten rekonstruiert, während der fail-closed
Secret-Scanning-Workflow aktiviert, redigiert und checksum-pinned bleibt.

- **Abhängigkeit:** aktuelle Benutzerentscheidung: Ersatz-Parent-PR
  autorisieren oder das exakte Nicht-Credential-Secret-Scanning-Risiko für
  PR #202 explizit akzeptieren.
- **Blocker:** veröffentlichte PR-Historie enthält den Detector-Match; Policy
  verbietet Force-Push, Rebase veröffentlichter Historie,
  Scanner-Abschwächung und Direkt-Push nach `master`.
- **Verwandt:** `FND-PARENT-0074` und `FND-SONAR-0016`.

## Restrisiko und Historie

Das Detector-Ergebnis belegt Token-förmigen historischen Text, kein Credential.
Ein Merge von PR #202 bei weiterhin fehlgeschlagenem Secret Scanning erfordert
eine aktuelle explizite Risikoakzeptanz. Ein Ersatz-PR erfordert separate
Benutzerautorisierung, weil die aktuelle Merge-Autorisierung PR #202 benennt.

- `2026-08-01T07:10:04Z` — Exact-Head-GitHub- und lokale Scans reproduzierten
  zwei redigierte generic-api-key-Heuristik-Ergebnisse. Der Final Tree ist
  strukturell repariert, aber der ursprüngliche veröffentlichte Commit bleibt
  in der gescannten Range.
