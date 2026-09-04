# Change Record

**Sprache:** [English](CR-20260904-protected-base-exact-head-nginx.md) | Deutsch

| Feld | Wert |
| --- | --- |
| Change-ID | CR-20260904-protected-base-exact-head-nginx |
| Datum (UTC) | 2026-09-04 |
| Basis-Revision | 95bc04203455bc74a9cd18fafc6fb5848af2bbb2 |
| Umfang | Parent-only-Vorbereitung für unabhängige NGINX-Exact-Head-Evidence über geschützte Base |
| Auslieferungsstatus | Draft-PR-#355-Successor-Remediation in Vorbereitung; keine Merge-Autorisierung |
| Candidate | PR #354; exakter Head muss beim Dispatch aufgelöst und zurückgelesen werden |

## Zweck

Dieser Record dokumentiert die separat geprüfte Steuerung, die ein Testen des
Candidate-NGINX-Moduls ermöglicht, ohne dass der Candidate-PR privilegierten
Launcher oder Evidence-Collector besitzt. Der vertrauenswürdige Base-Dispatcher
bindet den kanonischen offenen PR und die vollständige Head-SHA; der
unprivilegierte Build paketiert feste Artefakte; ein geschützter Base-Launcher
führt die beiden nativen On/Off-Zellen aus; und ein unabhängiger Collector
erzeugt begrenzte hostseitige Evidence.

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

## Ausgeschlossener Umfang

Keine Produktreparatur, Framework-/MRTS-Source, Gitlink-, Dependency-,
Branch-Schutz-, Merge-, Force-Push-, Secret-, privilegierte PR-Workflow- oder
Sonar-Suppression-Änderung gehört zu diesem Record. `FND-PARENT-1013` bleibt
`fixed, verification pending`. `FND-GITHUB-0009` bleibt offen, bis eine
frische geschützte Runtime die Akzeptanzkriterien und Host-Gate-/Lifetime-
Kontrollen validiert.

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

Siehe geschützte Dispatcher-, Builder-, Preflight-, Launcher-, Collector-,
Helper-, Workflow-, fokussierte Test- und bilingualen Dokumentationsdateien
dieses Draft-PRs.

## Ausgeführte Befehle

Fokussierte Python-`unittest`: bestanden, 86 Tests. Python-Kompilierung,
`/bin/sh -n` und `actionlint` für den geschützten Workflow bestanden.
Descriptor-verankerte Evidence-Root-/Leaf-Lesezugriffe sowie Dispatcher- und
Collector-Path-Substitution-Regressionen bestanden ebenfalls. JSON-Schema-
Versionen verlangen einen tatsächlichen JSON-Integer; `true` kann daher nicht
als Version `1` auftreten. Dies sind ausschließlich lokale Ergebnisse vor dem
Successor-Commit; Hosted- und Sonar-Evidence müssen für dessen exakte SHA neu
zurückgelesen werden.

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

## Beobachtete lokale Validierung

Die fokussierte Python-Unit-Suite für Protected-Dispatcher, Builder,
Preflight, Launcher, Collector, Helper und Workflow-Contracts bestand mit 86
Tests. Descriptor-verankerte Evidence-Root-/Leaf-Lesezugriffe, Dispatcher- und
Collector-Path-Substitution-Regressionen, die strikte Ablehnung boolescher
Schema-Versionen sowie Environment-Variable-only-Handling der übergebenen
PR-Nummer und erwarteten SHA bestanden. Candidate-Task-/Build-/Output-
Directory-Swap-Regressionen bestanden ebenfalls: Ersatzverzeichnisse werden
nicht verwendet und ersetzte Task-/Output-Identitäten vor der Rückgabe eines
Package-Pfads fail-closed abgelehnt. Python-Kompilierung und Shell-
Syntaxprüfungen bestanden.
`actionlint` bestand für `.github/workflows/run-protected-nginx-exact-head.yml`.
Eine lokale Bubblewrap-Mount-Layout-Probe wird durch die Namespace-Policy dieses
Containers blockiert und nicht als Host-Runtime-Ergebnis behauptet. Ein
gehosteter NGINX-Runtime-Lauf, geschützte Environment, dedizierter Runner und
unabhängige Attestierung waren lokal nicht verfügbar und bleiben blockierte
externe Evidence.

Ausschließlich Vorbereitung — keine Merge-Autorisierung.
