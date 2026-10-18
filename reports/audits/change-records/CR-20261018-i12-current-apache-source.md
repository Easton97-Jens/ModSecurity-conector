# Change Record: CR-20261018-i12-current-apache-source

**Language:** English | [Deutsch](CR-20261018-i12-current-apache-source.de.md)

## Identity

| Field | Value |
| --- | --- |
| Change ID | CR-20261018-i12-current-apache-source |
| Date (UTC) | 2026-10-18 |
| Base revision | `2c38d0ff2960a9ff2a76291955e808683febf06e` |

Owner: Parent PR #410; consumer: Apache PR #414.

## Motivation and problem statement

The historical Apache capture profile pins native observer input bytes from its
original export. Applying it to the current committed observer correctly fails.
A current full build needs a separately named, strictly bound source profile.
Integration also changed five repository-backed HAProxy/lighttpd bases. Their
historical content hashes must continue to resolve to their original bytes.

## Acceptance criteria

Accept a complete current Git export only with its v2 source inventory. Preserve
all historical objects and profiles, capture output bytes and runtime route IDs.
Reject a substituted v1 identity, changed source bytes and unknown formats before
writing capture files. Source application alone must never qualify a host case.

## Implementation decision and rationale

The additive `apache-current` profile changes the two native C/header input pins
and declares the existing v2 format mandatory. Its output hashes, three Apache
product overlays and SDK ABI remain identical to the historical `apache` profile.
Registry validation rejects an unknown required identity format; application
checks the profile requirement before its first write. Complete inventory and
per-file hash checks remain in force.
The integrated shared repair already freezes the five historical objects as
lossless text-line objects. All 155 previous content hashes remain unchanged.
The Apache profile needs no duplicate preservation objects; no historical overlay
is silently applied to a changed base.

## Changed files

The shared capture registry, manifest, negative controls and EN/DE capture guide. No historical content bytes, product source or
Framework/MRTS gitlink changes.

## Commands executed

RTK-wrapped Parent Python unittest discovery for `test_capture_sources.py`:
54 tests passed, exit 0. Controls export the entire committed Parent Git tree,
bind its actual revision/tree/modes/hashes and exercise the real application.
Historical profile equality and all unchanged output hashes are checked.
Registry verification: 155 content objects, ten source profiles, exit 0. The
initial current-head run failed on the changed repository bases; that failure
was corrected by preserving their historical bytes rather than bypassing hashes.

## Security impact

No validation, compiler warning, isolation, authentication or quality gate is
relaxed. The profile requires stronger provenance than the historical v1 path.

## Runtime evidence

These are source-integrity controls. They produce zero runtime PASS. A fresh
Apache build, loaded-image proof and per-case qualification remain separate.

## Known limitations

The profile intentionally refuses future source changes until their exact input
bytes and capture compatibility have been reviewed. It does not update old runs.

## Remaining risks

Successful source application does not establish build reproducibility or host
behavior. PR #414 must supply those observations on the integrated revision.

## Checks not run and rationale

No connector host matrix, deployment, release or master integration is performed
by this shared source-profile change. Hosted checks follow normal publication.

## Final diff and review status

The bounded profile delta and refusal controls were reviewed. Historical evidence
remains attached to its actual source revision and instrumented binary.
