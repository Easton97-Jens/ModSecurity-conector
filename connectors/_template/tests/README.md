# tests – Connector Template

Dieses Verzeichnis ist für connector-spezifische Testbausteine vorgesehen,
sobald ein konkreter Connector implementiert wird.

## Teststrategie (Template)

1. **Struktur- und Syntaxchecks**
   - Nur als frühe Qualitätsbarriere, nicht als Funktionsbeweis.
2. **Build-Validierung**
   - Reproduzierbarer Build des Connector-Artefakts.
3. **Harness-Smoke**
   - Start/Stop + Minimalrequest über realen Serverprozess.
4. **Regel-/Interventionstests**
   - Definierte Fälle mit erwarteten Allow/Block-Ergebnissen.
5. **Log- und Report-Validierung**
   - Nachvollziehbare Artefakte für Debugging und Bewertung.
6. **Promotionskriterien**
   - Promotion erst nach dokumentierter Runtime-Evidenz und stabiler
     Wiederholbarkeit.

## Vor Promotion nötig

- Nachweisbare reale HTTP-Ausführung
- Konsistente Ergebnisreports
- Dokumentierte bekannte Lücken (xfail/gap/pending)
- Keine unbelegten Kompatibilitätsbehauptungen
