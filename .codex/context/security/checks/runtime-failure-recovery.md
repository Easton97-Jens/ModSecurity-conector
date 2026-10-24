# Runtime Failure and Recovery Check

Assess applicable startup failure, dependency/service unavailability, timeout, malformed peer response, client abort, upstream abort, parser error, host reload/restart, companion/service restart, cleanup after failure, and a legitimate follow-up request.

Record whether failure is isolated to the affected transaction/process, whether stale state survives, whether the host fails open or closed, and whether cleanup leaves sockets/files/processes/listeners behind.

A successful later retry does not erase earlier failure evidence; distinguish setup correction from product instability.
