from __future__ import annotations

import importlib.util
from pathlib import Path
import re
import tempfile
import unittest
from urllib.parse import urlparse


ROOT = Path(__file__).resolve().parents[1]
GENERATOR_PATH = ROOT / "scripts" / "generate_compiler_guides.py"
GUIDE_DIRECTORY = ROOT / "docs" / "build" / "compilers"
SLUGS = ("apache", "nginx", "haproxy", "envoy", "traefik", "lighttpd")
COMMON_BEGINNER_COMMANDS = (
    "git clone https://github.com/owasp-modsecurity/ModSecurity.git",
    "cd ModSecurity",
    "git submodule update --init --recursive",
    "git submodule status",
    "./build.sh",
    "./configure",
    "make",
    "sudo make install",
)

ENGLISH_HEADINGS = [
    "1. Purpose and selected integration path",
    "2. Build components",
    "3. Official upstream documentation",
    "4. Prerequisites",
    "5. Prepare libmodsecurity v3",
    "6. Provide the host or proxy",
    "7. Build and integrate the connector",
    "8. Configuration",
    "9. Build and ABI validation",
    "10. Local HTTP/1.1 functional test",
    "11. Package-assisted path",
    "12. Repository-controlled test path",
    "13. Update and rebuild",
    "14. Uninstall and cleanup",
    "15. Troubleshooting",
    "16. Variables and placeholders",
    "17. Boundaries and non-claims",
]

GERMAN_HEADINGS = [
    "1. Zweck und ausgewählter Integrationspfad",
    "2. Komponenten des Builds",
    "3. Offizielle Upstream-Dokumentation",
    "4. Voraussetzungen",
    "5. ModSecurity vorbereiten",
    "6. Host oder Proxy bereitstellen",
    "7. Connector bauen und einbinden",
    "8. Konfiguration",
    "9. Build- und ABI-Validierung",
    "10. Lokaler HTTP/1.1-Funktionstest",
    "11. Paketgestützter Weg",
    "12. Repository-gesteuerter Testweg",
    "13. Aktualisieren und neu bauen",
    "14. Deinstallation und Cleanup",
    "15. Troubleshooting",
    "16. Variablen und Platzhalter",
    "17. Grenzen und nicht erhobene Claims",
]


def load_generator() -> object:
    spec = importlib.util.spec_from_file_location("compiler_guides_generator", GENERATOR_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load generator: {GENERATOR_PATH}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


GENERATOR = load_generator()


def guide(slug: str, german: bool = False) -> str:
    suffix = ".de" if german else ""
    return (GUIDE_DIRECTORY / f"{slug}{suffix}.md").read_text(encoding="utf-8")


def common_guide(german: bool = False) -> str:
    suffix = ".de" if german else ""
    return (GUIDE_DIRECTORY / f"libmodsecurity{suffix}.md").read_text(encoding="utf-8")


def headings(content: str) -> list[str]:
    return re.findall(r"^## (.+)$", content, flags=re.MULTILINE)


def numbered_section(content: str, number: int) -> str:
    start = re.search(rf"^## {number}\. .+$", content, flags=re.MULTILINE)
    if start is None:
        raise AssertionError(f"missing section {number}")
    end = re.search(rf"^## {number + 1}\. .+$", content[start.end() :], flags=re.MULTILINE)
    return content[start.start() : start.end() + (end.start() if end else len(content))]


def h2_section(content: str, heading: str) -> str:
    start = re.search(rf"^## {re.escape(heading)}$", content, flags=re.MULTILINE)
    if start is None:
        raise AssertionError(f"missing heading: {heading}")
    end = re.search(r"^## (?!#)", content[start.end() :], flags=re.MULTILINE)
    return content[start.start() : start.end() + (end.start() if end else len(content))]


def h3_section(content: str, heading: str) -> str:
    start = re.search(rf"^### {re.escape(heading)}$", content, flags=re.MULTILINE)
    if start is None:
        raise AssertionError(f"missing heading: {heading}")
    end = re.search(r"^(?:## |### )(?!#)", content[start.end() :], flags=re.MULTILINE)
    return content[start.start() : start.end() + (end.start() if end else len(content))]


def shell_blocks(content: str) -> list[str]:
    return re.findall(r"```sh\n(.*?)\n```", content, flags=re.DOTALL)


def nonempty_shell_lines(content: str) -> list[str]:
    return [line for line in content.splitlines() if line.strip()]


def variable_names(content: str) -> set[str]:
    variables = numbered_section(content, 16)
    return set(re.findall(r"^\| ([A-Za-z_][A-Za-z0-9_]*) \|", variables, flags=re.MULTILINE))


def shell_variables(content: str) -> set[str]:
    return set(re.findall(r"\$\{?([A-Za-z_][A-Za-z0-9_]*)", "\n".join(shell_blocks(content))))


def shell_assignments(content: str) -> list[str]:
    return re.findall(r"^([A-Za-z_][A-Za-z0-9_]*)=", "\n".join(shell_blocks(content)), flags=re.MULTILINE)


def target_exists(target: str) -> bool:
    makefile = (ROOT / "Makefile").read_text(encoding="utf-8")
    if re.search(rf"^{re.escape(target)}(?:[\s:]|$)", makefile, flags=re.MULTILINE):
        return True
    return any(
        target in line.split()[1:]
        for line in makefile.splitlines()
        if line.startswith(".PHONY:")
    )


def is_allowed_official_url(url: str) -> bool:
    parsed = urlparse(url)
    if parsed.scheme != "https" or not parsed.netloc:
        return False
    origin_and_path = f"{parsed.netloc}{parsed.path}".rstrip("/")
    return any(
        origin_and_path == allowed or origin_and_path.startswith(f"{allowed}/")
        for allowed in GENERATOR.OFFICIAL_DOMAINS
    )


class CompilerGuideGenerationTest(unittest.TestCase):
    maxDiff = None

    def test_generator_model_contains_one_shared_engine_contract(self) -> None:
        common = GENERATOR.COMMON_MODSECURITY
        for key in (
            "common_modsecurity_beginner_commands",
            "common_modsecurity_command_explanations",
            "common_modsecurity_advanced",
            "connector_engine_reference",
        ):
            self.assertIn(key, common)
        self.assertEqual(COMMON_BEGINNER_COMMANDS, tuple(common["common_modsecurity_beginner_commands"]))
        explanations = tuple(common["common_modsecurity_command_explanations"])
        self.assertEqual(len(COMMON_BEGINNER_COMMANDS), len(explanations))
        self.assertTrue(all(len(explanation) == 2 for explanation in explanations))
        self.assertEqual(set(SLUGS), set(common["connector_engine_reference"]))
        self.assertEqual(set(SLUGS), set(GENERATOR.HOST_SETUP))
        required_host_fields = {
            "host_simple_intro",
            "host_simple_variables",
            "host_download_steps",
            "host_build_steps",
            "host_success_check",
            "host_advanced_verification",
            "host_source_alternative",
        }
        for slug, setup in GENERATOR.HOST_SETUP.items():
            self.assertTrue(required_host_fields.issubset(setup), slug)
            self.assertLessEqual(len(setup["host_simple_variables"]), 3, slug)
        for info in GENERATOR.MANUAL_GUIDES.values():
            self.assertNotIn("host_intro", info)
            self.assertNotIn("host_commands", info)
        self.assertEqual(set(SLUGS), set(GENERATOR.ACTIVE_MANUAL_VARIABLES))
        for slug, names in GENERATOR.ACTIVE_MANUAL_VARIABLES.items():
            available = {name for name, _, _ in GENERATOR.MANUAL_GUIDES[slug]["variables"]}
            self.assertTrue(names.issubset(available), slug)

    def test_generated_files_are_complete_current_and_idempotent(self) -> None:
        rendered = GENERATOR.rendered_files()
        expected = {
            "README.md",
            "README.de.md",
            "overview.md",
            "overview.de.md",
            "libmodsecurity.md",
            "libmodsecurity.de.md",
            *{f"{slug}{suffix}.md" for slug in SLUGS for suffix in ("", ".de")},
        }
        self.assertEqual(expected, set(rendered))
        self.assertEqual(expected, {path.name for path in GUIDE_DIRECTORY.glob("*.md")})
        for name, content in rendered.items():
            self.assertEqual(content.rstrip() + "\n", (GUIDE_DIRECTORY / name).read_text(encoding="utf-8"), name)

        with tempfile.TemporaryDirectory(prefix="compiler-guides-") as temporary:
            original_output = GENERATOR.OUTPUT
            GENERATOR.OUTPUT = Path(temporary)
            try:
                GENERATOR.main()
                first = {path.name: path.read_text(encoding="utf-8") for path in GENERATOR.OUTPUT.glob("*.md")}
                GENERATOR.main()
                second = {path.name: path.read_text(encoding="utf-8") for path in GENERATOR.OUTPUT.glob("*.md")}
            finally:
                GENERATOR.OUTPUT = original_output
        self.assertEqual(first, second)

    def test_common_beginner_block_is_exact_and_bilingual(self) -> None:
        english = common_guide()
        german = common_guide(german=True)
        english_beginner = h2_section(english, "Simple official build")
        german_beginner = h2_section(german, "Einfacher offizieller Build")
        english_meanings = h2_section(english, "Meaning of the commands")
        german_meanings = h2_section(german, "Bedeutung der Befehle")
        english_blocks = shell_blocks(english_beginner)
        german_blocks = shell_blocks(german_beginner)
        self.assertEqual(1, len(english_blocks))
        self.assertEqual(1, len(german_blocks))
        self.assertEqual(list(COMMON_BEGINNER_COMMANDS), nonempty_shell_lines(english_blocks[0]))
        self.assertEqual(english_blocks, german_blocks)

        for beginner in (english_beginner, german_beginner):
            self.assertNotRegex(beginner, r"(?m)^export\b")
            self.assertNotIn("PKG_CONFIG_PATH", beginner)
            self.assertNotIn("LD_LIBRARY_PATH", beginner)
            self.assertNotIn("pkg-config", beginner)
            self.assertNotRegex(beginner, r"(?m)^ldd\b")

        for command in COMMON_BEGINNER_COMMANDS:
            self.assertIn(f"| `{command}` |", english_meanings)
            self.assertIn(f"| `{command}` |", german_meanings)
        self.assertLess(english.index("## Simple official build"), english.index("## Meaning of the commands"))
        self.assertLess(german.index("## Einfacher offizieller Build"), german.index("## Bedeutung der Befehle"))

    def test_advanced_engine_information_follows_the_simple_build(self) -> None:
        for content, beginner_heading, heading in (
            (common_guide(), "Simple official build", "Advanced and reproducible builds"),
            (common_guide(german=True), "Einfacher offizieller Build", "Fortgeschrittene und reproduzierbare Builds"),
        ):
            self.assertLess(content.index(f"## {beginner_heading}"), content.index(f"## {heading}"))
            advanced = h2_section(content, heading)
            for marker in (
                "v3.0.16",
                "MODSECURITY_COMMIT",
                "verify-tag",
                "SHA",
                "MODSECURITY_PREFIX",
                "PKG_CONFIG_PATH",
                "LD_LIBRARY_PATH",
                "make check",
                "make -j",
                "CFLAGS",
                "CXXFLAGS",
                "LDFLAGS",
                "build-provenance.txt",
            ):
                self.assertIn(marker, advanced)

    def test_connector_guides_link_the_shared_engine_and_do_not_repeat_it(self) -> None:
        for slug in SLUGS:
            english = guide(slug)
            german = guide(slug, german=True)
            self.assertIn("](libmodsecurity.md)", english, slug)
            self.assertIn("](libmodsecurity.de.md)", german, slug)
            for content in (english, german):
                connector_shell = "\n".join(shell_blocks(content))
                self.assertNotIn(COMMON_BEGINNER_COMMANDS[0], connector_shell, slug)
                self.assertNotIn("\n./build.sh\n", f"\n{connector_shell}\n", slug)
                self.assertNotIn("sudo make install", connector_shell, slug)

    def test_connector_structure_and_bilingual_technical_parity(self) -> None:
        for slug in SLUGS:
            english = guide(slug)
            german = guide(slug, german=True)
            self.assertEqual(ENGLISH_HEADINGS, headings(english), slug)
            self.assertEqual(GERMAN_HEADINGS, headings(german), slug)
            self.assertEqual(shell_blocks(english), shell_blocks(german), slug)
            self.assertEqual(variable_names(english), variable_names(german), slug)

    def test_official_upstream_sources_are_described_allowed_and_present(self) -> None:
        required_url_fragments = {
            "apache": ("httpd.apache.org/docs/2.4/install.html", "httpd.apache.org/docs/2.4/programs/apxs.html"),
            "nginx": ("nginx.org/", "github.com/owasp-modsecurity/ModSecurity-nginx"),
            "haproxy": ("github.com/haproxy/haproxy", "docs.haproxy.org"),
            "envoy": ("envoyproxy.io",),
            "traefik": ("doc.traefik.io",),
            "lighttpd": ("github.com/lighttpd", "download.lighttpd.net"),
        }
        for slug in SLUGS:
            sources = [
                source
                for source in GENERATOR.MANUAL_GUIDES[slug]["official_sources"]
                if source[1] != "https://github.com/owasp-modsecurity/ModSecurity"
            ]
            self.assertGreaterEqual(len(sources), 2, slug)
            urls = []
            for title, url, english_scope, german_scope, version_scope in sources:
                self.assertTrue(title)
                self.assertTrue(english_scope)
                self.assertTrue(german_scope)
                self.assertTrue(version_scope)
                self.assertTrue(is_allowed_official_url(url), f"{slug}: {url}")
                urls.append(url)
                for content in (guide(slug), guide(slug, german=True)):
                    self.assertIn(f"]({url})", content, f"{slug}: {url}")
            joined = "\n".join(urls)
            for fragment in required_url_fragments[slug]:
                self.assertIn(fragment, joined, slug)

    def test_section_six_is_small_host_only_setup(self) -> None:
        localized = (
            (
                False,
                "Simple path",
                "What was installed or built?",
                "Check the result",
                "Source build and integrity checks",
                "Optional: verify download and version",
            ),
            (
                True,
                "Einfacher Weg",
                "Was wurde installiert oder gebaut?",
                "Erfolg prüfen",
                "Source-Build und Integritätsprüfung",
                "Optional: Download und Version verifizieren",
            ),
        )
        for slug in SLUGS:
            for german, simple_heading, installed_heading, success_heading, source_heading, verification_heading in localized:
                section = numbered_section(guide(slug, german=german), 6)
                for heading in (simple_heading, installed_heading, success_heading, source_heading):
                    self.assertIn(f"### {heading}", section, f"{slug}: {heading}")
                simple = h3_section(section, simple_heading)
                source = h3_section(section, source_heading)
                self.assertNotRegex(simple, r"(?m)^export\b", slug)
                self.assertLessEqual(len(shell_assignments(simple)), 3, slug)
                self.assertNotIn("LD_LIBRARY_PATH", simple, slug)
                for block in shell_blocks(section):
                    self.assertLessEqual(len(nonempty_shell_lines(block)), 6, slug)
                for forbidden in (
                    "SecRule",
                    "cat >",
                    "curl -i",
                    "curl --http1.1",
                    "http://127.0.0.1",
                    "full-lifecycle",
                    "evidence-check",
                    " -k start",
                    " -s quit",
                    "\nkill ",
                ):
                    self.assertNotIn(forbidden, section, f"{slug}: {forbidden}")
                self.assertIn(f"#### {verification_heading}", source, slug)
                self.assertRegex(source.lower(), r"sha256|gpg|checksum", slug)

    def test_connector_configuration_validation_and_runtime_stay_in_sections_seven_to_ten(self) -> None:
        nginx = {number: numbered_section(guide("nginx"), number) for number in range(6, 11)}
        for token in ("./auto/configure", "make install", "nginx.conf", "curl -i"):
            self.assertNotIn(token, nginx[6])
        for token in ("./auto/configure", "--add-module", 'make -j"$JOBS"', "make install"):
            self.assertIn(token, nginx[7])
        self.assertNotIn("--add-dynamic-module", nginx[7])
        self.assertNotIn("--with-compat", nginx[7])
        self.assertIn("modsecurity-local.conf", nginx[8])
        self.assertIn("nginx.conf", nginx[8])
        self.assertIn('"$INSTALL_DIR/sbin/nginx" -V', nginx[9])
        self.assertIn("--add-module=$WORKDIR/ModSecurity-nginx", nginx[9])
        for token in ('-t -p "$INSTALL_DIR"', "curl -i http://127.0.0.1:8080/", "-s quit"):
            self.assertIn(token, nginx[10])

        apache = {number: numbered_section(guide("apache"), number) for number in range(6, 11)}
        self.assertIn("apache2-dev", apache[6])
        self.assertIn('test -x "$INSTALL_DIR/bin/apxs"', apache[6])
        self.assertIn('APXS="$HOME/.local/apache-modsecurity/bin/apxs"', apache[7])
        self.assertIn('"$APXS" -q LIBEXECDIR', apache[9])
        self.assertIn("LoadModule security3_module", apache[8])

        haproxy = {number: numbered_section(guide("haproxy"), number) for number in range(6, 11)}
        self.assertNotIn("build-overlay.sh", haproxy[6])
        self.assertIn("build-overlay.sh", haproxy[7])
        self.assertIn("modsecurity-htx", haproxy[8])
        self.assertIn("phase4-mode safe", haproxy[8])
        self.assertIn("SPOE/SPOP", haproxy[7])
        self.assertNotIn('"$HAPROXY_HTX_BIN" -c', haproxy[8])
        self.assertIn('"$HAPROXY_HTX_BIN" -c', haproxy[9])

        envoy = {number: numbered_section(guide("envoy"), number) for number in range(6, 11)}
        self.assertNotIn("build_ext_proc.sh", envoy[6])
        self.assertIn("build_ext_proc.sh", envoy[7])
        self.assertIn("ExternalProcessor", envoy[7])
        self.assertNotIn("--mode validate", envoy[8])
        self.assertIn("--mode validate", envoy[9])
        self.assertIn("--check-config", envoy[9])

        traefik = {number: numbered_section(guide("traefik"), number) for number in range(6, 11)}
        self.assertNotIn("make test-unit", h3_section(traefik[6], "Simple path"))
        self.assertNotIn("git clone", h3_section(traefik[6], "Simple path"))
        for token in ("build-native-middleware.sh", "build-engine-service.sh", "Go middleware", "engine service"):
            self.assertIn(token, traefik[7])
        for token in ("engineMode: uds", "engineSocketPath", "localPlugins"):
            self.assertIn(token, traefik[8])
        self.assertNotIn('"$TRAEFIK_BIN" check', traefik[8])
        self.assertIn('"$TRAEFIK_BIN" check', traefik[9])
        self.assertIn("--check-config", traefik[9])

        lighttpd = {number: numbered_section(guide("lighttpd"), number) for number in range(6, 11)}
        self.assertIn("patch --dry-run -p1", lighttpd[6])
        self.assertIn("patch -p1", lighttpd[6])
        self.assertNotIn("build_module.sh", lighttpd[6])
        self.assertIn("build_module.sh", lighttpd[7])
        self.assertNotIn(" -tt -f", lighttpd[8])
        self.assertIn(" -tt -f", lighttpd[9])
        self.assertIn("Entity-Body", guide("lighttpd"))

        for slug, sections in (
            ("haproxy", haproxy),
            ("envoy", envoy),
            ("traefik", traefik),
            ("lighttpd", lighttpd),
        ):
            self.assertIn('cd "$CONNECTOR_ROOT"', sections[7], slug)

        traefik_source = h3_section(traefik[6], "Source build and integrity checks")
        self.assertIn('grep -E "^go " go.mod', traefik_source)
        self.assertIn("git rev-parse HEAD", traefik_source)
        for slug in ("apache", "haproxy", "traefik", "lighttpd"):
            source = h3_section(numbered_section(guide(slug), 6), "Source build and integrity checks")
            verification = source[source.index("#### Optional: verify download and version") :]
            self.assertIn('cd "$WORKDIR"', verification, slug)

    def test_repository_test_paths_follow_manual_steps_and_targets_exist(self) -> None:
        for connector in GENERATOR.CONNECTORS:
            slug = connector["slug"]
            repository = numbered_section(guide(slug), 12)
            self.assertIn('mkdir -p "$VERIFIED_RUN_PARENT"', repository)
            self.assertIn('cd "$VERIFIED_RUN_PARENT"', repository)
            self.assertIn("automate and test the build and integration steps described above", repository)
            for target in (
                "check-framework",
                "prepare-runtime-components",
                connector["build"],
                connector["config"],
                connector["start"],
                connector["runtime"],
                connector["full"],
                f"evidence-check-{slug}",
            ):
                self.assertIn(f"make {target}", repository, f"{slug}: {target}")
                self.assertTrue(target_exists(target), f"missing Make target: {target}")

    def test_manual_shell_placeholders_are_documented(self) -> None:
        ignored = {"HOME", "PWD"}
        for slug in SLUGS:
            manual = "".join(numbered_section(guide(slug), number) for number in range(6, 11))
            unexplained = shell_variables(manual) - variable_names(guide(slug)) - ignored
            self.assertEqual(set(), unexplained, slug)

    def test_guides_use_safe_defaults_and_state_required_boundaries(self) -> None:
        forbidden_claims = (
            "production-ready",
            "production hardened",
            "security verified",
            "crs verified",
            "full matrix verified",
        )
        prohibited_absolute_source = re.compile(r"(?:^|[=:\"'\s])/src(?:/|[\"'\s])")
        broad_library_copy = re.compile(r"\b(?:cp|install)\b[^\n]*?/usr/lib(?:/|\b)")
        german_boundary = "Diese Anleitung beschreibt einen nachvollziehbaren Entwicklungs- und Integrationsbuild. Sie ist keine Produktionsfreigabe."
        for content in (
            common_guide(),
            common_guide(german=True),
            *[guide(slug) for slug in SLUGS],
            *[guide(slug, german=True) for slug in SLUGS],
        ):
            self.assertIn(GENERATOR.MARKER, content)
            self.assertNotIn("/root", content)
            self.assertNotIn("/var/tmp", content)
            for block in shell_blocks(content):
                self.assertNotRegex(block, prohibited_absolute_source)
                self.assertNotRegex(block, broad_library_copy)
            for claim in forbidden_claims:
                self.assertNotIn(claim, content.lower())
        for slug in SLUGS:
            self.assertIn(german_boundary, guide(slug, german=True), slug)


if __name__ == "__main__":
    unittest.main()
