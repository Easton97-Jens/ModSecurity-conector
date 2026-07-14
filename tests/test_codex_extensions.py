from __future__ import annotations

from pathlib import Path
import re
import unittest

import yaml


ROOT = Path(__file__).resolve().parents[1]
SKILLS_ROOT = ROOT / ".agents" / "skills"
LOCK_PATH = ROOT / "ci" / "tooling" / "codex-extensions.lock.yml"
DEVELOPMENT_DOCS = (
    ROOT / "docs" / "development" / "codex-extensions.md",
    ROOT / "docs" / "development" / "codex-extensions.de.md",
)
SECURITY_DOCS = (
    ROOT / "docs" / "security" / "external-agent-services.md",
    ROOT / "docs" / "security" / "external-agent-services.de.md",
)
CHANGE_RECORD_DOCS = (
    ROOT
    / "reports"
    / "audits"
    / "change-records"
    / "CR-20260714-codex-extension-profile.md",
    ROOT
    / "reports"
    / "audits"
    / "change-records"
    / "CR-20260714-codex-extension-profile.de.md",
)

EXPECTED_LOCAL_SKILLS = {
    "create-plan",
    "gh-fix-ci",
    "gh-address-comments",
    "stop-slop",
    "valyu-research",
    "modsecurity-codebase-migrate",
    "bilingual-changelog-generator",
    "third-party-skill-audit",
}
VENDORED_SKILLS = {
    "create-plan",
    "gh-fix-ci",
    "gh-address-comments",
    "stop-slop",
}
EXPECTED_LOCK_ENTRIES = EXPECTED_LOCAL_SKILLS | {
    "superpowers",
    "codex-security",
    "warpgrep-morphmcp",
    "valyu-hosted-mcp",
    "valyu-local-mcp",
    "composio-pr-review-ci-fix",
    "composio-connect-apps",
    "composio-skill-share",
    "composio-mcp-builder",
    "composio-frontend-webapp",
}
REQUIRED_LOCK_FIELDS = {
    "name",
    "type",
    "source_owner",
    "source_repository",
    "source_url",
    "source_path",
    "source_commit",
    "upstream_version",
    "license",
    "integration_mode",
    "local_name",
    "requires_network",
    "requires_secret",
    "external_data_processing",
    "write_capabilities",
    "approved_tools",
    "disabled_tools",
    "update_policy",
    "status",
    "reviewed_at",
}
ALLOWED_STATUSES = {
    "enabled",
    "configured_pending_secret",
    "installed_pending_reload",
    "adapted_and_vendored",
    "documented_only",
    "rejected_due_to_overlap",
    "rejected_due_to_permissions",
    "blocked_license_unknown",
    "blocked_source_unverified",
    "not_applicable",
}
ROUTING_EXPECTATIONS = {
    "create-plan": ("needs a plan", "one-step factual answer"),
    "gh-fix-ci": ("github actions", "no check failure"),
    "gh-address-comments": ("review feedback", "no identified pull request"),
    "stop-slop": ("quality, clarity", "security audit"),
    "valyu-research": ("external research", "sensitive code"),
    "modsecurity-codebase-migrate": ("migrate a connector", "framework without"),
    "bilingual-changelog-generator": (
        "bilingual changelog",
        "local codex/rtk configuration",
    ),
    "third-party-skill-audit": (
        "add, update, enable",
        "source cannot be resolved",
    ),
}
REQUIRED_SKILL_CONTRACTS = {
    "create-plan": (
        "required plan format",
        "goal",
        "scope",
        "non-goals",
        "acceptance criteria",
        "files/components",
        "security impact",
        "test plan",
        "en/de impact",
        "parent/framework boundary",
        "risks",
        "open decisions",
        "blocked_waiting_for_clarification",
        "must not perform a code change",
    ),
    "gh-fix-ci": (
        "rtk gh auth status",
        "push and pull-request checks",
        "machine-readable",
        "sonarcloud, codeql",
        "compare with `master`",
        "ordinary follow-up commit",
        "verify the remote sha",
        "restart complete check and feedback monitoring",
    ),
    "gh-address-comments": (
        "open review threads",
        "general pr comments",
        "inline comments",
        "bot findings",
        "requested changes",
        "stale/outdated disposition",
        "local verification",
        "update the change record",
        "fresh complete check and feedback cycle",
    ),
    "stop-slop": (
        "c/c++ code",
        "shell script",
        "json",
        "verbatim quotation",
        "normative status value",
        "normative terms",
        "security severity",
        "english and german separately",
        "semantic-diff review",
        "do not alter a commit message",
    ),
    "valyu-research": (
        "already-available official source",
        "explicit maximum cost",
        "cite every external assertion",
        "internal source, logs, private reviews, credentials",
        "locally validate every result",
        "official openai sources",
    ),
    "modsecurity-codebase-migrate": (
        "exact transformation and blast radius",
        "disjoint file scope",
        "codemod before manual",
        "synthetic negative tests",
        "independently revertible",
        "do not use automatic merge",
    ),
    "bilingual-changelog-generator": (
        "explicit commit/tag range",
        "change records in that range as the primary evidence",
        "feature, fix, security change, breaking change, or internal change",
        "trace every entry",
        "internal refactor as a user feature",
        "do not automatically create a tag, release, or publication",
        "release readiness",
    ),
    "third-party-skill-audit": (
        "trigger and negative-trigger overlap",
        "deinstallation or recovery path",
    ),
}
UNSAFE_AUTOMATION = {
    "implicit staging": re.compile(r"\bgit\s+add\s+(?:\.|-A)\b", re.IGNORECASE),
    "history rewrite": re.compile(r"\b--force(?:-with-lease)?\b", re.IGNORECASE),
    "destructive reset": re.compile(r"\bgit\s+reset\s+--hard\b", re.IGNORECASE),
    "discarding checkout": re.compile(r"\bgit\s+checkout\s+--(?:\s|$)", re.IGNORECASE),
    "discarding restore": re.compile(r"\bgit\s+restore\b", re.IGNORECASE),
    "automatic merge": re.compile(r"\bauto[- ]merge\b", re.IGNORECASE),
    "workflow error suppression": re.compile(r"\bcontinue-on-error\b", re.IGNORECASE),
    "shell error suppression": re.compile(r"\|\|\s*true\b", re.IGNORECASE),
    "scanner suppression": re.compile(r"\b(?:NOSONAR|noqa)\b", re.IGNORECASE),
}
GIT_CLEAN_COMMAND = re.compile(r"\bgit\s+clean\b", re.IGNORECASE)
SAFETY_NEGATIONS = ("do not", "never", "forbid", "prohibit", "not allowed")
ABSOLUTE_USER_PATH_PATTERNS = {
    "Unix root path": re.compile(r"(?<![A-Za-z0-9])/(?:root|home|Users)/"),
    "file URL": re.compile(r"\bfile:///", re.IGNORECASE),
    "Windows user path": re.compile(r"\b[a-z]:\\Users\\", re.IGNORECASE),
}
GH_GUARDRAILS = {
    "gh-fix-ci": (
        "do not use `git add -a`",
        "do not amend a published commit",
        "do not force-push",
        "do not add `continue-on-error`",
        "do not use `|| true`",
        "do not weaken, skip, or suppress a quality gate",
    ),
    "gh-address-comments": (
        "do not automatically resolve a human review thread",
        "do not delete or hide another person's comment",
    ),
}
SECRET_PATTERNS = {
    "GitHub personal token": re.compile(r"\b(?:ghp|github_pat)_[A-Za-z0-9_-]{20,}\b"),
    "OpenAI-style key": re.compile(r"\bsk-[A-Za-z0-9_-]{20,}\b"),
    "Slack token": re.compile(r"\bxox[baprs]-[A-Za-z0-9-]{20,}\b"),
    "Morph key assignment": re.compile(
        r"\bMORPH_API_KEY\s*=\s*(?!\$\{|<|environment\b)[^\s]+"
    ),
    "Valyu key assignment": re.compile(
        r"\bVALYU_API_KEY\s*=\s*(?!\$\{|<|environment\b)[^\s]+"
    ),
}


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def normalize_whitespace(text: str) -> str:
    return " ".join(text.lower().split())


def extension_material_paths() -> list[Path]:
    return (
        [LOCK_PATH]
        + list(SKILLS_ROOT.rglob("*"))
        + list(DEVELOPMENT_DOCS)
        + list(SECURITY_DOCS)
        + list(CHANGE_RECORD_DOCS)
    )


def has_destructive_git_clean(line: str) -> bool:
    command = GIT_CLEAN_COMMAND.search(line)
    if command is None:
        return False
    for argument in line[command.end() :].split():
        option = argument.strip("\x60.,;:()[]{}")
        if option == "--force":
            return True
        if option.startswith("-") and not option.startswith("--") and "f" in option.lower():
            return True
    return False


def is_unprotected_unsafe_instruction(line: str) -> bool:
    normalized = line.lower()
    has_unsafe_construct = has_destructive_git_clean(line) or any(
        pattern.search(line) for pattern in UNSAFE_AUTOMATION.values()
    )
    has_safety_negation = any(negation in normalized for negation in SAFETY_NEGATIONS)
    return has_unsafe_construct and not has_safety_negation


class CodexExtensionContractTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.lock = yaml.safe_load(read_text(LOCK_PATH))
        cls.entries = cls.lock["extensions"]
        cls.by_name = {entry["name"]: entry for entry in cls.entries}

    def test_local_skill_directories_and_frontmatter(self) -> None:
        self.assertEqual(
            EXPECTED_LOCAL_SKILLS,
            {path.name for path in SKILLS_ROOT.iterdir() if path.is_dir()},
        )
        for name in EXPECTED_LOCAL_SKILLS:
            with self.subTest(skill=name):
                skill_path = SKILLS_ROOT / name / "SKILL.md"
                upstream_path = SKILLS_ROOT / name / "UPSTREAM.md"
                self.assertTrue(skill_path.is_file())
                self.assertTrue(upstream_path.is_file())
                text = read_text(skill_path)
                self.assertTrue(text.startswith("---\n"))
                closing_delimiter = text.find("\n---", 4)
                self.assertGreater(closing_delimiter, 4)
                frontmatter = text[4:closing_delimiter]
                self.assertRegex(frontmatter, rf"(?m)^name: {re.escape(name)}$")
                self.assertRegex(frontmatter, r"(?m)^description: .+")
                self.assertIn("## Trigger conditions", text)
                self.assertIn("## Do not use when", text)

    def test_vendored_licenses_and_provenance(self) -> None:
        for name in VENDORED_SKILLS:
            with self.subTest(skill=name):
                skill_directory = SKILLS_ROOT / name
                self.assertTrue((skill_directory / "LICENSE.txt").is_file())
                upstream = read_text(skill_directory / "UPSTREAM.md")
                self.assertIn("Immutable source commit:", upstream)
                self.assertRegex(upstream, r"\b[0-9a-f]{40}\b")
                self.assertIn("Update procedure", upstream)

    def test_relative_markdown_links_resolve(self) -> None:
        markdown_files = (
            list(SKILLS_ROOT.rglob("*.md"))
            + list(DEVELOPMENT_DOCS)
            + list(SECURITY_DOCS)
            + list(CHANGE_RECORD_DOCS)
        )
        link_pattern = re.compile(r"(?<!!)\[[^\]]+\]\(([^)]+)\)")
        for markdown_file in markdown_files:
            for raw_target in link_pattern.findall(read_text(markdown_file)):
                target = raw_target.split("#", 1)[0].strip("<>")
                if not target or "://" in target or target.startswith("mailto:"):
                    continue
                with self.subTest(file=markdown_file, target=target):
                    self.assertTrue((markdown_file.parent / target).exists())

    def test_lock_schema_is_complete_and_pinned_when_required(self) -> None:
        self.assertEqual(1, self.lock["schema_version"])
        self.assertEqual(EXPECTED_LOCK_ENTRIES, set(self.by_name))
        self.assertEqual(len(self.entries), len(self.by_name))
        for entry in self.entries:
            with self.subTest(extension=entry["name"]):
                self.assertTrue(REQUIRED_LOCK_FIELDS.issubset(entry))
                self.assertIn(entry["type"], {"skill", "plugin", "mcp"})
                self.assertIn(entry["status"], ALLOWED_STATUSES)
                self.assertTrue(entry["source_url"].startswith("https://"))
                self.assertIsInstance(entry["approved_tools"], list)
                self.assertIsInstance(entry["disabled_tools"], list)
                source_commit = entry["source_commit"]
                if source_commit is not None:
                    self.assertRegex(str(source_commit), r"^[0-9a-f]{40}$")
                elif entry["source_owner"] != "repository":
                    self.assertIn(
                        entry["status"],
                        {"blocked_source_unverified", "blocked_license_unknown"},
                    )
        for name in VENDORED_SKILLS:
            self.assertEqual("adapted_and_vendored", self.by_name[name]["status"])
        self.assertEqual(
            "bd2122cb92f2ade874d8c2b1d00383976ab9415b",
            self.by_name["superpowers"]["source_commit"],
        )
        self.assertEqual("installed_pending_reload", self.by_name["superpowers"]["status"])
        self.assertEqual(
            "bd2122cb92f2ade874d8c2b1d00383976ab9415b",
            self.by_name["codex-security"]["source_commit"],
        )
        self.assertEqual("enabled", self.by_name["codex-security"]["status"])

    def test_declared_routing_contract_has_positive_and_negative_boundaries(self) -> None:
        for name, (positive, negative) in ROUTING_EXPECTATIONS.items():
            text = read_text(SKILLS_ROOT / name / "SKILL.md").lower()
            with self.subTest(skill=name, boundary="positive"):
                self.assertIn(positive, text)
            with self.subTest(skill=name, boundary="negative"):
                self.assertIn(negative, text)

    def test_local_skill_contracts_include_required_repository_boundaries(self) -> None:
        for name, requirements in REQUIRED_SKILL_CONTRACTS.items():
            text = normalize_whitespace(read_text(SKILLS_ROOT / name / "SKILL.md"))
            for requirement in requirements:
                with self.subTest(skill=name, requirement=requirement):
                    self.assertIn(requirement, text)

    def test_blocked_mcp_contract_does_not_claim_unverified_tool_mapping(self) -> None:
        morph = self.by_name["warpgrep-morphmcp"]
        valyu = self.by_name["valyu-hosted-mcp"]
        self.assertEqual("blocked_source_unverified", morph["status"])
        self.assertEqual(
            ["codebase_search", "github_codebase_search"], morph["approved_tools"]
        )
        self.assertEqual("blocked_source_unverified", valyu["status"])
        self.assertIn("knowledge", valyu["disabled_tools"])
        self.assertIn("feedback", valyu["disabled_tools"])
        for document in DEVELOPMENT_DOCS + SECURITY_DOCS:
            text = read_text(document)
            with self.subTest(document=document):
                self.assertIn("codebase_search", text)
                self.assertIn("github_codebase_search", text)
                self.assertIn("knowledge", text)
                self.assertIn("feedback", text)
        english_routing = read_text(DEVELOPMENT_DOCS[0])
        german_routing = read_text(DEVELOPMENT_DOCS[1])
        self.assertIn("semantic exploration", english_routing)
        self.assertIn("exact symbol", english_routing)
        self.assertIn("semantische Exploration", german_routing)
        self.assertIn("exakten Symbolnamen", german_routing)
        self.assertIn("`rg`", english_routing)
        self.assertIn("`rg`", german_routing)

    def test_versioned_extension_material_has_no_literal_secret(self) -> None:
        for path in extension_material_paths():
            if not path.is_file():
                continue
            text = read_text(path)
            for pattern_name, pattern in SECRET_PATTERNS.items():
                with self.subTest(file=path, pattern=pattern_name):
                    self.assertIsNone(pattern.search(text))

    def test_versioned_extension_material_has_no_absolute_user_path(self) -> None:
        for path in extension_material_paths():
            if not path.is_file():
                continue
            text = read_text(path)
            for pattern_name, pattern in ABSOLUTE_USER_PATH_PATTERNS.items():
                with self.subTest(file=path, pattern=pattern_name):
                    self.assertIsNone(pattern.search(text))

    def test_local_guidance_rejects_unsafe_automation(self) -> None:
        paths = [LOCK_PATH] + list(SKILLS_ROOT.rglob("SKILL.md")) + list(
            SKILLS_ROOT.rglob("UPSTREAM.md")
        )
        for path in paths:
            for line_number, line in enumerate(read_text(path).splitlines(), start=1):
                with self.subTest(file=path, line=line_number):
                    self.assertFalse(is_unprotected_unsafe_instruction(line))

    def test_unsafe_automation_classifier_has_positive_and_negative_cases(self) -> None:
        for instruction in (
            "git reset --hard",
            "git checkout -- tracked-file",
            "git restore src/example.c",
            "git clean -fdx",
            "git clean -xdf",
        ):
            with self.subTest(instruction=instruction):
                self.assertTrue(is_unprotected_unsafe_instruction(instruction))
        for instruction in (
            "Do not run `git reset --hard`.",
            "Never use `git checkout -- tracked-file`.",
            "Do not use `git restore src/example.c` to discard work.",
            "Never run `git clean -fdx`.",
            "git status --short",
        ):
            with self.subTest(instruction=instruction):
                self.assertFalse(is_unprotected_unsafe_instruction(instruction))

    def test_github_workflows_explicitly_prohibit_unsafe_automation(self) -> None:
        for name, requirements in GH_GUARDRAILS.items():
            text = normalize_whitespace(read_text(SKILLS_ROOT / name / "SKILL.md"))
            for requirement in requirements:
                with self.subTest(skill=name, requirement=requirement):
                    self.assertIn(requirement, text)


if __name__ == "__main__":
    unittest.main()
