# Change Record: Apache-Phase-4-Response-Enforcement

**Status:** PR #60 ist weiterhin offen und Draft. Sein Remote-Head ist
`7c83583b4e208b8945daeec226d04abe364cbc8e`. Der lokale Delivery-Kandidat
basiert auf dem normalen Current-Master-Merge
`93c5f30c181710f5c2cecf207fb92aaecb215035` und enthält ungepushte fokussierte
Parent-Remediation. Historische Remote-Checks gelten nur für
`7c83583b4e208b8945daeec226d04abe364cbc8e`, nicht für den lokalen Kandidaten.
Die aktuelle Exact-Native-Validierung ist bestanden, aber Exact-Pushed-Head-CI,
CodeQL, SonarCloud, Review-, Thread- und Protected-Merge-Checks bleiben
erforderlich. Ein Merge wird nicht behauptet.

**Sprache:** Deutsch | [English](CR-20260718-apache-phase4-response.md)

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | CR-20260718-apache-phase4-response |
| Datum (UTC) | 2026-07-18; aktuelle Evidence am 2026-07-19 erneuert |
| Basisrevision | aabde81a9a315bf3e494e595ab0399357c596f9c |
| Scope | Nur Parent-Repository |
| Zugehöriger Finding | FND-PARENT-0038 |
| Zugehöriger Harness-Finding | FND-PARENT-0041 |
| Zugehöriger Kapazitäts-Finding | FND-PARENT-0042 (lokal fixed; Delivery-Verifikation ausstehend) |
| Framework-/MRTS-Zustand | Parent-Gitlink `cdc91a398d6c156eaff927d742b23018a3817fb6`; MRTS-Gitlink `13aa91291adea12d5c607fdd165d010fcfb1da78`; keine Framework-, MRTS- oder Gitlink-Änderung |

## Problem und Sicherheitsinvariante

Apache darf kein Byte freigeben, das Phase 4 berücksichtigen kann, bevor
`msc_process_response_body` und seine Intervention entschieden haben. Ein
normaler interner Redirect kann die native Transaction außerdem nicht sicher
an Ziel-URI, Regeln oder Request-Variablen binden. Daher darf ein unsicherer
Redirect weder die geschützte Response freigeben noch einen Ziel-Quick-Handler
oder normalen Ziel-Handler ausführen.

Der einzige erlaubte Redirect ist ein begrenzter lokaler `ErrorDocument`-
Übergang: Apache-Core-abgeleitete `no_local_copy`- und `REDIRECT_STATUS`-
Evidence müssen übereinstimmen, der gemeinsame Phase-4-Zustand muss
`EMITTING` sein, und die einmalige Erlaubnis wird an die frische Notes-Tabelle
genau dieses Requests gebunden.

## Aktuelle Implementierung

- `MODSECURITY_OUT` hält jede Pre-EOS-Response-Brigade zurück und normalisiert
  sie, trifft die Phase-4-Entscheidung bei EOS und führt genau einen
  Downstream-Release aus.
- `MODSECURITY_PHASE4_GUARD` bleibt in der Protocol-Chain, um spätere
  Producer-Output nach Deny, EOS oder terminalem Fehler zu versiegeln.
- Die Redirect-Remediation ergänzt einen `APR_HOOK_REALLY_FIRST`-
  Quick-Handler-Guard, bevor Apache einen Ziel-Quick-Handler ausführen kann,
  sowie einen ebenso frühen Fallback für normale Handler. Beide geben für
  einen unsicheren `r->prev`-Request `DONE` zurück.
- Der Source setzt eine request-lokale Permission-Note erst, nachdem der
  bestehende Core-geformte lokale-`ErrorDocument`-Proof erfolgreich ist. Ein
  späterer verschachtelter oder normaler Redirect erhält eine neue
  Notes-Tabelle und kann diese Erlaubnis nicht erben.
- Um neben den Payload-Bytes auch den Aufwand zurückgehaltener APR-Objekte/
  Setaside zu begrenzen, zählt sie normalisierte Buckets über Filter-Aufrufe
  hinweg; bei 4.096 gehaltenen Buckets schlägt sie fail-closed fehl, bevor ein
  weiterer Bucket zurückgehalten wird, und setzt den Zähler bei Release oder
  Verwerfen zurück.
- Keine Framework-, MRTS- oder Gitlink-Änderung ist Teil dieser Reparatur.

## Aktuelle Exact-Native-Evidence

Die task-eigene externe read-only Kopie des vom Parent referenzierten
Framework-Commits `cdc91a398d6c156eaff927d742b23018a3817fb6` baute die
Apache-Connector-Komponente
`904cb576c6a344cb38f330d5842fe750fafc81041c459ce0dfcda4a75eabfbc3`.

Der erste exakte Target-Handler-Control reproduzierte den unvollständigen
Redirect-Abschluss: Sein H1-Lauf endete mit `1`, und das aufbewahrte Log
enthielt sowohl die Connector-Ablehnung als auch
`ModSecurity Phase4 redirect target handler executed`. Die fokussierte
Source-Reparatur wurde danach gegen dieselbe exakte Framework-Revision neu
gebaut.

Die Post-Fix-Controls `redirect-target-handler-abort-h1` und
`redirect-target-handler-abort-h2` bestanden beide. Ihre Logs enthalten die
erwartete Connector-Ablehnung und keinen Target-Handler-Marker. Danach endete
eine serielle exakte Native-Matrix mit 30 Controls mit `0`; sie deckte Deny,
Allow, log-only, Client-Abort, leere Responses, Body-Limits, Custom-MIME,
ProcessPartial, Redirect-Ablehnung, Target-Configuration- und URI-Varianten,
Target-Handler H1/H2, Upstream-/Downstream-/Nested-/Pre-Output-`ErrorDocument`
sowie H1/H2-Late-Producer- und Phase-3-Header-Controls ab.

Die finale lokale Security-Diff-Validierung reproduzierte zusätzlich eine
eigenständige Verfügbarkeitsbedingung: Vor der fokussierten Kapazitätsreparatur
gab ein echter Apache-Handler 4.097 Ein-Byte-Response-Buckets (4.097 Bytes,
weit unter dem Ein-MiB-Payload-Limit) als HTTP 200 frei. Das aktuell neu
gebaute Modul lehnt dieselben 4.097 über zwei Filteraufrufe aufgeteilten
Buckets mit einem Pre-Release-HTTP-500 und einer spezifischen
Bucket-Limit-Diagnose ab. Seine Grenze aus 4.095 Daten-Buckets plus EOS gibt
HTTP 200 mit exakt 4.095 Bytes frei. Die serielle sichere Matrix lief mit
diesen beiden neuen Controls erneut und bestand alle 32 Modi.

Der frühere versiegelte Redirect-Receipt mit 30 Modi ist
`/var/tmp/codex/ModSecurity-conector/runs/20260719T162259Z-pr60-exact-head-revalidation-dfba422e/evidence/pr60-exact-native-phase4-manifest.json`
mit SHA-256
`1f44c2817676ef2952f70573917657d67645d8d85d57e829a47c9d67ee2ea548`.
Er dokumentiert Pre-Fix-Log, Post-Fix-H1/H2-Logs, Component-Manifest, neu
gebautes Modul, Command-Result, Source-Zustand und seinen 30-Modus-Matrix-
Scope.

Die aufbewahrte lokale Security-Diff-Validierung für den Bucket-Rerun mit 32
Modi ist
`/var/tmp/codex/ModSecurity-conector/runs/20260719T183551Z-pr60-final-security-diff-93404fdd/evidence/security-diff/artifacts/05_findings/CAND-PR60-001/validation_report.md`
mit SHA-256
`79e7e1b3fcca6acdf8d02ed941eaadcea566258656abe269a54289a59e88db8c`.
Sie dokumentiert die Split-Overflow- und Boundary-Logs sowie den 32-Modus-
Matrix-Driver; sie ist aufbewahrte lokale Validierung, kein versiegelter
Receipt.

Auch die fokussierte statische Validierung bestand:

- `tests.test_apache_phase4_response_regression_wiring`: 10/10;
- Shell-Syntax für Phase-4-Runner und Apache-Harness;
- `git diff --check`; und
- ein vollständiger uninstalled Apache-Module-Build gegen die exakten Apache-,
  APR- und libModSecurity-Header.

## Evidence-Grenzen und verbleibende Delivery-Gates

Historische Runtime-Beobachtungen früherer Heads sind keine aktuelle
Exact-Head-Evidence: zentrale Artefakte fehlten oder waren unversiegelt und
bleiben nur in FND-PARENT-0038 beschrieben. Die aktuelle Matrix ist das
maßgebliche lokale Native-Resultat.

Es gibt keine repository-native Apache-Phase-4-ASan/UBSan-Route; der Common-
Allocator-Micro-Smoke wird nicht als Apache-Sanitizer-Evidence dargestellt.
Der CRS-Control ist durch den aktuellen Framework-Provenance-Guard blockiert,
nachdem er `.gitmodules` der genehmigten Source erkennt; dieser Control wurde
nicht umgangen. Das MRTS-Profil wird nicht als aktuell bestanden behauptet,
bis es aus einer task-eigenen read-only Materialisierung läuft.

Bevor PR #60 ready oder gemergt werden kann, benötigt der finale lokale Diff
einen frischen Codex-Security-Diff-Scan, und der gepushte Exact-Head benötigt
terminale Required Checks, CodeQL, SonarCloud, Review-/Thread-Evidence,
Protected Merge und Resulting-Master-Verifikation. Der Nutzer autorisierte
sichere Master-Integration, keinen Bypass dieser Gates.
