# Common-Sicherheitsvertrag für Datenflüsse

Dieses Dokument beschreibt nur connector-neutrales Common-SDK-Scaffolding. Es behauptet keine Production-, Runtime-, CRS-, Full-Matrix- oder Connector-Fähigkeit, bis ein Connector ausdrücklich migriert wurde.

Datenfluss: untrusted input -> bounded parse -> validate -> immutable view -> phase guard -> decision -> integrity event -> JSONL -> cleanup.

Harte Resource-Limits schützen Header-Anzahl und -Größen, Body-Puffer, Event-JSON, Transaction-IDs, Rule-IDs und Log-Meldungen. Events und JSONL-Datensätze dürfen keine Request- oder Response-Body-Payloads enthalten.

Memory Ownership: borrowed bleibt beim Aufrufer, owned muss vom Besitzer freigegeben werden, static darf nicht freigegeben werden, arena wird mit der Arena freigegeben. Der checked allocator zählt owned Allocations ohne globalen veränderlichen Zustand.

Die `non_crypto_hash` FNV-1a-Kette ist nur deterministische Tamper-Evidence für CI und Smoke-Tests. Echte Manipulationssicherheit braucht später HMAC oder Signatur mit sicherem Schlüssel und append-only Storage.
