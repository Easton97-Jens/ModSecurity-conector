# CR-20260819 — Präsenz optionaler CRS-Provenance-Exporte bewahren

**Sprache:** [English](CR-20260819-fnd-parent-0185-crs-provenance-exports.md) | Deutsch

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | CR-20260819-fnd-parent-0185-crs-provenance-exports |
| Datum (UTC) | 2026-08-19 |
| Basis-Revision | `0edc0dd24fcd16b5fec72c85a7a86e456babfd8b` |
| Finding | `FND-PARENT-0185` |
| Delivery-Branch | `agent/fix-fnd-parent-0185-crs-export` |
| Framework-Grenze | Gitlink `bd69ee96e0e7082317d4afe1232bee625665eb9a`; weder Source noch Gitlink geändert |
| Delivery-Disposition | PR #303: Geschützte Integration nach `master` am 2026-08-20 ausdrücklich autorisiert; Abschluss erfordert exakte Current-Head-Checks, einen exakten Head-gebundenen Merge und Post-Merge-Verifikation |

## Motivation und Problemstellung

Blieb eine aktive Provenance-Variable beim Aufrufer undefiniert, exportierte
Parent-`make` sie als explizit leere Umgebungsvariable. Das Framework wertet
dies korrekt als nicht-kanonischen Override-Versuch und stoppt vor den fünf
HAProxy-Fixture-Assertions. Dieselbe Präsenzabweichung betraf CRS-, NGINX-,
HAProxy-, HTTPD-, APR-, APR-util- und PCRE2-Pins.

## Akzeptanzkriterien

- Undefinierte optionale Eingaben bleiben an der Framework-Grenze abwesend.
- Explizit leere und veränderte CRS-Eingaben bleiben vor Seiteneffekten fail
  closed.
- Die fünf HAProxy-Tests erreichen ihre Assertions ohne Framework-, Gitlink-
  oder MRTS-Änderung.
- Exact-Head-Hosted-Actions und das unveränderte SonarQube-Cloud-Gate
  bestanden. Vor `verified` bleiben ein separat autorisierter Merge und eine
  Reproduktion auf dem resultierenden Master erforderlich.

## Implementierungsentscheidung und Begründung

Das `Makefile` verwendet jetzt eine zentrale bedingte Exportliste. Ein
optionaler Pin wird nur weitergereicht, wenn Make ihn erhalten hat; ein
explizit leerer oder veränderter Wert bleibt unverändert. Geprüfte
Framework-Defaults greifen daher nur bei wirklicher Abwesenheit, während die
bestehende Framework-Validierung explizit fehlerhafte Werte weiter ablehnt.

Die Parent-Tests prüfen diese Semantik für jedes Listenelement. Die HAProxy-
Fixtures tragen nun zudem den vom aktuellen Framework verlangten Binärdigest;
der Future-Pin-Test erwartet den vorgelagerten Inherited-Pin-Guard statt eines
späteren Runtime-Lock-Fehlers.

Der All-Active-Pin-Test liest das definierte APR-util-Tupel nur zur Testlaufzeit
aus dem sauberen Framework am exakten Gitlink. So wird Parent nicht zu einer
zweiten statischen Pin-Autorität, während die vollständige Defined-Value-
Coverage erhalten bleibt; APR-util-Scanner und seine Allowlist bleiben
unverändert.

## Security-Auswirkung

Die Reparatur entfernt nur versehentliche Leereinträge. Framework-Guard,
Origin-Validierung, CI-Kontrollen, Scanner und Quality Gate bleiben unverändert.

## Geänderte Dateien

- `Makefile` und die vier fokussierten Parent-Testmodule
- dieses gekoppelte Change-Record-Paar und sein zweisprachiger Archivindex

## Ausgeführte Befehle

- Fünf betroffene HAProxy-Tests bestanden direkt sowie über die Parent-Make-
  Grenze.
- `test_prepare_runtime_components` (41), `test_ci_security_workflows` (28),
  `test_all_connectors_no_crs_workflow_contract` (9) und
  `make check-ci-security-contract` (122; 5 erwartete Capability-Skips)
  bestanden.
- Veränderte und explizit leere `CRS_REPO_URL`-Controls wurden vor Build oder
  Download abgelehnt.
- Der abschließende unabhängige Security-Review fand keinen Bypass und kein
  reportable Issue.
- Die APR-util-Contracts im Hosted-Job-Umfang des Nachfolgers (22 Tests) und
  sein exakter Implementierungs-Head `5e9e69d9109d10650dc37e63b41af9372716658b`
  bestanden. SonarQube Cloud meldet `0,0 % Duplication on New Code` und 0
  neue Issues. Diese Dokumentationskorrektur unterliegt den exakten
  Current-Head-Checks des PR vor dem geschützten Merge.

## Runtime-Evidence

Der zurückgehaltene Receipt ist
`.codex/runs/20260819T230619Z-fix-fnd-parent-0185-crs-export/evidence/post-remediation-local-validation.md`
mit SHA-256 `bf6b0ba026a3135ea7ea4ee10cc977c46f1b63c1252997d694db3a25b6e74235`.
Der Exact-Head-Hosted-Receipt ist
`.codex/runs/20260819T230619Z-fix-fnd-parent-0185-crs-export/evidence/pr303-successor-exact-head-hosted-validation.md`
mit SHA-256 `3e224c6dbf68dfd9e687a1f4252e88b87ec84bc34cc18fd30ad1ae62cd84e7df`.

## Nicht ausgeführte Prüfungen mit Begründung

`make check-no-crs-source-normalization` erreichte die korrigierten Tests,
endet in diesem absichtlich nicht initialisierten Task-Worktree aber mit zwei
unabhängigen fest verdrahteten Catalog-Pfadfehlern. Das Initialisieren oder
Ändern des Framework-Moduls würde die vom Benutzer gesetzte Grenze verletzen;
die breitere Evidence muss daher auf Exact-Head-Hosted-Checks erfolgen.

## Bekannte Einschränkungen

Der isolierte Worktree hat absichtlich keinen initialisierten Framework-
Checkout; deshalb können seine zwei statischen Catalog-Pfad-Fälle lokal nicht
enden.

## Verbleibende Risiken

Der aktuelle Benutzer hat die geschützte Integration von PR #303 nach
`master` ausdrücklich autorisiert. `FND-PARENT-0185` kann erst nach exakten
Current-Head-Checks, einem exakten Head-gebundenen Merge ohne Bypass sowie
bestandenen resultierenden Master-Workflows und der ursprünglichen
Reproduktion fortschreiten.

## Finaler Diff- und Review-Status

Geändert sind ausschließlich Parent-`Makefile`, Parent-Tests und dieses
zweisprachige Traceability-Paar. Framework-Source, Gitlink und verschachteltes
MRTS bleiben unverändert. `FND-PARENT-0185` ist `fixed`, nicht `verified` oder
geschlossen. Implementierungs-Head `5e9e69d9109d10650dc37e63b41af9372716658b`
bestand die unveränderten GitHub-Actions- und SonarQube-Cloud-Gates. Der
aktuelle Benutzer hat den geschützten Merge von PR #303 autorisiert; dieser
Record hält diese Tatsache fest, kann den Merge jedoch nicht ausführen.
