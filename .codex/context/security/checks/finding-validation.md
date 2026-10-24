# Finding Validation and Attack-Path Check

A suspicious pattern, scanner signal, advisory hit, or AI result begins as a candidate.

Before reporting it as a validated security finding establish: attacker-controlled source/precondition, reachable path, broken/missing security control, sink, security invariant, impact, relevant counterevidence, and reproducible or otherwise strong validation evidence.

For remediation-oriented validation also define a same-boundary legitimate control and at least one alternate bypass class.

Keep independently reachable instances separate when one correction would not close all of them. Cross-cutting root causes identify the owning repository/component without authorizing edits there.
