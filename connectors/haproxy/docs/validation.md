# HAProxy Runtime Validation Requirements

## Grundsatz

Strukturchecks allein reichen nicht. Für HAProxy sind echte Runtime-Nachweise
mit reproduzierbaren Artefakten erforderlich.

No tests are stored in this connector repository.

All test definitions, test execution, runners, and generated reports belong to
Easton97-Jens/ModSecurity-test-Framework.

## Mindestanforderungen (Runtime Evidence)

Für einen neuen Connector sind mindestens folgende Nachweise erforderlich
(Framework-seitig):

1. **HAProxy startet mit Testkonfiguration**
   - Konfiguration lädt ohne kritische Fehler.
2. **Connector-Komponente startet**
   - Alle erforderlichen Komponenten laufen stabil.
3. **Request wird geprüft**
   - Ein realer Request durchläuft den vorgesehenen Prüfpfad.
4. **Block/Allow wird nachweisbar gemappt**
   - Interventionen werden korrekt in HAProxy-Actions umgesetzt.
5. **Logs werden erzeugt**
   - Relevante HAProxy-/Connector-/Audit-Logs sind vorhanden.
6. **Report wird generiert**
   - Ergebnisbericht/JSON im erwarteten Schema liegt vor.

## Ergänzende Prüfungen (noch zu prüfen)

- Streaming-/Buffering-Randfälle
- Fehlerpfade bei Ausfall einzelner Komponenten
- Wiederholbarkeit über mehrere Durchläufe

## Nicht ausreichend

- Nur Datei-/Ordner-Existenztests
- Nur Lint/Syntaxchecks ohne reale Request-Ausführung
- Unbelegte Funktionsbehauptungen
