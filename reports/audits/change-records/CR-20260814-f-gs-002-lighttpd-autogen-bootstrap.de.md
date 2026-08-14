# Change Record: F-GS-002 Lighttpd-configure-Bootstrap-Validierung

**Sprache:** [English](CR-20260814-f-gs-002-lighttpd-autogen-bootstrap.md) | Deutsch

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | CR-20260814-f-gs-002-lighttpd-autogen-bootstrap |
| Datum (UTC) | 2026-08-14 |
| Basis-Revision | `ea3b48abab7940de49997a371f9117b409c05a2a` |
| Delivery-Status | Pre-Merge-Follow-up für Parent-PR [#285](https://github.com/Easton97-Jens/ModSecurity-conector/pull/285). Sein erster validierter Evidence-Head war `62e226bd016c01231d6cbb7da6bb8f552441f7ab`; dieser erforderliche Record erzeugt einen neuen Candidate-Head, daher müssen seine geschützten Checks und die Review-Runde vor jedem Merge wiederholt werden. Hier wird kein Merge behauptet. |

## Motivation und Problemstellung

Der verifizierte Lighttpd-1.4.84-Release-Quellbaum kann berechtigterweise kein
generiertes `configure` enthalten. Der gepatchte Core-Builder scheiterte zuvor
vor dem realen Core- und Host-Build in diesem Zustand, obwohl der Release das
Upstream-`autogen.sh` und seine Autotools-Eingabedateien bereitstellt.
F-GS-002 / FND-PARENT-0129 verfolgt diesen reproduzierbaren Build-Blocker.

## Akzeptanzkriterien

- Ein vorhandenes ausführbares `configure` ohne Bootstrap wiederverwenden.
- Andernfalls Upstream-`autogen.sh` nur in der disponierbaren gepatchten
  externen Quellkopie ausführen, seinen Fehlerstatus erhalten und ein
  ausführbares Ergebnis verlangen.
- Den offiziellen Release `lighttpd-1.4.84.tar.xz` vor der Nutzung mit dem
  gepinnten SHA-256 `076dd43bec8f2ba9ce6db7e7ca7e8ad72271cd529805ead2400b56efaa026f70`
  und der offiziellen Prüfsummenzeile verifizieren.
- Fresh-Core-, gepatchten Host- und Same-Root-Reuse-Build ohne Netzwerkzugriff
  nachweisen und belegen, dass Reuse `autogen.sh` nicht erneut ausführt.
- Nachweisen, dass der originale verifizierte Quellbaum vor, während und nach
  den Builds unverändert bleibt; FND-PARENT-0129 erst nach diesen Gates auf
  `fixed` setzen.

## Implementierungsentscheidung und Begründung

`build_patched_core.sh` behält den Fast Path für ausführbares `configure`.
Wenn es fehlt oder nicht ausführbar ist, akzeptiert `ensure_configure` ein
ausführbares `autogen.sh` oder ein nicht ausführbares Skript mit exakt
`#!/bin/sh` oder `#!/usr/bin/env sh`; es führt den gewählten Upstream-Einstieg
in `PATCHED_SOURCE_DIR` aus. Das begrenzte `autogen.log` erhält Diagnosen. Ein
nicht erfolgreicher Bootstrap, ein nicht unterstütztes nicht ausführbares
Skript oder ein fehlendes ausführbares erzeugtes `configure` scheitern mit der
bestehenden Blocked-Exit-Semantik fehlgeschlossen.

Die Implementierung verändert niemals den bereitgestellten Originalbaum. Das
Repository kopiert ihn in einen verwalteten externen gepatchten Baum, wendet
dort den gepinnten Connector-Patch an und bootstrapt nur diese Kopie. Die reale
Quellenbeschaffung verwendete ausschließlich das autorisierte offizielle Archiv
und die Prüfsumme; Quellpfad und vollständiges Befehlsinventar liegen im
Validation-Receipt. Es wurde kein Paket installiert und während der realen
Validierung keine Bootstrap-Logik geändert.

Der ignorierte lokale `.codex`-Backlog-/Roadmap-Korpus wurde nicht per Force
hinzugefügt: Das würde hunderte nicht zusammenhängende lokale Control-Plane-
Einträge importieren. Die kanonischen FND-EN/DE/JSON-Datensätze und ihr
retained Receipt sind die begrenzte versionierte Evidenz für diesen Fix; die
Einschränkung ist explizit statt verborgen.

## Security-Auswirkung

Die Änderung berührt eine Build-Skript-Ausführungsgrenze. Ihre
Sicherheitsinvariante ist, dass nur ein zuvor verifizierter Lighttpd-1.4.84-
Baum in den externen gepatchten Arbeitsbereich kopiert wird und nur diese Kopie
`autogen.sh` ausführen darf. No-follow-Manifeste des Originalbaums vor und nach
den Builds waren identisch. Bootstrap-Fehler werden nicht unterdrückt, es wird
weder ein Paket noch ein Netzwerkschritt hinzugefügt, und ein ausführbares
erzeugtes `configure` ist vor Konfiguration und Kompilierung erforderlich.
Dies ist die Behebung eines Build-/Lifecycle-Defekts, keine behauptete
Sicherheitslücke oder Runtime-Exploit-Behebung.

## Geänderte Dateien

- `connectors/lighttpd/build/build_patched_core.sh`
- `connectors/lighttpd/tests/test_patched_host_contract.py`
- `scripts/generate_compiler_guides.py`
- `tests/test_compiler_guides.py`
- `docs/build/compilers/lighttpd.md`
- `docs/build/compilers/lighttpd.de.md`
- `.codex/findings/FND-PARENT-0129/finding.json`
- `.codex/findings/FND-PARENT-0129/finding.md`
- `.codex/findings/FND-PARENT-0129/finding.de.md`
- `.codex/runs/20260814T115110Z-f-gs-002-autogen-bootstrap/evidence/validation.md`
- dieses englische/deutsche Change-Record-Paar und seine englischen/deutschen
  Archivindex-Einträge.

Enthalten sind keine Traefik-, Framework-, MRTS- oder Gitlink-Änderungen,
Archive, Binärdateien, Buildprodukte, Caches oder Zugangsdaten.

## Ausgeführte Befehle

- Das offizielle Archiv und die Prüfsumme wurden mit den vom Benutzer
  autorisierten fehlgeschlossenen HTTPS-`curl`-Befehlen beschafft; die exakten
  Aufrufe und Exit-Codes liegen im Validation-Receipt.
- Fresh und Reuse verwendeten `env LIGHTTPD_SOURCE_DIR="$LIGHTTPD_SOURCE_DIR" make -C connectors/lighttpd check-lighttpd-patched-host` mit den aufgezeichneten externen Build-Roots und ModSecurity-Include-/Library-Pfaden.
- Netzwerkisolierte Fresh- und Reuse-Läufe wiederholten diesen Befehl mit
  `unshare --net -- env` und denselben aufgezeichneten Eingaben.
- Fokussierte Prüfungen verwendeten `sh -n connectors/lighttpd/build/build_patched_core.sh`,
  `shellcheck -s sh connectors/lighttpd/build/build_patched_core.sh`,
  `python3 connectors/lighttpd/tests/test_patched_host_contract.py` und die
  aufgezeichneten fokussierten `CompilerGuideGenerationTest`-Kontrollen.
- Dokumentations- und finale Konsistenzprüfungen verwendeten
  `make check-compiler-guides`, `make check-bilingual-docs`,
  `make check-doc-links`, relevante JSON-Prüfungen und `git diff --check`.

## Tests und tatsächliche Ergebnisse

Das vollständige Befehlsinventar, Arbeitsverzeichnisse, Umgebungswerte,
Exit-Codes, begrenzte Logauszüge und Quellmanifest-Dateien liegen in
`.codex/runs/20260814T115110Z-f-gs-002-autogen-bootstrap/evidence/validation.md`.
Beobachtet wurden:

| Prüfung | Tatsächliches Ergebnis |
| --- | --- |
| Beschaffung von offiziellem Archiv und Prüfsumme | bestanden; XZ-Größe `895228`; erwarteter und tatsächlicher SHA-256 stimmten als `076dd43bec8f2ba9ce6db7e7ca7e8ad72271cd529805ead2400b56efaa026f70` überein |
| Archiv-/Member- und Quellidentitätsprüfungen | bestanden; sicheres 361-Member-Archiv; `AC_INIT([lighttpd],[1.4.84]`; originales `configure` fehlte |
| Fresh `make -C connectors/lighttpd check-lighttpd-patched-host` | bestanden, Exit 0; Patch, Bootstrap, Core, Host, Config-Check und Host-Contract bestanden |
| Same-Root-Reuse-Befehl | bestanden, Exit 0; `mode=reused`; Hash, Größe und Zeitstempel von `autogen.log` unverändert |
| Fresh und Reuse unter `unshare --net` | beide bestanden, Exit 0; kein Netzwerkinterface verfügbar |
| Erhalt der Originalquelle | bestanden; Vorher-/Nachher-/Final-Manifeste haben SHA-256 `65da21d0e8e18198fd84f7deb6d014bd6c4cb582869318d0e9e13fc7144566fb`, 361 Einträge und byteweises `cmp` mit Exit 0 |
| `sh -n connectors/lighttpd/build/build_patched_core.sh` | bestanden, Exit 0 |
| `shellcheck -s sh connectors/lighttpd/build/build_patched_core.sh` | bestanden, Exit 0 |
| `python3 connectors/lighttpd/tests/test_patched_host_contract.py` | bestanden, 26 Tests, Exit 0 |
| Vier fokussierte `CompilerGuideGenerationTest`-Kontrollen | bestanden, Exit 0 |
| `make check-compiler-guides` | bestanden, 21 Tests, Exit 0 |
| Fokussierte Lighttpd-Guide-/Link- und relevante JSON-Kontrollen | bestanden, Exit 0 |
| `git diff --check` | bestanden, Exit 0 |

## Runtime-Evidence

Die Fresh- und Reuse-Läufe sind reale Build-Evidenz für Core und den gepatchten
Host einschließlich des Repository-Host-Contracts. Sie beanspruchen keinen
Live-HTTP-Verkehr oder einen Production-Service-Runtime-Lauf.

## Nicht ausgeführte Prüfungen mit Begründung

Optionale GPG-Verifikation lief nicht, weil kein bereits vertrauenswürdiger
Upstream-Schlüsselfingerprint verfügbar war; der gepinnte Archivdigest und die
offizielle Prüfsummenzeile bleiben die Pflichtverifikation. Im sauberen
Task-Worktree endeten `make check-bilingual-docs` und `make check-doc-links`
nur mit Exit 2, weil sein absichtlich nicht initialisierter Framework-Gitlink
fehlte. Dieselben Ziele bestanden read-only im bestehenden Parent-Checkout mit
diesem Gitlink. Es wurde keine Framework-Aktion ausgeführt.

## Bekannte Einschränkungen

Das Upstream-`autogen.sh` gab unter der System-POSIX-Shell `trap: ERR: bad trap`
aus und endete danach erfolgreich; das resultierende `configure`, Core, Host
und die Contract-Prüfungen bestanden. Dies bleibt als begrenzte Upstream-
Diagnose-Evidenz erhalten und wird nicht als reine Erfolgslog maskiert.

FND-PARENT-0129 ist `fixed`, nicht `verified` oder `closed`. Die Post-Merge-
Verifikation muss die gemergte `master`-SHA bestätigen und die stärkste
angemessene Reproduktion erneut ausführen, bevor der spätere Lifecycle-
Übergang erfolgt.

## Verbleibende Risiken

`autogen.sh` bleibt Upstream-definierte Codeausführung, ebenso wie der
anschließende bestehende `configure`-/`make`-Pfad. Die Kontrolle besteht aus
Quellenprovenienz, exakter Archivverifikation, External-Copy-Isolation,
fehlgeschlossenen Ergebnisprüfungen und dem Originalquellen-Erhaltnachweis;
sie ersetzt keinen Aufrufer, der die verifizierte Quellenbereitstellung
umgeht.

## Finaler Diff- und Review-Status

Die erste vollständige Finalprüfung fand PR #285 offen, Ready, mergebar, sauber
und gegen `master` gerichtet; seine Required Checks `actions`,
`bounded-c-cpp`, `envoy-go`, `traefik-go`, `actionlint` und `zizmor` bestanden
für `62e226bd016c01231d6cbb7da6bb8f552441f7ab`. SonarCloud bestand; keine
Freigaben waren erforderlich; es gab keine Reviews, Inline-Kommentare oder
Review-Threads. Die Repository-Einstellungen erlauben nur Squash. Dieser
erforderliche Record ändert den PR-Head, daher sind diese Fakten nur
Pre-Follow-up-Evidenz. Vor der Auslieferung sind eine neue Exact-Head-Check-,
Review-, Base-Freshness- und geschützte Squash-Merge-Runde erforderlich.
