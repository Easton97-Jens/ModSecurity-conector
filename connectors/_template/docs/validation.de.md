# Validierung – Connector-Vorlage

**Sprache:** [English](validation.md) | Deutsch

## Prinzip

Dateistruktur, generierte Abdeckung oder ein erfolgreicher Build sind nicht laufzeitabhängig
Überprüfung. Ein Connector wird nur für den genauen Befehl zur Laufzeit überprüft.
Umfang, Fälle und Ergebnisdateien, die ausgeführt und aufgezeichnet wurden.

## Erforderlicher Laufzeitnachweis

- [ ] Befehl
- [ ] Umgebung
- [ ] Exit-Code
- [ ] Anschlussumfang
- [ ] PASS/FAIL/BLOCKED zählt
- [ ] Zusammenfassung der JSON-Pfade
- [ ] pro Fall erwarteter und tatsächlicher Status für beanspruchte Fälle
- [ ] relevante Protokolle oder Prüfungsnachweise
- [ ] nicht aufgelöste FAIL/BLOCKED-Zeilen dokumentiert

## No-CRS-Validierung

Notieren Sie den konkreten Befehl, zum Beispiel:

```sh
SOURCE_ROOT=<path> BUILD_ROOT=<path> REFRESH=1 make test-no-crs
```

No-CRS-Ansprüche müssen Zählungen und Zusammenfassungspfade für den beanspruchten Connector enthalten.

## With-CRS-Validierung

Notieren Sie den konkreten Befehl, zum Beispiel:

```sh
SOURCE_ROOT=<path> BUILD_ROOT=<path> REFRESH=1 make test-with-crs
```

With-CRS-Ansprüche müssen den CRS-Quellpfad, den CRS-Präambelpfad, die Anzahl und die Zusammenfassung enthalten
Pfade und CRS-spezifische Fallbeweise. Ein With-CRS-Fall erfordert möglicherweise eine
variantenspezifische Erwartung; Ändern Sie nicht eine grundlegende No-CRS-Erwartung, um eine zu stellen
Mit-CRS-Laufpass.

## RESPONSE_BODY blockiert minimale Beweise

Die RESPONSE_BODY-Blockierung bleibt `not-verified` bestehen, bis alle folgenden Aktionen ausgeführt werden
vorhanden:

- [] Repository-gestützter Laufzeittestfall im Framework
- [ ] erwarteter blockierender Response-Body-Trigger
- [ ] tatsächliches Blockierungsergebnis, z. B. HTTP 403
- [ ] Beweise protokollieren/melden
- [ ] Befehl ausgeführt
- [ ] betroffener Anschluss
- [ ] Apache und NGINX separat dokumentiert, wenn ein gemeinsamer Anspruch geltend gemacht wird

Pass-Through- oder Log-Only-Response-Body-Beweise beweisen keine Blockierung.

## Mindestmatrix für mehr als `partial`

- [ ] `phase1_header_block`
- [ ] Blockierung des Anfragetextes
- [ ] Antwort-Header-Blockierung, wenn Framework-unterstützt
- [ ] Blockierung des Antworttextes
- [ ] Audit-/Protokollnachweise
- [ ] Start-/Neuladevalidierung
- [ ] Negativ-/Durchgangsfall
- [ ] No-CRS- und With-CRS-Ergebnisse separat dokumentiert
- [ ] keine ungelöste FAIL/BLOCKED-Zeile in der beanspruchten Mindestmatrix

## Nicht ausreichend

- Nur Datei- oder Ordnerexistenz
- nur statische Flusen
- nur generierte Deckung
- Nur Erfolg aufbauen
- Kein-CRS-Beweis wird als Mit-CRS-Beweis verwendet
- PASS für einen Fall, der als PASS für ein ganzes Ziel verwendet wird
