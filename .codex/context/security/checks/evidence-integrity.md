# Evidence Integrity and Claim-Binding Check

Every runtime/security/quality claim must bind to the applicable connector logical profile, Parent/Framework/MRTS revisions where required, run ID, effective configuration/rules, host/tool versions, transport when relevant, and the actual evidence schema.

Check for stale evidence, generated-report drift, wrong revision/profile, mixed runs, incompatible coverage merges, host/source mismatch, missing cleanup disposition, and promotion of source/build/config/service evidence into host runtime claims.

No profile may inherit PASS from another profile. No generated report is a fresh execution merely because it exists.
