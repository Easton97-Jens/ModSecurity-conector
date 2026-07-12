# HAProxy-Architektur

**Sprache:** [English](architecture.md) | Deutsch

Status: Produktions-SPOA-Laufzeit, teilweise und evidenzbezogen

Der HAProxy-Connector verwendet einen Produktions-SPOA/SPOP-Prozess anstelle eines
In-Process-HAProxy-Modul:

```text
HTTP client -> HAProxy -> SPOE/SPOP -> haproxy-modsecurity-spoa -> libmodsecurity -> HAProxy response
```

## Implementierter Pfad

- `haproxy-modsecurity-spoa` besteht aus
  `connectors/haproxy/src/haproxy_spop_diagnostic_runtime.c`.
- Die lokale libmodsecurity-Bindung wird aus erstellt
  `connectors/haproxy/src/haproxy_modsecurity_binding.c`.
- HAProxy sendet Anforderungs- und Antwortdaten über SPOE/SPOP.
- Der SPOA-Prozess gibt typisierte `txn.modsec.*`-Variablen für HAProxy zurück
  Durchsetzung.
- Laufzeitnachweise umfassen `decision.jsonl`, Überwachungsprotokollinstallation, HAProxy-Protokolle,
  SPOA-Protokolle, JSONL-Fallergebnisse und generierte Zusammenfassungen.

## Phasenabdeckung

- Anforderungsphasen 1/2: Live-Laufzeitnachweis.
- Antwort-Header der Phase 3: implementiert und live nachgewiesen.
- Phase 4 / RESPONSE_BODY: `not_implemented` im ausgewählten SPOE/SPOP-Pfad.

Das frühere begrenzte Strict-Abort-Beispiel ist deaktiviert und wird nur als Beispiel beibehalten
Vermächtnis, nichtkanonisches Artefakt. Es darf nicht verwendet oder als aktuell gemeldet werden
Laufzeitbeweise. Es wird das separate Profil `full-lifecycle-haproxy-htx` ausgewählt
die HAProxy 3.2.21 HTX-Route. Es verfügt über einen eigenen P1–P4-Transportrauch für den echten Wirt
mit geliehenen Anfrage-/Antwortblöcken. P1/P3 kann ein lokales Precommit ausgeben
antworten; Die Ein-Block-P2-Sonde kann einem Client 403 auf Anforderung EOS ausstellen, während die
Runner zeichnet null oder eine beobachtete Upstream-Anfrage auf, ohne deren Nachweis zu erbringen
bestellen. Dieses Ergebnis wird bewusst nicht als inkrementell dargestellt
Anforderungsweiterleitungsnachweise, und P4 Safe ist ein
explizites `log_only`-Ergebnis.

Dieser Smoke-Test beweist, dass ein gepatchter HTX-Filter in allen vier Fällen libmodsecurity aufrufen kann
Phasen. Die kanonischen P1-Regeln `1100001`/`1100002` erzeugen echte 403/429-Antworten.
und die P3-Regel `1100201` erzeugt einen echten 403 vor dem empfangenen Upstream-Header
Antwort wird weitergeleitet. Der Ein-Block-Client 403 von P2 verfügt über einen beobachteten Upstream
Die Anforderungsanzahl ist Null, sodass der Host-Smoke keine inkrementellen Schritte durchführt
Anforderungsweiterleitung oder eine allgemeine Puffereigenschaft. P4 Safe leitet die weiter
ursprüngliche Antwort und Datensätze `host_action=log_only`; P4 Strenge bleibt bestehen
`host_action=not_attempted`. Keiner der Pfade ist ein Stream-Abort, First-Byte oder
Client-No-Full-Buffer-Proof.

## Aktuelle Beweise

| Beweissatz | Versucht | PASS | FEHLER | GESPERRT | NOT_EXECUTABLE |
| --- | ---: | ---: | ---: | ---: | ---: |
| Standard-HAProxy-Smoke-Test | 55 | 55 | 0 | 0 | 0 |
| HAProxy Force-All | 133 | 104 | 23 | 0 | 6 |

## Grenzen

Es gibt keinen Schreiber für synthetische Matrizen. Generierte HAProxy-Berichte werden live genutzt
Laufzeitzusammenfassungen und der Laufzeitvalidierungs-Snapshot. Ganzkörpergarantien,
beliebige dynamische, disruptive Statuszuordnung und lang andauernde Produktion
Die Härtung bleibt bis zur Beförderung über den Teilstatus hinaus offen.

## Gemeinsame SDK-Einführungsschicht

HAProxy behandelt Common jetzt als Eigentümer für wiederverwendbare Semantiken: Konfigurationsvorgaben/Zusammenführung/Validierung, Direktivenspezifikationen, Parser für primitive Optionen, Request/Response-Mapper-Verträge, Header-/Inhaltshelfer, Ereignis-JSONL-Generierung, Regel-ID-Extraktion, Protokollbereinigung/-redaktion, Ressourcenlimits, DoS-Schutz, Flussschutz, Integritätsereignisse, Regelladestatistiken, CRS-Setup-Verträge und Test-/Artefaktverträge, sofern zutreffend.

Der HAProxy-eigene Code bleibt auf die Verarbeitung des SPOE/SPOP-Protokolls, generierte HAProxy-CFG-Fragmente, die Handhabung von SPOA-Laufzeitschleifen/Sockets, den HAProxy-Prozesslebenszyklus, Frame-Parsing, Rückgabe-/Aktionskodierung, Protokollierungstransport und Build-Glue beschränkt. Die C17-Standardprüfung kompiliert die adoptionsrelevanten C-Objekte, ohne HAProxy zu starten, und meldet `BLOCKED`/77, wenn erforderliche externe Header fehlen.
