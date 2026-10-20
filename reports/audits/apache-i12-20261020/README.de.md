# Apache-Verfahren zur abschließenden Prüfung physischer Nachweise

Englische Begleitdatei: [README.md](README.md).

`final_review.py` ergänzt den vorhandenen Apache-Batchextraktor und die
unveränderten gemeinsamen Lifecycle-Validatoren um ein konservatives
Root-Prüfverfahren. Es führt keinen Hosttest aus. Seine synthetischen Tests
sind keine Hostnachweise.

Die CLI verlangt ausdrückliche Pfade und SHA256-Prüfsummen für die unveränderliche
Baseline, den Fallplan, den unsignierten Index aller 155 Fälle, die erwartete
Identität und die Admission-Spec sowie das aufbewahrte Attempt-Verzeichnis und
ein neues Ausgabeverzeichnis. Siehe
`rtk proxy python3 -B reports/audits/apache-i12-20261020/final_review.py --help`.
Für die tatsächliche Ausführung ist die Python-Umgebung des Repositorys zu
verwenden. Eine optionale separate Oracle-Prüfdatei benötigt ebenfalls ihre
SHA256. Das JSON der erwarteten Identität verlangt `run_id`, vollständige
`parent_sha`, `framework_sha`, `mrts_sha` sowie vollständige SHA256-Werte
`apache_sha256`, `module_sha256`, `sdk_sha256`. Diese Werte müssen das tatsächliche
versiegelte Produkt und den Lauf beschreiben; sie werden nicht aus Kandidaten
abgeleitet.

Ohne `--approve-supported-families` erzeugt das Verfahren Entscheidungen mit
null-Ergebnissen. Der ausdrückliche Schalter ruft ausschließlich die Prüfung
der registrierten begrenzten Fallfamilien auf. Er löst kein Oracle auf und gibt
keine neue Testumgebung frei. Das Verfahren verlangt Gleichheit mit einer neuen
Extraktion aus dem aufbewahrten physischen Attempt und der Spec, alle 35
anwendbaren gemeinsamen Messrollen, alle erforderlichen Extraktorprüfungen,
einen tatsächlich vollständig ausgeführten Fallvertrag, exakte Produkt- und
Laufidentitäten sowie ausdrückliche Prädikate für Wire, Backend, Regel, native
Phasen und Append-Bytezahlen, EOS, physischen Commit, Finish/Free,
Descriptor-/Prozessbereinigung und unabhängige Kontrollanfragen. Das ursprüngliche
Oracle und frühere Fehler bleiben unverändert.

Die Registry umfasst vier genaue Request-IDs: leer, einzelner Chunk, CSV und
EOS genau einmal. Content-Type vorhanden/fehlend und Charset vorhanden/fehlend
bleiben null: Wire-Felder allein beweisen keine native Mapper-/Header-/MIME-
Weitergabe; die vorhandene generische MIME-Beobachtung ist kein vollständiger
unabhängiger Nachweis für diese vier Pflichten. CSV bezeichnet rohe Requestbytes; daraus folgt kein CSV-spezifischer
Engine-Prozessor. Andere Familien bleiben auch bei vollständigen strukturellen
Rollen null. Jede registrierte Request-ID hat ausdrücklich die Lifecycle-
Oraclephase 2. Sie ist an genau eine tatsächlich erfolgreiche Rückgabe von
`native_process_request_body` in den physischen nativen Phasenbeobachtungen
gebunden. Die P1-Sentinel-Regel 91041950 des Plans wird getrennt gegen natives
Audit und physisches Common-Event geprüft; ihre Regelphase ist nicht die
Lifecycle-Oraclephase. Zusätzliche Oracle-Schlüssel oder Scope-Semantik, die das Verfahren
nicht auswerten kann, bleiben unbekannt. Bei vorhandenem `scope`-Schlüssel wird
ausschließlich die genaue Zeichenfolge `SUPPORTED_ORACLE_SCOPE` im Quelltext
unterstützt; ein anderer Geltungsbereich benötigt eine eigene unabhängige
Implementierung und Prüfung.

Die Reihenfolge wird anhand der vorhandenen physischen nativen API-JSONL
geprüft, die Enter- und Return-Edges bewahrt. Jede P2-/P4-/Finish-/Logging-/
Cleanup-/Retirement-Operation benötigt genau einen passenden tatsächlichen Call
mit steigender nativer Sequenz und monotoner Zeit, gebunden an PID, Lauf und
Allokation des Hauptvorgangs. Request-APR-EOS muss vor P2-Enter liegen;
Response-APR-EOS muss nach P2-Return und vor P4-Enter liegen. Auf den gepaarten
P4-Return folgt der physische Socket-Commit, danach Common-Finish, erfolgreiches
natives Logging, Common-Cleanup, native Freigabe und Retirement der Zuordnung
in dieser Reihenfolge. Ein Zähler allein genügt nicht. Fehlende Enter-/Return-
Nachweise oder ein physisch früherer Commit lassen den Fall unqualifiziert.
Das Verfahren bewertet einen früheren Streaming-Commit nicht als Produktfehler.

Config- und Prä-Nativ-Parserkontrollen verweisen immer auf das separate Verfahren
`review_controls.py` und dessen ausdrückliche Approval-Eingabe. Dieses Verfahren
importiert deren Freigaben nicht. Ein Root-Prüfer kann ihre unabhängig validierten
Pakete zusammen mit dem Paketindex dieses Verfahrens an das Apache-Ledger geben.

`decisions.json` bewahrt alle 155 ursprünglichen Reihen, einzelne
`PASS`-/`FAIL`-/null-Prädikate, physische Referenzen, das ursprüngliche Oracle,
eine getrennte nullable Oracleentscheidung und ein Registry-/Lückeninventar pro
Fall. Ein fehlgeschlagenes oder unbekanntes Prädikat verhindert ein freigegebenes
Paket. `reviewed-packets.json` führt ausschließlich Pakete auf, die der
unveränderte gemeinsame Validator vor Veröffentlichung akzeptiert hat.
`i12_complete` bleibt false. Eingabedateien und alle erkannten transitiven
JSON-Referenzen werden vor der Prüfung gehasht und vor Veröffentlichung erneut
validiert, einschließlich direkt gelesener Control-Receipt-, Prozess- und
Responsedateien. Der JSON-Graph ist auf 10.000 Referenzen und 64 MiB pro JSON-Datei
begrenzt; eine Überschreitung führt zum Abbruch.

Ein lesendes Inventar des aufbewahrten `case-plan-v4.json` (SHA256
`19ab9da01d000f8875f21d12c4322b102717fa8a7871edb856201dec11baba51`)
umfasste alle 155 IDs: 4 registrierte begrenzte Request-IDs, 4 fehlende unabhängige
native Header-/MIME-Weitergabenachweise, 14 getrennte typisierte
Kontrollen, 24 physische Fehlerfamilien mit fehlender eigener Semantik, 24
Sonderoperationsfamilien mit fehlender eigener Semantik, 74 Fälle mit fehlender
unabhängiger Erwartungs- und Familienprüfung sowie 11 Fälle mit geplanten
Erwartungen und fehlendem vollständigem unabhängigem Familienprädikat. Das sind
Implementierungs-/Lückenkategorien, keine Testergebnisse oder neu vollständig
qualifizierten PASS-Fälle. Ein späterer Plan wird eigenständig inventarisiert.

Verifikation: `rtk proxy <Repository-Python> -B -m unittest discover -s tests -p
test_apache_i12_final_root_review.py -v`. Negative Mutationen umfassen vollständige
35-Rollen-Pakete mit falscher Regel, Status, Backendanzahl/-Bytezahl, nativen
Appendbytes, Phase, EOS, Commitreihenfolge, Finish/Free, Bereinigung, Neighbor-
und nativer Allokationsidentität, Oraclephase/-Scope sowie fehlendem unabhängigem
Oracle beziehungsweise Nachweis.
