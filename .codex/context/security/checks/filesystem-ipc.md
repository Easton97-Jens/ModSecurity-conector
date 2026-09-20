# Filesystem, UDS, and Local IPC Check

For local sockets, runtime directories, temporary files, companion protocols, and private service paths assess absolute/canonical containment, parent ownership/mode, symlink/hardlink/replacement risks, path length, world/group writable ancestors, same-UID limitations, creation/bind/readiness races, cleanup ownership, and post-readiness replacement.

Where peer credentials are used, verify when and for which connection they are checked, expected versus actual UID/PID semantics, restart/PID-reuse behavior, platform fallbacks, and fail-closed behavior when the primitive is unavailable.

A private `0700` directory is not proof against a hostile process running as the same UID.
