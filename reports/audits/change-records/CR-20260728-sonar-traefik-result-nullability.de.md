# Change Record: Traefik-Resultat-Optionaltext-Nullability-Remediation für SonarQube Cloud

**Sprache:** [English](CR-20260728-sonar-traefik-result-nullability.md) | Deutsch

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | CR-20260728-sonar-traefik-result-nullability |
| Datum (UTC) | 2026-07-28 |
| Basis-Revision | 8e8acb8dab1cd03723de269cab7da7dd62e5e010 |
| Grenze | Ausschließlich Parent-Traefik-C-Engine-Resultatserialisierung und ihr fokussierter Source-Contract-Test sowie dieses englisch/deutsche Change-Record-Paar und die Indizes. Framework, MRTS, beide Gitlinks, Workflows, Scanner-Policy und generierte Reports bleiben unverändert. |
| Finding-Verknüpfung | Zielt auf die Live-SonarQube-Cloud-`c:S2637`-Issue-Keys `AZ9cRyv8HhV2CayPTP10`, `AZ9cRyv8HhV2CayPTP11` und `AZ9cRyv8HhV2CayPTP12`. Die Issues bleiben extern offen, bis eine Exact-Head-Analyse den Kandidaten beobachtet. |

## Motivation und Problemstellung

`traefik_engine_send_result` serialisiert optionalen Transaktions-, Regel- und
Redirect-Text in einen Resultatframe für den privaten Local-Engine-Unix-Socket.
Die vorherige Implementierung schützte jedes `memcpy` mit einem Nulltest und
einem Längentest. Der Runtime-Accessor und die Decision-Felder dürfen
legitimerweise null sein, der Analyzer konnte jedoch am Copy-Site nicht
beweisen, dass der Pointer nicht null ist.

Die notwendige Behebung muss den Wire-Vertrag erhalten: ein fehlender
Optionalwert ist ein leeres Feld mit Länge null und vorhandene Werte behalten
ihre exakten Bytes sowie Feldreihenfolge. Sie darf weder eine Unterdrückung
hinzufügen noch das Protokoll ändern oder die bestehenden Größenlimits
abschwächen.

## Akzeptanzkriterien

- Die drei optionalen Source-Pointer des Resultatserializers haben einen
  nichtnullen unveränderlichen Empty-Text-Default.
- Nullable Runtime- und Decision-Eingaben ersetzen den Default nur nach einem
  expliziten Nulltest.
- Leere Optionalwerte erzeugen weiterhin Felder der Länge null; nichtleere
  Werte erhalten die bisherige Reihenfolge, Längen, Action, Phase, Status und
  Flags.
- Ein direkter C17-Socketpair-Harness kompiliert die tatsächliche Translation
  Unit und prüft sowohl den vollständig leeren als auch den gefüllten
  Resultatframe bytegenau.
- Fokussierter Source-Contract, Whitespace-Prüfung und fokussierte
  Security-Diff-Review bestehen ohne Unterdrückung oder Scanner-/CI-
  Policyänderung.
- Vor beobachteter Ausführung werden keine gehostete Issue-Closure,
  PR-Status, Merge, Master-Update, Framework-/MRTS-Änderung oder vollständige
  Host-Runtime-Ergebnisse behauptet.

## Implementierungsentscheidung und Begründung

`traefik_engine_empty_text` ist ein privater unveränderlicher leerer C-String.
Die drei Serializer-Pointer beginnen mit diesem Wert. Die Funktion übernimmt
den nullable Runtime-Transaction-ID und die nullable Decision-Felder in lokale
Variablen und verwendet jeden nur, wenn er nicht null ist. Dadurch erhalten
der Bounded-String-Helper und die späteren `memcpy`-Aufrufe stets nichtnullige
Eingaben, während die bereits größenbegrenzte Serialisierung erhalten bleibt.

Kein Control Flow wird über die Decision-/Session-Grenze verschoben. Decision
Kind, Phase, HTTP-Status-Clamp, Disruptive- und Late-Intervention-Flags,
Frame-Header, Feldreihenfolge und maximale Feldgrenzen bleiben an ihrer
bisherigen Stelle. Ein fehlender Wert hat wie vorher Größe null und schreibt
keine Payload-Bytes.

## Geänderte Dateien

- `connectors/traefik/src/traefik_engine_service.c`
- `tests/test_sonar_reliability_contract.py`
- `reports/audits/change-records/README.md` und `README.de.md`
- dieses englische/deutsche Change-Record-Paar

## Ausgeführte Befehle

| Befehl oder Kontrolle | Ergebnis |
| --- | --- |
| `PYTHONDONTWRITEBYTECODE=1 PYTHONNOUSERSITE=1 .venv/bin/python -B tests/test_sonar_reliability_contract.py` | bestanden: 11 Tests einschließlich des C17-Compile-and-Run-Resultatframe-Harness. |
| `.venv/bin/python -m unittest -v tests.test_c_cpp_diagnostics` | bestanden: 7 C/C++-Diagnostics-Contract-Tests. |
| `TMPDIR=<task-eigene externe Wurzel> make check-remaining-connectors-c17` | bestanden: jede Remaining-Connector-C-Translation-Unit einschließlich des geänderten Traefik-Engine-Service kompiliert unter C17 mit `-Wall -Wextra -Werror`. |
| `.venv/bin/python -m unittest -v tests.test_bilingual_docs tests.test_traefik_native_local_plugin tests.test_traefik_runtime_smoke_security` | bestanden: 39 fokussierte Dokumentations- und Traefik-Runtime-/Security-Contract-Tests. |
| `git diff --check` | bestanden; keine Whitespace-Fehler. |
| Repository-Bilingual-Dokumentationschecker gegen ein task-eigenes externes Kandidaten-Overlay mit der Parent-gebundenen Framework-Revision `47e50e7bc43ba7a3b5bad1a9448111794f664cc0` | bestanden: Sprachpaare, Change-Record-Struktur, Links und Framework-Referenzen lösen ohne Checkout-Änderung auf. |
| Fokussierter `codex-security:security-diff-scan` des exakten lokalen Patches | bestanden; kein berichtspflichtiger Vulnerability-Kandidat. Der versiegelte Scanreport ist an Patch-SHA-256 `f221a59b23fe79abd46f3f0ec9a3364030492960d0381c8552c8bd4c415a2df7` gebunden. |
| Normaler Task-Branch-Push und Draft-PR-Erstellung | abgeschlossen: [Parent-PR #150](https://github.com/Easton97-Jens/ModSecurity-conector/pull/150) ist gegen `master` offen; seine Exact-Head-Hosted-Checks stehen aus. |

## Security-Auswirkung

Die geänderte Funktion ist eine sicherheitsrelevante private Unix-Socket-
Serialisierungsgrenze. Die Behebung entfernt nullable Pointerwerte an den
Copy-Sites, ohne zu erweitern, was serialisiert werden kann. Bestehende
Feldgrößengrenzen, uint16-Clamping, Resultatframe-Erzeugung, Sessionprüfungen
und Decision-Metadatenbehandlung bleiben erhalten. Die fokussierte Review fand
keinen neuen Untrusted-Source-to-Sink-Pfad, keinen Längenbypass, keine
Lifetime-Regression und keine Transportänderung.

## Runtime-Evidence

Der direkte Test inkludiert die reale C-Translation-Unit, linkt nur den eng
benötigten Transaction-ID-Accessor-Stub und führt
`traefik_engine_send_result` über ein Unix-Socketpair aus. Er beweist die
Null-Längen-Kodierung fehlenden Optionaltexts und die bytegenaue Kodierung
gefüllter Felder. Es ist Source-Level-Protokoll-Evidence, kein vollständiger
Traefik/Common/libmodsecurity-Host-Runtime-Test.

## Bekannte Einschränkungen

In der isolierten Umgebung gibt es keine verifizierten libmodsecurity-Header
oder -Library: `pkg-config libmodsecurity` ist nicht verfügbar und in den
zugelassenen lokalen Orten wurde kein kompatibles Include-/Library-Paar
gefunden. Eine vollständige Host-/Plugin-Ausführung ist daher nicht als
bestandenes lokales Ergebnis vertreten.

## Verbleibende Risiken

Ein externer Traefik-Host, geladenes Plugin und eine Live-
Common/libmodsecurity-Transaktion können Verhalten hinzufügen, das der lokale
Source-Level-Harness nicht ausführt. Auch die exakte SonarQube-Cloud-
Rule-Disposition bleibt extern, bis eine frische Analyse des Kandidatenheads
abgeschlossen ist.

## Nicht ausgeführte Prüfungen mit Begründung

- Das vollständige `connectors/traefik`-Native-Host-Runtime-Target lief nicht,
  weil seine erforderliche verifizierte libmodsecurity-Development-Abhängigkeit
  fehlt; es wird keine Ersatz-Full-Runtime behauptet.
- Exact-PR-Head-CI, SonarQube-Cloud-Analyse, Review und Merge stehen für
  Draft-PR #150 aus. Der Draft-Status behauptet absichtlich weder ein
  Quality-Ergebnis noch Merge-Berechtigung.

## Finaler Diff- und Review-Status

Die Implementierung wurde auf ihrem Task-Branch committet und normal gepusht,
und [Draft-Parent-PR #150](https://github.com/Easton97-Jens/ModSecurity-conector/pull/150)
ist gegen `master` offen. Sein fokussierter Source-Contract und die
Security-Diff-Review bestehen. GitHub Actions, SonarQube Cloud, Review und
jede Master-Aktion sind für den aktuellen PR-Head noch unbeobachtet. Die drei
zielgerichteten externen Issues werden nicht als geschlossen behauptet, bis
frische Exact-Head-SonarQube-Cloud-Evidence dies bestätigt.
