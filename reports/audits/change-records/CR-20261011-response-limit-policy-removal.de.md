# Change Record: CR-20261011-response-limit-policy-removal

**Sprache:** [English](CR-20261011-response-limit-policy-removal.md) | Deutsch

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | CR-20261011-response-limit-policy-removal |
| Datum (UTC) | 2026-10-11 |
| Basis-Revision | `498653c2a193d34b7b25b2903b1e4db1c45e7f73` |

## Motivation und Problemstellung

Connector-Response-Grenzen konnten Daten ablehnen oder kürzen, bevor libModSecurity
seine konfigurierte Response-Policy anwendete. Die Stack-Änderung entfernt diese
zweite Policy aus Common und allen zehn logischen Connectorprofilen.
Response-Inspektionslimit und Aktion gehören ausschließlich zu
`SecResponseBodyLimit` und `SecResponseBodyLimitAction`.

## Akzeptanzkriterien

Connector-Response-Konfiguration, Defaults, kumulative Bytegrenzen und Kürzung
entfernen; Request-Policy, Access-/MIME-Auswahl und `off`/`safe`/`strict`-
Hostverhalten erhalten. Echte technische Schutzgrenzen erhalten und deren Fehler
von nativem Response-`BODY_LIMIT` unterscheiden. Native Operationsergebnisse,
Interventionen und Phasenabschluss erhalten. Jede Response-Inspektionsfixture
setzt beide nativen Direktiven explizit. Grenzfälle, Modi, mehrere Chunks und
Dateieingabe, unterschiedliche Limits, Ablehnung entfernter Optionen und Bodies
über der früheren 1-MiB-Grenze prüfen. EN/DE-Referenzen pflegen und Hostnachweise
getrennt ausweisen. Eine abgeschlossene Sonar-Analyse des aktuellen Heads ohne
neue Issues, Hotspots und New-Code-Duplikation bleibt für verifizierte Auslieferung
erforderlich.

## Implementierungsentscheidung und Begründung

Entfernte Optionen sind Common `response_body_limit`, HAProxy
`response-body-limit` und Envoy `max_response_body_bytes`, einschließlich ihrer
Response-Felder, Defaults und Fallback-Helper. Request-Limits und
Request-`body_limit_action` bleiben erhalten. Adapter bieten vollständige gültige
Chunks der Engine an; libModSecurity wählt Reject oder ProcessPartial. Common
bewahrt eine beim Append erfasste disruptive Response-Intervention über spätere
Chunks und den Phasenabschluss. Native Response-Limit-Ablehnung behält Phase 4
und HTTP 403; technische Pointer-, Overflow-, Transport- oder Speicherfehler
behalten ihre technische Klassifikation. Der Zähler inspizierter Bytes beschreibt
der Engine angebotene Bytes, nicht deren internen ProcessPartial-Präfix.

## Geänderte Dateien

- Common-Konfiguration, Body-/Resource-/Mapper-/Transaktionsverträge, native Runtime,
  Decision-/Intervention-Klassifikation und MRC1-Response-Transport.
- Apache-, NGINX-, HAProxy-, Envoy-, Traefik- und lighttpd-Response-Routen,
  Connector-Konfiguration, Harnesses, Tests und EN/DE-READMEs.
- `ci/checks/documentation/connector_config_reference.py`, seine generierten
  `examples/*/configuration-reference.md`- und `.de.md`-Begleiter,
  `examples/common/`-Referenzen und
  `reports/connector-configuration-inventory.json`.
- Response-Fixtures unter `common/rules/`, Connector-Harnesses und
  `ci/runtime/lifecycle/cases/apache-phase4-response/`; NGINX-Workflow-Fixture-
  Argumente; Common-, Adapter-, Transport-, Event- und Optionsentfernungsregressionen.
- `docs/phase4-mode-budget.md` / `.de.md`,
  `docs/response-limit-stack-checklist.md` / `.de.md`, Repository-Konzept,
  Runtime-Fehlerpolicy, Traefik-Compilerleitfaden und Beispiel-README-Paare.
- Dieses EN/DE-Change-Record-Paar. Framework-/MRTS-Quellen und Dependency-Manifeste
  werden nicht geändert.

## Ausgeführte Befehle

Die folgenden Koordinatorprüfungen bestanden im Implementierungsworktree vor
abschließendem Stack-Transfer. Ihre Ergebnisse belegen keine Prüfungen für einen
künftigen PR-SHA.

```sh
rtk proxy /root/git/ModSecurity-conector/.venv/bin/python -m unittest -v tests.test_engine_response_limits
rtk proxy make check-common-helpers check-common-sdk-contract check-common-security-contract check-common-memory-safety check-common-flow-integrity check-adapter-contracts check-directive-parity PYTHON=/root/git/ModSecurity-conector/.venv/bin/python BUILD_ROOT=/var/tmp/codex/ModSecurity-conector/runs/engine-response-limits-20261011/root-checks/build
rtk proxy make check-bilingual-docs check-doc-links PYTHON=/root/git/ModSecurity-conector/.venv/bin/python
rtk proxy git diff --check
```

Die Engine-Suite bestand 81 echte native Szenarien. Common-Helper-, SDK-,
Security-, Speicher-, Flow-, Adapter- und Direktivenprüfungen bestanden.
Dokumentations- und Linkprüfungen bestanden; Generierung/Prüfung der Referenzen
bestand. Zwei Compilefehler integrierter Fixtures wurden behoben. Der gezielte
13-Test-Wiederholungslauf und der folgende integrierte 57-Test-Lauf bestanden.
Der abschließende integrierte 57-Test-Lauf im frischen Worktree bestand in
22,053 Sekunden, einschließlich aller 81 nativen Common-Szenarien und der
Regression mit passender Phase-4-Regel.

Weitere Komponentenvalidierung bestand: HAProxy-Binding-/SPOA-Builds und echte
16-Fall-Response-Suite und abschließende Sechs-Methoden-Suite mit echter Library; Envoy `build_ext_proc.sh` mit
`ENVOY_EXT_PROC_COMMON_TEST=1` über acht CGo-/libModSecurity-Packages und das
Binary; Envoy-Authz-/Observer-, Traefik-forwardAuth- und lighttpd-Stock-Sidecar-
Builds; strikte C17-MRC1- und Observer-Companion-Tests; 31 lighttpd-Gate-/Supervisor-/
Namespace-Tests. Apache-C17-Syntaxprüfung bestand nach Änderungen zum Interventionserhalt. Der
nativ zugeordnete pytest-Lauf bestand 136 Tests und 174 Subtests, einschließlich
19 Tests erforderlicher Fixture-Helper. Externe Laufartefakte bleiben
unter `/var/tmp/codex/ModSecurity-conector/runs/engine-response-limits-20261011/`.

## Security-Auswirkung

Nicht vertrauenswürdige Response-Daten erreichen die Engine ohne
Connector-Inspektionsgrenze. Begrenzte Operationen bleiben erhalten: Pointer- und
Integerprüfungen, Dateilesen und Deskriptoren, fester Scratch-Speicher,
MRC1-Body-Chunks von 32 KiB und Frames von 64 KiB, Protokoll-/Nachrichtengrenzen,
Header-/Eventmetadaten und Transporttimeouts. Request-Policy bleibt erhalten.
Authentifizierung, Isolation, Warnungen, Tests, Scanner-Ausnahmen oder
Quality-Gate-Anforderungen werden nicht abgeschwächt. Fehlende Engine-Policy
verwendet native Semantik; Betreiber müssen ihr gewünschtes natives Limit und
die Aktion konfigurieren.

## Runtime-Evidence

Die Common-Suite mit echter Library verwendet libModSecurity 3.0.14 mit Limits
128 und 1024, Reject und ProcessPartial, `off`/`safe`/`strict`, Payloads
unter/exakt/über Limit und Chunkgrößen 17/65536. Zusätzliche Markerfälle
unterscheiden den nativen Teilpräfix von späteren Daten. Explizite Limits von
1,5 MiB und 3 MiB mit 2-MiB-Bodies decken die frühere versteckte 1-MiB-Grenze
auf. HAProxys echte Komponentensuite umfasst Speicher-/Dateieingabe und erhaltene
native Interventionen. Envoys native Regression setzt `2097152` und Reject
explizit und inspiziert einen Tail nach 1 MiB; sein Test mit geliehenen Responses
akzeptiert 300 Callbacks. MRC1-Komponentenprüfungen senden mehrere gültige Chunks
über der früheren kumulativen Grenze und lehnen übergroße Frames technisch ab.
Dies sind Komponenten-/Engine-Ergebnisse; sie beweisen keinen gehosteten
Lebenszyklus eines der zehn Profile.

## Bekannte Einschränkungen

Die Stock-Sidecar-Suite bestand 33 von 34 Tests; ihr RST-Test für Rule-Block-
Auslieferung erzeugte keine Events. Auch die ältere Lossy-Event-Assertion in
`transaction_phase_runtime_companion_test.c` schlägt mit echter Library fehl.
Beide Fehler wurden auf der unveränderten ursprünglichen Basis reproduziert;
ihre Assertions bleiben erhalten. Eine weitere Auswahl nativer Transaktions-
Bindingtests bestand 24 Tests; zwei alte Request-ID-/Stop-Erwartungen schlugen
fehl und wurden ebenfalls auf unveränderter Basis reproduziert. Ein breiter
zugeordneter Lauf wurde ohne abschließende Zusammenfassung abgebrochen und gilt
nicht als bestanden. Der auskompilierte gepufferte lighttpd-
Legacy-Austausch unter `#if 0` ist keine aktive Response-Kapazität; der aktive
Sidecar streamt feste Scratch-Chunks. Für native NGINX-/HAProxy-C17-/Hostprüfung
fehlen weiterhin erforderliche Hostquellen/-Header oder Runtime-Artefakte.
Frische gehostete Lifecycle-Evidence fehlt für alle zehn Profile.

## Verbleibende Risiken

Komponentenerfolg belegt keine native Host-Buffer-Ownership, Commit-Zeitpunkte,
Auslieferung später Interventionen oder Transportlebenszyklen in eingesetzten
Hosts. Die vier reproduzierten Basisfehler bleiben offen. Der frische integrierte Lauf und unabhängiger statischer Sicherheitsreview
bestanden. Aktuelle Head-CI/Sonar und Auslieferungsverifikation müssen vor
vollständiger Verifikation abgeglichen werden.

## Nicht ausgeführte Prüfungen mit Begründung

Keine frische gehostete Zehn-Profil-Matrix wurde ausgeführt: Die erforderlichen
gepinnten Hostumgebungen und Laufnachweise fehlen. Noch existiert keine
abgeschlossene Sonar-Analyse für den neuen PR-Head; die Analyse des Basis-PRs
belegt diese Änderung nicht. Wegen fehlender Hostartefakte blockierte native
NGINX-/HAProxy-Prüfungen sind keine bestandenen Prüfungen. Der frische integrierte Wiederholungslauf bestand. Der frische native pytest-
Lauf bestand 136 Tests und 174 Subtests in 44,77 Sekunden. Abschließende
Common-Helper-/SDK-/Security-/Speicher-/Flow-/Adapter-/Direktivenprüfungen,
21 generierte Referenzen, bilinguale Dokumentation, Pfade und Links bestanden.
Die fünf neuen Basisdateien und der Framework-Gitlink blieben unverändert.

## Finaler Diff- und Review-Status

Die Diff-Whitespace-Prüfung im Implementierungsworktree bestand. Statischer
Quellcode-Sicherheitsreview fand kein aktuelles Problem; seine Diff-Whitespace-
Prüfung bestand. Inhaltsreview und Abgleich mit frischer Basis sind abgeschlossen; die lokale
Änderung ist zur Commit-Vorbereitung bereit. Aktueller
Auslieferungsstand ist lokale Arbeit; dieser Record behauptet keinen neuen
Draft-PR, Push oder Merge. Die
[Stack-Checkliste](../../../docs/response-limit-stack-checklist.de.md) trennt
Implementierung, ausführbare Tests und fehlende echte Hostnachweise.
