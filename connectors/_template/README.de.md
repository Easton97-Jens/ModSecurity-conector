# Connector-Vorlage

**Sprache:** [English](README.md) | Deutsch


Status:

- Vorlage: ja
- eingerüstet: ja
- geeignet_scaffold: ja
- umgesetzt: nein
- build_verified: nein
- runtime_verified: nein
- befördert: nein

## Zweck

Dieses Verzeichnis ist ein wiederholbares Dokumentationsgerüst für die Zukunft
`connectors/<name>/`-Implementierungen. Es beschreibt, was ein neuer Connector haben muss
ausfüllen, bevor es Build- oder Laufzeitverhalten beanspruchen kann.

Es handelt sich nicht um eine produktive Connector-Implementierung. Es enthält absichtlich nein
produktiver Adaptercode, keine lokale Testsuite und keine serverspezifische Laufzeit
Ansprüche.

Vorlagenstatus: geeignetes Gerüst, nicht laufzeitverifiziert.

Deutsch: geeignet als Scaffold-Vorlage, nicht runtime-verifiziert.

## Wann diese Vorlage verwendet werden sollte

Verwenden Sie diese Vorlage, wenn Sie einen neuen Connector-Baum erstellen, der noch benötigt wird
Repository-gestützte Beweise für Herkunft, Metadaten, Build-Integration, Laufzeit
Verhalten und Beförderungsstatus.

Verwenden Sie diese Vorlage nicht, um zu behaupten, dass es sich um Apache, NGINX oder einen anderen Connector handelt
Das Verhalten ist automatisch auf einen neuen Server übertragbar. Serverlebenszyklus, Hook
Modell, Anforderungs-/Antwortkörperverarbeitung, Protokollierung und Interventionszuordnung müssen erforderlich sein
für jeden Connector nachgewiesen werden.

## Dateien, die für einen neuen Connector erstellt werden sollen

Kopieren Sie diese Struktur nach `connectors/<name>/` und ersetzen Sie nur Platzhalter
mit Beweisen, die im Repository gefunden oder durch ausgeführte Befehle erzeugt wurden:

```text
connectors/<name>/
|-- README.md
|-- TODO.md
|-- ORIGIN.md
|-- SOURCE_MAP.json
|-- metadata.c or metadata.*
|-- docs/
|   |-- architecture.md
|   |-- build.md
|   |-- coverage-decision-matrix.md
|   `-- validation.md
|-- harness/
|   `-- README.md
`-- src/
    `-- README.md
```

Erstellen Sie nicht `connectors/<name>/tests`. Ausführbare Connector-Tests sind
Framework-eigene, nicht Connector-lokale.

## Erforderliche Metadaten

Pro Connector erforderlich. Dies ist kein Template-Defekt. Jeder neue Connector muss
Erstellen Sie `metadata.*` oder die von diesem Repository erwartete Metadatenform.

- [ ] `metadata.*` erstellt.
- [ ] Connector-Name ist eindeutig.
- [ ] Upstream-Projekt und Version dokumentiert.
- [ ] Build-Modus dokumentiert.
- [ ] Betreuer oder Eigentum dokumentiert.
- [ ] Statusvokabular wird konsequent verwendet.

## Erforderlicher Herkunfts-/Lizenznachweis

Pro Connector erforderlich. Dies ist kein Template-Defekt. Jeder neue Connector muss
Dokument `ORIGIN.md`, Lizenz-/Herkunftsnachweis und importierte Dateien.

- [ ] `ORIGIN.md` erstellt.
- [ ] Upstream-Quelle dokumentiert.
- [ ] Lizenz dokumentiert.
- [ ] Importierte Dateien dokumentiert.
- [ ] Lokale Änderungen dokumentiert.
- [ ] Quellkarte oder gleichwertige Provenienzdatei dokumentiert.

Es dürfen keine Upstream-Quellen, Dateien, Lizenzen oder Versionen erraten werden. Wenn nicht
gefunden, schreiben Sie `Nicht im Repository gefunden` oder lassen Sie das Element geöffnet.

## Erforderlicher Baunachweis

- [ ] Build-Befehl dokumentiert.
- [ ] Dokumentierte Pfade einschließen.
- [ ] Bibliothekspfade dokumentiert.
- [ ] Build-Artefakte dokumentiert.
- [ ] Build-Protokollpfad dokumentiert.
- [ ] Bereinigungs- oder Aktualisierungsverhalten dokumentiert.
- [ ] Externe Abhängigkeitsversionen oder Pins werden dokumentiert, wenn sie gefunden werden.

Ein Build-Anspruch erfordert den genauen Befehl, das Ergebnis und den Protokollpfad. Statische Datei
Anwesenheit allein ist keine Build-Verifizierung.

## Erforderlicher Laufzeitnachweis

Gilt nicht für die Vorlage. Laufzeitnachweise können nur durch Beton erbracht werden
Anschlüsse.

- [ ] `make test-no-crs` wird ausgeführt, wenn das Ziel existiert.
- [ ] `make test-with-crs` wird ausgeführt, wenn das Ziel existiert.
- [ ] `make smoke-common` wird ausgeführt, wenn das Ziel existiert.
- [ ] Apache/NGINX oder Connector-spezifischer Bereich dokumentiert.
- [ ] PASS/FAIL/BLOCKED-Zählungen dokumentiert.
- [ ] Zusammenfassung der JSON-Pfade dokumentiert.
- [ ] RESPONSE_BODY-Blockierung überprüft.
- [ ] Negativ/Durchgang geprüft.
- [ ] Audit-/Protokollnachweise überprüft.

Laufzeitansprüche erfordern ausgeführte Befehle und Ergebnisdateien. Generierte Abdeckung
Berichte können die Planung unterstützen, sie allein sind jedoch nicht laufzeitsicher.

Die RESPONSE_BODY-Blockierung ist ein Laufzeit-Promotion-Gate. Betonverbinder ggf
Markieren Sie es erst als verifiziert, nachdem Repository-gestützte Laufzeitnachweise beweisen, dass a
Blockierungsantwort-Body-Trigger und Blockierungsergebnis.

Der Harnessvertrag wird durch die Vorlage dokumentiert. Die Implementierung des Harnesss ist
pro Connector erforderlich.

## No-CRS-Validierung

Dokumentieren Sie für einen Betonverbinder den genauen No-CRS-Befehl und das Ergebnis:

```sh
SOURCE_ROOT=<path> BUILD_ROOT=<path> REFRESH=1 make test-no-crs
```

Aufnahme:

- Befehls- und Exit-Code
- Anschlussbereich
- PASS/FAIL/BLOCKED-Zählungen
- relevante erwartete und tatsächliche Status auf Fallebene
- Zusammenfassung der JSON-Pfade

Ein No-CRS-PASS bedeutet nicht, dass es sich um einen With-CRS-PASS handelt.

## With-CRS-Validierung

Dokumentieren Sie für einen Betonverbinder den genauen With-CRS-Befehl und das Ergebnis:

```sh
SOURCE_ROOT=<path> BUILD_ROOT=<path> REFRESH=1 make test-with-crs
```

Aufnahme:

- Befehls- und Exit-Code
- CRS-Quellpfad
- CRS-Laufzeit-Präambelpfad
- Anschlussbereich
- PASS/FAIL/BLOCKED-Zählungen
- CRS-spezifische Fallbeweise
- Zusammenfassung der JSON-Pfade

Wenn ein Fall im No-CRS- und With-CRS-Modus unterschiedliche gültige Erwartungen hat, wird der
Das Erwartungsmodell muss diese Varianten getrennt halten. Ändern Sie keine Basis
No-CRS-Erwartung, ein With-CRS-Ergebnis zu erfüllen.

## Deckungsentscheidungsmatrix

Jeder Betonverbinder muss `docs/coverage-decision-matrix.md` beibehalten.
Die Matrix muss trennen:

- Verfügbarkeit von Rahmenkoffern
- Kein CRS-Laufzeitergebnis
- With-CRS-Laufzeitergebnis
- Beweispfad
- Beförderungsentscheidung

Die Matrix muss mindestens Phase 1, Phase 2, Phase 3, Phase 4 abdecken.
RESPONSE_BODY-Blockierung, negatives/Pass-Through-Verhalten, Audit-/Protokollnachweise,
Start-/Neuladevalidierung und verbleibende FAIL/BLOCKED-Zeilen.

## Promotion-Tore

`scaffolded`:

- Struktur vorhanden
- Dokumentationsgrundlage vorhanden
- keine Laufzeitansprüche

`adapter-owned`:

- Quell-, Build-, Metadaten- und Ursprungsdateien sind vorhanden
- Provenienz und lokale Veränderungen werden dokumentiert

`runtime-smoke-verified`:

- aktueller `make test-no-crs` PASS für den beanspruchten Connector/Oszilloskop
- aktueller Connector Smoke PASS für den beanspruchten Connector/Zielfernrohr
- Befehls- und Ergebnispfade dokumentiert

`crs-verified`:

- aktueller `make test-with-crs` PASS für den beanspruchten Connector/Oszilloskop
- CRS geladen/wirksame Beweise dokumentiert
- CRS-spezifische Erwartungen dokumentiert

`more-than-partial`:

- Kein CRS-PASS
- Mit CRS-PASS
- Phase 1/2/3/4 Mindestmatrix PASS
- Negativ/Pass-Through-PASS
- Audit-/Protokollnachweise vorhanden
- RESPONSE_BODY-Blockierung verifiziert oder explizit als nicht unterstützt dokumentiert oder
  eine bekannte Lücke mit Beweisen
- Keine offenen FAIL/BLOCKED-Zeilen in der definierten Mindestmatrix

## Statusvokabular

- `template`: generischer Ausgangspunkt, keine Implementierung.
- `scaffolded`: Struktur vorhanden, keine Repository-gestützte Adapterimplementierung
  ist bewiesen.
- `adapter-owned`: Produktiver Connector-Code lebt im Connector-Baum mit
  Herkunft und Metadaten.
- `runtime-smoke-verified`: Nur bestimmte Smoke-Fälle mit aufgezeichnetem Befehl und
  Ergebnis überprüft werden.
- `crs-verified`: With-CRS-Ziel- oder Fallanspruch hat Befehl, CRS, aufgezeichnet
  Beweise und Ergebnis.
- `partial`: Struktur oder teilweiser Laufzeitnachweis vorhanden, aber vollständige Validierung
  ist nicht bewiesen.
- `not-verified`: Unzureichende Laufzeitnachweise.

## Was nicht beansprucht werden darf

- Behaupten Sie nicht, dass eine lokale `connectors/<name>/tests`-Suite existiert.
- Fordern Sie keinen Laufzeit-PASS ohne Befehl, Exit-Code und Ergebnispfad an.
- Beanspruchen Sie keinen With-CRS PASS aufgrund von No-CRS-Beweisen.
- Beanspruchen Sie keine RESPONSE_BODY-Blockierung von Pass-Through- oder Log-Only-Beweisen.
- Behaupten Sie nicht, dass ein Connector mehr als `partial` hat, solange die Mindestmatrix vorhanden ist
  unadressierte FAIL/BLOCKED-Zeilen.
- Erfinden Sie keine Upstream-Quellen, Lizenzen, Build-Flags, APIs, Tests usw
  Rahmenpfade.

## Externe Framework-Tests

Von der Connector-Dokumentation verwendete Repository-gestützte Framework-Pfade:

- `modules/ModSecurity-test-Framework/tests/cases/`
- `modules/ModSecurity-test-Framework/tests/cases/connector-specific/<connector>/`
- `modules/ModSecurity-test-Framework/tests/runners/case_cli.py`

Make-Ziele dürfen nur zitiert werden, wenn sie im übergeordneten Element `Makefile` vorhanden sind.
