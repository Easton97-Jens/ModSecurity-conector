# Change Record

**Sprache:** [English](CR-20260822-nginx-updater-workflow-publication.md) | Deutsch

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | CR-20260822-nginx-updater-workflow-publication |
| Datum (UTC) | 2026-08-22 |
| Basis-Revision | `c8881eaadf7d3ef5d4173d581a62726a2df3fdf2` |
| Lieferstatus | Auf einem dedizierten Branch und Pull Request vorbereitet; kein Merge wird behauptet. |

## Motivation und Problemstellung

Der Framework-Update-Lauf `32557767129` validierte den Kandidaten
`52fe6ee334f1381c35d5c3b7140433c626469523` einschließlich NGINX `1.31.4`.
Der Publisher-Push wurde jedoch abgelehnt, weil dem eingebauten
Workflow-Token die Berechtigung zum Ändern von
`.github/workflows/nginx-root-broker.yml` fehlte.

## Akzeptanzkriterien

NGINX muss in seinem eigenen geschützten Root-Broker-Workflow bleiben; das geprüfte Release-Tupel muss auf `release-1.31.4`, `nginx-1.31.4.tar.gz` und den registrierten SHA-256 wechseln; Validierungsjobs dürfen kein Publisher-Credential erhalten; und die Änderung bleibt ein Draft-PR ohne Auto-Merge.

## Implementierungsentscheidung und Begründung

Der dedizierte, unveränderlich gepinnte NGINX-Root-Broker bleibt
bestehen. Der Submodule-Publisher verwendet das eingebaute Token
weiterhin nur für Pull-Request-Metadaten und nutzt die bestehende,
repository-begrenzte Workflow-Publisher-GitHub-App ausschließlich für
Git-Pushes, die geprüfte Workflow-Pin-Änderungen enthalten können. Das
eingebaute Token verliert `contents: write`; es werden weder Auto-Merge
noch eine veränderliche Reusable-Workflow-Referenz oder eine breitere
Root-Grenze eingeführt.

## Geänderte Dateien

- Framework-Gitlink und registrierte Parent-Pins werden auf den
  validierten Kandidaten synchronisiert, einschließlich NGINX
  `release-1.31.4`.
- Der bestehende Workflow-Publisher-App-Token wird nur mit
  `contents:write` und `workflows:write` für die Git-Veröffentlichung
  erzeugt.
- `github.token` bleibt für Draft-PR-Identität und Metadatenoperationen
  erhalten.
- Statische Regressionstests sichern die getrennte Token-Grenze ab.
- Das NGINX-Archive-Cache-Identity-Fixture wird auf das registrierte `1.31.4`-Release-Tupel ausgerichtet.

## Ausgeführte Befehle

Der Branch-Bootstrap führt den exakten Komponenten-Synchronisierer in
den Modi `--sync` und `--check` aus, regeneriert Compiler-Leitfäden,
führt die fokussierten Updater- und CI-Security-Unittests sowie den
aggregierten CI-Security-Contract aus, prüft die zweisprachige
Dokumentation und führt `git diff --check` aus. Nach der PR-Erstellung
bleiben die Hosted-PR-Checks maßgeblich.

## Security-Auswirkung

Der NGINX-Root-Broker bleibt von den anderen Connectoren getrennt und
weiterhin über eine unveränderliche SHA gepinnt. Die Berechtigung zum
Schreiben von Workflow-Dateien erhält nur die bereits konfigurierte,
repository-begrenzte Publisher-App während des isolierten
Publisher-Jobs; Validierungsjobs erhalten keine
Veröffentlichungs-Credentials.

## Runtime-Evidence

Im Bootstrap-Lauf `32573726344` bestanden alle `48` fokussierten Tests und alle `122` aggregierten CI-Security-/Submodule-Tests. Der Lauf stoppte ausschließlich am hier korrigierten zweisprachigen Change-Record-Schema. Das synchronisierte NGINX-Tupel ist `release-1.31.4`, `nginx-1.31.4.tar.gz` und SHA-256 `e6f20b644a17a643f059ae6467a1971fe2811587d025e071068753a1f1e3b3c3`.

Der Exact-Head-Folgelauf `32574140575` bestand alle `29` Framework-Protocol-Client-Tests und zeigte ausschließlich das veraltete, noch an `1.31.3` gebundene Parent-Cache-Identity-Fixture. Diese Reparatur richtet das Fixture auf `1.31.4` aus; der fokussierte Cache-/Protocol-Contract und der aggregierte CI-Security-Contract werden vor der erneuten Veröffentlichung des Ein-Commit-Branches erfolgreich ausgeführt.

## Bekannte Einschränkungen

Nach dem Merge dieses Updates benötigt der geschützte NGINX-Caller
weiterhin einen separaten geprüften Repin auf den resultierenden
gemergten Broker-Commit und die Framework-Kandidaten-SHA. Diese
zweistufige Aktivierung bewahrt die unveränderliche Broker-
Vertrauensgrenze.

## Verbleibende Risiken

Die finale Exact-Head-Hosted-Matrix, GitHub-Autorisierung für Workflow-Dateien und der Protected-master-NGINX-Lifecycle benötigen weiterhin Hosted-Evidence. Ein Fehler blockiert die Delivery und erlaubt keine veränderlichen Workflow-Refs oder PR-kontrollierte Root-Ausführung.

## Nicht ausgeführte Prüfungen mit Begründung

Die vollständige Connector-Matrix des final umgeschriebenen Commits, Review-/Branch-Protection-Gates, Merge und der Protected-master-Aufruf nach dem Merge können vor finaler Veröffentlichung und geprüfter Integration nicht behauptet werden.

## Finaler Diff- und Review-Status

PR #317 bleibt offen und Draft. Der finale Commit wird ohne die temporären Bootstrap-Workflows direkt auf Basis-Revision `c8881eaadf7d3ef5d4173d581a62726a2df3fdf2` erzeugt. Weder Merge noch Ready-for-Review-Übergang oder Protected-Caller-Aktivierung werden behauptet.
