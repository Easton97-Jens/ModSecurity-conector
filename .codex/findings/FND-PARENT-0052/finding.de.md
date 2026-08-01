# FND-PARENT-0052 — Full-Evidence-Producer akzeptiert veränderliche Supply-Chain-Eingaben

## Identität

| Feld | Wert |
| --- | --- |
| ID | `FND-PARENT-0052` |
| Kategorie | `dependency_risk` |
| Repository / Ownership | Parent / Parent |
| Priorität / Schweregrad / Konfidenz | P1 / medium / confirmed |
| Status | `fixed` |
| Release-Blocker | `true` |
| Security-relevant | `true` |

## Zusammenfassung

Der vorgeschlagene vollständige Verified-Report-Producer von PR #74 machte zwei
veränderliche externe Eingaben verpflichtend: Expat wurde über GitHubs
Latest-Release-Endpunkt aufgelöst und der Workflow verwendete einen Bootstrap,
der Pip aktualisiert und eine bereichsbasierte PyYAML-Abhängigkeit installiert.
Beide Eingaben können sich ändern, obwohl Parent- und Framework-Revision gleich
bleiben; die entstehende Runtime-Evidence wäre dann nicht reproduzierbar an
ihre Provenienz gebunden.

## Evidence und Source-to-Sink-Pfad

1. `.github/workflows/verified-report-governance.yml` ruft den
   strikten/vollständigen `make verified-report-run`-Producer auf.
2. `ci/runtime/lifecycle/run-verified-report-run.py` verlangt
   `make prepare-runtime-components`.
3. `ci/provisioning/components/prepare-runtime-components.py` verwendete für
   verpflichtendes Expat `prepare_release_git_component` und löste zur
   Laufzeit den aktuellen GitHub-Tag `releases/latest` vor dem Checkout auf.
4. Der vorgeschlagene Workflow rief zuvor `make setup-dev` auf; der
   Framework-Bootstrap aktualisiert Pip und installiert `requirements-dev.txt`
   mit bereichsbasierter PyYAML-Deklaration.

Das strikte Evidence-Gate bleibt selbst fehlgeschlossen; dieses Finding betrifft
die Vertrauenswürdigkeit der neu verpflichtenden Producer-Eingaben, nicht einen
Gate-Bypass.

## Remediation und Akzeptanzkriterien

- Der strikte Evidence-Expat-Pfad akzeptiert nur eine überprüfte vollständige
  unveränderliche Commit-ID, niemals Branch, Tag, abgekürzten SHA oder
  Latest-Release-Lookup, und verifiziert den aufgelösten Checkout dagegen. Der
  Nicht-Strict-Kompatibilitätspfad bleibt release-basiert und kann keine
  strikte Evidence erzeugen.
- Der Workflow liefert den überprüften Expat-Commit für das verifizierte
  Release `R_2_8_2` und zeichnet diese Konfiguration als exakte Workflow-
  Eingabe auf.
- Python-Werkzeuge des Producers werden mit dem ausgewählten Python,
  Framework-`requirements-ci.lock`, `--require-hashes` und `--only-binary`
  installiert; Pip wird nicht aktualisiert und `requirements-dev.txt` nicht
  konsumiert.
- Fokussierte Unit- und Workflow-Contract-Tests weisen veränderliche
  Expat-Refs und den früheren ungepinnten Bootstrap zurück.
- Ein frischer Exact-Head-Full-Runtime-Lauf und das terminale strikte Gate
  bestehen mit der daraus resultierenden revisionsgebundenen Evidence-Kette.

## Aktueller Status und Restrisiko

Die Parent-Source-Remediation ist implementiert und bestand fokussierte lokale
Kontrollen im isolierten PR-#74-Worktree: strikter Expat-Dispatch,
Mutable-Ref-Ablehnung, Checkout-Head-Mismatch-Ablehnung, Nicht-Strict-
Kompatibilität, Workflow-/Tool-Vertrag, bilinguale Dokumentation und
Whitespace-Validierung. Seit der Entdeckung wurden weder Branch noch
geschützter Merge veröffentlicht. Der Full-Runtime-Producer und beide PR-
Integrationen bleiben bis zur Exact-Head-Hosted-Validierung blockiert. Es wird
kein Risiko akzeptiert.

## Historie

- `2026-07-26T06:32:35Z`: Ein unabhängiges Security-Review validierte die veränderlichen
  Expat- und Python-Bootstrap-Eingaben im neu aktivierten Full-Producer. Der
  geplante Push wurde vor der Veröffentlichung ausgesetzt; das strikte Gate
  wurde nicht abgeschwächt.
- `2026-07-26T06:44:31Z`: Die Parent-only-Strict-Path-Remediation und die
  fokussierte Validierung bestanden. Das retained Validierungsartefakt
  dokumentiert Befehle und Ergebnisse; gehostete Full-Evidence steht weiter
  aus.
