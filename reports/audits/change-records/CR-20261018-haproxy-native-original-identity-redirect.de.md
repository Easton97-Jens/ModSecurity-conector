# Change Record: CR-20261018-haproxy-native-original-identity-redirect

**Sprache:** [English](CR-20261018-haproxy-native-original-identity-redirect.md) | Deutsch

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | CR-20261018-haproxy-native-original-identity-redirect |
| Datum (UTC) | 2026-10-18 |
| Basis-Revision | `fc7e0d25c6ed3240d6e257e92f25475e63f150c8` |

## Motivation und Problemstellung

Bei allen 80 vorbereiteten nativen Original-Fixtures wichen die Observer-Bezeichnungen von den Original-IDs ab. Die globale Teilstring-Ersetzung verfälschte außerdem die ausgewählte Receipt-ID von `NEED-request-eos-once`. Das benannte P3-Fixture deklarierte weiterhin 503, obwohl die Quellanforderung 302 und Location vorsieht.

## Akzeptanzkriterien

Vollständige Original-IDs genau einmal in Observer-CASE und ausgewähltem Receipt binden; alle 112 nativen Originalverträge und Oracles sowie die eingefrorene Inventur mit 278 Zeilen erhalten; P3-Erwartungen unabhängig ableiten; Sequenzvektoren und Socket-Verhalten erhalten; ältere Snapshots behalten. Neue Fixture-Wurzeln bleiben für das Root-Review unversiegelt.

## Implementierungsentscheidung und Begründung

Kontextgebundene Anker mit genau einem Vorkommen ersetzen die Teilstring-Umschreibung. Das ursprüngliche benannte `NEED-p3-redirect` verwendet nun `phase3_redirect_before_commit`, die kanonische Regel `1100202` und deren YAML-Deklaration: Status 302 und `https://no-crs.invalid/phase3-redirect`. Der Client verlangt genau einen passenden Location-Header für main und keinen für neighbor. Für diese P3-Umleitung wird kein P4-Body-Prädikat deklariert. Die öffentliche HAProxy-3.2.25-Funktion `http_apply_redirect_rule` und der aktuelle Produktquelltext sind im Review-Receipt separat gehasht. Die Sequenzvorbereitung akzeptiert nur die vertraglich gebundene ursprüngliche Allow-Basis mit bekanntem altem `NEED-allow` oder vollständigem Original-CASE; fehlende, wiederholte, gemischte oder unbekannte Anker führen zum Fehler.

## Geänderte Dateien

`connectors/haproxy/harness/i12_native_cases.py`, `connectors/haproxy/harness/i12_native_contracts.py`, `connectors/haproxy/harness/i12_native_sequences.py`, `tests/test_haproxy_i12_native_cases.py`, `tests/test_haproxy_i12_native_sequences.py`. Dieser EN/DE-Record begleitet die begrenzten Harness- und Teständerungen. Vorhandene Source-Descriptor- und Socket-Cleanup-Schutzmaßnahmen bleiben erhalten.

## Ausgeführte Befehle

Hier bezeichnet `R2` den externen Abnahmelauf. `rtk proxy R2/test-env/bin/python -m pytest -q tests/test_haproxy_i12_native_cases.py tests/test_haproxy_i12_native_sequences.py` bestand 41 Tests und 9 Untertests unter CPython 3.14.7; exakte argv, Exit und Rohdaten-Hashes stehen in `R2/commands/haproxy-native-v8-components-final-20261018.json`. Vorbereitungs-Receipts: `native-originals-prepare-v8-pinned-20261018`, `native-sequences-prepare-v5-final-20261018`. Vergleichs-Receipt: `native-v8-review-final-20261018`, Exit 0. Frühere Versuche mit relativem Pfad und falschem Capture scheiterten und bleiben erhalten; ein Befehl mit einer nicht vorhandenen separaten Vertragstestdatei endete mit Exit 4, anschließend bestand die tatsächliche Suite aus zwei Dateien.

## Security-Auswirkung

Dies korrigiert die Evidence-Identität und unabhängig deklarierte Client-Erwartungen. Produkt, gemeinsamer Capture, Originalinventur, Autorisierung, Isolation und physischer Observer werden nicht geändert. Erfolgreiche Komponententests ergeben keinen Lifecycle-PASS.

## Runtime-Evidence

In diesem Teilauftrag liefen keine Hosts. `R2/native/original-fixtures-v8` enthält 80 Original-Fixtures; `R2/native/sequence-fixtures-v5` enthält zwei Sequenz-Fixtures. Beide Wurzelverzeichnisse haben bis zur Root-Freigabe Modus 0700; die enthaltenen Dateien behalten die Producer-Versiegelung. `R2/native/identity-redirect-v8-review/review.json` und `native-v7-v8.diff` binden Vergleiche und unabhängige Quell-Hashes. Native Plan-SHA256: `fbd1f780f5122eca0beed5e5a19278208644aa3b8f883e49496d38b767c3ae36`; Sequenzindex: `8ebf64383be8a360d1fd9b5e32c51bf2e11cbbd5f32aa41639c9d964d3f741e0`; nativer Diff: `29a12a7b4a6df6b56159ca53ac6a93119d355d0e3213109c77ce933163c6bb68`.

## Bekannte Einschränkungen

Deklarierte P3-Erwartungen stammen aus Regel/YAML und öffentlicher Host-API, nicht aus einem gemessenen Status. Tatsächlicher Commit, Clienttransport, EOS, Logging, Finish und Free erfordern weiterhin neue unabhängig beobachtete Hostläufe. Historische Bezeichnungen und Evidence bleiben ohne Umschreibung erhalten.

## Verbleibende Risiken

Root muss den neuen Fixture-Diff und die Quellbindungen vor Versiegelung und Ausführung abgleichen. Ein tatsächlicher Hostfehler muss als Fehler erhalten bleiben. Gemeinsam verwendete Requests dürfen niemals als unabhängige native, SPOP- und Companion-Läufe zählen.

## Nicht ausgeführte Prüfungen mit Begründung

Dieser Worker führte keine Builds, Hostläufe, Git-Auslieferung, CI oder Sonar aus; diese Aktionen liegen bei Root. Dieser Teilauftrag erstellt ausschließlich quellgebundene Fixtures und Komponentenvalidierung.

## Finaler Diff- und Review-Status

Der Worker prüfte die fünf begrenzten Quell-/Test-Diffs und beide vollständigen Sprachfassungen. Quell- und Fixture-Hashes werden an Root übergeben. Root-Review, Versiegelung, Commits und erneute Hostläufe stehen noch aus; Merge oder Force-Push sind nicht autorisiert.
