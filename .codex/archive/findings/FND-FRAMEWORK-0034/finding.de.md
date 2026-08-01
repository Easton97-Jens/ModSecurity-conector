# Finding: ModSecurity-v3-Validator kann durch Git-Index-Flags versteckte veränderliche getrackte Source-Bytes akzeptieren

**Sprache:** [English](finding.md) | Deutsch

| Feld | Wert |
| --- | --- |
| ID | FND-FRAMEWORK-0034 |
| Kategorie | security_validated |
| Repository / Ownership | framework / framework |
| Priorität / Schwere / Konfidenz | P0 / high / validated |
| Status / Feasibility | fixed / feasible_now |
| Release-Blocker / sicherheitsrelevant | ja / ja |
| Betroffene Revision | 784977615acfc55567e37b863309abc4a38ac877 |
| Source-Runs | 20260720T173133Z-pr55-runtime-remediation-7e38e876; 20260720T201536Z-pr55-runtime-snapshot-revalidation-20f91607 |

## Zusammenfassung und Sicherheitsinvariante

Ein vorhandenes `MODSECURITY_V3_SOURCE_DIR` darf nur die geprüften gepinnten
Source-Bytes liefern, wenn ein Framework-Build später seine Inputs kopiert und
ausführt. Ein Clean-Status darf keine geänderte getrackte Datei verbergen, und
der validierte Pfad darf nach der Validierung nicht als veränderlicher Build-
Input kopiert werden.

## Beobachtetes und erwartetes Verhalten

Vor der Remediation akzeptierte `ci_modsecurity_v3_require_clean_checkout` ein
leeres `git status --porcelain` als Nachweis, dass die Source der gepinnten
Git-Identität entspricht. Eine task-eigene Real-Git-Fixture commitete
`build.sh` mit `approved-source`, markierte sie mit
`git update-index --assume-unchanged` und änderte sie zu
`unapproved-source`. Status war leer, `git ls-files -v` gab kleingeschriebenes
`h build.sh` aus, und der Helper gab trotzdem `0` zurück. Die direkten,
Apache- und NGINX-Consumer kopieren und führen anschließend das veränderliche
`MODSECURITY_V3_SOURCE_DIR` aus.

Die Kontrolle muss `assume-unchanged`- und `skip-worktree`-Index-Zustand vor
jeder Build-Aktion abweisen. Sie muss Root- und statische geprüfte Child-Trees
aus ihren exakten gepinnten Git-Objekten in das task-eigene Ziel
materialisieren, statt den gelieferten Worktree zu kopieren. Das eliminiert
auch das verwandte Validation-to-Copy-Replacement-Intervall.

## Auswirkung und Voraussetzungen

Ein Akteur, der einen vorhandenen Source-Checkout und dessen lokalen Index
bereitstellen oder verändern kann, kann beliebige Build-Inputs wie `build.sh`,
`configure` oder ein `Makefile` trotz gepinnter Root-/Child-Commits mit der
Framework-Build- oder CI-Identität kopieren und ausführen lassen. Dies ist ein
Supply-Chain-Provenance-Bypass mit hoher Auswirkung.

Der Pfad verlangt ein akzeptiertes vorhandenes `MODSECURITY_V3_SOURCE_DIR`,
einen gepinnten Origin/HEAD/Topologie-Eindruck und entweder eine geänderte
getrackte Datei mit unsicherem Index-Bit oder das Ersetzen des gelieferten
Source-Pfads nach der Validierung.

## Betroffene Dateien und Symbole

- `ci/lib/common.sh`: `ci_modsecurity_v3_require_clean_checkout`,
  `ci_require_approved_modsecurity_v3_checkout`,
  `ci_modsecurity_v3_materialize_git_tree` und
  `ci_materialize_approved_modsecurity_v3_source`.
- `ci/provisioning/build-v3-under-src.sh`,
  `ci/provisioning/prepare-apache-build.sh` und
  `ci/provisioning/prepare-nginx-build.sh`: Build-Consumer für vorhandene
  Checkouts.
- `tests/security_regression/git_provenance_test_support.py` und
  `tests/security_regression/test_modsecurity_v3_git_ref_provenance.py`.
- `docs/connector-integration.md` und `docs/connector-integration.de.md`.

## Reproduktion und Evidenz

1. Ein task-eigenes wegwerfbares Git-Repository mit commiteter `build.sh` mit
   `approved-source` erstellen.
2. `git update-index --assume-unchanged build.sh` ausführen und sie danach zu
   `unapproved-source` ändern.
3. Leere Ausgabe von `git status --porcelain=v1 --untracked-files=all
   --ignore-submodules=none` und `h build.sh` von `git ls-files -v` beobachten.
4. Die isolierte Candidate-`ci/lib/common.sh` sourcen und
   `ci_modsecurity_v3_require_clean_checkout` aufrufen; vor dem Fix gibt sie
   `0` zurück, obwohl `HEAD` und Worktree-Bytes abweichen.

| Run | Artefakt | SHA-256 | Ergebnis |
| --- | --- | --- | --- |
| 20260720T173133Z-pr55-runtime-remediation-7e38e876 | `/var/tmp/codex/ModSecurity-conector/runs/20260720T173133Z-pr55-runtime-remediation-7e38e876/evidence/framework-modsecurity-v3-assume-unchanged-reproduction.md` | `1327e5e8d8e4afc92c160f408acf45db59adc15f6ab66a2706501fb1714602b6` | RTK-umhüllte Real-Git-Reproduktion endete mit 0 und bewies die Pre-Fix-Akzeptanz versteckter Bytes. |
| 20260720T201536Z-pr55-runtime-snapshot-revalidation-20f91607 | `/var/tmp/codex/ModSecurity-conector/runs/20260720T201536Z-pr55-runtime-snapshot-revalidation-20f91607/evidence/framework-modsecurity-v3-provenance-remediation-postfix.md` | `b20ccffd871b9e4d821f5bdf08bb98061a0d7e6ed41a8921551b8fa2ec542aec` | Post-Fix-fokussierte Suite 24/24, Make-Contract, vollständiger Lint, Objekt-Snapshot-Kontrolle und unabhängiges Review bestanden; kein High-/Critical-Cross-UID-Blocker blieb. |

Keine geänderte Fixture-Datei wurde ausgeführt. Kein Parent-Checkout,
offizieller Framework-Checkout, Remote-Service oder MRTS-Pfad wurde geändert
oder aufgerufen.

## Root Cause und Remediation

Normaler Status sowie Index-/Gitlink-Identität galten als Proxy für alle
konsumierten Worktree-Bytes. Git-Index-Flags schwächen diesen Proxy; danach
kopierten die Consumer den validierten Pfad. Der lokale Candidate weist jetzt
nicht normale Index-Flags ab und ersetzt jede ausführbare `cp -a`-Source-Kopie
durch objektbasierte Materialisierung über den gehärteten Git-Wrapper und
`tar`. Er archiviert den geprüften Root und jeden statischen geprüften
Child-Commit in ein privates task-eigenes Ziel, weist eingebettete `.git`-
Metadaten ab und prüft den Ziel-Parent vor jeder Zielpfad-Mutation.

## Akzeptanzkriterien und Validierung

1. Ein kleingeschriebenes `assume-unchanged`- oder `skip-worktree`-Index-Bit
   führt vor einer Build-Aktion zu `77`.
2. Direkte, Apache- und NGINX-Consumer verwenden für ausführbare Build-Inputs
   kein `cp -a` auf `MODSECURITY_V3_SOURCE_DIR`.
3. Root und statische geprüfte Children werden über `ci_modsecurity_v3_git`
   aus exakten gepinnten Objekten materialisiert und enthalten keine `.git`-
   Metadaten.
4. Eine Real-Git-Fixture mit `unapproved-source` im Worktree erzeugt einen
   `approved-source`-Objekt-Snapshot.
5. Der saubere exakte Acht-Child-Control, fokussierte Security-Regressionen,
   Syntax, Dokumentation, Change Record, Make, Lint und unabhängiger
   Bypass-Review bestehen.

Die geplanten Prüfungen sind die beiden Real-Git-Regressionen, die vollständige
hermetische Provenance-Suite, `make test-modsecurity-v3-provenance-contract`,
Syntax, Dokumentations-/Change-Record-Validierung, Lint und ein
Change-aware-Review von Index-Flags, Archive-Coverage, Extraktion,
Source-Replacement und den vorhandenen Local-Git-Kontrollen.

Alle genannten lokalen Kontrollen bestanden: Die fokussierte Suite bestand
24/24, der Make-Contract 24/24, die CI-Root-Bootstrap-Suite 6/6, der Objekt-
Snapshot enthielt 5.532 Dateien ohne `.git` und ohne Gruppen-/Andere-
Berechtigungen, und der vollständige Framework-Lint bestand. Das unabhängige
Review fand keinen verbleibenden High- oder Critical-Blocker für das
dokumentierte Cross-UID-Lokal-Angreifer-Modell.

## Abhängigkeiten, verwandte Findings und Restrisiko

Dieses Finding hängt von derselben isolierten Framework-Umgebung wie
`FND-FRAMEWORK-0030` und `FND-FRAMEWORK-0032` ab; es ist kein Duplikat davon.
`FND-FRAMEWORK-0030` besitzt den Recursive-Topology-Availability-Defekt und
`FND-FRAMEWORK-0032` die Ausführung lokaler Git-Konfiguration bzw.
schreibgeschützte Metadatenmutation. `FND-CROSS-0001` bleibt der separate
Parent-Runtime-Evidence-Blocker.

Die direkte Race ist Source-to-Sink-validiert, aber nicht dynamisch geraced.
Das Object-Snapshot-Design entfernt die Abhängigkeit von Worktree-Bytes nach
der Validierung. Portable pfadbasierte Shell-Kontrollen können einen
konkurrierenden Schreiber mit derselben UID nicht isolieren; diese
Restrisiko-Grenze ist dokumentiert. Dieses Finding ist `fixed`, nicht
`verified`: Ein separater Framework-PR, Exact-Head-Checks/Review/Sonar-
Evidence, Framework-master-Verifikation und ein separat autorisiertes Parent-
Gitlink-Update bleiben erforderlich, bevor Parent-PR-#55-Runtime-Evidence
fortfahren kann. Es gab keine Framework-master-, Parent-Gitlink- oder MRTS-
Aktion.

## Historie

| UTC | Ereignis | Detail |
| --- | --- | --- |
| 2026-07-20T19:12:35Z | validated_task_owned_real_git_assume_unchanged_reproduction | Leerer Status plus `h build.sh` ließ geänderte Bytes durch den Pre-Fix-Clean-Check; Source-to-Sink-Review bestätigte spätere Copy-and-Execute-Consumer. |
| 2026-07-20T19:12:35Z | deduplicated_and_started_framework_remediation | Als P0/high/validated, in_progress, feasible_now klassifiziert; getrennt von FND-FRAMEWORK-0030 und FND-FRAMEWORK-0032. |
| 2026-07-20T21:20:47Z | local_remediation_fixed_pending_framework_delivery | Index-Flags werden abgewiesen und direkte/Apache-/NGINX-Consumer materialisieren gepinnte Objekte. Fokussierte-/Make-/Lint-/Dokumentations-/Snapshot-Kontrollen und unabhängiges Review bestanden; Status ist fixed, nicht verified, weil kein Framework-PR oder keine Master-Verifikation existiert. |
