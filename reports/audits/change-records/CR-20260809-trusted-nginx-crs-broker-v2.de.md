# Change Record

**Sprache:** [English](CR-20260809-trusted-nginx-crs-broker-v2.md) | Deutsch

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | CR-20260809-trusted-nginx-crs-broker-v2 |
| Datum (UTC) | 2026-08-09 |
| Basis-Revision | cc58f94e6a0dd17eea651cd46376843472b83f7c |

## Motivation und Problemstellung

Der historische vertrauenswürdige NGINX-Broker führt `with-crs` nur als
Matrix-Label und verwendet immer seine Broker-eigene `/blocked`-Regel. Damit
lässt sich kein echter NGINX-OWASP-CRS-Block belegen. Die autorisierte
v2-Änderung erweitert den bestehenden engen Broker-Vertrag, bevor PR #240
einen neuen geschützten Merge-SHA verwenden darf.

## Akzeptanzkriterien

Schema v1 bleibt eine reproduzierbare No-CRS-Kontrolle. Schema v2 liefert nur
geschlossene Profile `no-crs` und `owasp-crs`; der Caller wählt weder CRS-Pfad
noch Regel, Ref oder Digest. Der geschützte Workflow muss ein frisches
CRS-Bundle aus Repository/Tag/Commit bauen, root darf nur dessen exakte
digestverifizierte Inhalte aufnehmen, und `owasp-crs` muss seinen eigenen
NGINX-Allow/Block, CRS-Regel, Audit, Identität, Evidence und Cleanup belegen.
Kein PR-240-, Framework-in-PR- oder Caller-Code darf als root laufen.

## Implementierungsentscheidung und Begründung

Der bestehende SHA-gebundene wiederverwendbare Workflow und Python-Broker
werden erweitert, statt einen zweiten Root-Runner zu bauen. Der v2-Broker
pinnt unabhängig https://github.com/coreruleset/coreruleset.git, Tag
`v4.28.0`, Commit `55b09f5acfd16413e7b31041100711ceb7adc89c` und erwartete
Blockregel `949110`. Eine geschützte unprivilegierte Fresh-Source-Stufe erzeugt
ein sortiertes manifestiertes Bundle. Root verwendet descriptor-relative
no-follow-Admission mit Owner-/Mode-/Device-/Linkcount-/Inode-/Größen- und
Vorher-/Nachher-Digest-Prüfungen und erzeugt feste root-lokale
ModSecurity-Includes und portable serielle Audit-Konfiguration.

## Geänderte Dateien

- `.github/workflows/nginx-root-broker.yml`
- `ci/runtime/broker/nginx_root_broker.py`
- `ci/runtime/lifecycle/prepare-fresh-crs-source.sh`
- `tests/test_nginx_root_broker_crs_profile.py`
- `tests/test_nginx_root_broker_workflow.py`
- `tests/test_ci_security_workflows.py`
- `docs/security/trusted-nginx-root-broker.md` und `.de.md`
- dieser Change Record und seine deutsche Begleitdatei

## Ausgeführte Befehle

Bisher beobachtet: Python-Kompilierung des Brokers sowie die fokussierte
Broker-, v2-Profil-, Workflow-Vertrag- und CI-Security-Suite. Die fokussierte
Suite lief mit 53 Tests erfolgreich. Weitere projektnative Qualitäts-,
Dokumentations-, Shell-, Security-Diff- und Hosted-Prüfungen bleiben vor der
Auslieferung erforderlich.

## Security-Auswirkung

Die Änderung behält die feste Action-Allowlist bei und weist Caller-Command,
Shell, Konfiguration, Regel, CRS-Source und Binary-Eingaben an der
Root-Grenze ab. Der neue Root-Input ist ausschließlich ein Protected-Build-
Bundle, dessen Topologie und Inhalt vor der Materialisierung erneut validiert
werden. Das CRS-Profil kann keinen PASS aus der Broker-eigenen No-CRS-
`/blocked`-Regel ableiten: Es verlangt die kanonische CRS-Anfrage, einen echten
Audit-Record, die exakte Regel `949110` und das gebundene Tupel/Digest. Cleanup
bleibt descriptor-relativ und entfernt nur die feste Run-Root.

## Runtime-Evidence

Es wurde noch kein Protected-master-Hosted-v2-Lifecycle beobachtet. Lokale
fokussierte Tests beweisen weder GitHub-Reusable-Workflow-Semantik noch einen
realen NGINX-Root-Master, Nicht-root-Worker, echte CRS-Auswertung,
Audit-Ausgabe, Listener-Freigabe oder den hochgeladenen Cleanup-Record. Das
sind verpflichtende Resulting-master-Validierungen nach einem normalen
geschützten Merge und vor Änderungen an PR #240.

## Bekannte Einschränkungen

Das v2-Profil ist absichtlich keine allgemeine CRS-Ausführungsplattform. Es
nimmt nur das feste geprüfte CRS-Tupel, die ausgewählte Dateitopologie, feste
Loopback-Anfragen und die feste Evidence-Allowlist auf. Es fügt keine
Caller-Overrides, dynamischen Includes, Archiv-Input oder beliebigen
privilegierten Aktionen hinzu.

## Verbleibende Risiken

GitHub-Actions-Kontextwerte, aktuelles Hosted-Image-Verhalten,
Framework-Fetch-Verhalten, NGINX-/ModSecurity-/CRS-Runtime-Kompatibilität und
Artefakt-Upload müssen noch auf dem geschützten resultierenden master bewiesen
werden. Ein Fehler blockiert Merge oder Post-Merge-Validierung; er autorisiert
niemals einen Fallback zu PR-Branch-Root-Ausführung oder einen synthetischen
CRS-PASS.

## Nicht ausgeführte Prüfungen mit Begründung

Zum Zeitpunkt dieser lokalen Implementierung wurden actionlint, ShellCheck,
zizmor, das vollständige projektnative Local-Gate, der fokussierte
Security-Diff-Scan, Hosted-Checks, CodeQL, SonarQube Cloud,
Review-/Branch-Protection-Gates und die Protected-master-Runtime-Validierung
noch nicht beobachtet. Sie werden absichtlich nicht behauptet, bevor sie auf
dem finalen exakten Head laufen.

## Finaler Diff- und Review-Status

Dieser Record beschreibt eine uncommittete v2-Implementierung im separaten
Branch `fix/ci-trusted-nginx-crs-broker-v2`, basierend auf
`cc58f94e6a0dd17eea651cd46376843472b83f7c`. Es gab noch keinen neuen
Pull-Request, Push, Merge, PR-240-Update, Framework-Source-Change, MRTS-Change,
Force-Push, History-Rewrite oder Auto-Merge. Der neue Broker-PR bleibt
auslieferungsblockiert, bis alle erforderlichen lokalen, Security-, Hosted-,
Sonar-, Review- und Branch-Protection-Evidence dokumentiert sind.
