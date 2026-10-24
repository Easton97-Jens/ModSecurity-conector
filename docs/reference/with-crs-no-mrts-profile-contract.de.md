# With-CRS/No-MRTS-Vertrag für das exakte Fünf-Connector-Profil

**Sprache:** [English](with-crs-no-mrts-profile-contract.md) | Deutsch

Diese Seite beschreibt die Parent-eigene Evidenzgrenze, die durch
`ci/runtime/lifecycle/with-crs-no-mrts-profile.py` und
`ci/runtime/lifecycle/aggregate-five-connector-with-crs-no-mrts.py`
implementiert wird. Es handelt sich um ein geschlossenes, exaktes Fünferprofil
für einen ausgewählten CRS-Blockfall. Es ist keine Protected-Host-Attestierung
und schließt `FND-CROSS-0004` nicht.

## Umfang und Identität

Das Profil akzeptiert genau einmal jeden dieser fünf Connectoren:

`apache`, `haproxy`, `envoy`, `lighttpd` und `traefik`.

Jede Zelle ist an den exakten Kandidaten-Head (`parent_sha`), den Base-Commit,
Framework-Commit, MRTS-Commit, CRS-Commit und die CRS-Regel-SHA-256 sowie an
GitHub-Run-ID, Versuch, den tatsächlich ausgeführten Test
(`crs_sqli_anomaly_block`) und die Profil-Run-ID gebunden. Die Profil-Run-ID lautet
`with-crs-no-mrts-<github_run_id>-<github_run_attempt>`. Die Zell-Run-ID ist
`crs-<github_run_id>-<github_run_attempt>-<connector>` und wird ausdrücklich
als `cell_run_id_kind: workflow_cell` markiert. Sie ist ein vom Workflow
verwalteter Namensraum und behauptet keine native, von Apache oder HAProxy
ausgegebene Run-ID.

Bei Pull-Request-Läufen erhält der Workflow den unveränderlichen Head und die
Base aus dem Pull-Request-Event. Ein manueller Diagnoselauf verlangt getrennt
übergebene vollständige Eingaben `parent_sha` und `base_sha`; sie werden
syntaktisch geprüft und an Checkout/Aggregat gebunden. Kein Pfad fällt auf
`github.sha` oder einen Branch-Namen zurück.

Der Producer prüft die CRS-Datei
`rules/REQUEST-942-APPLICATION-ATTACK-SQLI.conf`, ihre vertrauenswürdige
vollständige SHA-256 und den Commit der exakt vorbereiteten CRS-Quelle.
Evidenz wird über no-follow-, descriptor-verankerte und begrenzte Prüfungen
privater Dateien gelesen. JSON ist kanonisch, doppelte Schlüssel und nicht
endliche Werte werden abgelehnt; exakte Profilassertions verlangen zusätzlich
exakte JSON-Primitivtypen statt wertgleicher bool/Integer- oder
Integer/Float-Ersetzungen. Die Veröffentlichung erfolgt einmalig in einem neuen
privaten Verzeichnis mit exklusiver Dateierzeugung.

## Native Quellgrenzen

Der Producer leitet Identität weder aus Artefaktverzeichnisnamen noch aus
rohen Pfadangaben ab. Er verwendet je Connector genau eine begrenzte
Quellform:

| Connector | Quelltyp | Erforderliche Quellfakten |
| --- | --- | --- |
| Apache | `apache_case_summary` | Der Workflow startet ausdrücklich nur den ausgewählten Fall (`RUN_ONE_CASE=1`), den auch der Profil-Receipt verlangt. Der ausgewählte Fall `crs_sqli_anomaly_block` steht konsistent in Summary und genau einem JSONL-Ergebnis, mit live ausgeführtem CRS-Deny und HTTP 403. Jeder erforderliche Summary-/JSONL-Skalar und jede Cleanup-Receipt-Identität verwendet einen exakten JSON-Primitivtyp; wertgleiche bool/Integer- oder Integer/Float-Ersetzungen werden abgewiesen. Sein rohes serielles Audit muss genau eine Transaction für die exakte Block-Anfrage, HTTP 403 und genau einen `REQUEST-942-APPLICATION-ATTACK-SQLI.conf`-/Regel-`942270`-Record enthalten. Ein Parent-Cleanup-Receipt wird erst nach dem Teardown getrackter PIDs, der Entfernung der PID-Datei und dem Probe des ausgewählten Listeners publiziert. |
| HAProxy | `haproxy_projected_evidence` | Das versiegelte projizierte Paket wird durch seinen bestehenden strikten Evidence-Owner-Verifier erneut geprüft, der die ausdrücklich gebundene getrennte Evidence-UID/GID verwendet und den normalen Runner nur als Leser verwendet. Seine Quelle und versiegelte Evidence binden die vor dem Runtime-Start vergebene Parent-`cell_run_id` und kennzeichnen sie als `workflow_cell`; sie wird nicht als native HAProxy-ausgegebene ID dargestellt. Das Paket ist exakt und manifestgebunden und protokolliert den ausgewählten HTX/CRS-Deny, HTTP 403, Regel 942270 und vollständiges Cleanup. |
| Envoy, lighttpd, Traefik | `generic_runtime_observation` | Der kanonische Runtime-Observation-Vertrag validiert Connector/Profil/Run sowie Parent-/Framework-/MRTS-Identität, einschließlich Allow 200, Block 403/Deny/Regel 942270, Cleanup und aller fünf auf `false` gesetzten No-MRTS-Flags. |

Die ausgewählten Apache- und HAProxy-Quellen belegen nur die Block-Kontrolle.
Ihr `allow_control` ist ausdrücklich `not_observed`; der Producer erzeugt
keine synthetische Allow-Behauptung. Generische Quellen müssen sowohl Allow-
als auch Block-Beobachtungen liefern.

Der Apache-Receipt zeichnet die workflow-eigenen `cell_run_id`,
`github_run_id` und `github_run_attempt` auf und setzt nur für die tatsächlich
ausgeführten begrenzten Prüfungen auf null:
`tracked_host_processes_remaining`, `tracked_helper_processes_remaining`,
`selected_listeners_remaining` und `pid_files_remaining`. Er behauptet nicht,
dass jeder Prozess oder Socket auf dem Runner inventarisiert wurde. Rohes
Audit, Cleanup-Receipt, Summary und JSONL werden jeweils im Profil-Receipt
gehasht. Eine fehlende, fehlerhafte, nichtkanonische, falsch typisierte,
falsche Regel-, falsche Transaction-, fehlgeschlagene-Cleanup- oder
Restzählungs-Quelle wird abgelehnt, bevor ein Zellpaket publiziert werden kann.

Das HAProxy-Paket bleibt unter seiner getrennten Evidence-Identität. Das Profil
schwächt weder die generischen Privatdatei-Prüfungen noch relabelt oder kopiert
es das Paket als native Evidence: Es ruft den etablierten Verifier des
versiegelten Pakets mit der ausdrücklich getrennten Evidence-UID/GID, den
vertrauenswürdigen Parent-/Framework-/MRTS-Identitäten des Workflows und der
vorab festgelegten Workflow-Zellrun-ID auf und bindet dessen verifizierte
Digests an das Receipt.

## Kanonisches Zellpaket

Jede erfolgreiche Zelle erzeugt in einem neuen `profile-cell`-Verzeichnis
genau diese drei Dateien:

1. `functional-facts.json` — ausgewähltes Ergebnis, expliziter Umfang der
   Allow-Kontrolle, Block-Fakt, Cleanup-Status, No-MRTS-Disposition und
   `source_files_sha256`, der kanonische Digest der geordneten
   Quellartefakt-Bindungsliste.
2. `profile-cell-receipt.json` — vollständige Identitätsbindung,
   Quellartefakt-Hashes, CRS-Provenienz, Workflow-Zellidentität und Hash des
   Faktenpakets sowie tatsächlich ausgeführter Test.
3. `manifest.json` — kanonische Hashes und Größen der ersten beiden Dateien.

Das Aggregat akzeptiert genau fünf solcher Verzeichnisse und weist fehlende,
doppelte, unerwartete, symlinkte, nicht private oder identitätsabweichende
Zellen zurück. Es weist auch nichtkanonisches JSON, wertgleiche aber falsche
Primitivtypen, zusätzliche Dateien, ungültige Hashes, Receipt-Quellpfade oder
-Digests mit Abweichung von `source_files_sha256`, falsche Profil- oder
Connectoridentitäten sowie Abweichungen bei Quell- oder Workflow-Pins zurück.
Das Aggregat erzeugt getrennt und einmalig
ein Paket mit `aggregate.json`, `aggregate.md`, `aggregate.de.md`,
`matrix-24.json`, `matrix-24.md`, `matrix-24.de.md` und `manifest.json`.

## Bedeutung der Ergebnisse

Das Aggregat hält vier Entscheidungen getrennt:

- `technical_validity` ist nur dann `PASS`, wenn die exakt fünf unabhängig
  validierten Zellpakete samt Bindungen vorhanden sind.
- `functional_success` ist nur für den ausgewählten CRS-Blockfall in allen
  fünf Zellen `PASS`. Die unbeobachtete Allow-Kontrolle von Apache/HAProxy
  wird dadurch nicht aufgewertet.
- `matrix_24_completeness` zeichnet die ehrliche aktuelle Disposition aller
  24 CRS/MRTS-Zeilen auf. Die feste aktuelle Disposition lautet: 5 `passed`,
  6 `blocked`, 13 `not_run`, 0 `failed` und 0 `not_applicable`; die Disposition
  ist vollständig, die Ausführungsabdeckung jedoch nicht.
- `merge_eligible` bleibt `false`. Technische Gültigkeit und ausgewählter
  Funktionserfolg sind keine Merge-Freigabe.

Die sechs blockierten Zeilen sind die nicht verfügbaren Framework-eigenen
MRTS-Routen für Envoy, Traefik und lighttpd (je zwei MRTS-Profile). Die übrigen
13 Zeilen bleiben `not_run`; aus einem anderen Connector, Profil oder
historischen Artefakt wird kein Ergebnis abgeleitet. Die durch
`FND-CROSS-0004` dargestellte Framework-Abnahmekondition bleibt separat
blockiert. Keine Zeile wird als Protected-Host-Attestierung bezeichnet und
kein Finding wird durch diesen Vertrag geschlossen.

## Verhältnis zur Workflow-Abnahme

Der Workflow muss entweder den exakten Head und die Base des Pull-Request-
Events oder explizite vollständige manuelle Eingaben liefern, beide Commits im
exakten Checkout prüfen und GitHub-Run-ID, Versuch, frisch vorbereitete CRS-
Provenienz sowie die fünf Quellpakete bereitstellen. Für Apache übergibt er
diese Runtime-Identität an den Harness, validiert rohes Audit und Cleanup-
Receipt und erzeugt erst danach die Zelle. Ein erfolgreiches Aggregat ist ein
auf diese konkrete Ausführung begrenztes Evidenzergebnis. Es ersetzt keine
Repository-Regeln, erforderlichen Checks, Sonar-, Framework-/MRTS-Abnahme,
unabhängige Hostevidenz oder spätere Merge-Entscheidung.
