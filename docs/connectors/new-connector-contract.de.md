# Neuer Connector-Contract

Ein Starter-Connector darf dünne Adapter-Mapper auf die Common-SDK-Contracts für Request, Response und Config legen, muss aber `runtime_status=not_verified` und `verification_status=connector-gap` behalten, bis echte Runtime-Evidence vorliegt. Body-Payloads dürfen nicht geloggt werden. Server-spezifische Typen gehören nicht nach `common/`. Host-API-Glue, Runtime-Lifecycle, Build-Glue und Protokoll-/Frame-Handling bleiben im Connector-Baum.

## Generic mapper adoption

Starter connectors should prefer the connector-neutral generic mapper helper when their local source can be expressed as `msconnector_generic_request_source` or `msconnector_generic_response_source`. Local files should stay thin adapters and must not duplicate header mapping, Host fallback, Common validation, or ownership cleanup logic. This does not imply runtime verification.
