# Change Record: Traefik-Remediation für begrenzte Resultattext-Serialisierung für SonarQube Cloud

**Sprache:** [English](CR-20260728-sonar-traefik-result-nullability.md) | Deutsch

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | CR-20260728-sonar-traefik-result-nullability |
| Datum (UTC) | 2026-07-28 |
| Basis-Revision | 8e8acb8dab1cd03723de269cab7da7dd62e5e010 |
| Grenze | Ausschließlich Parent-Traefik-Resultatserialisierung, ihr direkter C17-Source-Contract-Test, dieses englisch/deutsche Paar und seine Indizes. Framework, MRTS, Gitlinks, Workflows, Sonar-Policy und generierte Reports bleiben unverändert. |
| Finding-Verknüpfung | Zielt auf `c:S2637`-Keys `AZ9cRyv8HhV2CayPTP10`, `AZ9cRyv8HhV2CayPTP11` und `AZ9cRyv8HhV2CayPTP12` sowie auf die `c:S3519`-Keys des ersten Kandidaten `AZ-oL-mYW3nRPo6lC6ub`, `AZ-oL-mYW3nRPo6lC6uc` und `AZ-oL-mYW3nRPo6lC6ud`, die `FND-SONAR-0019` verfolgt. Vor Exact-Head-Hosted-Evidence wird kein externes Issue als geschlossen behauptet. |

## Motivation und Problemstellung

`traefik_engine_send_result` schreibt optionalen Transaktions-, Regel- und
Redirect-Text in einen privaten Local-Engine-Unix-Socket-Resultatframe. Die
Nullable-Copy-Form erzeugte drei `c:S2637`-Meldungen. Der erste Kandidat nutzte
einen gemeinsamen einbytegroßen leeren C-String-Fallback, entfernte damit diese
Meldungen, erzeugte aber drei BLOCKER-`c:S3519`-Meldungen, weil Sonar eine
positive Kopie aus dem Fallback modellieren konnte.

Der bestehende Bounded-Size-Helper liefert für den Fallback null zurück; der
gemeldete Out-of-Bounds-Pfad ist daher nicht als dynamisch erreichbar bewiesen.
Er bleibt ein Quality-Gate-Blocker. Die Korrektur muss Null-Längen-Felder,
Feldreihenfolge, Bytes, Maxima, Action, Phase, Status und Flags ohne
Suppression, Protokolländerung oder schwächere Grenze erhalten.

## Akzeptanzkriterien

- Nullable Optionalpointer behalten für fehlende Werte Größe null.
- Ein privater begrenzter Copy-Helper akzeptiert Größe null ohne Quelle und
  weist eine positive Länge mit Nullquelle vor Lesen oder Schreiben ab.
- Der direkte C17-Socketpair-Harness prüft fehlende, gefüllte und maximal
  lange Felder bytegenau sowie den Nullquellen-Negativcontrol.
- Fokussierte C17-, Diagnostics-, Traefik-Security-Contract-, Dokumentations-
  und Security-Diff-Validierung besteht ohne Sonar-Policy-Änderung.
- Vor Beobachtung werden weder Hosted-Ergebnis, Review, Merge, Master-Update,
  Framework-/MRTS-Änderung noch Full-Host-Runtime behauptet.

## Implementierungsentscheidung und Begründung

Der Serializer behält nullable Source-Pointer und lässt
`traefik_engine_bounded_string_size` ein fehlendes Feld als null ausdrücken.
Der neue private `traefik_engine_copy_bounded_text` ist bei Größe null
erfolgreich; andernfalls weist er eine Null-Destination oder -Quelle vor seiner
begrenzten Byte-Schleife ab. `traefik_engine_send_result` gibt seinen Payload
frei und liefert Fehler, wenn diese Invariante verletzt ist. Decision-/
Session-Control-Flow, Frame-Layout, Maxima, Clamping und Decision-Metadaten
bleiben unverändert.

## Geänderte Dateien

- `connectors/traefik/src/traefik_engine_service.c`
- `tests/test_sonar_reliability_contract.py`
- `reports/audits/change-records/README.md` und `README.de.md`
- dieses englisch/deutsche Change-Record-Paar

## Ausgeführte Befehle

| Befehl oder Kontrolle | Ergebnis |
| --- | --- |
| `PYTHONDONTWRITEBYTECODE=1 PYTHONNOUSERSITE=1 <workspace-venv>/python -B tests/test_sonar_reliability_contract.py` | bestanden: 11 Tests einschließlich C17-Harness-Controls für fehlende, gefüllte, maximale und positive-Länge-mit-Nullquelle. |
| `<workspace-venv>/python -B -m unittest -v tests.test_c_cpp_diagnostics` | bestanden: 7 C/C++-Diagnostics-Contract-Tests. |
| `TMPDIR=<task-eigene externe Wurzel> make check-remaining-connectors-c17` | bestanden: jede Remaining-Connector-C-Translation-Unit einschließlich Traefik kompiliert unter C17 mit `-Wall -Wextra -Werror`. |
| `<workspace-venv>/python -B -m unittest -v tests.test_bilingual_docs tests.test_traefik_native_local_plugin tests.test_traefik_runtime_smoke_security` | bestanden: 39 fokussierte Dokumentations- und Traefik-Runtime-/Security-Contract-Tests. |
| `git diff --check` und vollständiges Bilingual-Dokumentations-Overlay | bestanden: kein Whitespace-Fehler; alle Sprachpaare, Change-Record-Struktur, Repository-Pfadreferenzen und Dokumentationslinks bestanden in einem task-eigenen Overlay mit der Parent-gebundenen Framework-Revision `47e50e7bc43ba7a3b5bad1a9448111794f664cc0`. |
| Fokussierter `codex-security:security-diff-scan` des lokalen Nachfolger-Patches | bestanden: Die versiegelte Exact-Local-Patch-Review mit Snapshot `2d37a63df4555e967210366aad018478e3385564a02cb57c6dce62588d59651c` prüfte beide geänderten Dateien vollständig und erzeugte keinen berichtspflichtigen Security-Befund. |

## Security-Auswirkung

Dies ist eine private Unix-Socket-Serialisierungsgrenze. Der Datensatz
behauptet keinen nachgewiesenen Runtime-Out-of-Bounds-Read: Dem vorherigen
`c:S3519`-Pfad fehlt die interprozedurale Size-Beziehung. Der überarbeitete
Helper scheitert dennoch fehlgeschlossen bei einer positiven Länge mit
Nullquelle, ohne die Serialisierung zu erweitern. Die versiegelte lokale
Security-Review fand weder im geänderten Serializer noch in seinem direkten
unterstützenden Test einen berichtspflichtigen Vulnerability-Befund.

## Runtime-Evidence

Die reale C-Translation-Unit wird über ein Unix-Socketpair kompiliert und
ausgeführt. Der direkte Harness beweist fehlende, gefüllte, maximal lange und
Nullquellen-Verhalten, einschließlich der Ablehnung vor einer
Destination-Mutation bei positiver Länge mit Nullquelle. Dies ist fokussierte
Source-Level-Protokoll-Evidence, kein vollständiger Traefik/Common/
libmodsecurity-Host-Runtime-Test.

## Bekannte Einschränkungen

Verifizierte libmodsecurity-Development-Header/-Libraries fehlen, daher wird
die vollständige Host-/Plugin-Runtime nicht behauptet. Die fokussierte Review
beschränkt sich auf die beiden geänderten Dateien und ersetzt keine Exact-Head-
Hosted-Sonar-Analyse.

## Verbleibende Risiken

Ein bereitgestellter Traefik-Host, geladenes Plugin und eine Live-Common/
libmodsecurity-Transaktion können Verhalten hinzufügen, das der lokale Harness
nicht ausführt. Die externen `c:S2637`- und `c:S3519`-Dispositionen bleiben
offen, bis eine frische Hosted-Analyse den Nachfolger-PR-Head beobachtet.

## Nicht ausgeführte Prüfungen mit Begründung

- Die vollständige Traefik-Host-/Plugin-Runtime lief nicht, weil in der
  zugelassenen lokalen Umgebung kein verifiziertes libmodsecurity-
  Development-Header/-Library-Paar verfügbar ist.
- Exact-Head-GitHub-, SonarQube-Cloud-, Review- und Merge-Checks sind für
  diesen Nachfolger aktuell nicht beobachtet; sie müssen nach seinem normalen
  Update von Draft-PR #150 erneut gelesen werden.

## Finaler Diff- und Review-Status

Draft-Parent-PR #150 bleibt gegen `master` offen; sein erster veröffentlichter
Head scheiterte an den neuen `c:S3519`-Blockern. Der lokale Nachfolger besteht
seine versiegelte Security-Diff-Review und fokussierten lokalen Prüfungen,
behauptet aber kein Hosted-Ergebnis. Nach seinem normalen Update bleiben
Exact-Head-Checks, SonarQube-Cloud-Readback und Review verpflichtend.
