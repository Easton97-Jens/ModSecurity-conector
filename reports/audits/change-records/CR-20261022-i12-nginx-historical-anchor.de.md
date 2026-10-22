# Change Record: CR-20261022-i12-nginx-historical-anchor

**Sprache:** [English](CR-20261022-i12-nginx-historical-anchor.md) | Deutsch

Ausschließlich Reparatur historischer Quellspeicherung.

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | CR-20261022-i12-nginx-historical-anchor |
| Datum (UTC) | 2026-10-22 |
| Basis-Revision | `7284aa598adf04c8321163d5e7c5f45e3f1bd649` |

## Motivation und Problemstellung

Die NGINX-Produktaktualisierung schrieb `ngx_http_modsecurity_access.c` fort.
Die vollständige I12-Registry löste ihr historisches Objekt `3ad4e4d8…` weiterhin
über die aktuelle Repository-Datei auf und scheiterte deshalb vor jedem Staging.

## Akzeptanzkriterien

Das Objekt rekonstruiert die exakten 38.520 historischen Bytes. Seine
SHA256-Identität, das abhängige Delta und die Profilhashes bleiben unverändert;
vollständige Registry- und Capture-Kontrollen bestehen.

## Implementierungsentscheidung und Begründung

Die authentifizierte historische Quelle wird nach dem vorhandenen Muster für
HAProxy, lighttpd und Traefik verlustfrei als `text_lines` eingefroren. Die
vollständige Registry-Prüfung wird weder übersprungen noch werden aktuelle
Produktbytes mit einem historischen Hash bezeichnet.

## Geänderte Dateien

`ci/runtime/lifecycle/i12/manifest.json`, die EN/DE-READMEs des I12-Capture-Vertrags,
das Objekt `3ad4e4d8…-ngx_http_modsecurity_access.c.lines.json` und dieser EN/DE-Beleg.

## Ausgeführte Befehle

`capture_sources.py verify`: PASS (155 Objekte/10 Profile). Die fokussierte
Capture-Suite: PASS (57 Tests). Die unabhängige Rekonstruktion ergab 38.520 Bytes
mit SHA256 `3ad4e4d801672b0aec1c94326e6e0a2e12e2422e57d1e747121a0bbc2c1b73c8`.
Der Traefik-Current-Capture-Test gehört zu PR #413 und läuft nach der Integration.

## Security-Auswirkung

Keine Änderung an Produkt, Protokoll, Authentifizierung, Autorisierung oder Isolation.
Strenge Hashes für Gesamt-Registry, Quelleingaben und Deltas bleiben aktiv.

## Runtime-Evidence

Kein Host wurde gestartet; Quellprüfung vergibt keine Lifecycle-Qualifikation.

## Bekannte Einschränkungen

Aktuelle NGINX- und andere Produktquellen unterliegen weiterhin den vorhandenen
Profil- und vollständigen Exportverträgen.

## Verbleibende Risiken

Die zuständige Routenaufgabe muss weiterhin frische Inputs und Runtime-Belege für
den aktuellen Head erzeugen.

## Nicht ausgeführte Prüfungen mit Begründung

Go-/Race-/Vet- und Hostprüfungen liegen außerhalb dieser reinen Speicherreparatur
und verbleiben in der zuständigen Traefik-Abnahme.

## Finaler Diff- und Review-Status

Die begrenzte Prüfung bestätigt unveränderte historische Identität, abhängiges
Delta, Profile und Capture-Implementierung. Change-Record-Vertrag und Diffprüfung
bestehen. Die vollständige Zweisprachigkeitsprüfung erreicht ausschließlich 22
vorhandene fehlende Links in das nicht initialisierte Framework-Gitlink; die
geänderten EN/DE-Paare und lokalen Links stimmen überein. Die integrierte
Traefik-Capture-Prüfung läuft nach dem normalen Merge von #410 nach #413.
