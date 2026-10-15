# Traefik native I12 host measurements

**Language:** English | [Deutsch](README.de.md)

`prepare.py` consumes the existing central `traefik-native` capture objects and
copies historical build scaffolding into an explicitly selected external root.
Every Common/Traefik C/header and native Go build input is refreshed from the
current checkout before the exact hash-checked observation overlays are applied.
The resulting product/capture binding, sealed file ledgers and controller
admission remain separate from runtime qualification.

The seven host probes cover a chunked request, delayed response writes,
P1/P2/P3 denial, late P4 Safe denial, MIME exclusion and an independent neighbor.
The separate client retains socket bytes and the backend retains received entity
bytes. A denied P1/P2 request must have no backend request. MIME/charset decisions,
native EOS, Finish and Free require native observer records. TCP EOF proves only
the transport observation. A client process exiting successfully records a
completed measurement; inspect `oracle_pass` for its actual expected outcome.

Preparation never launches a host:

```sh
rtk proxy python3 -B connectors/traefik/harness/i12/native/prepare.py \
  --repo /absolute/current/checkout \
  --historical /absolute/approved/historical/source-run \
  --output /var/tmp/codex/ModSecurity-conector/runs/task/native
```

Use only the separately reviewed private controller, its unchanged nonroot
admission checks and task-local resource/storage budget. Review `admission.json`
and all sealed bindings before launch. Do not launch archived drivers against
old evidence or a product checkout. The output root must be new for preparation. All three preparation commands
reject symlinked paths, Git checkout destinations and paths outside the configured
external storage before writing; followups also require fresh output targets.

`review.py ATTEMPT_DIRECTORY` summarizes fresh physical client/backend/native
and host records, executable/library maps and controller cleanup. Its output
deliberately keeps qualification false pending independent original-oracle and
complete lifecycle packet review. It does not update the central I12 ledger.
`prepare_followup.py ROOT faults-v3` prepares a separate real-engine UDS relay
fixture for corrupt MSE1 replies, internal error replies, actual opcode10
`AcknowledgeApplied`, a delayed16KiB response with a second-chunk error and an
active client RST. The physical relay log records the exact injected opcode.
`strict` separately tests profile admission; a rejected Strict configuration
does not establish a supported Strict lifecycle. `mime` separately exercises
request/response Content-Type and charset presence/absence and MIME exclusion.

The central host observer admits only its two historical synthetic IDs.
`prepare_host_scope.py ROOT` makes a separate sealed source copy with only that
observer allowlist expanded to the18 declared synthetic IDs. Retake using its
`admission-*-host-v2.json` specs. Earlier runs with nonadmitted IDs remain partial
measurements. `packet.py ATTEMPT LABEL ORIGINAL_CASE_ID` emits all35 prescribed
observation fields for independent review; absent callbacks remain unknown.
It never evaluates the oracle or grants qualification. Real fault outcomes can
include zero client bytes despite a logical host write; report that physical
outcome separately from an HTTP recorder or a native deny decision.
