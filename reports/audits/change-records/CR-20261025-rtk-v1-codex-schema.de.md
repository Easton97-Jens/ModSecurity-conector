# Change Record: CR-20261025-rtk-v1-codex-schema

**Sprache:** [English](CR-20261025-rtk-v1-codex-schema.md) | Deutsch

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | CR-20261025-rtk-v1-codex-schema |
| Datum (UTC) | 2026-10-25 |
| Basis-Revision | `42fd5a8e895aca3a36b09eb09fe5c7cf9c3399e3` |

## Motivation und Problemstellung

Der Parent schrieb die Ausführung über RTK in seiner lokalen Policy vor, hatte aber keine versionierte native Codex-Hook-Registrierung. Diese Änderung übernimmt das von RTK v1.0.1 unterstützte Codex-Hook-Schema und dokumentiert die v1-Befehlsnamen. Bestehende `rtk make`-Befehle bleiben gültig; historische `rtk proxy`-Nachweise bleiben entsprechend ihrer tatsächlichen Ausführung erhalten.

## Akzeptanzkriterien

- Die projektlokale Hook-Konfiguration entspricht `rtk init --codex` aus RTK v1.0.1.
- Unterstützte Git- und Make-Befehle werden über `updatedInput` umgeschrieben; andere Eingabefelder bleiben erhalten, und bereits umschlossene oder nicht unterstützte Eingaben werden nicht umgeschrieben.
- Ungefilterte Ausführung verwendet `rtk bypass` und erhält stdout, stderr sowie den Exitcode des Kindprozesses.
- Der Strukturvalidator prüft genau einen nativen RTK-Handler und erlaubt unabhängige Hooks. Der Digest der geänderten Policy ist aktuell; fachfremde Befunde der Baseline bleiben sichtbar.

## Implementierungsentscheidung und Begründung

`rtk hook codex` wird unter `hooks.PreToolUse` mit dem Matcher `Bash` registriert. Die Ausführungsanweisungen bleiben in der bestehenden Policy, statt eine zusätzliche `RTK.md` zu erzeugen oder `AGENTS.md` zu verändern. Dokumentiert werden das lokale Vertrauen in Projekt und Hook, die explizite RTK-Ausführung bei nicht verfügbarer Interception sowie `bypass` als aktueller Name des veralteten Alias `proxy`. Eigene Filter, eine Pipeline oder ein Provider-API-Proxy sind nicht erforderlich.

Referenzen: [RTK v1.0.1 Codex-Integration](https://github.com/rtk-ai/rtk/blob/v1.0.1/hooks/codex/README.md), [v1.0.0-Migration](https://github.com/rtk-ai/rtk/releases/tag/v1.0.0) und [Codex-Hooks](https://developers.openai.com/codex/hooks).

## Geänderte Dateien

- `.codex/hooks.json`: native projektlokale Hook-Registrierung.
- `.codex/context/command-execution-policy.md`: aktuelle Hinweise zu Schema, Aufruf, Vertrauen und Fallback.
- `.codex/bin/validate-v32-structure.py`: minimale JSON-Prüfung der RTK-Registrierung unter Erhalt anderer Hooks.
- `.codex/inheritance-manifest.toml`: ausschließlich den Digest von `COMMAND-EXECUTION` aktualisieren.
- `reports/audits/change-records/CR-20261025-rtk-v1-codex-schema.md` und `reports/audits/change-records/CR-20261025-rtk-v1-codex-schema.de.md`: gleichwertige englische und deutsche Records.

## Ausgeführte Befehle

Die Prüfungen liefen aus dem Parent-Checkout mit dem absoluten Pfad zur aufgabenlokalen RTK-v1.0.1-Datei. In den folgenden Befehlsangaben bezeichnet `rtk` diese ausführbare Datei; `RTK_DB_PATH` wählte eine aufgabenlokale Datenbank, mit `PYTHONNOUSERSITE=1` und `PYTHONDONTWRITEBYTECODE=1`.

| Befehl oder Verfahren | Tatsächliches Ergebnis |
| --- | --- |
| `rtk bypass python3 -` mit einem Inline-Heredoc für die Akzeptanzprüfungen | PASS: alle neun unten aufgeführten Prüfungen |
| `rtk init --codex` in einer isolierten Fixture, aufgerufen durch dieses Prüfskript | PASS: erzeugte Hook-Konfiguration entspricht dem versionierten JSON |
| `rtk bypass python3 .codex/bin/validate-v32-structure.py` | Exit 0: `V3.2 structure: OK` |
| `rtk bypass python3 .codex/bin/validate-codex-inheritance.py --check --repository parent --json` | Exit 1: dieselben sechs fachfremden veralteten Digests wie in der Baseline; kein Befund zu `COMMAND-EXECUTION` |
| `rtk bypass make check-bilingual-docs` | Exit 0: `bilingual docs ok` |
| `rtk bypass make check-doc-links` | Exit 0: `repository path references: PASS` und `doc links ok` |
| `rtk bypass python3 ci/tools/new-change-record.py check` | Exit 0: `Change Record contract: PASS (structure only, not evidence validation)` |
| `rtk bypass git diff --check` und `rtk bypass git diff --cached --check` | Exit 0: keine Whitespace-Fehler |

Das offizielle Linux-musl-Releasearchiv wurde gegen SHA-256 `5b919c3bccb799b67a61866d0e617410a4fcdf173e2614440e59de2fa2003436` geprüft.

## Security-Auswirkung

Die Änderung betrifft die Agentensteuerung des Parents, nicht das Produktverhalten der Connectoren. Das Hook-Protokollfeld `permissionDecision = "allow"` ermöglicht den Eingabeersatz; normale Befehlsfreigaben, Sandbox-Prüfungen und die jeweilige Handlungsbefugnis gelten weiterhin. Globale Konfiguration, ein Trust-Bypass oder automatisches Host-Vertrauen werden nicht eingeführt. Bestehende Authentifizierungswrapper bleiben verpflichtend. Framework und MRTS bleiben unverändert.

## Runtime-Evidence

Die echte RTK-v1.0.1-Datei bestand diese frisch ausgeführten lokalen Prüfungen:

| Szenario | Ergebnis |
| --- | --- |
| Konfiguration entspricht der isoliert erzeugten Ausgabe von `rtk init --codex` | PASS |
| `git status` wird zu `rtk git status`; `timeout` und `description` bleiben in `updatedInput` erhalten | PASS |
| `make quick-check` wird zu `rtk make quick-check` | PASS |
| Bereits mit RTK umschlossener Befehl: keine Umschreibung | PASS |
| Unbekannter `permission_mode`: keine Umschreibung | PASS |
| Fehlender `permission_mode`: keine Umschreibung | PASS |
| Fehlerhaftes JSON: keine Umschreibung | PASS |
| Dateiumleitung: keine Umschreibung | PASS |
| `rtk bypass` erhält stdout, stderr und Exitcode 7 | PASS |

Diese Prüfungen belegen das Protokoll der ausführbaren Datei und die ungefilterte Ausführung. Sie belegen weder die Hook-Aktivierung in der laufenden Codex-Sitzung des Benutzers noch die Ausführung eines Connector-Build-/Testziels.

## Bekannte Einschränkungen

Die Parent-Vererbungsprüfung scheitert bereits an sechs veralteten Digests: `CHANGE-WORKFLOW`, `CONNECTOR-MATRIX`, `DEFINITION-OF-DONE`, `INDEX`, `PHASE4-TARGET-SEMANTICS` und `TESTING-AND-EVIDENCE`. Sie liegen außerhalb dieses Fixes und bleiben unverändert. Der native Hook lässt nicht unterstützte Eingaben absichtlich unverändert; die Vorgabe zur expliziten RTK-Ausführung gilt weiterhin.

## Verbleibende Risiken

Der Host benötigt eine kompatible RTK-Datei im `PATH` des Codex-Prozesses und Unterstützung für native Hook-Umschreibung. Der konkrete Projekthook muss über `/hooks` geprüft und als vertrauenswürdig bestätigt werden; ein Commit seines JSON erteilt dieses Vertrauen nicht. Die Befehlsklassifikation kann sich bei einem RTK-umschlossenen Befehl ändern, wie Upstream dokumentiert. Eine aktive Host-Sitzung oder durchgängige Host-Interception wird nicht behauptet.

## Nicht ausgeführte Prüfungen mit Begründung

Connector-Builds, Runtime-Suites, I12-Tests und die Validierung der Kind-Repositories wurden nicht ausgeführt, da diese Änderung auf die RTK-Agentensteuerung des Parents begrenzt ist. Die Parent-Dokumentationslinkprüfung verwendete den Framework-Helfer auf der unveränderten, vom Parent festgeschriebenen Revision `99a7985c1be92a2297b1b59208f64df6768f2cbf`; dies ist keine Framework- oder MRTS-Qualifikation. Die durchgängige Aktivierung in der Codex-Sitzung des Benutzers und entfernte CI-/Quality-Gate-Ergebnisse bleiben ungeprüft.

## Finaler Diff- und Review-Status

Die Änderung an sechs Dateien ist auf `fix/rtk-v1-codex-schema` vorbereitet. Die gezielten RTK-Akzeptanzprüfungen, der Strukturvalidator, die Dokumentationsprüfungen und die Diff-Prüfungen bestehen; das Vererbungsergebnis enthält weiterhin den bekannten Baseline-Fehler. Das koordinierende Diff-Review bestätigt die Begrenzung auf den Parent und den unveränderten Submodulzeiger. Dieser Record erfasst die lokalen Nachweise vor der Übergabe; der tatsächliche Pull Request ist für den entfernten Delivery- und CI-Status maßgeblich. Es wird kein Merge, Deployment oder aktive Host-Interception behauptet.
