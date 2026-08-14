# FND-PARENT-0129 — Gepatchter Lighttpd-Core-Build benötigt automatischen Autotools-Bootstrap, wenn dem verifizierten 1.4.84-Release configure fehlt

| Feld | Wert |
| --- | --- |
| ID / Source-Input | `FND-PARENT-0129` / `F-GS-002` |
| Kategorie | `build_defect` |
| Repository / Ownership | `parent` / `parent` |
| Priorität / Severity | `P1` / `not_applicable` |
| Confidence / Status | `confirmed` / `fixed` |
| Machbarkeit | `feasible_now` |
| Release-Blocker / Candidate-Integration-Blocker | ja / nein |
| Security-relevant | ja; Source-/Bootstrap-Ausführungsgrenze, kein Exploit behauptet |

## Zusammenfassung

Das offizielle Lighttpd-`1.4.84`-XZ-Archiv wurde ausschließlich vom
autorisierten offiziellen Release-Host bezogen, gegen den gepinnten SHA-256
`076dd43bec8f2ba9ce6db7e7ca7e8ad72271cd529805ead2400b56efaa026f70`
verifiziert, sicher entpackt und über den geforderten absoluten
`LIGHTTPD_SOURCE_DIR` verwendet. Sein Originaltree enthielt kein ausführbares
`configure`.

Der reparierte Parent-Builder kopierte und patchte diesen Originaltree nur in
einen disponierbaren externen Arbeitsbereich, führte dort Upstream-`autogen.sh`
aus, prüfte das erzeugte ausführbare `configure`, baute gepatchten Core und
Host und bestand den Host-Contract. Ein zweiter Aufruf desselben Build-Roots
gab `mode=reused` aus, ließ Hash und mtime von `autogen.log` unverändert und
führte keinen zweiten Bootstrap aus. Die Originalsource-Manifeste vor und nach
beiden Fresh-/Reuse-Paaren sind byteidentisch. Das Finding ist daher
`fixed`; es ist noch nicht `verified` oder `closed`, weil diese Status die
autorisierte Delivery und Post-Merge-Master-Evidence erfordern.

## Beobachtetes und erwartetes Verhalten

Der unveränderliche Analysis-only-Record
`.codex/analysis/general-state/20260814T083829Z-ea3b48a/findings/F-GS-002/`
zeichnet den ursprünglichen Defekt auf: Einer frischen gepatchten Kopie von
verifiziertem Lighttpd `1.4.84` fehlte ausführbares `configure`, sodass der
frühere Builder vor der Konfiguration stoppte. Die aufbewahrte Beobachtung
zeigte auch, dass ein task-lokaler Upstream-Bootstrap den anschließenden realen
Core- und Host-Build ermöglichte.

Nach Source-/Patch-Verifikation muss der Builder vorhandenes ausführbares
`configure` weiterverwenden; andernfalls muss er `autogen.sh` nur in der
gepatchten Source-Kopie ausführen und ausführbares erzeugtes `configure`
verlangen, bevor Core-Output existiert. Fehlendes `autogen.sh`, ein nicht
unterstützter nicht ausführbarer Interpreter, ein Bootstrap-Fehler oder
fehlendes/nicht ausführbares erzeugtes `configure` müssen den nativen
präzisen Exit-`77`-Fehlerpfad beibehalten.

## Nachweise für reale Source und Integrität

| Control | Ergebnis |
| --- | --- |
| Archividentität | Offizieller XZ-SHA-256 und Größe bestanden: `076dd43…26f70`, `895228` Bytes. |
| Source-Identität | `configure.ac` enthält `AC_INIT([lighttpd],[1.4.84]`; `autogen.sh`, `Makefile.am` und `src/` sind vorhanden. |
| Fresh-Zustand | Original-`configure` war vor dem Build nicht vorhanden/nicht ausführbar. |
| Patch-Identität | `e9bad85fe2f740350e090947f1dcebd2d7111c76b6914f80328ae49d1aad106d`. |
| Originalsource-Manifest | Vorher-, Nachher- und finales Nachher-SHA-256 sind jeweils `65da21d0e8e18198fd84f7deb6d014bd6c4cb582869318d0e9e13fc7144566fb`; beide `cmp`-Checks Exit `0`. |
| Fresh Core/Host/Contract | Bestanden mit Exit `0`, einschließlich Wiederholung im Netzwerk-Namespace. |
| Reuse | Bestanden mit Exit `0`; Core gab `mode=reused` aus. |
| Kein zweiter Bootstrap | `autogen.log` SHA-256 `60040f093546e8d3d754b4a6fb3ab962abba12031cad677fa603c0e0635b48f6`, Größe `916` und mtime `1786717176` blieben über Reuse unverändert. |

Die vollständige Evidence mit exakten Pfaden, Befehlen, Exit-Codes, begrenzten
Logreferenzen und der Trennung von Archiv- und Tree-Hashes befindet sich im
[Validation-Receipt](../../runs/20260814T115110Z-f-gs-002-autogen-bootstrap/evidence/validation.md).

## Security-Invariante und Implementierung

Die sicherheitsrelevante Grenze ist Upstream-Bootstrap-Ausführung aus einem
aufruferkontrollierten Source-Pfad. Die bewahrte Invariante lautet: Nur eine
bereits verifizierte Lighttpd-`1.4.84`-Source wird zu einer gepatchten
disponierbaren Kopie; Bootstrap darf nur dort laufen, Fehler bleiben sichtbar,
und ausführbares `configure` ist vor dem Core-Build zwingend. Die
Originalsource bleibt unverändert; es wurden keine Paketinstallation, kein
chmod, keine Hash-Abschwächung und keine Netzbeschaffung hinzugefügt.

Die realen Fresh- und Reuse-Targets liefen im netzlosen Namespace. Das
Upstream-Skript schrieb unter `/bin/sh` `trap: ERR: bad trap`, gab aber
`0` zurück, erzeugte `configure` und schloss den realen Core-/Host-Pfad ab;
das rechtfertigt keine weitere Änderung der Bootstrap-Logik.

## Betroffene Dateien und Symbole

- `connectors/lighttpd/build/build_patched_core.sh`: `run_autogen`,
  `ensure_configure` und `verify_core`.
- `connectors/lighttpd/tests/test_patched_host_contract.py`: fokussierte
  Bootstrap-, Fehler- und Reuse-Controls.
- `scripts/generate_compiler_guides.py` sowie generierte Lighttpd-EN/DE-Guides.
- `tests/test_compiler_guides.py`: generierte Guide-Regression-Controls.

## Akzeptanzkriterien und Validierung

1. Vorhandenes ausführbares `configure` überspringt Bootstrap.
2. Fehlendes `configure` bootstrappt nur die gepatchte Kopie und erzeugt
   ausführbares `configure`.
3. Fehlendes Skript, nicht unterstützter Interpreter, Bootstrap-Fehler und
   fehlendes Output stoppen fail closed vor Core-Output.
4. Fresh verifizierte Source Core/Host/Contract und Same-Root-Reuse bestehen.
5. Die Originalsource bleibt unverändert und Reuse führt `autogen.sh` nicht erneut aus.
6. Fokussierte Contract-, Guide-, Syntax-, JSON- und relevante Dokumentations-Controls bestehen.

Beobachtete lokale Ergebnisse:

- `sh -n connectors/lighttpd/build/build_patched_core.sh`: bestanden.
- `shellcheck -s sh connectors/lighttpd/build/build_patched_core.sh`: bestanden.
- `python3 connectors/lighttpd/tests/test_patched_host_contract.py`: 26 Tests bestanden.
- Vier ausgewählte Lighttpd-Guide-Idempotenz-/EN-DE-/Shell-/Parity-Controls: bestanden.
- `make check-compiler-guides`: 21 Tests bestanden.
- Die beiden Lighttpd-Guide-Links bestanden im sauberen PR-Worktree.
- `make check-bilingual-docs` und `make check-doc-links` bestanden im
  bestehenden Checkout mit vorhandenem Framework-Gitlink. Dieselben generischen
  Targets sind im sauberen PR-Worktree umgebungsbedingt blockiert, weil sein
  Gitlink bewusst nicht initialisiert ist; die Fehler betreffen Root-/Example-
  Framework-Links, nicht diese Lighttpd-Änderung.
- Relevantes JSON-Parsing und `git diff --check` bestanden.

## Abhängigkeiten, Blocker und Restrisiko

Der frühere externe Source-Blocker ist aufgelöst. Kein F-GS-002-
Akzeptanzkriterium bleibt blockiert. Der generische ignorierte Backlog-/Roadmap-
Korpus gehört nicht zur PR-Baseline und wurde nicht force-added, weil dadurch
unrelated Findings importiert würden.

Das Restrisiko betrifft nur den Lifecycle: Das Finding bleibt `fixed`, nicht
`verified` oder `closed`, bis der aktuelle PR-Head gemergt, das exakte
`origin/master`-Ergebnis und die erforderlichen Workflows geprüft und die
ursprüngliche Reproduktion oder das stärkste Äquivalent auf Master wiederholt
wurde. Keine Traefik-, Framework- oder MRTS-Datei wurde geändert.

## Historie

- `2026-08-14T11:58:05Z`: Die enge Bootstrap-Entscheidung in der gepatchten
  Kopie, sechs Real-Skript-Szenarien und generierte bilinguale Guide-Updates wurden implementiert.
- `2026-08-14T12:15:11Z`: Explizite Controls für nicht ausführbares
  `configure` und einen nicht unterstützten Interpreter kamen hinzu; 26
  fokussierte Tests, Shell-Syntax und ShellCheck bestanden.
- `2026-08-14T14:23:16Z`: Offizielle Archiv-/Source-Identität,
  Originalsource-Integrität, realer Fresh Core/Host/Contract und Same-Root-
  No-Network-Reuse ohne zweiten Bootstrap wurden verifiziert; Status auf
  `fixed` gesetzt.
- `2026-08-14T15:08:19Z`: Das erforderliche gepaarte Change Record und die
  Archivindex-Einträge wurden ergänzt; das Receipt zeichnet nun die strikten
  Change-Record-Dokumentationschecks einschließlich der temporären Overlay-
  Pässe ohne Parent-, Framework- oder MRTS-Source-Änderungen auf.
- `2026-08-14T15:17:30Z`: Die Change-Record-Formulierung wurde auf die
  tatsächliche Vorher-/Nachher-/Final-Manifest-Evidence eingegrenzt und beide
  Standard-Dokumentationsziele in einem frisch erzeugten task-eigenen Overlay
  wiederholt; beide bestanden, danach wurde die Kopie ohne Source-Änderungen
  entfernt.
