# Change Record: CR-20261102-independent-host-context-policy

**Sprache:** [English](CR-20261102-independent-host-context-policy.md) | Deutsch

Unabhängige Policy-Lieferung; Framework-Pin bleibt getrennt.

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | CR-20261102-independent-host-context-policy |
| Datum (UTC) | 2026-11-02 |
| Basis-Revision | `2abad408cae7e5a103d12a9a9e432129bfe0468f` |

## Motivation und Problemstellung

Die unabhängige Anleitung zum Host-Ausführungskontext jetzt veröffentlichen; die breitere Framework-Pin-Qualifikation bleibt in [#436](https://github.com/Easton97-Jens/ModSecurity-conector/pull/436) offen. UID 0 allein belegt keine Voraussetzungen für Identitätswechsel oder private Sockets.

## Akzeptanzkriterien

Native Host-Kontextentscheidungen aus dem Parent-Index routen; Identitäts-, Ownership-, Socket-, Broker- und Cleanup-Anforderungen erhalten; die separat integrierte Framework-Anleitung ohne Parent-Pin-Update binden; nur die zwei eigenen Katalogdigests aktualisieren; vor regulärer Master-Integration die anwendbaren Prüfungen am exakten Head bestehen.

## Implementierungsentscheidung und Begründung

Unveränderlicher Anleitungsverweis auf Framework `b85280278310f4034af78149ac13671438965c7b`. Parent bleibt bei `e6284e8a8a64d999bf60f777252987172ab24756`; dort fehlen neue Anleitung und `--execution-context-only`. Das Beispiel verlangt eine ausdrücklich ausgewählte, kompatible und genehmigte Framework-Implementierung. Fehlende Implementierung blockiert den Hosttest. Die Policy bewirkt weder automatische Eskalation noch Kompatibilitätszulassung. Die Anleitung ist über `AGENTS.md` → `.codex/context/index.md` → `.codex/context/security-runtime-preflight.md` erreichbar.

## Geänderte Dateien

`.codex/context/index.md`, `.codex/context/security-runtime-preflight.md`, `.codex/inheritance-manifest.toml` und dieses EN/DE-Berichtspaar. Keine Änderung von Produkt, Gitlink, Lock, Workflow-Projektion, Framework-Quellen oder MRTS.

## Ausgeführte Befehle

Alle Shellbefehle verwenden RTK. `rtk bypass env PYTHONNOUSERSITE=1 PYTHONDONTWRITEBYTECODE=1 /var/tmp/codex/ModSecurity-test-Framework/venv/bin/python -P .codex/bin/validate-v32-structure.py`: PASS. Derselbe Interpreter mit `.codex/bin/validate-codex-inheritance.py --check --repository parent --json`: Exit 1, fünf unabhängige veraltete Digests erhalten (sechs auf der Basis einschließlich des eigenen Indexeintrags). `git diff --check`: PASS. `make check-bilingual-docs check-doc-links PYTHON=/var/tmp/codex/ModSecurity-test-Framework/venv/bin/python` mit explizitem `TEST_ROOT`, `FRAMEWORK_ROOT`, `CONNECTOR_ROOT`, exakter `CONNECTOR_REVISION` und externem Ausgabeziel: PASS (Sprachpaare, Repository-Pfade und Links). `ci/tools/new-change-record.py check`: PASS (nur Struktur). Die zwei eigenen Digests und unveränderte Pin-/Projektions-/Produktoberflächen: PASS. Inheritance-Vergleich Basis/Kandidat: PASS für keine neuen Diagnosen (9 → 8 einschließlich Framework-Kinddiagnosen; globaler Validator scheitert weiterhin). Gitleaks 8.30.1 auf dem Quellexport der fünf Dateien: PASS. Exakte Staging-/Commitbytes und Lieferungsergebnisse werden vor Integration erneut geprüft.

## Security-Auswirkung

Preflight im selben Launcher/Namespace, tatsächliche Worker-Wechsel und Zugriffsverbote, private UDS-Prüfung und Brokerzulassung erhalten. RTK und werkzeugspezifische Wrapper bleiben verpflichtend. Keine Guards, UID-Prüfungen, CI-Anforderungen oder Quality Gates werden abgeschwächt. Private Verification-JSON, Rohlogs, Runtime-Verzeichnisse und Umgebungsdaten sind ausgeschlossen.

## Runtime-Evidence

Kein neuer Hostlauf wird behauptet. Der private Beleg vom 2026-11-01 ist ausschließlich datierte Evidenz des ursprünglichen Quell-/Artefaktpaars. Envoy bleibt ohne eigenen Hostlauf unbestätigt. Wiederverwendete NGINX-Artefakte brauchen weiterhin passende Produktquell-, Build- und Artefaktzulassung.

## Bekannte Einschränkungen

Der unveränderte Parent-Framework-Pin kann das neue CLI-Beispiel nicht ausführen. Vollständiges Pin-Update, kompatible Produkt-APIs aus separat bearbeitetem [#348](https://github.com/Easton97-Jens/ModSecurity-conector/pull/348) und finale Paarqualifikation bleiben außerhalb dieser reinen Policy-Integration. Der erforderliche `traefik-go`-Fehler am #436-Head `1c91434752b7da3e31a4fe03c4d8c7d4a3707add` meldet fehlendes `Summary.ResponseIncomplete`.

## Verbleibende Risiken

Fünf unabhängige Parent-Katalogeinträge bleiben veraltet: `PARENT-CHANGE-WORKFLOW`, `PARENT-CONNECTOR-MATRIX`, `PARENT-DEFINITION-OF-DONE`, `PARENT-PHASE4-TARGET-SEMANTICS`, `PARENT-TESTING-AND-EVIDENCE`. Die vorhandene Inheritance-Abweichung der Framework-Kind-Befehlsrichtlinie bleibt unverändert. Das ist dokumentierte Drift, kein globales Inheritance-PASS.

## Nicht ausgeführte Prüfungen mit Begründung

Finale Framework-Pin-/Provenienzqualifikation, Apache-Vertrag, erneute NGINX-Artefaktzulassung, frischer NGINX-Hostnachweis, separate Launcher- und Cleanup-Evidenz gehören nach Erfüllung ihrer Abhängigkeiten zu #436. Sie werden durch diese reine Dokumentationsänderung nicht nachgewiesen und nicht als PASS behauptet.

## Finaler Diff- und Review-Status

Begrenzte Trennung gegen Basis `2abad408cae7e5a103d12a9a9e432129bfe0468f` geprüft. Nur Policy, Routing, zwei eigene Digests und Berichtspaar ausgewählt. Der Nutzer autorisierte die getrennte reguläre Master-Integration; aktuelle Head-CI, Sonar-Rücklesen mit null neuen Issues/Hotspots, Reviews und Schutzprüfungen am exakten Head bleiben vor Merge verpflichtend. Lieferungs-/Mergefakten werden aus GitHub zurückgelesen und hier nicht vorweggenommen.
