# Change Record: Entfernen eines redundanten Native-Oracle-JSON-Fallbacks

**Sprache:** [English](CR-20260720-sonar-native-oracle-null-fallback.md) | Deutsch

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | CR-20260720-sonar-native-oracle-null-fallback |
| Datum (UTC) | 2026-07-20 |
| Basis-Revision | cbd8385ce1b34318c84cf8f4a5a92ef98c83f82a |
| Tracking | SonarQube-Cloud-Issue AZ7b3dgOcO69wzd-_jHv, c:S3519, native JSON-Result-Serialisierung |
| Grenze | Nur Parent ci/tools Native Oracle und sein fokussierter Parent-Source-Contract; keine Framework-, MRTS-, Gitlink-, Scanner- oder Quality-Gate-Änderung. |

## Motivation und Problemstellung

Die frische Parent-Master-Analyse 6cc3a8ba-3926-4240-b6ec-f2c1f99509ff meldet
AZ7b3dgOcO69wzd-_jHv als offenen Blocker c:S3519 in
ci/tools/native_modsecurity_oracle.c. Sein gespeicherter interprozeduraler
Flow ruft json_string über den redundanten Caller-Ausdruck whoami ? whoami : ""
auf.

Der vorhandene Callee besitzt bereits einen expliziten NULL-Zweig, der einen
leeren JSON-String schreibt und zurückkehrt, bevor ein Byte-Cursor
initialisiert wird. Ein künstlich erzeugtes leeres Literal im Caller dupliziert
daher dieses Verhalten und erlaubt dem Analyzer, einen unmöglichen
Ein-Byte-Literal-Loop-Pfad zu modellieren.

## Akzeptanzkriterien

- Ein NULL-whoami-Wert wird wie bisher als derselbe leere JSON-String serialisiert.
- Ein nicht-NULL-whoami-Wert durchläuft weiterhin den vorhandenen JSON-Escape-Pfad.
- Der Caller enthält keinen redundanten whoami ? whoami : "" Fallback.
- Der fokussierte Source-Contract deckt den direkten nullable Aufruf und den
  NULL-Guard des Callees ab.
- Es werden keine Sonar-Suppression, Issue-Dismissal, Scanner-Exclusion,
  Quality-Gate-Änderung, Framework-/MRTS-Änderung oder Gitlink-Änderung verwendet.

## Implementierungsentscheidung und Begründung

write_result übergibt whoami nun direkt an json_string. json_string bleibt der
einzige Owner des nullable-String-Contracts: Bei NULL schreibt die Funktion ""
und kehrt zurück, andernfalls initialisiert sie den Unsigned-Byte-Cursor und
bewahrt den vorhandenen Escape-Switch.

Dies ist die kleinste verhaltenserhaltende Korrektur für den exakt
gespeicherten Sonar-Flow. Sie entfernt die einzige verbleibende
Caller-Level-Empty-String-Literalquelle für json_string, statt eine echte
Source-Änderung als False Positive zu klassifizieren.

## Geänderte Dateien

- ci/tools/native_modsecurity_oracle.c
- tests/test_sonar_reliability_contract.py
- dieses englische/deutsche Change-Record-Paar

## Ausgeführte Befehle

| Befehl | Ergebnis |
| --- | --- |
| Fokussierter Unittest für tests.test_sonar_reliability_contract | bestanden: 6 Tests |
| git diff --check vor dem Staging | bestanden |
| Git-Staged-Diff-Check für die zwei Source-/Test-Dateien | bestanden |
| Direkter Sonar-Issue-Flow-Readback für AZ7b3dgOcO69wzd-_jHv | bestätigte den Caller-Level-Empty-Literal-Datenfluss |

## Security-Auswirkung

Das betroffene Programm ist ein kurzlebiges connector-freies CI-/Native-Oracle,
keine Connector-Request-Senke. Das Issue ist ein Reliability-/Static-Analysis-
Resultat, kein belegter Remote-Memory-Safety-Exploit. Die Korrektur bewahrt die
sichere NULL-Serialisierung und entfernt einen irreführenden
interprozeduralen Literalpfad, ohne eine Kontrolle abzuschwächen.

## Runtime-Evidence

Der fokussierte Source-Contract belegt die beabsichtigte NULL-/Nicht-NULL-
Grenze auf Source-Level. Eine vollständige Native-Oracle-Runtime wurde in
diesem Worktree nicht ausgeführt. Die Parent-Source-Änderung bleibt
absichtlich auf die vorhandene JSON-Result-Serialisierungsgrenze begrenzt.

## Bekannte Einschränkungen

Eine frische SonarQube-Cloud-Analyse des exakten PR-Heads ist erforderlich,
bevor behauptet wird, dass das Issue fixed oder resolved ist. Das Parent-Master-
Quality-Gate hat außerdem unabhängige Vulnerabilities und drei unreviewte
Security Hotspots; dieser kleine Record beansprucht nicht, sie zu lösen.

## Verbleibende Risiken

Bis Exact-Head- und Resulting-Master-Sonar-Evidence beobachtet wurde, bleibt
der c:S3519-Alert offen. Der unabhängige aktuelle Master-Backlog enthält 220
offene Vulnerabilities und drei TO_REVIEW-python:S5332-Hotspots. Es wird kein
Risiko akzeptiert und kein externes Issue durch diesen lokalen Commit
geschlossen.

## Nicht ausgeführte Prüfungen mit Begründung

- Native C17-Kompilierung und ein tatsächlicher Native-Oracle-Lauf sind
  blockiert, weil gcc und clang vorhanden sind, aber libmodsecurity-Header,
  pkg-config-Metadaten und eine linkbare Runtime fehlen.
- Vollständige Connector-/Runtime-Matrizen liegen außerhalb dieses Zwei-Datei-
  Parent-Scopes und benötigen die fehlenden nativen Voraussetzungen.
- PR-, CodeQL-, OSV-, Secret-Scanning-, Scorecard- und SonarQube-Cloud-Checks
  sind noch nicht für diesen exakten Source-Commit gelaufen.

## Finaler Diff- und Review-Status

Die Source-/Test-Korrektur ist Commit
9415510c135a021c9c119d73f68fde4d621c49b1 auf dem isolierten Parent-Branch
codex/sonar-json-string-null-guard-20260720. Sie ist noch nicht gepusht, in
keinem Pull Request, nicht gemergt und nicht als gefixter externer Alert
dargestellt. Der nächste Delivery-Gate ist ein normaler Push, Draft-PR,
Exact-Head-Checks, Review-/Thread-Readback und ein geschützter Merge nur bei
bestehenden Gates.
