# Geschütztes Exact-Head-Host-Gate

**Sprache:** [English](protected-exact-head-host-gate.md) | Deutsch

Der privilegierte Job verwendet absichtlich einen vorinstallierten
Host-Bootstrap unter:

`/usr/local/libexec/modsecurity-protected-exact-head/run-exact-base-launcher`

Der Bootstrap ist Plattform-Infrastruktur und kein Pull-Request-Code. Vor der
Ausführung eines Base-Launchers MUSS er:

1. eine reguläre Datei `root:root` mit Modus `0755` und ohne symbolische
   Pfadkomponente sein;
2. jeden Python-Entrypoint anhand von `--trusted-base-sha` und
   `--entrypoint-relative-path` aus dem geschützten Base-Checkout lesen, das
   Git-Objekt und den Checkout-Commit prüfen und eine private, root-eigene
   Momentaufnahme erstellen;
3. die Umgebung bereinigen und die Momentaufnahme als root ausführen, wobei
   nur Argumente nach `--` weitergereicht werden;
4. fehlende, fehlerhafte, nicht passende, beschreibbare oder veränderliche
   Eingaben ablehnen.

Die Entrypoint-Allowlist des Gates ist exakt und geschlossen:

- `ci/runtime/broker/nginx_exact_head_root_launcher.py`
- `ci/runtime/broker/nginx_exact_head_result_collector.py`

Jeder andere Wert von `--entrypoint-relative-path` MUSS abgelehnt werden,
auch Pfade, die erst durch Normalisierung einem erlaubten Pfad entsprechen.
Der angegebene Base-Repository-Root MUSS ein absoluter, normalisierter,
symlinkfreier Verzeichnisbaum sein, dessen verifiziertes Git-`HEAD` der
`--trusted-base-sha` entspricht. Das Gate MUSS alle weitergereichten Optionen
vor dem Snapshot parsen und prüfen, unbekannte Gate-Optionen ablehnen und nur
Argumente nach dem alleinstehenden `--` weiterreichen.

Der Workflow verwendet dasselbe Gate für
`ci/runtime/broker/nginx_exact_head_root_launcher.py` und
`ci/runtime/broker/nginx_exact_head_result_collector.py`, stets mit der
exakten Base-SHA. Er gibt `sudo` niemals für einen Python-Pfad aus Checkout
oder Task-Root frei und führt nach dem Collector keine privilegierte
Pfadoperation aus. Das Runner-Preflight bricht außerdem ab, wenn das Gate
fehlt oder Eigentümer, Gruppe, Modus bzw. Dateityp nicht stimmen.

Die beiden erlaubten Parent-Pfade sind jetzt kleine Entrypoints für die
Quellintegration. Der umfangreiche Launcher, Collector, Dispatcher und
Zelltreiber gehören zum gepinnten Test-Framework unter
`connector_suite/modsecurity_connector_ci/runtime/broker/`. Die Shims prüfen
`ci/run-trusted-framework.py` vor Ausführung seiner Bytes anhand ihres
geprüften `BRIDGE_SHA256`. Diese Brücke bestimmt die Framework-Revision
ausschließlich aus dem Gitlink `modules/ModSecurity-test-Framework` der exakt
vertrauten Parent-Base, prüft beide Checkout-Identitäten und vergleicht die
angeforderte Implementierung mit ihrem exakten Framework-Git-Blob.
Vom Kandidaten ausgewählte Framework-Revisionen, veränderte
Implementierungsbytes, symbolische Quellpfade, nichtreguläre Dateien und
übergroße Quellen werden abgelehnt.

Bei einem Aufruf als root laufen Git-Prüfungen über `/usr/bin/setpriv` unter
der explizit angegebenen Nicht-root-Identität `--runner-uid` und
`--runner-gid`, ohne Zusatzgruppen oder Capability-Sets und mit
`--no-new-privs`. Authentifizierte Python-Bytes gelangen über einen versiegelten
`memfd` in einen neuen isolierten Interpreter. Kandidatenimporte oder
Änderungen an `sys.path` bzw. `sys.modules` sind nicht erforderlich. Der
Launcher bindet den Shell-Zelltreiber zusätzlich an den Framework-Blob des
vertrauten Parent-Gitlinks und hält dessen Deskriptor während des
Sandbox-Aufbaus offen.

Beide Shim-Aufrufe übergeben nach dem `--`-Trennzeichen des Gates explizit
`--base-repo-root` und `--trusted-dispatcher-base-sha`, zusätzlich zu den
bisherigen Evidenz- und Runner-Argumenten des Entrypoints. Der Collector-Shim
verarbeitet diese beiden Optionen zur Quellenbindung vor dem Aufruf des
Framework-Collectors. Host-Eigentümer müssen die Prüfung weitergereichter
Optionen im installierten Gate mit diesem Aufrufvertrag abgleichen. Lehnt
ein Gate diese Optionen ab, bleibt der Lauf blockiert. Der Workflow darf das
Gate weder umgehen noch einen Launcher direkt aus dem Checkout ausführen.
Die geschlossene Entrypoint-Allowlist des Gates bleibt unverändert.

Die aktuelle Workflow-Orchestrierung liegt im wiederverwendbaren
Framework-Workflow `connector-protected-nginx-exact-head.yml`. Der Parent
behält den kleinen Dispatch-Entrypoint
`run-protected-nginx-exact-head.yml` mit exaktem Framework-Commit-Pin.
Prüfungen für geschützten Branch, Akteur, Environment, Runner, Manifeste und
Artefakte bleiben im aufgerufenen Workflow erhalten. Historische
NGINX-Root-Broker-Aufrufer behalten ihre unveränderlichen Verträge für Parent
`8ae707d72f1a8acb25d239e55e28a73cbc7522b1` und Framework
`99a7985c1be92a2297b1b59208f64df6768f2cbf`. Diese historischen Aufrufe
qualifizieren die migrierte Quellrevision nicht.

Die Installation und das Verhalten des Host-Bootstraps können aus einem
normalen Checkout nicht nachgewiesen werden. Ein geschützter Exact-Head-Lauf
benötigt daher einen dedizierten, ephemeren Runner mit einem vom Host-Eigentümer
installierten und geprüften Gate. Ein generischer oder selbst gehosteter Runner
ohne diese Voraussetzung liefert keinen Laufzeitnachweis, sondern ist ein
blockiertes Hosted-Gate.
