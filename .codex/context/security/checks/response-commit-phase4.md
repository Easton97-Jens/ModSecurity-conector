# Response Commit and Phase-4 Check

Keep these observations separate:

1. P3/P4 code path executed;
2. rule evaluated;
3. rule matched;
4. engine requested intervention;
5. connector selected an action;
6. host accepted/executed that action;
7. response commit state;
8. client-visible status/bytes/stream result;
9. cleanup/event outcome.

Test applicable pre-commit and post-commit cases, partial response, flush/streaming, EOS, disconnect, error path, and host-specific abort/reset support.

Current implementation semantics and the target contract in `../../phase4-target-semantics.md` are different evidence classes. Do not report target semantics as current implementation.

A match is not automatically a block. A configured strict mode is not proof of a real abort/reset.
