# Change Record: Vorbereitung der Framework-Handoff-Reparatur

**Sprache:** [English](CR-20260929-framework-handoff-repair-preparation.md) | Deutsch

## Identität

| Feld | Wert |
| --- | --- |
| Change ID | CR-20260929-framework-handoff-repair-preparation |
| Datum | 2026-09-29 |
| Parent-Basis | `d56af0856507eb048987974d3960e301e7c24371` |
| Lieferstatus | Nur Vorbereitung; die Produktionskorrektur ist nicht angewendet. |

## Motivation

Der Benutzer hat Diagnose, Behebung und einen separaten Pull Request für
[Lauf 36608694822, Job 109544329844](https://github.com/Easton97-Jens/ModSecurity-conector/actions/runs/36608694822/job/109544329844)
angefordert.

Der erste maßgebliche Fehler lautet
`Framework common.sh differs from approved reviewed structure`, aus
`ci/tools/verify-framework-candidate-contract.py`, Exitcode 2. Die abschließende
Sandbox-Erfolgsprüfung scheitert, weil Vorbereitung und Kandidatenausführung
übersprungen wurden; sie ist nicht die ursprüngliche Ursache.

Der Updater schlägt Framework
`0290a979ba4bc63a7abed175a53471367b385553` statt
`f9e48b0774b5bdf7aaa8e38ce98eb6c50bf293c8` vor. Die `common.sh` des
Kandidaten ändert zwölf literale Pins: NGINX-Release/Prüfsumme,
AWS-LC-Tag/Commit, go-ftw-Tag/Commit, Node.js-Version, CodeQL-Version/Commit
sowie Ruff-Version/Commit/Prüfsumme. Diese Bytes bleiben absichtlich von
der strukturellen Parent-Review-Grenze erfasst.

## Akzeptanzkriterien

Die angeforderte Reparatur ist erst abgeschlossen, wenn der erzeugte Patch
geprüft und angewendet wurde, der echte Kandidat die unveränderten
Vertragsprüfungen besteht und die CI des aktuellen Heads verifiziert wurde.
Dieser reine Vorbereitungs-PR erfüllt das noch nicht. Er darf nicht als
abgeschlossene Produktionskorrektur gemergt werden.

## Technische Entscheidungen

Der neue einmalige Generator liest die zwei exakten Framework-Git-Objekte als
Daten. Er prüft, dass die Basis den aktuell freigegebenen Strukturhash
`7ad268af3baa17d2c2e9b5857ced2138684fab70e5066ddddd6f3656e8baa6af`
reproduziert und der Kandidat ausschließlich die zwölf geprüften Zuweisungen
ändert. Anschließend berechnet er den neuen Hash, statt einen Wert zu raten.

Der geplante Patch gleicht 19 fest begrenzte Parent-Textpfade und einen
Framework-Gitlink ab. Er aktualisiert den ausdrücklichen Freigabehash, die
ungeschützte NGINX-Übergabe samt Fixtures und alle registrierten
CRS/no-MRTS-Framework-SHA-Verbraucher. Er ergänzt eine Regression mit der
echten `common.sh` und hält den Negativtest für das nächste ungeprüfte
Release mit `release-1.31.7` unterscheidbar.

Das geprüfte NGINX-Tupel lautet `release-1.31.6`, Asset
`nginx-1.31.6.tar.gz`, SHA-256
`974ed5298a5e398e008704ed5db284e655fc270c596493dbccada452448fc9f1`.
Der Hash wurde aus den
[offiziellen Release-Metadaten](https://github.com/nginx/nginx/releases/tag/release-1.31.6)
gelesen. Diese Quellherkunftsprüfung ist kein Laufzeittest.

Der Generator lehnt Zieldateien ab, die von der geprüften Parent-Basis
abweichen, prüft die Syntax geänderter Python-Dateien und ruft
`git apply --check --index` auf. Er schreibt nur eine neue Patchdatei und
überschreibt keine vorhandene Ausgabe. Er führt weder Apply, Staging,
Fetch, Checkout, Commit oder Push durch noch erstellt er einen Workflow.
Der vollständige Patch aus dem echten Repository wurde in dieser Sitzung
noch nicht erzeugt oder angewendet.

## Sicherheitsauswirkung

Diese Vorbereitung ändert keine produktive Schutzprüfung, Parsergrammatik,
Liste veränderlicher Felder, Provenance-Policy, Sandbox,
Publisher-Berechtigung oder geschützten NGINX-Root-Broker-Pin. Auch der
geplante Patch lässt diese Grenzen bestehen. Keine Framework- oder
MRTS-Quelldatei soll geändert werden. NGINX wird nicht dem generischen
Synchronisierer hinzugefügt. Der Generator sourct niemals Kandidaten-Shellcode.

## Geänderte Dateien

- `ci/tools/prepare-reviewed-framework-handoff.py`
- `tests/test_prepare_reviewed_framework_handoff.py`
- `reports/audits/change-records/CR-20260929-framework-handoff-repair-preparation.md`
- `reports/audits/change-records/CR-20260929-framework-handoff-repair-preparation.de.md`

## Tests und tatsächliche Ergebnisse

Der unveränderte Generator und seine Testdatei wurden mit Python 3.13.5
aus einem isolierten Fixture-Verzeichnis geladen: **19 Unit-Tests bestanden**.
Beide neuen Python-Dateien bestanden AST-Parsing und eine Prüfung auf
nachgestellte Leerzeichen. Die Tests prüfen zusätzliche
Kandidatenänderungen, Basisabweichungen, fehlende/doppelte Zuweisungen,
begrenzte Zielpfade, wirksame Negativtests, Python-Syntax, Gitlink-Patchinhalt,
fehlende letzte Zeilenumbrüche, Symlinks und den Schutz bestehender Ausgaben.

Das war kein projektnativer Testlauf und verwendete nicht die gepinnte
Python-3.14.7-CI-Umgebung. Die exakte Patchprüfung am echten Repository
wurde noch nicht ausgeführt.

## Laufzeit-Evidence

Keine. Es wird kein nativer Connector-Build, NGINX-Lauf oder nachfolgender
Laufzeitmatrix-Erfolg behauptet.

## Nicht ausgeführte Prüfungen

Der echte Kandidaten-Verifier nach Patchanwendung, die vollständige
CI-Security-Suite, die NGINX-/Evidence-Suite, Bilingual-/Link-Prüfungen
sowie die gehostete CI-/Sonar-Verifikation des aktuellen Heads stehen aus.
Ein lokaler Checkout war wegen fehlgeschlagener GitHub-DNS-Auflösung
nicht verfügbar. Auch der vorgeschriebene lokale RTK-Wrapper war nicht
vorhanden. Ein versuchter schreibender Vorbereitungsworkflow wurde
abgewiesen und nicht erstellt; er gehört nicht zu dieser Änderung.

## Bekannte Einschränkungen

Der Generator benötigt einen vorhandenen Parent-Checkout und einen
Framework-Klon mit beiden exakten Commits. Seine Integration mit den
echten Quelldateien ist noch ungeprüft. Bereits geänderte Zieldateien
werden absichtlich abgelehnt, statt fremde Arbeit zu vermischen.
Der aktuelle Produktionsworkflow lehnt den Kandidaten weiterhin ab,
bis der tatsächliche Patch angewendet wurde.

## Anwendung und Validierung

Den Task-Branch verwenden, fremde Änderungen erhalten und den unterstützten
Aufruf des installierten RTK-Wrappers verwenden. Die folgenden Befehle sind
native Befehlspayloads, keine Erlaubnis, den vorgeschriebenen Wrapper
wegzulassen. Das Ausgabeverzeichnis muss unter dem freigegebenen externen
Projektspeicher bereits existieren.

```sh
git submodule update --init -- modules/ModSecurity-test-Framework
git -C modules/ModSecurity-test-Framework fetch origin 0290a979ba4bc63a7abed175a53471367b385553
python3 ci/tools/prepare-reviewed-framework-handoff.py --repo-root "$PWD" --output /var/tmp/codex/ModSecurity-conector/reviewed-framework-handoff.patch
```

Den erzeugten Diff vor diesen ausdrücklichen Schreiboperationen prüfen:

```sh
git apply --index /var/tmp/codex/ModSecurity-conector/reviewed-framework-handoff.patch
git submodule update --init --checkout -- modules/ModSecurity-test-Framework
python3 ci/tools/verify-framework-candidate-contract.py --repo-root "$PWD" --candidate-sha 0290a979ba4bc63a7abed175a53471367b385553 --framework-common "$PWD/modules/ModSecurity-test-Framework/ci/lib/common.sh"
python3 -m unittest -v tests.test_prepare_reviewed_framework_handoff
make check-ci-security-contract
python3 -m unittest -v tests.test_nginx_exact_head_gate_contract tests.test_nginx_body_buffer_fixture tests.test_prepare_runtime_components tests.test_runtime_component_cache_identity tests.test_runtime_component_cache_contract tests.test_runtime_env_snapshot_contract tests.test_report_presentation_literals tests.test_evidence_output_security tests.test_nginx_functional_evidence
make check-bilingual-docs
make check-doc-links
git diff --cached --check
```

Den gestagten Diff prüfen, nur Task-Änderungen auf dem Task-Branch committen,
diesen Record mit tatsächlichen Ergebnissen aktualisieren und den exakten
nachfolgenden PR-Head verifizieren, bevor die Reparatur als abgeschlossen
gilt. Ein Merge ist nicht autorisiert.

## Restrisiken

Der Reparaturablauf kann bei der Ausführung am echten Checkout weitere
Integrationsfehler sichtbar machen. Erfolgreiche Unit-Tests beseitigen
diese Unsicherheit nicht. Die Vorbereitung darf nicht mit einem angewendeten
oder vollständig verifizierten Fix verwechselt werden.

## Abschließender Review-Status

Diagnose und Offline-Generator-Tests sind durch beobachtete Evidence gestützt.
Produktive Anwendung, vollständige Validierung und Behebung des ursprünglichen
CI-Fehlers stehen weiterhin aus.
