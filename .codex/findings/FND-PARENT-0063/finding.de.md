# FND-PARENT-0063 — Normale Runtime-Provisionierung führt release-ausgewählten veränderlichen Upstream-Source aus

## Identität

| Feld | Wert |
| --- | --- |
| ID | `FND-PARENT-0063` |
| Kategorie | `security_validated` |
| Repository / Ownership | Parent / Parent |
| Priorität / Schweregrad / Konfidenz | P3 / low / validated |
| Status / Feasibility | `validated` / `requires_user_decision` |
| Release-Blocker / Security-relevant | false / true |

## Zusammenfassung

Der gewöhnliche nicht-strikte Komponenten-Producer akzeptiert den
veränderlichen Tag aus GitHub `releases/latest`, zeichnet eine Differenz zum
erwarteten Latest nur als Metadaten auf und baut danach den ausgewählten Source
auf einem vertrauenswürdigen Runner.

## Beobachtetes Verhalten und Source-to-Sink-Pfad

Auf Parent-master `8e8acb8dab1cd03723de269cab7da7dd62e5e010`
übergibt `prepare_release_git_component` den zur Laufzeit ermittelten
Latest-Release-Tag selbst bei `strict=True` direkt an
`prepare_git_component`. Eine Differenz zu `expected_prompt_latest` setzt
`release_tag_deviation`, blockiert aber nicht. Der betroffene
Entrypoint/Control ist
`ci/provisioning/components/prepare-runtime-components.py:1504-1579`; die
Sinks sind der Expat-Source-Build bei `:2709-2768` und der Go-Package-Build
bei `:4292-4312`.

Erwartetes Verhalten ist ein expliziter überprüfter unveränderlicher
Provenance-Vertrag vor Checkout und Build. Ein geändertes Latest-Release muss
fehlgeschlossen scheitern statt nur protokolliert zu werden.

## Impact, Voraussetzungen und Attack-Path-Scope

Ein Angreifer muss einen konfigurierten Upstream-GitHub-Release-Maintainer oder
dessen veränderlichen `releases/latest`-Zustand kompromittieren und dann einen
geplanten oder vertrauenswürdig manuellen
`make prepare-runtime-components`-Lauf abwarten. Das Repository-Threat-Model
umfasst ausdrücklich Imported-Upstream-Provenance und die CI-Supply-Chain.

Die überprüften Provisioner-Workflows sind geplant oder manuell, haben
`permissions: contents: read` und verwenden `persist-credentials: false`.
Es wurden kein `pull_request_target`, keine Secret-Referenz, kein schreibbares
Repository-Token und kein Production-/Deployment-Impact gefunden. Die starke
externe Voraussetzung und der begrenzte Runner-/Cache-/Netzwerk-Impact machen
dies zu einem reportable low/P3 Finding, nicht zu high oder critical.

## Evidence und Reproduktion

Run `sonar-652-duplication-zero-20260728-W8wqjk` hat eine Offline-Fixture
zurückgehalten:

```sh
rtk proxy env PYTHONDONTWRITEBYTECODE=1 PYTHONNOUSERSITE=1 .venv/bin/python -B \
  validation_artifacts/validate_mutable_release_execution.py \
  --repo-root /root/git/ModSecurity-conector \
  --artifact-root validation_artifacts
```

Sie bestand. Die Fixture übergab dem Production-Modul einen synthetischen
geänderten Tag, belegte dessen Übergabe mit `strict=True` an den Git-Preparer
und baute über den realen Build-Sink eine harmlose lokale Git-basierte
Go-Fixture zu einem Executable. Sie kontaktierte keinen Netzwerk-Endpunkt und
führte keinen Upstream-Source aus. Die Ergebnis-SHA-256 ist
`515ef4bcaa82ffd0bf33925cf5c3091c3050d76e4db51dc6637539abed50113d`.

Die Attack-Path-Report-SHA-256 ist
`cedea4cfe9d493d3cf6cc692f8112fd0ac2c91cffc6729eaefa1cb6193974d8f`.
Sie dokumentiert die In-Scope-Entscheidung, Counterevidence und die
low/P3-Kalibrierung.

## Root Cause und vorgeschlagene Remediation

`prepare_release_git_component` ist zur Kompatibilitätsverfolgung aktueller
GitHub-Releases entworfen. Es verwendet Latest-Release-Auswahl für Expat
außerhalb strikter Evidence-Läufe und für go-ftw/albedo erneut, während expected
latest eine Beobachtung statt einer Admission-Control ist.

Für jede release-ausgewählte Komponente muss ein unveränderlicher
Provenance-Vertrag ausgewählt und dokumentiert werden: überprüfter vollständiger
Git-Commit, verifizierter signierter Tag oder unveränderlicher
Source-Archive-Digest. Die Parent-Admission muss einen unerwarteten Latest-Tag
vor Checkout/Build ablehnen. Ein Framework-owned Default-Pin darf nur über
einen getrennt autorisierten Framework-PR geändert werden.

## Akzeptanzkriterien und Validierungsplan

1. Der ausgewählte unveränderliche Vertrag ist für Expat-Nicht-Strict-
   Kompatibilität, go-ftw und albedo explizit.
2. Eine Release-Tag-Differenz wird vor Checkout oder Source-Build abgelehnt.
3. Bestehende Safe-Cache-, URL-Allowlist-, Clean-Checkout-, Submodule- und
   `git fsck`-Controls bleiben erhalten.
4. Fokussierte Tests decken ein abgelehntes geändertes Latest-Release und einen
   legitimen genehmigten unveränderlichen Source ab.
5. Exact-Head-Hosted-Workflow- und SonarQube-Cloud-Nachweis bestehen ohne
   Abschwächung von Scanner-, Gate-, Permission- oder Provenance-Controls.

## Abhängigkeiten, Blocker, verwandte Findings und Restrisiko

Der ausgewählte unveränderliche Vertrag ist eine Entscheidung des aktuellen
Nutzers. Framework-Write-Scope ist für diese Task nicht ausgewählt, falls die
Default-Pins Framework gehören. Verwandte Records sind `FND-PARENT-0050`,
`FND-PARENT-0052` und `FND-SONAR-0016`. Dies ist kein Duplikat von
`FND-PARENT-0052`: Dieses besitzt den strikten Full-Evidence-Producer-
Expat-/Python-Vertrag, während dieses Finding normale Release-Tracking-
Provisionierung besitzt.

Bis zur Remediation kann ein kompromittierter Upstream-Release-Auswahlzustand
sein Source-Build-Verhalten in geplanter oder vertrauenswürdig manueller
Provisionierung ausführen lassen. Es wird kein Risiko akzeptiert.

## Historie

- `2026-07-28T10:16:00Z`: No-Network-Selector-/Build-Sink-Fixture bestand.
- `2026-07-28T10:20:00Z`: Attack-Path-Analyse bestätigte den In-Scope-Pfad
  und kalibrierte ihn als low/P3.
