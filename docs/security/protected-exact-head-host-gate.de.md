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

Die Installation und das Verhalten des Host-Bootstraps können aus einem
normalen Checkout nicht nachgewiesen werden. Ein geschützter Exact-Head-Lauf
benötigt daher einen dedizierten, ephemeren Runner mit einem vom Host-Eigentümer
installierten und geprüften Gate. Ein generischer oder selbst gehosteter Runner
ohne diese Voraussetzung liefert keinen Laufzeitnachweis, sondern ist ein
blockiertes Hosted-Gate.
