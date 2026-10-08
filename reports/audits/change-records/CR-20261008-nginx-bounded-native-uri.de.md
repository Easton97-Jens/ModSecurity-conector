# Begrenzte URI-Projektion nativer NGINX-Events

Die NGINX-Event-Grenze projiziert ausschließlich die URI in einen begrenzten
Stack-Puffer, erhält die expliziten Truncation-/Redaction-Flags und bewahrt
`?<redacted>` auch bei einer Query hinter dem maximal sicheren Präfix.
Die Grenze gilt für escapte JSON-Bytes, nicht nur Eingabezeichen. Alle anderen
Common-Serializer-Felder und die strikte Behandlung von Schreibfehlern bleiben
unverändert.

Fünf URI-Grenzprüfungen und 15 Prüfungen des tatsächlichen Request-Error-Producers
bestanden mit echtem Common-JSON-Serializer und C17-Warnungen als Fehler.
Zu große andere Metadaten bleiben Fehler. Der Materializer listet den neuen
Header explizit. Diese kompilierten Kontrollen sind keine Live-Runtime-,
Canonical- oder Exact-Head-Evidence; frischer Source-gebundener Native-Build und
Ausführung der erforderlichen Cases stehen aus.
