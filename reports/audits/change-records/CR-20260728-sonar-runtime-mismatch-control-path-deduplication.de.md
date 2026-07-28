# Change Record: Parent-Runtime-Mismatch-Control-Path-Deduplizierung für SonarQube Cloud

**Sprache:** [English](CR-20260728-sonar-runtime-mismatch-control-path-deduplication.md) | Deutsch

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | CR-20260728-sonar-runtime-mismatch-control-path-deduplication |
| Datum (UTC) | 2026-07-28 |
| Basis-Revision | 8e8acb8dab1cd03723de269cab7da7dd62e5e010 |
| Umfang und Grenze | Ausschließlich Parent `ci/evidence/reports/generate-verified-runtime-mismatch-analysis.py` und der fokussierte Test `tests/test_report_conditional_remediation.py` sowie dieses englisch/deutsche Change-Record-Paar und seine Indizes. Framework, MRTS, beide Gitlinks, Workflows und generierte Reports bleiben unverändert. |
| Finding-Verknüpfung | Parent-SonarQube-Cloud-Remediation eines doppelten Runtime-Mismatch-Control-Pfads, gefolgt vom Exact-PR-Head-Code-Smell `AZ-o2G_i1eeMvlV2C-0t`, Regel `python:S1192`, für das wiederholte Literal `nginx-summary.json`. Der Folge-Kandidat behauptet keine Alert-Closure oder Delivery-Vollständigkeit. |

## Motivation und Problemstellung

Der Runtime-Mismatch-Report enthielt wiederholt dieselbe Zusammensetzung der
no-MRTS-Control-Root aus `build_root`, der ersten CRS-Komponente einer
slash-haltigen Variante und dem Connector. Die getrennten Zusammensetzungen
erschwerten die Wartung und trugen zu dupliziertem Control-Path-Code bei.

Die angeforderte Remediation zentralisiert nur diese bereits vorhandene
Root-Zusammensetzung im privaten Helper `_no_mrts_control_identity`. Sie ist
bewusst keine Änderung daran, welche Evidence akzeptiert wird oder wie ein
Report erzeugt wird.

Der erste exakte Draft-PR-Head legte danach drei wiederholte Verwendungen des
NGINX-Force-All-Summary-Dateinamens im neu konzentrierten Source-Bereich offen.
Das Follow-up verwendet eine private benannte Konstante für diesen unveränderten
Dateinamen; es ändert weder Summary-Location noch Reader-Verhalten.

## Akzeptanzkriterien

- `_no_mrts_control_identity` erhält das bestehende Slash- und First-CRS-
  Verhalten und liefert die vorhandene feste no-MRTS-Control-Root nur für
  Apache, HAProxy und NGINX.
- Apache und HAProxy behalten ihre vorhandenen Result-Layouts; NGINX behält
  seine vorhandene Summary-Traversal.
- Die vorhandenen Pass/`403`-Gates und die NGINX-Phase-4-Marker-Semantik
  bleiben unverändert.
- Eine private NGINX-Force-All-Summary-Dateinamen-Konstante erhält den exakt
  vorhandenen Dateinamen an allen drei vorhandenen Reader-Stellen.
- Die fokussierte Conditional-Remediation-Testkontrolle besteht alle 9 Tests.
- Die Runtime-Environment-Snapshot-Contract-Testkontrolle besteht alle 9
  Tests nur in ihrem disposablen externen Overlay mit dem read-only
  Parent-gebundenen Framework-Archiv `47e50e7bc43ba7a3b5bad1a9448111794f664cc0`.
- Es wird kein Ergebnis für Report-Generation, `runtime-all`, Matrix,
  Framework/MRTS, Hosted oder Delivery behauptet.

## Implementierungsentscheidung und Begründung

`_no_mrts_control_identity` erhält `build_root`, `connector` und `variant`;
es verwirft eine Variante ohne `/` und einen Connector außerhalb der festen
Apache/HAProxy/NGINX-Menge. Für eine akzeptierte Variante behält es die erste
Komponente aus `variant.split("/", 1)` und liefert die bereits vorhandene
Root `build_root / "full-matrix" / crs / "no-mrts" / connector` zurück.

`no_mrts_control_evidence`, `no_mrts_case_control_evidence` und
`nginx_no_mrts_phase4_log_control` verwenden diese Identität, behalten aber
ihre eigene Result-Auswahl und Prädikate. Apache und HAProxy behalten ihre
vorhandenen Runtime-Result-Layouts. NGINX behält seine vorhandene
Summary-File-Traversal einschließlich der Phase-4-Marker-Behandlung. Der
Refactor führt keine neue Connector-Route und keine Path-Broadening ein.

`NGINX_FORCE_ALL_SUMMARY_FILE` liefert denselben Leaf `nginx-summary.json` an
alle drei unveränderten NGINX-Summary-Pfade. Der fokussierte Test prüft den
Wert der Konstante, während seine vorhandenen Temporary-Tree-Kontrollen alle
drei Consumer ausüben.

## Geänderte Dateien

- `ci/evidence/reports/generate-verified-runtime-mismatch-analysis.py`
- `tests/test_report_conditional_remediation.py`
- `reports/audits/change-records/README.md` und `README.de.md`
- dieses englische/deutsche Change-Record-Paar

## Ausgeführte Befehle

| Befehl oder Kontrolle | Tatsächliches Ergebnis |
| --- | --- |
| Fokussierte Conditional-Remediation-Testkontrolle (9 Tests) | bestanden. |
| Runtime-Environment-Snapshot-Contract-Testkontrolle (9 Tests) | nur in einem disposablen externen Overlay mit dem read-only Parent-gebundenen Framework-Archiv `47e50e7bc43ba7a3b5bad1a9448111794f664cc0` bestanden. |
| `git diff --check` | bestanden; kein Whitespace-Fehler wurde gemeldet. |
| `rtk proxy env PYTHONDONTWRITEBYTECODE=1 make check-bilingual-docs` | blocked_environment: Es meldete 20 fehlende lokale Ziele unter dem nicht ausgefüllten Framework-Gitlink; keine Diagnose nannte dieses Change-Record-Paar oder seine Indizes. |
| Disponibles Exact-Candidate-Overlay mit dem read-only Parent-gebundenen Framework-Archiv: `check-bilingual-docs.py`, `check-repository-path-references.py` und Framework-`check-doc-links.py` | bestanden: `bilingual docs ok`, `repository path references: PASS` und `doc links ok`. |

## Security-Auswirkung

Die Auswahl der no-MRTS-Control-Identität des Reports ist eine Evidence-
Reclassification-Grenze. Die fokussierte Security-Review fand keinen
validierten Befund. Die Änderung zentralisiert die vorhandene feste Root-
Zusammensetzung und identifiziert nur die vorhandenen Apache-, HAProxy- und
NGINX-Routen; sie verbreitert keinen Pfad und fügt keine neue Evidence-Quelle
hinzu.

Durch diesen Batch werden keine Framework- oder MRTS-Quellen, Gitlinks,
Runtime-Pfade, Access-Controls oder generierten Reports geändert.

## Runtime-Evidence

Die beiden 9-Test-Kontrollen sind nur lokale Source- und Snapshot-Contract-
Evidence. Das Snapshot-Contract-Ergebnis ist auf sein disponables externes
Overlay und das read-only Parent-gebundene Framework-Archiv begrenzt. Es ist
keine Evidence für Report-Generation, `runtime-all`, eine Connector-Matrix,
eine Framework/MRTS-Runtime oder ein Hosted-Ergebnis.

## Bekannte Einschränkungen

Für diesen Kandidaten wurden weder Report-Generation noch `runtime-all`,
Connector/CRS-Matrix oder Framework/MRTS-Check ausgeführt. Der vorherige
exakte PR-Head hatte ein `OK` Quality Gate und null neue Duplikation, legte
aber `AZ-o2G_i1eeMvlV2C-0t` offen; frischer Hosted-Nachweis für das
Dateinamen-Konstanten-Follow-up bleibt erforderlich. Es wurde kein generierter
Report oder Runtime-Matrix-Artefakt erstellt oder aktualisiert.

## Verbleibende Risiken

Künftige Änderungen an der festen Connector-Menge, der First-CRS-Behandlung
oder der no-MRTS-Control-Root-Zusammensetzung könnten Evidence reklassifizieren.
Die fokussierten Tests begrenzen das reviewte Verhalten, aber ein nicht
ausgeführter Report-Generation- oder Runtime-Matrix-Pfad könnte eine
Integrationsdifferenz außerhalb dieses Batch zeigen.

## Nicht ausgeführte Prüfungen mit Begründung

- Report-Generation wurde nicht ausgeführt; sie liegt außerhalb dieser
  Duplication-only-Source-Remediation, und kein generierter Report wurde
  aktualisiert.
- `runtime-all` und Matrix-Checks wurden nicht ausgeführt; ihre Runtime- und
  Artefaktvoraussetzungen liegen außerhalb des reviewten lokalen Source-Test-
  Umfangs.
- Framework- und MRTS-Checks wurden nicht ausgeführt. Das einzige Framework-
  Material der Snapshot-Contract-Kontrolle war das oben genannte read-only
  Parent-gebundene Archiv; kein Framework- oder MRTS-Worktree, keine Quelle,
  kein Branch und kein Gitlink wurden geändert.
- Das native Target `make check-doc-links` wurde nicht ausgeführt, weil es den
  nicht ausgefüllten Framework-Gitlink verwenden würde; das Framework-eigene
  Äquivalent `check-doc-links.py` bestand nur im disponiblen read-only-Archiv-
  Overlay oben.
- Hosted-Checks wurden nicht ausgeführt, weil dieser Kandidat keinen
  ausgelieferten Exact-Head-Review- oder Analysezyklus besitzt.

## Finaler Diff- und Review-Status

Der initiale Commit `ba8d2b2b9048ccc0d1716cc2d5b689bbe24c64c8` liegt auf
Draft-PR #152. Seine exakte Hosted-Analyse bestand das Quality Gate und hatte
null neue Duplikation, meldete aber `AZ-o2G_i1eeMvlV2C-0t`. Dieser Kandidat
ergänzt nur die private Dateinamen-Konstante und ihre fokussierte Assertion.
Die bereitgestellte fokussierte Test-Evidence und `git diff --check` bestehen
vor diesem normalen Follow-up-Push; das direkte repository-weite Bilingual-
Target war durch fehlende Framework-Ziele blockiert, aber das Exact-Candidate-
Overlay bestand Bilingual-, Repository-Pfad- und Framework-Dokumentlink-
Prüfung. Die fokussierte Security-Review fand keinen validierten Befund und
hielt zugleich die Evidence-Reclassification-Grenze fest. Es werden weder
Merge, Master-Update, Report-Generation noch finales Hosted-Analyse-Ergebnis
behauptet.
