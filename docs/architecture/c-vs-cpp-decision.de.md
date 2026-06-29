# Entscheidung zwischen C und C++

**Sprache:** [English](c-vs-cpp-decision.md) | Deutsch

Status: für die aktuellen Connector-Refactoring-Phasen akzeptiert.

## Entscheidung

Die öffentliche gemeinsame Connector-API bleibt C-first.

Das Repository kann dünne C++-Header-Wrapper über C-Strukturen bereitstellen und verwenden
C++ für Build-Tools, Test-Tools oder optionale Hilfsprogramme. Produktiv
Apache-, NGINX- und zukünftige Server-Connector-Kerne dürfen nicht nach C++ portiert werden
Teil des gemeinsamen Refaktors.

## Begründung

– libmodsecurity v3 ist hier über seine öffentliche C-API integriert.
– Der importierte Apache-Connector ist C-orientiert und wird über APXS/Autotools. erstellt
- NGINX-Module sind C-Module und überschreiten Server-ABI-Grenzen direkt.
– C++ würde die ABI- und Linker-Komplexität zu den Ladepfaden von Servermodulen erhöhen.
– Der HAProxy SPOA/SPOP-Runtimepfad und zukünftige Lighttpd-Integrationen sind
wird voraussichtlich in der Nähe von C bleiben.

## Zulässige C++-Nutzung

- Dünne `.hpp`-Aliase um C-Strukturen herum.
- Dienstprogramme erstellen und testen.
- Optionale Hilfsprogramme, die die ABI-Grenzen des Servermoduls nicht überschreiten.

## Unzulässige Verwendung von C++

- Portierung des produktiven Apache- oder NGINX-Connector-Codes nach C++.
- Übergabe von C++-Objekten über Apache-, NGINX- oder zukünftige Server-ABI-Grenzen hinweg.
– Versteckt den Besitz von libmodsecurity-Transaktionen hinter einer undokumentierten C++-Lebensdauer
Regeln.
– Ersetzen allgemeiner C-First-Header durch eine Nur-C++-Adapter-API.

## Aktuelle Zuordnung

Die aktuellen Kabelbäume sind shell/Python.. Sie verwenden FFI nicht zur Instanziierung
C-Strukturen direkt. Stattdessen schreiben sie JSON-Felder, die absichtlich spiegeln
die C-first gemeinsamen Datenformen:

- `msconnector_status` -> `operation_status` und `status_model`
- `msconnector_origin` -> Anschluss `origin`
- `msconnector_intervention` -> pro Fall `intervention`

Dadurch bleibt die Evidenceschicht portierbar, während die öffentliche C-First-API erhalten bleibt
für zukünftige kompilierte Adapter.
