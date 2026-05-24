# Connector Template

Status:
- scaffolded: yes
- implemented: no
- build_verified: no
- runtime_verified: no
- promoted: no

## Zweck

Dieses Verzeichnis ist ein **generisches, adapter-owned Connector-Template** für
neue Integrationen. Es liefert nur Struktur, Dokumentation und Checklisten.

## Wichtige Warnung

Dieses Template ist **keine Implementierung** eines produktiven Connectors.
Es enthält absichtlich **keinen produktiven C-Code** und macht **keine Aussage**,
dass ein neuer Connector funktioniert.

Alles, was nicht durch echte Build- und Runtime-Evidenz belegt ist, bleibt
"TODO" oder "noch zu prüfen".

## Erwartete Ordnerstruktur

```text
connectors/_template/
├── README.md
├── TODO.md
├── docs/
│   ├── architecture.md
│   ├── build.md
│   └── validation.md
├── harness/
│   └── README.md
├── src/
│   └── README.md
└── tests/
    └── README.md
```

## Herkunft des Musters (belegt)

Die Struktur orientiert sich an den im Repository vorhandenen adapter-owned
Connector-Bäumen (insbesondere Apache und NGINX), ohne deren Runtime-Verhalten
als generisch zu behaupten.

## Nutzungshinweis

Für einen konkreten neuen Connector sollte dieses Template nach
`connectors/<name>/` kopiert und anschließend ausschließlich mit nachweisbarer
Build-/Runtime-Evidenz weiterentwickelt werden.
