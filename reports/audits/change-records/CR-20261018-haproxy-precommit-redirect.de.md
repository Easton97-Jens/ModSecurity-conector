# Change Record: CR-20261018-haproxy-precommit-redirect

**Sprache:** [English](CR-20261018-haproxy-precommit-redirect.md) | Deutsch

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | CR-20261018-haproxy-precommit-redirect |
| Datum (UTC) | 2026-10-18 |
| Basis-Revision | `38edee9431192ea8b691a46d37601ecea0915142` |

## Motivation und Problemstellung

Die ursprüngliche Framework-P3-Regel1100202 verlangt HTTP302 und
`Location: https://no-crs.invalid/phase3-redirect`. Der HTX-Filter stufte Redirects
stattdessen als nicht unterstützt ein und antwortete503. Das ursprüngliche
Oracle bleibt erhalten: gültige P1/P2/P3-Redirects vor Commit anwenden,
Finish/Free einmal ausführen und bei ungültigen Entscheidungen oder technischen
Fehlern fail-closed bleiben.

## Akzeptanzkriterien

Original302/Location vor Commit direkt und über Companion erhalten; URL vollständig besitzen, native Freigabe einmal ausführen und ungültige oder technische Ergebnisse fail-closed behandeln. Unabhängige integrierte Host-Retests bleiben erforderlich.

## Implementierungsentscheidung und Begründung

Das Binding besitzt die vollständige native URL vor Intervention-Cleanup und
lehnt Überlänge, rohe Steuerzeichen und DEL ab. Ein kleiner HAProxy-lokaler
Inline-Validator wird von Erfassung und HTX-Aufrufer verwendet. Der Filter nutzt
in gepinntem HAProxy3.2.25 `http_apply_redirect_rule` mit literalem
`REDIRECT_TYPE_LOCATION`, dem erlaubten ursprünglichen Status301/302/303/307/308
und `FROM_REQ` nur für P1/P2. Er finalisiert und deaktiviert den nativen Kontext
vor der synchronen Reply-API; nur Rückgabe1 gilt als Erfolg.

Der Companion kopiert seine ergebniseigene URL vor Reset, führt die Hostantwort
aus und zeichnet anschließend REDIRECT OUTCOME mit302 vor RELEASE auf. Eine
fehlgeschlagene Bestätigung nach der tatsächlichen Antwort bricht ohne zweite
HTTP-Antwort ab. Common-/MRC1-Verträge und Layouts bleiben unverändert. Geändert
sind HAProxy-Binding/Header, HTX-Filter und Overlay-Prüfung; Regressionen decken
Redirect-Erfassung, native Hostaufrufer und bestehende Fail-closed-Verträge ab.
Das HAProxy-README-Paar und dieses Change-Record-Paar dokumentieren den
unterstützten Pfad und die Evidenzgrenzen.

## Geänderte Dateien

HAProxy-Binding/Header, HTX-Filter, Overlay-Prüfung, neuer Redirect-Vertragstest und bestehende I10-Hostaufrufer-/Security-/Payload-Vertragstests; HAProxy-README-Paar und dieses Change-Record-Paar. Keine Common-/MRC1-Änderung.

## Ausgeführte Befehle

RTK-umhüllte kompilierte Regressionen des alten Quellstands scheitern an der
302-Antwort beziehungsweise Ablehnung überlanger URLs. Echte
libModSecurity3.0.14-Kontrollen für kanonisches P3 direkt/Companion und P1/P2
bestanden. Erfassungs-Sanitizer und drei Mutationskontrollen bestanden; die native
Hostmatrix erhielt19 bestehende, sechs Strict- und sieben neue Redirect-
Mutationen. Sechs Sanitizer-/physische Event-/Owner-Prüfungen, fünf frühere
Request-Scope-/Versions-/First-Cause-/Reentry-Kontrollen,15 Quellverträge und
C17-/Overlay-Prüfungen bestanden. Frische vollständige HAProxy3.2.25-, Binding-
Selbsttest- und produktive SPOA-Builds bestanden. Exakte argv, Exits,147
Rohdatei-Hashes und die eingefrorene Quelldateiidentität der neun Dateien liegen
im Lauf `i12-haproxy-415-acceptance-20261015/product-spop/redirect`.


Zusätzlicher Root-Lauf: deklarierter CPython3.14.7-pytest für die vier betroffenen Testdateien bestand mit23 Tests/34 Subtests. Exakte argv/Exits liegen in commands/redirect-root-focused-regression-20261018-v2.json; der vorherige Versuch mit ungültigem Interpreterpfad exit127 bleibt erhalten.

## Security-Auswirkung

Die Antwort verwendet die öffentliche API für literale Header ohne
Logformat-Auswertung oder still abgeschnittenen geliehenen Text. Nicht
unterstützter Status, ungültige URL, früherer Fehler, Finish- und Host-API-Fehler
bleiben fail-closed; nach Commit kann die Antwort nicht ersetzt werden. Keine
Abhängigkeits-, Warnungs-, Gate-, Admission- oder Isolationskontrolle wird
geschwächt. Die Arbeit ist eine begrenzte defensive Korrektheitsreparatur.

## Runtime-Evidence

Echte libModSecurity3.0.14- und Host-API-Komponentenprüfungen bestanden. Für diesen Redirect-Fix wurde noch kein unabhängiger Client-/Backend-Hostlauf qualifiziert.

## Bekannte Einschränkungen

Die Tests belegen native Engine und Host-API. Frische Capture-Builds des aktuellen
Quellstands und unabhängige native/Companion302-Retests für Client, Backend und
Transport bleiben erforderlich. HTTP-only- oder Komponentenergebnisse erhalten
keine Lifecycle-Anrechnung. Der separat beobachtete Companion-Safe-OUTCOME-Fehler
bleibt ein offener Produktfehler und ändert seine ursprüngliche Erwartung nicht.

## Verbleibende Risiken

Die separat beobachtete Companion-Safe-OUTCOME-Abweichung benötigt eine eigene Produktkorrektur und erneute Hostläufe. Native und Companion302 benötigen frische integrierte Capture-Binaries; Komponenten-PASS ist kein Lifecycle-PASS.

## Nicht ausgeführte Prüfungen mit Begründung

Integrierte Redirect-Hostläufe und Final-Head-CI/Sonar folgen der regulären Lieferung #382→#410→#415. Kein automatischer PR-Merge und keine Änderung ursprünglicher Oracles. Der historische #382-Gitleaks-Releaseblocker bleibt unabhängig.

## Finaler Diff- und Review-Status

Root prüfte den produktiven Dispatcher, URL-Besitz, Fail-closed-Pfade und Regressionen. Die separate unabhängige Prüfung wird mit der Laufübergabe festgehalten; ihr Ergebnis wird erst nach Eingang berichtet.
