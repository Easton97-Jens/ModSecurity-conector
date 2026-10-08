# Change Record: CR-20261008-nginx-native-response-limit-classification

**Sprache:** [English](CR-20261008-nginx-native-response-limit-classification.md) | Deutsch


## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | CR-20261008-nginx-native-response-limit-classification |
| Datum (UTC) | 2026-10-08 |
| Basis-Revision | `8b575c094140f3a92bb030a83f27b4c44b00127e` |

## Motivation und Problemstellung

Ein natives Response-Body-Reject besitzt keine Regelkorrelation. Es darf weder den regelbasierten SAFE-Log-only-Pfad benutzen noch Engine-EOS behaupten.

## Akzeptanzkriterien

Nur die exakte native Response-Limit-Signatur akzeptieren; BODY_LIMIT ohne Regel versiegeln, Downstream-Weitergabe verhindern und unerwartete Append-Regelentscheidungen vor echter Engine-Completion ablehnen.

## Implementierungsentscheidung und Begründung

Das vorhandene geschlossene Prädikat `ngx_http_modsecurity_is_response_body_limit_rejection` vor dem regelbasierten Dispatch in `ngx_http_modsecurity_process_intervention` verwenden. Der tatsächliche Kontext unterscheidet natives Request-/Response-Body-Limit-Reject. Beliebige regelose 403-Antworten sind kein Body-Limit-Nachweis und dürfen keine SAFE-Regelsemantik übernehmen.

## Geänderte Dateien

`connectors/nginx/SOURCE_MAP.json`, `connectors/nginx/src/ngx_http_modsecurity_common.h`, `connectors/nginx/src/ngx_http_modsecurity_module.c` und `tests/test_nginx_native_intervention_chain.py`. Die Materialisierung enthält die vorhandenen Response-Limit-/P4-Beobachtungsheader. Dokumentation: nur dieses `.md`-/`.de.md`-Paar; Framework, MRTS, generische Validatoren und Gitlinks werden durch diese Dokumentationsreparatur nicht geändert.

## Ausgeführte Befehle

Verifikation des Source-Owners: `/root/.local/bin/rtk proxy env RUNNER_TEMP=/var/tmp/codex/ModSecurity-conector/runs/nginx-all-required-20261008T124555Z PYTHONPYCACHEPREFIX=/var/tmp/codex/ModSecurity-conector/runs/nginx-all-required-20261008T124555Z/pycache /root/git/ModSecurity-conector/.venv/bin/python -m unittest tests.test_nginx_bounded_event_uri tests.test_nginx_request_error_events tests.test_nginx_native_intervention_chain -v` bestand frisch mit insgesamt 32 Kontrollen, darunter zwölf tatsächliche Source-Collector-Kontrollen und `-std=c17 -Wall -Wextra -Werror`. Gültige SAFE-/STRICT-/off-Kontrollen und Negative für falsche Signatur, frühe Regel, ungültige Returns und fehlende Korrelation bleiben abgedeckt. Diese Dokumentationsreparatur führt die Source-Tests nicht erneut aus. Parent-Vorlagenerzeugung und `rtk proxy python3 ci/tools/new-change-record.py check` prüfen nur die Dokumentstruktur.

Prüfungen der Dokumentationsreparatur (keine native Ausführung): `rtk proxy env PYTHONDONTWRITEBYTECODE=1 PYTHONNOUSERSITE=1 /root/git/ModSecurity-conector/.venv/bin/python ci/tools/new-change-record.py check` endete mit 0; `rtk proxy env PYTHONDONTWRITEBYTECODE=1 PYTHONNOUSERSITE=1 /root/git/ModSecurity-conector/.venv/bin/python -m unittest -v tests.test_change_record` bestand mit 20 Tests, Exit 0. `rtk proxy make check-bilingual-docs PYTHON=/root/git/ModSecurity-conector/.venv/bin/python` endete mit 2 wegen 22 bestehenden fehlenden Framework-Submodule-Links; `rtk proxy make check-doc-links FRAMEWORK_ROOT=/var/tmp/codex/ModSecurity-conector/worktrees/framework-nginx-seven-contracts-20261008 PYTHON=/root/git/ModSecurity-conector/.venv/bin/python` endete mit 2 wegen bestehender fehlender Submodule-Pfadreferenzen. Keine betrifft dieses Paar. `rtk git diff --check` endete mit 0. Das frische kombinierte Source-Owner-Log `root-uri-limit-final-focus.log` meldet 32 bestandene Kontrollen (fünf URI, 15 Request-Error, zwölf Intervention), keinen Native-Runtime-Nachweis.

## Security-Auswirkung

Keine synthetische Regel oder EOS wird eingeführt; technisches Reject verhindert Downstream-Body-Weitergabe. Framework-Containment/Freshness, Required-Auswahl und strikte Event-Validatoren bleiben unverändert.

## Runtime-Evidence

Dies ist ein Source-Zustands-/Collector-Unit-Nachweis, kein frisches Modul-Artefakt oder tatsächliches natives Request-Ergebnis. Kein kanonisches PASS oder Exact-Head-Runtime-Nachweis wird behauptet.

## Bekannte Einschränkungen

Die Klassifizierung hängt von der geschlossenen Engine-spezifischen Signatur und echter Response-Body-Completion ab. Parallele Budget-/Cleanup-Änderungen gehören nicht zum Source-Umfang dieses Nachweises.

## Verbleibende Risiken

Integrierte native Validierung mit tatsächlich neu gebauten Artefakten muss Engine-Signatur, technisches Reject und Completion-Verhalten bestätigen.

## Nicht ausgeführte Prüfungen mit Begründung

Frischer vollständiger Modul-/Binary-Build, integrierte native Requests, vollständige Required-Canonical-Validierung und Remote-CI/Sonar wurden in dieser reinen Dokumentationsaufgabe nicht ausgeführt; Source-Owner-/Runtime-Koordination bleibt erforderlich.

## Finaler Diff- und Review-Status

Die gezielte Dokumentationsreparatur folgt Parent-Generator/-Schema und verwendet die vollständige Basisrevision. Äquivalente EN/DE-Fakten erhalten die ursprüngliche Source-/Unit-Evidence-Grenze. Fremde Orchestrierungs- und Source-Änderungen bleiben erhalten; ein erfolgreicher Archive-Check belegt nur Struktur.
