from __future__ import annotations

import importlib.util
from pathlib import Path
import re
import shlex
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
GENERATOR_PATH = ROOT / "scripts" / "generate_compiler_guides.py"


def load_generator() -> object:
    spec = importlib.util.spec_from_file_location("compiler_guides_generator", GENERATOR_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load generator: {GENERATOR_PATH}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


GENERATOR = load_generator()


ENGLISH_HEADINGS = [
    "Purpose and current integration route",
    "Compare the three paths",
    "Shared prerequisites",
    "Path 1: Repository-controlled test",
    "Path 2: Local source build",
    "Path 3: Package or package-assisted installation",
    "Configure after the build",
    "Validate build and installation",
    "Run a real HTTP/1.1 test",
    "Inspect evidence and logs",
    "Update and rebuild",
    "Uninstall and clean up",
    "Troubleshooting",
    "Variables and placeholders",
    "Limitations and non-claims",
]

GERMAN_HEADINGS = [
    "Zweck und aktueller Integrationspfad",
    "Die drei Wege im Vergleich",
    "Gemeinsame Voraussetzungen",
    "Weg 1: Repository-gesteuert testen",
    "Weg 2: Lokal aus Source bauen",
    "Weg 3: Über Pakete beziehungsweise paketgestützt installieren",
    "Nach dem Build konfigurieren",
    "Build und Installation validieren",
    "Realen HTTP/1.1-Test ausführen",
    "Evidence und Logs prüfen",
    "Aktualisieren und neu bauen",
    "Deinstallieren und bereinigen",
    "Troubleshooting",
    "Variablen und Platzhalter",
    "Einschränkungen und nicht erhobene Claims",
]


def headings(content: str) -> list[str]:
    return re.findall(r"^## (.+)$", content, flags=re.MULTILINE)


def make_targets(makefile: Path) -> set[str]:
    """Collect explicit target names without running any Make target."""
    text = makefile.read_text(encoding="utf-8").replace("\\\n", " ")
    targets: set[str] = set()
    for line in text.splitlines():
        if line.startswith(".PHONY:"):
            targets.update(token for token in line.split()[1:] if "=" not in token)
            continue
        match = re.match(r"^([A-Za-z0-9_.% -]+):", line)
        if match:
            targets.update(token for token in match.group(1).split() if "%" not in token)
    return targets


def documented_make_commands(content: str) -> list[tuple[Path, str]]:
    commands: list[tuple[Path, str]] = []
    for block in re.findall(r"```sh\n(.*?)\n```", content, flags=re.DOTALL):
        for line in block.splitlines():
            tokens = shlex.split(line)
            while tokens and re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]*=.*", tokens[0]):
                tokens.pop(0)
            if not tokens or tokens.pop(0) != "make":
                continue
            directory = None
            if tokens[:1] == ["-C"]:
                tokens.pop(0)
                if not tokens:
                    continue
                directory = tokens.pop(0)
            if not tokens:
                continue
            target = tokens.pop(0)
            commands.append((ROOT / directory if directory else ROOT, target))
    return commands


class CompilerGuideGenerationTest(unittest.TestCase):
    maxDiff = None

    def test_expected_files_are_generated_and_current(self) -> None:
        rendered = GENERATOR.rendered_files()
        expected = {
            "README.md",
            "README.de.md",
            "overview.md",
            "overview.de.md",
            *{
                f"{slug}{suffix}.md"
                for slug in ("apache", "nginx", "haproxy", "envoy", "traefik", "lighttpd")
                for suffix in ("", ".de")
            },
        }
        self.assertEqual(expected, set(rendered))
        on_disk_names = {path.name for path in (ROOT / "docs" / "build" / "compilers").glob("*.md")}
        self.assertEqual(expected, on_disk_names)
        for name, generated in rendered.items():
            on_disk = (ROOT / "docs" / "build" / "compilers" / name).read_text(encoding="utf-8")
            self.assertEqual(generated.rstrip() + "\n", on_disk, name)

    def test_rendering_is_idempotent(self) -> None:
        with tempfile.TemporaryDirectory(prefix="compiler-guide-render-") as temporary:
            original_output = GENERATOR.OUTPUT
            GENERATOR.OUTPUT = Path(temporary)
            try:
                GENERATOR.main()
                first = {
                    path.name: path.read_text(encoding="utf-8")
                    for path in GENERATOR.OUTPUT.glob("*.md")
                }
                GENERATOR.main()
                second = {
                    path.name: path.read_text(encoding="utf-8")
                    for path in GENERATOR.OUTPUT.glob("*.md")
                }
            finally:
                GENERATOR.OUTPUT = original_output
        self.assertEqual(first, second)

    def test_indexes_cover_all_connectors_and_package_statuses(self) -> None:
        for german, name in ((False, "README.md"), (True, "README.de.md")):
            index = (ROOT / "docs" / "build" / "compilers" / name).read_text(encoding="utf-8")
            suffix = ".de" if german else ""
            for connector in GENERATOR.CONNECTORS:
                slug = connector["slug"]
                self.assertIn(f"({slug}{suffix}.md)", index)
                self.assertIn(f"`make {connector['full']}`", index)
                self.assertIn(f"`{GENERATOR.DETAILS[slug]['package_status']}`", index)
        for german, name in ((False, "overview.md"), (True, "overview.de.md")):
            overview = (ROOT / "docs" / "build" / "compilers" / name).read_text(encoding="utf-8")
            suffix = ".de" if german else ""
            for connector in GENERATOR.CONNECTORS:
                self.assertIn(f"({connector['slug']}{suffix}.md)", overview)
                self.assertIn(f"`{connector['full']}`", overview)

    def test_connector_data_has_required_structured_fields(self) -> None:
        required = {
            "package_status",
            "test_prerequisites",
            "test_commands",
            "source_prerequisites",
            "source_commands",
            "source_validation",
            "package_debian",
            "package_fedora",
            "package_notes",
            "package_validation",
            "cleanup_commands",
        }
        allowed_statuses = {
            "package-only",
            "package-assisted source build",
            "selected profile not available package-only",
        }
        for connector in GENERATOR.CONNECTORS:
            detail = GENERATOR.DETAILS[connector["slug"]]
            self.assertTrue(required.issubset(detail), connector["slug"])
            self.assertIn(detail["package_status"], allowed_statuses, connector["slug"])
            for field in required - {"package_status"}:
                self.assertTrue(detail[field], f"{connector['slug']} missing {field}")
            self.assertIn("pkg-config --atleast-version=3.0 libmodsecurity", detail["package_validation"])
            self.assertTrue(
                any("major version must be 3" in command for command in detail["package_validation"]),
                connector["slug"],
            )
            self.assertIn(
                f'NO_CRS_RUN_ID="$run_id" make {connector["full"]}',
                detail["source_commands"],
                connector["slug"],
            )
            self.assertIn(
                f'NO_CRS_RUN_ID="$run_id" make evidence-check-{connector["slug"]}',
                detail["source_validation"],
                connector["slug"],
            )

    def test_every_connector_has_all_three_paths_and_bilingual_structure(self) -> None:
        for connector in GENERATOR.CONNECTORS:
            slug = connector["slug"]
            english = (ROOT / "docs" / "build" / "compilers" / f"{slug}.md").read_text(encoding="utf-8")
            german = (ROOT / "docs" / "build" / "compilers" / f"{slug}.de.md").read_text(encoding="utf-8")
            self.assertEqual(ENGLISH_HEADINGS, headings(english), slug)
            self.assertEqual(GERMAN_HEADINGS, headings(german), slug)
            self.assertEqual(len(headings(english)), len(headings(german)), slug)
            self.assertIn(f"`{GENERATOR.DETAILS[slug]['package_status']}`", english)
            self.assertIn(f"`{GENERATOR.DETAILS[slug]['package_status']}`", german)

    def test_bilingual_guides_share_technical_values(self) -> None:
        for connector in GENERATOR.CONNECTORS:
            slug = connector["slug"]
            detail = GENERATOR.DETAILS[slug]
            english = (ROOT / "docs" / "build" / "compilers" / f"{slug}.md").read_text(encoding="utf-8")
            german = (ROOT / "docs" / "build" / "compilers" / f"{slug}.de.md").read_text(encoding="utf-8")
            tokens = {
                connector["build"],
                connector["config"],
                connector["start"],
                connector["runtime"],
                connector["full"],
                f"evidence-check-{slug}",
                detail["package_status"],
                *detail["test_commands"],
                *detail["source_commands"],
                *detail["source_validation"],
                *GENERATOR.HOST_VALIDATION[slug],
                *GENERATOR.ARTIFACT_VALIDATION[slug],
                *GENERATOR.TEST_HOST_VALIDATION[slug],
                *GENERATOR.TEST_ARTIFACT_VALIDATION[slug],
                *detail["package_debian"],
                *detail["package_fedora"],
                *detail.get("package_host_query", ()),
                *detail["package_validation"],
                *detail["cleanup_commands"],
            }
            for pin in detail["pins"]:
                tokens.update(pin)
            for variable, default, example, _, _ in detail["vars"]:
                tokens.update((variable, default, example))
            for key in ("go_requirement", "go_module"):
                if key in detail:
                    tokens.add(detail[key])
            for token in tokens:
                self.assertIn(str(token), english, f"{slug} English missing {token!r}")
                self.assertIn(str(token), german, f"{slug} German missing {token!r}")

    def test_path_sections_have_reproducible_handoffs(self) -> None:
        for connector in GENERATOR.CONNECTORS:
            slug = connector["slug"]
            detail = GENERATOR.DETAILS[slug]
            english = (ROOT / "docs" / "build" / "compilers" / f"{slug}.md").read_text(encoding="utf-8")
            path_one = english.split("## Path 1: Repository-controlled test\n", 1)[1].split(
                "## Path 2: Local source build\n", 1
            )[0]
            path_three = english.split("## Path 3: Package or package-assisted installation\n", 1)[1].split(
                "## Configure after the build\n", 1
            )[0]
            for command in (
                "git clone --recurse-submodules https://github.com/Easton97-Jens/ModSecurity-conector.git",
                "git switch feature/all-connectors-no-crs-baseline",
                "git submodule update --init --recursive",
                "make check-framework",
                "make prepare-runtime-components",
                f"make {connector['build']}",
                f"make {connector['config']}",
                f"make {connector['start']}",
                f"make {connector['runtime']}",
                f"make {connector['full']}",
                f"make evidence-check-{slug}",
            ):
                self.assertIn(command, path_one, f"{slug}: test path missing {command}")
            for command in (*GENERATOR.TEST_HOST_VALIDATION[slug], *GENERATOR.TEST_ARTIFACT_VALIDATION[slug]):
                self.assertIn(command, path_one, f"{slug}: test-path validation missing {command}")
            self.assertIn("Debian / Ubuntu (apt)", path_three, slug)
            self.assertIn("Fedora / RHEL / Rocky Linux / AlmaLinux (dnf)", path_three, slug)
            self.assertIn("pkg-config --atleast-version=3.0 libmodsecurity", path_three, slug)
            if detail["package_status"] != "package-only":
                for command in detail["source_commands"]:
                    self.assertIn(command, path_three, f"{slug}: package handoff missing {command}")
                for command in detail["source_validation"]:
                    self.assertIn(command, path_three, f"{slug}: package validation missing {command}")
            source_path = english.split("## Path 2: Local source build\n", 1)[1].split(
                "## Path 3: Package or package-assisted installation\n", 1
            )[0]
            for command in GENERATOR.ARTIFACT_VALIDATION[slug]:
                self.assertIn(command, source_path, f"{slug}: source validation missing {command}")
                self.assertIn(command, path_three, f"{slug}: package validation missing {command}")

    def test_documented_make_targets_exist_without_running_builds(self) -> None:
        root_targets = make_targets(ROOT / "Makefile")
        makefiles = {ROOT: root_targets}
        for guide in sorted((ROOT / "docs" / "build" / "compilers").glob("*.md")):
            content = guide.read_text(encoding="utf-8")
            for directory, target in documented_make_commands(content):
                makefile = directory / "Makefile"
                self.assertTrue(makefile.is_file(), f"{guide}: missing Makefile for {directory}")
                if directory not in makefiles:
                    makefiles[directory] = make_targets(makefile)
                self.assertIn(target, makefiles[directory], f"{guide}: unsupported target {target}")

    def test_generated_guides_do_not_contain_unsafe_or_stale_text(self) -> None:
        forbidden_claims = (
            "production-ready",
            "production hardened",
            "security verified",
            "CRS verified",
            "full matrix verified",
        )
        for guide in (ROOT / "docs" / "build" / "compilers").glob("*.md"):
            content = guide.read_text(encoding="utf-8")
            self.assertIn(GENERATOR.MARKER, content, guide)
            self.assertNotIn("/root/", content, guide)
            self.assertNotIn("/var/tmp/", content, guide)
            self.assertNotIn("COMPILE_", content, guide)
            self.assertNotRegex(content, r"<[A-Za-z][^>]*>", guide)
            for claim in forbidden_claims:
                self.assertNotIn(claim.lower(), content.lower(), f"{guide}: {claim}")


if __name__ == "__main__":
    unittest.main()
