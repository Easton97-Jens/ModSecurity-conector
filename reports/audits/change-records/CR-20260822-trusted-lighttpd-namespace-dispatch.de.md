# Change Record

**Sprache:** [English](CR-20260822-trusted-lighttpd-namespace-dispatch.md) | Deutsch

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | CR-20260822-trusted-lighttpd-namespace-dispatch |
| Datum (UTC) | 2026-08-22 |
| Basis-Revision | `423abcc130cf5d29ccf15dd7d82e4e7d89d495d3` |
| Delivery-Status | Separater Protected-master-Bootstrap-Pull-Request; weder Merge noch erfolgreicher Trusted-Runtime-Lauf werden behauptet. |

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

## Akzeptanzkriterien

- Der Dispatcher besitzt nur `workflow_dispatch`, genau eine `target`-Eingabe,
  ein Protected-`master`-/kanonisches-Repository-Gate und ein exaktes
  Owner-Maintainer-Actor-Gate.
- Er besitzt nur `contents: read`, keine Secrets, Caches, Artefakte,
  `pull_request_target`, Status-Write oder Checkout einer lokalen Action.
- Feste Systemschritte vor dem Checkout installieren nur feste Pakete, laden
  das feste AppArmor-User-Namespace-Profil, erzeugen `ns-test` und prüfen
  Binary-, Gruppen-, Docker-Socket- und Capability-Voraussetzungen.
- Die API-Auflösung akzeptiert eine offene kanonische PR-Nummer oder deren
  exakten 40-stelligen kleingeschriebenen Head-SHA; der Source-Checkout nutzt
  ausschließlich den aufgelösten SHA.
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

Vor dem Checkout prüfen feste absolute root-eigene Binaries, installieren nur
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

Der vertrauenswürdige Source-Pfad lautet:

~~~text
manual target -> strict format validation -> fixed public GitHub API request
-> one open canonical PR/head SHA -> exact SHA checkout -> remove .git
-> aa-exec -> setpriv -> env -i -> ns-test namespace test
~~~

Kein PR-abgeleiteter Text gelangt in einen privilegierten Shell-Befehl, und der
rohe Input ist niemals ein Checkout-Ref. Die PR-Source wird erst nach dem
Identity-Drop kopiert. Die entsorgbare GitHub-hosted-VM besitzt abschließend
Account-/Profil-/Temp-Teardown; bewusst gibt es nach gelaufenem PR-Code kein
root-seitiges rekursives Löschen eines von `ns-test` beschreibbaren Baums.

Das Pre-Checkout-Bootstrap erzeugt seinen Run-State ausschließlich unter dem
vorab geprüften root-eigenen, nicht beschreibbaren `/var/lib`-Parent. Es nutzt
bewusst nicht `/var/tmp`, dessen Standardmodus `1777` sowohl mit der
Trusted-Directory-Invariante unvereinbar ist als auch keinen geeigneten Parent
für einen privilegierten Runtime-Root bildet. Der Dispatcher prüft den exakten
root-eigenen `0755`-State-Root sowie die exakten Non-root-`source`- und
privaten `0700`-Temp-Children vor Checkout oder PR-Code-Ausführung.

## Geänderte Dateien

- `.github/workflows/run-trusted-lighttpd-namespace-dispatch.yml` —
  geschützter manueller Ubuntu-24.04-Dispatcher, API-gebundener exakter
  Checkout und eingeschränkte `ns-test`-Ausführung.
- `tests/test_trusted_lighttpd_namespace_dispatch_workflow.py` — positive und
  Mutation-Contracts für die Vertrauensgrenze.
- Dieses englisch/deutsche Change-Record-Paar und Archiveinträge —
  Autorisierung, Aufruf, Validierung und expliziter Pending-Runtime-Status.

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
API-validierte PR und SHA vor dem Checkout aus. Sein erfolgreicher manueller
Lauf ist die erforderliche Runtime-Evidence; er lässt den gewöhnlichen
Pull-Request-Workflow keinen Erfolg behaupten.

## Bekannte Einschränkungen

Das exakte Actor-/Triggering-Actor-Gate ist bewusst enger als eine allgemeine Maintainer-Rolle.
Eine Protected Environment mit Required Reviewers würde Governance ergänzen,
Repository-Settings-Änderungen liegen jedoch außerhalb dieses Pull Requests.
Der Dispatcher weist Fork-PRs und Nicht-Head-SHAs bewusst ab; er ist nur für
einen offenen Same-Repository-PR autorisiert, dessen Head vor dem Checkout
durch die API gebunden wird.

PR #309 bleibt Draft, bis dieser Workflow gemergt und ein Exact-Head-Manuallauf
erfolgreich ist.

## Security-Auswirkung

Die Reparatur entfernt das Modell, in dem ein PR privilegierte Schritte im
selben Pull-Request-Workflow verändern konnte, der seine Source ausführt.
Privilegierte Arbeit stammt nun aus geprüftem Protected-master-YAML und endet
vor dem Checkout. Die einzigen Root-Aktionen nach dem Checkout sind festes
Git-State-Entfernen und der statische `aa-exec`-zu-`setpriv`-Launcher; keine
davon liest, kopiert, parst oder startet PR-Source. Jede Source-Verarbeitung
erfolgt erst nach dem Non-root-Drop.

Der Dispatcher ergänzt weder Root-Path-Cleanup noch einen
privilegierten-Container-Fallback, globale AppArmor-Abschwächung oder einen
erfolgreichen Skip.

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
