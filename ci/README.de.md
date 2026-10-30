# Connector-CI-Einstiege

**Sprache:** [English](README.md) | Deutsch

## Ownership und Aufruf

Dieses Verzeichnis behält Produktpflege-/Buildhelfer und kleine authentifizierte
CI-Einstiege. Sämtliche Tests, Fixtures, Harnesses, Inventare, Provisionierung,
Evidence-Verarbeitung und Testreport-Generatoren gehören zum unabhängigen
Framework. Siehe [die Schnittstelle](../docs/test-ownership-migration.de.md) und
[Tests und Nachweise](../docs/testing-and-evidence.de.md).

Das Connector-Root-Makefile delegiert Testtargets an
`$FRAMEWORK_ROOT/connector_suite/connector.mk`. CI ruft gepinnte Framework-
Composite-Actions oder wiederverwendbare Workflows auf. Connector-Checkout,
exakte Revision, Framework-Checkout, Profil und vorhandener externer Ausgaberoot
werden explizit angegeben; der Produktcheckout wird nicht aus dem Skriptpfad
abgeleitet.

## Produkt- und Vertrauensgrenzen

Produktkonfiguration, Abhängigkeiten, Build, Installation und Deployment bleiben
Connector-eigen. Produktbinärdateien benötigen das Framework nicht zur Laufzeit.
`ci/run-trusted-framework.py` und die vom Gate verlangten `ci/runtime/broker/`-
Einstiege authentifizieren geschützte Parent-Basis und Framework-Gitlink vor der
Auswahl privilegierten Testcodes. Kandidatenquellen sind kein vertrauenswürdiger
Code. Feste Tool-Allowlist und geschütztes Host-Gate bleiben Pflicht; fehlende
Hostvoraussetzungen bedeuten `BLOCKED`, niemals automatischen Fallback oder PASS.

## Auswahl und Evidence

Das Framework-Inventar bewahrt 100 Standardfälle / 80 Ausführungen und die
ursprünglichen 1893 On-demand-Fälle / 839 Ausführungen. Neue Migrationsregressionen
bleiben auf Abruf. Die Standardgrenze ist 100; Auswahl wird vor Ausführung
validiert. Retries erzeugen keine zusätzlichen unterschiedlichen Fälle.
Statische Prüfung, native Suite, Workflowerfolg, Build oder Konfigurationsladen
belegen weder gehosteten Verkehr noch Produkt-Promotion. Laufartefakte bleiben
außerhalb beider Quellcheckouts.

## Pflege

Testimplementierung und reine Testabhängigkeiten werden im Framework ergänzt.
Hier bleiben nur kleine gepinnte Integrationsaufrufe. Bei Vertragsänderungen
beide Sprachfassungen und den Change Record dieses Repositories aktualisieren.
Framework und Connector haben getrennte Branches, Commits und PRs; zuerst
Framework integrieren, danach Connector-Gitlink und vollständige SHA-CI-Verweise.
Ein Testlauf erteilt keine Merge-Freigabe.
