# Vertrauenswürdiger NGINX-Root-Broker

**Sprache:** [English](trusted-nginx-root-broker.md) | Deutsch

Der vertrauenswürdige NGINX-Root-Broker ist ein bewusst enger
wiederverwendbarer GitHub-Actions-Workflow. Er ist die einzige geplante
privilegierte Grenze für den NGINX-Master-/Worker-Nachweis im F-GS-003-
Lieferweg. Er ist kein allgemeiner Root-Command-Runner: PR-240-Code,
Framework-Skripte aus einem PR-Checkout, Caller-Shellfragmente,
Konfigurations-/Regeldateien, CRS-Pfade, Binaries, Module und generierte
Umgebungsdateien laufen niemals als Host-root.

## Unveränderliche Aufrufgrenze

Der Caller verwendet den wiederverwendbaren Workflow über den exakten
40-stelligen Commit-SHA, der bereits vom geschützten Parent-`master` erreichbar
ist:

```yaml
uses: Easton97-Jens/ModSecurity-conector/.github/workflows/nginx-root-broker.yml@1df2fcbd0c764c52253348a29034ff9e9b1bf7e2
```

Beide Caller-`uses`-Werte und beide `protected_broker_sha`-Werte sind an den
resultierenden geschützten Broker-Repair-Commit-SHA
`1df2fcbd0c764c52253348a29034ff9e9b1bf7e2` gepinnt; weder ein Branch noch
`master` sind zulässige Alternativen.

GitHub dokumentiert, dass der `github`-Kontext in einem aufgerufenen
wiederverwendbaren Workflow einschließlich `github.workflow_ref` seinem Caller
zugeordnet ist. Der Broker behandelt diesen Wert daher ausschließlich als die
exakte Caller-Identität
`Easton97-Jens/ModSecurity-conector/.github/workflows/run-protected-nginx-root-broker.yml@refs/heads/master`
und nicht als Identität von `.github/workflows/nginx-root-broker.yml`. Der
unveränderliche `uses`-SHA wählt den called Workflow aus; GitHub empfiehlt
einen Commit-SHA als sicherste Referenz. Die
[Reusable-Workflow-Referenz](https://docs.github.com/en/actions/reference/workflows-and-actions/reusing-workflow-configurations)
und die [Contexts-Referenz](https://docs.github.com/en/actions/reference/workflows-and-actions/contexts)
definieren diese Semantik.

Vor dem Broker-Checkout akzeptiert ein festes Shell-Gate nur den exakten
Same-Repository-`workflow_dispatch`-Caller-Kontext: kanonisches Repository,
Nicht-Fork, `refs/heads/master`, Default-Branch `master`, exakte
Caller-Workflow-Referenz und kanonisches `github.sha`. Falls
`github.workflow_sha` verfügbar ist, muss es ebenfalls kanonisches SHA-40 sein
und `github.sha` entsprechen; andernfalls wird der Caller-Commit über
`github.sha` und sein Gitobjekt gebunden, ohne eine positive Prüfung zu
erfinden. Der Broker validiert separat kanonisches `protected_broker_sha` und
checkt dann exakt diesen Broker-SHA ohne persistierte Credentials und mit voller
Historie aus. Dieser Checkout dient ausschließlich dazu, die Protected-`master`-
Abstammung zu belegen, das Caller-Gitobjekt abzufragen und die Brokerquelle zu
binden; die Caller-YAML-Validierung ist vor jedem Manifest-Download, Build,
Candidate-Erzeugen oder jeder Root-Aktion abgeschlossen. Der Broker beweist,
dass der Caller-Commit existiert, auf geschütztem `master` liegt und vom
Broker-Commit abstammt.

Die Caller-Workflowdatei wird vom Broker niemals ausgecheckt, gesourct oder
ausgeführt. Der Broker liest nur ihren festen Pfad als begrenzten regulären
`100644`-Gitblob aus dem Caller-Commit mittels `git cat-file` und parst dann
eine bewusst eingeschränkte deklarative YAML-Teilmenge. Er weist doppelte
Schlüssel, Anchors, Aliase, Tags, Merge-Keys, Flow-Syntax, unsichere
Kodierungen, fehlerhafte Verschachtelung und unerwartete Jobschemata ab. Nur
exakt `run-no-crs-broker` und `run-with-crs-broker` dürfen den Broker aufrufen;
beide müssen denselben Literal-SHA-40 gleich `protected_broker_sha`, die exakte
Variante, exakte Inputs und ausschließlich `contents: read` ohne Secrets oder
zusätzlichen Reusable-Job verwenden.

Der Broker bindet den ausgecheckten Framework-HEAD und Input an den im
Broker-Commit aufgezeichneten `160000`-Framework-Gitlink und fordert saubere
rekursive Submodule. Er prüft sowohl
`.github/workflows/nginx-root-broker.yml` als auch
`ci/runtime/broker/nginx_root_broker.py` als reguläre Nicht-Symlink-Dateien,
deren Gitblobs vor der Caller-YAML-Validierung, nach Setup- oder
Build-Aktivität, vor der Candidate-Erzeugung und unmittelbar vor jeder
Root-Aktion dem Broker-Commit entsprechen. Python bleibt für Root-Aktionen
isoliert.

Keiner der Workflows gewährt `id-token: write`; die beobachtete Token-Grenze
ist auf `Contents: read` und `Metadata: read` begrenzt. Dieser Gitobjekt- und
deklarative YAML-Vertrag macht eine OIDC-Alternative überflüssig.

Kein `@master`, kein PR-Branch-Ref, kein lokales `uses: ./`, kein
`pull_request_target`, kein Fork-Kontext, kein breites `sudo`, kein
`sudo -E`, kein `sudo sh -c`, kein `sudo bash -c`, kein Shell-Callback,
kein Command-String und kein vom Caller vorgegebener Ausführungspfad gehören zu
diesem Vertrag.

### Beobachtete fail-closed Abweichung

[Run `31310183097`](https://github.com/Easton97-Jens/ModSecurity-conector/actions/runs/31310183097)
war ein `workflow_dispatch` von `master` bei Caller-SHA
`128a2f63f182758b1c1a1d4746f5e56f609d245d`. Seine Manifestvorbereitung war
erfolgreich, doch beide Brokerprofile scheiterten im früheren Binding-Schritt
und der Evidence-Readback wurde übersprungen. Die alte Prüfung erwartete
`Easton97-Jens/ModSecurity-conector/.github/workflows/nginx-root-broker.yml@e06254ea9622d214a9030b9ba786756560ace417`,
während GitHub die tatsächliche Caller-Referenz
`Easton97-Jens/ModSecurity-conector/.github/workflows/run-protected-nginx-root-broker.yml@refs/heads/master`
lieferte. Der Fehler war korrekt fail-closed, verglich jedoch Identitäten aus
verschiedenen Schichten. Er trat vor geschütztem Broker-Checkout, Build,
CRS-Erzeugung, `sudo`, Root-Admission, NGINX-Start, Artefaktprojektion und
Cleanup auf. Er ist ausschließlich Caller-Kontext-Evidence und keine Root-,
NGINX-, CRS-, Worker-, Artefakt- oder Cleanup-PASS-Evidence.

## Geschützter resulting-master-Caller

Der nur wiederverwendbare Broker kann selbst keine resulting-`master`-
Runtime-Evidence erzeugen. Der getrennte Workflow `Protected NGINX Root Broker
Lifecycle` unter `.github/workflows/run-protected-nginx-root-broker.yml`
liefert diesen engen Einstiegspunkt. Er besitzt ausschließlich
`workflow_dispatch`, akzeptiert ausschließlich das erforderliche
`parent_head_sha`, erhält nur `contents: read` und hat eine nicht abbrechende
workflowweite Concurrency-Gruppe. Jeder Caller-Job fordert das kanonische
Nicht-Fork-Repository, ein `workflow_dispatch`-Event und `refs/heads/master`
als geschützten Default-Branch.

`parent_head_sha` ist eine deklarative Evidence-Identität und kein
Source-Selektor. Der unprivilegierte Vorbereitungsjob akzeptiert ausschließlich
lowercase SHA-40, bestätigt den Commit über einen festen read-only-GitHub-API-
Endpunkt und bindet ihn in die zwei Caller-Manifeste. Er checkt diesen Commit
nicht aus, importiert, sourct, baut, startet, lädt oder root-exekutiert ihn
nicht. Der Caller checkt nur seinen geschützten aktuellen Master-Source aus,
um den geprüften reinen Datenhelper auszuführen. Die einzigen Root-Aktionen
bleiben im folgenden unveränderlichen Aufruf; der Framework-Gitlink ist an die
Broker-Revision und nicht an einen späteren Parent-Stand gebunden:

```yaml
uses: Easton97-Jens/ModSecurity-conector/.github/workflows/nginx-root-broker.yml@1df2fcbd0c764c52253348a29034ff9e9b1bf7e2
```

```text
protected_broker_sha = 1df2fcbd0c764c52253348a29034ff9e9b1bf7e2
framework_sha        = 03880bf66b3905940466ff10b3a431a27ecc6b26
```

Der Caller erstellt zwei explizite unveränderliche Aufrufe und niemals eine
benutzergewählte Matrix: `no-crs` mit Profil `no-crs` sowie `with-crs` mit
Profil `owasp-crs`. Für jede feste Run-ID erzeugt er ein privates,
deterministisches, vor dem Upload erneut geparstes Manifest-Artefakt. Jedes
Artefakt enthält ausschließlich `caller-manifest.json`, wird einen Tag
aufbewahrt und dem passenden unveränderlichen Reusable-Aufruf übergeben.

Der Helper akzeptiert keinen vom Caller gewählten Manifest- oder Evidence-
Dateisystempfad. Er leitet die zwei festen Verzeichnis-Roots ausschließlich
aus dem vom Runner bereitgestellten absoluten, nicht-symlinkenden
`RUNNER_TEMP`-Verzeichnis und den validierten gepaarten Run-IDs
`protected-nginx-root-…-no-crs` / `protected-nginx-root-…-with-crs` ab. Eine
fehlende, relative, symlinkende, fehlerhafte oder nicht passende Pfadidentität
schlägt vor API-Zugriff, Artefakterzeugung oder Evidence-Readback fehl. Beide
abgeleiteten Roots müssen zusätzlich eigenständig nicht-symlinkende
Verzeichnisse sein.

## Versionierter deklarativer Caller-Vertrag

Die wiederverwendbare Workflow-Schnittstelle besitzt exakt sechs Inputs:

- `caller_manifest_artifact`
- `parent_head_sha`
- `framework_sha`
- `protected_broker_sha`
- `matrix_variant`
- `run_id`

Diese Call-Inputs unterscheiden sich vom Schema-v2-JSON-Manifest. Schema v2
besitzt exakt sieben Felder; das zusätzliche Feld ist das geschlossene
`policy_profile`:

Schema v1 bleibt der reproduzierbare No-CRS-Kontrollvertrag. Schema v2
akzeptiert exakt die v1-Identitätsfelder plus `policy_profile`:

- `schema_version`
- `run_id`
- `matrix_variant`
- `policy_profile` (nur Schema v2)
- `parent_head_sha`
- `framework_sha`
- `protected_broker_sha`

Das Profil ist geschlossen und an die Variante gebunden: `no-crs` wählt das
geschützte `no-crs`-Profil, während `with-crs` `owasp-crs` wählt. Unbekannte
Schema-Versionen, Profile, Felder und Profil-/Variant-Kombinationen schlagen
fail-closed fehl. Der Caller kann weder CRS-Source-/Konfigurationspfad,
Regelinclude, Ref, Commit, Bundle-Digest, ModSecurity-Direktive, Command noch
Umgebungswert wählen. Ein Runtime-Environment-Snapshot wird nur als
deklarativer Text geparst; er wird niemals als Shellcode gesourct.

## Geschützter Runtime-Snapshot-Vertrag

Der Broker akzeptiert ausschließlich einen privaten Record mit fester Provenance
unter `build/runtime-component-reports/trusted-nginx-broker-provenance.json`
und seinen passenden privaten Snapshot. Der Snapshot exportiert exakt diese
drei Werte und keine weiteren:

- `NGINX_BINARY`
- `NGINX_MODULE`
- `MODSECURITY_SHARED_PREFIX`

Vor der Admission validiert der Broker die Pfade, Digests, Metadaten sowie die
Parent- und Framework-Identitäten des Records. Ein generischer Runtime-Snapshot
oder ein direkter Harness-Environment-Override wird an der Broker-Grenze nicht
akzeptiert. Der aktive Caller pinnt die Broker-Revision, die diesen geschützten
Snapshot-Vertrag enthält; ein resultierender Parent-master-Dispatch wählt ihn
damit direkt.

## Geschützte Artefakte und CRS-Bundle

Der Workflow baut das geprüfte NGINX-Binary, das ModSecurity-NGINX-Modul und
die ModSecurity-Shared-Library ohne root aus dem ausgecheckten geschützten
Source. Für Schema-v2-`owasp-crs` erzeugt er zusätzlich eine frische private
CRS-Source-Root und verwendet den kanonischen Fresh-Source-Weg des exakten
Framework-Gitlinks. Die Broker-Revision prüft dieses geprüfte Tupel unabhängig:

| Feld | Fester Wert |
| --- | --- |
| Repository | `https://github.com/coreruleset/coreruleset.git` |
| Release-Tag | `v4.28.0` |
| Commit | `55b09f5acfd16413e7b31041100711ceb7adc89c` |
| Erwartete CRS-Blockregel | `949110` |

### ABI-Loader-Vertrag für die nächste Broker-Revision

Das gewöhnliche ModSecurity-Präfix darf Libtools unversionierten Linker-Alias
`libmodsecurity.so` behalten, aber dieser Alias ist üblicherweise ein Symlink
und kein vertrauenswürdiges Runtime-Artefakt. Die nächste unveränderliche
Broker-Revision löst die Libtool-Aliasse descriptor-relativ auf und fordert,
dass jeder erwartete Alias ein direktes Basename-Ziel enthält. Beide Aliasse
müssen sich auf dasselbe reguläre Terminalobjekt auflösen. Die geschützte
reguläre Kopie `prefix/lib/libmodsecurity.so.3` wird über den an dieses
validierte Terminal gebundenen Deskriptor erzeugt, sodass weder ein
Nested-Symlink-Escape noch ein Austausch die Kopie umleiten kann.
Producer-Provenance, Candidate-Manifest, root-owned Artefaktverzeichnis und
`LD_LIBRARY_PATH` binden anschließend alle diesen ABI-SONAME-Namen. An der
geschützten Producer-, Candidate- oder Root-Grenze wird kein Symlink
zugelassen.

Nur für diesen geschützten Build verhindert der feste Workflow-Wert
`NGX_IGNORE_RPATH=YES`, dass das explizit angegebene ModSecurity-
Library-Verzeichnis zu einem dynamischen Suchpfad des NGINX-Moduls wird. Vor
der Candidate-Erstellung untersucht der Broker sowohl das geprüfte Modul als
auch `libmodsecurity.so.3` mit dem festen absoluten Tool `/usr/bin/readelf`
und leerem `PATH`, begrenzter Ausgabe sowie einer realen begrenzten Deadline.
Für jedes der beiden ELFs blockieren `DT_RPATH`, `DT_RUNPATH`, ein Slash
enthaltendes `DT_NEEDED` oder jeder Eintrag `DT_AUDIT`, `DT_DEPAUDIT`,
`DT_FILTER` beziehungsweise `DT_AUXILIARY` die Admission; dasselbe gilt für
eine fehlgeschlagene Untersuchung oder Nicht-Text-Ausgabe. Diese Untersuchung
läuft unprivilegiert und endet vor der Candidate-Erstellung sowie jeder
Root-Aktion. Diese Prüfungen sind Teil der ausstehenden Broker-Reparatur und
kein Nachweis, dass der aktuell gepinnte Caller einen Runtime-Lifecycle
abgeschlossen hat. Ein separater unveränderlicher Caller-Repin und ein neuer
Protected-master-Lauf bleiben erforderlich.

Das Bundle-Manifest bindet das Tupel, den Framework-Gitlink, den
Broker-Commit, Erzeugungszeitpunkt, sortierte erlaubte Dateirecords,
Dateianzahl und Gesamtdigest. Nur `crs-setup.conf.example`, `rules/*.conf`
und die geschlossenen Plugin-Konfigurationsformen sind zulässig. Ein Record
enthält einen portablen relativen Pfad, SHA-256, Größe, Modus, Typ,
Broker-Commit und CRS-Commit. Symlinks, zusätzliche Dateien, Hardlinks,
Sonderdateien, ausführbare Regeldateien, Traversal, absolute Pfade, doppelte
Records und bewegliche Refs werden abgewiesen.

Bei der Admission liest root nur das manifestierte Bundle aus dem festen
geschützten Build-Layout mit descriptor-relativen Opens und `O_NOFOLLOW`. Es
prüft Owner, Mode, Device, Linkcount, Inode-/Größenstabilität und Digest vor
und nach dem Kopieren. Die einzige materialisierte CRS-Konfiguration ist
root-owned und read-only unter der privaten Root des aktuellen Broker-Runs;
NGINX oder ModSecurity lädt keinen Caller-Pfad.

## Feste Profile und Aktionen

Nur diese Root-Aktionen existieren:

- `validate-manifest`
- `config-test`
- `start`
- `verify-runtime-profile`
- `verify-master-worker-identity`
- `project-evidence`
- `stop`
- `cleanup-status`

Der Broker schreibt NGINX-Konfiguration, Regeldatei und Dokument selbst. Er
startet genau einen Root-Master nur auf Loopback und einem nicht privilegierten
Port, fordert genau einen getrennten Nicht-root-Worker mit dem zugelassenen
Binary-Inode und prüft vor dem Cleanup, dass Prozessgruppe und Listener
verschwunden sind.

Das `no-crs`-Profil behält ausschließlich die Broker-eigene `/blocked`-
Kontrollregel und trägt kein scheinbares CRS-Tupel. Das `owasp-crs`-Profil
schreibt die portable serielle Audit-Konfiguration und feste Includes für das
root-owned CRS-Bundle. Es verwendet die kanonische CRS-Smoke-Anfrage des
Frameworks `/?id=1%20UNION%20SELECT%20password%20FROM%20users`, fordert einen
200-Allow und einen 403-Block und weist den Lauf ab, sofern der private Audit-
Record nicht Run, Anfrage, Transaction, Status, Bundle-Digest und CRS-Regel
`949110` bindet.

Candidate- und Final-Manifest tragen das ausgewählte Profil. Ein
`owasp-crs`-Final-Manifest enthält zusätzlich Repository/Tag/Commit,
Bundle-Manifest- und Gesamtdigests, Dateianzahl, root-lokale Bundle-/Audit-
Pfade, erwartete Regel-Evidence und geschützte Producer-Bindungen. Ein
No-CRS-Manifest darf diese CRS-Felder nicht tragen.

## Evidence- und Cleanup-Grenze

Die Root-zu-Runner-Projektion hat eine exakte profilabhängige Allowlist. Schema
v2 projiziert `identity.json`, `runtime.json`, `policy.json`, Access-/Error-
Logs und für `owasp-crs` zusätzlich `nginx-audit.log`. Die Projektion nutzt
no-follow-Opens, Owner-/Mode-/Device-/Größenprüfungen, temporäre Ausgabe und
atomare Veröffentlichung. Ein geschützter Nicht-root-Workflow-Schritt kopiert
nur diese feste Liste vor dem descriptor-relativen Cleanup aus der
run-spezifischen Root heraus. Er ergänzt ein festes `cleanup.json` erst
nachdem `cleanup-status` zurückkehrt; es enthält gebundenen Broker-SHA, Run-ID,
Variante und PASS/FAIL-Cleanup-Ergebnis.

`runtime.json` meldet `root_broker_status: PASS` erst nachdem der eigene
Root-/Master-/Worker-/Artefakt-Lifecycle des ausgewählten Profils bestanden
hat. Für `owasp-crs` enthält dieses Ergebnis zusätzlich das feste CRS-Tupel
und die Bundle-Identität; es ist kein Apache-Ergebnis und ein bloßer HTTP 403
genügt nicht.

Anschließend lädt der Caller nur die zwei Run-gebundenen Broker-Artefakte in
einem unprivilegierten Evidence-Readback-Job herunter. Er fordert die exakte
profilabhängige Dateimenge, weist unbekannte JSON-Felder und Symlinks ab und
bindet beide Run-IDs, den deklarativen Parent-SHA, die unveränderlichen
Broker-/Framework-SHAs, Root-Master- und Nicht-root-Worker-Identitäten,
`PASS`-Cleanup sowie für `owasp-crs` Bundle-/Audit-Digest. Das No-CRS-Artefakt
darf keine Auditdatei enthalten. Sein finaler Always-Run-Ergebnisjob schlägt
fehl, falls Manifestvorbereitung, eines der Brokerprofile oder Evidence-
Readback nicht erfolgreich waren; er kann keinen fehlgeschlagenen Brokerjob
grün überdecken.

## Validierungsgrenze

Lokale fokussierte Tests decken Schema-/Profil-Ablehnung, Provenance,
Bundle-Pfad- und Dateisicherheit, feste root-generierte Konfiguration,
stale/fehlende Audit-Evidence, IPv6-Loopback, Workflow-Pins/-Kontext,
begrenztes Evidence-Staging und descriptor-relativen Cleanup ab. Nach der
anfänglichen Loader-Reparatur bestanden 83 fokussierte Tests. Nach der
erweiterten Security-Remediation bestand eine spätere Broker-/CRS-Suite 43
Tests, die fokussierte Remediation bestand 2 Tests und die fokussierte
Producer-Matrix bestand 5 Tests. Das vollständige owning Cache-Modul bestand
38 Tests und hatte einen bekannten Isolated-Worktree-Fixture-Fehler. Dies sind
lokale Source-/Static-Ergebnisse. Ein Protected-master-Hosted-Aufruf bleibt
erforderlich, um GitHub-Reusable-Workflow-Kontextsemantik, einen realen
Root-Master/Nicht-root-Worker, reale CRS-Ausführung, Audit-Ausgabe,
Listener-Freigabe und die endgültig hochgeladene Cleanup-Evidence zu beweisen.
Dieses Dokument ist ein Sicherheitsvertrag, nicht diese Runtime-Evidence.

PR #240 bleibt blockiert, bis dieser Caller normal gemergt, vom resultierenden
geschützten `master` gestartet und mit erfolgreichen `no-crs`- sowie
`owasp-crs`-Profilen einschließlich Evidence-Readback und Cleanup beobachtet
wurde. Ein späterer Dispatch darf den finalen PR-240-Head nur als deklarative
Evidence binden; er führt niemals PR-240-Code an der Root-Grenze aus.
