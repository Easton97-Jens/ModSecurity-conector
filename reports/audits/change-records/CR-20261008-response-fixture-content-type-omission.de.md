# Change Record: CR-20261008-response-fixture-content-type-omission

**Sprache:** [English](CR-20261008-response-fixture-content-type-omission.md) | Deutsch


## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | CR-20261008-response-fixture-content-type-omission |
| Datum (UTC) | 2026-10-08 |
| Basis-Revision | `b7403e30111688da00d8e7ce376ea91ced1c6145` |

## Motivation und Problemstellung

Explizit fehlendes Content-Type wurde in leeren Header oder Backend-Default umgewandelt.

## Akzeptanzkriterien

Echtes HTTP muss Content-Type vollständig weglassen; Defaults unverändert; Framing/unbekannte/konfligierende Auslassungen fail-closed.

## Implementierungsentscheidung und Begründung

Optionales omit_headers=['Content-Type'] durch geschlossenen Helper validieren und nur explizite Auslassung im bestehenden Backend anwenden.

## Geänderte Dateien

ci/runtime/common/response_fixture_omission.py; ci/runtime/common/response-header-test-backend.py; tests/test_response_fixture_omission.py; EN/DE Record-Paar.

## Ausgeführte Befehle

RTK-umhülltes Parent-Python: fehlender Helper RED1; echter Wire RED1/Default-Header; GREEN6 Tests0; bestehendes Backend10 Tests0/keine SKIPs mit vertrauenswürdigem Framework und externem TMPDIR. Nativer Record-Archivcheck0. Bilingual-/Doc-Link-Target2: nicht initialisierte Framework-Links im isolierten Worktree; keine Prüfung abgeschwächt.

## Security-Auswirkung

Keine Framing-/Security-Header-Auslassung oder Produktsemantikänderung; Auslassungs-/konfigurierte Headerkonflikte einschließlich Leerwerte werden abgelehnt.

## Runtime-Evidence

Echte begrenzte Loopback-HTTP-Unitoperation erhielt200/Body mit Content-Length15 ohne Content-Type-Feld. Keine Root/nobody-Connector- oder Canonical-Evidence.

## Bekannte Einschränkungen

Koordinator muss explizites omit_headers in geteilten Metadaten weitergeben; nativer NGINX-Missing-Header-Fokus bleibt offen.

## Verbleibende Risiken

Integrierte Wire-/Native-Evidence muss den Vertrag erfüllen; kein PASS allein aus Fixtures oder Abwesenheit.

## Nicht ausgeführte Prüfungen mit Begründung

Vollständiger Parent-Lint, integrierte native Requests und Remote-Prüfungen warten auf Koordinatorintegration. Vollständige Bilingual-/Doc-Link-Prüfungen benötigen den tatsächlichen nested Framework-Checkout; dieser isolierte Worktree lässt ihn nicht initialisiert.

## Finaler Diff- und Review-Status

Nur explizite Taskdateien; kein Push/Merge/Gitlink-Update. Unit-/bestehende Backendprüfungen grün; finale Integration bleibt offen.
