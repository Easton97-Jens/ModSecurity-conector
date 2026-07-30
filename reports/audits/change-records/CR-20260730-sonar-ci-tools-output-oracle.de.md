# Change Record: Parent-CI-Tools-Output-Containment und Native-Oracle-Zerlegung für SonarQube Cloud

**Sprache:** [English](CR-20260730-sonar-ci-tools-output-oracle.md) | Deutsch

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | CR-20260730-sonar-ci-tools-output-oracle |
| Datum (UTC) | 2026-07-30 |
| Initiale Quell-Revision | 77947c2ebe9523a24054b90bc1339657bed07ddb |
| Tracking | Aktuelle Master-SonarQube-Cloud-Issues `AZ8d8_sBE36x1qGA4xhY` (`pythonsecurity:S8707`) in `ci/tools/generate-block-status-config.py`, `AZ7b3dgOcO69wzd-_jHt` (`c:S107`) und `AZ7b3dgOcO69wzd-_jHu` (`c:S3776`) in `ci/tools/native_modsecurity_oracle.c`. |
| Grenze | Parent-`ci/tools`, ein Parent-Smoke-Checker, ein Parent-Source-Contract-Test und dieses englisch/deutsche Change-Record-Paar. Framework/MRTS-Quelle, Gitlinks, Workflows, Scanner-Konfiguration, Suppressions, Exclusions, Quality Gates und `master` bleiben unverändert. |

## Motivation und Problemstellung

Der aktuelle Master-Generator akzeptierte ein vom Aufrufer gewähltes
`--out-dir` und nutzte es ohne Containment für Verzeichniserzeugung und
Generated-File-Writes. Eine task-eigene Baseline-Kontrolle bestätigte sowohl
einen ausbrechenden Parent-Traversal als auch einen bestehenden Symlink des
finalen Generated-Headers, die eine externe Datei erzeugen oder überschreiben
konnten. Dies ist eine reale Filesystem-Integrity-Grenze hinter
`pythonsecurity:S8707` und kein kosmetisches Scanner-Signal.

Das native libmodsecurity-Oracle hatte außerdem einen `write_result`-Helper
mit acht Argumenten und eine `main`-Funktion oberhalb der konfigurierten
Cognitive-Complexity-Grenze. Die notwendige Wartung musste Phase-Order,
JSON-Schema, Exit-States, nullsichere Serialisierung und Resource-Ownership
bewahren. Während des Refactorings änderte sich zusätzlich der Source-Level
Body-Append-Fehlerpfad von zwei Frees desselben non-null Buffers zu einem
One-Owner-Cleanup; ein tatsächlicher libmodsecurity-Append-Fehler-Return wurde
nicht reproduziert, deshalb stellt dieser Record diesen bedingten Pfad nicht
als separat runtime-validierte Vulnerability dar.

## Akzeptanzkriterien

- `--out-dir` akzeptiert nur einen relativen Pfad unterhalb des bewusst
  gewählten Current-Working-Directory; absolute Pfade und jede `..`-Komponente
  schlagen fehl.
- Bestehende Intermediate-Symlink-Escapes schlagen fehl, bevor ein Verzeichnis
  oder Generated-File außerhalb der Output-Root erzeugt wird.
- Ein bestehender Final-Generated-File-Symlink wird als Directory-Entry ersetzt
  statt verfolgt; das externe Target bleibt abwesend.
- Ein gültiges verschachteltes Output-Verzeichnis bleibt zulässig und die
  Generated-Bytes bleiben für einen repräsentativen HAProxy-Statussatz gleich.
- `write_result` überschreitet die Parameter-Count-Grenze nicht mehr und die
  Request-Phase-Processing liegt nicht mehr in `main`, ohne CLI-Order,
  JSON-Felder/-Order, Status-Classification, Exit-Codes oder Native-Phase-Order
  zu ändern.
- Es erfolgt keine Änderung an SonarQube-Cloud-Regel, Quality Gate, Exclusion,
  Suppression, `NOSONAR`, Framework/MRTS-Quelle, Gitlink, Workflow oder Master.

## Implementierungsentscheidung und Begründung

`resolve_output_dir` weist absolute und Parent-Traversal-Inputs ab, löst den
Kandidaten unter einem strikt aufgelösten Current-Working-Directory auf und
bestätigt kanonisches Containment. `open_output_dir` erzeugt und öffnet jede
Directory-Komponente mit `O_DIRECTORY`, `O_NOFOLLOW` und einem
Directory-Descriptor. Der Generator schreibt jeden festen Dateinamen in eine
exklusive Temporary-File unter diesem geöffneten Directory und verwendet für
den Final-Namen descriptor-anchored `os.replace`. Plattformen ohne die
erforderlichen Descriptor-Primitiven schlagen mit einem normalen CLI-
Validation-Fehler fail-closed fehl.

Das Oracle gruppiert Request-Argumente und Result-Felder in private Contexts,
zieht die ursprüngliche lineare Phase-Sequence nach `process_request` heraus
und zentralisiert Cleanup in `cleanup_oracle`. `json_string` bleibt der einzige
nullsichere Serializer für `whoami`; alle Error-/Success-Result-Felder und ihre
serialisierte Order bleiben unverändert. Der Buffer wird nach erfolgreichem
Append sofort oder auf einem Error-Path einmal durch den Common-Cleanup-Owner
freigegeben.

## Betrachtete Alternativen

Eine rein lexikalische Relative-Path-Prüfung wurde verworfen, weil sie nicht
verhindern kann, dass ein bestehender Symlink der finalen Generated-Datei
verfolgt wird. Auch kanonisches Path-Containment ohne Descriptor-anchored
Erzeugung wurde verworfen, weil ein Directory-Entry nach der Kanonisierung und
vor einem pfadbasierten Write ersetzt werden kann. Das gewählte Design
kombiniert Input-Rejection, kanonisches Containment, No-Follow-
Directory-Descriptor-Traversal und Atomic-Final-Replacement; bei fehlenden
Primitiven schlägt es fail-closed fehl.

## Geänderte Dateien

- ci/tools/generate-block-status-config.py
- ci/checks/common/check-block-status-generator.py
- ci/tools/native_modsecurity_oracle.c
- tests/test_sonar_reliability_contract.py
- reports/audits/change-records/CR-20260730-sonar-ci-tools-output-oracle.md
- reports/audits/change-records/CR-20260730-sonar-ci-tools-output-oracle.de.md
- reports/audits/change-records/README.md
- reports/audits/change-records/README.de.md

## Ausgeführte Befehle

```sh
rtk proxy -- make check-block-status-generator
rtk proxy -- env PYTHONNOUSERSITE=1 PIP_REQUIRE_VIRTUALENV=true PIP_DISABLE_PIP_VERSION_CHECK=1 <venv-python> -B -P tests/test_sonar_reliability_contract.py
rtk proxy -- cc -std=c17 -Wall -Wextra -Werror -I /usr/include ci/tools/native_modsecurity_oracle.c -L /usr/lib/x86_64-linux-gnu -lmodsecurity -o <task-owned-output>
rtk proxy -- clang -std=c17 -Wall -Wextra -Werror -I /usr/include ci/tools/native_modsecurity_oracle.c -L /usr/lib/x86_64-linux-gnu -lmodsecurity -o <task-owned-output>
rtk proxy -- <task-owned-native-oracle> <allow-or-block-fixture-arguments>
rtk proxy -- diff -r --brief <base-generated-output> <candidate-generated-output>
```

## Tests und tatsächliche Ergebnisse

| Kommando oder Check | Ergebnis |
| --- | --- |
| `make check-block-status-generator` | bestanden: bestehende Success-, Invalid-Input-, Full-Status- und Deterministic-Controls plus legitime Nested-Output-, Traversal-, Absolute-Path-, Intermediate-Symlink- und Final-File-Symlink-Controls. |
| Final-Generated-File-Symlink-Control | bestanden: der feste Generated-Header ersetzte den Link und erzeugte das task-eigene externe Target nicht. |
| Generator-Kompatibilitätsvergleich | bestanden: Header-, C-Source- und HAProxy-Konfigurations-Bytes entsprachen der Base-Output für Status `501,403`. |
| `tests/test_sonar_reliability_contract.py` | bestanden: 12 Tests einschließlich der nullsicheren JSON- und extrahierten-Phase-Source-Contracts. |
| Python-Syntaxkompilierung | bestanden für den geänderten Generator, Checker und Source-Contract-Test. |
| Native-Oracle-C17-Kompilierung | bestanden unter GCC und Clang mit `-Wall -Wextra -Werror` gegen libmodsecurity 3.0.14. |
| Native-Oracle-Allow-Control | bestanden: erwarteter und tatsächlicher Status `200`, keine Intervention. |
| Native-Oracle-Block-Control | bestanden: erwarteter und tatsächlicher Status `403`, Native-Intervention bei `request_headers`. |
| Native-Oracle-Setup-Error-Control | bestanden: eine fehlende Headers-Datei lieferte Exit `2` und JSON `setup_error` mit dem bestehenden Reason. |
| Fokussierter Security-Diff-Scan | bestanden: jede geänderte source-like Datei wurde vollständig geprüft; kein diff-eingeführter reportbarer Befund überlebte. |

## Security-Auswirkung

Der Baseline-S8707-Source-to-Sink-Pfad ist in task-eigenem Temporary-Storage
direkt demonstriert: ein relativer Traversal und ein Final-Generated-File-
Symlink konnten einen festen Generated-Header außerhalb der gewählten
Output-Root leiten. Der Kandidat fügt vor den Write-Sinks lexikalische,
kanonische und descriptor-anchored Controls hinzu und ersetzt anschließend den
finalen Directory-Entry atomar, statt durch ihn zu schreiben.

Die resultierende Garantie setzt voraus, dass der Aufrufer eine vertrauenswürdige
exklusive Current-Working-Directory-Root wählt. Eine Partei mit Autorität, die
Ancestry dieser Root umzubenennen oder das geöffnete Output-Directory
gleichzeitig zu verändern, liegt außerhalb dieser CLI-Grenze; die
Implementierung behauptet keine globale hostile-shared-directory-Garantie. Der
lokale Security-Review fand unter dieser expliziten Annahme keinen
diff-eingeführten Kandidaten. Kein SonarQube-Cloud-Issue wird vor einer
beobachteten Hosted-Analyse am exakten Delivery-Head geschlossen.

## Dokumentationsstatus

Dieses vollständige englisch/deutsche Change-Record-Paar hält das aktuelle Live-
Issue-Inventar, die Output-Containment-Entscheidung, Native-Oracle-Invarianten,
lokale Runtime-Evidence und bekannte Einschränkungen fest. Beide Change-Record-
Indizes werden aktualisiert. Kein Generated-Source-Artefakt oder unverbundenes
Reader-Facing-Dokument wird geändert.

## Runtime-Evidence

Die Generator-Controls laufen über seine tatsächliche Python-CLI in einem
task-eigenen Temporary-Directory. Die Oracle-Controls verwenden die kompilierte
finale Source mit der installierten libmodsecurity-3.0.14-Library: eine normale
Allow-Request, eine Phase-1-Blocking-Request und den extrahierten
Missing-Headers-Error-Path. Dies sind lokale Controls und kein Connector-Matrix-
oder Production-Deployment-Ergebnis.

## Kompatibilität und generierte Artefakte

Für den repräsentativen Input `501,403` sind die Bytes des generierten Headers,
der C-Source und der HAProxy-Konfiguration mit dem Basisgenerator kompatibel.
Der Output-File-Replacement-Mechanismus ändert absichtlich die Filesystem-
Metadata-Semantik: Replacement erzeugt eine neue Datei gemäß Process-Umask und
trennt einen bestehenden Hardlink, statt dessen Referent zu truncaten. Diese
Änderung commitet kein generiertes Artefakt.

## Bekannte Einschränkungen

Der Generator ändert absichtlich die Metadata-Semantik der Output-File-
Replacement: Atomic Replacement nutzt eine neue Datei gemäß Process-Umask und
trennt einen bestehenden Hardlink, statt dessen Referent zu truncaten. Im
Repository wurde außer dem fokussierten Smoke-Checker kein direkter Production-
Caller gefunden. Der Native-Append-Failure-Branch ließ sich mit dem verfügbaren
Rule-/Body-Control nicht erzwingen, daher ist die Common-Cleanup-Korrektur
source-evidenced, wird aber nicht als reproduziertes Memory-Safety-Event
behauptet.

## Verbleibende Risiken

Die Output-Root muss exklusiv bleiben, während ein Aufrufer den Generator
ausführt. Ein privilegierter Concurrent-Writer mit Autorität über seine
Ancestry oder das geöffnete Directory könnte spätere Namespace-Observations
beeinflussen, obwohl der Generator keinen bestehenden Intermediate- oder Final-
Symlink verfolgt. Der breitere Sonar-Backlog und alle anderen Komponenten liegen
außerhalb dieser fokussierten `ci/tools`-Aufgabe.

## Nicht ausgeführte Prüfungen mit Begründung

- Vollständige Connector-Builds, vollständige Runtime-Matrizen, Framework/MRTS-
  Tests und Report-Generierung liegen außerhalb der engen Parent-`ci/tools`-
  Remediation.
- ASan/Valgrind wurde nicht ausgeführt, weil der exakte
  `msc_append_request_body`-Error-Path mit der verfügbaren begrenzten
  libmodsecurity-Fixture nicht reproduzierbar war; dies ist als
  Verifikationslimit statt als Evidenz eines abgeschlossenen Memory-Safety-
  Proofs festgehalten.
- Gehostete GitHub-Checks und eine Exact-Head-SonarQube-Cloud-Analyse benötigen
  einen Delivery-Branch und Draft PR. Dieser Record gibt weder externes Issue-
  Closure noch Master-Merge-Autorisierung.

## Finaler Diff- und Review-Status

Der lokale Kandidat enthält die begrenzte S8707-Output-Containment-Reparatur,
die zwei Sonar-Maintainability-Refactorings, direkte Regression-Controls und
erforderliche bilinguale Traceability. Der vollständige fokussierte Security-
Diff-Scan hat null reportbare diff-eingeführte Befunde. Zum Zeitpunkt der
Record-Erstellung gibt es keinen Task-Commit, Push, Draft PR, gehosteten Check,
Exact-Head-SonarQube-Cloud-Result oder Master-Integration-Claim; diese Fakten
dürfen erst nach Beobachtung ergänzt werden.
