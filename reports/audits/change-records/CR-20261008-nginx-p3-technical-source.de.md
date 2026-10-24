# Change Record: CR-20261008-nginx-p3-technical-source

**Sprache:** [English](CR-20261008-nginx-p3-technical-source.md) | Deutsch

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | CR-20261008-nginx-p3-technical-source |
| Datum (UTC) | 2026-10-08 |
| Basis-Revision | `ec632b50d439385859113f9667fcbddb29cde357` |

## Motivation und Problemstellung

P3-Fehler bei Native-Return und monotoner Uhr versiegelten Common-Fehler, erzeugten aber kein zugehöriges technisches JSONL-Event. Tests einzelner Helper führten den vollständigen Header-Filter-Caller nicht aus.

## Akzeptanzkriterien

Native-Return 0/negative/undokumentierte Werte und beide Uhrfehler müssen im tatsächlichen vollständigen header_filter geschlossen scheitern: keine P3-Completion, kein Downstream, genau ein technisches Event und idempotenter Wiederaufruf. Gültiger Return 1 über Budget erzeugt genau Mess- und Timeout-Event. Deaktiviertes Budget und exakte Grenze schließen P3 ab und leiten einmal weiter.

## Implementierungsentscheidung und Begründung

Die neue C17-Fixture extrahiert den tatsächlichen vollständigen header_filter, Erfolgsdispatch und Event-Writer, Modul-Budget-Helper, technischen Emitter, Common-begin/complete-Wrapper und Inline-JSONL-Writer/Disposition. Reale Common-Zustandslogik, Profilregistry und Serializer werden gelinkt; der tatsächliche URI-Helper wird eingebunden. Leichtgewichtige NGX-Header-/Mapper-Hostplumbing, Poolhooks, Native-Return/Intervention ohne Pending-Decision, Downstream/Finalize, monotone Uhr und FD-Erfassung sind kontrollierte Seams. Die Fixture liefert keine Common-Ergebnisse, Budgetentscheidungen oder Events aus Erwartungen.

Ein realer Common-Vertrag schließt request_headers und request_body vor P3 ab. Tatsächlicher Zustand, Native-/Hostzähler und serialisiertes JSON werden geprüft. Fehlerwiederaufrufe führen dieselbe volle Funktion aus und erkennen doppelte Effekte. ROOT bleibt standardmäßig der Testcheckout; der Integrationstest überschreibt nur das importierte Python-Modulattribut mit dem aktuellen Root-Checkout, ohne Quellkopien oder produktive Umgebungsfeatures.

## Geänderte Dateien

Nur die neue tests/test_nginx_p3_technical_source.py und dieses EN/DE-Paar. Root verantwortet Caller-/Mapper-Quelländerungen; bestehende Quellen/Tests und der Integrationsworktree wurden nicht geändert.

## Ausgeführte Befehle

RTK-gekapselter Framework-Python-Loader mit externem RUNNER_TEMP/PYTHONPYCACHEPREFIX kompiliert kontrolliertes C17 -Wall -Wextra -Werror und linkt reale Common-Quellen. Nach Korrekturen der Fixture-Deklarationen, Phasennamen und Identität scheiterte der beabsichtigte RED an fünf fehlenden Events; Erfolg bei deaktiviertem/exaktem Budget und gemessener Timeout bestanden bereits. Nach Roots Caller-Korrektur bestanden alle fünf Testmethoden, einschließlich Native 0/-1/2 und beider Erfolgskontrollen. Logs stream-c-p3-technical-red.log und stream-c-p3-technical-green.log liegen im externen Run-Analyseverzeichnis.

## Security-Auswirkung

Keine erfundene Rule-ID; explizite technische Taxonomie. Native-Fehler werden weder durch Timing verdeckt noch als erlaubte Antwort behandelt. Kein Native-/Uhr-/Budgetfehler schließt Common P3 ab, leitet Header weiter oder wiederholt Native-/Eventarbeit.

## Runtime-Evidence

Kontrollierte quellgebundene Ausführung, keine native NGINX-/Engine-Runtime, HTTP-Auslieferungs- oder PASS-Evidenz.

## Bekannte Einschränkungen

Der isolierte eigene Checkout enthält Roots Budget-/Technik-/URI-Helper noch nicht. Der Test verwendete die tatsächliche aktuelle Root-Quelle über das Loader-Modulattribut; nach Integration gilt ROOT standardmäßig. Headerinhaltsmapping und Pending-Intervention-Klassifikation liegen außerhalb dieser Fixture.

Change-Record-Struktur und neues EN/DE-Paar bestehen. Die vollständige zweisprachige Dokumentationsprüfung bleibt wegen bereits fehlender Framework-Submodul-Linkziele im isolierten Worktree blockiert; der neue Record hat keine verbleibende Verletzung. Diff-Whitespace-Prüfungen bestehen.

## Verbleibende Risiken

Vollständige native Quellkompilierung, Runtime-Eventsink und tatsächliche HTTP-Auslieferung bleiben Integrationsprüfungen von Root. Reales JSONL wird über einen kontrollierten FD erfasst, nicht über einen NGINX-Prozess oder Dateisystemlauf.

## Nicht ausgeführte Prüfungen mit Begründung

Kein nativer Connector-Build, E2E oder Runtime-Slot. Native Runtime und frische CI/Sonar bleiben Root-owned.

## Finaler Diff- und Review-Status

Fokussierter Parent-Slice aus drei neuen Dateien; keine Root-/Quellmutation, fremden Änderungen, Gitlink-/MRTS-Änderungen oder Veröffentlichung.
