# ModSecurity-Regelbeispiele

**Sprache:** [English](rule-examples.md) | Deutsch

## Regel-Engine-Modi

```apache
# Einen zulässigen deny vor dem Commit durchsetzen.
SecRuleEngine On

# Ohne disruptive Action treffen und protokollieren.
SecRuleEngine DetectionOnly

# Regeln nach dem Laden nicht auswerten.
SecRuleEngine Off
```

`DetectionOnly` lädt und bewertet Regeln, protokolliert Treffer, führt disruptive Actions aber nicht durch. `Off` deaktiviert die Engine-Regelauswertung; ein Connector-Schalter kann dabei weiterhin aktiv sein. Umgekehrt erreicht `SecRuleEngine On` keinen Verkehr, wenn der Hostconnector abgeschaltet ist.

## P1–P4-Beispiel

```apache
SecRequestBodyAccess On
SecResponseBodyAccess On
SecResponseBodyMimeType text/plain text/html application/json
SecResponseBodyLimit 1048576
SecResponseBodyLimitAction ProcessPartial
SecRule RESPONSE_BODY "@contains response-attack" \
    "id:1100301,phase:4,deny,log,status:403"
```

P1 sind Request-Header, P2 der Request-Body, P3 Response-Header und P4 der Response-Body. Die P4-Regel wünscht vor Commit eine 403; nach Commit bleibt der sichtbare Status hostabhängig und darf nicht als garantiert dokumentiert werden.
