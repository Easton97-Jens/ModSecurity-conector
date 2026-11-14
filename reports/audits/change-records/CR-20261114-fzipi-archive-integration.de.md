# Change Record: CR-20261114-fzipi-archive-integration

**Sprache:** [English](CR-20261114-fzipi-archive-integration.md) | Deutsch

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | CR-20261114-fzipi-archive-integration |
| Datum (UTC) | 2026-11-14 |
| Basis-Revision | `b1017969f766209eb9401820a4aca01d71180636` |

## Motivation und Problemstellung

Parent b1017969 wählte Framework 2cc331d8. Fünf Parent-Workflows stoppten am
veralteten generierten Testarchiv. Der vollständige lokale native Pfad zeigte
zusätzlich veraltete Apache-/HAProxy-Quellverträge und eine Common-Prüfung, die
Framework-Dateien getrennter Eigentümer als Parent-relative Pfade behandelte.
Der separate [Framework PR 173](https://github.com/Easton97-Jens/ModSecurity-test-Framework/pull/173)
repariert diese Verträge ohne Abschwächung ihrer Prüfungen.

## Akzeptanzkriterien

Verifizierten Framework-Master auswählen, Produktverhalten und alle anderen
Komponenten-/Tool-/Runtime-Versionen erhalten, 100 automatische Fälle und MRTS
unverändert lassen und native Publikationsrekonstruktion sowie neue Pin-Prüfungen
bestehen. Aktuelle Parent-CI und Sonar müssen vor der separat autorisierten
Master-Integration bestehen. Frühere Resultate qualifizieren keinen neuen Head.

## Implementierungsentscheidung und Begründung

Tatsächlichen Squash-Master `939d1718b7548a36ff7a550080ed8b811aad8a98` statt
PR-Head `c250f92d34e8e7f04304f54067d049acd3b76c3c` auswählen. Beide besitzen den
exakten Git-Tree `ddd24ee9293efeba21ee151b2439c4a1cb71a301`. Framework ändert
drei strikte Prüfer, vier Regressionsmodule, kanonisches Archiv und EN/DE-Nachweis.
Die Quellenbindungsprüfung meldet VERIFIED ohne Inventaränderung. Das Archiv
beschreibt 8211 Definitionen; diese werden dadurch nicht alle ausgewählt/ausgeführt.

Vorhandenen nativen Synchronizer mit fester Zielregistry verwenden. Eingabe ist
eine unveränderliche Git-Extraktion von Framework `ci/lib/common.sh`, SHA-256
`38be065c9214c1953cba6baec49c3cf3e7ae5a369dec61ba56e59b36be083f87`,
unter der erlaubten temporären Runner-Wurzel. Das Tool parst sie als Daten und
führt sie niemals aus. Zwei anfängliche Validierungen lehnten Checkout-Pfade
außerhalb dieser Wurzel mit Exit 2 ab. Der dokumentierte extrahierte Snapshot
bestand unveränderte Kontrollen; Eingabegrenzen und Prüfer bleiben unverändert.

## Geänderte Dateien

Framework-Gitlink, Parent-Projektversions-Lock, 22 generierte Workflow-Projektionen
und dieses neue EN/DE-Nachweispaar: 26 Pfade. Keine Parent-Produktquellen oder
MRTS-Inhalte geändert. Framework-Implementierung/Tests wurden separat mit PR173 geliefert.

## Ausgeführte Befehle

Tatsächlicher Shell-Einstieg: `rtk bypass python3`, danach `rtk bypass bash -c`
mit externem Archive-pin-`context.sh`, danach folgende RTK-Kindbefehle mit dem
konfigurierten Framework-Python. Kontext bindet Parent b1017969, Framework939d1718,
Profil h1, explizite Wurzeln und externe Ausgabe-/Build-/Temp-/Logverzeichnisse.

- `ci/tools/sync-framework-component-versions.py --validate`: 0 vor/nach Sync.
- Dasselbe Tool `--sync` und `--check`: 0 / 0. Eingaben: extrahierter Common-
  Snapshot, exakter Framework-SHA, vorhandenes read-only Framework-Objektrepo und
  explizit unveränderter MRTS-SHA `ee2174431c4edf97e66afe32558ce8454deb2397`.
- Natives `ci/tools/new-change-record.py create --name fzipi-archive-integration --base-revision b1017969f766209eb9401820a4aca01d71180636 --date 2026-11-14`: 0.

Native `--verify-primary --base b1017969f766209eb9401820a4aca01d71180636`,
`rtk make check-active-inventory` und vollständiger `rtk make quick-check` bestanden
(0). Der vollständige Quick-check-Log mit 660705 Bytes wurde vor Einsicht in
begrenzten überlappenden Abschnitten mit Secrets geprüft: echte Apache-/NGINX-/
HAProxy-C17-Kompilierung, Common-Sicherheit, Dokumentation sowie finale Syntax-/
Whitespace-Schritte bestanden. Alle 23 bestehenden regulären Projektionen sind
gegenüber der vertrauenswürdigen Basis ausschließlich im exakten Framework-SHA
geändert; alle übrigen Komponenten-/Tool-/Runtime-Bytes bleiben gleich. Finale
Nachweis-/Archiv- und Indexprüfungen erfolgen separat vor Commit.

## Security-Auswirkung

Strikte Zähler-/native Aufrufprüfungen und vollständiger Common-Scanumfang bleiben
erhalten. Keine Regelunterdrückung, Warnungsabschwächung, Gate-Änderung oder WAF-
Ausnahme. Frühere exakte Operatorfreigaben gelten für andere Indizes/Framework-
Commits und werden nicht übertragen. Erforderliche neue Zulassung bleibt separat.

## Runtime-Evidence

Externe Framework-Evidenz: 71 gezielte Tests und vollständiger nativer Quick-check
bestanden vor Veröffentlichung. Alle neun Framework-PR-Head-Workflows bestanden (sieben PR- und zwei Push-Läufe).
Vollständiger Sonar-Log bindet SCM c250f92d, terminales Gate PASSED und EXECUTION
SUCCESS; vollständige PR173-API-Abfragen: null unaufgelöste Issues, null Hotspots
in beiden Review-Zuständen, Gate OK, 0,0 % neue Duplikation. Autoritativer Merge/
Master und Tree-Gleichheit verifiziert. Dies sind Framework-Auslieferungsresultate,
keine neue Parent-CI oder Host-Runtime. Kein neuer Host-Laufzeitlauf für diese Pinänderung.

## Bekannte Einschränkungen

Archivverfügbarkeit ist keine Ausführung von 8211 Definitionen. Strikte statische
Verträge sind keine allgemeinen C-Erreichbarkeits- oder vollständigen Hostnachweise.
Neue lokale Parent-Prüfungen bestanden; aktuelle entfernte Auslieferungsevidenz
steht aus. Die anschließende Framework-Master-Analyse ist separat fehlgeschlagen:
115 bestehende Issues (32 Sicherheitsmeldungen, 83 Code Smells), alle vor diesem
Auftrag angelegt, keiner in PR173 geänderten Dateien. Der Nutzer wählte ausdrücklich
Auftragsänderungen auf null und Altfunde separat. Keine Regel, Gate-Einstellung,
Befunddisposition oder Basis wurde zum Verbergen dieses Resultats geändert.

## Verbleibende Risiken

Ein geänderter Index oder Framework-Zielcommit entwertet einen exakten Operatorplan.
Parent-Merge bleibt an aktuelle Prüfungen und erforderliche exakte Zulassung
gebunden; keine frühere Zulassung wird erweitert oder anders wiederverwendet.

## Nicht ausgeführte Prüfungen mit Begründung

Kein neuer Parent-Commit, CI- oder Master-Merge beansprucht. Lokale neue Pin-Prüfungen
bestanden; finale Nachweis-/Indexverifikation und exakte Zulassung stehen aus. MRTS bleibt beim obigen unveränderten SHA
read-only; keine Initialisierung, Aktualisierung, Checkout oder Vollmaterialisierung.

## Finaler Diff- und Review-Status

Kanonische Scaffold-Identität, Datum und Basis erhalten. Nativer Sync/Check,
Arbeitsbaum-Primärverifikation, Inventar und vollständiger Quick-check bestanden.
Bestehende reguläre Projektionen als reine SHA-Ersetzungen geprüft. Nachweisprüfung,
Indexverifikation und exakte Zulassung folgen vor regulärem Commit/Push; aktuelle
Parent-CI/Sonar bleiben vor autorisierter Master-Integration verpflichtend.
