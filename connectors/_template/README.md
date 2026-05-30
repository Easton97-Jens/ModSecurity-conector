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

## Status-Vokabular

- `template`: generische Vorlage, keine Implementierung.
- `scaffolded`: Struktur vorhanden, aber keine belegte Adapter-Implementierung.
- `adapter-owned`: produktiver Connector-Code liegt im Connector-Baum mit
  Herkunft und Metadaten.
- `runtime-smoke-verified`: nur konkret gelaufene Smoke-Fälle mit Command und
  Ergebnis.
- `partial`: Struktur oder Teilruntime ist belegt, aber keine vollständige
  Verifikation.
- `not-verified`: keine ausreichende Runtime-Evidenz.

## Erwartete Ordnerstruktur

```text
connectors/_template/
├── README.md
├── TODO.md
├── docs/
│   ├── architecture.md
│   ├── build.md
│   ├── coverage-decision-matrix.md
│   └── validation.md
├── harness/
│   └── README.md
├── src/
│   └── README.md
```

## Herkunft des Musters (belegt)

Die Struktur orientiert sich an den im Repository vorhandenen adapter-owned
Connector-Bäumen (insbesondere Apache und NGINX), ohne deren Runtime-Verhalten
als generisch zu behaupten.

## Nutzungshinweis

Für einen konkreten neuen Connector sollte dieses Template nach
`connectors/<name>/` kopiert und anschließend ausschließlich mit nachweisbarer
Build-/Runtime-Evidenz weiterentwickelt werden.

Runtime-Claims dürfen erst gesetzt werden, wenn der konkrete Command, das
Ergebnis und die betroffenen Fälle dokumentiert sind. Ein Strukturcheck oder
ein Build-Artefakt ist kein Runtime-PASS.

## Tests

Dieses Template enthält keinen lokalen `tests`-Ordner. Neue Connectoren dürfen
keinen lokalen `connectors/<name>/tests`-Ordner anlegen. Ausführbare Tests
werden nicht connector-lokal gepflegt.

Belegte externe Framework-Pfade für neue Connector-Dokumentation:

- `modules/ModSecurity-test-Framework/tests/cases/`
- `modules/ModSecurity-test-Framework/tests/cases/connector-specific/<connector>/`
- `modules/ModSecurity-test-Framework/tests/runners/case_cli.py`

Wenn die Make-Targets im konkreten Repository vorhanden sind, muessen
Runtime-Ergebnisse fuer CRS-Varianten getrennt dokumentiert werden:

- `make test-no-crs`: lokale YAML-Regeln ohne CRS.
- `make test-with-crs`: CRS vorbereiten/laden und danach lokale YAML-Regeln
  ausfuehren.

Ein PASS in `test-no-crs` ist kein PASS fuer `test-with-crs`. Ein einzelner
PASS eines CRS-Falls ist kein Gesamt-PASS fuer `test-with-crs`, wenn ein
anderer Fall FAIL ist.

## Coverage / Runtime Decision Matrix

Neue Connectoren muessen `docs/coverage-decision-matrix.md` ausfuellen. Die
Matrix trennt Framework-Coverage von Runtime-Verifikation und zeigt, welche
Evidenz erforderlich ist, bevor ein Connector mehr als `partial` sein darf.

## RESPONSE_BODY

`RESPONSE_BODY` bleibt `not-verified`, bis mindestens diese Evidenz vorhanden
ist: belegbarer Runtime-Testcase im Framework, erwarteter blockierender
Response-Body-Trigger, tatsächliches blockierendes Ergebnis wie HTTP 403,
Log-/Report-Evidence, ausgeführter Command und betroffener Connector.
