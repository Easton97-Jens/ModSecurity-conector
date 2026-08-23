# Change Record

**Sprache:** [English](CR-20260822-trusted-lighttpd-namespace-dispatch.md) | Deutsch

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | CR-20260822-trusted-lighttpd-namespace-dispatch |
| Datum (UTC) | 2026-08-22 |
| Basis-Revision | `423abcc130cf5d29ccf15dd7d82e4e7d89d495d3` |
| Delivery-Status | Separater Protected-master-Dispatcher-Reparatur-Pull-Request; reguläres Master-Refresh und manuelle Integration sind autorisiert, während Exact-Head-Validierung, Integration und erfolgreicher Trusted-Runtime-Lauf bei diesem Record-Update noch ausstehen. |

## Motivation und Problemstellung

Die Lighttpd-Reparatur der Same-UID-TOCTOU benötigt einen realen
unprivilegierten User-/Mount-/PID-Namespace-Runtime-Test. GitHub-hosted
Pull-Request-Runner brechen korrekt fail-closed ab, wenn Ubuntus
AppArmor-User-Namespace-Beschränkung diesen Test verhindert. `sudo` oder ein
AppArmor-Setup im Pull-Request-Workflow wären unsicher, weil das Workflow-YAML
vom PR geliefert wird.

Dieser separate, manuell ausgelöste Workflow muss zuerst nach geschütztes
`master` geprüft und gemergt werden. Er stellt das kurzlebige Ubuntu-24.04-
Setup bereit, ohne einem PR-kontrollierten Workflow einen privilegierten Schritt
zu geben.

## 2026-08-22 Master-Integrationsautorisierung

Der aktuelle Benutzer autorisierte ausdrücklich nur PR #320, auf den aktuellen
`master` gebracht und integriert zu werden. Das Branch-Refresh verwendet einen
normalen Merge des aktuellen `origin/master`; es autorisiert keinen Rebase,
Force-Push, direkten Push nach `master`, Auto-Merge, Schutz-Bypass, PR-#309-
Merge, Framework-/MRTS-Änderung oder Gitlink-Update. Ein manueller
repository-konventioneller Merge bleibt von frischen Exact-Head-Checks,
SonarQube Cloud und dem geschützten Ruleset abhängig.

## Akzeptanzkriterien

- Der Dispatcher besitzt nur `workflow_dispatch`, genau eine `target`-Eingabe,
  ein Protected-`master`-/kanonisches-Repository-Gate und ein exaktes
  Owner-Maintainer-Actor-Gate.
- Der PR-Code-Testjob besitzt nur `contents: read`; ein separater Job ohne
  Checkout besitzt nur `statuses: write`, erhält weder PR-Source noch Artefakt
  und kann ausschließlich den festen Status
  `trusted-lighttpd-namespace` für den API-gebundenen Ziel-SHA schreiben.
- Feste Systemschritte vor dem Checkout installieren nur feste Pakete, laden
  das feste AppArmor-User-Namespace-Profil, erzeugen `ns-test` und prüfen
  Binary-, Gruppen-, Docker-Socket- und Capability-Voraussetzungen.
- Die API-Auflösung akzeptiert eine offene kanonische PR-Nummer oder deren
  exakten 40-stelligen kleingeschriebenen Head-SHA; der eingeschränkte Prozess
  materialisiert ausschließlich diesen aufgelösten SHA vom festen öffentlichen
  HTTPS-Origin.
- Git-Credentials und `.git` werden vor der Source-Ausführung entfernt. Source
  läuft nur als `ns-test`, mit `NoNewPrivs`, leeren Gruppen/Capabilities,
  `env -i`, privatem `0700`-Temp-Root und fail-closed Namespace-Probes.

## Implementierungsentscheidung und Begründung

`run-trusted-lighttpd-namespace-dispatch.yml` ist ein
Protected-default-branch-Control-Plane-Workflow und kein Pull-Request-Trigger.
Er verlangt sowohl `github.actor == 'Easton97-Jens'` als auch
`github.triggering_actor == 'Easton97-Jens'`; dadurch kann diese erste Version
nur der kanonische Repository-Owner manuell auslösen oder erneut ausführen. Das Hinzufügen eines
weiteren Maintainers benötigt eine separat geprüfte Protected-master-
Allowlist-Änderung.

Vor der Source-Materialisierung prüfen feste absolute root-eigene Binaries, installieren nur
`apparmor-utils`, `bubblewrap` und `jq`, bestätigen die erforderlichen
Bubblewrap-Flags, belassen `kernel.apparmor_restrict_unprivileged_userns` auf
`1` und laden dieses feste root-eigene Profil:

~~~text
profile trusted-lighttpd-ci-userns flags=(unconfined) {
  userns,
}
~~~

Es ergänzt keine AppArmor-Capability-, Mount-, Ptrace-, Network-,
Wildcard-Datei- oder Profilübergangsregel und ändert keinen globalen Sysctl.
Es wird nicht als Sandbox dargestellt; die tatsächliche Grenze sind die frische
`ns-test`-Identität, `NoNewPrivs`, Null-Capability-Sets, bereinigte Umgebung,
unzugänglicher Docker-Socket und die verschachtelten privaten Namespace-/
Bubblewrap-Probes.

Die frühere Behauptung `aa-status --profiled | grep <Profil>` wurde entfernt:
Unter Ubuntu 24.04 gibt `--profiled` eine Anzahl geladener Profile und nicht
deren Namen aus. Unmittelbar nach `apparmor_parser --replace` betritt ein
festes root-eigenes `aa-exec` das Profil `trusted-lighttpd-ci-userns` und prüft
`/proc/self/attr/current`. Ein anderes oder fehlendes Profil beendet den Job
vor der Source-Materialisierung mit `77`. Der statische Vertrag verbietet die alte
zählbasierte Form und mutiert den aktiven Profilnachweis, die Reporter-Isolation
und das Privilegieninventar.

## 2026-08-23 Reparatur der eingeschränkten Preflight-Diagnose

Der erste Protected-master-Dispatch nach der anfänglichen Korrektur band den
exakten PR-#309-SHA und schloss Bootstrap, Checkout und Git-State-Entfernung
ab, beendete sich aber nach 42 ms in einem unmarkierten Prädikat innerhalb des
nach Privilegienabgabe laufenden `aa-exec -> setpriv -> env -i`-Prozesses.
Diese Beobachtung beweist keinen Lighttpd-Runtime-Fehler und rechtfertigt
keinen Fallback.

Der reparierte Protected-Workflow führt denselben vollständig eingeschränkten
Launcher vor dem Checkout aus, ohne einen Checkout- oder PR-abgeleiteten Pfad
zu verwenden. Er prüft reale und effektive UID/GID, leere Zusatzgruppen,
`NoNewPrivs`, alle fünf Capability-Sets, das aktive AppArmor-Profil,
Unzugänglichkeit des Docker-Sockets sowie die User-/Mount-/PID- und
Bubblewrap-Namespace-Probes. Jeder Voraussetzungsfehler wird in ein festes
Label `BLOCKED: preflight.<reason>` ohne Helper-Stderr oder PR-Daten umgesetzt.
Der Launcher nach dem Checkout behält dieselben Kontrollen und gibt für seine
Setup- und Namespace-Prädikate korrespondierende Labels
`BLOCKED: runtime.<reason>` aus; der tatsächliche Python-Unittest bleibt
unmaskiert, damit ein echter Fixture-Fehler sichtbar bleibt. Beide
Namespace-Probes bleiben fail-closed und besitzen weder einen Root-,
Container- noch einen Out-of-Namespace-Fallback.

Dieses Record-Update dokumentiert ausschließlich eine Diagnose- und
Kontrolläquivalenz-Reparatur. Es behauptet keinen erfolgreichen Trusted-
Runtime-Lauf; diese Evidence muss aus einem frischen `master`-Dispatch gegen
den dann aktuellen exakten PR-#309-Head stammen.

Der vertrauenswürdige Source-Pfad lautet:

~~~text
manual target -> strict format validation -> fixed public GitHub API request
-> one open canonical PR/head SHA -> aa-exec -> setpriv -> env -i
-> fixed HTTPS exact-SHA materialization -> verify -> remove .git
-> ns-test namespace test
~~~

Kein roher oder nicht validierter PR-abgeleiteter Text, Pfad, Ref, URL oder
Shell-Syntax gelangt in einen privilegierten Befehl; ausschließlich der bereits
API-gebundene exakte SHA wird als validiertes Datum übergeben. Der rohe Input
ist niemals ein Checkout-Ref. Die PR-Source wird erst nach dem Identity-Drop
direkt materialisiert. Die entsorgbare GitHub-hosted-VM besitzt abschließend
Account-/Profil-/Temp-Teardown; bewusst gibt es nach gelaufenem PR-Code kein
root-seitiges rekursives Löschen eines von `ns-test` beschreibbaren Baums.

Das Pre-Checkout-Bootstrap erzeugt seinen Run-State ausschließlich unter dem
vorab geprüften root-eigenen, nicht beschreibbaren `/var/lib`-Parent. Es nutzt
bewusst nicht `/var/tmp`, dessen Standardmodus `1777` sowohl mit der
Trusted-Directory-Invariante unvereinbar ist als auch keinen geeigneten Parent
für einen privilegierten Runtime-Root bildet. Der Dispatcher prüft den exakten
root-eigenen `0755`-State-Root sowie die exakten Non-root-`source`- und
privaten `0700`-Temp-Children vor Checkout oder PR-Code-Ausführung.

Der Testjob exponiert ausschließlich sein API-validiertes `target_sha`-Output.
Eine frische GitHub-hosted-Reporter-VM läuft danach ohne Checkout, lokale
Action, Cache, Artefakt, `sudo` oder PR-Code-Ausführung. Sie validiert den
kleingeschriebenen 40-stelligen SHA erneut, ordnet nur das Ergebnis des
Trusted-Tests einem festen Wert `success`/`failure`/`error` zu und schreibt den
festen Statuskontext `trusted-lighttpd-namespace`. Das Status-Token existiert
nur in diesem Reporter; der Testjob erhält es niemals.

## 2026-08-23 Direkte eingeschränkte Source-Materialisierungs- und Mount-Lifecycle-Reparatur

Run `32614114266` bewies den vollständigen privilegierten Bootstrap, die API-
Bindung, exakte Zielvalidierung, die Identitätsgrenze
`aa-exec -> setpriv -> env -i` und beide Namespace-Probes. Danach brach er vor
einem Lighttpd-Unittest fail-closed mit `BLOCKED: runtime.source_root` ab: Der
eingeschränkte Prozess `ns-test` konnte den bisherigen Checkout im
Runner-Workspace nicht traversieren. Der Lauf beweist nicht, welcher
Workspace-Parent die Sichtbarkeitsstörung verursachte, und ist kein
Lighttpd-Testfehler.

Die Reparatur entfernt die Runner-Workspace-Übergabe vollständig. Der
geschützte Bootstrap erzeugt unter `/var/lib/trusted-lighttpd-namespace` einen
root-eigenen `0755`-Parent, ein leeres root-eigenes Git-Template und zwei
root-eigene feste Helper; nur die festen Children `source` und `tmp`, beide
`0700`, gehören `ns-test`. Der Source-Namespace-Helper erhält über eine
bereinigte Umgebung nur den bereits API-gebundenen SHA und die feste numerische
`ns-test`-Identität. Source-Pfad, Git-Template und öffentlicher HTTPS-Origin
sind Literale im vertrauenswürdigen, von `master` kontrollierten Text.

Ein nachfolgendes Security-Review verwarf den früheren Plan, das `tmpfs` nach
`--map-current-user` einzuhängen: Nach diesem Non-root-`exec` berechnet Linux
die Capability-Sets neu, sodass der Mount nicht sicher erfolgen kann. Der
vertrauenswürdige Helper validiert deshalb die leeren festen Untergründe für
Source und temporäre Daten, bevor Source existiert, erfasst die Host-Namespace-
IDs und erzeugt danach als root einen privaten Mount-/PID-Namespace. Er setzt
die Mount-Propagation explizit auf privat und mountet ein begrenztes
`256m`-Source-`tmpfs` sowie ein separates begrenztes `128m`-Temp-`tmpfs`, beide
mit `nosuid,nodev,noexec`. Bis dahin wurde keine PR-Source gefetcht, gelesen,
kopiert, geparst oder ausgeführt.

Erst nach diesem leeren privaten Mount leert `setpriv --reuid/--regid` die
Zusatzgruppen, setzt `NoNewPrivs` und entfernt inheritable, ambient und
bounding Capabilities. Ein bereinigtes `env -i` betritt danach einen
verschachtelten User-/Mount-/PID-Namespace mit derselben Identität. Das innere
`unshare --keep-caps` ist ausschließlich für den kurzen festen Übergang zur
root-eigenen Systembinary `/usr/bin/setpriv` erlaubt: Dieser Finalizer wiederholt
die Non-root-Identität sowie die Abgabe von Gruppen, `NoNewPrivs`, inheritable,
ambient und bounding Capabilities, bevor er das root-eigene Source-Runner-Skript
als `ns-test` ausführt. Solange diese namespace-lokalen Capabilities bestehen,
wird kein PR-Code ausgeführt. Der Source-Runner beweist reale Non-root-UID/GID,
alle fünf leeren Capability-Sets, `NoNewPrivs`, AppArmor-Label,
Docker-Socket-Isolation, abweichende User-/Mount-/PID-Namespaces, PID 1 und
beide privaten `tmpfs`-Mounts, bevor Git materialisiert wird. Danach nutzt er
nur absolute, zuvor als root-eigen geprüfte Binaries und einen zeitbegrenzt
laufenden Git-Launcher: Initialisierung des privaten Mounts mit dem leeren
Template, Fetch ausschließlich des exakten SHA
(`--no-tags --depth=1 --no-recurse-submodules`), Prüfung von Commit/Object und
`HEAD`, Löschen von `.git`, Ablehnung von Checkout-Symlinks und Ausführung des
Namespace-Unittests.

Die Materialisierungsumgebung entsteht mit `env -i`: HTTPS ist das einzige
zulässige Git-Protokoll; Prompts, LFS-Smudge, globale/System-Konfiguration,
Hooks, Credential-Helper, File-Protokoll und Filesystem-Monitoring sind
deaktiviert. Kein Token, Workspace-Pfad, Branch/Ref, URL oder Git-Konfiguration
wird vom PR akzeptiert. Die privaten Source- und Test-Temp-Mounts werden
zusammen mit ihrem an `--kill-child` gebundenen Namespace bei regulärem Ende
oder kontrollierter Terminierung des Parent freigegeben. Nach Rückkehr von
Python prüft der eingeschränkte Runner zusätzlich, dass der private Temp-Root
leer ist. Der Host prüft nur nicht-destruktiv die Abwesenheit beider Mounts in
seiner Mount-Tabelle. Er löst niemals einen Same-UID-beschreibbaren Pfad zum
Cleanup auf. Dies ersetzt das geprüfte unsichere Muster `find ... -delete`;
Root liest, kopiert, parst oder löscht weder PR-Source noch Test-Temp-Daten
rekursiv.

Diese Änderung schwächt weder Namespace-, AppArmor-, Capability-, Token- noch
Failure-Gate ab. Sie ändert weder Framework- noch MRTS-Source, Gitlink,
Dependency, Toolchain, Action-Pin, Repository-Setting, gewöhnlichen PR-
Workflow oder den Draft-Status von PR #309. Hosted-Exact-Head-Runtime- und
Sonar-Evidence bleiben ausstehend, bis diese separat geprüfte Master-Reparatur
gemergt und dispatcht ist.

## 2026-08-23 Begrenzte Wiederholung der öffentlichen API-Bindung

Run `32619161990` schloss den eingeschränkten Bootstrap ab und brach vor der
Source-Materialisierung ab, als die feste anonyme GitHub-API-Anfrage für den
exakten Commit HTTP `504` lieferte. Dieses Ergebnis bleibt fail-closed, doch
die frühere Regel `--retry 0` machte eine vorübergehende Control-Plane-Störung
von einem dauerhaften Bindungsfehler ununterscheidbar.

Nur der idempotente feste HTTPS-GET-Helper verwendet nun begrenzte Curl-
Wiederholungen: drei Wiederholungen, eine Sekunde Wiederholungsverzögerung und
ein 30-Sekunden-Wiederholungsfenster. Die normale Transient-Error-Policy von
Curl umfasst HTTP `504`; `--retry-all-errors` wird nicht verwendet. Der
Resolver besitzt weiterhin kein Token, akzeptiert nur das strikt formatierte
Ziel, validiert die API-Antwort und scheitert vor jeder PR-Source, wenn seine
Wiederholungen erschöpft sind. Der separate status-schreibende POST behält
`--retry 0`, damit keine Side-Effect-Statusanfrage wiederholt wird.

## 2026-08-23 Reparatur des User-Namespace-CapBnd-Finalizers

Der Protected-master-Dispatch `32620696697` bestand den vertrauenswürdigen
Bootstrap und die exakte anonyme PR-Bindung für den PR-#309-Head
`316a5de1ac5e663fce3cce58428f1e1dd306e573`, brach jedoch vor jeder PR-Source-
Materialisierung mit `BLOCKED: runtime.capability_CapBnd` fail-closed ab. Das
frühere äußere `--bounding-set=-all` leerte den Capability-Bounding-State des
Host-Namespace korrekt; beim Eintritt in den verschachtelten User-Namespace mit
derselben Identität entsteht jedoch ein neues namespace-lokales Bounding-Set.
Der direkte Übergang `unshare -> dash` konnte daher die All-five-mask-
Voraussetzung des Source-Runners nicht erfüllen.

Die Reparatur bestätigt beim vertrauenswürdigen Bootstrap die Unterstützung von
`unshare --keep-caps` und verwendet diese Option genau einmal am inneren
Same-Identity-`unshare`. Sie ruft unmittelbar die feste root-eigene
Systembinary `/usr/bin/setpriv` auf, die `--reuid`, `--regid`,
`--no-new-privs`, `--inh-caps=-all`, `--ambient-caps=-all` und
`--bounding-set=-all` vor dem finalen Non-root-`dash`-Exec wiederholt. Die
äußere vertrauenswürdige Abgabe leert die Zusatzgruppen vor dieser Abbildung;
der innere Finalizer behält absichtlich nur diese bereits geprüfte einzige
Primärgruppe, ohne später `setgroups(2)` aufzurufen. Der Source-Runner behält seine unabhängigen Nullchecks
für `CapInh`, `CapPrm`, `CapEff`, `CapBnd` und `CapAmb`, bevor Git-,
Filesystem- oder Python-Operationen möglich sind. `--keep-caps` ist damit
keine Capability-Gewährung an PR-Code, sondern ausschließlich der minimale
vertrauenswürdige Übergang, um das namespace-lokale Bounding-Set zu verwerfen.
Fehlende Unterstützung oder ein fehlgeschlagener Finalizer- oder Source-Runner-
Check bleibt fail-closed.

Der statische Vertrag erlaubt kein zweites oder verschobenes `--keep-caps`,
verlangt die vollständige unmittelbare Finalizer-Sequenz und mutiert das
Entfernen jeder Finalizer-Abgabe, des Finalizers selbst und der inneren
Capability-Retention. Die Hosted-Ubuntu-24.04-Ausführung gegen den dann
aktuellen exakten PR-#309-Head bleibt die maßgebliche Bestätigung dieser
Reparatur.

### Lokale Validierung der CapBnd-Reparatur

- `rtk test /var/tmp/codex/ModSecurity-conector/ci-security-venv/bin/python -m unittest -v tests.test_trusted_lighttpd_namespace_dispatch_workflow` — bestanden (`2` Tests, einschließlich der neuen Finalizer-Abschwächungs-Mutationen).
- `rtk test /var/tmp/codex/ModSecurity-conector/ci-security-venv/bin/python -m unittest -v tests.test_ci_security_workflows` — bestanden (`28` Tests).
- `rtk test /var/tmp/codex/ModSecurity-conector/ci-security-venv/bin/python -m unittest -v connectors.lighttpd.tests.test_no_crs_fixture_namespace` im exakten lokalen PR-#309-Head-Worktree `316a5de1ac5e663fce3cce58428f1e1dd306e573` — bestanden (`18` Tests; `10` erwartete Skips außerhalb des Trusted-Integration-Gate).
- Python-`compileall`, `actionlint` mit ShellCheck, Offline-`zizmor` und `git diff --check` — bestanden.

## 2026-08-23 Reparatur des User-Namespace-setgroups-Finalizers

Protected-master-Dispatch `32622549590` erreichte den vertrauenswürdigen
Bootstrap und die exakte anonyme Bindung von PR-#309-Head
`a599ccb2fe3256500e59aef3d0f7d578a079cd7a`, brach jedoch vor der Source-
Materialisierung mit `setpriv: setgroups failed: Operation not permitted`
fail-closed ab. `unshare --map-current-user` impliziert zwingend
`--setgroups=deny`; daher kann der innere CapBnd-Finalizer nach dieser Abbildung
`--clear-groups` nicht sicher verwenden.

Der äußere vertrauenswürdige Finalizer führt `--clear-groups` bereits aus,
solange dies zulässig ist, und für das frisch erstellte `ns-test`-Konto wird
unabhängig genau seine Primärgruppe verlangt. Der innere Finalizer nutzt jetzt
`--keep-groups` ausschließlich zur Beibehaltung dieses bereits geleerten
Zustands, während er Identität, `NoNewPrivs` sowie die inheritable, ambient und
bounding Capability-Abgabe wiederholt. Der finale Source-Runner verlangt vor
jeder Git-, Filesystem- oder Python-Operation unabhängig, dass reale/effektive
UID und GID sowie die vollständige Gruppenliste genau den `ns-test`-IDs
entsprechen. Damit wird ein abgewiesener `setgroups(2)`-Aufruf vermieden, ohne
eine Gruppe, Capability, Source-Pfad oder Fallback hinzuzufügen.

Der statische Vertrag erlaubt genau zwei äußere `--clear-groups`-Abgaben und
genau ein inneres `--keep-groups` innerhalb der festen Finalizer-Sequenz. Seine
Mutationen weisen einen wiederhergestellten inneren Clear-Aufruf oder jeden
Versuch zum Setzen einer anderen Gruppe ab. Der nächste geschützte
Ubuntu-24.04-Exact-Head-Dispatch bleibt der maßgebliche Runtime-Nachweis.

### Lokale Validierung

- `rtk test python3 -m unittest -v tests.test_trusted_lighttpd_namespace_dispatch_workflow` — bestanden (`2` Tests, einschließlich der Abschwächungs-Mutationen).
- `rtk test /var/tmp/codex/ModSecurity-conector/ci-security-venv/bin/python -m unittest -v tests.test_ci_security_workflows` — bestanden (`28` Tests).
- `rtk test /var/tmp/codex/ModSecurity-conector/ci-security-venv/bin/python -m unittest -v connectors.lighttpd.tests.test_no_crs_fixture_namespace` im sauberen PR-#309-Worktree — bestanden (`18` Tests; `10` erwartete Skips ohne das Trusted-Integration-Gate).
- `actionlint` mit ShellCheck, Offline-`zizmor`, Python-`compileall`, die zweisprachige Dokumentationssuite und `git diff --check` — bestanden.

## Geänderte Dateien

- `.github/workflows/run-trusted-lighttpd-namespace-dispatch.yml` —
  geschützter manueller Ubuntu-24.04-Dispatcher, API-gebundene direkte
  eingeschränkte Source-Materialisierung in einem privaten Mount-Lifecycle und
  eingeschränkte `ns-test`-Ausführung.
- `tests/test_trusted_lighttpd_namespace_dispatch_workflow.py` — positive und
  Mutation-Contracts für Vertrauensgrenze, aktiven Profilnachweis, direkte
  Git-Materialisierung, privaten Mount-Teardown und isolierten Statusreporter.
- Dieses englisch/deutsche Change-Record-Paar — Autorisierung, Aufruf,
  Validierung und expliziter Pending-Runtime-Status.

Der bestehende Pull-Request-Workflow erhält weder `sudo` noch AppArmor-Setup.
Framework, MRTS, Gitlinks, Dependencies, Action-Pins und Settings bleiben
unverändert.

## Ausgeführte Befehle

### PASS

~~~text
rtk proxy env PYTHONDONTWRITEBYTECODE=1 /root/git/ModSecurity-conector/.venv/bin/python -m unittest -v tests.test_trusted_lighttpd_namespace_dispatch_workflow
rtk proxy env PYTHONDONTWRITEBYTECODE=1 /root/git/ModSecurity-conector/.venv/bin/python -m unittest -v tests.test_ci_security_workflows
rtk proxy /var/tmp/codex/ModSecurity-conector/trusted-dispatch-security-tools/actionlint -shellcheck=/usr/bin/shellcheck .github/workflows/run-trusted-lighttpd-namespace-dispatch.yml
rtk proxy /var/tmp/codex/ModSecurity-conector/trusted-dispatch-security-tools/zizmor --offline .github/workflows/run-trusted-lighttpd-namespace-dispatch.yml
~~~

Der Dispatcher-Contract, Abschwächungs-Mutationen und der repositoryweite
CI-Security-Workflow-Contract bestanden. `actionlint` bestand und der gesperrte
Offline-`zizmor` meldete keine Befunde.

## Runtime-Evidence

Noch existiert kein erfolgreicher Trusted-Runtime-Lauf. Nach Merge dieses
Workflows nach geschütztem `master` kann der kanonische Owner PR #309 auslösen:

~~~text
gh workflow run run-trusted-lighttpd-namespace-dispatch.yml --repo Easton97-Jens/ModSecurity-conector --ref master -f target=309
~~~

Im SHA-Modus ist `309` durch den aktuellen vollständigen kleingeschriebenen
40-stelligen PR-#309-Head-SHA zu ersetzen. Der Dispatcher gibt die
API-validierte PR und SHA vor der Source-Materialisierung aus. Sein erfolgreicher manueller
Lauf ist die erforderliche Runtime-Evidence. Der Reporter publiziert seinen
festen Exact-SHA-Status erst nach der Bindung des Ziels; Bootstrap- oder
Zielauflösungsfehler besitzen keinen vertrauenswürdigen SHA und lassen den
Dispatcher daher ohne einen ungebundenen Status fehlschlagen.

## Bekannte Einschränkungen

Das exakte Actor-/Triggering-Actor-Gate ist bewusst enger als eine allgemeine Maintainer-Rolle.
Eine Protected Environment mit Required Reviewers würde Governance ergänzen,
Repository-Settings-Änderungen liegen jedoch außerhalb dieses Pull Requests.
Der Dispatcher weist Fork-PRs und Nicht-Head-SHAs bewusst ab; er ist nur für
einen offenen Same-Repository-PR autorisiert, dessen Head vor der
Source-Materialisierung durch die API gebunden wird.

PR #309 bleibt Draft, bis dieser Workflow gemergt und ein Exact-Head-Manuallauf
erfolgreich ist.

Das aktive Protected-master-Ruleset muss zusätzlich
`trusted-lighttpd-namespace` als erforderlichen Kontext verlangen, bevor ein
grüner gewöhnlicher PR-Check als automatische Merge-Bedingung gelten kann.
Repository-Settings liegen bewusst außerhalb dieses Pull Requests; bis diese
explizite Regel existiert, bleibt der Draft-Status von PR #309 die dokumentierte
verbindliche manuelle Merge-Sperre.

## Security-Auswirkung

Die Reparatur entfernt das Modell, in dem ein PR privilegierte Schritte im
selben Pull-Request-Workflow verändern konnte, der seine Source ausführt.
Privilegierte Arbeit stammt nun aus geprüftem Protected-master-YAML und endet
vor der Source-Materialisierung. Es gibt keinen Checkout im Runner-Workspace;
der Root-Helper erstellt nur leere private Mounts und liest, kopiert, parst,
startet oder bereinigt keinen PR-abgeleiteten Pfad. Jede Source-Verarbeitung
erfolgt erst nach dem Non-root-Drop.

Der Dispatcher ergänzt weder Root-Path-Cleanup noch einen
privilegierten-Container-Fallback, globale AppArmor-Abschwächung oder einen
erfolgreichen Skip.

Der Reporting-Job ist absichtlich vom PR-Code-Job getrennt. Sein kurzlebiges
`statuses: write`-Token kann PR-Code nicht lesen, weil der Reporter weder
Checkout noch übertragene Daten außer einem strikt geprüften SHA-Output und
der Testjob-Conclusion besitzt. Er kann Kontext, Ziel oder Ergebnis nicht aus
PR-Input wählen.

## Verbleibende Risiken

Das AppArmor-Profil nutzt `flags=(unconfined)`, um diesen Non-root-
User-Namespace-Pfad unter Ubuntu 24.04 zu erlauben, und ist deshalb keine
restriktive AppArmor-Sandbox. Sein Scope wird durch einen frischen Account ohne
Capabilities, Credentials, geerbte Umgebung oder Docker-Socket sowie die
Namespace-Probes begrenzt. Kernel- oder Bubblewrap-Defekte bleiben externe
Platform-Risiken.

Die öffentliche API ist absichtlich unauthenticated, um ein Secret zu
vermeiden. Rate-Limit oder API-Fehler brechen fail-closed ab. Der finale
Teardown der entsorgbaren VM entfernt Profil, Account und temporäre Daten ohne
Root-Cleanup eines von `ns-test` beschreibbaren Pfads.

Der Reporter-Kontext ist Evidence und keine durch Repository-Regeln erzwungene
Garantie, bis der Repository-Owner ihn zu den erforderlichen
Protected-master-Kontexten hinzufügt. Dieser Pull Request ändert keine
Branch-Regeln; PR #309 muss Draft bleiben, bis diese Governance-Aktion und ein
erfolgreicher Exact-Head-Dispatch unabhängig nachgewiesen sind.

## Nicht ausgeführte Prüfungen mit Begründung

Der manuelle Ubuntu-24.04-Runtime-Lauf kann erst nach Merge dieses separaten
Workflows nach geschütztem `master` erfolgen; die Kopie aus diesem Branch zu
dispatchen würde die Vertrauensgrenze zerstören. PR-#309-Code wurde unter
diesem Design lokal nicht ausgeführt. Kein Merge, Hosted-PR-Check,
SonarQube-Analyse oder Required Check wird behauptet.

## Finaler Diff- und Review-Status

Diese Parent-only-Bootstrap-Änderung ist für einen eigenen Draft-Pull-Request
bestimmt. Sie belässt den Pull-Request-Workflow von PR #309 unprivilegiert.
Nach Review und Merge des Bootstrap-PR muss der Owner von `master` dispatchen,
den resultierenden PR-#309-SHA verifizieren und #309 Draft belassen, sofern
nicht die vollständige Namespace-Evidence erfolgreich ist.
