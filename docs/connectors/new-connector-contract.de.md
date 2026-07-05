**Sprache:** [English](new-connector-contract.md) | Deutsch

# Neuer Connector-Contract

Ein Starter-Connector darf dünne Adapter-Mapper auf die Common-SDK-Contracts für Request, Response und Config legen, muss aber `runtime_status=not_verified` und `verification_status=connector-gap` behalten, bis echte Runtime-Evidence vorliegt. Body-Payloads dürfen nicht geloggt werden. Server-spezifische Typen gehören nicht nach `common/`. Host-API-Glue, Runtime-Lifecycle, Build-Glue und Protokoll-/Frame-Handling bleiben im Connector-Baum.

## Adaption des generischen Mappers

Starter-Connectoren sollen den connector-neutralen generischen Mapper-Helfer verwenden, wenn ihre lokale Quelle als `msconnector_generic_request_source` oder `msconnector_generic_response_source` beschrieben werden kann. Lokale Connector-Dateien sollen dünne Adapter bleiben und dürfen Common-Validation, Body-Metadaten-Zuweisung oder Ownership-Cleanup-Logik nicht duplizieren.

Diese Adaption bedeutet keine Runtime-Verifikation. Die betroffenen Connectoren bleiben `not_verified` / `connector-gap`, bis echte Runtime-Evidence vorliegt. Die verbleibenden Starter-Connectoren vermeiden connector-lokale Mapper-Quellkopien, indem ihre Einstiegspunkte auf den connector-neutralen generischen Mapper zeigen; Validierung und Body-Metadaten-Zuweisung liegen dadurch an einer Common-Stelle.

Aufrufer des generischen Mappers müssen `hostname` als NUL-terminierte Zeichenkette übergeben, wenn das Feld gesetzt ist. Header-Value-Slices werden niemals als C-String-Hostnamen exponiert. Body-Größen größer als null erfordern einen nicht-NULL Body-Zeiger und bleiben metadatenbezogen, sofern der Aufrufer sichere Body-Bytes besitzt.

## Erwartungen an das Common-Paket

Common-Dateien bleiben connector-neutral. Server-spezifische Includes, Typen und Laufzeit-Lifecycle-Code gehören in den jeweiligen Connector-Baum. Neue Connectoren sollen Source-Maps, Metadaten, Capabilities und Validierungsberichte so pflegen, dass Starter-, Compile-only- und Connector-Gap-Zustände ehrlich von echter Runtime-Evidence getrennt bleiben.
