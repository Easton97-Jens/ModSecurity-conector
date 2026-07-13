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


def load_generator() -> object:
    spec = importlib.util.spec_from_file_location("compiler_guides_generator", GENERATOR_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load generator: {GENERATOR_PATH}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


GENERATOR = load_generator()


ENGLISH_HEADINGS = [
    "1. Purpose and selected integration path",
    "2. Build components",
    "3. Official upstream documentation",
    "4. Prerequisites",
    "5. Build libmodsecurity v3 from source",
    "6. Prepare or build the host or proxy",
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
    "5. libmodsecurity v3 aus Source bauen",
    "6. Host oder Proxy vorbereiten beziehungsweise bauen",
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


def guide(slug: str, german: bool = False) -> str:
    suffix = ".de" if german else ""
    return (GUIDE_DIRECTORY / f"{slug}{suffix}.md").read_text(encoding="utf-8")


def headings(content: str) -> list[str]:
    return re.findall(r"^## (.+)$", content, flags=re.MULTILINE)


def section(content: str, number: int) -> str:
    start = re.search(rf"^## {number}\. .+$", content, flags=re.MULTILINE)
    if start is None:
        raise AssertionError(f"missing section {number}")
    end = re.search(rf"^## {number + 1}\. .+$", content[start.end() :], flags=re.MULTILINE)
    return content[start.start() : start.end() + (end.start() if end else len(content))]


def shell_blocks(content: str) -> list[str]:
    return re.findall(r"```sh\n(.*?)\n```", content, flags=re.DOTALL)


def variable_names(content: str) -> set[str]:
    variables = section(content, 16)
    return set(re.findall(r"^\| ([A-Za-z_][A-Za-z0-9_]*) \|", variables, flags=re.MULTILINE))


def shell_variables(content: str) -> set[str]:
    return set(
        re.findall(
            r"\$\{?([A-Za-z_][A-Za-z0-9_]*)",
            "\n".join(shell_blocks(content)),
        )
    )


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

    def test_generated_files_are_complete_current_and_idempotent(self) -> None:
        rendered = GENERATOR.rendered_files()
        expected = {
            "README.md",
            "README.de.md",
            "overview.md",
            "overview.de.md",
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

    def test_source_first_structure_and_bilingual_technical_parity(self) -> None:
        for slug in SLUGS:
            english = guide(slug)
            german = guide(slug, german=True)
            self.assertEqual(ENGLISH_HEADINGS, headings(english), slug)
            self.assertEqual(GERMAN_HEADINGS, headings(german), slug)
            self.assertEqual(shell_blocks(english), shell_blocks(german), slug)
            self.assertEqual(variable_names(english), variable_names(german), slug)

            manual = "".join(section(english, number) for number in range(5, 11))
            package = section(english, 11)
            repository = section(english, 12)
            self.assertGreaterEqual(len(manual), 3 * len(package), slug)
            self.assertGreaterEqual(len(manual), 3 * len(repository), slug)
            self.assertLess(english.index("## 10."), english.index("## 12."), slug)

    def test_every_guide_has_the_shared_fixed_libmodsecurity_source_contract(self) -> None:
        required = (
            'export BUILD_BASE="$HOME/src/modsecurity-build"',
            'git clone --recurse-submodules https://github.com/owasp-modsecurity/ModSecurity.git "$MODSECURITY_SRC"',
            'export MODSECURITY_REF="v3.0.16"',
            'export MODSECURITY_COMMIT="7ea9fefbe0ba409d8733b4d682c8c4c059cd028d"',
            'git -C "$MODSECURITY_SRC" submodule update --init --recursive',
            "./build.sh",
            "./configure --help",
            './configure --prefix="$MODSECURITY_PREFIX"',
            'make -j"$jobs"',
            "make check",
            "make install",
            'test -d "$MODSECURITY_PREFIX/include"',
            'test -d "$MODSECURITY_PREFIX/lib"',
            "pkg-config --modversion libmodsecurity",
            "LD_LIBRARY_PATH",
        )
        for slug in SLUGS:
            content = guide(slug)
            for token in required:
                self.assertIn(token, content, f"{slug}: {token}")

    def test_official_upstream_sources_are_described_allowed_and_present(self) -> None:
        required_url_fragments = {
            "apache": ("httpd.apache.org/docs/2.4/install.html", "httpd.apache.org/docs/2.4/programs/apxs.html"),
            "nginx": ("nginx.org/", "github.com/owasp-modsecurity/ModSecurity", "github.com/owasp-modsecurity/ModSecurity-nginx"),
            "haproxy": ("github.com/haproxy/haproxy", "docs.haproxy.org"),
            "envoy": ("envoyproxy.io",),
            "traefik": ("doc.traefik.io",),
            "lighttpd": ("github.com/lighttpd", "download.lighttpd.net"),
        }
        for slug in SLUGS:
            sources = GENERATOR.MANUAL_GUIDES[slug]["official_sources"]
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

    def test_connector_specific_source_and_integration_steps_are_documented(self) -> None:
        nginx = guide("nginx").lower()
        for token in (
            "nginx.org/download",
            "modsecurity-nginx",
            "./auto/configure",
            "--add-dynamic-module",
            "make -j\"$jobs\" v=1",
            "make install",
            "load_module modules/ngx_http_modsecurity_module.so",
            "-t -p \"$nginx_prefix\"",
            "curl -i http://127.0.0.1:8080/",
            "build-provenance.txt",
        ):
            self.assertIn(token, nginx)
        for forbidden in (
            "rustup",
            "luajit",
            "openresty",
            "openappsec",
            "brotli",
            "njs",
            "rtmp",
            "geoip2",
            "headers-more",
            "zstd",
            "nginx-auth-ldap",
        ):
            self.assertNotIn(forbidden, nginx)

        apache = guide("apache")
        self.assertIn('"$APXS" -q LIBEXECDIR', apache)
        self.assertIn("LoadModule security3_module", apache)
        self.assertIn("APXS", apache)

        haproxy = guide("haproxy")
        self.assertIn("modsecurity-htx", haproxy)
        self.assertIn("phase4-mode safe", haproxy)
        self.assertIn("SPOE/SPOP", haproxy)

        envoy = guide("envoy")
        self.assertIn("ext_proc", envoy)
        self.assertIn("ExternalProcessor", envoy)
        self.assertIn("--mode validate", envoy)

        traefik = guide("traefik")
        for token in ("native Go middleware", "engine service", "engineMode: uds", "engineSocketPath", "localPlugins"):
            self.assertIn(token, traefik)

        lighttpd = guide("lighttpd")
        self.assertIn('patch --dry-run -p1 < "$LIGHTTPD_PATCH_FILE"', lighttpd)
        self.assertIn("Entity-Body", lighttpd)

    def test_repository_test_paths_follow_the_manual_build_and_targets_exist(self) -> None:
        for connector in GENERATOR.CONNECTORS:
            slug = connector["slug"]
            content = guide(slug)
            repository = section(content, 12)
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

    def test_all_shell_placeholders_have_a_variable_table_entry(self) -> None:
        ignored = {"HOME", "PWD"}
        for slug in SLUGS:
            content = guide(slug)
            unexplained = shell_variables(content) - variable_names(content) - ignored
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
        german_boundary = (
            "Diese Anleitung beschreibt einen nachvollziehbaren Entwicklungs- und "
            "Integrationsbuild. Sie ist keine Produktionsfreigabe."
        )
        for slug in SLUGS:
            for content in (guide(slug), guide(slug, german=True)):
                self.assertIn(GENERATOR.MARKER, content)
                self.assertNotIn("/root", content)
                self.assertNotIn("/var/tmp", content)
                for block in shell_blocks(content):
                    self.assertNotRegex(block, prohibited_absolute_source)
                    self.assertNotRegex(block, broad_library_copy)
                for claim in forbidden_claims:
                    self.assertNotIn(claim, content.lower(), f"{slug}: {claim}")
            self.assertIn(german_boundary, guide(slug, german=True), slug)


if __name__ == "__main__":
    unittest.main()
