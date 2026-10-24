# Change Record: CR-20261018-haproxy-capture-storage-boundaries

**Language:** English | [Deutsch](CR-20261018-haproxy-capture-storage-boundaries.de.md)

## Identity

| Field | Value |
| --- | --- |
| Change ID | CR-20261018-haproxy-capture-storage-boundaries |
| Date (UTC) | 2026-10-18 |
| Base revision | `7ad1d7b1c6d88c7430213d408f1f184f2442314c` |

## Motivation and problem statement

Ten assigned Sonar findings cover capture complexity, repeated paths, an exception assertion and source admission. A bounded regression demonstrated that replacing the release archive after its digest check changed the parsed source. A second regression demonstrated that a writable source anchor was admitted.

## Acceptance criteria

The authenticated bytes must be the parsed bytes. Input and materialization must use held directory descriptors with no link following. Private storage ownership must be checked. Existing capture source bytes, modes and normalization receipts must remain identical; all original oracle gaps stay unchanged.

## Implementation decision and rationale

The archive is opened relative to a held storage descriptor, checked as a regular file and read once. The verified buffer is parsed through `BytesIO`. Output directories and exclusive regular files are accessed relative to held descriptors; replacing the visible source directory causes rejection. The final build receipt reuses the authenticated archive digest. Native source admission derives components from `relative_to` and checks the held private root. Export and port decisions use small helpers; repeated paths use constants.

## Changed files

- `connectors/haproxy/harness/i12_current_capture.py`
- `connectors/haproxy/harness/i12_native_contracts.py`
- `tests/test_haproxy_i12_current_capture.py`
- `tests/test_haproxy_i12_native_source_paths.py`
- `reports/audits/change-records/CR-20261018-haproxy-capture-storage-boundaries.md`
- `reports/audits/change-records/CR-20261018-haproxy-capture-storage-boundaries.de.md`

## Commands executed

```sh
rtk proxy env PYTHONNOUSERSITE=1 /root/git/ModSecurity-conector/.venv/bin/python -B -m unittest -v tests.test_haproxy_i12_current_capture tests.test_haproxy_i12_native_source_paths
rtk proxy env PYTHONNOUSERSITE=1 /root/git/ModSecurity-conector/.venv/bin/python -B -m unittest -v tests.test_haproxy_i12_native_cases
```

The two baseline regressions fail for their intended assertions; 19 focused tests and 19 existing native tests pass. A preparation-only export of the exact base revision and a release extraction compare bytes and modes against the frozen build. Exact arguments, exits and raw hashes are retained in the run receipts.

## Security impact

This is bounded defensive harness correction. No scan, exception, suppression, gate change or product authorization change is included. No shell-expanded archive paths are introduced. Descriptor operations require the existing Linux runtime and a private storage root owned by the executing user.

## Runtime evidence

No host run or new compilation is claimed. Preparation matches 2173 current-base files, 1944 historical-base files and 2175 files in each of the three capture variants, including inventory metadata. Only path-dependent receipt metadata and two existing generated staging helpers are excluded explicitly. All 1391 upstream files match bytes and modes; all 11 normalization entries are identical. Evidence root: `R2/sonar-haproxy/7ad-capture-boundaries-20261018`.

## Known limitations

The root operator and selected source revision remain trusted. This does not establish immutable storage against the same privileged operator or qualify any lifecycle route. The frozen build and historical fixtures remain unchanged.

## Remaining risks

Sonar server readback remains pending. Local code and regressions establish behavior, not server closure. Future consumer builds must record their own exact source revision; the existing build continues to identify its frozen producer.

## Checks not run and rationale

No host traffic, new product build or broad security assessment was run: this assignment concerns only the specified harness findings and source-preservation checks. Root owns host acceptance, publication and server readback.

## Final diff and review status

The owned changes preserve original source contracts and use existing capture machinery. Independent Root review and publication remain required. No Git mutation is part of this work.
