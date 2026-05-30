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
│   ├── test-framework-contract.md
│   └── validation.md
├── harness/
│   └── README.md
├── poc/
│   └── spoe/
│       ├── README.md
│       ├── agent/
│       ├── harness/
│       ├── reports/
│       ├── haproxy.cfg.example
│       └── spoe-agent.conf.example
└── src/
    └── README.md
```

No tests are stored in this connector repository.
All test definitions, test execution, runners, and generated reports belong to
Easton97-Jens/ModSecurity-test-Framework.
