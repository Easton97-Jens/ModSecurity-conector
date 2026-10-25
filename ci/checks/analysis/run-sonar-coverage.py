#!/usr/bin/env python3
"""Produce genuine, revision-bound Parent coverage in a fresh external directory.

This is a selected Sonar assessment, not a hosted-runtime qualification or a
claim that every existing test executes. Test ownership and coverage are separate.
"""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import tempfile
import xml.etree.ElementTree as ET


ROOT = Path(__file__).resolve().parents[3]
RCFILE = ROOT / "ci/sonar-coverage.ini"
# Explicit requirements: analysis scope, revision provenance, private artifacts,
# report input classification, and engine inventory. No discovery of unrelated
# runtime/I12 suites. Subprocess patching also measures invoked Parent writers.
PYTHON_TESTS = (
    "tests.test_sonar_scope",
    "tests.test_sonar_coverage",
    "tests.test_sonar_evidence_boundaries",
    "tests.test_evidence_input_security",
    "tests.test_framework_revision_pins.RevisionLockTests.test_offline_loader_requires_no_git_repository",
    "tests.test_framework_revision_pins.RevisionLockTests.test_invalid_schema_and_revision_values_are_rejected",
    "tests.test_runtime_artifact_utils.RuntimeArtifactUtilsTest.test_descriptor_backed_private_root_requires_existing_exact_root",
    "tests.test_runtime_artifact_utils.RuntimeArtifactUtilsTest.test_descriptor_backed_private_root_rejects_links_hardlinks_and_unsafe_names",
    "tests.test_runtime_artifact_utils.RuntimeArtifactUtilsTest.test_runtime_or_source_artifact_path_accepts_only_project_sources_or_private_files",
    "tests.test_nginx_mrts_http500_cluster_analysis",
    "tests.test_engine_lifecycle_artifacts.EngineLifecycleArtifactsTest.test_writes_payload_free_current_host_inventory",
    "tests.test_engine_lifecycle_artifacts.EngineLifecycleArtifactsTest.test_rejects_payload_bearing_event_input",
)
# Named lifecycle and negative-boundary scenarios, across each module's relevant
# packages; -coverpkg=./... retains zeroes in unexecuted default-build packages.
GO_TESTS = {
    "envoy": ("connectors/envoy/ext_proc", (
        "TestClientFramesBoundedOrderedOperations",
        "TestProcessStreamsChunksAndCleansUpAtResponseEOS",
        "TestProcessRejectsExcessActiveStreamBeforeTransactionOpenAndReleasesSlot",
        "TestCheckRejects33ByteBodyWith413",
        "TestCheckPreservesValidatedRedirect",
        "TestProcessMissingMetadataFailsClosed503",
        "TestJSONLObserverRejectsFinalSymlink",
        "TestPrivateEventLogRetainsValidatedParentDescriptor",
        "TestPrivateUDSAcceptsExpectedPeerCredentials",
        "TestOwnedListenerDoesNotRemoveReplacedSocket",
        "TestSourceOnlyBuildRefusesServingEngine",
        "TestCompositeObserverWritesOnlyBoundedLifecycleMetadata",
        "TestCheckConfigAdmissionRejectsUnprovenStrictPolicy",
    )),
    "traefik-native": ("connectors/traefik/native_middleware", (
        "TestMiddlewareForwardsRequestAuthorityAsHostHeader",
        "TestMiddlewareRejectsConflictingHostHeaderBeforeEngine",
        "TestMiddlewareStreamsRequestAndResponseInBoundedChunks",
        "TestMiddlewareFailsClosedAndClosesIdleRequestBody",
        "TestLateResponseDecisionDoesNotReplaceCommittedResponse",
        "TestUDSEngineUsesOneSessionForFullLifecycle",
        "TestUDSEngineCancellationClosesBlockedConnection",
        "TestUDSEngineAcknowledgesP1AndP2HostDenies",
    )),
    "traefik-composite": ("connectors/traefik/composite_middleware", (
        "TestStripInternalHeadersRemovesTrailerForms",
        "TestMiddlewareReplacesClientLeaseAndCompletesPrivateLifecycle",
        "TestReservationPayloadBindsActualRequestTransportMetadata",
        "TestResponseWriterRecordsDownstreamWriteFailures",
        "TestResponseWriterSuppressesRejectedResponseChunk",
        "TestResponseWriterForwardsAllowedResponseChunkAtSameBoundary",
        "TestMiddlewareReplacesPreCommitUDSFailureWith503",
        "TestNewRejectsUnsafeSocketPath",
    )),
    "traefik-observer": ("connectors/traefik/response_observer", (
        "TestResponseHeaderEncodingUsesLengthThenBytesOrder",
        "TestReadResultAcceptsCanonicalStatuslessSuccess",
        "TestMiddlewareStreamsHeaderOnlyResponseAndStripsHandle",
        "TestMiddlewareFailsClosedForRejectedReplay",
        "TestMiddlewareAppliesPrecommitBlockAndCancel",
        "TestMiddlewareSendsBoundedResponseBodyChunks",
        "TestConcurrentRequestsUseIndependentSessions",
        "TestReleaseFailureTriggersDeterministicCleanup",
    )),
}


def run(arguments: list[str], *, cwd: Path = ROOT, env: dict[str, str]) -> str:
    result = subprocess.run(arguments, cwd=cwd, env=env, check=True, text=True,
                            stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    print(result.stdout, end="", flush=True)
    return result.stdout


def validate_python_report(path: Path) -> int:
    """Require real repository-relative production paths and actual execution."""
    report = ET.parse(path)
    classes = report.findall(".//class")
    if not classes or not any(int(line.get("hits", "0")) > 0 for line in report.findall(".//line")):
        raise ValueError("Python coverage has no measured execution")
    for entry in classes:
        filename = Path(entry.attrib["filename"])
        if filename.is_absolute() or ".." in filename.parts or not (ROOT / filename).is_file():
            raise ValueError(f"Python coverage path is not a repository file: {filename}")
    return len(classes)


def publish_python_report(output: Path, env: dict[str, str]) -> dict[str, object]:
    """Merge real parallel runs, retaining the earlier selected-test data."""
    env["COVERAGE_FILE"] = str(output / "python.data")
    coverage = [sys.executable, "-m", "coverage"]
    run([*coverage, "combine", "--append", f"--rcfile={RCFILE}"], env=env)
    report = output / "python.xml"
    run([*coverage, "xml", f"--rcfile={RCFILE}", "-o", str(report)], env=env)
    source_files = validate_python_report(report)
    # subprocess collection can add an empty Cobertura source element. Every
    # filename above was checked against the project root, so one explicit '.'
    # makes resolution unambiguous without changing any measured counters.
    tree = ET.parse(report)
    sources = tree.getroot().find("sources")
    if sources is None:
        raise ValueError("Python coverage has no source-root declaration")
    sources.clear()
    ET.SubElement(sources, "source").text = "."
    tree.write(report, encoding="utf-8", xml_declaration=True)
    return {"report": str(report), "source_files": source_files,
            "selectors": list(PYTHON_TESTS)}


def python_coverage(output: Path, env: dict[str, str]) -> dict[str, object]:
    env["COVERAGE_FILE"] = str(output / "python.data")
    coverage = [sys.executable, "-m", "coverage"]
    run([*coverage, "run", f"--rcfile={RCFILE}", "--parallel-mode",
         "ci/checks/analysis/check-sonar-scope.py"], env=env)
    run([*coverage, "run", f"--rcfile={RCFILE}", "--parallel-mode", "-m",
         "unittest", "-v", *PYTHON_TESTS], env=env)
    return publish_python_report(output, env)


def finalize_python(output_root: Path, env: dict[str, str], revision: str,
                    *, allow_dirty: bool = False) -> dict[str, object]:
    """Only combine CLI-integration coverage from the same completed revision."""
    for language in ("python", "go", "native"):
        manifest = json.loads((output_root / language / "manifest.json").read_text(encoding="utf-8"))
        if manifest.get("revision") != revision:
            raise ValueError(f"{language} coverage revision does not match the checkout")
        if manifest.get("uncommitted_changes") and not allow_dirty:
            raise ValueError(f"{language} coverage was produced from uncommitted changes")
    return publish_python_report(output_root / "python", env)


def go_coverage(output: Path, env: dict[str, str]) -> dict[str, object]:
    env.update(GOTOOLCHAIN="local", GOWORK="off", GOCACHE=str(output / "build-cache"),
               GOMODCACHE=str(output / "module-cache"))
    reports = {}
    for name, (relative, names) in GO_TESTS.items():
        module = ROOT / relative
        pattern = "^(" + "|".join(re.escape(name) for name in names) + ")$"
        listing = run(["go", "test", "-mod=readonly", "-list", pattern, "./..."], cwd=module, env=env)
        missing = set(names) - set(listing.splitlines())
        if missing:
            raise ValueError(f"selected Go tests are missing in {relative}: {sorted(missing)}")
        report = output / f"{name}.out"
        run(["go", "test", "-mod=readonly", "-count=1", "-timeout=120s", "-run", pattern,
             "-coverpkg=./...", f"-coverprofile={report}", "./..."], cwd=module, env=env)
        if len(report.read_text(encoding="utf-8").splitlines()) < 2:
            raise ValueError(f"Go coverage is empty: {relative}")
        run(["go", "tool", "cover", f"-func={report}"], cwd=module, env=env)
        reports[name] = {"report": str(report), "selectors": list(names), "packages": "./..."}
    return reports


def native_coverage(output: Path, env: dict[str, str]) -> dict[str, object]:
    build = output / "build"
    env.update(BUILD_ROOT=str(build), VERIFIED_RUN_ROOT=str(output / "runtime"),
               MSCONNECTOR_CFLAGS="-std=c17 -Wall -Wextra -Werror --coverage -O0")
    run(["sh", "ci/checks/common/check-common-helpers.sh"], env=env)
    gcov = output / "gcov"
    gcov.mkdir()
    objects = sorted((build / "common-helper-smoke").glob("*.gcda"))
    if not objects:
        raise ValueError("native tests produced no execution counters (.gcda)")
    sources = set()
    reports = 0
    for index, counters in enumerate(objects):
        work = output / "gcov-work" / str(index)
        work.mkdir(parents=True)
        run(["gcov", "--hash-filenames", "--preserve-paths", "--branch-probabilities",
             "--branch-counts", str(counters)], cwd=work, env=env)
        for report in work.glob("*.gcov"):
            first = report.read_text(encoding="utf-8").splitlines()[0]
            source = Path(first.split("Source:", 1)[1])
            if not source.is_absolute():
                source = ROOT / source
            source = source.resolve(strict=True)
            if source.is_relative_to(ROOT):
                if not source.is_file():
                    raise ValueError(f"native coverage source is missing: {source}")
                sources.add(source.relative_to(ROOT).as_posix())
                # Unique object prefix preserves every binary's real report,
                # including overlapping source coverage; no output overwrite.
                report.rename(gcov / f"{index}-{report.name}")
                reports += 1
    expected = {path.relative_to(ROOT).as_posix() for path in (ROOT / "common/src").glob("*.c")}
    if not expected.issubset(sources):
        raise ValueError(f"native coverage lost Common sources: {sorted(expected - sources)}")
    return {"reports_path": str(gcov), "reports": reports, "source_paths": sorted(sources),
            "limitation": "Common helper/constructor/intervention tests; no connector-host coverage"}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--language", choices=("python", "go", "native", "finalize-python"), required=True)
    parser.add_argument("--output-root", type=Path, required=True,
                        help="external task-owned root; each language subdirectory must be fresh")
    parser.add_argument("--temp-root", type=Path, required=True,
                        help="external temporary parent with a short path for Unix sockets")
    parser.add_argument("--allow-dirty", action="store_true",
                        help="local development only; mark reports as uncommitted evidence")
    args = parser.parse_args()
    try:
        if not args.output_root.is_absolute():
            raise ValueError("output root must be absolute")
        output_root = args.output_root.resolve()
        if output_root == ROOT or output_root.is_relative_to(ROOT):
            raise ValueError("coverage output must be outside the checkout")
        output = output_root / args.language
        if args.language != "finalize-python":
            output.mkdir(parents=True, exist_ok=False)
        temp_root = args.temp_root.resolve()
        if not args.temp_root.is_absolute() or temp_root == ROOT or temp_root.is_relative_to(ROOT):
            raise ValueError("temporary root must be absolute and outside the checkout")
        temp_root.mkdir(parents=True, exist_ok=True)
        env = dict(os.environ)
        env.update(PYTHONDONTWRITEBYTECODE="1", PYTHONNOUSERSITE="1")
        revision = run(["git", "rev-parse", "HEAD"], env=env).strip()
        status = run(["git", "status", "--porcelain", "--untracked-files=normal"], env=env)
        if status and not args.allow_dirty:
            raise ValueError("clean checkout required for revision-bound reports; use --allow-dirty only for local development")
        result = {"revision": revision, "uncommitted_changes": bool(status), "language": args.language,
                  "evidence_layer": "selected real test coverage; runtime and analyzer import not implied"}
        with tempfile.TemporaryDirectory(prefix="scov-", dir=temp_root) as temporary:
            env["TMPDIR"] = temporary
            if args.language == "finalize-python":
                result["coverage"] = finalize_python(output_root, env, revision,
                                                     allow_dirty=args.allow_dirty)
                output = output_root / "python"
            else:
                result["coverage"] = {"python": python_coverage, "go": go_coverage,
                                      "native": native_coverage}[args.language](output, env)
        if run(["git", "rev-parse", "HEAD"], env=env).strip() != revision:
            raise ValueError("checkout revision changed while tests ran")
        if run(["git", "status", "--porcelain", "--untracked-files=normal"], env=env) != status:
            raise ValueError("checkout files changed while tests ran")
        (output / "manifest.json").write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    except (OSError, ValueError, ET.ParseError, subprocess.CalledProcessError) as exc:
        if isinstance(exc, subprocess.CalledProcessError):
            print(exc.stdout or "", file=sys.stderr, end="")
        print(f"Sonar coverage failed: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
