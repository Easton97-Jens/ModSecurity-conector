# Change Record: Parent-HAProxy-Append-String-Preflight für SonarQube Cloud c:S3519

**Sprache:** [English](CR-20260727-sonar-haproxy-append-string-s3519.md) | Deutsch

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | CR-20260727-sonar-haproxy-append-string-s3519 |
| Datum (UTC) | 2026-07-27 |
| Basis-Revision | 1b0f8825f3510b99b603bb6cd6f0777e1710358e |
| Tracking | Parent-SonarQube-Cloud-BLOCKER `c:S3519`, Receipt `AZ-URJYx1ap3oKwyiaQ7`, in `connectors/haproxy/src/haproxy_spop_diagnostic_runtime.c` in `append_string(...)`. |
| Grenze | Parent-HAProxy-Diagnose-Runtime-Quelltext, sein fokussierter Parent-Reliability-Contract-Test sowie dieses englisch/deutsche Change-Record-Paar mit seinen Indizes. Framework, MRTS, Gitlinks, Workflows, Scanner-Konfiguration, Quality Gates, Suppressions und der externe SonarQube-Cloud-Issue-Status bleiben unverändert. |
| Kandidatenstatus | Lokal und uncommittet. Es gab kein Staging, keinen Commit, Push, Pull Request oder Merge sowie keine Framework- oder MRTS-Änderung und kein Gitlink-Update. |

## Motivation und Problemstellung

Die frühere Implementierung von `append_string(...)` schrieb einen Header mit
variabler Länge und rief anschließend `append_bytes(buf, value, len, len)`
auf. Der Aufruf beschreibt die Quellgröße nur als die zu kopierende Länge;
dies ist das direkte Muster, das `c:S3519` meldet. Der Kandidat entfernt diesen
Aufruf aus dem String-Pfad und verändert die bestehende, separat begrenzte
Frame-Payload-Kopie nicht.

Bevor `append_string(...)` sein direktes Ziel verändert, validiert es nun den
Buffer-Zeiger und dessen Länge, einen NUL-terminierten C-String innerhalb von
`SPOP_FRAME_MAX`, berechnet die Größe des Headers variabler Länge und weist
nach, dass Header plus Payload in den verbleibenden Buffer passen. Danach
hängt es Header und String-Bytes direkt an. Die Preflight-Prüfung macht die
Zurückweisung durch direktes `append_string(...)` für NULL-, unterminierte und
Kapazitätsüberlauf-Eingaben atomar.

Die Grenzfälle sind bewusst exakt: Ein String mit 239 Bytes hat einen
Ein-Byte-Header mit `239` und erzeugt ein kodiertes Ergebnis mit 240 Bytes;
ein String mit 240 Bytes hat den Zwei-Byte-Header `240`, `0` und erzeugt ein
Ergebnis mit 242 Bytes. Ein exakter Fit bis zu `SPOP_FRAME_MAX` gelingt, eine
unzureichende kombinierte Header-und-Payload-Kapazität gibt dagegen `-1` zurück,
ohne den Buffer zu verändern.

`append_typed_string(...)` schreibt seinen bereits bestehenden Typmarker vor
dem Aufruf von `append_string(...)`; sein Markerverhalten und jeder
wrapperseitige partielle Zustand bleiben ausdrücklich außerhalb dieser
fokussierten Änderung.

## Akzeptanzkriterien

- `append_string(...)` enthält nicht mehr `append_bytes(buf, value, len, len)`.
- Direktes `append_string(...)` validiert C-String, Buffer und kombinierte
  Header-/Payload-Kapazität vor seiner ersten Mutation.
- Die Varint-Kodierungen für 239/240, erfolgreicher exakter Fit,
  Überlauf-Fehlschlag, Fehlschlag bei unterminierter Eingabe und NULL-Fehlschlag
  haben fokussierte Regressionstests.
- Der Record beansprucht weder Wrapper-Level-Atomizität für
  `append_typed_string(...)`, noch Live-HAProxy-Verhalten, ein gehostetes
  Quality Gate oder einen externen Issue-Abschluss.

## Implementierungsentscheidung und Begründung

`varint_encoded_length(...)` wird ergänzt, damit die Header-Länge mit
denselben Schwellwerten wie `append_varint(...)` berechnet wird: ein Byte unter
`240`, danach die bestehende Folge von Continuation-Bytes. `append_string(...)`
verwendet diese Länge ausschließlich für seinen Preflight. Nach erfolgreicher
Validierung serialisieren die bereits bestehenden Primitiven
`append_varint(...)` und `append_byte(...)` denselben Header und dieselbe
Payload, ohne `append_bytes(...)` eine künstliche Quellgröße `data_len == len`
zu übergeben.

Damit bleibt `append_bytes(...)` bewusst für den Frame-Payload-Aufruf erhalten,
bei dem die tatsächliche Quellkapazität `sizeof(payload->data)` ist, statt die
Remediation über den Sonar-Receipt hinaus auszudehnen.

## Geänderte Dateien

- `connectors/haproxy/src/haproxy_spop_diagnostic_runtime.c` — direkter
  `append_string(...)`-Preflight und begrenztes Anhängen von Bytes sowie
  `varint_encoded_length(...)`.
- `tests/test_sonar_reliability_contract.py` — Source-Contract-Assertions und
  die dauerhafte native C-Harness für die Grenzfallbehandlung durch direktes
  `append_string(...)`.
- `reports/audits/change-records/CR-20260727-sonar-haproxy-append-string-s3519.md`
  und `.de.md` — dieses bilinguale Change-Record-Paar.
- `reports/audits/change-records/README.md` und `README.de.md` — gepaarte
  Indexeinträge.

## Ausgeführte Befehle

| Ausgeführte Kontrolle oder dokumentierte Validierung | Beobachtetes Ergebnis |
| --- | --- |
| `rtk proxy env PYTHONDONTWRITEBYTECODE=1 PYTHONNOUSERSITE=1 /root/git/ModSecurity-conector/.venv/bin/python -B -m unittest -v tests.test_sonar_reliability_contract` | bestanden: 8 fokussierte Tests, einschließlich der dauerhaften nativen C-Harness, die direkte `append_string(...)`-Grenzfälle kompiliert und ausführt. |
| `rtk proxy make check-haproxy-common-adoption` | bestanden. |
| `rtk proxy make check-haproxy-c-standard-wiring` | bestanden. |
| `rtk proxy make check-haproxy-c17-lint` | bestanden. |
| `rtk proxy env BUILD_ROOT=<task-eigene externe Build-Wurzel> CC=gcc make check-haproxy-c17` | bestanden; die temporären GCC-Build-Ausgaben wurden nach der Validierung entfernt. |
| `rtk proxy env BUILD_ROOT=<task-eigene externe Build-Wurzel> CC=clang make check-haproxy-c17` | bestanden; die temporären Clang-Build-Ausgaben wurden nach der Validierung entfernt. |
| Unabhängiger Security-Review des fokussierten Source-/Test-Diffs | bestanden: kein neuer reportbarer Sicherheitsbefund; die direkte `append_string(...)`-Preflight-Invariante und das ausdrücklich ausgeschlossene `append_typed_string(...)`-Markerverhalten wurden geprüft. |
| `rtk proxy env PYTHONDONTWRITEBYTECODE=1 PYTHONNOUSERSITE=1 make check-bilingual-docs` | bestanden, nachdem der Parent-festgeschriebene Framework-Gitlink in diesem isolierten Kandidaten-Worktree nur lesend initialisiert wurde. |
| `rtk proxy env PYTHONDONTWRITEBYTECODE=1 PYTHONNOUSERSITE=1 make check-doc-links` | bestanden, nachdem der Parent-festgeschriebene Framework-Gitlink in diesem isolierten Kandidaten-Worktree nur lesend initialisiert wurde. |
| `rtk proxy git diff --check` | bestanden. |

## Security-Auswirkung

Der Sonar-BLOCKER betrifft eine native Buffer-Copy-Grenze. Die Korrektur erhält
eine fail-closed direkte API: NULL-Buffer- oder C-String-Eingaben, ein
unterminierter C-String, eine ungültige Buffer-Länge und unzureichende
kombinierte Header-und-Payload-Kapazität geben `-1` zurück, bevor
`append_string(...)` den Ziel-Buffer verändert. Die fokussierte native Harness
beweist die dokumentierten direkten Fälle einschließlich nicht mutierenden
Überlaufs. Sie verändert weder Authentifizierung, Autorisierung,
Konfigurations-Trust noch Connector-Prozessprivilegien.

Der Review beansprucht keine Fehleratomizität für `append_typed_string(...)`:
Der bestehende Marker dieses Wrappers bleibt bewusst außerhalb des Umfangs.

## Runtime-Evidence

Das fokussierte Testmodul enthält eine dauerhafte native C-Harness, die die
tatsächliche Diagnose-Runtime-Translation-Unit kompiliert und ausführt. Sie
prüft jede Varint-Länge bis `SPOP_FRAME_MAX`, die exakten 239/240-Kodierungen,
erfolgreichen exakten Fit, nicht mutierenden Überlauf, nicht mutierende
unterminierte Eingabe und einen NULL-direkten Buffer. Dies ist begrenzte native
Ausführungs-Evidence für `append_string(...)`; es ist kein Live-HAProxy-/SPOP-
Network-Runtime-Ergebnis.

## Bekannte Einschränkungen

- Der Receipt ist an die angegebene Basis-Revision gebunden. Eine frische
  Exact-Head-SonarQube-Cloud-Analyse ist erforderlich, bevor behauptet werden
  kann, dass `AZ-URJYx1ap3oKwyiaQ7` extern behoben ist.
- Für diesen Kandidaten lief keine Live-HAProxy-Runtime und keine vollständige
  Connector-Matrix.
- Das Markerverhalten von `append_typed_string(...)` ist vorbestehend und
  liegt außerhalb der Atomizitätsbehauptung für direktes `append_string(...)`.
- Die Dokumentations-Link-Validierung benötigte das im Parent festgeschriebene
  Framework; es wurde nur zum Ausführen der Parent-Dokumentationschecks nur
  lesend auf `47e50e7bc43ba7a3b5bad1a9448111794f664cc0` initialisiert. Es
  wurden keine Framework-/MRTS-Quellen, Branches oder Gitlinks geändert.

## Verbleibende Risiken

Der fokussierte Contract, die native Harness und die unabhängigen GCC-/Clang-
C17-Compiles reduzieren das Risiko einer Regression bei Header-Länge oder
Kapazitäts-Preflight, üben aber keinen Live-HAProxy-Prozess oder alle SPOP-
Message-Construction-Pfade aus. Gehostete CI und eine frische Exact-Head-
SonarQube-Cloud-Analyse können weiterhin nicht von dem lokalen Kandidaten
abgedeckte Probleme finden. Das externe Issue bleibt offen, bis eine solche
Analyse einen ausgelieferten Head beobachtet.

## Nicht ausgeführte Prüfungen mit Begründung

Es liefen keine Live-HAProxy-Runtime, keine vollständige Connector-Matrix,
keine gehostete GitHub-CI, keine gehostete SonarQube-Cloud-Analyse, keine
Delivery-Aktion, keine Framework-Quell-/Delivery-Aktion sowie keine MRTS-Aktion.
Der Kandidat ist lokal und diese Dokumentationsaufgabe ist auf den Parent-
Worktree begrenzt. Der Parent-festgeschriebene Framework-Gitlink wurde allein
zum Ausführen von `make check-bilingual-docs` und `make check-doc-links` nur
lesend auf `47e50e7bc43ba7a3b5bad1a9448111794f664cc0` initialisiert; beide
bestanden.

## Finaler Diff- und Review-Status

Zum Zeitpunkt der Record-Erstellung enthält der Worktree den lokalen,
uncommitteten HAProxy-Source-/Test-Kandidaten und dieses bilinguale
Dokumentationspaar mit seinen Indizes. Es wird keine Git- oder Delivery-Aktion
beansprucht. Die bestehende Evidence aus fokussiertem Source-/Test,
HAProxy-Adoption/Wiring/C17-Lint und unabhängigem Security-Review steht oben.
Der vollständige Bilingual-Docs- und Link-Check besteht nun nach der nur
lesenden Initialisierung des Parent-festgeschriebenen Frameworks; auch der
Whitespace-Diff-Check bestand. Eine frische Exact-Head-SonarQube-Cloud-Analyse
bleibt vor einer Behauptung externer Issue-Auflösung verpflichtend.
