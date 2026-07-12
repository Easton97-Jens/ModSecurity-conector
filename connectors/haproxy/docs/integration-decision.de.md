# HAProxy-Integrationsentscheidung

**Sprache:** [English](integration-decision.md) | Deutsch

Status: SPOE/SPOA für den aktuellen Produktionslaufzeitbereich ausgewählt

## Entscheidung

Verwenden Sie HAProxy SPOE/SPOP mit einem externen `haproxy-modsecurity-spoa`-Prozess
lädt libmodsecurity.

```text
HAProxy -> SPOE/SPOP -> haproxy-modsecurity-spoa -> libmodsecurity
```

## Warum dieser Weg

- HAProxy dokumentiert SPOE/SPOP für externe Stream-Verarbeitungsagenten.
- Der Pfad vermeidet die Erfindung einer nativen HAProxy-Modulschnittstelle.
- Das Repository verfügt jetzt über eine erstellbare SPOA-Laufzeit und eine libmodsecurity-Bindung.
- Der Laufzeit-Harness startet dann HAProxy, den SPOA-Prozess und ein Backend
  Verifiziert die YAML-Erwartungen des Live-Frameworks.
- Derselbe Pfad erzeugt `decision.jsonl`, Audit-Log-Plumbing und generiert
  Laufzeitzusammenfassungen.

## Alternativen

| Alternative | Aktuelle Entscheidung |
| --- | --- |
| Nativer HAProxy-Filter oder Erweiterung | Das separate `full-lifecycle-haproxy-htx`-Profil wählt eine HAProxy 3.2.21 HTX-Route mit isoliertem P1–P4-Transportnachweis aus. Es beweist kanonische P1/P3-Antworten; Seine Ein-Block-P2-Sonde gibt einen Client 403 zurück und zeichnet null oder eine beobachtete Upstream-Anfrage auf, ohne deren Reihenfolge oder inkrementelle Weiterleitung nachzuweisen. P4-sichere Datensätze `log_only`. Strict verfügt über keinen für den Client sichtbaren Abbruchnachweis und die Route verfügt über keinen Nachweis zur Fähigkeitsförderung. |
| Lua-Integration | Aufgeschoben. Für den gesamten ModSecurity-Lebenszyklus nicht nachgewiesen. |
| Externer HTTP-Sidecar | Aufgeschoben. Der implementierte Pfad verwendet stattdessen SPOE/SPOP. |

## Aktuelle Beweise

- Standard-HAProxy-Smoke-Test: `55/55 PASS`.
- HAProxy Force-All: `133 Versuche / 104 PASS / 23 FAIL / 0 BLOCKIERT /
  6 NOT_EXECUTABLE`.
- Details: `reports/testing/generated/haproxy-runtime-results.generated.md`.
- PoC-Bericht: `reports/testing/haproxy-poc.md`.

Phase 4 / RESPONSE_BODY ist `not_implemented` im ausgewählten SPOE/SPOP-Pfad.
Das ehemalige `wait-for-body`-Strict-Abort-Beispiel ist deaktiviert, veraltet und
nichtkanonisch; Es handelt sich nicht um aktuelle Laufzeitbeweise.
