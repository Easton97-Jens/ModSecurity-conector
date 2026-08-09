# Vertrauenswürdiger NGINX-Root-Broker

**Sprache:** [English](trusted-nginx-root-broker.md) | Deutsch

Der vertrauenswürdige NGINX-Root-Broker ist ein bewusst enger
wiederverwendbarer GitHub-Actions-Workflow. Er ist die einzige geplante
privilegierte Grenze für den im F-GS-003-Lieferweg verlangten
NGINX-Master-/Worker-Nachweis. Er ist kein allgemeiner Root-Command-Runner und
autorisiert weder PR-240-Code noch Binaries, Module, Shellfragmente oder
generierte Umgebungsdateien als Host-root.

## Unveränderliche Aufrufgrenze

Der Caller muss den wiederverwendbaren Workflow über den exakten
40-stelligen Merge-SHA verwenden, der bereits vom geschützten Parent-`master`
erreichbar ist:

```yaml
uses: Easton97-Jens/ModSecurity-conector/.github/workflows/nginx-root-broker.yml@<broker-merge-sha>
```

Der Broker akzeptiert nur Same-Repository-`workflow_dispatch`- oder
zeitgesteuerte Kontexte, hat eine read-only-`contents`-Berechtigung, prüft den
aufgerufenen Workflow-Ref, checkt den exakten Broker-SHA ohne persistierte
Credentials aus und prüft, dass der SHA ein Vorfahr des aktuellen `master`
ist. Unmittelbar vor jeder privilegierten Aktion vergleicht er den aktuellen
Git-Blob des Broker-Helfers mit dem Blob dieses geschützten SHA und ruft Python
im isolierten Modus auf.

Kein `@master`, kein PR-Branch-Ref, kein lokales `uses: ./`, kein
`pull_request_target`, kein Fork-Kontext, kein breites `sudo`, kein `sudo -E`,
kein Shell-Callback, kein Command-String und kein vom Caller vorgegebener
Ausführungspfad gehören zu diesem Vertrag.

## Deklarativer Caller-Vertrag

Das Caller-Artefakt enthält genau ein begrenztes JSON-Objekt mit exakt diesen
Feldern:

- `schema_version`
- `run_id`
- `matrix_variant`
- `parent_head_sha`
- `framework_sha`
- `protected_broker_sha`

Der Workflow bindet alle sechs Felder an seine eigenen Inputs. Das Manifest
enthält kein Command-, Shell-, Argumentlisten-, Konfigurationspfad- oder
Umgebungsfeld. Ein Runtime-Environment-Snapshot wird nur als deklarativer Text
geparst; er wird niemals als Shellcode gesourct.

## Geschützte Artefakte und feste Aktionen

Der Broker baut das geprüfte NGINX-Binary, das ModSecurity-NGINX-Modul und die
ModSecurity-Shared-Library ohne root aus dem ausgecheckten geschützten Source.
Er hasht die Artefakte, kopiert sie mit no-follow-Descriptor-Prüfungen in einen
frischen root-owned privaten Run-Tree und hasht jedes Artefakt erneut vor der
NGINX-Ausführung. Das finale Manifest fixiert jeden Artefakt-, Runtime-, PID-,
Log- und Evidence-Pfad unter diesem einen Run-Tree. Der privilegierte Parent
ist fest `/var/lib/msconnector-nginx-root-broker`, root-owned und nur für die
Runner-Gruppe durchsuchbar; weder Caller noch ein Broker-CLI-Argument können
ihn auswählen.

Nur diese Root-Aktionen existieren:

- `validate-manifest`
- `config-test`
- `start`
- `verify-master-worker-identity`
- `project-evidence`
- `stop`
- `cleanup-status`

Der Broker schreibt NGINX-Konfiguration, Regel und Dokument selbst. Er startet
genau einen Root-Master nur auf Loopback und einem nicht privilegierten Port,
fordert genau einen Nicht-root-Worker mit der konfigurierten UID/GID und dem
zugelassenen Binary-Inode und prüft vor dem Cleanup, dass Prozessgruppe und
Listener verschwunden sind.

## Evidence- und Cleanup-Grenze

Nur vier root-seitige Dateien dürfen zum Runner übertreten: `identity.json`,
`runtime.json`, `nginx-access.log` und `nginx-error.log`. Die Projektion nutzt
eine feste Allowlist, no-follow-Opens, Owner-/Mode-/Device-/Größenprüfungen,
temporäre Ausgabe und atomare Veröffentlichung. Nach dem Upload entfernt der
Cleanup genau den run-spezifischen Root-Tree descriptor-relativ; er verändert
niemals rekursiv einen Repository-, Cache- oder Systempfad.

`runtime.json` meldet `root_broker_status: PASS` nur für den eigenen
Root-/Master-/Worker-/Artefakt-Lifecycle des Brokers. Ein `matrix_variant`
wird für run-gebundene Attribution festgehalten, aber der Broker trifft bewusst
keine CRS-Aussage. Frische CRS-Source-Materialisierung und CRS-Verhalten
bleiben separate PR-240-Controls und müssen unabhängig belegt werden.

## Validierungsgrenze

Lokale fokussierte Tests decken Schema-Ablehnung, SHA-/Run-/Variant-Bindungen,
Artefaktpfad-/Digest-Prüfungen, no-follow-Sonderdatei-Ablehnung, feste Aktionen,
Workflow-Pins/-Kontext und descriptor-relativen Cleanup ab. Ein
Protected-master-Hosted-Aufruf ist weiterhin erforderlich, um den
GitHub-Reusable-Workflow-Kontext, die reale Root-/Master-/Worker-Identität,
Listener-Freigabe und Artefaktprojektion auf einem tatsächlichen Hosted Runner
zu validieren. Dieses Dokument ist ein Sicherheitsvertrag, nicht diese
Runtime-Evidence.
