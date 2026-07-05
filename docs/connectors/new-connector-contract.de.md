# Neuer Connector-Contract

Ein Starter-Connector darf dünne Adapter-Mapper auf die Common-SDK-Contracts für Request, Response und Config legen, muss aber `runtime_status=not_verified` und `verification_status=connector-gap` behalten, bis echte Runtime-Evidence vorliegt. Body-Payloads dürfen nicht geloggt werden. Server-spezifische Typen gehören nicht nach `common/`. Host-API-Glue, Runtime-Lifecycle, Build-Glue und Protokoll-/Frame-Handling bleiben im Connector-Baum.
