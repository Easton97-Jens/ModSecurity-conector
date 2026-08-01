# FND-PARENT-0051 — CPython-3.14-Testloader registriert das lokale Runtime-Smoke-Modul vor der Dataclass-Verarbeitung nicht

## Identität

| Feld | Wert |
| --- | --- |
| ID | FND-PARENT-0051 |
| Kategorie | test_failure |
| Repository / Ownership | Parent / parent |
| Priorität / Schwere / Vertrauen | P1 / not_applicable / reproduced |
| Status / Machbarkeit | fixed / feasible_now |
| Release-Blocker / sicherheitsrelevant | true / false |
| Profil | Parent PR #74 normal master update unter CPython 3.14.4 |
| Connector / Protokoll | lokaler Runtime-Smoke-Harness / Python-importlib-Testladen |
| MRTS-Auswirkung | keine; unverändert |

## Zusammenfassung, Beobachtung und Auswirkung

Während der Aktualisierung von Parent PR #74 durch einen normalen
Non-Fast-Forward-Merge des aktuellen Parent-master schlug die fokussierte
CPython-3.14.4-Testsuite fehl, bevor ihre Request-Body-Assertions liefen.
`tests/test_local_runtime_smoke_request_body.py` erzeugt `SMOKE` aus einer
importlib-Spezifikation und ruft unmittelbar `exec_module` auf. Das Modul wird
zuvor nicht unter `SPEC.name` in `sys.modules` registriert.

Der importierte Smoke-Runner enthält nun die `RuntimeOutputPaths`-`@dataclass`
aus aktuellem master. Die Dataclass-Verarbeitung von CPython 3.14.4 sucht daher
die Modulregistrierung und löst `AttributeError` aus, weil sie fehlt. Der
Fehler ist ein Testloader-Kompatibilitätsdefekt, kein nachgewiesener produktiver
Bypass des Request-Body-Parsers, der Autorisierung oder der Pfad-Einengung. Er
blockiert die fokussierte Evidenz des ausgewählten PR bis zur Korrektur.

## Reproduktion und Evidenz

Die Parent-virtuelle Umgebung mit CPython 3.14.4 wird im isolierten PR-#74-
Worktree mit dem aufgezeichneten fokussierten unittest-Befehl verwendet. Er
endet mit Exit `1` beim Laden von `test_local_runtime_smoke_request_body.py`;
der aufbewahrte Trace endet in `dataclasses._is_type` und
`sys.modules.get(cls.__module__)`.

Der aufbewahrte Beleg ist
`.codex/runs/20260726T000000Z-pr55-pr74-python314-import/evidence/python314-import-loader-failure.md`
mit SHA-256
`75c710e45b9db641bb82a4ef5b39ca088e0f35daf1ea5a0cb9f8a31852b0da2b`.
Er enthält auch den legitimen Direktimport-Kontrollfall: Die Registrierung des
Moduls unter seinem Spec-Namen vor `exec_module` endet mit Exit `0` und
importiert `RuntimeOutputPaths` erfolgreich.

## Ursache und Korrektur

Dem Test fehlt der übliche importlib-Modulregistrierungsschritt. Dieses
Versäumnis war vor der Dataclass-Deklaration des Runners latent und wird von
der Klassenverarbeitung in CPython 3.14.4 sichtbar.

`import sys` ergänzen und unmittelbar vor `SPEC.loader.exec_module(SMOKE)`
`sys.modules[SPEC.name] = SMOKE` setzen. Die Dataclass darf nicht entfernt,
die Request-Body-Kontrollen nicht gelockert und die Einengung verifizierter
Runtime-Ausgabepfade nicht abgeschwächt werden.

## Akzeptanz und Validierung

1. Der Test registriert `SMOKE` vor der Ausführung exakt unter `SPEC.name`.
2. `tests.test_local_runtime_smoke_request_body` besteht unter CPython 3.14.4.
3. Die ausgewählten Request-Body-, Runtime-Pfad-, Evidenz-, HAProxy-,
   Workflow-, Dokumentations-, Compiler-Guide-, Makefile- und C-Timeout-Checks
   bestehen auf demselben Kandidaten-Head.
4. Ein frischer Exact-Head-PR-Zyklus wird nach dem Veröffentlichen geprüft; er
   ist keine Master-Integrationsautorisierung.

Die legitimen Kontrollen behalten die Akzeptanz gültiger Request-Bodies, die
Ablehnung ungültiger Framing-/Größenwerte und die Ablehnung von Symlink- oder
Out-of-Root-Runtime-Ausgabepfaden bei.

## Abhängigkeiten, Restrisiko und Historie

Diese Parent-only-Korrektur hängt vom normalen PR-#74-Update-Branch ab. Sie
erfordert oder autorisiert keine Framework-, MRTS-, Gitlink-, Branch-Cleanup-
oder Master-Aktion. Sie steht nur zum separaten Python-3.14-Workflow-Contract-
Befund FND-PARENT-0046 in Beziehung; die technischen Ursachen sind verschieden.

Die fokussierte lokale Korrektur ist nun vorhanden und wiederholt: Das
ursprüngliche Request-Body-Modul besteht 10 Tests und die fokussierte #74-Suite
besteht 143 Tests unter CPython 3.14.4. Der Datensatz bleibt `fixed`, nicht
`verified`, bis der aktualisierte Exact-PR-Head frische GitHub- und SonarQube-
Cloud-Evidenz besitzt. Kein Sicherheitscontrol und kein Risiko wird aufgegeben.

- 2026-07-26T05:30:02Z — Auf dem PR-#74-Merge-Kandidaten reproduziert und mit
  einem erfolgreichen registrierten Import-Kontrollfall aufgezeichnet. Bei der
  Erstellung des Belegs wurden keine Produkt-, Framework-, MRTS-, Git-,
  GitHub- oder Gitlink-Änderungen vorgenommen.
- 2026-07-26T05:30:02Z — Die einzeilige Modulregistrierung vor der Ausführung
  ergänzt. Das ursprüngliche CPython-3.14.4-Request-Body-Modul (10 Tests) und
  die fokussierte PR-#74-Suite (143 Tests) bestanden. Frische Exact-Head-
  CI-/Sonar-Verifikation bleibt ausstehend; keine Master-Integration behauptet.
