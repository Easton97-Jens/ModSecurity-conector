#!/usr/bin/env python3
"""Build the existing Envoy I12 capture in a fresh, Git-free source copy.

This producer never launches a host. Its receipts qualify source/build and
native controls only; route qualification requires separate host evidence.
"""
import argparse
import hashlib
import importlib.util
import io
import json
import os
from pathlib import Path
import shutil
import subprocess
import tarfile
import time
import source_inventory


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def validate(source, out, env, run, go, sdk_include, sdk_library, controls_only=False):
    module = source / "connectors/envoy/ext_proc"
    before = {name: sha(module / name) for name in ("go.mod", "go.sum")}
    symbols = load(source / "tests/test_native_lifecycle_observer.py", "observer_validation").SYMBOLS
    observer_flags = " ".join([str(out / "libi12_envoy_observer.a"),
        "-Wl,--undefined=msconnector_lifecycle_sdk_transaction_id",
        *("-Wl,--wrap=" + name for name in symbols)])
    env.update(CGO_ENABLED="1", CGO_CFLAGS=" ".join(["-D_DEFAULT_SOURCE -std=c17",
        *('-I' + str(path) for path in (source, source / "common/include",
          source / "common/runtime", sdk_include))]),
        CGO_LDFLAGS=" ".join([str(out / "build/envoy-ext-proc/libmsconnector_envoy_ext_proc_common.a"),
            observer_flags, str(sdk_library), "-Wl,-rpath," + str(sdk_library.parent), "-lstdc++ -pthread"]))
    if not controls_only:
        run("go-native", [go, "test", "-tags", "libmodsecurity", "-count=1", "./..."], module)
        run("go-race", [go, "test", "-race", "-tags", "libmodsecurity", "-count=1", "./..."], module)
        run("go-vet", [go, "vet", "-tags", "libmodsecurity", "./..."], module)
    control_output = out / "observer-controls"
    suffix = 1
    while control_output.exists():
        suffix += 1
        control_output = out / ("observer-controls-" + str(suffix))
    env["NATIVE_OBSERVER_TEST_OUT"] = str(control_output)
    if sdk_include == Path("/usr/include"):
        # Shared controls hardcode -isystem. Use byte-identical physical headers
        # outside GCC's canonical include_next directory, without editing tests.
        private_include = out / "control-sdk-include"
        if not private_include.exists():
            shutil.copytree(sdk_include / "modsecurity", private_include / "modsecurity")
        headers = {str(path.relative_to(sdk_include)): sha(path)
                   for path in (sdk_include / "modsecurity").rglob("*") if path.is_file()}
        copied = {str(path.relative_to(private_include)): sha(path)
                  for path in private_include.rglob("*") if path.is_file()}
        if headers != copied:
            raise ValueError("private control SDK header bytes differ")
        (out / "control-sdk-headers.json").write_text(json.dumps({
            "source": str(sdk_include), "copy": str(private_include),
            "headers_sha256": headers, "byte_identical": True}, indent=2) + "\n")
        env["MODSECURITY_INCLUDE_DIR"] = str(private_include)
    run("native-observer-controls", ["python3", source / "tests/test_native_lifecycle_observer.py"], source)
    if before != {name: sha(module / name) for name in before}:
        raise ValueError("Go module input mutated")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--checkout", type=Path, required=True)
    parser.add_argument("--run-root", type=Path, required=True)
    parser.add_argument("--module-cache", type=Path, required=True,
                        help="Existing offline module cache; copied before use")
    parser.add_argument("--go", type=Path, default=Path("/usr/local/go/bin/go"))
    parser.add_argument("--sdk-include", type=Path, default=Path("/usr/include"))
    parser.add_argument("--sdk-library", type=Path,
                        default=Path("/usr/lib/x86_64-linux-gnu/libmodsecurity.so"))
    parser.add_argument("--tmp-root", type=Path,
                        help="Private physical short directory for Unix-socket test paths")
    parser.add_argument("--validate-existing", action="store_true",
                        help="Validate this producer's hash-bound existing build without rebuilding")
    parser.add_argument("--controls-only", action="store_true",
                        help="With --validate-existing, retry native controls after successful Go checks")
    args = parser.parse_args()
    if args.controls_only and not args.validate_existing:
        parser.error("--controls-only requires --validate-existing")
    checkout = args.checkout.resolve(strict=True)
    root = args.run_root.absolute()
    storage = Path("/var/tmp/codex/ModSecurity-conector")
    if storage not in root.parents or root.resolve() != root:
        parser.error("run root must be a physical external project-storage path")
    root.mkdir(parents=True, exist_ok=True)
    source, out = root / "source", root / "native-build"
    if not args.validate_existing and (source.exists() or out.exists()):
        parser.error("fresh source and native-build destinations required")
    out.mkdir(exist_ok=args.validate_existing)
    env = os.environ.copy()
    env.update(PYTHONNOUSERSITE="1", PYTHONDONTWRITEBYTECODE="1",
               PIP_REQUIRE_VIRTUALENV="true", PIP_DISABLE_PIP_VERSION_CHECK="1")
    receipt = {"schema": "i12.envoy.native-build.v1", "host_launched": False,
               "source_copy": str(source), "checks": [], "status": "in_progress"}
    if args.validate_existing:
        receipt = json.loads((out / "receipt.json").read_text())
        if not receipt.get("build_ready") or receipt["source_copy"] != str(source):
            parser.error("existing build receipt is not ready or names a different source")
        if args.controls_only:
            for label in ("go-native", "go-race", "go-vet"):
                if not any(check["exit_code"] == 0 and
                           (check["label"] == label or check["label"].startswith(label + "-retry-"))
                           for check in receipt["checks"]):
                    parser.error("--controls-only requires successful existing " + label)
    if args.tmp_root:
        temp = args.tmp_root.absolute()
        if storage not in temp.parents or temp.resolve() != temp:
            parser.error("temporary directory must be physical under external project storage")
        temp.mkdir(mode=0o700, parents=True, exist_ok=True)
        if temp.is_symlink() or temp.stat().st_uid != os.getuid() or temp.stat().st_mode & 0o077:
            parser.error("temporary directory must be private and owned by the current user")

    def save():
        (out / "receipt.json").write_text(json.dumps(receipt, indent=2) + "\n")

    def run(label, command, cwd=checkout, timeout=1800):
        previous = sum(check["label"] == label or check["label"].startswith(label + "-retry-")
                       for check in receipt["checks"])
        if previous:
            label += "-retry-" + str(previous)
        argv = ["rtk", "proxy", *map(str, command)]
        started = time.time_ns()
        try:
            proc = subprocess.run(argv, cwd=cwd, env=env, capture_output=True, timeout=timeout)
            stdout, stderr, code = proc.stdout, proc.stderr, proc.returncode
        except subprocess.TimeoutExpired as exc:
            stdout, stderr, code = exc.stdout or b"", exc.stderr or b"", 124
        for name, data in (("stdout", stdout), ("stderr", stderr)):
            (out / (label + "." + name)).write_bytes(data)
        receipt["checks"].append({"label": label, "argv": argv, "cwd": str(cwd),
            "start_ns": started, "finish_ns": time.time_ns(), "exit_code": code,
            "environment": {key: env[key] for key in (
                "CGO_ENABLED", "CGO_CFLAGS", "CGO_LDFLAGS", "TMPDIR",
                "MODSECURITY_INCLUDE_DIR", "NATIVE_OBSERVER_TEST_OUT") if key in env},
            "stdout_sha256": hashlib.sha256(stdout).hexdigest(),
            "stderr_sha256": hashlib.sha256(stderr).hexdigest()})
        save()
        print(json.dumps({"label": label, "exit_code": code}), flush=True)
        if code:
            raise RuntimeError(label + " failed; inspect " + str(out))
        return stdout

    try:
        if args.validate_existing:
            source_inventory.verify(source, receipt)
            module = source / "connectors/envoy/ext_proc"
            if receipt["module_inputs"] != {name: sha(module / name) for name in ("go.mod", "go.sum")}:
                raise ValueError("existing build Go module input hash mismatch")
            for relative, expected in receipt["binaries"].items():
                if sha(out / relative) != expected:
                    raise ValueError("existing build binary hash mismatch: " + relative)
            application = json.loads((source / "i12-source-application-receipt.json").read_text())
            for relative, expected in application["exact_written_sha256"].items():
                if sha(source / relative) != expected:
                    raise ValueError("existing source overlay hash mismatch: " + relative)
            if receipt["sdk_library"]["sha256"] != sha(args.sdk_library):
                raise ValueError("existing build SDK hash mismatch")
            env.update(receipt["environment"])
            env.update(MODSECURITY_LIB_DIR=str(args.sdk_library.parent),
                       PATH=str(args.go.parent) + os.pathsep + env["PATH"])
            if args.tmp_root:
                env["TMPDIR"] = str(args.tmp_root.absolute())
            receipt["validation_environment"] = {"TMPDIR": env["TMPDIR"]}
            validate(source, out, env, run, args.go, args.sdk_include, args.sdk_library, args.controls_only)
            receipt["status"] = "pass"
            receipt.pop("failure", None)
            save()
            return
        head = run("source-head", ["git", "rev-parse", "HEAD"]).decode().strip()
        archive = run("source-archive", ["git", "archive", "--format=tar", head])
        source.mkdir()
        with tarfile.open(fileobj=io.BytesIO(archive)) as stream:
            for member in stream.getmembers():
                target = source / member.name
                if (not target.is_relative_to(source) or ".." in Path(member.name).parts
                        or not (member.isfile() or member.isdir())):
                    raise ValueError("source archive contains unsupported entry: " + member.name)
            stream.extractall(source, filter="data")
        capture = load(source / "ci/runtime/lifecycle/i12/capture_sources.py", "envoy_capture")
        registry = capture.Registry(root=source / "ci/runtime/lifecycle/i12", repository=source)
        (source / capture.MARKER).write_text(json.dumps({
            "format": "i12-disposable-source-copy-v1", "path": str(source),
            "disposable": True, "parent_sha": registry.manifest["delivery_product_baseline"]}))
        receipt["actual_source_commit"] = head
        receipt["capture_marker_parent_is_historical_contract"] = True
        receipt["manifest_sha256"] = sha(source / "ci/runtime/lifecycle/i12/manifest.json")
        profile = registry.manifest["profiles"]["envoy"]
        receipt["source_before_overlay"] = {
            name: sha(source / name) for name in profile["source_targets"]}
        save()
        # The shared materializer verifies all original bytes before any overlay.
        receipt["capture_application"] = capture.apply(registry, "envoy", source)
        for name in profile["capture_files"]:
            if name.startswith("source-copy-tests/"):
                relative = name.removeprefix("source-copy-tests/")
                target = source / relative
                if target.exists():
                    raise ValueError("source-copy test already present: " + relative)
                target.write_bytes((source / ".i12-capture/envoy" / name).read_bytes())
        # The capture stores text modes; the native builder requires its helper executable.
        for name in ("build_ext_proc.sh", "build_composite.sh"):
            (source / "connectors/envoy/build" / name).chmod(0o755)
        receipt["source_copy_executable_modes"] = ["build_ext_proc.sh", "build_composite.sh"]
        receipt["complete_source_inventory"] = source_inventory.verify(source, receipt)
        module = source / "connectors/envoy/ext_proc"
        dependency_hashes = {name: sha(module / name) for name in ("go.mod", "go.sum")}
        receipt["module_inputs"] = dependency_hashes
        shutil.copytree(args.module_cache.resolve(strict=True), root / "offline-mod")
        (root / "tmp").mkdir()
        env.update(GOTOOLCHAIN="local", GOPROXY="off", GOSUMDB="off", GOWORK="off",
                   GOFLAGS="-mod=readonly -p=" + str(os.cpu_count() or 1),
                   GOMAXPROCS=str(os.cpu_count() or 1), GOCACHE=str(root / "go-cache"),
                   GOMODCACHE=str(root / "offline-mod"), TMPDIR=str(args.tmp_root.absolute() if args.tmp_root else root / "tmp"),
                   BUILD_ROOT=str(out / "build"), MODSECURITY_INCLUDE_DIR=str(args.sdk_include),
                   MODSECURITY_LIB_DIR=str(args.sdk_library.parent),
                   MODSECURITY_LIB_FILE=str(args.sdk_library),
                   PATH=str(args.go.parent) + os.pathsep + env["PATH"])
        receipt["environment"] = {key: env[key] for key in (
            "GOTOOLCHAIN", "GOPROXY", "GOSUMDB", "GOWORK", "GOFLAGS", "GOMAXPROCS",
            "GOCACHE", "GOMODCACHE", "TMPDIR", "BUILD_ROOT", "MODSECURITY_INCLUDE_DIR",
            "MODSECURITY_LIB_FILE")}
        receipt["sdk_library"] = {"path": str(args.sdk_library), "sha256": sha(args.sdk_library)}
        if sha(args.sdk_library) != profile["provenance"]["sdk_image_sha256"]:
            raise ValueError("SDK library differs from the selected capture contract")
        controls = load(source / "tests/test_native_lifecycle_observer.py", "envoy_observer_controls")
        symbols = controls.SYMBOLS
        if len(symbols) != 38 or len(set(symbols)) != 38:
            raise ValueError("expected exact shared 38-symbol observer contract")
        receipt["wrap_symbols"] = list(symbols)
        flags = ["-Wall", "-Wextra", "-Werror"]
        run("observer", ["gcc", "-std=c17", *flags, "-pthread", "-I", source / "common/include",
            "-I", args.sdk_include, "-c", source / "ci/runtime/lifecycle/native-lifecycle-observer.c",
            "-o", out / "observer.o"])
        # Re-adding /usr/include as -isystem changes include_next ordering in GCC.
        sdk_cpp_flags = [] if args.sdk_include == Path("/usr/include") else ["-isystem", args.sdk_include]
        run("accessor", ["g++", "-std=c++17", *flags, *sdk_cpp_flags, "-c",
            source / "ci/runtime/lifecycle/native-lifecycle-sdk.cpp", "-o", out / "accessor.o"])
        run("observer-archive", ["ar", "rcs", out / "libi12_envoy_observer.a",
            out / "observer.o", out / "accessor.o"])
        env["I12_ENVOY_OBSERVER_LDFLAGS"] = " ".join([str(out / "libi12_envoy_observer.a"),
            "-Wl,--undefined=msconnector_lifecycle_sdk_transaction_id",
            *("-Wl,--wrap=" + name for name in symbols)])
        run("go-version", [args.go, "version"])
        run("sdk-identity-build", ["gcc", "-std=c17", *flags, "-I", args.sdk_include,
            source / ".i12-capture/envoy/sdk-who.c", args.sdk_library, "-o", out / "sdk-who"])
        run("sdk-identity", [out / "sdk-who"])
        run("composite-build", ["sh", source / "connectors/envoy/build/build_composite.sh"], source)
        receipt["build_ready"] = True
        receipt["binaries"] = {str(path.relative_to(out)): sha(path) for path in (
            out / "build/envoy-ext-proc/msconnector_envoy_ext_proc",
            out / "build/envoy-composite/msconnector_composite")}
        ready = root / "host-ready-bin"
        ready.mkdir()
        for relative in receipt["binaries"]:
            shutil.copy2(out / relative, ready / Path(relative).name)
        receipt["host_ready_binaries"] = str(ready)
        save()
        validate(source, out, env, run, args.go, args.sdk_include, args.sdk_library)
        if dependency_hashes != {name: sha(module / name) for name in dependency_hashes}:
            raise ValueError("Go module input mutated")
        receipt["status"] = "pass"
        save()
    except Exception as exc:
        receipt["status"], receipt["failure"] = "failed", str(exc)
        save()
        raise


if __name__ == "__main__":
    main()
