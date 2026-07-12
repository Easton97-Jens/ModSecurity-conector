# lighttpd-Harness

**Sprache:** [English](README.md) | Deutsch

Status: native Konfigurationslade-, Start- und minimale Runtime-Smoke-Pfade

Der Connector verfügt über vier native Harness-Skripte:

- `prepare_native_smoke.sh` schreibt unten temporäre Common- und Lighttpd-Konfigurationen
  `BUILD_ROOT` mit deaktivierten beiden Körpermodi;
- `check_lighttpd_config.sh` lädt das reale Modul über reales `lighttpd -tt`;
- `start_lighttpd_smoke.sh` startet, prüft und stoppt lighttpd ohne Anfragen;
- `runtime_lighttpd_smoke.sh` sendet separat eine erlaubte und eine blockierte Anfrage.

Die entsprechenden Ziele sind:

```sh
make -C connectors/lighttpd check-lighttpd-config
make -C connectors/lighttpd start-smoke-lighttpd
make -C connectors/lighttpd runtime-smoke-lighttpd
```

Der Laufzeitrauch verwendet `OPTIONS *`, sodass der Lighttpd-Kern die zulässigen 200 zurückgeben kann
ohne nicht verwandte Bestandsmodule aus dem temporären Connector-Modul zu laden
Verzeichnis. Das Hinzufügen von `X-Modsec-Smoke: block` muss 403 aus der Regel `1000001` zurückgeben.
Das Skript überprüft auch die engen Common JSONL-Entscheidungsmetadaten.

`start-smoke-lighttpd` sendet bewusst null Anfragen und Berichte, die zählen.
Der Bridge-Selbsttest ist separat und wird niemals als Host-Beweis verwendet.

`run_lighttpd_smoke.sh` bleibt der Einstiegspunkt für das ältere Framework im Besitz
`sidecar_proxy`-Pfad. Es ist ein alternativer Weg und seine Beweise dürfen nicht sein
gemischt mit den Beweisen des nativen Moduls.

Der Dispatcher für den gesamten Lebenszyklus verwendet den generischen No-CRS-Bestandsläufer nicht wieder.
Es ruft `runtime-smoke-lighttpd-patched` auf
`full-lifecycle-lighttpd-patched`, das nur einen passenden Patch erstellt und lädt
lighttpd 1.4.84 Kern/Modul-Paar. Das isolierte Ziel sendet das gleiche schmale Signal
Phase-1-200/403-Anfragen mit deaktivierten beiden Körpermodi; es ist kein Anfragetext,
Response-Body-, Phase-4- oder Capability-Promotion-Evidenz.

Nachweis des Anforderungs-/Antwortkörpers, CRS, Produktionshärtung, Sicherheit
Eine Verifizierung und ein vollständiger Matrixbeweis werden von diesem Harness nicht bereitgestellt.
