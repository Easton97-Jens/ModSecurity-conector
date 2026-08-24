# Kanonischer Runtime-Observation-Vertrag

**Sprache:** [English](README.md) | Deutsch

Dieses Verzeichnis definiert den einen Parent-eigenen, connector-neutralen
Vertrag für einen Runtime-Claim. Es führt keinen Host aus, leitet keinen
Runtime-PASS aus einem Prozess-Exitcode ab und ersetzt nicht die strukturierte
Evidence-Erfassung eines Connectors.

```text
connector-specific structured evidence
  -> strict connector adapter
  -> canonical runtime observation
  -> common validator
  -> canonical validation result
```

Das versionierte [Transport-Schema](runtime-observation.schema.json) hat die
sieben Top-Level-Felder: sechs Objekte (`identity`, `runtime`, `framework`,
`isolation`, `cleanup` und `provenance`) sowie `schema_version`. Die semantischen Regeln und
die sichere Dateiverarbeitung liegen in
[runtime_observation.py](runtime_observation.py); JSON Schema allein gilt
nicht als Nachweis eines Runtime-Claims.

## Identität und Profilmatrix

Jede Observation bindet Connector, Integrationsmodus, Profil, CRS- und
MRTS-Achse, Run-ID, Parent-/Framework-/MRTS-Commit, Producer und
Producer-Version. Die folgende zentral definierte Matrix gilt für jeden
Connector; es gibt keine connector-spezifischen Validatorausnahmen.

| Profil | Framework-Anforderung | MRTS-Attestation | Erforderliches Ergebnis |
| --- | --- | --- | --- |
| `no-crs-no-mrts` | ausgewählter, ausgeführter Live-No-CRS-Fall | alle fünf No-MRTS-Fakten sind `false` | Live-Evidence und sauberes Cleanup |
| `no-crs-with-mrts` | ausgewählter, ausgeführter Live-No-CRS-Fall | alle fünf MRTS-Fakten sind `true` | Live-Evidence und sauberes Cleanup |
| `with-crs-no-mrts` | ausgewählter, ausgeführter Live-CRS-Fall | alle fünf No-MRTS-Fakten sind `false` | Live-Evidence und sauberes Cleanup |
| `with-crs-with-mrts` | ausgewählter, ausgeführter Live-CRS-Fall | alle fünf MRTS-Fakten sind `true` | Live-Evidence und sauberes Cleanup |

Für jedes Profil muss `identity.mrts_commit` der übergebene vollständige
Commit in Kleinbuchstaben sein. Für ein No-MRTS-Profil ist er ausschließlich
eine Identitätsbindung: Der Producer darf keinen MRTS-Runner aufrufen, dessen
Inventar laden, Prozess starten, Listener erzeugen, MRTS-Artefakt verwenden
oder einen MRTS-Checkout lesen.

Die erforderlichen Runtime-Assertions sind `config_test`, `host_start`,
`reachability`, `allow_case` und `block_case`. `bypass_case` ist die einzige
zentral optionale Assertion. Ein Connector darf kein anderes Feld als
`NOT_APPLICABLE` markieren; eine optionale Assertion muss ausdrücklich nicht
erforderlich, nicht anwendbar und nicht ausgeführt sein.

Der Framework-Abschnitt unterstützt typisierte Erwartungen, darunter
`http_status`, `intervention`, `action`, `rule_match`, `rule_id`, `event`,
Header-/Body-, Transport-, Lifecycle-, Cleanup-, Compound- und
`not_applicable`-Arten. Body- und Header-Fälle verwenden begrenzte semantische
Prädikate oder Digests, niemals rohe Payloads oder Headerwerte.

## PASS-Entscheidung

Der Validator liefert `PASS` nur, wenn alle folgenden Bedingungen erfüllt
sind:

- Identität und Profilmatrix mit der übergebenen Identität übereinstimmen;
- jede Pflicht-Runtime-Assertion vorhanden, live ausgeführt und passend ist;
- der Framework-Fall ausgewählt, ausgeführt, live ausgeführt und passend ist,
  `CONTRACT_VALIDATED` hat und null Failure- und Mismatch-Zähler aufweist;
- die MRTS-Fakten des Profils übereinstimmen und jeder Cleanup-Zähler null ist;
- Producer, Evidence-Klasse, Evidence-Inventar und Evidence-Digests zusammen
  gebunden sind; und
- Observation und referenzierte Evidence die sicheren Eingabeprüfungen
  bestehen.

Fehlende Pflicht-Evidence führt in `strict` zu `VALIDATION_FAILED` und darf
nur in der expliziten Policy `partial` als `PARTIAL` erscheinen. Keiner der
beiden Status ist ein PASS.

## Connector-Adapter-Grenze

| Connector | Vertragsstatus in dieser Änderung |
| --- | --- |
| Envoy | strikter strukturierter Adapter; normalisierte Observations verwenden den gemeinsamen Validator |
| Lighttpd | strikter strukturierter Adapter; normalisierte Observations verwenden den gemeinsamen Validator |
| Traefik | strikter strukturierter Adapter; normalisierte Observations verwenden den gemeinsamen Validator |
| Apache | nur Schnittstelle und kanonisches Unit-Fixture; Live-Claims bleiben bis zu einem separaten Producer fail-closed |
| HAProxy | nur Schnittstelle und kanonisches Unit-Fixture; Live-Claims bleiben bis zu einem separaten Producer fail-closed |
| NGINX | als `protected-separate` abbildbar; der generische Validator schlägt ohne verifizierte Broker-Bridge geschlossen fehl, und seine geschützte Root-/Broker-Produktionsgrenze bleibt unverändert |

Kanonische Fixtures sind Testeingaben, keine synthetische Live-Evidence und
kein Runtime-Capability-Nachweis. Die Policy `fixture` steht nur der
In-Process-API für diese Fixtures zur Verfügung; die CLI stellt nur `strict`
und `partial` bereit.

## Sichere Ein- und Ausgabe

`load_runtime_observation_file()` öffnet Evidence-Roots und Pfadkomponenten
komponentenweise per Deskriptor mit No-Follow-Flags. Es akzeptiert nur reguläre
Dateien mit exaktem Modus 0600 sowie Evidence-Roots und Unterverzeichnisse
mit exaktem Modus 0700 im Besitz der aktuellen UID, weist symbolische und
harte Links ab, prüft die Dateiidentität vor und nach dem Lesen, begrenzt die
Eingabe auf 1 MiB, verlangt striktes UTF-8-JSON und weist doppelte Schlüssel
sowie nicht-endliche Werte ab. Relative Evidence-Pfade sind begrenzt und
dürfen keinen absoluten Pfad, Traversal, Raw-Log-Inhalt, Payload oder
geheimnisähnliche Metadaten enthalten.

`write_canonical_evidence_file()` erzeugt über dieselbe
deskriptorgebundene Grenze ein frisches Owner-only-Leaf und verweigert das
Überschreiben eines bestehenden kanonischen Ergebnisses. Es erzeugt keine
privilegierten Listener, ändert keine Ownership und benötigt keinen
Root-Runner.

## API und CLI

Die öffentliche Python-API ist:

```python
validate_runtime_observation(observation, expected_identity, policy)
```

Sie liefert ein begrenztes `ValidationResult`; Aufrufer dürfen ausschließlich
`result.status == "PASS"` als Erfolg behandeln. Die Kommandozeilengrenze ist:

```sh
python3 ci/runtime/contracts/validate-runtime-observation.py \
  --observation "<private-evidence-root>/runtime-observation.json" \
  --evidence-root "<private-evidence-root>" \
  --connector envoy --profile with-crs-no-mrts --run-id RUN_ID \
  --parent-sha PARENT_SHA --framework-sha FRAMEWORK_SHA \
  --mrts-sha MRTS_SHA \
  --policy strict
```

Die CLI gibt payloadfreies JSON aus, liefert nur bei `PASS` Exitcode `0` und
bei Validierungsfehler oder Teilstatus Exitcode `2`. `--mrts-sha` ist für
jedes Profil erforderlich.

## Verifikationsgrenze

Die Contract-Tests prüfen Schema-/Semantikvalidierung, Fixtures, Adapter,
Dateisicherheit und CLI-Verhalten. Sie sind kein gehosteter Runtime-Lauf, kein
Live-Capability-Claim, keine Framework-Auslieferung und keine Änderung des
NGINX-Produktionspfads.
