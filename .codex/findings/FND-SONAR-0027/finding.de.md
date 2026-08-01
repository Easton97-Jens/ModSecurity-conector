# Finding FND-SONAR-0027: NGINX-Connector enthält sechzehn aktuelle SonarQube-Cloud-Maintainability-Befunde

**Sprache:** Deutsch | [English](finding.md)

## Klassifikation

| Feld | Wert |
| --- | --- |
| Kategorie | `maintainability` |
| Repository / Ownership | `parent` / `parent` |
| Priorität / Schwere / Konfidenz | `P2` / `not_applicable` / `confirmed` |
| Status / Machbarkeit | `verified` / `feasible_now` |
| Release-Blocker / Kandidat-Integrationsblocker / sicherheitsrelevant | nein / nein / ja |
| Sonar-Inventar | 3 × `c:S3776`, 1 × `c:S134`, 2 × `c:S3358`, 6 × `c:S1134`, 4 × `c:S1135` |

## Zusammenfassung, Verhalten und Auswirkung

Auf Parent-Master `caddd86d1eede95de53aa1bc971dd26d875df21c` besitzt das eingegrenzte `connectors/nginx/`-Inventar 16 offene C-Code-Smells, null Bugs, Vulnerabilities, Security-Hotspots und Duplikatzeilen. Die vier betroffenen Sources enthalten überkomplexe Lifecycle-Funktionen, verschachtelten Header-List-Control, verschachtelte Phase-4-Wertauswahl und nicht mehr umsetzbare Deferred-Work-Marker.

Dies ist keine belegte Security-Vulnerabilität, aber der Code verarbeitet HTTP-Request-, Response- und ModSecurity-Intervention-State. Die Remediation bewahrt Phase-Marker, Aufrufreihenfolge, Returns, Event-Reasons, Redirect-/Status-Verhalten, Cleanup und metadata-only-Logging. Exakte PR-Head-Security-, Hosted- und Sonar-Evidence verifizierte das Ergebnis vor dem autorisierten Squash-Merge; die Resulting-Master-Workflow-Evidence ist jetzt an die tatsächliche Merge-Revision gebunden.

## Scope, Remediation und Controls

- Scope sind die vier Parent-NGINX-C-Sources, ihr direkter Source-Contract-Check, zweisprachiger Change Record, gepaarte Indizes und lokale Finding-Evidence.
- Lifecycle-Funktionen zerlegen, verschachtelte Auswahl durch explizite Helper ersetzen, Header-Part-Advance explizit machen und stale Marker durch korrekte Lifecycle-Kommentare ersetzen.
- Keine Sonar-Regeln, Quality Gates, Exclusions, Suppressions, `NOSONAR`, Framework, MRTS, Gitlinks oder Security-Control ändern. Ein direkter Master-Change bleibt verboten; die einzige Master-Aktion war der separat autorisierte Squash-Merge dieses exakten PR.
- Erforderliche Controls sind NGINX-Common-Adoption, C-Standard-Wiring, C17-Lint, möglicher nativer C17-Compile, fokussierter Security-Diff-Review und Exact-Head-Hosted-Sonar-Verifikation.

## Aufbewahrte Evidence

Run-ID: `nginx-sonar-remediation-20260730`.

| Artefakt | SHA-256 | Ergebnis |
| --- | --- | --- |
| `evidence/sonar-nginx-initial.md` | `315a16d71c558cfa6a87d2a4917ae31e714751f50da308f65cff7b722c2546b6` | Exaktes 16-Key-Current-Master-NGINX-Inventar sowie null Directory-Bugs, Vulnerabilities, Hotspots und Duplikatzeilen. |
| `evidence/security-diff-review.md` | `f002a267559d7ad916e6e6e94ab6a08707f78944395aaa0df220b5fe3d16ce8c` | Fokussierter Security-Sensitive-Diff-Review fand keinen plausiblen neuen Kandidaten. |
| `evidence/sonar-pr206-final.md` | `0fbddb8d4f8514f5a71054705518acf1eb1943b92f0aa12e4d5102aeedb1f0c8` | Auf exaktem Draft-PR-#206-Head: Quality Gate `OK`, null OPEN/CONFIRMED-PR-Issues, null New-Code-Violations und `0.0%` / null New-Code-Duplikation. |
| `evidence/hosted-pr206-final.md` | `93805e39cb8561a732c73f0851b9173a7d8345706e7dea69f6bb54e80141db5e` | Exakter Head hat 33 bestandene, null fehlgeschlagene Hosted-Checks, null Reviews und null Review-Threads. |
| `evidence/pr-206-merge-and-master-validation-20260801.md` | `0ebea887fdd26634aede6b01e9785cc156419c72b71c385378ca1ba24870a948` | Finaler Head, geschütztes Squash-Ergebnis, 14 erfolgreiche Master-Workflows, getrennte Master-Sonar-Baseline und aufbewahrte Worktree-Disposition. |

Das Artefakt liegt unter `/var/tmp/codex/ModSecurity-conector/runs/nginx-sonar-remediation-20260730/`. Es enthält keine Credentials und ändert keinen SonarQube-Cloud-Status oder Control.

## Akzeptanz und Disposition

Alle Remediation-Akzeptanzkriterien sind auf [PR #206](https://github.com/Easton97-Jens/ModSecurity-conector/pull/206) mit finalem exaktem Head `eb1f199815b6ed3bc4ecd53bc3fd78a39629d198` verifiziert: alle 16 aufbewahrten Issue-Keys fehlen im PR-Readback; Quality Gate ist `OK`; null OPEN/CONFIRMED-PR-Issues, null New-Code-Violations und `0.0%` / null New-Code-Duplikation bleiben bestehen; direkte Source-Controls, fokussierter Security-Diff-Review und alle 34 Hosted-Checks bestehen. Es gibt keinen Review-Thread. GitHub squash-mergte diesen exakten PR am `2026-08-01T07:15:29Z` nach `master` auf `e870e8fbd1a31d43156d0baa79dc6d86b4e21bd3`; danach bestanden alle 14 anwendbaren Master-Workflows.

Lokale native C17-Translation-Unit-Compilation bleibt blockiert, weil task-lokale NGINX-/libmodsecurity-Header-Provisionierung keine verwendbaren Header herstellte. Kein fremder Cache und keine globale Installation werden als Ersatz verwendet. Dieser Task beansprucht keine Resulting-Master-NGINX-Runtime. Die exakte Resulting-Master-Sonar-Analyse bleibt nur wegen der unabhängig getrackten projektweiten `FND-SONAR-0001`-Baseline rot (New Security Rating `5`, Hotspot-Review `0%`); dies ist keine PR-#206-Regression, und es erfolgten keine externe Disposition, Suppression oder Risikoakzeptanz.

## Historie

- `2026-07-30T15:00:00Z`: Source-file-keyed Current-Master-Evidence bestätigte alle 16 in-Scope-Issues und allokierte das eigenständige Parent-NGINX-Remediation-Finding. Keine Scanner-Konfiguration, kein PR, Merge oder Master-Change erfolgte.
- `2026-07-30T15:55:23Z`: Draft-PR #206 exakter Head `9746d81cd73c54300d709357db453a93f4f358df` verifiziert: 33 bestandene / null fehlgeschlagene Hosted-Checks, null Reviews und Review-Threads, SonarQube-Cloud-Quality-Gate `OK`, null OPEN/CONFIRMED-PR-Issues, null New-Code-Violations und `0.0%` / null New-Code-Duplikation. Keine Master-Integration wurde autorisiert oder durchgeführt.
- `2026-08-01T07:15:29Z`: Nach finaler Exact-Head-Verifikation (`eb1f199815b6ed3bc4ecd53bc3fd78a39629d198`, 34 bestandene / null fehlgeschlagene Checks, keine Review-Threads, PR-Quality-Gate `OK`) erzeugte der nutzerautorisierte Squash-Merge Parent-Master `e870e8fbd1a31d43156d0baa79dc6d86b4e21bd3`. Alle 14 Master-Workflows bestanden. Die Analyse für diese exakte Master-Revision meldet weiterhin die bestehende `FND-SONAR-0001`-Quality-Gate-Baseline, keinen neuen PR-#206-Befund.
