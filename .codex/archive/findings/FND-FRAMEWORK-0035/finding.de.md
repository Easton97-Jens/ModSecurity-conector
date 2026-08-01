# FND-FRAMEWORK-0035 — ModSecurity-v3-Objektmaterialisierung verwendet einen vorhersagbaren Archivpfad außerhalb ihrer privaten Staging-Grenze

## Identität

- Kategorie: `security_validated`
- Repository / Ownership: `framework` / `framework`
- Priorität / Schweregrad / Konfidenz: `P0` / `high` / `validated`
- Status / Machbarkeit: `fixed` / `feasible_now`
- Release-Blocker / sicherheitsrelevant: `true` / `true`
- Betroffene Revision: `784977615acfc55567e37b863309abc4a38ac877`
- Parent-Auswirkung: blockiert die legitime Runtime-Evidence-Voraussetzung für Parent PR #55; keine Parent-Gitlink-Änderung ist autorisiert.
- MRTS-Auswirkung: keine; MRTS bleibt strikt read-only.

## Zusammenfassung, Invariante und Auswirkung

Der isolierte Framework-Kandidat materialisiert freigegebene ModSecurity-v3-
Git-Objekte, schreibt sein Archiv zunächst aber unter dem vorhersagbaren
Pfadnamen `$parent/.modsecurity-v3-archive-$$.tar`. Er prüft diesen Pfadnamen
vor dem Archivbefehl und übergibt ihn später an `git archive --output`. Die
Invariante lautet, dass Archiv- und Extraktions-Zwischendateien nur innerhalb
der frischen privaten Materialisierungsgrenze geschrieben werden dürfen, selbst
wenn ein konkurrierender Akteur Einträge im konfigurierten Ziel-Parent erstellen
kann.

Eine task-eigene Real-Git-Regression erstellte nach der Prüfung des Helpers
einen Symlink für den bisherigen vorhersagbaren Archivpfad. Der Helper gab
`0` zurück, Git folgte jedoch der Ersetzung und erzeugte sein Archiv am
kontrollierten äußeren Ziel. Der Nachweis verwendet nur harmlose temporäre
Dateien und führt keine veränderte Datei aus. Ein Akteur, der sich den
Ziel-Parent teilt, kann einen Git-Archiv-Schreibvorgang auf ein anderes, für
die Framework-/CI-Identität beschreibbares Filesystem-Ziel umleiten; dies ist
ein Pfad-Containment-Defekt mit hoher Auswirkung in einer Supply-Chain-
Build-Input-Grenze.

## Betroffener Pfad, Source-to-Sink und Reproduktion

- `ci/lib/common.sh` — `ci_modsecurity_v3_materialize_git_tree` und
  `ci_materialize_approved_modsecurity_v3_source`.
- `tests/security_regression/test_modsecurity_v3_git_ref_provenance.py` —
  Real-Git-Ersetzungsregression.

Der kontrollierte Ziel-Parent liefert nach der `-e`/`-L`-Prüfung des Helpers
einen Eintrag. Der Helper ruft `ci_modsecurity_v3_git archive
--output=<predictable path>` auf, daher folgt Git dem ersetzten Symlink, bevor
`tar` das Archiv liest. Reproduziere mit einer lokalen harmlosen Git-Quelle und
dem fokussierten Test
`test_git_object_materialization_does_not_use_predictable_parent_archive_path`.
Vor der Remediation gibt der Helper `0` zurück, während das kontrollierte
äußere Archiv existiert.

## Retained Evidence

- Run-ID: `20260720T173133Z-pr55-runtime-remediation-7e38e876`
- Artefakt:
  `/var/tmp/codex/ModSecurity-conector/runs/20260720T173133Z-pr55-runtime-remediation-7e38e876/evidence/framework-modsecurity-v3-materialization-archive-race-reproduction.md`
- Typ: `task_owned_real_git_path_containment_reproduction`
- SHA-256: `2251b587118c6c1fbb6a291c9ba05eca0efc8c5076fb3cd21432ba881515f0aa`
- Befehl: RTK-umhüllter ausgewählter Framework-Unittest für
  `test_git_object_materialization_does_not_use_predictable_parent_archive_path`
- Working Directory:
  `/var/tmp/codex/ModSecurity-conector/runs/20260720T173133Z-pr55-runtime-remediation-7e38e876/tmp/framework-worktree`
- Exit-Code / beobachtet: `1` / `2026-07-20T19:54:45Z`
- Retention: `retained_task_evidence`

Post-Fix-retained Evidence:

- Run-ID: `20260720T201536Z-pr55-runtime-snapshot-revalidation-20f91607`
- Artefakt:
  `/var/tmp/codex/ModSecurity-conector/runs/20260720T201536Z-pr55-runtime-snapshot-revalidation-20f91607/evidence/framework-modsecurity-v3-provenance-remediation-postfix.md`
- Typ: `framework_postfix_security_validation_report`
- SHA-256: `b20ccffd871b9e4d821f5bdf08bb98061a0d7e6ed41a8921551b8fa2ec542aec`
- Befehl: RTK-umhüllte fokussierte Provenance-Suite, Kontrolle für
  öffentlichen Parent/leeren Platzhalter, Framework-Make-Provenance-Contract,
  Dokumentations-Checks und vollständiger Framework-Lint
- Working Directory:
  `/var/tmp/codex/ModSecurity-conector/runs/20260720T173133Z-pr55-runtime-remediation-7e38e876/tmp/framework-worktree`
- Exit-Code / beobachtet: `0` / `2026-07-20T21:07:10Z`
- Retention: `retained_task_evidence`

## Remediation, Validierung und Restrisiko

Der lokale Candidate erzeugt ein atomar angelegtes privates Staging-Verzeichnis
unter einem Parent, den er vor jeder Zielpfad-Mutation validiert, schreibt
Archiv und extrahierten Baum nur darin und veröffentlicht den fertigen Baum an
einem zuvor nicht existierenden Ziel ohne vorhersagbaren Archivnamen. Er weist
normale, symlinked oder vorbestehende Ziele ab, ausgenommen den expliziten
leeren Gitlink-Platzhalter; die Public-Parent-Kontrolle belegt, dass dieser bei
abgewiesenem Parent unberührt bleibt.

Akzeptanz erfordert: Die Ersetzungsregression lässt das äußere Ziel abwesend,
während der commitierte Snapshot am Ziel vorhanden ist; im vom Aufrufer
kontrollierten Parent wird kein vorhersagbarer Archivname verwendet;
Ziel-Symlink oder vorbestehendes Ziel schlägt fail-closed fehl; direkte,
Apache- und NGINX-legitime Snapshot-Kontrollen bestehen ohne `.git`; und
fokussierte Sicherheitsregressionen, komplette Provenance-Suite, Syntax, Make,
Dokumentation, Change Record, Lint, Retained-Source-Checks und ein unabhängiger
Bypass-Review bestehen vor Delivery.

Die Archive-Race-, Public-Parent-, Normal-/Symlink-Ziel-, leerer-Gitlink-
Platzhalter-, unveränderlicher-Snapshot-, Make-, Dokumentations- und
vollständigen-Lint-Kontrollen bestanden alle. Das unabhängige Review fand
keinen verbleibenden High- oder Critical-Blocker für das dokumentierte
Cross-UID-Lokal-Angreifer-Modell. Portable pfadbasierte Shell-Kontrollen können
einen konkurrierenden Schreiber mit derselben UID nicht isolieren; diese
Restrisiko-Grenze bleibt dokumentiert. Dieses Finding ist `fixed`, nicht
`verified`: Ein separater Framework-PR, Exact-Head-Checks/Review/Sonar-
Evidence, Framework-master-Verifikation und ein separat autorisiertes Parent-
Gitlink-Update bleiben erforderlich, bevor Parent-PR-#55-Runtime-Evidence
fortfahren kann. Es ist kein Duplikat von `FND-FRAMEWORK-0034`, das
veränderbare Source-Bytes besitzt; dieser Befund besitzt Output-Path-
Containment nach unveränderlicher Objektselektion.

## Verwandte Findings und Verlauf

- Verwandt: `FND-FRAMEWORK-0030`, `FND-FRAMEWORK-0032`,
  `FND-FRAMEWORK-0034` und `FND-CROSS-0001`.
- `2026-07-20T19:54:45Z`: in einer task-eigenen Real-Git-
  Ersetzungs-Fixture validiert; Kandidat-Delivery pausiert.
- `2026-07-20T21:20:47Z`: privates zufälliges Staging und private-Parent-
  Validierung vor Mutation bestanden alle lokalen Kontrollen; Status ist
  `fixed`, nicht `verified`, bis separater Framework-PR und Master-
  Verifikation vorliegen.
