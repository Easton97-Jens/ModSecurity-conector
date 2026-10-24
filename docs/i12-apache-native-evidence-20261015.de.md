# Apache I12: native Host-Evidence — 2026-10-15

**Sprache:** [English](i12-apache-native-evidence-20261015.md) | Deutsch

**Historischer Kampagnenbericht.** Die folgenden Ergebnisse gehören nur zur
beibehaltenen Kampagne vom 2026-10-15 und ihren dokumentierten Build-Identitäten.
Die getrennte [aktuelle Kampagne vom 2026-10-22](../reports/audits/apache-i12-20261022/README.de.md)
führte die Produktquelle `57e94983e808bcc4c1ca4f5fcf9745f6dc9d4a38`
aus und verwendete das unabhängig gehärtete Prüfverfahren, das unter
`de23f2fa4b490c66f15ac97f2646434351f05c5e` veröffentlicht wurde. Dessen
aktuelles Ledger aller 155 Fälle, einschließlich vier frischen vollständig
qualifizierten Lifecycle-PASS und 151 null-Ergebnissen, ist für die Qualifikation
der aktuellen Quelle maßgeblich. Auch dieses Ledger behauptet kein
`I12_COMPLETE`.

Die Apache-Bewertung bleibt **unvollständig**. Dieser Bericht erteilt keine Freigabe und behauptet kein `I12_COMPLETE`. Das [maschinenlesbare Ledger aller 155 Fälle](../reports/audits/apache-i12-20261015/case-ledger.json) ist für jede Original-ID, Qualifikation, fehlende Beobachtung und Evidence-Referenz maßgeblich. Fehlende Beobachtungen bleiben `null`; eine Ausführung qualifiziert keine fremden Aliase.

## Umfang und Identität

Der isolierte Evidence-Branch `codex/i12-apache-410-20261015` basiert auf PR #410 mit `f27eb59b53beff6f65384fc2e5037881a3052c01`. Lieferziel ist `work/pr382-i12-host-evidence-20261011`, nicht `master`. PR #410 wird nicht direkt geändert.

Die wiederverwendete versiegelte, instrumentierte Runtime nennt die Produktquellbasis `02754040bced960cfc1857416cd7101bb3116ef4`. Diese Identität unterscheidet sich von der Basis des Evidence-Branches. Vergleiche in den Paketen binden ausgewählte Apache-/Common-Dateien an die aktuelle Basis; sie beweisen keine Runtime-Identität des gesamten Repositorys. Framework: `99a7985c1be92a2297b1b59208f64df6768f2cbf`; reine MRTS-Metadaten: `8a6bb546c4c81d8ffc7be801dceac60c6925685f`. MRTS wurde weder ausgeführt noch geändert.

Apache `2.4.66`, APR `1.7.6` und libModSecurity `3.0.14` gelten ausschließlich zusammen mit den Binary-, Modul-, SDK-, effektiven Config-, Run-, UID-, Prozess- und Quellhashes des jeweiligen freigegebenen Pakets. Ergebnisse übertragen sich nicht automatisch auf andere Builds. Native Hosts laufen im bestehenden privaten Controller mit UID/GID `65534`, ohne Capabilities, mit `NoNewPrivs`, schreibgeschützten Eingaben, begrenzten Ressourcen sowie getrennten Netzwerk-, Mount- und PID-Namespaces.

Ergänzt wurden ausschließlich Apache-I12-Fixtures, Harness-Erweiterungen, Tests und Apache-Evidence. Zentrale Matrix, Berichtgeneratoren, Capture-Manifest, gemeinsame Observer, andere Connectoren, Workflows, Framework-/MRTS-Gitlinks und Produktivcode liegen außerhalb dieser Änderung.

## Qualifikationsstand

| Gegenstand | Beobachtetes Ergebnis |
| --- | --- |
| Apache-Pflichtfälle | 155 |
| Historisch ausgeführte Fälle | 25 |
| Historische Config-PASS | 9 |
| Historischer vollständiger Lifecycle-PASS | 1 |
| Frische tatsächliche Host-Ausführungen, getrennte Pflicht-IDs | 28: 8 neu qualifiziert und 20 Teilpakete, einschließlich der unsignierten Baseline-Wiederholung |
| Pflicht-IDs ohne frische Host-Ausführung | 127 |
| Insgesamt erhaltene private Versuche | 46, einschließlich Setup-Fehlern und separater Kontrolle ohne Sinkfehler |
| Eindeutige vollständige Lifecycle-PASS, alt und neu | 9; 146 IDs haben weiterhin keinen vollständigen Lifecycle-PASS |
| Neu vollständig qualifizierte Host-Fälle | 8: sieben Requests und der unabhängig abgeglichene Duplicate-Header-Fall |
| Gelöste der ursprünglich 54 Oracle-Erwartungen | 8, einschließlich des historischen Lifecycle-Falls |
| Weiter offene Original-Oracles | 46 |

Die Zahlen stammen aus dem maschinenlesbaren Ledger; die Einzelqualifikation bleibt maßgeblich. Die Baseline-Wiederholung bestätigt das Verhalten, bleibt aber ein unsignierter Kandidat und fügt daher keine neu qualifizierte ID hinzu. Die sieben Request-Fälle sind `NEED-request-empty`, `NEED-request-single-chunk`, `NEED-request-content-type-present`, `NEED-request-content-type-missing`, `NEED-request-charset-present`, `NEED-request-charset-missing` und `NEED-request-csv`. Ihre getrennten Ausführungen erhalten Client-Ergebnisse, Backendzahlen, native Phasenaufrufe, physische Events, erforderliche EOS-/Commit-Reihenfolge, Finish, Cleanup und Folgerequests. Eine frische Baseline-Wiederholung erhält außerdem den bestehenden Lifecycle-Nachweis.

`phase2_truncated` sendet einen vollständig gerahmten 65-Byte-Request mit nativem `ProcessPartial`. Das beweist **keinen** abgeschnittenen HTTP-Transport. MIME-, Response-Limit-, Deny- und Redirect-Ausführungen bleiben einzelne Host-Beobachtungen, wenn ihre ursprünglichen Eventmetadaten oder Lifecycle-Pflichten fehlen. Phase-3-Fixtures liefern auch für den Nachbarn 403/302, weil die Fixture-Response-Header global gelten; diese Pakete bleiben unvollständig.

## Duplicate-Header-Oracle

Originalfixture und ursprünglicher Fehler bleiben erhalten. Vier Grenzen wurden unabhängig geprüft:

1. Die Wire-Aufzeichnung enthält zwei Felder `X-No-Crs-Duplicate` mit `one` und `two`.
2. Der gebundene Apache-Core-/APR-Pfad führt sie zu einem Feld `one, two` zusammen.
3. Der Connector-Mapper reicht das resultierende Feld ohne erfundene Aufteilung weiter.
4. Native SDK-Proben unterscheiden das ursprüngliche Zweiwerte-/Anzahl-zwei-Oracle vom zusammengeführten Einwert-/Anzahl-eins-Oracle.

Eine zusätzliche Apache-Fixture verwendet `one, two` ausschließlich für diese bestätigte, versionsgebundene Core-Semantik. Der unabhängige Abgleich qualifiziert diesen begrenzten Fall; sein tatsächlicher Host-Erfolg löscht das ursprüngliche FAIL nicht. Ein einzelnes literales Feld `one, two` bleibt hinter dieser Grenze mit einem zusammengeführten Paar mehrdeutig; nachgelagerte SDK-Evidence kann die ursprüngliche Wire-Anzahl nicht rekonstruieren.

## Physische Sink-Wiederholungen

Das [begrenzte Evidence-Verzeichnis](../reports/audits/apache-i12-20261015/) erhält die fünf ursprünglichen Fehlerdefinitionen und deren Readback. Fünf physische Szenarien beweisen nicht sämtliche operationsbezogenen `NEED-physical-event-sink-*`-Pflichten.

| Fehler | Tatsächlicher Hauptclient | Folgerequest / Nachbar | Backend Hauptrequest / Folge / Nachbar | Physische Grenze |
| --- | --- | --- | --- | --- |
| Fehlendes Elternverzeichnis | 500, 571 Bytes, Exit 0 | 200 / 200 | 0 / 1 / 1 | Common-/POSIX-Ablehnung vor APR; APR-Open `null` |
| Pfad `/dev/full` | 500, 571 Bytes, Exit 0 | 200 / 200 | 0 / 1 / 1 | Common-/POSIX-Ablehnung vor APR; APR-Open `null` |
| Elternverzeichnis Modus `0500` | 500, 571 Bytes, Exit 0 | 200 / 200 | 0 / 1 / 1 | Common-/POSIX-Ablehnung vor APR; APR-Open `null` |
| Geschlossener Descriptor | 500, 571 Bytes, Exit 0 | 200 / 200 | 0 / 1 / 1 | Echtes APR-`EBADF` 9; null geschriebene Bytes |
| Physisches ENOSPC | 500, 571 Bytes, Exit 0 | 200 / 200 | 0 / 1 / 1 | Echtes APR-`ENOSPC` 28; null geschriebene Bytes |

ENOSPC entsteht durch `dup2`-Umbindung des zugelassenen aufgabeneigenen Descriptors auf `/dev/full` mit anschließendem echtem APR-Write. Erschöpfte Dateisystemkapazität wurde nicht getestet.

Die letzten beiden Fehler führen vor dem unveränderten APR-Aufruf eine echte Descriptor-Operation aus; sie ersetzen keinen APR-Rückgabewert. Spätere native Sink-Schreibvorgänge gelingen mit neu geöffneten Descriptoren. Dauerhaft ungültige Pfade, Gerätedateien und Berechtigungen werden nicht repariert: erfolgreiche Folgerequests beweisen requestbezogene Wiederherstellung des Hosts. Folge- und Nachbarclient erhalten jeweils 3 Bytes und Exit 0. Native/API- und Host-Transkripte, physisches JSONL, Prozess-Maps, FD-Stichproben und Host-/Backend-/Controller-Cleanup bleiben getrennte Beweise.

Eine fehlerfreie Kontrolle an derselben Grenze verwendet `/sink-disruptive` und Regel `120016`, um gewöhnliche Ablehnung von Sinkfehlern zu unterscheiden. Die Konfiguration dieser Regel beweist ihre Ausführung nicht: die fehlerhaften Pfade protokollieren auch die frühere nichtterminale Regel `120001`. Die fehlerfreie Kontrolle liefert 403 mit 239 Bytes und physischen Common-Events für `120001`, danach `120016`. Auch Fehlerfälle enthalten eine native disruptive 403: Das Fehlen des physischen Common-Events zu `120016` beweist nicht, dass die Engine die Regel nicht ausgewertet hat. Unabhängige native Audit-Zuordnung zu `120016` bleibt `null`. Die Kontrolle belegt erfolgreiche APR-Schreibvorgänge mit 1052/1087/1049/1049 Bytes. Alle 18 beobachteten Transaktionen haben genau ein natives/Common-Cleanup; alle sechs zugehörigen Controller melden sauberes abschließendes Cleanup.

Alle fünf Fehlerpakete bleiben unvollständig qualifiziert: natives Audit, die Commit-Bindung des Apache-Standardfehlerrenderers und weitere ursprüngliche Lifecycle-Beobachtungen fehlen. `full_lifecycle_qualified` bleibt false; fehlende Ergebnisse bleiben `null`.

## Fixture-Fehler und unabhängige Reparatur

Erste kanonische Ausführungen endeten mit Exit 78, weil ihr verpflichtendes Preamble `tests/rules/no-crs-baseline.conf` fehlte. Apache-spezifische Launch-Einstellungen reichen nun `MODSECURITY_RULE_PREAMBLE_FILE` weiter; die Framework-Validierung bleibt erhalten. Fehlgeschlagene Versuche bleiben Setup-Fehler.

Response-Limit-Fixtures zeigten anschließend die doppelte Regel `1100301` aus lokaler Originalregel und kanonischem Preamble. Lokal fehlt explizites `t:none`, kanonisch ist es vorhanden. Echte SDK-Proben verglichen beide Formen mit denselben Direktiven, ohne `SecDefaultAction`, und mit den exakten 64-/65-Byte-ASCII-Fixture-Payloads. Append-/P4-Ergebnisse, Intervention, Status und protokollierte Regel-IDs stimmen überein. Neue Fixtures entfernen ausschließlich das lokale Duplikat und erhalten kanonische Regel, Original-YAML/-Hash, Erwartungen, Beweis und ursprünglichen Ladefehler. Dies ist ein begrenzter semantischer Nachweis, keine allgemeine Textgleichheit.

Die korrigierte `ProcessPartial`-Fixture prüft einen nativen 64-Byte-Inspektionspuffer mit nichtdisruptiver Regel `91041504`, unabhängig begründet durch SDK `src/transaction.cc:1195-1206`. Frühere Marker-Erwartungen, die ihre Payload nicht treffen konnten, bleiben als Fixture-Fehler erhalten. Reject-Erwartungen wurden nicht für ein künstliches PASS verändert. Die deduplizierten At-/Over-Limit-Wiederholungen erreichen echte Host-Ausführung mit Driver-/Controller-Exit 0. Der Reject-Versuch `attempt-1792074553855617952` endet ohne HTTP mit Driver 78/Controller 77: Der ursprüngliche NGINX-spezifische Fall mit `runtime_materializable:false` führt zu leerer Auswahl und `IsADirectoryError`. Dieser erhaltene Setup-Fehler lässt einen echten Apache-Reject-Treiber offen; für Reject liegt bislang nur unabhängige SDK-Evidence vor. Kein gemeinsames Validierungsflag wird geändert. Host-Ablehnung sowie Event-/Lifecycle-Metadaten benötigen weiterhin Einzelqualifikation.

Ein Controller-Versuch meldete drei vorübergehend verbleibende Namespace-Prozesse. Ein späteres Readback fand sie nicht mehr; der ursprüngliche fehlgeschlagene Cleanup-Beleg bleibt erhalten. Das erste Ergebnis wird nicht stillschweigend als sauberes Cleanup gewertet.

## Verifikation und Reproduktion

Frische Prüfungen der Aufgabe umfassen 122 fokussierte Tests plus fünf Paketierungs-Qualifikationstests, 76 native Regressionstests, Capture-Verifikation plus 15 Capture-Tests und die gezielten Launcher-Prüfungen. Die Mapper-Mutation wurde durch fünf Tests mit 14 fehlgeschlagenen Assertions erkannt; die Sink-Mutation durch acht Tests mit zwei Fehlern. Mutationsergebnisse sind erwartete Negativbeweise, keine erfolgreichen unveränderten Testläufe. Exakte Befehle, Exits, Hashes und Geltungsbereiche stehen in den [paketierten Belegen](../reports/audits/apache-i12-20261015/). [Identität](../reports/audits/apache-i12-20261015/identity.json) enthält vollständige Binary-/SDK-/Modul-Hashes; [Readback](../reports/audits/apache-i12-20261015/readback.json) zeigt alle Versuchs-Exits und begrenzte beobachtete Fakten. Diese Zusammenfassungen ersetzen die physischen SHA-gebundenen Aufzeichnungen unter dem externen Run-Root nicht.

Dokumentationsprüfungen bestanden (Exit 0): `check-bilingual-docs`, `check-doc-links` und Repository-Pfadreferenzen mit dem vorhandenen Framework read-only in einem privaten Mount-Namespace. Originale Gitfiles/Gitlinks und Host-Mounts blieben erhalten. Der erste direkte Worktree-Lauf scheiterte am nicht befüllten Framework; korrigierter deutscher Link und Namespace-Wiederholung sind dokumentiert. `new-change-record.py check` und `git diff --check` bestanden (Exit 0). Die begrenzten Artefakte `root-review-*.py` erhalten die genauen aufgabenspezifischen Review-Assertions; sie benötigen die erhaltenen Run-Inputs und sind kein allgemeiner Auto-Approval-Mechanismus.

Wiederverwendbare Einstiegspunkte sind `ci/runtime/lifecycle/apache-i12/prepare.py`, `prepare_sinks.py`, `review.py`, `ledger.py` und `package.py`. Shell-Aufrufe verwenden RTK. Vorbereitung versiegelt neue Eingaben und startet keinen Host. Root führt den bestehenden freigegebenen privaten Controller aus; `launch.py` / `sink_launch.py` erhalten tatsächlich abgewartete Exits. Review extrahiert Kandidaten; unabhängige explizite Prüfung geht ihrer Ledger-Aufnahme voraus.

```sh
rtk proxy python3 ci/runtime/lifecycle/apache-i12/prepare.py --list
rtk proxy python3 ci/runtime/lifecycle/apache-i12/review.py --help
rtk proxy python3 ci/runtime/lifecycle/apache-i12/ledger.py --help
rtk proxy python3 ci/runtime/lifecycle/apache-i12/package.py --help
rtk git diff --check
```

Die Vorbereitung benötigt die vorhandene PyYAML-Umgebung, etwa das bereits versiegelte Binding `python-site`; daraus folgt keine Paketinstallation. Ausgaben verwenden neue Verzeichnisse unter der genehmigten externen Run-Wurzel. `--deduplicate-response-rule` benötigt zusätzlich den exakten nativen Semantiknachweis und lehnt veränderte Eingaben ab.

## Restarbeit und Liefergrenze

Das Ledger nennt jeden fehlenden Fall und jedes unvollständige Feld. Streaming-/Chunk-Aufteilung, Transport-Trunkierung, Keep-alive, nicht ausgeführte Fehler und fehlende physische oder Lifecycle-Metadaten lassen sich nicht aus abgeschlossenen Request-Fällen oder Sink-Proben ableiten. Bestätigte Produktfehler benötigen einen getrennt freigegebenen Fix auf #382; dieser Branch enthält keinen Produktfix.

Normale Commits und ein Draft-PR sind für den isolierten Branch mit dem Zielbranch von #410 autorisiert. Dieser Bericht dokumentiert Evidence, kein CI-, Merge- oder Freigabeergebnis. Force-Push, automatischer Merge, Release und I12-Abschluss werden weder autorisiert noch behauptet.
