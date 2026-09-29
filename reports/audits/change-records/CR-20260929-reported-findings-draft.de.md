# Change Record: gemeldete Findings — ungeprüfter Patch-Entwurf

**Stand:** vorgeschlagene Quellcodeänderungen; keine Tests, Builds, Patch-Anwendbarkeitsprüfung oder Laufzeitausführung.
**Basis:** `d56af0856507eb048987974d3960e301e7c24371`.
**Umfang:** ausschließlich B09, B13 und C07. Kein Abschluss des gesamten Scanbestands.

## Vorgeschlagenes Verhalten

- **B13** (`csf_d60ac4261fdf382b0cdc51bf`): Der Original-URI-Puffer erhält das Headerwertmaximum plus ein Byte für NUL. Ein vorhandener leerer, nicht mit `/` beginnender, zu großer, NUL-haltiger oder nicht kopierbarer maßgeblicher Wert ergibt einen Fehler statt eines anderen Headers oder `/authorize`. Der Aufrufer antwortet vor Common mit HTTP 400. Bei vollständig fehlenden Metadaten bleibt der bisherige Rückfall bestehen. Endpunktauthentisierung und allgemeine Headerweitergabe werden damit nicht implementiert.
- **B09** (`csf_110c7b683d38cd566861364f`): Eine positive Intervention wird auch in einer Error-Page-Anfrage als aktiv klassifiziert. Nur ein inaktives Ergebnis darf den bestehenden Bypass verwenden. Negative Fehler und normale Freigaben behalten ihr Verhalten.
- **C07** (Cloud-Finding `8d2cfdfbd7ac819198af08de2ec1a8d4`): Der OFF-Zweig des Stock-lighttpd erhält die Engineentscheidung, protokolliert jedoch Hostaktion `log_only`, den ursprünglichen Antwortstatus und Transportergebnis `log_only`. Ein Fehler bei der Aufzeichnung wird weitergegeben statt bedingungslos Erfolg zu melden. Dadurch werden keine Responsebytes zurückgehalten; B07 wird nicht behoben.

## Regressionsmaterial

`tests/test_reported_security_regressions.py` ergänzt isolierte C-Helfertests für B09/B13 sowie Quelltext-Vertragsprüfungen für den B13-Aufrufer und den C07-OFF-Zweig. Die C-Tests übernehmen echte Funktionskörper mit minimalen Testtypen; sie starten keinen echten Parser, Proxy oder ModSecurity-Host. Fehlendes `cc` überspringt die kompilierten Checks, statt einen erfolgreichen Lauf zu behaupten.

Der zugehörige Framework-Draft ergänzt synthetische Normalizerfälle für C07 und Pre-Commit-Evidencegrenzen B06/B07. Ein normalisierter synthetischer Datensatz ist kein Host-Laufzeitergebnis.

## Ausstehende Abnahme — nicht ausgeführt

- Betroffene C-Übersetzungseinheiten in unterstützten Hostkonfigurationen bauen.
- Vorgeschlagene Tests und bestehende betroffene Suites in der vorgeschriebenen Umgebung ausführen.
- B13: 8.191 / 8.192 / 8.193-Byte-Ziele durch den realen Proxy sowie vorhandene ungültige bevorzugte und vollständig fehlende Metadaten prüfen.
- B09: erlaubter Ursprungspfad und durch eine echte Regel abgelehntes Error-Page-Ziel; Aufruf des Contenthandlers und Rekursionsverhalten beobachten. Die Klassifizierungsänderung ist allein kein nachgewiesener rekursionssicherer vollständiger Hostfix.
- C07: echten Upstream-Status 200 und P4 deny/status:403 bei explizitem OFF und ausgelassenem Standardwert beobachten; ausgelieferten Status/Body und Hostaktionsfelder getrennt beurteilen.
- Anwendbarkeit der Quellfenster-Patches am exakten Basisstand prüfen. Beim Entwurf stand kein vollständiger lokaler Checkout zur Verfügung.
- Jedes Finding bleibt bis zu seiner eigenen erfolgreichen Abnahme offen.

## Grenzen und Kompatibilität

Vorhandene ungültige URI-Metadaten führen absichtlich zu Ablehnung statt Rückfall. Die Größenkonstante für das direkte Requestziel bleibt unverändert.
Keine Änderung der P2-/P4-Streamingarchitektur, des Phase4-Defaults, von Regeln, Dependency-Pins, CI-Rechten, Scanner-Severity, historischen Abschlusszuständen, Parent-Framework-Gitlink oder MRTS.
Diese Datei erstellt keinen Branch, Commit, Push, Merge oder Online-PR.

Nur das lokale Paket enthält die vollständige Ursprungszuordnung. Rohscans, Exploitpayloads und persönliche Metadaten nicht automatisch veröffentlichen.
