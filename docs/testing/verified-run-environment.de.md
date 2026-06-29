# Verifizierte Ausführungsumgebung

**Sprache:** [English](verified-run-environment.md) | Deutsch

Verifizierte Ausführungen verwenden ein Worker-kompatibles Runtimestammverzeichnis außerhalb des Quell-Checkouts
und außerhalb `/root`.

`/root` ist kein sicherer Standardwert für NGINX-Harness-Runtimedaten. Unter gewöhnlichem Linux
Runners `/root` ist der Modus `0700`, während NGINX-Arbeitsprozesse als ausgeführt werden können
`nobody`. Auch wenn die generierten Dateien unterhalb des Harnesss lesbar sind, kann der Arbeiter
`/root` kann nicht durchlaufen werden, daher kann `htdocs/index.html` nicht angegeben oder gelesen werden. In
Dieser Zustand `try_files $uri $uri/ /index.html` kann eine Dateisystemberechtigung umwandeln
Problem in einen internen HTTP 500-Umleitungszyklus. Das Gurtzeug ist jetzt vorfliegend
Arbeiterzugriff und Berichte:

```text
BLOCKED: nginx worker cannot access harness docroot
```

Bei diesem Status handelt es sich um einen UmgebungsEvidence und nicht um eine Nichtübereinstimmung der Connector-Runtime.

## Runtimepfade

Der Standardstamm ist:

```sh
VERIFIED_RUN_ROOT=${RUNNER_TEMP:-${TMPDIR:-/var/tmp}}/ModSecurity-conector-verified
```

Abgeleitete Standardwerte:

```text
VERIFIED_STATE_ROOT=$VERIFIED_RUN_ROOT/state
VERIFIED_BUILD_ROOT=$VERIFIED_RUN_ROOT/build
VERIFIED_SOURCE_ROOT=$VERIFIED_RUN_ROOT/src
VERIFIED_TMP_ROOT=$VERIFIED_RUN_ROOT/tmp
VERIFIED_LOG_ROOT=$VERIFIED_RUN_ROOT/logs
VERIFIED_COMPONENT_CACHE=$VERIFIED_RUN_ROOT/component-cache
NGINX_HARNESS_PARENT=$VERIFIED_RUN_ROOT/nginx-harness
```

Die Kompatibilitätsvariablen `BUILD_ROOT`, `SOURCE_ROOT`, `TMP_ROOT`,
`LOG_ROOT` und `CONNECTOR_COMPONENT_CACHE` verwenden standardmäßig diese überprüften Pfade.
Runtimepfade dürfen sich nicht in `/root`, im Quell-Checkout oder an Systemstandorten befinden
wie `/usr`, `/etc`, `/var/lib`, `/bin` oder `/sbin`. `/var/tmp/...` und
`${RUNNER_TEMP}/...` sind gültige Runtime-Eltern.

## Lokal verifizierter Lauf

```sh
export VERIFIED_RUN_ROOT=/var/tmp/ModSecurity-conector-verified
export VERIFIED_RUN_FULL_MATRIX_JOB_TIMEOUT_SECONDS=3600
make verified-runtime-producers
make verified-report-refresh
make verified-report-checks
```

Für einen günstigeren lokalen Scheck:

```sh
export VERIFIED_RUN_ROOT=/var/tmp/ModSecurity-conector-verified
make verified-report-run-smoke
```

## CI-verifizierter Lauf

CI-Jobs sollten Läufer-eigenen temporären Speicher verwenden:

```yaml
env:
  VERIFIED_RUN_ROOT: ${{ runner.temp }}/ModSecurity-conector-verified
  XDG_STATE_HOME: ${{ runner.temp }}/state
```

Das Repository führt einfache syntax/layout/report-Governance-Prüfungen in CI durch.
Vollständig verifizierte Runtime- oder Vollmatrix-Jobs sollten manuell oder explizit bleiben
nachgefragt, weil sie teuer sind.

## Artefakte

Übertragen Sie generierte Berichte unter `reports/testing/generated/` nur dann, wenn sie vorhanden sind
aktualisiert anhand der aktuell verifizierten Eingaben. Übernehmen Sie Dokumentations- und Quelländerungen
die den Arbeitsablauf definieren.

Übernehmen Sie keine Runtime-Roots, Komponenten-Caches, Build-Bäume, temporäre Verzeichnisse usw.
Protokolle, `verified-runs/`-Befehlsprotokolle oder Quell-Downloads von
`VERIFIED_RUN_ROOT`.

## Statussemantik

`PASS` bedeutet, dass die überprüfte Eingabe oder der Befehl wie erforderlich abgeschlossen wurde.

`WARN` bedeutet, dass die optionale Evidence- oder Fallback-Validierung unvollständig ist, aber der Lauf
kann weitermachen.

`FAIL` bedeutet, dass eine erforderliche Prüfung ausgeführt wurde und zu einem fehlgeschlagenen Ergebnis geführt hat.

`UNKNOWN` bedeutet, dass keine verifizierte Eingabe zur Untermauerung einer stärkeren Behauptung verfügbar war.

`BLOCKED` bedeutet, dass der Lauf keine gültigen RuntimeEvidence liefern konnte, weil a
Die Vorbedingung ist fehlgeschlagen, z. B. ein unzugänglicher NGINX-Docroot. BLOCKIERTE Daten müssen
nicht als Evidence für PASS oder Runtimeinkongruenz umgeschrieben werden.

## Hilfskonsolidierung

| Doppelte Logik | Alte Standorte | Neuer Helfer | Verhalten geändert? |
| --- | --- | --- | --- |
| Überprüfte Runtimepfad-Standardeinstellungen und Systempfadprüfungen | `Makefile`, `ci/run-verified-report-run.py`, `ci/run-full-matrix-job.py`, `ci/run-full-matrix-resume.py`, `ci/check-runtime-producer-readiness.py` | `ci/runtime_path_utils.py` und `modules/ModSecurity-test-Framework/ci/common.sh` | Standardmäßig wird jetzt `VERIFIED_RUN_ROOT` verwendet; Die Validierung blockiert weiterhin unsichere Pfade. |
| SHA256-Datei-Hashing | Verifiziertes Manifest, Vollständigkeit der Matrix, Generatoren für Runtimeinkongruenzen | `ci/generated_report_utils.py` | NEIN. |
| UTC-generierte Zeitstempel | Verifizierte Manifest- und full-matrix/mismatch-Generatoren | `ci/generated_report_utils.py` | NEIN. |
| NGINX-Worker-Docroot-Zugriffsprüfungen | Berechtigungsdiagnose im NGINX-Harness und spätere HTTP-500-Analyse | `connectors/nginx/harness/run_nginx_smoke.sh` Preflight-Datensätze | Ja: Unzugängliches Docroot gibt jetzt BLOCKED zurück, bevor die NGINX-Anfrage bearbeitet wird. |
