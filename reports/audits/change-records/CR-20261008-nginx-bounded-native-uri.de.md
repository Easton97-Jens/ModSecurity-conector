# Change Record: CR-20261008-nginx-bounded-native-uri

**Sprache:** [English](CR-20261008-nginx-bounded-native-uri.md) | Deutsch


## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | CR-20261008-nginx-bounded-native-uri |
| Datum (UTC) | 2026-10-08 |
| Basis-Revision | `68bf814e0d850f68f20bd26da59ed7a351e3633d` |

## Motivation und Problemstellung

Lange oder stark escapte Request-URIs können den strikten Common-JSON-Writer erschöpfen. NGINX benötigt eine begrenzte URI-Projektion, ohne Fehler anderer Metadaten zu verbergen.

## Akzeptanzkriterien

Nur die URI begrenzen; bestehende Truncation-/Redaction-Flags und den Query-Marker auch bei einer Query hinter dem sicheren Präfix erhalten. Zu große andere Metadaten und Schreibfehler bleiben strikte Fehler.

## Implementierungsentscheidung und Begründung

`ngx_http_modsecurity_bounded_event_uri` projiziert die URI in einen begrenzten Stack-Puffer. Der 256-Byte-Speicher erlaubt höchstens 255 escapte JSON-Bytes; `?<redacted>` bleibt bei Queries auch mit langen escapten Präfixen erhalten. `ngx_http_modsecurity_write_event_jsonl` und `ngx_http_modsecurity_write_phase_event_jsonl` verwenden diese Projektion mit dem echten Common-Serializer. Alle anderen Felder bleiben unverändert.

## Geänderte Dateien

`connectors/nginx/src/ngx_http_modsecurity_event_uri.h`, `connectors/nginx/src/ngx_http_modsecurity_common.h`, `connectors/nginx/SOURCE_MAP.json` und `tests/test_nginx_bounded_event_uri.py`; bestehende Producer-Kontrollen stehen in `tests/test_nginx_request_error_events.py`. Der Materializer enthält den neuen Header explizit. Dokumentation: nur dieses `.md`-/`.de.md`-Paar; Framework, MRTS und Gitlinks werden durch diese Dokumentationsreparatur nicht geändert.

## Ausgeführte Befehle

Verifikation des Source-Owners: `/root/.local/bin/rtk proxy env RUNNER_TEMP=/var/tmp/codex/ModSecurity-conector/runs/nginx-all-required-20261008T124555Z PYTHONPYCACHEPREFIX=/var/tmp/codex/ModSecurity-conector/runs/nginx-all-required-20261008T124555Z/pycache /root/git/ModSecurity-conector/.venv/bin/python -m unittest tests.test_nginx_bounded_event_uri tests.test_nginx_request_error_events tests.test_nginx_native_intervention_chain -v` bestand mit insgesamt 32 Kontrollen (fünf URI-, 15 Request-Error- und zwölf Intervention-Kontrollen), die tatsächlichen Producer-Code und Common-JSON-Serialisierung mit `-std=c17 -Wall -Wextra -Werror` kompilieren. Diese Dokumentationsreparatur führt die Source-Tests nicht erneut aus. Parent-Vorlagenerzeugung und `rtk proxy python3 ci/tools/new-change-record.py check` prüfen nur die Dokumentstruktur.

Prüfungen der Dokumentationsreparatur (keine native Ausführung): `rtk proxy env PYTHONDONTWRITEBYTECODE=1 PYTHONNOUSERSITE=1 /root/git/ModSecurity-conector/.venv/bin/python ci/tools/new-change-record.py check` endete mit 0; `rtk proxy env PYTHONDONTWRITEBYTECODE=1 PYTHONNOUSERSITE=1 /root/git/ModSecurity-conector/.venv/bin/python -m unittest -v tests.test_change_record` bestand mit 20 Tests, Exit 0. `rtk proxy make check-bilingual-docs PYTHON=/root/git/ModSecurity-conector/.venv/bin/python` endete mit 2 wegen 22 bestehenden fehlenden Framework-Submodule-Links; `rtk proxy make check-doc-links FRAMEWORK_ROOT=/var/tmp/codex/ModSecurity-conector/worktrees/framework-nginx-seven-contracts-20261008 PYTHON=/root/git/ModSecurity-conector/.venv/bin/python` endete mit 2 wegen bestehender fehlender Submodule-Pfadreferenzen. Keine betrifft dieses Paar. `rtk git diff --check` endete mit 0. Das frische kombinierte Source-Owner-Log `root-uri-limit-final-focus.log` meldet 32 bestandene Kontrollen (fünf URI, 15 Request-Error, zwölf Intervention), keinen Native-Runtime-Nachweis.

## Security-Auswirkung

Query-Redaction und explizite Truncation bleiben sichtbar. Zu große andere Metadaten bleiben Fehler; Serializer- und Sink-Fehler werden nicht zu erfolgreichen Events. Keine Payload, synthetische Regel oder gelockerte Validierung wird eingeführt.

## Runtime-Evidence

Es wird keine Live-Native-Runtime-Evidence behauptet. Kompilierte Kontrollen sind Source-/Serializer-Unit-Nachweise, keine kanonische Required-Case-Abdeckung oder Exact-Head-Nachweise.

## Bekannte Einschränkungen

Die begrenzte Projektion ist NGINX-spezifisch und gilt nur für URI-Metadaten. Sie ist keine allgemeine Common-Metadaten-Truncation-Policy.

## Verbleibende Risiken

Ein frischer Source-gebundener Modul-/Binary-Build und tatsächliche Required-Case-Ausführung müssen integriertes natives Verhalten und Artefaktidentität noch nachweisen.

## Nicht ausgeführte Prüfungen mit Begründung

Frischer vollständiger Modul-/Binary-Build, integrierte native Requests, vollständige Required-Canonical-Validierung und Remote-CI/Sonar wurden in dieser reinen Dokumentationsaufgabe nicht ausgeführt; sie benötigen separate Source-Owner-/Runtime-Koordination.

## Finaler Diff- und Review-Status

Die Vier-Dateien-Dokumentationsreparatur verwendet Parent-Generator/-Schema, vollständige Basisrevision und äquivalente EN/DE-Fakten. Source-Dateien und fremde Arbeit bleiben erhalten. Ein erfolgreicher Archive-Check belegt nur Struktur, keine native Ausführung.
