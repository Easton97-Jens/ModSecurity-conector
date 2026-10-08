# Änderungsnachweis: CR-20261008-nginx-response-limit-signature

**Sprache:** [English](CR-20261008-nginx-response-limit-signature.md) | Deutsch

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | CR-20261008-nginx-response-limit-signature |
| Datum (UTC) | 2026-10-08 |
| Basis-Revision | `91625ef984dcff914ea3a631dc738645d78abf45` |

## Motivation und Problemstellung

Die festgelegte Engine liefert bei SecResponseBodyLimitAction Reject eine gültige Intervention ohne Regel-ID. NGINX klassifiziert sie aktuell als ungültiges Engine-Ergebnis. Eine allgemeine Ausnahme für fehlende Regelidentitäten würde die Validierung schwächen.

## Akzeptanzkriterien

Nur Antwortkörperphase, disruptive 1, Status403, keine URL, keine Regelidentität und exakt die native Diagnose akzeptieren. Andere Phasen, Statuswerte, boolesche Werte, Diagnosepräfixe/-suffixe, Umleitungen und Interventionen mit Regel-ID ablehnen.

## Implementierungsentscheidung und Begründung

Das neue ausschließlich NGINX betreffende statische Inline-Prädikat übernimmt die bestehende gemeinsame Interventionsdarstellung und eine begrenzt extrahierte Regelidentität. Der Vergleich liest höchstens52 Diagnosebytes einschließlich Terminator. Dies erkennt eine vorhandene Engine-Policy; Common und off/safe/strict sowie Connector-Limit-Policy bleiben unverändert.

## Geänderte Dateien

connectors/nginx/src/ngx_http_modsecurity_response_body_limit.h; tests/fixtures/nginx_response_body_limit.c; tests/test_nginx_response_body_limit.py; dieses EN/DE-Paar. Modul-Timing und Source-Map-Verdrahtung gehören dem Koordinator.

## Ausgeführte Befehle

RTK-vermittelter expliziter Parent-Python-Unittest kompiliert C17 mit -Wall -Wextra -Werror -pedantic-errors für MODSECURITY_SANITY_CHECKS=0 und1. RED scheiterte zunächst am fehlenden Header; GREEN kompilierte und führte sämtliche Positiv-/Negativkontrollen mit Exit0 aus.

## Security-Auswirkung

Keine globale Ausnahme für fehlende Regel-ID, abgeschwächte Validierung oder neue Berechtigung. NULL-Intervention/-Diagnose, nicht exakte disruptive-Werte und jede nicht-NULL-URL werden abgelehnt. Eingaben sind gültige NUL-terminierte Engine-Zeichenketten, keine beliebigen unterminierten Puffer.

## Runtime-Evidence

Der aufbewahrte externe reine Engine-CAPI-Test beobachtete append1, retained length0 und eine unmittelbare Intervention1/Status403/disruptive1/ohneURL/ohneRegel mit exakt nativer Diagnose: Response body limit is marked to reject the request. Dies ist keine synthetische NGINX-Evidence. Der frühere echte NGX-Reject-Aufruf hatte Client18 mit Invalid-Engine-Abbruch; der Header allein behauptet keine integrierte Reparatur.

## Bekannte Einschränkungen

Der Adapter ruft den Helfer noch nicht auf. Die Koordinatorintegration muss die Intervention unmittelbar am tatsächlichen Auftreten abholen, normale Regel-ID-Prüfungen erhalten und das Modul neu bauen.

## Verbleibende Risiken

Eine passende Signatur beweist weder das Enforcement-Timing noch ein kanonisches Response-Limit-PASS.

## Nicht ausgeführte Prüfungen mit Begründung

Frischer integrierter nativer Reject-Test und vollständige Suite warten auf Modul-/Timing-/SOURCE_MAP-Integration und Neubau des Koordinators. Kein finales Exact-Head, geschützter Nachweis oder kanonisches PASS behauptet.

## Finaler Diff- und Review-Status

Nur exklusive neue Helfer-, C-Fixture-, Test- und Dokumentationsdateien; MRTS, Gitlinks, gemeinsame Adapter- und Common-Dateien unverändert.
