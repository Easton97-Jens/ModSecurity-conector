from pathlib import Path
root=Path(__file__).resolve().parents[1]
mk=(root/'Makefile').read_text()
need=['check-remaining-connectors-c17','check-remaining-connectors-c23','check-remaining-connectors-future-c','check-remaining-connectors-c17-lint']
missing=[n for n in need if n not in mk]
if missing: raise SystemExit('missing Makefile targets: '+', '.join(missing))
print('remaining connector C standard wiring: ok')
