# Change Record: CR-20261114-ai-handoff-and-framework-pin

**Sprache:** [English](CR-20261114-ai-handoff-and-framework-pin.md) | Deutsch


## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | CR-20261114-ai-handoff-and-framework-pin |
| Datum (UTC) | 2026-11-14 |
| Basis-Revision | `5672c5ff562495ddbc47a1932b1641e0073746f5` |

## Motivation und Problemstellung

Der Nutzer beauftragte eine Claude-Code-Übergabe und danach einen PR einschließlich der anderen vorhandenen Änderungen. Ein reines Framework-Zeigerupdate ließe Parent-Lock und Workflow-Identitäten inkonsistent.

## Akzeptanzkriterien

Bestehende Anweisungen und Ignore-Ergänzungen erhalten, eine korrekte EN/DE-Übergabe liefern, den veröffentlichten Framework-Commit konsistent auswählen, native Veröffentlichungs-/Dokumentationsprüfungen bestehen und einen aufgabeneigenen Draft-PR ohne Merge öffnen.

## Implementierungsentscheidung und Begründung

Den vorhandenen transaktionalen Synchronisierer mit dem exakten Git-common.sh-Blob als Daten verwenden. Framework `31531f74cfe26c2a40d4bb5f6eaae4c0920127e1` statt `62b411e073551ef0fef22ab3d372e2489f2ae168` auswählen; MRTS `ee2174431c4edf97e66afe32558ce8454deb2397` erhalten. Ein unabhängiger Vergleich belegte, dass jede Workflow-Änderung die Framework-SHA exakt ersetzt und sich im Lock nur `framework_sha` ändert. Generische Komponententupel bleiben unverändert. Ignorierte lokale `CLAUDE.md` außerhalb von Git halten. Für die Whitespace-Prüfung nur die vorhandene zusätzliche Leerzeile in `.gitignore` entfernen.

## Geänderte Dateien

`.gitignore`, `AGENTS.md`, `docs/AI-HANDOFF.md`, `docs/AI-HANDOFF.de.md`, Parent-Framework-Gitlink, `ci/tooling/project-versions.lock.json`, die 22 `.github/workflows/`-Einträge der festen Framework-Projektionsregistry des Synchronisierers und dieses Change-Record-Paar. Die lokale ignorierte `CLAUDE.md` wurde zur Fortsetzung aktualisiert, bleibt aber vom PR ausgeschlossen. Keine Connector-, Framework- oder MRTS-Quelltextänderungen.

## Ausgeführte Befehle

| Befehl | Tatsächliches Ergebnis |
| --- | --- |
| `rtk bypass git ls-remote https://github.com/Easton97-Jens/ModSecurity-conector.git refs/heads/master` | Exit 0; Basis `5672c5ff562495ddbc47a1932b1641e0073746f5`. |
| `rtk bypass git ls-remote https://github.com/Easton97-Jens/ModSecurity-test-Framework.git refs/heads/master` | Exit 0; ausgewählte Framework-SHA ist veröffentlichter master. |
| `rtk bypass .venv/bin/python -I ci/tools/verify-framework-candidate-contract.py --candidate-sha 31531f74cfe26c2a40d4bb5f6eaae4c0920127e1 --framework-common /var/tmp/codex/ModSecurity-conector/ai-handoff-pr-20261114/framework-common.sh --candidate-framework-root /root/git/ModSecurity-conector/modules/ModSecurity-test-Framework --expected-parent-framework-sha 31531f74cfe26c2a40d4bb5f6eaae4c0920127e1` | Exit 0, `status=verified`; derselbe Prüfer bestand vor der Synchronisation auch mit der alten erwarteten Parent-SHA. |
| `rtk bypass env RUNNER_TEMP=/var/tmp/codex/ModSecurity-conector/ai-handoff-pr-20261114 .venv/bin/python -B ci/tools/sync-framework-component-versions.py --sync --framework-common /var/tmp/codex/ModSecurity-conector/ai-handoff-pr-20261114/framework-common.sh --framework-sha 31531f74cfe26c2a40d4bb5f6eaae4c0920127e1 --framework-object-root /root/git/ModSecurity-conector/modules/ModSecurity-test-Framework` | Exit 0; Lock und 22 Workflow-Identitäten generiert. |
| `rtk bypass env RUNNER_TEMP=/var/tmp/codex/ModSecurity-conector/ai-handoff-pr-20261114 .venv/bin/python -B ci/tools/sync-framework-component-versions.py --check --framework-common /var/tmp/codex/ModSecurity-conector/ai-handoff-pr-20261114/framework-common.sh --framework-sha 31531f74cfe26c2a40d4bb5f6eaae4c0920127e1 --framework-object-root /root/git/ModSecurity-conector/modules/ModSecurity-test-Framework` | Exit 0; `changed=[]`. |
| `rtk bypass env RUNNER_TEMP=/var/tmp/codex/ModSecurity-conector/ai-handoff-pr-20261114 .venv/bin/python -B ci/tools/sync-framework-component-versions.py --verify-primary --base 5672c5ff562495ddbc47a1932b1641e0073746f5 --framework-common /var/tmp/codex/ModSecurity-conector/ai-handoff-pr-20261114/framework-common.sh --framework-sha 31531f74cfe26c2a40d4bb5f6eaae4c0920127e1 --framework-object-root /root/git/ModSecurity-conector/modules/ModSecurity-test-Framework` | Exit 0; `FRAMEWORK_PRIMARY_VERIFIED`. |
| `rtk bypass /usr/local/bin/sonar-with-env analyze secrets --stdin` | Ausdrückliche Scans ausgewählter Inhalte mit Exit 0; rohe Ausgabe unterdrückt. |
| `rtk make check-doc-links`; `rtk bypass git diff --cached --check` | Exit 0; Repository-Pfade, lokale Links und gestagter Whitespace sauber. |
| `rtk make check-bilingual-docs` | Nach 15 Minuten CPU-Arbeit in wiederholter Ignore-Pfadabfrage beendet; Exit 2 nach Abbruch, kein PASS. |
| `rtk bypass env CONNECTOR_REVISION=5672c5ff562495ddbc47a1932b1641e0073746f5 .venv/bin/python -B /var/tmp/codex/ModSecurity-conector/ai-handoff-pr-20261114/check_bilingual.py` | Exit 0, `bilingual docs ok`; alle vorhandenen Regeln/Auswahlen des vollständigen Prüfers erhalten, mit gleichwertigem indiziertem Ignore-Pfadprädikat. Kein Prüferquelltext geändert. |
| `rtk bypass env CONNECTOR_ROOT=/root/git/ModSecurity-conector TEST_ROOT=/root/git/ModSecurity-conector/modules/ModSecurity-test-Framework FRAMEWORK_ROOT=/root/git/ModSecurity-conector/modules/ModSecurity-test-Framework PYTHONPATH=/root/git/ModSecurity-conector/modules/ModSecurity-test-Framework:/root/git/ModSecurity-conector/modules/ModSecurity-test-Framework/connector_suite .venv/bin/python -B ci/tools/new-change-record.py check` | Exit 0; Change-Record-Strukturvertrag bestanden. |
| `rtk bypass git commit -m 'Prepare AI handoff and synchronize Framework maintenance pin'` | Exit 1; pre-commit-Hook verweigerte den gestagten Gitlink: `No exact operator V2 admission for selected Gitlink`. In diesem ersten Versuch kein Commit erstellt. |
| `rtk bypass python3 -B /var/tmp/codex/ModSecurity-conector/ai-handoff-pr-20261114/operator_admission.py install --expected-plan-sha256 4da207519ebc4839396b5ea98de19b6db3b4bc5f747e98e0a4ca6ae1822dd362` | Exit 0; vom Nutzer autorisierte exakte Indexfreigabe nach vollständigen Quellen-/geschützten nativen Prüfungen installiert; bestehende Einträge und ausführbare Guards erhalten. |
| `rtk bypass git commit -m 'Prepare AI handoff and synchronize Framework maintenance pin'` | Folgeversuch mit Exit 0 durch den normalen Hook; erster 30-Dateien-Commit `82472f02170c34183998780f8ab77b90a7c8a299`. |
| `rtk bypass .venv/bin/python -I ci/tools/read-framework-revisions.py --parent-sha 82472f02170c34183998780f8ab77b90a7c8a299` | Exit 0; committete Framework-/MRTS-Pins stimmen mit den materialisierten Checkouts überein. |

Auch die Prüfung der gestagten Veröffentlichung `--verify-primary --staged` endete mit Exit 0 und `FRAMEWORK_PRIMARY_VERIFIED`. Anfängliche Einrichtungsfehler wurden mit expliziter Framework-Umgebung/Importpfaden, `.venv/bin/python` für PyYAML und dem aufgabeneigenen erlaubten `RUNNER_TEMP` behoben. Keine Pakete installiert.

Der erste große Quellenbatch lief in eine Zeitüberschreitung (Exit 1); sein gesamter Inhalt wurde vor Ausgabe der vollständigen Nachweise erfolgreich in kleineren vollständigen Blob-Batches erneut geprüft. Zwei große Git-Blobs wurden tatsächlich über ganze Dateien geprüft; keine Quellbytes ausgelassen. Die Prüfung mit verkürzter Parent-SHA wurde abgewiesen (Exit 1); der obige Aufruf mit vollen 40 Zeichen bestand.

## Security-Auswirkung

Keine Authentifizierung, Autorisierung, Laufzeit-Sicherheitsstandards oder CI-Gates abgeschwächt. Lokale `.claude`-, `.rtk`- und `.aws`-Pfade ignorieren; keine Inhalte dieser Verzeichnisse oder Zugangsdatenablagen ausgewählt. Generierte Workflows ändern nur die exakte Framework-Revision. Secrets-Scanning ist kein Codequalitäts- oder Laufzeitnachweis.

## Runtime-Evidence

Es wurde keine Runtime-Evidence erhoben oder beansprucht.

## Bekannte Einschränkungen

Behobene Auslieferungssperre: Der Nutzer erlaubte ausdrücklich die exakte Operator-Freigabe für Gitlink/Index. Vollständige Quellenprüfungen für Framework 2514 reguläre/9 Alias-Blobs und MRTS 431 reguläre/41 Alias-Blobs bestanden; geschützte native und Parent-Index-Prüfungen bestanden vor Veröffentlichung des Registry-Eintrags. Bestehende Einträge und ausführbare Guards blieben erhalten. Der normale Commit-Hook bestand anschließend.

Ignorierte `CLAUDE.md` ist nur lokal verfügbar. Die Übergabe nennt bewusst ihre ursprüngliche Basis und den zuletzt beobachteten Commit; späteren HEAD/PR-Stand aus Git/GitHub ermitteln. Die lokale Validierungsumgebung belegt keine Bereitschaft gepinnter Werkzeugketten oder gehosteter Laufzeiten. Das gewöhnliche zweisprachige Target wurde nach 15 Minuten beendet; der gesamte vorhandene Prüfer bestand mit dem gleichwertigen indizierten Ignore-Adapter, während das ursprüngliche Nichtbestehen oben erhalten bleibt.

## Verbleibende Risiken

Framework-Integration ist nur auf Vertrags-/Projektionsebene geprüft. Gehostete Checks, Reviews und gegebenenfalls ein Quality Gate für den aktuellen HEAD bleiben eigenständige Auslieferungsanforderungen; keine Merge- oder Release-Bereitschaft beansprucht.

## Nicht ausgeführte Prüfungen mit Begründung

Keine Produkt-Builds, `quick-check`, `test`, gehosteten Laufzeit-/Konfigurationsproben, vollständigen Matrizen oder I12-Kampagnen: Diese Arbeit bereitet Dokumentation vor und übernimmt einen bereits veröffentlichten Wartungs-Pin. Gehostete CI-/Cloud-Ergebnisse sind vor dem Push nicht verfügbar; keine früheren Ergebnisse werden auf den neuen Commit übertragen.

## Finaler Diff- und Review-Status

Der erste geprüfte 30-Pfade-Stand wurde als `82472f02170c34183998780f8ab77b90a7c8a299` durch den ursprünglichen Hook committet. Die exakte Prüfung der committeten Framework-/MRTS-Pins bestand. Diese Dokumentationsaktualisierung erfasst die behobene Freigabesperre vor Push/Draft-PR-Veröffentlichung; spätere Auslieferung aus Git/GitHub ermitteln. Keine master-Integration oder Schreibaktion in verschachtelten Repositorys erfolgte.
