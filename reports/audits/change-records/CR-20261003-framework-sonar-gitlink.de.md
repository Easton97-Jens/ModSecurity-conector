# Change Record: validierter Framework-Wartbarkeits-Gitlink

**Sprache:** [English](CR-20261003-framework-sonar-gitlink.md) | Deutsch

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | `CR-20261003-framework-sonar-gitlink` |
| Datum (UTC) | `2026-10-03` |
| Basis-Revision | `209e6f003282695e62876332a4b916eb3e170969` |

Delivery: Draft-PR #396.
Framework: `b9b9534b7e0b15edad31393699ebd0617748148d` →
`dd4af7d24b0ae90f8fa81513e5c9c290d40847f3`, separat in Framework-PR #135 geliefert.
MRTS bleibt `615b13bacbd008562c17408246c41ab27dca3104`.

## Motivation und Problemstellung

Der Benutzer wählte zusätzlich die 28 echten Framework-Sonar-Findings und ein
separates Parent-Pointer-Update. Dies repariert nicht historische Parent-PR
#135: Deren aktuelle Report-Helper-Linie hat keinen beobachteten Sonar-Defekt.

## Akzeptanzkriterien

Den veröffentlichten sauberen exakten Framework-Commit nach Erfolg aller sechs
SHA-gebundenen Workflows nutzen. Neue Sonar-Analyse muss ohne Suppression
bestehen; alle 28 ursprünglichen Issue-IDs müssen CLOSED/FIXED sein. Parent-
Source, Required-Selection-/Evidence-Verträge, Protocol-Trennung und MRTS erhalten.

## Implementierungsentscheidung und Begründung

Nur Gitlink und gepaarte Integrations-Traceability/Index ändern. Der Helper-only
Framework-Vertrag verlangt keine Parent-Dispatch-/API-Änderung. Frame-Source
und Tests gehören zu separaten Commits; siehe dessen Record
`20261003-02-no-crs-sonar-maintainability`. Bestehende unabhängige With-CRS-
Profilpins unverändert lassen; ihre frühere Abweichung ist kein neu durch die
Wartbarkeit verursachter Wiring-Defekt. Retained-Runtime-Daten nicht umetikettieren.

## Security-Auswirkung

Kein Validator, Containment, Receipt-Identität, Descriptor-Autorität,
Event-Anforderung oder Statusvorrang wird gelockert. Kein neuer Runtime-Claim.
Protected-Dispatcher-/Builder-/Launcher-/Collector-Source bleibt unverändert.

## Geänderte Dateien

`modules/ModSecurity-test-Framework`, dieses EN/DE-Record-Paar und sein EN/DE-Index.
Keine Connector-/Common-C-, Parent-Runtime-Script-, Protocol-Test- oder MRTS-Änderung.

## Ausgeführte Befehle

Artefaktreferenzen mit Präfix `analysis/` beziehen sich unten auf den freigegebenen
externen Run-Root `/var/tmp/codex/ModSecurity-conector`, niemals auf den Checkout.

Parent-Baseline-Fokus: 31 Tests PASS, keine Skips, Exit 0, mit zwei Trusted-
Framework-API-Aufrufen. Exakter Befehl und Log stehen extern in
`analysis/framework-pr135-sonar-plan.md` und
`analysis/framework-pr135-parent-pointer-baseline-focus.log` / `.exit`.
Derselbe Fokus muss vor Push gegen den neu committeten Parent-Gitlink laufen.
Native `rtk proxy make check-bilingual-docs check-doc-links` und
`rtk proxy git diff --check` sind Precommit-Dokumentations-/Diff-Gates.

Separat bestand natives Framework-Lint; Postcommit No-CRS/API bestand 166 + 23
Tests; endliche Baseline-Parität bestand 2.081 Vergleiche. Remote-Framework-
Workflows bestanden 6/6. Sonar-Analyse `2026-10-03T14:09:15+0000` am exakten dd4
meldet Quality Gate OK, 0 offene Issues, 0 Hotspots, Duplikation 0.0% und
28/28 ursprüngliche Issue-IDs CLOSED/FIXED. Dies sind keine Parent-Runtime-Nachweise.

## Runtime-Evidence

Kein manueller Lifecycle, Requests, neue Canonical-Runtime-Evidence oder Full E2E.
Collector-Source-Commit bleibt `209e6f003282695e62876332a4b916eb3e170969`.

## Nicht ausgeführte Prüfungen mit Begründung

Neue Parent-Head-CI/Sonar und Coverage-Neuberechnung warten auf Veröffentlichung.
Kein vollständiger Connector-Build oder E2E ist in diesem Schritt freigegeben.

## Bekannte Einschränkungen

Erhaltene Source-Parität erfüllt keine fehlenden Required-Runtime-Cases.
Alte Zahlen sind keine frische Coverage.

## Verbleibende Risiken

Aktuelle Parent-CI/Sonar muss vor
Neuberechnung und MIME-Arbeit bestehen. Beide PRs bleiben Draft; kein Merge ist erlaubt.

## Finaler Diff- und Review-Status

Fünf-Pfad-Diff, exakten Gitlink, unveränderte Producer-/Dispatch-Bytes und
separaten Protocol-Worktree prüfen. Postcommit-Parent-Kompatibilität und neue
Remote-Head-Verifikation bleiben erforderlich. Keine Secrets oder Rohlogs hier.
