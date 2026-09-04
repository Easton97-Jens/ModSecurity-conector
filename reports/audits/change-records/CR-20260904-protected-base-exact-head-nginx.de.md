# Change Record

**Sprache:** [English](CR-20260904-protected-base-exact-head-nginx.md) | Deutsch

| Feld | Wert |
| --- | --- |
| Change-ID | CR-20260904-protected-base-exact-head-nginx |
| Datum (UTC) | 2026-09-04 |
| Basis-Revision | 2b3d7f7f0bec006b236b5998d011069c9125033f |
| Umfang | Parent-only-Vorbereitung für unabhängige NGINX-Exact-Head-Evidence über geschützte Base |
| Auslieferungsstatus | Draft-PR-#355-Branch-only-Base-Merge `5368569351e968e8ea641fc485590654df6a4336` plus Protected-Workflow-Remediation-Checkpoint `fa9064a560b31b377dc1dea3a9b8b99e6867809c`; keine Merge-Autorisierung |
| Candidate | PR #354; exakter Head muss beim Dispatch aufgelöst und zurückgelesen werden |

## Zweck

Dieser Record dokumentiert die separat geprüfte Steuerung, die ein Testen des
Candidate-NGINX-Moduls ermöglicht, ohne dass der Candidate-PR privilegierten
Launcher oder Evidence-Collector besitzt. Der vertrauenswürdige Base-Dispatcher
bindet den kanonischen offenen PR und die vollständige Head-SHA; der
unprivilegierte Build paketiert feste Artefakte; ein geschützter Base-Launcher
führt die beiden nativen On/Off-Zellen aus; und ein unabhängiger Collector
erzeugt begrenzte hostseitige Evidence.

Der Branch-only-Checkpoint ist ein normaler Merge von aktuellem
`origin/master` `2b3d7f7f0bec006b236b5998d011069c9125033f` in den Draft-PR-
Branch; sein anderer Parent ist der frühere PR-Head
`de1c3c05b53a00e077aca1c08a2fcdc552b0344e`. Er mergt weder PR #355 noch PR
#354 in `master`. Der historische gemeinsame Base bleibt
`95bc04203455bc74a9cd18fafc6fb5848af2bbb2`.

## Finales Successor-Update — Source-Checkpoint `fa9064a5`

Das frische GitHub-`zizmor`-Ergebnis für den vorherigen Successor
`737c9674…` identifizierte eine direkte Expansion von
`needs.resolve.outputs.tested_pr_head` in den Bash-`run:`-Body des
Candidate-SHA-Vergleichs. Der normale Folgecommit
`fa9064a560b31b377dc1dea3a9b8b99e6867809c` bindet diesen vom Dispatcher
zugelassenen Wert nur als Step-lokale `VALIDATED_PR_HEAD`-Daten und vergleicht
die quotierte Shell-Variable. Das exakte Checkout-`ref` bleibt ein
Action-Input; der geschützte Framework-Gitlink-Vergleich, der unprivilegierte
Build, das root-eigene Host-Gate und alle späteren Privileggrenzen bleiben
unverändert. Dies ist die eng begrenzte Behebung für `FND-PARENT-1034`, keine
Workflow-Suppression und keine Quality-Gate-Änderung.

Am Source-Checkpoint `fa9064a5` bestand der exakte Sieben-Module-Befehl
`python -B -m unittest -q tests.test_nginx_exact_head_base_helper tests.test_nginx_exact_head_result_collector tests.test_nginx_exact_head_root_launcher tests.test_protected_nginx_exact_head_builder tests.test_protected_nginx_exact_head_dispatcher tests.test_protected_nginx_exact_head_runner_preflight tests.test_protected_nginx_exact_head_workflow`
mit 99 fokussierten Protected-Base-Tests; 22 bilinguale Tests und der getrennt
abgegrenzte Workflow-plus-Dispatcher-Control mit 29 Tests bestanden ebenfalls.
Python-Kompilierung, POSIX-Shell-Syntax, `actionlint`, Offline-`zizmor`,
Policy-Audit, Variable-Documentation-Check und `git diff --check` bestanden.
Der dedizierte Zwei-Dateien-Successor-Scan ist unter
`security-diff-final-fa9064a5/report.md` versiegelt und gültig; er meldet
keinen verbleibenden Source-Fund und explizit partielle Hosted-/Runtime-
Abdeckung. `make check-nginx-c17` ist **blockiert**, nicht bestanden:
unterstützte NGINX-Header/-Quellen fehlen und das zugrunde liegende Target gibt
Exit 77 zurück. Breite Documentation-Link-Checks sind ausschließlich durch den
geerbten, nicht initialisierten Framework-Gitlink blockiert; er wurde weder
initialisiert noch geändert.

SonarCloud analysierte exakt `fa9064a5` um `2026-09-04T19:44:32+0000`.
GitHub-Check `101153230682` endete um `19:46:39Z` mit `failure`; das Gate ist
`ERROR`, weil `new_security_rating=3` den geforderten Wert `1` überschreitet.
Die übrigen Gate-Bedingungen sind OK. Das authentifizierte aktuelle Inventar
enthält dieselben 80 offenen Schlüssel wie der vorherige Exact-Head (15
Vulnerabilities und 65 Code Smells); jeder Schlüssel besitzt eine aufbewahrte
individuelle Source-/Sink-/Privileg-/Ownership-Triage. Das Gesamtergebnis ist
`A=0`, `B=26`, `C=35`, `D=19`; kein Issue wird stillschweigend als False
Positive bezeichnet und unsichere kosmetische Änderungen bleiben
`blocked_by_security_invariant`. Der frische GitHub-`zizmor`-Check für
`fa9064a5` war erfolgreich. Dies sind ausschließlich Checkpoint-Fakten: der
normale Push des finalen Documentation-Successors, dessen exakter Remote-
Readback und frische Checks bleiben getrennt erforderlich und dürfen keinen
früheren grünen Lauf als Nachweis wiederverwenden.

`FND-PARENT-1013` bleibt `fixed, verification pending`. `FND-PARENT-1034` ist
`fixed, verification pending`, bis die Successor-Delivery-Evidenz abgeglichen
ist. Für die erforderliche Review-Anfrage existiert kein berechtigter
unabhängiger GitHub-Collaborator; es wurden weder Zugang, Einladung noch
erfundene Review vorgenommen.

## Akzeptanzkriterien

- Jeder privilegierte Befehl und Evidence-Parser stammt aus geschützter Base-
  Source; kein Candidate-Workflow und kein Candidate-Shellcode läuft
  privilegiert.
- Der Dispatcher liest kanonisches Repository, PR-Status, Base und
  vollständige Head-SHA zurück und lässt nur diese unveränderliche Candidate-
  Revision zu.
- Artefakt- und Runtime-Evidence sind an Candidate-SHA und vertrauenswürdigen
  Base-Digest gebunden; Candidate-schreibbare Pfade können sie nicht ersetzen.
- Frische On/Off-Zellen liefern unabhängig root-seitig beobachtete getrennte
  Master-/Worker-Identitäten, transaktionskorrelierte Callback-/JSONL-
  Beobachtungen, gleichwertige beobachtete Candidate-WAF-Entscheidungen und
  Exit 0. Der transportseitige HTTP-403 und die Identitätsgrenze werden root-
  seitig beobachtet; die semantische Candidate-WAF-Entscheidung und Callback/
  JSONL sind begrenzte Sandbox-Beobachtungen, keine kryptografisch oder
  provenance-authentifizierten semantischen Attestierungen. Der Collector-
  Status lautet `validated_observations`, mit `candidate_scratch_untrusted` für
  Callback/JSONL und `root_pidfd_network_namespace` für root-seitiges HTTP.
- Negative Substitution, Pfad, Descriptor, Environment und Runner-Kontrollen
  schlagen geschlossen fehl; kein Bypass und keine Quality-Gate-Abschwächung
  wird eingeführt.

## Obligatorisches Hosted-Gate

Der privilegierte Workflow darf nur auf einem dedizierten geschützten Runner
mit einem vorinstallierten root-eigenen, nicht beschreibbaren Bootstrap unter
`/usr/local/libexec/modsecurity-protected-exact-head/run-exact-base-launcher`
zugelassen werden. Der Bootstrap muss das geschützte Base-Git-Objekt prüfen und
Launcher/Helper vor der Ausführung in einen root-eigenen temporären Snapshot
kopieren. Veränderliche Source-Pfade, unsichere Eigentümer/Rechte, eine
abweichende Base-SHA und eine nicht vertrauenswürdige Umgebung müssen abgelehnt
werden. Dieses Repository provisioniert oder attestiert diese Host-Komponente
nicht; ihr Fehlen blockiert Hosted-Evidence.

## Evidence-Status

Zum Zeitpunkt dieses Records liegt nur lokale Source-Contract- und Unit-Test-
Evidence vor. GitHub hat derzeit weder eine geschützte Environment noch einen
dedizierten gelabelten Runner für den privilegierten Job konfiguriert. Deshalb
sind Exact-Head-Hostlauf, unabhängige Runtime-Attestierung und abschließende
PR-#354-Verifikation blockiert/nicht verifiziert; frühere Läufe werden nicht
als Nachweis verwendet.
Linux-`pidfd` plus `setns(CLONE_NEWNET)` bildet die Source-seitige Lifetime-
Grenze für das root-seitige HTTP-Kind. Der Hosted-Runtime-Nachweis muss noch am
exakten Hosted-Head validiert werden; hier wird kein Runtime-Nachweis behauptet.

Das Host-AppArmor-Profil verwendet absichtlich `flags=(unconfined)`. Es dient
nur der Zulassung des Host-User-Namespace und der Validierung des Profil-Labels;
es ist keine Zusage einer MAC-Einschränkung. Namespace-Isolation,
Capability-Begrenzung und `no_new_privs` bleiben getrennte Kontrollen und
benötigen eine unabhängige Validierung.

## SonarCloud-Readback und Source-Remediation

Der erste veröffentlichte Draft-PR-Head
`78163d65dc19ee2cf1500dafa4d0f5d5cc36893b` erhielt ein frisches SonarCloud-
Quality-Gate `ERROR`: `new_security_rating=5` überschreitet den konfigurierten
Grenzwert `1`. Das authentifizierte PR-Inventar enthielt 26 Vulnerabilities und
72 Code Smells. Zwei `githubactions:S7630`-Zeilen wurden bestätigt: Die manuell
übergebene PR-Nummer wurde direkt in Shell-Source gerendert, bevor der Python-
Validator laufen konnte. Der Successor übergibt diesen Wert ausschließlich
über eine quotierte Step-Environment-Variable.

Diese SonarCloud-Werte sind ein aufbewahrter historischer Readback für
`78163d65dc19ee2cf1500dafa4d0f5d5cc36893b`, keine Current-Head-Evidence.
Dieser Record enthält weder ein unveränderliches lokales Sonar-Artefakt noch
eine aktuelle Check-Run-URL für diese historische Abfrage; ihre Provenienz ist
daher für die aktuell geprüfte Source `not_verified`. Nach dem finalen
normalen Branch-Push sind ein neues authentifiziertes PR-#355-Inventar und eine
Quality-Gate-Abfrage erforderlich.

Der Successor stärkt außerdem Dispatcher- und Collector-Dateigrenzen durch
Full-Chain-, descriptor-relative, no-follow-Operationen; bindet das
Collector-Manifest an seinen festen privaten Task-Root-Ort; lehnt beschreibbare
Input-Artefakte ab; und verschiebt temporären Sandbox-Speicher in einen frischen
privaten `/run/nginx-exact-head-tmp`-Mount. Der unprivilegierte Candidate-
Builder hält den zugelassenen Task-Descriptor über Candidate-`make` hinweg;
beim Packaging öffnet und hält er die zugelassenen Build- und Package-
Deskriptoren. Den ausgewählten Snapshot und feste Artefakte liest er
ausschließlich relativ zu diesen Deskriptoren und die festen Artefaktnamen samt
Manifest veröffentlicht er nur relativ zu ihnen. Die Snapshot-Aufzählung ist
nur lexikalisch zur Auswahl eines Candidate-Namens; das Packaging öffnet dessen
Komponenten unterhalb des gehaltenen Task-Descriptors. Kontrollierte Task-
Root-, Build-Root- und Output-Directory-Swap-Regressionen belegen, dass kein
Ersatzverzeichnis verwendet wird und ein Identitätswechsel das Package-
Ergebnis vor der Rückgabe fail-closed ablehnt. Fokussierte Source-Refactorings
erhalten das bestehende fail-closed Verhalten. Es werden weder `NOSONAR`,
Issue-/Risikoakzeptanz,
Scanner-Exclusion, Quality-Gate-/Regeländerung, Coverage-Reduktion noch
Workflow-Abschwächung verwendet. Eine frische Exact-Successor-Sonar-Analyse ist
weiterhin erforderlich; das Ergebnis des Initial-Heads ist kein Nachweis für
einen Successor.

Der Source-Review nach dem Merge fand zusätzlich, dass der Candidate-Builder
sein Candidate-gesteuertes `Makefile` auf einem als root konfigurierten Runner
erreichen konnte, weil reale, effektive oder gespeicherte root-Identitäten nicht
abgelehnt wurden. Der Builder lehnt jetzt jede root-UID/GID vor jedem
Candidate-Pfadzugriff oder festen `make`-Vektor ab und gibt das zugelassene
`nginx`-Binary mit festem Modus `0500` aus; die reinen Datenartefakte Modul und
Library bleiben `0400`. Regressionstests prüfen Root-Ablehnung, Nicht-root-
Kontrollen, Ablehnung eines nicht ausführbaren Binary und feste Output-Modi.
Dies ist die Source-Korrektur für `FND-PARENT-1032`; sie bleibt ausstehend,
bis finale Exact-Head-Validierung und Readback abgeschlossen sind.

Der Source-Review des Successors fand zusätzlich ein geerbtes Root-Control-
File-Rennen in derselben Launcher-Grenze. Ein Candidate kann in das
runner-eigene Runtime-Verzeichnis der Zelle schreiben. Der frühere Publisher
schloss einen vorhersagbaren temporären Pfad vor der pfadbasierten Ersetzung;
die Release- und Completion-Caller führten danach pfadbasierte Root-
Metadatenoperationen aus. Ein ersetzter Symlink konnte deshalb Root-`chmod`
oder `chown` umleiten; außerdem lehnte der normale Completion-Pfad sein
absichtlich fehlendes Leaf ab. Der korrigierte zentrale Publisher hält einen
No-Follow-Parent-Descriptor, schreibt, prüft den Modus und identifiziert die
temporäre Datei über ihren Descriptor vor der descriptor-relativen Ersetzung;
anschließend öffnet und vergleicht er das veröffentlichte Leaf ohne Follow.
Caller führen keine pfadbasierten Metadatenänderungen nach der Veröffentlichung
mehr aus. Kontrollierte Pre-Fix-Tests zeigten, dass das Release-Rennen nicht
fail-closed abbrach und einen task-eigenen Opfermodus von `0644` nach `0400`
änderte; die Post-Fix-Regressionen lehnen sowohl Release- als auch Completion-
Substitution ab und der normale Completion-Control wird korrekt veröffentlicht.
Release- und Completion-Marker liegen jetzt unterhalb einer root-eigenen
Cell-Hierarchie in einem getrennt angelegten und für den Candidate nicht
schreibbaren Control-Verzeichnis; der Base-Helper prüft dieses Verzeichnis,
bevor er einem der festen Marker vertraut, sodass ein Candidate sie nach der
Veröffentlichung nicht neu erzeugen kann. Ein frischer Exact-Successor-Source-
und Hosted-Review bleibt erforderlich.

## Ausgeschlossener Umfang

Keine Produktreparatur, Framework-/MRTS-Source, Gitlink-, Dependency-,
Branch-Schutz-, Merge-, Force-Push-, Secret-, privilegierte PR-Workflow- oder
Sonar-Suppression-Änderung gehört zu diesem Record. `FND-PARENT-1013` bleibt
`fixed, verification pending`. `FND-GITHUB-0009` bleibt offen, bis eine
frische geschützte Runtime die Akzeptanzkriterien und Host-Gate-/Lifetime-
Kontrollen validiert. `FND-PARENT-1032` ist eine Parent-only-Source-Korrektur
und reduziert nicht die getrennte Host-Gate- oder Runner-Isolationsvoraussetzung.

## Erforderliche nächste Evidence

Nach Provisionierung von geschützter Environment und Runner: aus der geprüften
Base dispatchen, die exakte Candidate-SHA aus GitHub zurücklesen und den
vollständigen Collector-Record aufbewahren, einschließlich `tested_pr_head`,
`trusted_dispatcher_base_sha`, NGINX-Version/Source-Digest, Modul-Digest,
Master-/Worker-Identitäten, On/Off-Callback- und JSONL-Ergebnissen, WAF-
Entscheidungen, `decision_equivalent` und `final_exit_code`.

## Identität

Parent-only-Vorbereitungsrecord für die geschützte Base-Exact-Head-Steuerung;
kein Record der Produktreparatur von PR #354.

## Motivation und Problemstellung

Candidate-gesteuerter PR-Code darf während des Exact-Head-Tests weder
privilegierten Runtime-Start noch Evidence-Sammlung besitzen.

## Implementierungsentscheidung und Begründung

Verwendet werden geschützte Base-Admission, das obligatorische Host-Gate,
unprivilegierter Build und root-seitige Sammlung. Root-seitiges HTTP verwendet
Linux-`pidfd` und `setns(CLONE_NEWNET)`; Candidate-WAF-Semantik und Callback/JSONL
bleiben Beobachtungen.

## Geänderte Dateien

Der Protected-Base-Diff gegenüber aktueller Base enthält genau diese 23 Pfade:

- `.github/actionlint.yaml`
- `.github/workflows/run-protected-nginx-exact-head.yml`
- `ci/runtime/broker/nginx_exact_head_result_collector.py`
- `ci/runtime/broker/nginx_exact_head_root_launcher.py`
- `ci/runtime/broker/protected_nginx_exact_head_builder.py`
- `ci/runtime/broker/protected_nginx_exact_head_dispatcher.py`
- `ci/runtime/broker/protected_nginx_exact_head_runner_preflight.py`
- `ci/runtime/broker/run_nginx_exact_head_cells.sh`
- `docs/security/protected-exact-head-host-gate.de.md`
- `docs/security/protected-exact-head-host-gate.md`
- `docs/security/protected-exact-head-nginx.de.md`
- `docs/security/protected-exact-head-nginx.md`
- `reports/audits/change-records/CR-20260904-protected-base-exact-head-nginx.de.md`
- `reports/audits/change-records/CR-20260904-protected-base-exact-head-nginx.md`
- `reports/audits/change-records/README.de.md`
- `reports/audits/change-records/README.md`
- `tests/test_nginx_exact_head_base_helper.py`
- `tests/test_nginx_exact_head_result_collector.py`
- `tests/test_nginx_exact_head_root_launcher.py`
- `tests/test_protected_nginx_exact_head_builder.py`
- `tests/test_protected_nginx_exact_head_dispatcher.py`
- `tests/test_protected_nginx_exact_head_runner_preflight.py`
- `tests/test_protected_nginx_exact_head_workflow.py`

## Ausgeführte Befehle

### Tests und tatsächliche Ergebnisse

Die folgenden lokalen Ergebnisse wurden für den Source-Checkpoint
`53aee10ddeb448ed7506e645709d2162aeab091f` beobachtet; finaler Branch-
Readback und Hosted-Checks bleiben getrennt erforderlich.

- `python -B -m unittest -q tests.test_protected_nginx_exact_head_dispatcher tests.test_protected_nginx_exact_head_builder tests.test_protected_nginx_exact_head_runner_preflight tests.test_nginx_exact_head_root_launcher tests.test_nginx_exact_head_result_collector tests.test_nginx_exact_head_base_helper tests.test_protected_nginx_exact_head_workflow` — bestanden, 98 Tests.
- `python -B -m unittest -q tests.test_bilingual_docs` — bestanden, 22 Tests.
- `python -B -m unittest -q tests.test_event_runtime_security_contract tests.test_nginx_native_security_contract tests.test_nginx_upstream_security_contract tests.test_connector_config_reference tests.test_sonar_reliability_contract` — bestanden, 48 Tests.
- `python -B -m py_compile` für die fünf geschützten Broker-Python-Dateien — bestanden; `sh -n` und `bash -n` für `run_nginx_exact_head_cells.sh` — bestanden; `actionlint .github/workflows/*.yml` — bestanden.
- `make check-variable-documentation` — bestanden, 101 dokumentierte Variablenreferenzen; Parent-Lokalpolicy-Validierung — konsistent; `git diff --check` — vor dem Staging bestanden.
- `make check-nginx-c17` — blockiert: unterstützte NGINX-Header/-Quellen fehlen, und das zugrunde liegende Target gab Exit 77 zurück. Dies ist kein erfolgreiches natives NGINX-Ergebnis.
- `make check-bilingual-docs` und `make check-doc-links` — ausschließlich durch bereits vorhandene fehlende Links innerhalb des nicht initialisierten Framework-Gitlinks blockiert; der Change-Record-spezifische deutsche Linkfehler wurde korrigiert.

## Security-Auswirkung

Die Steuerung schlägt bei Source-, SHA-, Pfad-, Descriptor-, Environment- und
Runner-Substitution geschlossen fehl. Root-seitiger Transport-HTTP-403 und
Prozessidentität bilden die Grenze; Candidate-WAF-Semantik und Callback/JSONL
sind keine vertrauenswürdigen Attestierungen.

## Runtime-Evidence

Für diesen Head existiert keine Hosted-Runtime-Evidence. Der erforderliche
Collector-Status ist `validated_observations`, mit den Labels
`root_pidfd_network_namespace` und `candidate_scratch_untrusted`.

## Bekannte Einschränkungen

Host-Bootstrap, geschützte Environment, dedizierter Runner und unabhängige
Attestierung sind externe Voraussetzungen und in diesem Checkout nicht verfügbar.

## Verbleibende Risiken

Candidate-Code kann Callback/JSONL und WAF-Semantikwerte nachahmen. PID-/
Namespace-Lifetime und Host-Gate-Verhalten benötigen Exact-Head-Hosted-Validierung.
Nach den finalen Descriptor-Identitätsprüfungen des Builders könnte ein
gleichberechtigter Candidate-Hintergrundprozess noch in einem Race den an
seinen unprivilegierten Caller zurückgegebenen lexikalischen Upload-Pfad
austauschen. Dies liegt außerhalb des Packaging-Fensters mit gehaltenen
Builder-Deskriptoren; das zurückgegebene Bundle wird vom Root-Launcher als
untrusted behandelt und durch Fixed-Name-Descriptor-/Digest-Prüfungen erneut
zugelassen. Für diesen Handoff ist weiterhin Exact-Hosted-Runner-Evidence
erforderlich.

## Nicht ausgeführte Prüfungen mit Begründung

Geschützter Hosted-NGINX-Runtime-Lauf und unabhängige Host-Attestierung wurden
wegen der fehlenden Environment und des fehlenden Runners nicht ausgeführt.
PR-#354-/Sonar-Remediation-Prüfungen liegen außerhalb dieses Base-Umfangs.

## Finaler Diff- und Review-Status

Lokale Prüfungen bestanden wie oben vermerkt. Hosted-Verifikation bleibt
blockiert; dies ist ausschließlich Vorbereitung ohne Merge-Autorisierung.


Ausschließlich Vorbereitung — keine Merge-Autorisierung.
