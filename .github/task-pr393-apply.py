#!/usr/bin/env python3
"""Temporary, isolated PR 393 repair preparation; never included in its repair tree."""
from pathlib import Path
import ast
import hashlib
import importlib.util
import json
import os
import subprocess
import sys
import urllib.request

HEAD = "bbd74521ee9b1c7544b11c225e399a1c7f8d49da"
BASE = "d56af0856507eb048987974d3960e301e7c24371"
OLD = "f9e48b0774b5bdf7aaa8e38ce98eb6c50bf293c8"
NEW = "0290a979ba4bc63a7abed175a53471367b385553"
FRAMEWORK = "modules/ModSecurity-test-Framework"
DIGEST = "2c3a5774da760981804907a357dc5dafb62f9ba3de1db17a2807ff53fd83c291"
NGINX_SHA = "974ed5298a5e398e008704ed5db284e655fc270c596493dbccada452448fc9f1"
WRITER = "ci/runtime/lifecycle/write-nginx-functional-a-evidence.py"
GATE_TEST = "tests/test_nginx_exact_head_gate_contract.py"
EVIDENCE_TEST = "tests/test_nginx_functional_evidence.py"
CACHE_TEST = "tests/test_runtime_component_cache_identity.py"
QUICK = ".github/workflows/quick-framework-check.yml"
SANDBOX_TEST = "tests/test_prepare_readonly_submodule_validation_sandbox.py"
NAMESPACE_TEST = "tests/test_run_readonly_submodule_validation_namespace.py"
NEW_PATHS = (
    "ci/tools/check-reviewed-version-handoff.py",
    "tests/test_reviewed_version_handoff.py",
    "docs/reviewed-version-upgrades.md",
    "docs/reviewed-version-upgrades.de.md",
    "reports/audits/change-records/CR-20260930-complete-framework-handoff.md",
    "reports/audits/change-records/CR-20260930-complete-framework-handoff.de.md",
)


def require(condition, message):
    if not condition:
        raise ValueError(message)


def git(root, *args):
    result = subprocess.run(["git", "-C", str(root), *args], check=True,
                            stdout=subprocess.PIPE, timeout=300)
    return result.stdout


def blob(data):
    return hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data,
                        usedforsecurity=False).hexdigest()


def read_bounded(url, limit):
    request = urllib.request.Request(url)
    with urllib.request.urlopen(request, timeout=120) as response:
        payload = response.read(limit + 1)
    require(len(payload) <= limit, "Upstream response exceeds bound")
    return payload


def replace_once(text, before, after, label):
    require(text.count(before) == 1, "Unexpected source precondition: " + label)
    return text.replace(before, after, 1)


NGINX_TESTS = r'''    def test_writer_version_matches_the_exact_head_workflow(self) -> None:
        workflow = yaml.safe_load(
            (ROOT / ".github/workflows/test-nginx-exact-head.yml").read_text(encoding="utf-8")
        )
        release = workflow["jobs"]["nginx-exact-head"]["env"]["NGINX_RELEASE_TAG"]
        self.assertEqual(release, "release-1.31.6")
        self.assertEqual(WRITER_MODULE.EXPECTED_NGINX_VERSION, release.removeprefix("release-"))

    def test_unreviewed_nginx_version_blocks_collection(self) -> None:
        for mode in ("on", "off"):
            for version in ("1.31.5", "1.31.7", "1.31.60", "1.31.6.1", "1.31.6-unreviewed"):
                with self.subTest(mode=mode, version=version):
                    self._write_mode("on")
                    self._write_mode("off")
                    target = self.functional_root / mode / "phase4" / "logs" / "nginx-version.log"
                    self._write_private(target, f"nginx version: nginx/{version}\n".encode("ascii"))
                    with self.assertRaisesRegex(WRITER_MODULE.EvidenceError, "did not use NGINX"):
                        self.collect()
                    self.assertFalse((self.evidence_root / "result.json").exists())

    def test_malformed_or_conflicting_version_readback_is_rejected(self) -> None:
        for payload in (
            b"prefix nginx/1.31.6\n",
            b"nginx version: nginx/1.31.6\nnginx version: nginx/1.31.5\n",
            b"nginx version: nginx/1.31.6\nnginx version: nginx/1.31.6\n",
        ):
            with self.subTest(payload=payload):
                self._write_mode("on")
                target = self.functional_root / "on" / "phase4" / "logs" / "nginx-version.log"
                self._write_private(target, payload)
                with self.assertRaisesRegex(WRITER_MODULE.EvidenceError, "did not use NGINX"):
                    self.collect()
                self.assertFalse((self.evidence_root / "result.json").exists())

'''

CACHE_TESTS = r'''    def _upgrade_modsecurity_inputs(self, record, env=None):
        expat = {
            "actual_head": "expat-source", "prefix": "/cache/expat",
            "cache_key": "expat-key",
            "cache_identity": {"cache_key": "expat-key", "source_sha256": "expat-source"},
        }
        with mock.patch.object(components, "toolchain_identity", return_value={"cc": "cc"}), \
             mock.patch.object(components, "patchset_identity", return_value={"sha256": "patchset", "files": []}):
            return components.modsecurity_build_inputs(env or {}, record, expat, ROOT)

    def test_modsecurity_upgrade_changes_source_submodule_and_flag_cache_identity(self) -> None:
        record = {
            "url": "https://github.com/owasp-modsecurity/ModSecurity.git",
            "expected_ref": "fixture-release", "actual_head": "a" * 40,
            "submodule_status": "fixture-submodules-a",
        }
        baseline = self._upgrade_modsecurity_inputs(record)
        for field, value in (("actual_head", "b" * 40),
                             ("expected_ref", "fixture-next-release"),
                             ("submodule_status", "fixture-submodules-b")):
            with self.subTest(field=field):
                changed = self._upgrade_modsecurity_inputs({**record, field: value})
                self.assertNotEqual(baseline["cache_key"], changed["cache_key"])
        changed_flags = self._upgrade_modsecurity_inputs(record, {"CXXFLAGS": "-O0"})
        self.assertNotEqual(baseline["cache_key"], changed_flags["cache_key"])

    def test_connector_is_rebuilt_for_a_different_modsecurity_build(self) -> None:
        for connector in ("apache", "nginx"):
            with self.subTest(connector=connector):
                before = self.connector_plan({}, [], connector=connector)
                after = self.connector_plan({}, [], connector=connector,
                                            modsecurity_build_id="next-modsecurity-build")
                self.assertNotEqual(before["connector_build_id"], after["connector_build_id"])

    def test_modsecurity_runtime_aliases_allow_changed_v3_terminal_suffix(self) -> None:
        # Synthetic filenames, not a claim that a corresponding release exists.
        for suffix in ("0.16", "99.99"):
            with self.subTest(suffix=suffix), tempfile.TemporaryDirectory() as temporary:
                root = Path(temporary)
                terminal = root / f"libmodsecurity.so.3.{suffix}"
                terminal.write_bytes(b"fixture-library")
                terminal.chmod(0o644)
                (root / "libmodsecurity.so.3").symlink_to(terminal.name)
                (root / "libmodsecurity.so").symlink_to("libmodsecurity.so.3")
                descriptor, details = components._verified_modsecurity_runtime_library(root)
                try:
                    self.assertEqual(os.read(descriptor, 128), b"fixture-library")
                    self.assertEqual(details.st_ino, terminal.stat().st_ino)
                finally:
                    os.close(descriptor)

    def test_unreviewed_modsecurity_soname_is_not_silently_accepted(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            terminal = root / "libmodsecurity.so.4.0.0"
            terminal.write_bytes(b"unreviewed-layout")
            terminal.chmod(0o644)
            (root / "libmodsecurity.so.3").symlink_to(terminal.name)
            (root / "libmodsecurity.so").symlink_to("libmodsecurity.so.3")
            with self.assertRaisesRegex(RuntimeError, "terminal_name_invalid"):
                components._verified_modsecurity_runtime_library(root)

'''

NAMESPACE_REGRESSION = '''    def test_external_virtualenv_alias_resolves_to_existing_jail_runtime(self) -> None:
        """Resolve a venv alias without adding its writable parent to the jail."""
        if sys.platform != "linux":
            self.skipTest("Linux runtime layout is required")
        system_python = Path("/usr/bin/python3").resolve(strict=True)
        self.assertTrue(HELPER._runtime_path_is_exposed(system_python))
        with tempfile.TemporaryDirectory(prefix="external-python-alias-") as raw:
            alias = Path(raw) / "python"
            alias.symlink_to(system_python)
            with self.assertRaisesRegex(RuntimeError, "outside the jailed runtime allowlist"):
                HELPER._hosted_python_runtime_root(alias)
            resolved = alias.resolve(strict=True)
            self.assertEqual(resolved, system_python)
            self.assertIsNone(HELPER._hosted_python_runtime_root(resolved))

'''


def repair_namespace_test(text, method):
    nodes = [n for n in ast.walk(ast.parse(text)) if isinstance(n, ast.FunctionDef) and n.name == method]
    require(len(nodes) == 1, "Unexpected namespace test method")
    node = nodes[0]
    lines = text.splitlines(keepends=True)
    part = "".join(lines[node.lineno-1:node.end_lineno])
    part = replace_once(part, "Path(sys.executable)", "Path(sys.executable).resolve(strict=True)", method)
    part = replace_once(part, "except BaseException:\n", "except BaseException as error:\n", method)
    at = part.index("except BaseException as error:\n") + len("except BaseException as error:\n")
    tail_line = part[at:].splitlines()[0]
    indentation = tail_line[:len(tail_line)-len(tail_line.lstrip())]
    require(tail_line.strip() == "os._exit(1)", "Unexpected fork failure handler")
    diagnostic = indentation + 'os.write(2, ("namespace test child failed: " + type(error).__name__ + ": " + ascii(str(error))[:500] + "\\n").encode("ascii"))\n'
    part = part[:at] + diagnostic + part[at:]
    return "".join(lines[:node.lineno-1]) + part + "".join(lines[node.end_lineno:])


def amend_tests(desired, root):
    desired[WRITER] = replace_once(desired[WRITER], 'EXPECTED_NGINX_VERSION = "1.31.5"\n',
                                  'EXPECTED_NGINX_VERSION = "1.31.6"\n', WRITER)
    desired[WRITER] = replace_once(
        desired[WRITER],
        '    if f"nginx/{EXPECTED_NGINX_VERSION}".encode("ascii") not in sources["nginx_version"]:\n',
        '    expected_version = b"nginx version: nginx/" + EXPECTED_NGINX_VERSION.encode("ascii")\n'
        '    if sources["nginx_version"].splitlines() != [expected_version]:\n',
        "exact single-line version readback")
    gate = replace_once(desired[GATE_TEST], "import unittest\n", "import unittest\n\nimport yaml\n", GATE_TEST)
    desired[GATE_TEST] = replace_once(gate,
        '        self.assertIn("permissions:\\n  contents: read", workflow)\n',
        '        parsed = yaml.safe_load(workflow)\n'
        '        self.assertEqual(parsed["permissions"], {})\n'
        '        self.assertEqual(\n'
        '            parsed["jobs"]["nginx-exact-head"]["permissions"], {"contents": "read"}\n'
        '        )\n', "job-scoped permissions")
    tests = replace_once(desired[EVIDENCE_TEST], "from unittest import mock\n",
                         "from unittest import mock\n\nimport yaml\n", EVIDENCE_TEST)
    needle = "    def test_canary_in_jsonl_blocks_publication(self) -> None:\n"
    desired[EVIDENCE_TEST] = replace_once(tests, needle, NGINX_TESTS + needle, EVIDENCE_TEST)
    cache = replace_once(desired[CACHE_TEST], "import importlib.util\n", "import importlib.util\nimport os\n", CACHE_TEST)
    cache = replace_once(cache, '        connector: str = "apache",\n',
                         '        connector: str = "apache",\n        modsecurity_build_id: str = "modsecurity-build",\n', CACHE_TEST)
    cache = replace_once(cache, '{"build_id": "modsecurity-build", "prefix": "/cache/modsecurity"}',
                         '{"build_id": modsecurity_build_id, "prefix": "/cache/modsecurity"}', CACHE_TEST)
    desired[CACHE_TEST] = replace_once(cache, '\n\nif __name__ == "__main__":',
                         '\n\n' + CACHE_TESTS + '\nif __name__ == "__main__":', CACHE_TEST)
    needle = '          python3 -m unittest -v tests.test_change_record tests.test_prepare_reviewed_framework_handoff\n'
    desired[QUICK] = replace_once(desired[QUICK], needle,
        needle + '          python3 ci/tools/check-reviewed-version-handoff.py --repo-root .\n'
        '          python3 -m unittest -v tests.test_reviewed_version_handoff\n', QUICK)
    for path, method in (
        (SANDBOX_TEST, "test_prepare_candidate_verify_and_cleanup_preserve_source_metadata"),
        (NAMESPACE_TEST, "test_privileged_candidate_cannot_escape_the_chroot_or_outlive_pid1"),
    ):
        desired[path] = repair_namespace_test((root/path).read_text(), method)
    desired[NAMESPACE_TEST] = replace_once(desired[NAMESPACE_TEST], '\n\nif __name__ == "__main__":',
        '\n\n' + NAMESPACE_REGRESSION + '\nif __name__ == "__main__":', "venv alias regression")


def prepare():
    root = Path(os.environ["TARGET_ROOT"]).resolve(strict=True)
    source = Path(os.environ["GITHUB_WORKSPACE"]).resolve(strict=True)
    temp = Path(os.environ["RUNNER_TEMP"])
    require(git(root, "rev-parse", "HEAD").decode().strip() == HEAD, "Parent head changed")
    generator_path = root / "ci/tools/prepare-reviewed-framework-handoff.py"
    require(blob(generator_path.read_bytes()) == "8737184da5f71d7cb599f868e8a4858f8e10d84b", "Generator drift")
    spec = importlib.util.spec_from_file_location("reviewed_generator", generator_path)
    require(spec is not None, "Generator specification unavailable")
    require(spec.loader is not None, "Generator loader unavailable")
    generator = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(generator)
    framework = root / FRAMEWORK
    require(git(framework, "rev-parse", "HEAD").decode().strip() == OLD, "Unexpected original gitlink")
    git(framework, "fetch", "--no-tags", "--no-recurse-submodules", "origin", NEW)
    git(framework, "merge-base", "--is-ancestor", OLD, NEW)
    require(git(framework, "ls-tree", OLD, "--", "tools/MRTS") ==
            git(framework, "ls-tree", NEW, "--", "tools/MRTS"), "MRTS gitlink changed")
    previous = git(framework, "show", OLD + ":ci/lib/common.sh")
    candidate = git(framework, "show", NEW + ":ci/lib/common.sh")
    require(generator.reviewed_candidate_digest(previous.decode(), candidate.decode()) == DIGEST,
            "Candidate delta/digest mismatch")
    release = json.loads(read_bounded("https://api.github.com/repos/nginx/nginx/releases/tags/release-1.31.6", 2*1024*1024))
    assets = [a for a in release["assets"] if a["name"] == "nginx-1.31.6.tar.gz"]
    require(not release["draft"] and not release["prerelease"] and len(assets) == 1, "Unexpected release")
    require(assets[0].get("digest") == "sha256:" + NGINX_SHA, "NGINX metadata digest mismatch")
    archive = read_bounded("https://github.com/nginx/nginx/releases/download/release-1.31.6/nginx-1.31.6.tar.gz", 16*1024*1024)
    require(hashlib.sha256(archive).hexdigest() == NGINX_SHA, "NGINX archive digest mismatch")
    candidate_path = temp / "candidate-common.sh"
    candidate_path.write_bytes(candidate)
    baseline = subprocess.run([sys.executable, "ci/tools/verify-framework-candidate-contract.py",
        "--repo-root", str(root), "--candidate-sha", NEW, "--framework-common", str(candidate_path),
        "--expected-parent-framework-sha", OLD], cwd=root, capture_output=True, text=True, timeout=120)
    print("Baseline verifier exit:", baseline.returncode, flush=True)
    print(baseline.stdout + baseline.stderr, flush=True)
    require(baseline.returncode == 2 and "differs from approved reviewed structure" in baseline.stderr,
            "Original verifier failure was not reproduced")
    originals = {}
    for path in generator.TARGET_PATHS:
        data = git(root, "show", BASE + ":" + path)
        require((root/path).read_bytes() == data, "Changed target since review: " + path)
        originals[path] = data.decode()
    desired = generator.build_changes(originals, DIGEST)
    writer = (root/WRITER).read_bytes()
    require(blob(writer) == "20eb6e33795e3fd7bcbb068de0897beab60fe08b", "Writer drift")
    desired[WRITER] = writer.decode()
    desired[QUICK] = (root/QUICK).read_text()
    amend_tests(desired, root)
    for path in NEW_PATHS:
        require(not (root/path).exists(), "New target already exists: " + path)
        desired[path] = (source/path).read_text(encoding="utf-8")
    for path, text in desired.items():
        if path.endswith(".py"):
            ast.parse(text, filename=path)
        require(not any(line.rstrip() != line for line in text.splitlines()), "Trailing whitespace: " + path)
        destination = root/path
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_text(text, encoding="utf-8", newline="")
    git(root, "add", "--", *sorted(desired))
    git(root, "update-index", "--cacheinfo", "160000," + NEW + "," + FRAMEWORK)
    git(root, "-c", "protocol.file.allow=never", "submodule", "update", "--init", "--recursive", "--checkout", "--", FRAMEWORK)
    require((framework/"ci/lib/common.sh").read_bytes() == candidate, "Checkout/candidate mismatch")
    (temp/"repair-paths.json").write_text(json.dumps(sorted(desired)))
    (temp/"repair-tree.txt").write_bytes(git(root, "write-tree"))
    git(root, "diff", "--cached", "--check")
    git(root, "diff", "--cached", "--exit-code", "--", ".github/workflows/nginx-root-broker.yml", "ci/runtime/broker")
    print("Prepared source corrections:", len(desired), "text files and one Framework gitlink", flush=True)
    print("Reviewed structure SHA256:", DIGEST, flush=True)


if __name__ == "__main__":
    prepare()
