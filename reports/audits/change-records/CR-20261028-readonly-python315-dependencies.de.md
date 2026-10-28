# Change Record: CR-20261028-readonly-python315-dependencies

**Sprache:** [English](CR-20261028-readonly-python315-dependencies.md) | Deutsch

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | CR-20261028-readonly-python315-dependencies |
| Datum (UTC) | 2026-10-28 |
| Basis-Revision | `d50877a697c8eae3e18f2226d0b6532622ecdcd0` |

## Motivation und Problemstellung

Updater-Lauf `40648924250`, Job `122684319837`, besteht die vorherige NGINX-Übergabereparatur, scheitert aber im privaten Namespace bei `PyYAML==6.0.3`: Es gibt kein passendes CPython-3.15-Binärwheel. Der übersehene Namespace-Pfad verwendete noch den alten Binary-only-Lock statt des bereits geprüften Parent-Quellinstallers. Gewünscht ist die Reparatur unter Beibehaltung von Quellschutz und Kandidaten-Privilegientrennung.

## Akzeptanzkriterien

Nur die geprüfte PyYAML-Abhängigkeit vor dem Runtime-Schutz vorbereiten; den Framework-Lock des Kandidaten ausschließlich als Daten prüfen. Ursprünglich gewähltes Python und isolierten Import im Jail erhalten. Bei fehlgeschlagener Vorbereitung beziehungsweise Import vor Make stoppen. Alle Quell-, Namespace-, Ausgabe-, Rechte- und Veröffentlichungskontrollen sowie die exakte automatische Auswahl von 100 Fällen / 80 Ausführungen erhalten. Neue gehostete Validierung am tatsächlichen Head bleibt erforderlich.

## Implementierungsentscheidung und Begründung

Der normale Runner ruft nach den Kandidatendatenprüfungen und vor privatem Guard/Sandbox den unveränderten vertrauenswürdigen Parent-Installer `ci/tools/install-ci-dependencies.py --ci-toolcache --framework-lock modules/ModSecurity-test-Framework/requirements-ci.lock` auf und führt danach `python3 -m pip check` aus. Nur die gewählte setup-python-Runtime erhält das geprüfte reine Python-Wheel. Sie wird anschließend schreibgeschützt eingebunden. Während der Vorbereitung wird kein Framework-Kandidatencode ausgeführt.

Der Namespace ersetzt den veralteten Binary-only-pip-Aufruf durch `"$PYTHON" -I -c "import yaml; assert not yaml.__with_libyaml__"` und erhält anschließend ursprünglichen Make-Aufruf und Interpreter. `-I` ignoriert Kandidaten-`PYTHONPATH`. Keine Installer-API, Abhängigkeitsversion, Quell-/Build-Tool-Lockdatei, Job-Berechtigung oder Ref-Allowlist wird geändert.

Ein Prototyp mit privatem Virtual Environment wurde verworfen: Python 3.15 kopiert Modusbits der Aktivierungsvorlagen einschließlich Gruppenschreibrechten, die der bestehende Ausgabeschutz korrekt ablehnt. Die Vorbereitung außerhalb des Validator-Ausgabebaums vermeidet dort sowohl Ziel- als auch Builder-Umgebung und erhält diesen Schutz.

## Geänderte Dateien

- `.github/workflows/update-submodules.yml`: geprüfte Abhängigkeitsvorbereitung und pip-Prüfung vor dem Schutz.
- `ci/tools/run-readonly-submodule-validation-namespace.py`: isolierte Prüfung der vorbereiteten Abhängigkeit, keine Installation im Jail.
- `tests/test_ci_security_workflows.py`, `tests/test_run_readonly_submodule_validation_namespace.py`: Regressionen für Reihenfolge, Argumente, Isolation, Fehlerweitergabe und unveränderten Interpreter. Eine neue Methode bleibt nur auf Abruf.
- `config/testing/active-cases.json`: sechs ausdrücklich geprüfte Quell-SHA256-Felder; vollständige Standard-/Archiv-Ausführungslisten unverändert (100/80 und 1893/839).
- `reports/testing/test-selection-archive.generated.json`: durch nativen Generator erneuert; eine zusätzliche erhaltene Methode auf Abruf.
- `docs/build/README.md`, `docs/build/README.de.md`, `docs/security/ci-security-tooling.md`, `docs/security/ci-security-tooling.de.md`: gleichwertige Dokumentation von aktuellem Verhalten und Vertrauensgrenzen.
- Dieses englisch/deutsche Change-Record-Paar.

## Ausgeführte Befehle

Jeder Projekt-Shell-Payload wurde durch aufgabeneigenes, prüfsummenverifiziertes RTK `v1.0.1` gekapselt.

| Prüfung | Beobachtetes Ergebnis |
| --- | --- |
| Geprüfter Installer in einem aufgabeneigenen Python-3.15.1-Venv mit `--build-root /workspace/scratch/5e0fa1c15f63/task-state/pyyaml315-host-validation/build --framework-lock modules/ModSecurity-test-Framework/requirements-ci.lock` | Exit 0; tatsächlicher gepinnter Quellbau/Installation, PyYAML 6.0.3, `libyaml_extension: false`. |
| Derselbe Interpreter, `-m pip check` | Exit 0, keine defekten Anforderungen. |
| Sieben explizite betroffene Unittest-Selektoren unter Python 3.15.1 mit `ON_DEMAND_TESTS=1` | Exit 0, 7 bestanden; Kandidatenprogramm-/Preflight-/Workflow-Tests sowie Ablehnung beschädigter Quelle, beschädigtem Builder, abweichender Framework-Version und nativem Wheel. |
| Drei finale Kandidaten-/Preflight-/Workflow-Regressionen unter Python 3.12.14 | Exit 0, 3 bestanden. Der im Speicher geladene ursprüngliche Helper scheitert bei beiden neuen Preflight-Szenarien an der beabsichtigten Grenze. |
| Tatsächlich vorbereitetes Python 3.15.1/PyYAML 6.0.3 durch den Kandidaten-Shell-Abschluss; nur Make an seiner externen Grenze ersetzt | Exit 0; isolierter Import erfolgreich, ursprünglicher Interpreter erreicht Make, keine Abhängigkeitsdateien in der externen Ausgabe ergänzt. |
| Vollständige Quell-/Inventarzulassung, exakter Auswahlvergleich, Archivgenerator und `--check`, Projektversionsprüfung | Bestanden; Standard- und Archiv-Ausführungslisten unverändert. |
| Lokales `make quick-check` mit Python 3.15.1 und Kandidaten-Ausgabepfadumgebung | Bei `common.memory-lifetime` blockiert: LeakSanitizer kann in dieser Umgebung `/proc/.../task` nicht prüfen; kein Sanitizer deaktiviert. Frühere lokale Versuche hatten fehlende Ausgabeverzeichnisse; der eingerichtete Versuch bestand diese Voraussetzungen. |
| `python3 ci/checks/common/check-python-version-contract.py` | Exit 1: fünf bestehende Abweichungen; ein Vergleich im Speicher mit unverändertem Master-Workflow liefert exakt dieselben fünf. Dieser Patch ergänzt keine. |
| Dokumentation und finale Whitespace-Prüfungen | Bestanden: zweisprachige Dokumentation, Dokumentationslinks, Change-Record-Struktur und finale Whitespace-Prüfungen. |

Quell-SHA256: `d76623373421df22fb4cf8817020cbb7ef15c725b9d5e45f17e189bfc384190f`; SHA256 des lokal gebauten Wheels: `4806af48a4cec5305abb1d0f44a64c0351aa22ed9a941dd3c89979bde5b73dc9`. Die getrennte Python-3.15.1-Testlaufzeit stammt aus `astral-sh/python-build-standalone`-Release `20261021`, geprüft mit SHA256 `01d901e09ca673c99a6c9bd9ec2cfbd58dbe8813d07514c36cb73cfd20b18bd8`; sie ersetzt keine Repository-Pins oder gehostete Runtime.

## Security-Auswirkung

Abhängigkeitsausführung bleibt auf die zuvor geprüfte hash-gepinnte Parent-Quell-/Build-Tool-Ausnahme unter dem normalen Runner mit der von Zugangsdaten bereinigten Backend-Umgebung des Installers begrenzt. Framework-Kandidateneingaben sind ausschließlich passive Lock-Daten. Kandidatencode läuft weiterhin erst nach UID-/GID-Wechsel im vorhandenen privaten Jail. Runtime-/Quell-Mounts, Schreibproben, Ausgabe-Rechte-/Link-Prüfungen, Sanitizer-Prüfungen, CI-Berechtigungen, Ref-Gates und Veröffentlichungstrennung bleiben unverändert.

## Runtime-Evidence

Lokaler Bau und Import belegen das Abhängigkeits-Bootstrap-Verhalten unter exakt Python 3.15.1. Sie belegen weder vollständige privilegierte Namespace-Ausführung noch einen erfolgreichen gehosteten Updater, Connector-Runtime-Qualifizierung oder I12-Abnahme. Keine solche Behauptung wird erhoben.

## Bekannte Einschränkungen

Die lokale Umgebung kann weder den Sanitizer-gestützten Quick-Check noch den privilegierten gehosteten Namespace vollständig ausführen. Updater-Dispatch ist absichtlich auf Master oder dessen vorhandene geprüfte Validierungs-Ref beschränkt; dieser Patch erweitert die Allowlist nicht für einen Task-Branch. Gehostete Validierung muss nach normaler Integration ausgelesen werden. Die erste vollständig bereinigte lokale Netzwerkprobe konnte den Artefakthost nicht auflösen; anschließend bestand der dokumentierte hostseitige Installer unter normaler Host-Umgebung.

## Verbleibende Risiken

Der aktuelle Master hat zusätzlich fünf unveränderte Python-Workflow-Vertragsabweichungen: ein vertrauenswürdiges lighttpd-Profil, zwei geschützte wiederverwendbare NGINX-Referenzen und zwei nicht gelistete native Sonar-Jobs. Sie werden als Basiszustand dokumentiert und in dieser reinen Abhängigkeitsänderung weder stillschweigend akzeptiert noch repariert. Neue PR-CI/Sonar kann weitere bestehende Fehler zeigen. Kein bestandenes Gesamt-Gate wird behauptet.

## Nicht ausgeführte Prüfungen mit Begründung

Vollständige Updater-Veröffentlichung, neue gehostete schreibgeschützte Namespace-Validierung, Connector-Runtime/-Matrix und neue Sonar-Analyse sind keine lokalen Ausführungsnachweise. Der vollständige lokale Quick-Check ist wie oben umgebungsbedingt blockiert; keine Regel, kein Sanitizer, Test oder Gate wurde umgangen. Historische I12-Arbeit bleibt außerhalb des Umfangs.

## Finaler Diff- und Review-Status

Ein unabhängiges rein lesendes Review fand keinen materiellen Blocker in finalem Workflow/Helper/Tests. Abschließende integrierte Auslieferung und gehostete Prüfungen des tatsächlichen Heads stehen aus. Dieser Record behauptet weder Merge, Master-Änderung, neuen Updater-Erfolg noch Status `verified_pr`.
