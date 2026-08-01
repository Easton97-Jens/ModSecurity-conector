# FND-FRAMEWORK-0015 — OSV-Evidence-Validierung verlangte keine vollständige Schwachstellengruppen-Abdeckung

## Identität

| Feld | Wert |
| --- | --- |
| ID | `FND-FRAMEWORK-0015` |
| Kategorie | `evidence_gap` |
| Repository / Ownership | `framework` / `framework` |
| Priorität / Schwere | `P2` / `not_applicable` |
| Confidence / Status | `validated` / `fixed` |
| Machbarkeit | `blocked_external_dependency` |
| Release-Blocker | `false` |
| Security-relevant | `true` |

## Zusammenfassung

OSV-Vergleichs-Evidence konnte strukturell gültiges JSON sein und trotzdem
Schwachstellen-IDs auslassen, duplizieren oder inkonsistent gruppieren.

## Evidence und Remediation

OSV-Report-Schema und Comparator scheitern jetzt fail-closed bei fehlerhaften
Reports, unvollständigen oder überlappenden Gruppen, doppelten IDs sowie nicht
vertrauenswürdigen oder verlinkten Evidence-Pfaden. Alias-Enrichment bleibt
eine legitime nicht-neue Gruppe. Die Remediation steht in
`768a06b5b734547f8213cc6918c26ef4a8ef9f67`; der exakte lokale HEAD bestand 64
CI-Security-Tests und `make lint`. Aufbewahrte Artefakt-SHA-256:
`979715e7ec9a24e700f04ab6722b5f717b1f229023a6c4de6051c675a79155c5`.

Auf dem exakten Framework-PR-#50-Head
`b0f3e745075d57ee727bdfcd61f6258d488d4dc1` erreichte der gehostete OSV-
`pull-request-head`-Job seinen begrenzten Base/Head-Vergleich, aber der OSV-
Scanner meldete beim Auflösen des unveränderten Trusted-Base-Manifests
`service unavailable`. Der Job endete mit `127`, bevor vertrauenswürdige
Vergleichs-Evidenz entstand. Das ist ein externer Verifikationsblocker und
keine Evidenz für eine Regression der reparierten Schema-/Comparator-Kontrolle;
der fail-closed-Workflow wurde nicht geschwächt. Beleg:
[Run 30204914941, Job 89801198064](https://github.com/Easton97-Jens/ModSecurity-test-Framework/actions/runs/30204914941/job/89801198064).

## Akzeptanzkriterien

- Jede berichtete Schwachstellen-ID gehört genau zu einer validierten Gruppe.
- Reines Alias-Enrichment erzeugt keine falsche neue Gruppe.
- Fehlerhafte, unvollständige, überlappende, übergroße oder nicht
  vertrauenswürdige Evidence schlägt fehl.
- Exakte Final-PR-Head-OSV-CI bestätigt die committete Kontrolle.

## Restrisiko und Historie

Die lokale Remediation bleibt behoben, aber die Remote-Exact-Head-OSV-
Verifikation ist `blocked_external_dependency`, bis der Scanner-Service wieder
verfügbar ist und ein frischer PR-#50-Run besteht. `2026-07-18T15:18:00Z`:
erstellt und lokal repariert. `2026-07-26T13:52:18Z`: externer Service blockiert
den exakten PR-#50-OSV-Run.
