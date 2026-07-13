# TODO – Neuer Connector aus Vorlage

**Sprache:** [English](TODO.md) | Deutsch

Status: geeignete Scaffold-Vorlage, nicht runtime-verifiziert

Template-Bewertung: geeignet als Scaffold-Vorlage, nicht runtime-verifiziert

Begründung: Die Vorlage beschreibt einen wiederholbaren Connector-Ablauf und
eignet sich als Scaffold. Sie ist bewusst keine produktive Connector-
Implementierung und nicht runtime-verifiziert. Origin, Metadata, Build, No-CRS,
With-CRS, Coverage Matrix, Runtime Evidence und Promotion Evidence sind für
jeden Connector erforderlich.

Legende:

- [x] erledigt / durch Template-Dateien belegt
- [ ] offen / muss für einen konkreten Connector beantwortet werden
- [ ] blockiert / kann ohne Connector-Quellcode, Build-Artefakte oder
      Runtime-Setup nicht geprüft werden
- [ ] nicht verifiziert / keine ausreichende Runtime-Evidence

Statusvokabular:

- `template`: allgemeiner Ausgangspunkt, keine Implementierung.
- `scaffolded`: Struktur ist vorhanden, aber keine Repository-gestützte
  Adapter-Implementierung ist belegt.
- `adapter-owned`: produktiver Connector-Code liegt mit Provenance und Metadata
  im Connector-Baum.
- `runtime-smoke-verified`: nur bestimmte Smoke-Fälle mit aufgezeichnetem
  Befehl und Ergebnis sind verifiziert.
- `crs-verified`: With-CRS-Target oder Case-Claim besitzt aufgezeichneten
  Befehl, CRS-Evidence und Ergebnis.
- `partial`: Struktur oder partielle Runtime-Evidence ist vorhanden, aber eine
  vollständige Validierung ist nicht belegt.
- `not-verified`: unzureichende Runtime-Evidence.

## Phase 0: Scaffold erstellen

Status: für das allgemeine Scaffold vollständig.

- [x] `README.md` vorhanden.
- [x] `TODO.md` vorhanden.
- [x] Kanonischer Vertrag für neue Connectoren vorhanden.
- [x] `harness/README.md` vorhanden.
- [x] `src/README.md` vorhanden.
- [x] Lokaler Template-Testordner ist entfernt.
- [x] Template warnt, dass es keine produktive Implementierung ist.
- [x] Keine Runtime-Claims im Template.
- [ ] Connector-namenspezifische Platzhalter je Connector ersetzt.

## Phase 1: Origin/Metadata belegen

Status: für jeden Connector erforderlich.

Dies ist kein Template-Defekt. Jeder konkrete Connector muss Origin-, Lizenz-,
Source-Map- und Metadata-Evidence bereitstellen, bevor er über ein Scaffold
hinaus bewertet werden kann.

Metadata-Checkliste:

- [ ] `metadata.*` angelegt.
- [ ] Connector-Name eindeutig.
- [ ] Upstream-Projekt/Version dokumentiert.
- [ ] Build-Modus dokumentiert.
- [ ] Maintainer/Ownership dokumentiert.

Origin-/Lizenz-Checkliste:

- [ ] `ORIGIN.md` angelegt.
- [ ] Upstream-Quelle dokumentiert.
- [ ] Lizenz dokumentiert.
- [ ] importierte Dateien dokumentiert.
- [ ] lokale Änderungen dokumentiert.
- [ ] `SOURCE_MAP.json` oder eine gleichwertige Provenance-Datei ausgefüllt.

Blockiert, bis Evidence vorliegt:

- [ ] `adapter-owned` erst markieren, wenn Evidence zu Quellcode, Build,
      Metadata und Origin vorhanden ist.
- [ ] Wenn ein Quellcode, eine Lizenz oder eine Version fehlt,
      `Nicht im Repository gefunden` schreiben.

## Phase 2: Build integrieren

Status: blockiert, bis ein konkreter Connector-Build vorhanden ist.

Build-Checkliste:

- [ ] Build-Befehl dokumentiert.
- [ ] Include-Pfade dokumentiert.
- [ ] Library-Pfade dokumentiert.
- [ ] Build-Artefakte dokumentiert.
- [ ] Build-Log-Pfad dokumentiert.
- [ ] Clean/Refresh-Verhalten dokumentiert.
- [ ] Externe Abhängigkeitsversion bzw. Pin dokumentiert, falls gefunden.

Blockierte Punkte:

- [ ] SDK für Servermodul/Plugin identifiziert.
- [ ] Build-Ausgabe bleibt unter dem dokumentierten `BUILD_ROOT`.
- [ ] Reproduzierbarer lokaler Build-Befehl endet mit Exit-Code 0.
- [ ] Compiler-/Linker-Logs geprüft.

## Phase 3: No-CRS Runtime validieren

Status: auf das Template nicht anwendbar; für jeden Connector erforderlich.

- [ ] `make test-no-crs` ausgeführt, falls das Target vorhanden ist.
- [ ] Connector-spezifisches Smoke-Target ausgeführt, falls vorhanden.
- [ ] Befehl, Exit-Code und Umgebung dokumentiert.
- [ ] PASS/FAIL/BLOCKED-Zählungen dokumentiert.
- [ ] Summary-JSON-Pfade dokumentiert.
- [ ] `phase1_header_block` oder ein gleichwertiger Phase-1-Case dokumentiert.
- [ ] Blockierung von Request-Bodies dokumentiert.
- [ ] Blockierung von Response-Headers dokumentiert, sofern vom Framework
      unterstützt.
- [ ] Negativer Pass-through-Case dokumentiert.
- [ ] Audit-/Log-Evidence dokumentiert.

Ein No-CRS-PASS darf nicht als With-CRS-PASS verwendet werden.

## Phase 4: With-CRS Runtime validieren

Status: auf das Template nicht anwendbar; für jeden Connector erforderlich.

- [ ] `make test-with-crs` ausgeführt, falls das Target vorhanden ist.
- [ ] CRS-Quellpfad dokumentiert.
- [ ] CRS-Runtime-Preamble-Pfad dokumentiert.
- [ ] CRS-Loaded-/Effective-Evidence dokumentiert.
- [ ] CRS-spezifisches Case-Ergebnis dokumentiert.
- [ ] PASS/FAIL/BLOCKED-Zählungen dokumentiert.
- [ ] Summary-JSON-Pfade dokumentiert.
- [ ] Cases mit unterschiedlichen No-CRS-/With-CRS-Erwartungen als
      variantenspezifische Erwartungen dokumentiert.

Eine grundlegende No-CRS-Erwartung nicht ändern, um ein With-CRS-Ergebnis zu
erfüllen.

## Phase 5: Coverage Matrix ausfüllen

Status: Scaffold-Vertrag dokumentiert; Ausfüllung der Matrix für jeden
Connector erforderlich.

- [ ] Spalte für vorhandene Framework-Cases ausgefüllt.
- [ ] No-CRS-Statusspalte ausgefüllt.
- [ ] With-CRS-Statusspalte ausgefüllt.
- [ ] Spalte für Evidence-Pfad ausgefüllt.
- [ ] Entscheidungsspalte ausgefüllt.
- [ ] Phase-1-Zeile ausgefüllt.
- [ ] Phase-2-Zeile ausgefüllt.
- [ ] Phase-3-Zeile ausgefüllt.
- [ ] Phase-4-Zeile ausgefüllt.
- [ ] RESPONSE_BODY-Gate ausgefüllt.
- [ ] Negativ-/Pass-through-Gate ausgefüllt.
- [ ] Audit-/Log-Gate ausgefüllt.
- [ ] Start-/Reload-Validation-Gate ausgefüllt.
- [ ] Promotion-Gate ausgefüllt.

Generierte Coverage ist Planungs-Evidence. Sie ist für sich kein Runtime-Nachweis.

## Phase 6: Promotion prüfen

Status: Runtime-Promotion-Gates für jeden Connector erforderlich.

- [ ] `scaffolded`: Struktur und Docs vorhanden, keine Runtime-Claims.
- [ ] `adapter-owned`: Source-/Build-/Metadata-/Origin-Evidence vorhanden.
- [ ] `runtime-smoke-verified`: aktueller No-CRS- und Connector-Smoke-PASS für
      den beanspruchten Scope mit Befehls- und Ergebnispfaden.
- [ ] `crs-verified`: aktueller With-CRS-PASS für den beanspruchten Scope;
      CRS-Evidence und CRS-spezifische Erwartungen dokumentiert.
- [ ] `more-than-partial`: vollständige Mindestmatrix ohne offene
      FAIL-/BLOCKED-Zeilen dokumentiert.

Mehr als `partial` erfordert:

- [ ] No-CRS-PASS.
- [ ] With-CRS-PASS.
- [ ] Mindestmatrix für Phase 1/2/3/4 PASS.
- [ ] Negativ-/Pass-through-PASS.
- [ ] Audit-/Log-Evidence vorhanden.
- [ ] RESPONSE_BODY-Blockierung verifiziert oder ausdrücklich als nicht
      unterstützt bzw. bekannter Gap mit Evidence dokumentiert.
- [ ] Start-/Reload-Validation dokumentiert.

RESPONSE_BODY-Blockierung ist ein Runtime-Promotion-Gate. Sie ist kein
Template-Fehler. Konkrete Connectoren dürfen sie erst nach einem
Repository-gestützten Runtime-Test als verifiziert markieren, der einen
blockierenden Response-Body-Trigger und ein Blockierungsergebnis belegt.

## Phase 7: Offene Gaps dokumentieren

Status: für jeden Connector erforderlich.

- [ ] Fehlende Upstream-/Source-/License-Evidence dokumentiert.
- [ ] Fehlende Metadata dokumentiert.
- [ ] Fehlende Build-Evidence dokumentiert.
- [ ] Fehlende No-CRS-Evidence dokumentiert.
- [ ] Fehlende With-CRS-Evidence dokumentiert.
- [ ] Jede FAIL-/BLOCKED-Zeile dokumentiert, ohne sie als PASS umzuklassifizieren.
- [ ] RESPONSE_BODY-Blockierung bleibt `not-verified`, bis Mindest-Evidence
      vorhanden ist.
- [ ] Nicht unterstütztes Verhalten mit Evidence dokumentiert.

## Externe Tests

- [x] Lokaler Template-Testordner entfernt.
- [x] Neue Connectoren dürfen `connectors/<name>/tests` nicht erstellen.
- [x] Ausführbare Tests sind bewusst extern und dem Framework zugeordnet.
- [x] Tests müssen referenziert und dürfen nicht nach
      `connectors/_template/tests` kopiert werden.
- [x] Framework-Testpfade dokumentiert:
      `modules/ModSecurity-test-Framework/tests/cases/`,
      `modules/ModSecurity-test-Framework/tests/cases/connector-specific/<connector>/`,
      `modules/ModSecurity-test-Framework/tests/runners/case_cli.py`.

## Abschließende Template-Entscheidung

Das Template ist als Scaffold-Vorlage geeignet. Es ist bewusst nicht
runtime-verifiziert und enthält keine produktive Connector-Implementierung.
Neue Connectoren müssen die Connector-spezifischen Gates für Origin, Metadata,
Build, No-CRS, With-CRS, Coverage Matrix und Runtime Evidence erfüllen, bevor
sie über partial hinaus bewertet werden können.

## Vollständige Bewertung

Die wiederverwendbaren Template-Anforderungen sind in
`docs/connectors/README.md` zusammengefasst; Runtime-Promotion erfordert
weiterhin einen Connector-spezifischen Evidence-Run.
