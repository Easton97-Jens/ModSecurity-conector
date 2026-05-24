# HAProxy Connector Scaffold

Status:
- scaffolded: true
- implemented: false
- build_verified: false
- runtime_verified: false
- promoted: false

No HAProxy connector is implemented yet.

## Zweck

Dieses Verzeichnis ist ein vorsichtiger, adapter-owned Scaffold für einen
zukünftigen HAProxy-Connector. Es enthält nur Struktur- und Planungsdokumente,
keine produktive Runtime-Implementierung.

## Wichtige Grenzen

- Keine Aussage über Funktionsfähigkeit.
- Keine Aussage über Build-Erfolg.
- Keine Aussage über Runtime-Kompatibilität.
- Alle unbelegten Punkte sind als "noch zu prüfen" markiert.

## Struktur

```text
connectors/haproxy/
├── README.md
├── TODO.md
├── docs/
│   ├── architecture.md
│   ├── build.md
│   ├── public-sources.md
│   └── validation.md
├── harness/
│   └── README.md
├── src/
│   └── README.md
└── tests/
    └── README.md
```
