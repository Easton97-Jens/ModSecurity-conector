#!/usr/bin/env python3
"""Source-backed configuration inventory and Markdown renderer.

This module is deliberately shared by the generator and the checker.  It does
not use an aspirational option list: every connector-specific entry starts with
one of the parser/registration surfaces below.  Example-only host fields are
kept separate and carry their checked-in example as the source anchor.
"""

from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path
import json
import re
from typing import Any, Iterable


ROOT = next(parent for parent in Path(__file__).resolve().parents if (parent / "Makefile").is_file())
CONNECTORS = ("apache", "nginx", "haproxy", "envoy", "traefik", "lighttpd")


@dataclass(frozen=True)
class StackEntry:
    indent: int
    path: str
    kind: str


def _read(root: Path, relative: str) -> str:
    return (root / relative).read_text(encoding="utf-8")


def _line_of(root: Path, relative: str, needle: str) -> int:
    for number, line in enumerate(_read(root, relative).splitlines(), 1):
        if needle in line:
            return number
    return 1


def _source(relative: str, symbol: str) -> str:
    return f"{relative}:{symbol}"


def _slug(value: str) -> str:
    value = value.lower().replace("@", "").replace("_", "-")
    value = re.sub(r"[^a-z0-9]+", "-", value).strip("-")
    return value or "configuration"


def _language_switch(name: str, german: bool) -> str:
    if german:
        return f"**Sprache:** [English]({name}.md) | Deutsch"
    return f"**Language:** English | [Deutsch]({name}.de.md)"


def _option(
    connector: str,
    name: str,
    layer: str,
    source_file: str,
    source_symbol: str,
    *,
    syntax: str,
    value_type: str,
    allowed_values: str,
    default: str,
    default_source: str,
    required: bool,
    contexts: str,
    inheritance: str,
    merge_behavior: str,
    validation: str,
    phase_relevance: str,
    security_relevance: str,
    runtime_effect: str,
    example_file: str,
    description: str,
    example_value: str = "",
    implemented: bool = True,
    compatibility_only: bool = False,
    deprecated: bool = False,
) -> dict[str, Any]:
    """Create the stable JSON schema consumed by the documentation checker."""
    return {
        "connector": connector,
        "name": name,
        "configuration_layer": layer,
        "source_file": source_file,
        "source_symbol": source_symbol,
        "implemented": implemented,
        "selected_integration_mode": integration_mode(connector),
        "documented_in": documented_path(connector, False),
        "german_documented_in": documented_path(connector, True),
        "syntax": syntax,
        "value_type": value_type,
        "allowed_values": allowed_values,
        "default": default,
        "default_source": default_source,
        "required": required,
        "contexts": contexts,
        "inheritance": inheritance,
        "merge_behavior": merge_behavior,
        "validation": validation,
        "phase_relevance": phase_relevance,
        "security_relevance": security_relevance,
        "runtime_effect": runtime_effect,
        "example_file": example_file,
        "example_value": example_value,
        "compatibility_only": compatibility_only,
        "deprecated": deprecated,
        "description": description,
    }


def integration_mode(connector: str) -> str:
    return {
        "apache": "native-httpd-module",
        "nginx": "native-nginx-http-module",
        "haproxy": "native-htx-filter",
        "envoy": "ext-proc",
        "traefik": "native-middleware-uds-engine",
        "lighttpd": "patched-native-lighttpd",
        "common": "connector-neutral-common-runtime",
        "engine": "libmodsecurity-engine",
    }[connector]


def documented_path(connector: str, german: bool) -> str:
    suffix = ".de.md" if german else ".md"
    if connector == "common":
        return f"examples/common/common-connector-configuration{suffix}"
    if connector == "engine":
        return f"examples/common/modsecurity-directives{suffix}"
    return f"examples/{connector}/configuration-reference{suffix}"


def directive_macros(root: Path) -> dict[str, str]:
    text = _read(root, "common/include/msconnector/directives.h")
    return dict(re.findall(r"#define\s+(MSCONNECTOR_DIRECTIVE_[A-Z0-9_]+)\s+\"([^\"]+)\"", text))


DIRECTIVE_DETAILS: dict[str, dict[str, str]] = {
    "modsecurity": {
        "type": "boolean",
        "values": "on | off (the shared parser additionally accepts true/false/1/0/yes/no where the host passes it through)",
        "default": "off",
        "default_source": "common/include/msconnector/options.h:MSCONNECTOR_DEFAULT_ENABLE",
        "effect": "Gates connector transaction creation; it is not SecRuleEngine.",
        "security": "off bypasses connector P1–P4 processing even if a rule file is configured.",
    },
    "modsecurity_rules": {
        "type": "string",
        "values": "one inline ModSecurity rule/configuration string",
        "default": "none; optional",
        "default_source": "parser registration has no default",
        "effect": "Loads inline content through libmodsecurity during configuration loading.",
        "security": "Inline rules are executable policy; restrict who may alter host configuration.",
    },
    "modsecurity_rules_file": {
        "type": "path",
        "values": "readable ModSecurity configuration/rules file path",
        "default": "none; optional",
        "default_source": "parser registration has no default",
        "effect": "Loads a local rule file through libmodsecurity during configuration loading.",
        "security": "Keep the file and parent directories non-writable by untrusted identities.",
    },
    "modsecurity_rules_remote": {
        "type": "two strings",
        "values": "key and URL",
        "default": "none; optional",
        "default_source": "parser registration has no default",
        "effect": "Passes the key/URL pair to libmodsecurity's remote-rule loader.",
        "security": "Remote policy is not exercised by the selected no-CRS examples; do not treat it as a local-file substitute.",
    },
    "modsecurity_transaction_id": {
        "type": "string/expression",
        "values": "non-empty host-specific transaction identifier",
        "default": "none; connector creates a fallback identifier",
        "default_source": "connector transaction creation path",
        "effect": "Supplies the engine and event correlation identifier for a transaction.",
        "security": "Do not put credentials or sensitive request data in a correlation identifier.",
    },
    "modsecurity_transaction_id_expr": {
        "type": "Apache string expression",
        "values": "one non-empty Apache expression",
        "default": "none",
        "default_source": "Apache parser registration has no default",
        "effect": "Evaluates an Apache expression per request for the transaction identifier.",
        "security": "Treat expression inputs as metadata; avoid exposing secrets in logs.",
    },
    "modsecurity_use_error_log": {
        "type": "boolean",
        "values": "on | off",
        "default": "on",
        "default_source": "common/include/msconnector/options.h:MSCONNECTOR_DEFAULT_USE_ERROR_LOG",
        "effect": "Controls forwarding of libmodsecurity messages to the host error log; it does not switch rule evaluation.",
        "security": "Error logs can contain security metadata; protect and rotate them.",
    },
    "modsecurity_phase4_mode": {
        "type": "enum",
        "values": "minimal | safe | strict",
        "default": "safe",
        "default_source": "common/include/msconnector/options.h:MSCONNECTOR_DEFAULT_PHASE4_MODE",
        "effect": "Selects the requested late P4 policy. Before response commit a deny can be applied; after commit the current Apache/NGINX/HTX paths distinguish strict from non-strict only. Minimal and safe therefore share the current non-strict log-only path.",
        "security": "strict must not be described as a guaranteed later 403; host-specific abort evidence is required.",
    },
    "modsecurity_phase4_content_types_file": {
        "type": "path",
        "values": "one readable file with MIME tokens",
        "default": "host defaults when omitted",
        "default_source": "connector-specific default content-type loader",
        "effect": "Scopes P4 response-body inspection to configured MIME types.",
        "security": "Keep the scope narrow and validate that the host exposes the intended representation of response bytes.",
    },
    "modsecurity_phase4_log": {
        "type": "path",
        "values": "one connector JSONL event/intervention-log path",
        "default": "none",
        "default_source": "parser registration has no default",
        "effect": "Sets a connector event path; current Apache and NGINX paths also use it for earlier rule/intervention metadata, not only P4.",
        "security": "Treat JSONL metadata as sensitive operational data and set safe ownership/rotation.",
    },
    "modsecurity_phase4_body_limit": {
        "type": "positive decimal byte count",
        "values": "positive integer",
        "default": "1048576",
        "default_source": "common/include/msconnector/options.h:MSCONNECTOR_DEFAULT_PHASE4_BODY_LIMIT",
        "effect": "Bounds response bytes offered to P4 processing by the native connector.",
        "security": "A larger limit raises memory/CPU exposure; zero is invalid in the native setters.",
    },
}


# Apache's Phase-4 all-response gate intentionally differs from the shared
# late-intervention descriptions used by other native hosts. Keep the override
# local so a connector-specific security invariant cannot silently rewrite the
# NGINX/HTX documentation contract.
APACHE_DIRECTIVE_DETAILS: dict[str, dict[str, str]] = {
    "modsecurity_phase4_mode": {
        "effect": (
            "Apache retains every normalized response brigade through first EOS and resolves "
            "the normal P4 decision before original output release. This mode selects only the "
            "defensive fallback for independently proven already-committed output: minimal/safe "
            "record log_only and strict requests abort_connection."
        ),
        "security": (
            "A normal Phase-4 deny must not be reinterpreted as log_only: Apache discards the "
            "saved original brigade and emits one terminal error before release. strict is not a "
            "guaranteed later 403; host-specific abort evidence is still required."
        ),
        "phase_relevance": (
            "P4 only. Apache's EOS-only all-response gate resolves intervention before original "
            "output release; this setting applies only if independent commit proof already exists."
        ),
    },
    "modsecurity_phase4_content_types_file": {
        "type": "deprecated path",
        "values": "one readable legacy file with MIME tokens",
        "default": "none; deprecated Apache compatibility input",
        "default_source": "Apache compatibility parser; deprecated",
        "effect": (
            "Deprecated Apache compatibility parser for a legacy MIME list. It does not narrow "
            "the all-response Phase-4 gate; use SecResponseBodyMimeType to select libModSecurity "
            "inspection."
        ),
        "security": (
            "Do not use this legacy list to permit a pass-through route. The connector cannot safely "
            "query libModSecurity's effective MIME selection, so every response remains gated through EOS."
        ),
        "phase_relevance": (
            "P4 only. The parser is retained for compatibility but cannot select which Apache "
            "responses bypass the EOS-only enforcement gate."
        ),
    },
    "modsecurity_phase4_body_limit": {
        "effect": (
            "Bounds Apache's saved all-response brigade before Phase-4 completion. The configurable "
            "default is 1048576 bytes; independently, a fixed non-configurable 4096-normalized-bucket "
            "ceiling applies across filter calls. An over-byte-limit or over-bucket-limit response fails "
            "closed before any original response byte is released."
        ),
        "security": (
            "The byte and fixed bucket ceilings bound payload and retained APR-object/setaside memory/CPU "
            "exposure. Do not process a prefix and release an uninspected tail: exceeding either connector "
            "limit must fail closed."
        ),
        "phase_relevance": (
            "P4 only. The byte limit and the fixed bucket ceiling apply while normalized brigades are "
            "retained through first EOS for the all-response enforcement decision; the bucket count spans "
            "filter calls and resets on release or discard."
        ),
    },
}


def _directive_option(
    connector: str,
    name: str,
    source_file: str,
    source_symbol: str,
    syntax: str,
    contexts: str,
    inheritance: str,
    merge: str,
    validation: str,
    example: str,
) -> dict[str, Any]:
    detail = dict(DIRECTIVE_DETAILS[name])
    if connector == "apache":
        detail.update(APACHE_DIRECTIVE_DETAILS.get(name, {}))
    return _option(
        connector,
        name,
        "host_connector_directive",
        source_file,
        source_symbol,
        syntax=syntax,
        value_type=detail["type"],
        allowed_values=detail["values"],
        default=detail["default"],
        default_source=detail["default_source"],
        required=False,
        contexts=contexts,
        inheritance=inheritance,
        merge_behavior=merge,
        validation=validation,
        phase_relevance=detail.get(
            "phase_relevance",
            "P1 controls integration; rules and P4 controls affect the stated phase only.",
        ),
        security_relevance=detail["security"],
        runtime_effect=detail["effect"],
        example_file=example,
        description=detail["effect"],
        deprecated=(connector == "apache" and name == "modsecurity_phase4_content_types_file"),
    )


def extract_apache(root: Path) -> list[dict[str, Any]]:
    source = "connectors/apache/src/msc_config.c"
    text = _read(root, source)
    macros = directive_macros(root)
    expected = re.findall(
        r"AP_INIT_(TAKE[12])\s*\(\s*(MSCONNECTOR_DIRECTIVE_[A-Z0-9_]+)\s*,\s*(msc_[a-z0-9_]+)",
        text,
        flags=re.S,
    )
    if len(expected) != 11:
        raise ValueError(f"Apache command_rec extractor found {len(expected)}, expected 11")
    result: list[dict[str, Any]] = []
    for take, macro, handler in expected:
        name = macros[macro]
        if name not in DIRECTIVE_DETAILS:
            raise ValueError(f"Apache directive lacks reference metadata: {name}")
        syntax = f"{name} " + ({"TAKE1": "<value>", "TAKE2": "<key> <url>"}[take])
        if name == "modsecurity":
            syntax = "modsecurity On | Off"
        elif name == "modsecurity_phase4_mode":
            syntax = "modsecurity_phase4_mode minimal | safe | strict"
        elif name == "modsecurity_phase4_body_limit":
            syntax = "modsecurity_phase4_body_limit <positive-bytes>"
        elif name == "modsecurity_transaction_id_expr":
            syntax = "modsecurity_transaction_id_expr <apache-string-expression>"
        example = (
            "connectors/apache/src/msc_config.c"
            if name == "modsecurity_phase4_content_types_file"
            else "examples/apache/minimal/httpd.conf"
            if name in {"modsecurity", "modsecurity_rules_file", "modsecurity_use_error_log"}
            else "examples/apache/safe/httpd.conf"
        )
        result.append(_directive_option(
            "apache", name, source, f"module_directives[] / {handler}", syntax,
            "Apache RSRC_CONF | ACCESS_CONF (server/vhost and per-directory contexts supported by Apache's context rules)",
            "Parent value is available to the child unless a child value is set; see the Apache directory-config merge function.",
            "Common scalar values use child-over-parent merge; rule sets are merged through msc_rules_merge. Transaction-id expression/static-id are mutually exclusive.",
            f"{handler} returns an Apache configuration error for its documented invalid input; validate the installed configuration with apachectl -t.",
            example,
        ))
    return result


def extract_nginx(root: Path) -> list[dict[str, Any]]:
    source = "connectors/nginx/src/ngx_http_modsecurity_module.c"
    text = _read(root, source)
    macros = directive_macros(root)
    table = text[text.index("static ngx_command_t ngx_http_modsecurity_commands"):text.index("ngx_null_command", text.index("static ngx_command_t ngx_http_modsecurity_commands"))]
    expected = re.findall(
        r"ngx_string\((MSCONNECTOR_DIRECTIVE_[A-Z0-9_]+)\)\s*,\s*([^,]+)\s*,\s*([a-zA-Z0-9_]+)",
        table,
        flags=re.S,
    )
    if len(expected) != 10:
        raise ValueError(f"NGINX ngx_command_t extractor found {len(expected)}, expected 10")
    result: list[dict[str, Any]] = []
    for macro, context_flags, handler in expected:
        name = macros[macro]
        if name not in DIRECTIVE_DETAILS:
            raise ValueError(f"NGINX directive lacks reference metadata: {name}")
        syntax = f"{name} <value>;"
        if name in {"modsecurity", "modsecurity_use_error_log"}:
            syntax = f"{name} on | off;"
        elif name == "modsecurity_phase4_mode":
            syntax = "modsecurity_phase4_mode minimal | safe | strict;"
        elif name == "modsecurity_phase4_body_limit":
            syntax = "modsecurity_phase4_body_limit <positive-bytes>;"
        elif name == "modsecurity_rules_remote":
            syntax = "modsecurity_rules_remote <key> <url>;"
        option = _directive_option(
            "nginx", name, source, f"ngx_http_modsecurity_commands[] / {handler}", syntax,
            "NGX_HTTP_MAIN_CONF (http), NGX_HTTP_SRV_CONF (server), NGX_HTTP_LOC_CONF (location)",
            "http → server → location; a child inherits if it does not set a value.",
            "ngx_conf_merge_* combines scalar/pointer configuration, while msc_rules_merge combines parent and child rules.",
            f"{handler} rejects invalid values during nginx -t; {context_flags.strip()} is the registered context mask.",
            "examples/nginx/minimal/nginx.conf" if name in {"modsecurity", "modsecurity_rules_file"} else "examples/nginx/safe/nginx.conf",
        )
        if name == "modsecurity_rules_file":
            # The registration only proves the directive shape.  Keep the
            # path, loader, and Include semantics tied to the native setter
            # instead of borrowing assumptions from Apache or a host manual.
            effect = (
                "During NGINX configuration loading, ngx_conf_set_rules_file passes the supplied "
                "path to libmodsecurity's msc_rules_add_file. The NGINX setter neither "
                "canonicalizes nor requires an absolute path; use an absolute path to avoid "
                "a process-working-directory dependency. A missing, unreadable, or invalid "
                "top-level rule file returns the libmodsecurity loader error and fails the "
                "configuration check/reload. Include and IncludeOptional inside that file are "
                "then interpreted by libmodsecurity, not expanded by the NGINX parser. Unlike "
                "modsecurity_rules, which sends one inline configuration string to msc_rules_add, "
                "this directive sends a file path to msc_rules_add_file; both contribute to the "
                "configured rule set and its normal parent/child merge."
            )
            option.update(
                allowed_values=(
                    "one readable libmodsecurity configuration/rules path; absolute paths are "
                    "recommended, while relative-path resolution is delegated to libmodsecurity"
                ),
                runtime_effect=effect,
                description=effect,
                validation=(
                    "ngx_conf_set_rules_file calls msc_rules_add_file while nginx -t/configuration "
                    "loading runs. A missing, unreadable, or syntactically invalid top-level rule "
                    "file (including an engine Include failure) returns the loader error and rejects "
                    "the NGINX configuration."
                ),
                security_relevance=(
                    "Keep the file, its parent directories, and any engine-included files "
                    "non-writable by untrusted identities. Prefer an absolute path so a changed "
                    "working directory cannot select unintended policy."
                ),
            )
        elif name == "modsecurity_phase4_mode":
            # Both non-strict enum values deliberately resolve through the
            # common log-only branch.  Strict is a transport action, never a
            # promise that a response status already sent to a client changes.
            effect = (
                "Before response headers/body are committed, minimal, safe, and strict all resolve "
                "a P4 intervention as deny_if_possible, so NGINX can still return the requested "
                "engine status (or 403 fallback). Once headers are committed or the body started, "
                "minimal and safe both use the common log_only action; they record the late decision "
                "without a later status rewrite. Strict instead resolves to abort_connection: the "
                "native body filter marks the connection as errored, records connection_aborted, and "
                "returns NGX_ERROR. The known host boundary is that NGINX invokes the P4 engine finish "
                "only at last_buf/last_in_chain after bounded in-scope body accumulation, so a response "
                "may already be visible. Strict can therefore terminate a connection, but cannot "
                "guarantee a later 403 or replace an already-sent status line."
            )
            option.update(
                allowed_values=(
                    "minimal | safe | strict; before commit all use deny_if_possible, after commit "
                    "minimal/safe are log_only and strict is abort_connection"
                ),
                phase_relevance=(
                    "P4 only. The response-body filter accumulates bounded in-scope bytes and finishes "
                    "the engine at EOS (last_buf/last_in_chain); header/body commitment determines "
                    "whether a status or only a late transport action remains possible."
                ),
                runtime_effect=effect,
                description=effect,
                validation=(
                    "ngx_conf_set_phase4_mode accepts only minimal|safe|strict during nginx -t. Runtime "
                    "late behavior is source-defined: non-strict post-commit paths emit log_only; strict "
                    "marks the connection errored and returns NGX_ERROR, without manufacturing a later 403."
                ),
                security_relevance=(
                    "safe/minimal retain late-decision evidence without interrupting an already-started "
                    "response. strict requests a connection abort after commit, which can expose clients "
                    "to a partial response; it is not a reliable post-commit HTTP-status enforcement mode."
                ),
            )
        result.append(option)
    return result


def extract_haproxy(root: Path) -> list[dict[str, Any]]:
    source = "connectors/haproxy/htx-overlay/haproxy_modsecurity_htx_filter.c"
    text = _read(root, source)
    required = ("modsecurity-htx", "rules-file", "phase4-mode")
    if any(token not in text for token in required):
        raise ValueError("HAProxy HTX parser surface is incomplete")
    common = dict(
        contexts="The selected and checked-in native use is a HAProxy frontend. The local parser does not assert additional host scopes.",
        inheritance="No connector-local inheritance callback is registered; each filter declaration owns one filter configuration.",
        merge_behavior="No connector-local merge; filter arguments initialise a per-filter common configuration.",
        example="examples/haproxy/safe/haproxy-htx.cfg",
    )
    result = [
        _option("haproxy", "filter modsecurity-htx", "host_connector_directive", source,
                "haproxy_modsecurity_htx_filter_keywords / haproxy_modsecurity_htx_filter_parse",
                syntax="filter modsecurity-htx rules-file <path> [phase4-mode minimal|safe|strict]",
                value_type="HAProxy filter declaration", allowed_values="one required rules-file argument; optional phase4-mode",
                default="not applicable; a filter is active only when declared", default_source="native HTX keyword parser",
                required=True, contexts=common["contexts"], inheritance=common["inheritance"], merge_behavior=common["merge_behavior"],
                validation="The patched HAProxy parser rejects missing/unknown arguments; validate with haproxy -c -f <config>.",
                phase_relevance="P1–P4 native HTX callbacks are attached only when this filter is declared.",
                security_relevance="A stock HAProxy binary does not provide this keyword; do not silently substitute SPOE.",
                runtime_effect="Registers the repository's native HTX filter and creates the config passed to the lifecycle callbacks.",
                example_file=common["example"], description="Native HTX full-lifecycle filter declaration."),
        _option("haproxy", "rules-file", "host_connector_directive", source,
                "haproxy_modsecurity_htx_filter_parse / msc_rules_add_file",
                syntax="rules-file <path>", value_type="path", allowed_values="one readable rules/configuration path",
                default="none; required", default_source="native HTX parser requires rules-file",
                required=True, contexts=common["contexts"], inheritance=common["inheritance"], merge_behavior=common["merge_behavior"],
                validation="Missing argument or rule-load failure fails native filter initialisation.",
                phase_relevance="Rules can evaluate P1–P4 through the declared HTX filter.",
                security_relevance="Protect policy-file ownership and permissions.", runtime_effect="Loads rules with msc_rules_add_file during filter initialisation.",
                example_file=common["example"], description="Required native HTX rule-file argument."),
        _option("haproxy", "phase4-mode", "host_connector_directive", source,
                "haproxy_modsecurity_htx_filter_parse / msconnector_parse_phase4_mode",
                syntax="phase4-mode minimal | safe | strict", value_type="enum", allowed_values="minimal | safe | strict",
                default="safe", default_source="common/include/msconnector/options.h:MSCONNECTOR_DEFAULT_PHASE4_MODE",
                required=False, contexts=common["contexts"], inheritance=common["inheritance"], merge_behavior=common["merge_behavior"],
                validation="Unknown mode fails parsing. The selected host uses haproxy -c -f <config>.",
                phase_relevance="P4 only. The current HTX host action distinguishes strict from non-strict; minimal and safe share the non-strict late log-only path.",
                security_relevance="strict records an abort policy request but the native HTX path currently records host action not_attempted; it is not an abort guarantee.",
                runtime_effect="Initialises common_config.phase4_mode for the filter.", example_file=common["example"], description="Native HTX late-P4 policy argument."),
        _option("haproxy", "filter spoe", "compatibility", "examples/haproxy/compatibility-spoe/haproxy-request-only.cfg",
                "compatibility-spoe example", syntax="filter spoe engine <name> config <file>", value_type="compatibility filter", allowed_values="HAProxy SPOE syntax only",
                default="not part of the native HTX path", default_source="compatibility example", required=False,
                contexts="Compatibility frontend only", inheritance="not documented as native inheritance", merge_behavior="not part of native HTX merge", validation="Separate compatibility smoke/configuration only.",
                phase_relevance="Compatibility request path; it is not a native HTX P3/P4 configuration.", security_relevance="Do not promote this historical path as the selected native core.",
                runtime_effect="Routes to the separate SPOE/SPOP compatibility service.", example_file="examples/haproxy/compatibility-spoe/haproxy-request-only.cfg", description="Compatibility-only SPOE filter.", compatibility_only=True),
    ]
    compatibility_source = "connectors/haproxy/src/haproxy_spop_diagnostic_runtime.c"
    compatibility_text = _read(root, compatibility_source)
    parser_body = compatibility_text[compatibility_text.index("static int config_set"):compatibility_text.index("static char *trim_in_place")]
    raw_compatibility_keys = list(dict.fromkeys(re.findall(r'"([a-z][a-z-]+)"', parser_body)))
    expected_compatibility_keys = {
        "listen", "host", "port", "ready-file", "pid-file", "port-file", "log-file", "decision-log", "audit-log", "modsecurity-conf", "crs-root", "rules-file", "rules-dir", "mode", "fail-mode", "runtime-mode", "variant", "case", "expected-status", "request-body-limit", "response-body-limit", "response-body-timeout", "spoe-timeout", "worker-count", "max-transactions", "debug", "enable-response-headers", "response-phases",
    }
    parser_literals = {"true", "yes", "on", "false", "off", "no"}
    unexpected = set(raw_compatibility_keys) - expected_compatibility_keys - parser_literals
    compatibility_keys = [key for key in raw_compatibility_keys if key in expected_compatibility_keys]
    if set(compatibility_keys) != expected_compatibility_keys or unexpected:
        raise ValueError(f"HAProxy SPOP parser/schema drift: missing={sorted(expected_compatibility_keys - set(compatibility_keys))}, unexpected={sorted(unexpected)}")
    defaults = {
        "host": "127.0.0.1", "mode": "block", "fail-mode": "closed", "runtime-mode": "production", "variant": "-", "log-file": "-",
        "request-body-limit": "65532", "response-body-limit": "0", "response-body-timeout": "0", "spoe-timeout": "2000", "worker-count": "1", "max-transactions": "4096", "response-phases": "false",
    }
    for key in compatibility_keys:
        value_type = "string/path"
        allowed = "parser-supported compatibility value"
        if key in {"port", "expected-status", "request-body-limit", "response-body-limit", "response-body-timeout", "spoe-timeout", "worker-count", "max-transactions"}:
            value_type, allowed = "integer", "decimal integer"
        elif key in {"debug", "enable-response-headers", "response-phases"}:
            value_type, allowed = "boolean", "on/off-style compatibility boolean"
        elif key in {"mode", "fail-mode", "runtime-mode"}:
            value_type = "compatibility policy string"
        effect = "SPOP compatibility-agent configuration; it is not a native HTX filter option."
        if key in {"response-body-limit", "response-body-timeout", "response-phases", "enable-response-headers"}:
            effect = "Compatibility response control. The selected SPOE messages do not supply a response body, so this is not native P4 support."
        result.append(_option(
            "haproxy", f"spoe-agent:{key}", "compatibility", compatibility_source, f"config_set(key={key})",
            syntax=f"{key}=<value>", value_type=value_type, allowed_values=allowed,
            default=defaults.get(key, "unset unless configured"), default_source="config_init() where stated; otherwise zero/empty initialization",
            required=False, contexts="SPOE/SPOP compatibility agent key=value file", inheritance="No native HTX inheritance; one compatibility-agent config file.",
            merge_behavior="No merge; config_set applies one parsed value.", validation="Unknown keys fail compatibility-agent configuration parsing.",
            phase_relevance="Compatibility request/response-header path only; no native response-body lifecycle claim.",
            security_relevance="Compatibility logs, ports, rules, and fail policy require operator review; do not promote this path to the selected native core.",
            runtime_effect=effect, example_file="examples/haproxy/compatibility-spoe/modsecurity-agent.conf", description=effect,
            compatibility_only=True,
        ))
    result.append(_option(
        "haproxy", "legacy-phase4-strict-abort", "compatibility", "examples/haproxy/compatibility-spoe/legacy-phase4-strict-abort.cfg", "disabled historical example",
        syntax="legacy / disabled example", value_type="historical configuration", allowed_values="not an active selected option", default="not available", default_source="legacy example header", required=False,
        contexts="Historical compatibility documentation only", inheritance="not applicable", merge_behavior="not applicable", validation="Do not use for native validation.",
        phase_relevance="No selected response-body P4 path.", security_relevance="Never use as P4 or strict-abort evidence.", runtime_effect="Retained solely to explain retired compatibility material.",
        example_file="examples/haproxy/compatibility-spoe/legacy-phase4-strict-abort.cfg", description="Disabled historical compatibility material.", implemented=False, compatibility_only=True, deprecated=True,
    ))
    return result


def extract_lighttpd(root: Path) -> list[dict[str, Any]]:
    source = "connectors/lighttpd/module/mod_msconnector.c"
    text = _read(root, source)
    keys = re.findall(r'CONST_STR_LEN\("(msconnector\.[^\"]+)"\)\s*,\s*\n?\s*(T_CONFIG_[A-Z]+)\s*,\s*\n?\s*(T_CONFIG_SCOPE_[A-Z]+)', text)
    if keys != [("msconnector.enabled", "T_CONFIG_BOOL", "T_CONFIG_SCOPE_SERVER"), ("msconnector.config-file", "T_CONFIG_STRING", "T_CONFIG_SCOPE_SERVER")]:
        raise ValueError(f"lighttpd plugin key extractor found unexpected keys: {keys!r}")
    values: list[dict[str, Any]] = []
    values.append(_option(
        "lighttpd", "msconnector.enabled", "host_connector_directive", source,
        "mod_msconnector_set_defaults / config_plugin_values_init",
        syntax='msconnector.enabled = "enable" | "disable"', value_type="lighttpd boolean", allowed_values="lighttpd boolean values; examples use enable/disable",
        default="off", default_source="ck_calloc plugin_data allocation and default config", required=False,
        contexts="T_CONFIG_SCOPE_SERVER", inheritance="Only defaults are loaded; the module has no request-time conditional patch path.",
        merge_behavior="config_plugin_values_init populates defaults; no documented per-request merge.",
        validation="When enabled, lighttpd validates the runtime file during set-defaults; validate host syntax with lighttpd -tt -f <config>.",
        phase_relevance="off disables the module P1/P3 callbacks and any patched P2/P4 callbacks.",
        security_relevance="Disabling the module bypasses connector processing even if a rule file exists.",
        runtime_effect="Selects whether mod_msconnector initialises Common Runtime.", example_file="examples/lighttpd/minimal/lighttpd.conf",
        description="Enables the native lighttpd plugin."))
    values.append(_option(
        "lighttpd", "msconnector.config-file", "host_connector_directive", source,
        "mod_msconnector_set_defaults / msconnector_runtime_config_check",
        syntax='msconnector.config-file = "<runtime-key-value-file>"', value_type="path", allowed_values="non-empty readable Common Runtime key=value file",
        default="none", default_source="plugin config_file defaults to NULL", required=True,
        contexts="T_CONFIG_SCOPE_SERVER", inheritance="Only defaults are loaded; no documented conditional request-time override.",
        merge_behavior="Plugin defaults retain the configured string.",
        validation="Required only when msconnector.enabled is true; missing, unreadable, or invalid runtime configuration returns HANDLER_ERROR during startup.",
        phase_relevance="The referenced Common Runtime file chooses body modes and P1–P4 policy.",
        security_relevance="The runtime file contains executable rule paths and limits; use trusted ownership and permissions.",
        runtime_effect="Loads and creates the connector-neutral runtime before requests are served.", example_file="examples/lighttpd/minimal/lighttpd.conf",
        description="Path to the Common Runtime configuration used by the native plugin."))
    values.append(_option(
        "lighttpd", "sidecar proxy", "compatibility", "examples/lighttpd/compatibility-sidecar/lighttpd-sidecar-proxy.conf",
        "compatibility-sidecar example", syntax="proxy.server = (...)", value_type="compatibility host setup", allowed_values="ordinary lighttpd proxy fields",
        default="not a native connector option", default_source="compatibility example", required=False,
        contexts="Compatibility example", inheritance="not applicable to native plugin", merge_behavior="not part of mod_msconnector", validation="Validate as ordinary lighttpd proxy configuration.",
        phase_relevance="No native mod_msconnector lifecycle claim.", security_relevance="Do not treat a proxy endpoint as a configured native ModSecurity integration.",
        runtime_effect="Compatibility-only proxy routing.", example_file="examples/lighttpd/compatibility-sidecar/lighttpd-sidecar-proxy.conf", description="Compatibility-only sidecar proxy setup.", compatibility_only=True))
    compatibility_example = "examples/lighttpd/compatibility-sidecar/lighttpd-sidecar-proxy.conf"
    compatibility_fields = sorted(set(re.findall(r"^\s*([A-Za-z0-9_.-]+)\s*=", _read(root, compatibility_example), flags=re.M)))
    for field in compatibility_fields:
        values.append(_option(
            "lighttpd", f"compatibility.{field}", "compatibility", compatibility_example, f"compatibility-sidecar field {field}",
            syntax=f"{field} = <value>", value_type="lighttpd compatibility host field", allowed_values="explicit compatibility example value",
            default="not part of native mod_msconnector", default_source="compatibility example", required=False,
            contexts="lighttpd sidecar compatibility configuration", inheritance="Host-defined compatibility behavior; not native plugin inheritance.",
            merge_behavior="Host-defined compatibility behavior; not part of mod_msconnector.", validation="Validate as ordinary lighttpd proxy configuration.",
            phase_relevance="No native connector lifecycle claim.", security_relevance="Compatibility-only host routing; do not represent it as native ModSecurity configuration.",
            runtime_effect="Configures the retained sidecar compatibility example.", example_file=compatibility_example,
            description="Compatibility-only lighttpd host field.", compatibility_only=True,
        ))
    return values


COMMON_DETAILS: dict[str, dict[str, str]] = {
    "enabled": ("boolean", "on | off | true | false | 1 | 0 | yes | no", "off", "common/src/config.c:msconnector_config_apply_defaults", "Enables the Common Runtime; enabled runtime requires an inline, file, or remote rule source."),
    "use_error_log": ("boolean", "on | off | true | false | 1 | 0 | yes | no", "on", "common/include/msconnector/options.h:MSCONNECTOR_DEFAULT_USE_ERROR_LOG", "Stores the Common logging preference. A connector must consume it before a host logging effect can be claimed."),
    "rules_inline": ("string", "one inline rule/configuration string", "none", "runtime parser has no default", "Adds inline rule configuration."),
    "rules_file": ("path", "one readable rule/configuration file", "none", "runtime parser has no default", "Loads rules from a local file."),
    "rules_remote_key": ("string", "remote key paired with rules_remote_url", "none", "runtime parser has no default", "Supplies one half of a remote-rule pair."),
    "rules_remote_url": ("URL", "remote URL paired with rules_remote_key", "none", "runtime parser has no default", "Supplies the remote-rule endpoint; the selected examples do not exercise it."),
    "transaction_id": ("string", "non-empty text", "none", "runtime parser has no default", "Sets a static runtime transaction identifier."),
    "transaction_id_header": ("header name", "non-empty HTTP header name", "x-request-id", "common/runtime/msconnector_runtime.c:runtime_defaults", "Selects the fallback correlation-header name."),
    "phase4_mode": ("enum", "minimal | safe | strict", "safe", "common/include/msconnector/options.h:MSCONNECTOR_DEFAULT_PHASE4_MODE", "Stores the late P4 policy. Common alone owns no host abort primitive."),
    "phase4_content_types_file": ("path", "one configuration path", "none", "runtime parser has no default", "Stores a content-type file path; consumption is connector-specific."),
    "event_path": ("path", "path without a parent-directory segment", "none", "runtime parser has no default", "Appends metadata-only JSONL events when configured."),
    "phase4_event_log": ("path alias", "same grammar as event_path", "none", "runtime parser has no default", "Alias for event_path."),
    "request_body_mode": ("enum", "none | buffered | streaming", "buffered", "common/runtime/msconnector_runtime.c:runtime_defaults", "Selects the Common request-body handling mode; a particular host may support only a subset."),
    "response_body_mode": ("enum", "none | buffered | streaming", "none", "common/runtime/msconnector_runtime.c:runtime_defaults", "Selects the Common response-body handling mode; a particular host may support only a subset."),
    "request_body_limit": ("positive decimal bytes", "positive integer", "1048576", "common/include/msconnector/limits.h:MSCONNECTOR_MAX_BODY_BUFFER_SIZE", "Bounds request bytes offered to the engine."),
    "response_body_limit": ("positive decimal bytes", "positive integer", "1048576", "common/include/msconnector/limits.h:MSCONNECTOR_MAX_RESPONSE_BODY_BUFFER_SIZE", "Bounds response bytes offered to the engine."),
    "body_limit_action": ("enum", "reject | process_partial (accepted spelling variants are parser-specific)", "reject", "common/src/config.c:msconnector_config_apply_defaults", "Controls whether an over-limit chunk is rejected or truncated before engine input."),
    "late_intervention_timeout": ("non-negative decimal milliseconds", "0 or positive integer", "0", "common/src/config.c:msconnector_config_apply_defaults", "Stores an optional late-intervention budget; Common owns no timer/cancellation primitive."),
    "default_block_status": ("HTTP status", "allowed blocking status", "403", "common/include/msconnector/block_statuses.h:MSCONNECTOR_DEFAULT_BLOCK_STATUS", "Fallback status for supported pre-commit block actions."),
    "default_error_status": ("HTTP error status", "valid HTTP error status", "500", "common/include/msconnector/block_statuses.h:MSCONNECTOR_DEFAULT_ERROR_STATUS", "Fallback status for runtime errors."),
    "max_header_count": ("positive decimal count", "positive integer", "256", "common/include/msconnector/limits.h:MSCONNECTOR_MAX_HEADER_COUNT", "Bounds accepted header count."),
    "max_header_name_size": ("positive decimal bytes", "positive integer", "256", "common/include/msconnector/limits.h:MSCONNECTOR_MAX_HEADER_NAME_LENGTH", "Bounds each header-name size."),
    "max_header_value_size": ("positive decimal bytes", "positive integer", "8192", "common/include/msconnector/limits.h:MSCONNECTOR_MAX_HEADER_VALUE_LENGTH", "Bounds each header-value size."),
    "max_total_header_bytes": ("positive decimal bytes", "positive integer", "65536", "common/include/msconnector/limits.h:MSCONNECTOR_MAX_TOTAL_HEADER_BYTES", "Bounds total header bytes."),
    "max_event_json_bytes": ("positive decimal bytes", "positive integer", "16384", "common/include/msconnector/limits.h:MSCONNECTOR_MAX_EVENT_JSON_BYTES", "Bounds serialized metadata event size."),
}


def extract_common_runtime(root: Path) -> list[dict[str, Any]]:
    source = "common/runtime/msconnector_runtime.c"
    text = _read(root, source)
    # This is a parser-branch extractor, not a scan of a documentation list.
    keys = re.findall(r'strcmp\(key, "([a-z0-9_]+)"\)', text)
    keys = list(dict.fromkeys(keys))
    missing = set(COMMON_DETAILS) - set(keys)
    unexpected = set(keys) - set(COMMON_DETAILS)
    if missing or unexpected:
        raise ValueError(f"Common Runtime parser/schema drift: missing={sorted(missing)}, unexpected={sorted(unexpected)}")
    profile_keys: set[str] = set()
    for connector in ("envoy", "traefik", "lighttpd"):
        for config in (root / "examples" / connector).glob("**/*.conf"):
            if config.name not in {"msconnector-runtime.conf", "traefik-engine-service.conf"}:
                continue
            for line in config.read_text(encoding="utf-8").splitlines():
                match = re.match(r"\s*([a-z0-9_]+)=", line)
                if match:
                    profile_keys.add(match.group(1))
    undocumented_profile_keys = profile_keys - set(COMMON_DETAILS)
    if undocumented_profile_keys:
        raise ValueError(f"Common Runtime profile uses undocumented parser keys: {sorted(undocumented_profile_keys)}")
    options: list[dict[str, Any]] = []
    for name in keys:
        value_type, allowed, default, default_source, effect = COMMON_DETAILS[name]
        options.append(_option(
            "common", name, "common_runtime", source, f"assign_config_value(key={name})",
            syntax=f"{name}=<value>", value_type=value_type, allowed_values=allowed,
            default=default, default_source=default_source, required=False,
            contexts="Common Runtime key=value file", inheritance="No file-level inheritance; host integrations may merge their own configuration before starting Common Runtime.",
            merge_behavior="When a host uses msconnector_config, scalar child values override parent values; runtime files are parsed as one concrete configuration.",
            validation="Unknown keys, empty values, malformed assignments, and key-specific invalid values fail the runtime configuration check.",
            phase_relevance="See runtime effect; body modes/limits affect P2 and P4, header limits affect P1 and P3.",
            security_relevance=("Limits bound resource use. " + effect), runtime_effect=effect,
            example_file="examples/lighttpd/safe/msconnector-runtime.conf", description=effect,
        ))
    return options


ENGINE_DETAILS: dict[str, tuple[str, str, str, str]] = {
    "SecRuleEngine": ("SecRuleEngine On | Off | DetectionOnly", "On | Off | DetectionOnly", "The used examples select On; no repository source establishes a global engine default.", "Controls rule execution/disruptive action inside libmodsecurity, independently of the host connector switch."),
    "SecRequestBodyAccess": ("SecRequestBodyAccess On | Off", "On | Off", "No default is inferred from examples.", "On makes request-body input available to engine P2 only when the host supplies it; Off leaves P1 headers available but removes body input from P2. The directive itself sets neither a body-size limit nor a request MIME scope: those remain host/engine mapping choices and, where selected, Common Runtime request_body_limit/body mode controls. Enabling body handling can add buffering, memory, CPU, and logging exposure, so retain bounded host input."),
    "SecResponseBodyAccess": ("SecResponseBodyAccess On | Off", "On | Off", "No default is inferred from examples.", "On makes P4 possible only when the host supplies response bytes that are in scope; Off removes response-body input from P4. It does not widen SecResponseBodyMimeType, override SecResponseBodyLimit/SecResponseBodyLimitAction, or force a status change after headers commit. With the selected safe late-intervention policy, a post-commit disruptive result is recorded as log_only rather than a promised later 403; response capture can add bounded memory, CPU, and sensitive-data exposure."),
    "SecResponseBodyMimeType": ("SecResponseBodyMimeType <type/subtype> [...]", "one or more MIME types", "No default is inferred from examples.", "Scopes engine response-body inspection by MIME type."),
    "SecResponseBodyLimit": ("SecResponseBodyLimit <bytes>", "positive byte count", "No default is inferred from examples.", "Caps engine response-body input."),
    "SecResponseBodyLimitAction": ("SecResponseBodyLimitAction ProcessPartial | Reject", "ProcessPartial | Reject", "No default is inferred from examples.", "Defines engine behavior when the response body exceeds the engine limit."),
    "SecAuditEngine": ("SecAuditEngine RelevantOnly", "engine audit mode", "No default is inferred from examples.", "Enables the selected audit-log policy."),
    "SecAuditLogType": ("SecAuditLogType Serial", "audit log type", "No default is inferred from examples.", "Sets the selected audit-log write mode."),
    "SecAuditLogParts": ("SecAuditLogParts <parts>", "audit part letters", "No default is inferred from examples.", "Selects audit-log parts."),
    "SecAuditLog": ("SecAuditLog <path>", "path", "No default is inferred from examples.", "Sets the engine audit-log path."),
    "IncludeOptional": ("IncludeOptional <path-or-glob>", "path or glob", "No default is inferred from examples.", "Loads optional engine configuration/rules if present."),
    "SecRule": ("SecRule VARIABLE \"OPERATOR\" \"id:<id>,phase:<n>,actions\"", "rule expression", "No default is inferred from examples.", "Defines a rule from a variable, operator, and comma-separated actions. The local illustration uses RESPONSE_BODY, @contains, id, phase, deny, log, and status; redirect and transformations are separate action forms whose validity and observable effect remain engine/host- and commit-boundary dependent."),
}


# The common section renderer supplies standard fields for every engine
# directive.  These overrides retain the cross-directive relationships that a
# reader needs for the body-access switches and rule action syntax without
# inventing a libmodsecurity default that is not established by this repo.
ENGINE_RUNTIME_OVERRIDES: dict[str, dict[str, str]] = {
    "SecRequestBodyAccess": {
        "phase_relevance": (
            "P2. On permits body inspection only after the connector has supplied request bytes; "
            "the selected host/runtime body mode and limit determine how many bytes can reach the engine."
        ),
        "validation": (
            "The host/libmodsecurity rejects invalid engine syntax when loading the rule file. "
            "A syntactically valid On still cannot create P2 input when the selected host path "
            "does not expose a request body."
        ),
        "security_relevance": (
            "Request bodies may contain credentials or personal data. Use bounded body limits, "
            "appropriate MIME/parser policy, and protected audit/debug logs; no performance "
            "quantity is inferred here."
        ),
    },
    "SecResponseBodyAccess": {
        "phase_relevance": (
            "P4. On is necessary but not sufficient: the connector must expose response bytes, "
            "the MIME type must be in SecResponseBodyMimeType scope, and host/engine response limits apply."
        ),
        "validation": (
            "The host/libmodsecurity rejects invalid engine syntax when loading the rule file. "
            "At runtime, an out-of-scope MIME type, disabled host body path, or exceeded limit "
            "can leave P4 without the expected complete body input."
        ),
        "security_relevance": (
            "Response bodies can be large and sensitive. Keep MIME scope and response limits narrow, "
            "protect logs, and do not equate safe post-commit evidence with a client-visible later 403."
        ),
    },
    "SecRule": {
        "phase_relevance": (
            "The phase action selects the evaluation point; the local RESPONSE_BODY example uses P4. "
            "A disruptive action can affect the visible HTTP result only while the host can still intervene."
        ),
        "validation": (
            "The host/libmodsecurity rejects malformed variable/operator/action syntax, duplicate or "
            "invalid identifiers, and invalid action combinations when loading the rule file."
        ),
        "security_relevance": (
            "Rules are executable security policy. Give each rule a stable id, keep transformations "
            "explicit and minimal, protect rule-file ownership, and verify disruptive/redirect behavior "
            "on the selected host before relying on it."
        ),
    },
}


def extract_engine_directives(root: Path) -> list[dict[str, Any]]:
    seen: dict[str, str] = {}
    for path in sorted((root / "examples").glob("*/rules/*.conf")):
        for line in path.read_text(encoding="utf-8").splitlines():
            match = re.match(r"\s*(Sec[A-Za-z0-9]+|Include[A-Za-z0-9]+)\b", line)
            if match:
                seen.setdefault(match.group(1), path.relative_to(root).as_posix())
    if set(seen) != set(ENGINE_DETAILS):
        raise ValueError(f"ModSecurity directive extractor/schema drift: {sorted(seen)}")
    result: list[dict[str, Any]] = []
    for name in sorted(seen):
        syntax, values, default, effect = ENGINE_DETAILS[name]
        override = ENGINE_RUNTIME_OVERRIDES.get(name, {})
        result.append(_option(
            "engine", name, "modsecurity_engine", seen[name], "used engine directive in checked-in rule examples",
            syntax=syntax, value_type="ModSecurity engine directive", allowed_values=values, default=default,
            default_source="not inferred; only checked-in example usage is documented", required=False,
            contexts="Loaded ModSecurity configuration/rule file", inheritance="Engine-specific; not a host connector merge setting.",
            merge_behavior="Engine-specific; include order and rule configuration determine effective behavior.",
            validation=override.get("validation", "The host/libmodsecurity rejects invalid engine syntax when loading the rule file."),
            phase_relevance=override.get("phase_relevance", "See directive runtime effect."),
            security_relevance=override.get("security_relevance", "Engine policy can inspect, log, detect, or disrupt traffic; protect rule and audit-log paths."),
            runtime_effect=effect, example_file=seen[name], description=effect,
        ))
    return result


def _host_example_option(connector: str, name: str, example_file: str, validation: str) -> dict[str, Any]:
    return _option(
        connector, name, "host_example_field", example_file, f"checked-in {connector} example field",
        syntax=f"{name} <host-specific-value>", value_type="host-owned configuration field", allowed_values="the explicit value in the selected checked-in example",
        default="No connector default; this host field is explicit in the example.", default_source="active example configuration", required=False,
        contexts="The context shown in the checked-in example; consult the pinned host documentation for all host-specific contexts.",
        inheritance="Host-defined; not implemented by this connector.", merge_behavior="Host-defined; not implemented by this connector.", validation=validation,
        phase_relevance="Host setup/routing/logging; it does not itself configure ModSecurity rule-engine phases.",
        security_relevance="Network addresses, paths, and logging destinations must be selected and access-controlled by the operator.",
        runtime_effect="Provides surrounding host setup used by the selected connector example.", example_file=example_file,
        description="Host-owned setting appearing in the checked-in example; it is not a connector directive.",
    )


def _apache_example_names(root: Path) -> list[str]:
    names: set[str] = set()
    for path in sorted((root / "examples" / "apache").glob("*/httpd.conf")):
        for line in path.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if not line or line.startswith("#") or line.startswith("<"):
                continue
            names.add(line.split()[0])
    return sorted(names)


def _nginx_example_names(root: Path) -> list[str]:
    names: set[str] = set()
    for path in sorted((root / "examples" / "nginx").glob("*/nginx.conf")):
        for line in path.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if not line or line.startswith("#") or not line.endswith(";"):
                continue
            names.add(line.split()[0].rstrip(";"))
    return sorted(names)


def _haproxy_example_names(root: Path) -> list[str]:
    names: set[str] = set()
    for path in sorted((root / "examples" / "haproxy").glob("*/haproxy-htx.cfg")):
        for line in path.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if not line or line.startswith("#") or line.startswith(("global", "defaults", "frontend", "backend")):
                continue
            names.add(" ".join(line.split()[:2]) if line.startswith("timeout ") else line.split()[0])
    return sorted(names)


def _lighttpd_example_names(root: Path) -> list[str]:
    names: set[str] = set()
    profile_dirs = {"minimal", "safe", "strict", "detection-only", "disabled"}
    for path in sorted((root / "examples" / "lighttpd").glob("*/*.conf")):
        if path.parent.name not in profile_dirs or not path.name.startswith("lighttpd"):
            continue
        for line in path.read_text(encoding="utf-8").splitlines():
            match = re.match(r"\s*([A-Za-z0-9_.-]+)\s*=", line)
            if match:
                names.add(match.group(1))
    return sorted(names)


def extract_host_example_fields(root: Path, existing: Iterable[dict[str, Any]]) -> list[dict[str, Any]]:
    existing_by_connector: dict[str, set[str]] = defaultdict(set)
    for option in existing:
        existing_by_connector[option["connector"]].add(option["name"])
    result: list[dict[str, Any]] = []
    groups = {
        "apache": (_apache_example_names(root), "examples/apache/safe/httpd.conf", "apachectl -t"),
        "nginx": (_nginx_example_names(root), "examples/nginx/safe/nginx.conf", "nginx -t"),
        "haproxy": (_haproxy_example_names(root), "examples/haproxy/safe/haproxy-htx.cfg", "haproxy -c -f <config>"),
        "lighttpd": (_lighttpd_example_names(root), "examples/lighttpd/safe/lighttpd-http1-identity.conf", "lighttpd -tt -f <config>"),
    }
    for connector, (names, example, validation) in groups.items():
        for name in names:
            if name in existing_by_connector[connector] or name in {"filter", "modsecurity-htx"}:
                continue
            result.append(_host_example_option(connector, name, example, validation))
    return result


def extract_yaml_fields(path: Path) -> list[tuple[str, str]]:
    """Extract YAML mapping paths using indentation and list structure.

    It is intentionally limited to the checked-in, simple YAML templates.  It
    distinguishes list items from mapping keys instead of treating YAML as a
    bag of words, which lets the checker catch nesting drift in the examples.
    """
    result: list[tuple[str, str]] = []
    stack: list[StackEntry] = []
    key_re = re.compile(r'(?:(?:"([^\"]+)")|([A-Za-z_@][A-Za-z0-9_@-]*))\s*:\s*(.*)$')
    for raw in path.read_text(encoding="utf-8").splitlines():
        if not raw.strip() or raw.lstrip().startswith("#"):
            continue
        indent = len(raw) - len(raw.lstrip(" "))
        body = raw.strip()
        list_item = body.startswith("- ")
        if list_item:
            while stack and (stack[-1].indent > indent or (stack[-1].indent == indent and stack[-1].kind == "item")):
                stack.pop()
            parent = stack[-1].path if stack else ""
            item_path = f"{parent}[]" if parent else "[]"
            stack.append(StackEntry(indent, item_path, "item"))
            body = body[2:].strip()
            if not body:
                continue
        else:
            while stack and stack[-1].indent >= indent:
                stack.pop()
        match = key_re.match(body)
        if not match:
            if list_item and body:
                result.append((stack[-1].path, body))
            continue
        key = match.group(1) or match.group(2)
        value = match.group(3).strip()
        parent = stack[-1].path if stack else ""
        field = f"{parent}.{key}" if parent else key
        result.append((field, value))
        # The checked-in compatibility templates use small inline mappings and
        # lists (for example socket_address and entryPoints).  Keep their
        # nested fields in the inventory instead of hiding them in one scalar.
        if value.startswith("{") and value.endswith("}"):
            for inline_key, inline_value in re.findall(r"([A-Za-z_@][A-Za-z0-9_@-]*)\s*:\s*([^,}]+)", value[1:-1]):
                result.append((f"{field}.{inline_key}", inline_value.strip()))
        elif value.startswith("[") and value.endswith("]") and value != "[]":
            for inline_value in value[1:-1].split(","):
                result.append((f"{field}[]", inline_value.strip()))
        if not value or value in {"{}", "[]"}:
            stack.append(StackEntry(indent, field, "mapping"))
    return result


def extract_yaml_paths(path: Path) -> list[str]:
    return list(dict.fromkeys(field for field, _ in extract_yaml_fields(path)))


def extract_yaml_example_values(path: Path) -> dict[str, str]:
    values: dict[str, list[str]] = defaultdict(list)
    for field, value in extract_yaml_fields(path):
        if value:
            values[field].append(value)
    return {field: ", ".join(dict.fromkeys(field_values)) for field, field_values in values.items()}


def _yaml_detail(
    value_type: str,
    allowed_values: str,
    default: str,
    runtime_effect: str,
    security_relevance: str,
    phase_relevance: str,
    *,
    default_source: str,
) -> dict[str, str]:
    """Return the source-scoped metadata for one concrete YAML path.

    YAML is only a serialization layer here.  A bare ``YAML field`` type or an
    "explicit YAML value" pseudo-default would hide whether a setting is a
    listener, route, ext_proc visibility control, or local-plugin control.
    Envoy and Traefik therefore use closed path metadata below.  A new path in
    either selected example fails extraction until it has a real description.
    """
    return {
        "value_type": value_type,
        "allowed_values": allowed_values,
        "default": default,
        "runtime_effect": runtime_effect,
        "security_relevance": security_relevance,
        "phase_relevance": phase_relevance,
        "default_source": default_source,
    }


def _selected_template_default(subject: str, selected: str) -> str:
    """State a non-invented default when the repository owns no host default."""
    return (
        f"No connector-owned {subject} default is declared; the selected template "
        f"sets {selected}."
    )


def _without_compatibility_prefix(path: str) -> str:
    """Recover the real host path from an inventory-only compatibility name."""
    if not path.startswith("compatibility."):
        return path
    _, _, remaining = path.partition(".")
    _, _, remaining = remaining.partition(".")
    return remaining


def _envoy_listener_yaml_detail(path: str, example_value: str, compatibility: bool = False) -> dict[str, str] | None:
    """Describe the selected Envoy listener/HCM/ext_proc path exactly.

    The selected template is intentionally a static bootstrap.  The details
    avoid claiming arbitrary Envoy defaults where this repository only pins an
    explicit example, while relying on the pinned v1.37.0 ext_proc API for the
    protocol defaults that matter to lifecycle visibility.
    """
    prefix = "static_resources.listeners[]"
    tail = path.removeprefix(prefix).lstrip(".")
    base_default_source = "selected Envoy v3 template; connector owns no bootstrap default"
    listener_phase = (
        "Compatibility bootstrap only; this listener carries ext_authz request authorization before the router and does not establish selected native P2/P3/P4 visibility."
        if compatibility else
        "Bootstrap only; this listener carries the selected ext_proc HTTP filter chain, "
        "whose processing_mode exposes P1 request headers, P2 request body chunks, "
        "P3 response headers, and P4 response body chunks."
    )
    policy_filter = "ext_authz compatibility" if compatibility else "ext_proc"
    routing_phase = (
        "Compatibility route selection follows ext_authz P1 request authorization and forwards an allowed request; the compatibility filter has no selected P2/P3/P4 response lifecycle."
        if compatibility else
        "Routes are consulted after P1 request-header filtering; they direct the upstream response that later reaches P3/P4."
    )
    if tail == "name":
        return _yaml_detail(
            "Envoy Listener.name string",
            "unique non-empty listener name in this bootstrap",
            _selected_template_default("listener-name", "`msconnector_ext_proc_listener`"),
            "Names the downstream HTTP listener for Envoy configuration and observability.",
            "A name is control-plane metadata, but it should not disclose tenant or secret identifiers.",
            listener_phase,
            default_source=base_default_source,
        )
    if tail == "address":
        return _yaml_detail(
            "Envoy core.Address mapping",
            "one supported Envoy address form; the example selects socket_address",
            _selected_template_default("listener-address", "a loopback socket_address mapping"),
            "Contains the downstream listener bind address used before the HTTP filter chain runs.",
            "Changing the child socket address changes network exposure before any ModSecurity processing.",
            listener_phase,
            default_source=base_default_source,
        )
    if tail == "address.socket_address":
        return _yaml_detail(
            "Envoy core.SocketAddress mapping",
            "address plus port_value (or another Envoy-supported socket-address form)",
            _selected_template_default("listener socket-address", "127.0.0.1 and @LISTEN_PORT@"),
            "Pairs the listener host and TCP port that accept downstream traffic.",
            "The selected loopback pair keeps the example private; a wildcard bind requires an explicit exposure decision.",
            listener_phase,
            default_source=base_default_source,
        )
    if tail == "address.socket_address.address":
        selected_visibility = (
            "The selected value is loopback-only." if example_value in {"127.0.0.1", "::1"}
            else "A wildcard or public value exposes the listener before ext_proc policy can run."
        )
        return _yaml_detail(
            "Envoy SocketAddress host/IP string",
            "a valid listener host or IP literal; selected value is 127.0.0.1",
            _selected_template_default("listener host", "127.0.0.1"),
            "Binds the downstream HTTP listener to the selected network interface.",
            selected_visibility,
            listener_phase,
            default_source=base_default_source,
        )
    if tail == "address.socket_address.port_value":
        return _yaml_detail(
            "Envoy SocketAddress uint32 TCP port",
            "materializer-validated decimal port 1..65535",
            _selected_template_default("listener port", "the @LISTEN_PORT@ materializer input"),
            "Selects the TCP port on which downstream requests enter the ext_proc filter chain.",
            "Use a private, non-conflicting port; port selection affects reachability before P1.",
            listener_phase,
            default_source="selected template and prepare_envoy_ext_proc_config.sh materializer",
        )
    if tail == "filter_chains":
        return _yaml_detail(
            "repeated Envoy Listener.FilterChain mapping",
            "one or more filter-chain mappings; the example has one HTTP chain",
            _selected_template_default("filter-chain set", "one chain containing the HTTP connection manager"),
            "Defines the network-filter sequence applied to accepted downstream connections.",
            f"Filter ordering determines whether {policy_filter} sees traffic before routing; do not insert an unreviewed bypass.",
            listener_phase,
            default_source=base_default_source,
        )
    if tail == "filter_chains[].filters":
        return _yaml_detail(
            "repeated Envoy NetworkFilter mapping",
            "network filters with a name and typed_config; selected item is HTTP connection manager",
            _selected_template_default("network-filter list", "the HCM filter"),
            f"Installs the HTTP connection manager that owns routing and the nested {policy_filter} HTTP filter chain.",
            f"Removing or replacing HCM removes the selected HTTP/{policy_filter} lifecycle path.",
            listener_phase,
            default_source=base_default_source,
        )
    if tail == "filter_chains[].filters[].name":
        return _yaml_detail(
            "Envoy NetworkFilter factory name",
            "registered network-filter name; selected value is envoy.filters.network.http_connection_manager",
            _selected_template_default("network-filter factory", "the HTTP connection manager factory name"),
            "Selects Envoy's HTTP connection manager implementation for the listener.",
            f"A different network filter can remove HTTP routing and all {policy_filter} visibility.",
            listener_phase,
            default_source=base_default_source,
        )
    if tail == "filter_chains[].filters[].typed_config":
        return _yaml_detail(
            "google.protobuf.Any mapping for HttpConnectionManager",
            "an Any payload whose @type is the Envoy v3 HttpConnectionManager URL",
            _selected_template_default("HCM typed configuration", "the explicit HttpConnectionManager payload"),
            "Carries the HCM stat prefix, inline route configuration, and ordered HTTP filters.",
            "The payload controls which filters receive downstream traffic; validate the concrete type URL with Envoy.",
            listener_phase,
            default_source=base_default_source,
        )
    if tail == "filter_chains[].filters[].typed_config.@type":
        return _yaml_detail(
            "protobuf Any type URL string",
            "type.googleapis.com/envoy.extensions.filters.network.http_connection_manager.v3.HttpConnectionManager",
            _selected_template_default("HCM Any type", "the explicit v3 HttpConnectionManager URL"),
            "Lets Envoy decode the surrounding typed_config as an HTTP connection manager.",
            "A mismatched type URL prevents a valid HTTP/ext_proc listener configuration.",
            listener_phase,
            default_source=base_default_source,
        )
    hcm_prefix = "filter_chains[].filters[].typed_config"
    if not tail.startswith(hcm_prefix):
        return None
    hcm_tail = tail.removeprefix(hcm_prefix).lstrip(".")
    if hcm_tail == "stat_prefix":
        return _yaml_detail(
            "HttpConnectionManager statistics-prefix string",
            "non-empty metrics namespace token; selected value is msconnector_ext_proc_ingress",
            _selected_template_default("HCM statistic prefix", "msconnector_ext_proc_ingress"),
            "Prefixes HCM metrics for the selected ingress listener.",
            "Metric names should not embed secrets, user identifiers, or unbounded request data.",
            "Observability only; it does not change P1–P4 payload visibility.",
            default_source=base_default_source,
        )
    if hcm_tail == "route_config":
        return _yaml_detail(
            "Envoy RouteConfiguration mapping",
            "inline route configuration with a name and virtual_hosts",
            _selected_template_default("inline route configuration", "msconnector_ext_proc_route"),
            "Defines the route lookup that selects the upstream after request-side filters run.",
            "Routes control upstream reachability; constrain domains and prefixes in a real deployment.",
            routing_phase,
            default_source=base_default_source,
        )
    if hcm_tail == "route_config.name":
        return _yaml_detail(
            "Envoy RouteConfiguration.name string",
            "non-empty local route-config name; selected value is msconnector_ext_proc_route",
            _selected_template_default("route-config name", "msconnector_ext_proc_route"),
            "Names the inline route configuration for Envoy diagnostics and references.",
            "The name is not an authorization boundary; do not encode secrets in it.",
            "Routing metadata only; request filtering still occurs in the preceding HTTP filter order.",
            default_source=base_default_source,
        )
    if hcm_tail == "route_config.virtual_hosts":
        return _yaml_detail(
            "repeated Envoy VirtualHost mapping",
            "one or more virtual-host mappings; the example has local_service",
            _selected_template_default("virtual-host list", "one local_service entry"),
            "Groups host/domain matches and routes for the HCM.",
            "Over-broad virtual hosts can route unexpected Host values to the upstream.",
            routing_phase,
            default_source=base_default_source,
        )
    if hcm_tail == "route_config.virtual_hosts[].name":
        return _yaml_detail(
            "Envoy VirtualHost.name string",
            "non-empty virtual-host name; selected value is local_service",
            _selected_template_default("virtual-host name", "local_service"),
            "Labels the virtual-host route group.",
            "Use opaque operational names rather than confidential data.",
            "Routing metadata only; it does not independently change ext_proc visibility.",
            default_source=base_default_source,
        )
    if hcm_tail in {"route_config.virtual_hosts[].domains", "route_config.virtual_hosts[].domains[]"}:
        item = hcm_tail.endswith("[]")
        return _yaml_detail(
            "repeated Envoy VirtualHost domain matcher" if not item else "Envoy VirtualHost domain-pattern string",
            "a list of Envoy domain patterns" if not item else "exact host, suffix/wildcard domain pattern, or *; selected item is *",
            _selected_template_default("virtual-host domain matcher", "the catch-all `*` pattern"),
            "Selects which Host/:authority values enter this virtual host's route list.",
            "The selected `*` catches all hosts; replace it with intended domains before exposure.",
            "Host matching precedes upstream routing after request-header P1 processing.",
            default_source=base_default_source,
        )
    if hcm_tail == "route_config.virtual_hosts[].routes":
        return _yaml_detail(
            "repeated Envoy Route mapping",
            "one or more match/action route mappings; the example has one prefix route",
            _selected_template_default("route list", "one `/` prefix route to upstream_service"),
            "Contains ordered route matching and upstream actions for the virtual host.",
            "Route order and match breadth determine where request traffic can be sent.",
            "The matched route is selected after P1; its upstream yields the response seen at P3/P4.",
            default_source=base_default_source,
        )
    if hcm_tail in {
        "route_config.virtual_hosts[].routes[].match",
        "route_config.virtual_hosts[].routes[].match.route",
        "route_config.virtual_hosts[].routes[].route",
    }:
        kind = "RouteMatch mapping" if hcm_tail.endswith("match") else "RouteAction mapping"
        purpose = (
            "Groups the prefix matcher for the selected route."
            if hcm_tail.endswith("match") else
            "Groups the cluster action selected after the route match."
        )
        return _yaml_detail(
            f"Envoy {kind}",
            "the child fields shown in this template",
            _selected_template_default(kind, "the explicit `/` prefix and upstream_service action"),
            purpose,
            "An over-broad match or unsafe route action can expose an unintended upstream.",
            routing_phase,
            default_source=base_default_source,
        )
    if hcm_tail == "route_config.virtual_hosts[].routes[].match.prefix":
        return _yaml_detail(
            "Envoy RouteMatch prefix string",
            "path-prefix matcher; selected value is /",
            _selected_template_default("route prefix", "the catch-all `/` prefix"),
            "Matches request paths for the selected route.",
            "The catch-all `/` reaches every path in the virtual host; narrow it when policy requires.",
            routing_phase,
            default_source=base_default_source,
        )
    if hcm_tail in {
        "route_config.virtual_hosts[].routes[].match.route.cluster",
        "route_config.virtual_hosts[].routes[].route.cluster",
    }:
        return _yaml_detail(
            "Envoy RouteAction cluster-name string",
            "name of a declared static_resources.clusters entry; selected value is upstream_service",
            _selected_template_default("route cluster target", "upstream_service"),
            "Routes matching downstream requests to the named upstream cluster.",
            "The target must be a reviewed local/upstream endpoint; an untrusted target creates an egress path.",
            routing_phase,
            default_source=base_default_source,
        )
    if hcm_tail == "http_filters":
        filter_pair = "ext_authz then router" if compatibility else "ext_proc then router"
        filter_lifecycle = (
            "The selected order enables compatibility P1 request authorization before the router; it does not create P2/P3/P4 coverage."
            if compatibility else
            "The selected order enables P1/P2/P3/P4 ext_proc callbacks before traffic is handed to the router."
        )
        return _yaml_detail(
            "ordered repeated Envoy HTTP filter mapping",
            f"HTTP filters with factory name and typed_config; selected order is {filter_pair}",
            _selected_template_default("HTTP-filter chain", f"{filter_pair} ordered pair"),
            f"Orders HTTP processing: {filter_pair.split(' then ')[0]} runs before the router forwards upstream.",
            f"Moving router ahead of {filter_pair.split(' then ')[0]} bypasses the selected inspection/authorization path.",
            filter_lifecycle,
            default_source=base_default_source,
        )
    http_prefix = "http_filters[]"
    if not hcm_tail.startswith(http_prefix):
        return None
    http_tail = hcm_tail.removeprefix(http_prefix).lstrip(".")
    if http_tail == "name":
        selected_filters = (
            "envoy.filters.http.ext_authz and envoy.filters.http.router"
            if compatibility else
            "envoy.filters.http.ext_proc and envoy.filters.http.router"
        )
        first_filter = "ext_authz" if compatibility else "ext_proc"
        lifecycle = (
            "ext_authz is compatibility request authorization; router forwards after it and no selected P2/P3/P4 path exists."
            if compatibility else
            "ext_proc exposes P1–P4; router terminates the filter chain and forwards to the upstream."
        )
        return _yaml_detail(
            "Envoy HTTP filter factory-name string",
            f"registered HTTP filter name; selected values are {selected_filters}",
            _selected_template_default("HTTP-filter factories", f"the {first_filter}/router ordered pair"),
            f"Selects the {first_filter} policy filter and terminal router implementations in the HCM chain.",
            f"Filter order is an enforcement boundary: {first_filter} must remain before router for the selected path.",
            lifecycle,
            default_source=base_default_source,
        )
    if http_tail == "typed_config":
        selected_type = "ExtAuthz" if compatibility else "ExternalProcessor"
        lifecycle = (
            "The ExtAuthz payload controls compatibility P1 request authorization; the Router payload forwards the allowed request."
            if compatibility else
            "The ExternalProcessor payload sets concrete P1–P4 visibility; the Router payload forwards the post-filter request."
        )
        return _yaml_detail(
            "repeated google.protobuf.Any HTTP-filter configuration mapping",
            f"Any payloads whose @type values select {selected_type} and Router",
            _selected_template_default("HTTP typed configurations", f"the explicit {selected_type} and Router payloads"),
            "Holds the per-filter configuration corresponding to each HTTP filter item.",
            "A mismatched Any payload/name pair can invalidate or bypass the intended inspection chain.",
            lifecycle,
            default_source=base_default_source,
        )
    if http_tail == "typed_config.@type":
        selected_type = "ExtAuthz" if compatibility else "ExternalProcessor"
        lifecycle = (
            "ExtAuthz performs compatibility P1 request authorization; Router is terminal forwarding and does not expose selected P2/P3/P4 callbacks."
            if compatibility else
            "ExternalProcessor chooses P1–P4 callbacks; Router supplies the terminal forwarding stage."
        )
        return _yaml_detail(
            "protobuf Any type URL string",
            f"{selected_type} and Router v3 type URLs in the same order as the HTTP filters",
            _selected_template_default("HTTP Any type URLs", f"the explicit {selected_type} and Router v3 URLs"),
            "Lets Envoy decode each HTTP filter's typed configuration.",
            "The type URL must match the neighboring filter factory; otherwise Envoy cannot apply the selected lifecycle policy.",
            lifecycle,
            default_source=base_default_source,
        )
    if http_tail == "typed_config.grpc_service":
        return _yaml_detail(
            "Envoy GrpcService mapping",
            "one gRPC service selector; selected form is envoy_grpc",
            _selected_template_default("ext_proc gRPC service", "the msconnector_ext_proc envoy_grpc target"),
            "Names the bidirectional gRPC side stream used by the ExternalProcessor filter.",
            "The processor endpoint must be trusted and private; it receives selected request/response metadata and body chunks.",
            "Transport for all selected ext_proc callbacks: P1, P2, P3, P4, and trailer/EOS notifications.",
            default_source=base_default_source,
        )
    if http_tail == "typed_config.grpc_service.envoy_grpc":
        return _yaml_detail(
            "EnvoyGrpc cluster-reference mapping",
            "cluster_name child naming a declared HTTP/2 cluster",
            _selected_template_default("Envoy gRPC target", "the msconnector_ext_proc cluster reference"),
            "Uses Envoy-managed gRPC transport rather than an inline URI for the external processor.",
            "The cluster reference must resolve to the reviewed ext_proc service, not an arbitrary remote endpoint.",
            "Carries the full selected P1–P4 external-processing stream.",
            default_source=base_default_source,
        )
    if http_tail == "typed_config.grpc_service.envoy_grpc.cluster_name":
        return _yaml_detail(
            "Envoy cluster-name string",
            "name of a declared HTTP/2-capable cluster; selected value is msconnector_ext_proc",
            _selected_template_default("ext_proc service cluster", "msconnector_ext_proc"),
            "Binds ExternalProcessor gRPC traffic to the local ext_proc cluster.",
            "Changing it can send inspected headers/bodies to another processor; retain a private trusted target.",
            "Transport target for P1 request headers, P2 request chunks, P3 response headers, P4 response chunks, and EOS trailers.",
            default_source=base_default_source,
        )
    if http_tail == "typed_config.grpc_service.timeout":
        return _yaml_detail(
            "Envoy protobuf Duration",
            "non-negative duration; selected value is 0.2s",
            _selected_template_default("gRPC service timeout", "0.2s"),
            "Bounds service establishment/operation as configured on the ext_proc gRPC service reference.",
            "A value that is too small creates avoidable processor failures; too large retains request resources longer.",
            "Applies to the ext_proc transport that serves selected P1–P4 callbacks.",
            default_source=base_default_source,
        )
    if http_tail == "typed_config.processing_mode":
        return _yaml_detail(
            "Envoy ext_proc ProcessingMode mapping",
            "header, body, and trailer send-mode child enums",
            "Envoy defaults send request/response headers, skip trailers, and send no bodies; this template overrides every selected lifecycle field.",
            "Groups the ext_proc visibility controls for request/response headers, bodies, and trailers.",
            "Omitting body modes loses body visibility; preserve explicit streaming modes for the selected full-lifecycle bridge.",
            "Controls P1 request headers, P2 request body, P3 response headers, P4 response body, and trailer/EOS delivery.",
            default_source="Envoy ext_proc v3 ProcessingMode API pinned by connectors/envoy/ext_proc/go.mod",
        )
    if http_tail in {
        "typed_config.processing_mode.request_body_mode",
        "typed_config.processing_mode.response_body_mode",
    }:
        direction = "request/P2" if "request_" in http_tail else "response/P4"
        return _yaml_detail(
            "Envoy ext_proc BodySendMode enum",
            "NONE | STREAMED | BUFFERED | BUFFERED_PARTIAL | FULL_DUPLEX_STREAMED | GRPC",
            "Envoy proto default NONE; the selected template explicitly sets STREAMED.",
            f"Selects {direction} body delivery to ext_proc; STREAMED sends incremental body chunks.",
            "Body delivery exposes payload data and consumes stream resources; the selected Common bridge requires STREAMED with bounded service controls.",
            f"{direction}: selected STREAMED makes the body available incrementally to the ext_proc bridge.",
            default_source="Envoy ext_proc v3 ProcessingMode.BodySendMode API pinned by connectors/envoy/ext_proc/go.mod",
        )
    if http_tail in {
        "typed_config.processing_mode.request_header_mode",
        "typed_config.processing_mode.response_header_mode",
    }:
        direction = "request/P1" if "request_" in http_tail else "response/P3"
        return _yaml_detail(
            "Envoy ext_proc HeaderSendMode enum",
            "DEFAULT | SEND | SKIP",
            "Envoy effective default SEND for request and response headers; the selected template explicitly sets SEND.",
            f"Selects whether {direction} headers are sent to the external processor.",
            "Headers can include security-sensitive metadata; use the private local ext_proc service and its configured bounds.",
            f"{direction}: selected SEND exposes the header callback to the bridge.",
            default_source="Envoy ext_proc v3 ProcessingMode.HeaderSendMode API pinned by connectors/envoy/ext_proc/go.mod",
        )
    if http_tail in {
        "typed_config.processing_mode.request_trailer_mode",
        "typed_config.processing_mode.response_trailer_mode",
    }:
        direction = "request" if "request_" in http_tail else "response"
        return _yaml_detail(
            "Envoy ext_proc HeaderSendMode enum for trailers",
            "DEFAULT | SEND | SKIP",
            "Envoy effective default SKIP for trailers; the selected template explicitly sets SEND.",
            f"Sends {direction} trailers/EOS metadata to the external processor when trailers are present.",
            "Trailer metadata is part of the transaction; do not treat it as a body-size bypass.",
            f"{direction} EOS/trailer visibility after the corresponding body stream; it complements P2/P4 streaming.",
            default_source="Envoy ext_proc v3 ProcessingMode.HeaderSendMode API pinned by connectors/envoy/ext_proc/go.mod",
        )
    if http_tail == "typed_config.request_attributes":
        return _yaml_detail(
            "repeated Envoy request-attribute name list",
            "supported Envoy request attribute names; selected list requests protocol, source/destination address, and source/destination port",
            "Absent list requests no additional attributes; this template explicitly requests five attributes used by processor.requestMetadataFromEnvoy.",
            "Requests concrete peer/protocol metadata for the ext_proc ProcessingRequest attributes map.",
            "Peer addresses and ports are operationally sensitive; the processor bounds and validates received metadata rather than deriving it from the gRPC peer.",
            "P1 request metadata only; it seeds the transaction before P2 body callbacks and before later response callbacks.",
            default_source="Envoy ext_proc v3 ExternalProcessor API and connectors/envoy/ext_proc/internal/processor/processor.go:requestMetadataFromEnvoy",
        )
    if http_tail == "typed_config.request_attributes[]":
        return _yaml_detail(
            "Envoy request-attribute path string",
            "request.protocol | source.address | source.port | destination.address | destination.port",
            "No additional attribute is requested when omitted; this template explicitly requests all five metadata paths consumed by requestMetadataFromEnvoy.",
            "Makes protocol and client/server endpoint metadata available to the ext_proc processor's request-metadata mapper.",
            "Do not add unbounded or sensitive attributes without reviewing processor handling and event logging.",
            "P1 request metadata visibility; the selected bridge uses it to construct transaction metadata before P2/P3/P4 callbacks.",
            default_source="selected template and connectors/envoy/ext_proc/internal/processor/processor.go:requestMetadataFromEnvoy",
        )
    if http_tail == "typed_config.send_body_without_waiting_for_header_response":
        return _yaml_detail(
            "Envoy ext_proc boolean",
            "true | false",
            "Envoy proto default false; the selected template explicitly sets false.",
            "When true with STREAMED bodies, Envoy sends body chunks before the processor's header response; false retains header-response ordering.",
            "Keeping false preserves the selected decision ordering and avoids uncontrolled early body delivery to the processor.",
            "Controls P1-to-P2/P3-to-P4 sequencing for STREAMED bodies; it does not itself enable body visibility.",
            default_source="Envoy ext_proc v3 ExternalProcessor API pinned by connectors/envoy/ext_proc/go.mod",
        )
    if http_tail == "typed_config.allow_mode_override":
        return _yaml_detail(
            "Envoy ext_proc boolean",
            "true | false",
            "Envoy proto default false; the selected template explicitly sets false.",
            "Allows or ignores a processor-supplied mode_override that would change processing_mode after request headers.",
            "false prevents the remote processor from widening/narrowing configured P1–P4 visibility at runtime.",
            "Guards the configured P1–P4 processing_mode contract; false keeps the static selected lifecycle surface.",
            default_source="Envoy ext_proc v3 ExternalProcessor API pinned by connectors/envoy/ext_proc/go.mod",
        )
    if http_tail == "typed_config.failure_mode_allow":
        return _yaml_detail(
            "Envoy ext_proc boolean",
            "true | false",
            "Envoy proto default false; the selected template explicitly sets false.",
            "Chooses whether processor stream errors/timeouts fail open (true) or produce Envoy's error handling (false).",
            "false avoids silently allowing traffic when the local processor cannot be reached; availability and denial behavior still need runtime evidence.",
            "Failure behavior for the ext_proc stream serving all selected P1–P4 callbacks.",
            default_source="Envoy ext_proc v3 ExternalProcessor API pinned by connectors/envoy/ext_proc/go.mod",
        )
    if http_tail == "typed_config.message_timeout":
        return _yaml_detail(
            "Envoy protobuf Duration per ext_proc message",
            "non-negative duration; selected value is 0.2s",
            "Envoy ext_proc default 200 milliseconds when omitted; the selected template explicitly sets 0.2s.",
            "Limits how long Envoy waits for each required external-processor response.",
            "Too large a timeout retains stream resources; too small a timeout creates processor failures governed by failure_mode_allow.",
            "Applies to per-message P1/P2/P3/P4 ext_proc exchanges except observability/full-duplex/gRPC cases documented by Envoy.",
            default_source="Envoy ext_proc v3 ExternalProcessor API pinned by connectors/envoy/ext_proc/go.mod",
        )
    if http_tail == "typed_config.max_message_timeout":
        return _yaml_detail(
            "Envoy protobuf Duration maximum override timeout",
            "non-negative duration; selected value is 0.25s",
            "Envoy default is 0, which disables the processor override_message_timeout API; the selected template permits overrides up to 0.25s.",
            "Caps a processor-requested extension of the per-message timeout.",
            "A finite cap limits remote processor influence over stream retention; setting a positive cap deliberately enables this API.",
            "Applies to timeout control for selected P1–P4 ext_proc exchanges; it does not change their visibility modes.",
            default_source="Envoy ext_proc v3 ExternalProcessor API pinned by connectors/envoy/ext_proc/go.mod",
        )
    if http_tail == "typed_config.http_service":
        return _yaml_detail(
            "Envoy ext_authz HTTP service mapping (compatibility only)",
            "one HTTP service; mutually exclusive with grpc_service",
            "No selected native ext_proc default; the compatibility template explicitly chooses HTTP service.",
            "Configures the compatibility ext_authz-style HTTP service instead of the selected gRPC ext_proc service.",
            "HTTP service is compatibility-only and cannot provide the selected body/trailer full-lifecycle path.",
            "Compatibility request authorization only; do not infer selected native P3/P4 coverage.",
            default_source="Envoy ext_proc v3 API and compatibility template",
        )
    if http_tail == "typed_config.http_service.server_uri":
        return _yaml_detail(
            "Envoy HttpService.server_uri mapping (compatibility only)",
            "URI, cluster, and timeout child fields",
            "No selected native default; compatibility template supplies a local authorization endpoint.",
            "Groups the compatibility service URI, logical cluster, and deadline.",
            "Keep the authorization service private and do not embed credentials in a URI.",
            "Compatibility request authorization only; no selected full response lifecycle.",
            default_source="compatibility template",
        )
    if http_tail == "typed_config.http_service.server_uri.uri":
        return _yaml_detail(
            "Envoy HTTP service URI string (compatibility only)",
            "absolute HTTP/HTTPS URI; selected value is http://127.0.0.1:9000",
            "No selected native default; compatibility template explicitly supplies the local URI.",
            "Identifies the HTTP authorization endpoint for compatibility ext_authz requests.",
            "Loopback limits the example exposure; a remote URI needs TLS, identity, and egress review.",
            "Compatibility request authorization only; no native response-body P4 visibility.",
            default_source="compatibility template",
        )
    if http_tail == "typed_config.http_service.server_uri.cluster":
        return _yaml_detail(
            "Envoy cluster-name string (compatibility only)",
            "name of a declared compatibility cluster; selected value is modsecurity_authz",
            "No selected native default; compatibility template explicitly supplies modsecurity_authz.",
            "Associates the HTTP authorization URI with its configured Envoy cluster.",
            "The name must resolve to a reviewed service cluster; do not treat it as the native ext_proc target.",
            "Compatibility request authorization only; no selected P3/P4 coverage.",
            default_source="compatibility template",
        )
    if http_tail == "typed_config.http_service.server_uri.timeout":
        return _yaml_detail(
            "Envoy protobuf Duration (compatibility HTTP authorization timeout)",
            "non-negative duration; selected value is 0.2s",
            "No repository default; compatibility template explicitly sets 0.2s.",
            "Bounds one compatibility authorization HTTP request.",
            "Deadline choice changes failure pressure; it is not an ext_proc full-lifecycle timeout guarantee.",
            "Compatibility request authorization only; no P3/P4 response inspection.",
            default_source="compatibility template",
        )
    if http_tail == "typed_config.http_service.authorization_request":
        return _yaml_detail(
            "Envoy ext_authz AuthorizationRequest mapping (compatibility only)",
            "allowed_headers child mapping shown in the compatibility template",
            "No selected native default; the compatibility template supplies an explicit request-header policy.",
            "Groups the header-forwarding policy for the compatibility authorization request.",
            "Only forward the headers the compatibility service needs; extra headers may disclose credentials or user data.",
            "Compatibility P1 request-header authorization only; no selected body or response visibility.",
            default_source="compatibility template",
        )
    if http_tail in {
        "typed_config.http_service.authorization_request.allowed_headers",
        "typed_config.http_service.authorization_request.allowed_headers.patterns",
    }:
        return _yaml_detail(
            "Envoy HeaderMatcher list mapping (compatibility only)",
            "one or more header matcher patterns; selected policy has exact authorization and content-type",
            "No selected native default; compatibility template explicitly enumerates forwarded headers.",
            "Groups the allow-list of request headers forwarded to the compatibility authorization service.",
            "Header forwarding can expose credentials; keep the matcher list minimal and audit changes.",
            "Compatibility P1 request-header authorization only; no native P2/P3/P4 visibility.",
            default_source="compatibility template",
        )
    if http_tail == "typed_config.http_service.authorization_request.allowed_headers.patterns[].exact":
        return _yaml_detail(
            "Envoy HeaderMatcher exact header-name string (compatibility only)",
            "lower-case/HTTP header name exact matcher; selected values are authorization and content-type",
            "No selected native default; compatibility template explicitly allow-lists two headers.",
            "Forwards only matching request headers to the compatibility authorization service.",
            "The authorization value is sensitive; ensure the compatibility service and its logs are trusted.",
            "Compatibility P1 request-header authorization only; no selected P2/P3/P4 visibility.",
            default_source="compatibility template",
        )
    return None


def _envoy_cluster_yaml_detail(path: str, compatibility: bool = False) -> dict[str, str] | None:
    """Describe endpoint and transport fields under static_resources.clusters[]."""
    prefix = "static_resources.clusters[]"
    tail = path.removeprefix(prefix).lstrip(".")
    source = "selected Envoy v3 template; connector owns no bootstrap default"
    lifecycle = (
        "The compatibility cluster list contains modsecurity_authz for request authorization and app_backend for the allowed upstream flow; "
        "it does not establish selected native P2/P3/P4 coverage."
        if compatibility else
        "The selected cluster list contains upstream_service, which receives the post-request-filter flow and returns the response seen at P3/P4, "
        "and msconnector_ext_proc, which transports selected P1/P2/P3/P4 callbacks."
    )
    if tail == "name":
        return _yaml_detail(
            "Envoy Cluster.name string",
            "unique non-empty cluster name; selected values are upstream_service and msconnector_ext_proc",
            _selected_template_default("cluster-name", "the two named static clusters"),
            "Names a static endpoint group referenced by the route or ext_proc gRPC service.",
            "Cluster names resolve traffic destinations; do not redirect an inspection target to an unreviewed service.",
            "upstream_service supplies the normal request/response flow; msconnector_ext_proc carries P1–P4 processor traffic.",
            default_source=source,
        )
    if tail == "connect_timeout":
        return _yaml_detail(
            "Envoy protobuf Duration for cluster connection attempts",
            "non-negative duration; selected native value is 0.5s (compatibility example uses 0.25s)",
            _selected_template_default("cluster connect timeout", "the explicit template duration"),
            "Bounds TCP connection establishment to the upstream or local processor endpoint.",
            "A long timeout retains connections; a short timeout can trigger processor failures or upstream unavailability.",
            lifecycle,
            default_source=source,
        )
    if tail == "type":
        return _yaml_detail(
            "Envoy Cluster DiscoveryType enum",
            "Envoy discovery type; selected native value STATIC, compatibility values STRICT_DNS",
            _selected_template_default("cluster discovery type", "STATIC for the selected native local endpoints"),
            "Determines how Envoy resolves the endpoint set for the named cluster.",
            "STATIC keeps the selected endpoints explicit; DNS discovery changes endpoint resolution and should be reviewed for egress/identity impact.",
            lifecycle,
            default_source=source,
        )
    if tail == "http2_protocol_options":
        return _yaml_detail(
            "Envoy Http2ProtocolOptions mapping",
            "empty or configured HTTP/2 options; selected value is {} on the ext_proc cluster",
            "Absent unless configured; the selected ext_proc cluster explicitly sets an empty HTTP/2 options mapping.",
            "Enables the HTTP/2 protocol options needed by the Envoy gRPC ext_proc cluster.",
            "Do not remove HTTP/2 support from the selected gRPC processor cluster.",
            "Transport prerequisite for the ext_proc bidirectional stream carrying P1–P4 callbacks.",
            default_source=source,
        )
    if tail == "load_assignment":
        return _yaml_detail(
            "Envoy ClusterLoadAssignment mapping",
            "cluster_name plus endpoint/lb_endpoints children",
            _selected_template_default("static load assignment", "the explicit loopback endpoint set"),
            "Groups the endpoints assigned to a static cluster.",
            "Endpoint assignments are egress/control-plane inputs; review every address and port.",
            lifecycle,
            default_source=source,
        )
    if tail == "load_assignment.cluster_name":
        return _yaml_detail(
            "Envoy ClusterLoadAssignment.cluster_name string",
            "must match the enclosing Cluster.name; selected values match upstream_service or msconnector_ext_proc",
            _selected_template_default("load-assignment cluster name", "the enclosing static cluster name"),
            "Associates the endpoint assignment with its enclosing cluster.",
            "A mismatch invalidates or misroutes the endpoint configuration.",
            lifecycle,
            default_source=source,
        )
    if tail == "load_assignment.endpoints":
        return _yaml_detail(
            "repeated Envoy LocalityLbEndpoints mapping",
            "one or more locality endpoint groups; the example has one group",
            _selected_template_default("endpoint-group list", "one loopback locality group"),
            "Groups load-balanced endpoints for the static cluster.",
            "Each endpoint is a traffic destination; preserve the intended private scope.",
            lifecycle,
            default_source=source,
        )
    if tail == "load_assignment.endpoints[].lb_endpoints":
        return _yaml_detail(
            "repeated Envoy LbEndpoint mapping",
            "one or more endpoint mappings; the example has one endpoint per cluster",
            _selected_template_default("load-balancer endpoint list", "one explicit loopback endpoint"),
            "Defines endpoint candidates selected by Envoy's cluster load balancer.",
            "An added endpoint receives copied requests or ext_proc messages; require explicit trust review.",
            lifecycle,
            default_source=source,
        )
    if tail == "load_assignment.endpoints[].lb_endpoints[].endpoint":
        return _yaml_detail(
            "Envoy Endpoint mapping",
            "endpoint address child mapping",
            _selected_template_default("endpoint object", "the explicit loopback socket address"),
            "Contains the network address of one cluster endpoint.",
            "The endpoint is a concrete traffic target and must be constrained to the intended service.",
            lifecycle,
            default_source=source,
        )
    endpoint_prefix = "load_assignment.endpoints[].lb_endpoints[].endpoint.address"
    if tail == endpoint_prefix:
        return _yaml_detail(
            "Envoy core.Address mapping",
            "one supported Envoy address form; selected form is socket_address",
            _selected_template_default("cluster endpoint address", "a loopback socket_address mapping"),
            "Contains the TCP address for one upstream or ext_proc service endpoint.",
            "Changing it changes egress or inspection-service reachability.",
            lifecycle,
            default_source=source,
        )
    if tail == f"{endpoint_prefix}.socket_address":
        return _yaml_detail(
            "Envoy core.SocketAddress mapping",
            "address and port_value child fields",
            _selected_template_default("cluster endpoint socket-address", "127.0.0.1 plus its materialized port"),
            "Pairs the static cluster endpoint host and TCP port.",
            "The selected loopback values keep both upstream and processor endpoint examples local.",
            lifecycle,
            default_source=source,
        )
    if tail == f"{endpoint_prefix}.socket_address.address":
        return _yaml_detail(
            "Envoy SocketAddress host/IP string",
            "valid endpoint host or IP literal; selected value is 127.0.0.1",
            _selected_template_default("cluster endpoint host", "127.0.0.1"),
            "Targets the static upstream or ext_proc endpoint host.",
            "Loopback avoids external egress in the example; a remote host needs transport and trust controls.",
            lifecycle,
            default_source=source,
        )
    if tail == f"{endpoint_prefix}.socket_address.port_value":
        return _yaml_detail(
            "Envoy SocketAddress uint32 TCP port",
            "materializer-validated decimal port 1..65535",
            _selected_template_default("cluster endpoint port", "the @UPSTREAM_PORT@ or @EXT_PROC_PORT@ materializer input"),
            "Targets the TCP port of the selected upstream or ext_proc endpoint.",
            "Port changes can send traffic to a different local service; retain explicit private service ownership.",
            lifecycle,
            default_source="selected template and prepare_envoy_ext_proc_config.sh materializer",
        )
    return None


def _envoy_admin_yaml_detail(path: str) -> dict[str, str] | None:
    """Describe management-plane fields separately from the HTTP data path."""
    tail = path.removeprefix("admin").lstrip(".")
    source = "selected Envoy v3 template; connector owns no bootstrap default"
    if tail == "access_log_path":
        return _yaml_detail(
            "filesystem path string",
            "writable path accepted by Envoy; selected value is /dev/null",
            _selected_template_default("admin access-log path", "/dev/null"),
            "Selects where Envoy writes administrative HTTP access records.",
            "Administrative logs can contain operational metadata; /dev/null suppresses them in this example rather than providing an audit design.",
            "Management-plane only; it does not alter P1–P4 ext_proc visibility.",
            default_source=source,
        )
    if tail == "address":
        return _yaml_detail(
            "Envoy admin core.Address mapping",
            "one supported address form; selected form is a loopback socket_address",
            _selected_template_default("admin address", "127.0.0.1 and @ADMIN_PORT@"),
            "Groups the Envoy administration listener address.",
            "Admin endpoints are sensitive; keep the selected listener loopback/private.",
            "Management-plane only; independent of P1–P4 transaction processing.",
            default_source=source,
        )
    if tail == "address.socket_address":
        return _yaml_detail(
            "Envoy admin SocketAddress mapping",
            "address and port_value child fields",
            _selected_template_default("admin socket-address", "127.0.0.1 plus @ADMIN_PORT@"),
            "Pairs the Envoy administration host and TCP port.",
            "Do not bind the administration socket publicly without a separate access-control design.",
            "Management-plane only; independent of P1–P4 transaction processing.",
            default_source=source,
        )
    if tail == "address.socket_address.address":
        return _yaml_detail(
            "Envoy admin host/IP string",
            "valid host or IP literal; selected value is 127.0.0.1",
            _selected_template_default("admin host", "127.0.0.1"),
            "Binds the Envoy administration listener to the selected interface.",
            "Loopback prevents the example admin interface from being reachable remotely.",
            "Management-plane only; independent of P1–P4 transaction processing.",
            default_source=source,
        )
    if tail == "address.socket_address.port_value":
        return _yaml_detail(
            "Envoy admin uint32 TCP port",
            "materializer-validated decimal port 1..65535",
            _selected_template_default("admin port", "the @ADMIN_PORT@ materializer input"),
            "Selects the local TCP port for Envoy administration endpoints.",
            "Use a private, non-conflicting port; exposing admin APIs is unrelated to ModSecurity enforcement.",
            "Management-plane only; independent of P1–P4 transaction processing.",
            default_source="selected template and prepare_envoy_ext_proc_config.sh materializer",
        )
    return None


def _envoy_yaml_detail(path: str, example_value: str) -> dict[str, str] | None:
    """Return non-generic metadata for every Envoy example YAML path."""
    compatibility = path.startswith("compatibility.")
    selected_path = _without_compatibility_prefix(path)
    source = "selected Envoy v3 template; connector owns no bootstrap default"
    if selected_path == "static_resources":
        return _yaml_detail(
            "Envoy Bootstrap static_resources mapping",
            "listener and cluster child mappings shown in the template",
            _selected_template_default("static-resource set", "the explicit listener and static clusters"),
            "Declares the complete static data-plane topology used by the checked-in example.",
            "All listener and cluster children affect traffic exposure or destination; review as one topology.",
            "Bootstrap establishes the selected ext_proc P1–P4 path but does not itself process a transaction.",
            default_source=source,
        )
    if selected_path == "static_resources.listeners":
        return _yaml_detail(
            "repeated Envoy Listener mapping",
            "one or more Listener objects; selected template declares one loopback HTTP listener",
            _selected_template_default("listener list", "one msconnector_ext_proc_listener"),
            "Declares the downstream listener objects present in the static bootstrap.",
            "A listener changes the network attack surface before request policy is reached.",
            "Bootstrap container for the filter chain that exposes selected P1–P4 ext_proc callbacks.",
            default_source=source,
        )
    if selected_path == "static_resources.clusters":
        return _yaml_detail(
            "repeated Envoy Cluster mapping",
            "one or more Cluster objects; selected template declares upstream_service and msconnector_ext_proc",
            _selected_template_default("cluster list", "the explicit upstream and local processor clusters"),
            "Declares the static service destinations used by routing and ext_proc gRPC.",
            "Clusters define where application traffic and inspection data can leave the listener.",
            "upstream_service provides the request/response path; msconnector_ext_proc transports selected P1–P4 callbacks.",
            default_source=source,
        )
    if selected_path == "admin":
        return _yaml_detail(
            "Envoy Admin mapping",
            "access_log_path and address child fields",
            _selected_template_default("admin configuration", "a loopback listener with /dev/null access log"),
            "Groups Envoy management-interface configuration.",
            "Admin exposure is a separate privileged surface and must remain private in the example.",
            "Management plane only; it does not create or alter P1–P4 callbacks.",
            default_source=source,
        )
    if selected_path.startswith("static_resources.listeners[]"):
        return _envoy_listener_yaml_detail(selected_path, example_value, compatibility)
    if selected_path.startswith("static_resources.clusters[]"):
        return _envoy_cluster_yaml_detail(selected_path, compatibility)
    if selected_path.startswith("admin"):
        return _envoy_admin_yaml_detail(selected_path)
    return None


def _traefik_yaml_detail(path: str, example_value: str) -> dict[str, str] | None:
    """Return exact metadata for static, native dynamic, and forwardAuth YAML.

    The local plugin's own seven configuration leaves are documented from
    ``CreateConfig``/``normalizedConfig`` by ``_traefik_plugin_option``.  This
    function covers the surrounding Traefik host topology so those fields do
    not accidentally inherit generic YAML wording.
    """
    compatibility = path.startswith("compatibility.")
    selected_path = _without_compatibility_prefix(path)
    host_source = "selected Traefik example; no connector-owned Traefik host default"
    native_lifecycle = (
        "The native middleware is attached to the router; its source-defined streaming callbacks cover P1/P2/P3/P4 when the UDS engine path is running. "
        "Configuration alone is not runtime evidence."
    )
    compatibility_lifecycle = (
        "Compatibility forwardAuth runs before upstream handling for request authorization; it has no selected P3/P4 response-header/body visibility."
    )
    lifecycle = compatibility_lifecycle if compatibility else native_lifecycle
    if selected_path == "experimental":
        return _yaml_detail(
            "Traefik static experimental configuration mapping",
            "localPlugins child mapping shown in the selected native static file",
            _selected_template_default("experimental configuration", "the modsecurityNative local-plugin declaration"),
            "Groups static experimental features needed to make the repository-owned local plugin discoverable.",
            "Local plugin loading executes selected repository code; pin and review the module source before use.",
            "Static bootstrap prerequisite for the native P1–P4 middleware path; it does not process traffic itself.",
            default_source=host_source,
        )
    if selected_path == "experimental.localPlugins":
        return _yaml_detail(
            "Traefik static local-plugin registry mapping",
            "named local plugin declarations; selected key is modsecurityNative",
            _selected_template_default("local-plugin registry", "one modsecurityNative declaration"),
            "Registers the local plugin name that dynamic middleware configuration later references.",
            "A registry entry selects executable plugin source; do not add unreviewed local modules.",
            "Static bootstrap prerequisite for the native router middleware and its P1–P4 callback surface.",
            default_source=host_source,
        )
    if selected_path == "experimental.localPlugins.modsecurityNative":
        return _yaml_detail(
            "Traefik local-plugin declaration mapping",
            "moduleName and settings child fields",
            _selected_template_default("modsecurityNative declaration", "the repository module and empty environment settings"),
            "Binds the dynamic plugin name modsecurityNative to its local module configuration.",
            "The declaration controls which local code Traefik loads; protect its configuration and source tree.",
            "Static prerequisite for attaching the native middleware; no transaction lifecycle event occurs at declaration time.",
            default_source=host_source,
        )
    if selected_path == "experimental.localPlugins.modsecurityNative.moduleName":
        return _yaml_detail(
            "Traefik local-plugin Go module path string",
            "module path resolving to the repository native_middleware package",
            _selected_template_default("local-plugin module path", "github.com/Easton97-Jens/ModSecurity-conector/connectors/traefik/native_middleware"),
            "Selects the Go module/package Traefik loads for the modsecurityNative local plugin.",
            "This is code-selection input; use a reviewed, pinned source path and do not substitute an arbitrary module.",
            "Static prerequisite for the native middleware's P1–P4 callback implementation.",
            default_source=host_source,
        )
    if selected_path == "experimental.localPlugins.modsecurityNative.settings":
        return _yaml_detail(
            "Traefik local-plugin settings mapping",
            "settings.envs child list; selected mapping contains an empty list",
            _selected_template_default("local-plugin settings", "an empty envs list"),
            "Groups host-level settings for the selected local-plugin declaration.",
            "Avoid placing credentials or production-specific secrets in plugin settings.",
            "Static bootstrap only; the selected native request lifecycle starts when a router invokes the plugin.",
            default_source=host_source,
        )
    if selected_path == "experimental.localPlugins.modsecurityNative.settings.envs":
        return _yaml_detail(
            "Traefik local-plugin environment-settings list",
            "list of Traefik local-plugin environment setting strings; selected list is empty",
            "Selected value is []; no example-provided plugin environment setting is added.",
            "Leaves the local-plugin declaration without example-provided environment inputs.",
            "An environment setting can carry secrets or change behavior; keep the selected empty list unless an explicit documented input is required.",
            "Static bootstrap only; it does not change P1–P4 visibility by itself.",
            default_source=host_source,
        )
    if selected_path == "entryPoints":
        return _yaml_detail(
            "Traefik static entry-point mapping",
            "named entry-point mappings; selected key is web",
            _selected_template_default("entry-point registry", "the web listener"),
            "Groups named listener definitions used by dynamic routers.",
            "Entry-point addresses define the pre-policy network exposure of Traefik.",
            "Static listener bootstrap; its named entry point selects which requests can reach the router/middleware lifecycle.",
            default_source=host_source,
        )
    if selected_path == "entryPoints.web":
        return _yaml_detail(
            "Traefik EntryPoint mapping",
            "address child field; selected entry point is web",
            _selected_template_default("web entry point", "the :8080 listener"),
            "Defines the named web listener that dynamic routers attach to.",
            "Changing this listener changes client reachability before middleware enforcement.",
            "Static entry point for the router; the native middleware begins after request routing selects it.",
            default_source=host_source,
        )
    if selected_path == "entryPoints.web.address":
        return _yaml_detail(
            "Traefik listener address string",
            "Traefik entry-point address such as host:port or :port; selected value is :8080",
            _selected_template_default("web listener address", ":8080"),
            "Binds the named web entry point used by the example router.",
            "The selected :8080 form changes listener exposure according to host networking; use a private bind or explicit edge control as appropriate.",
            "Listener bootstrap before router selection and the attached native P1–P4 middleware path.",
            default_source=host_source,
        )
    if selected_path == "providers":
        return _yaml_detail(
            "Traefik static provider registry mapping",
            "file provider child mapping",
            _selected_template_default("provider registry", "the adjacent dynamic File Provider"),
            "Groups configuration providers that supply dynamic routers, middlewares, and services.",
            "A provider controls live routing configuration; protect its source file and directory.",
            "Static-to-dynamic handoff; it makes the router/middleware lifecycle available but does not process a transaction itself.",
            default_source=host_source,
        )
    if selected_path == "providers.file":
        return _yaml_detail(
            "Traefik File Provider mapping",
            "filename and watch child fields",
            _selected_template_default("file provider", "the adjacent traefik-dynamic.yaml file"),
            "Configures the on-disk dynamic configuration provider.",
            "The dynamic file can alter routes and middleware; grant write access only to trusted operators.",
            "Loads the router/middleware configuration that exposes the native lifecycle path or compatibility request path.",
            default_source=host_source,
        )
    if selected_path == "providers.file.filename":
        return _yaml_detail(
            "Traefik File Provider path string",
            "readable dynamic-configuration path; selected relative path is ./traefik-dynamic.yaml",
            _selected_template_default("dynamic file path", "./traefik-dynamic.yaml"),
            "Selects the companion dynamic file containing routers, middleware, and upstream service definitions.",
            "A relative path resolves from the host configuration context; deploy the matching file together and protect it from untrusted writes.",
            "Supplies the routing configuration that attaches native P1–P4 middleware or compatibility P1 authorization.",
            default_source=host_source,
        )
    if selected_path == "providers.file.watch":
        selected = "true" if example_value == "true" else "false"
        return _yaml_detail(
            "Traefik File Provider boolean",
            "true | false",
            _selected_template_default("File Provider watch behavior", selected),
            "Controls whether Traefik watches the dynamic file for reloads after initial load.",
            "watch=true makes future file writes live configuration changes; selected native file uses false, compatibility example uses true.",
            "Dynamic lifecycle configuration reload control; it does not itself change per-request P1–P4 visibility.",
            default_source=host_source,
        )
    if selected_path == "log":
        return _yaml_detail(
            "Traefik log configuration mapping",
            "level child field",
            _selected_template_default("log configuration", "level INFO"),
            "Groups Traefik process-log settings.",
            "Logs can contain request and operational metadata; choose retention and access controls separately.",
            "Host observability only; no direct P1–P4 payload visibility change.",
            default_source=host_source,
        )
    if selected_path == "log.level":
        return _yaml_detail(
            "Traefik log-level token",
            "Traefik-supported level token; selected value is INFO",
            _selected_template_default("log level", "INFO"),
            "Controls Traefik process-log verbosity.",
            "Debug logging can expose more operational metadata; do not equate host logs with ModSecurity audit output.",
            "Host observability only; it does not change native or compatibility lifecycle callbacks.",
            default_source=host_source,
        )
    if selected_path == "accessLog":
        return _yaml_detail(
            "Traefik access-log configuration mapping",
            "empty mapping or documented access-log fields; selected value is {}",
            _selected_template_default("access-log configuration", "an empty configuration mapping"),
            "Enables/configures the Traefik access-log surface in the selected static example.",
            "Access logs can contain request metadata; configure safe storage, rotation, and privacy controls for deployment.",
            "Host observability only; it does not substitute for transaction P1–P4 processing or engine audit logging.",
            default_source=host_source,
        )
    if selected_path == "http":
        return _yaml_detail(
            "Traefik dynamic HTTP configuration mapping",
            "routers, middlewares, and services child mappings",
            _selected_template_default("dynamic HTTP topology", "one app router, one middleware, and one app service"),
            "Groups the request router, middleware attachment, and upstream service used by the example.",
            "This topology controls which requests reach the engine and which upstream receives them; protect dynamic configuration writes.",
            lifecycle,
            default_source=host_source,
        )
    if selected_path == "http.routers":
        return _yaml_detail(
            "Traefik dynamic router registry mapping",
            "named router mappings; selected key is app",
            _selected_template_default("router registry", "one app router"),
            "Groups dynamic request-routing definitions.",
            "Router rules and middleware order are enforcement-relevant; avoid unaudited route additions.",
            lifecycle,
            default_source=host_source,
        )
    if selected_path == "http.routers.app":
        return _yaml_detail(
            "Traefik dynamic Router mapping",
            "rule, entryPoints, middlewares, and service child fields",
            _selected_template_default("app router", "the explicit catch-all app route"),
            "Binds a request rule and entry point to the listed middleware and app service.",
            "The router is the attachment point for the native UDS middleware or compatibility forwardAuth; removing it bypasses that path.",
            lifecycle,
            default_source=host_source,
        )
    if selected_path == "http.routers.app.rule":
        return _yaml_detail(
            "Traefik router-rule expression string",
            "Traefik rule DSL; selected value is PathPrefix(`/`)",
            _selected_template_default("app router rule", "the catch-all PathPrefix(`/`) expression"),
            "Matches incoming requests to the app router.",
            "The selected catch-all rule routes every path on the entry point; narrow it in a real deployment if required.",
            "Selects requests that enter the attached native middleware P1/P2 path or compatibility P1 authorization path.",
            default_source=host_source,
        )
    if selected_path in {"http.routers.app.entryPoints", "http.routers.app.entryPoints[]"}:
        item = selected_path.endswith("[]")
        return _yaml_detail(
            "Traefik router entry-point name list" if not item else "Traefik entry-point name string",
            "defined static entry-point names" if not item else "name declared under static entryPoints; selected value is web",
            _selected_template_default("router entry-point binding", "the web entry point"),
            "Restricts the app router to the named static listener.",
            "Binding a router to a public entry point exposes its middleware/service path to that listener's clients.",
            "Selects which listener traffic can reach the attached native P1–P4 middleware or compatibility request path.",
            default_source=host_source,
        )
    if selected_path in {"http.routers.app.middlewares", "http.routers.app.middlewares[]"}:
        item = selected_path.endswith("[]")
        mode = "compatibility forwardAuth" if compatibility else "native UDS"
        return _yaml_detail(
            "ordered Traefik middleware-name list" if not item else "Traefik middleware-name string",
            "names declared under http.middlewares" if not item else f"selected {mode} middleware name",
            _selected_template_default("router middleware list", f"the selected {mode} middleware"),
            "Attaches middleware to the router in listed order before forwarding to the app service.",
            "Removing/reordering this reference can bypass inspection or authorization; retain the reviewed middleware before the service.",
            lifecycle,
            default_source=host_source,
        )
    if selected_path == "http.routers.app.service":
        return _yaml_detail(
            "Traefik service-name string",
            "name declared under http.services; selected value is app",
            _selected_template_default("router service target", "the app service"),
            "Selects the upstream service after router middleware completes.",
            "The target service URL is an egress destination; review it separately from middleware selection.",
            "Forwarding occurs after request-side middleware; the native path can observe the returned response at P3/P4.",
            default_source=host_source,
        )
    if selected_path == "http.middlewares":
        middleware_key = "modsecurity-auth" if compatibility else "modsecurity-native-streaming"
        return _yaml_detail(
            "Traefik dynamic middleware registry mapping",
            f"named middleware mappings; selected key is {middleware_key}",
            _selected_template_default("middleware registry", "the selected native or compatibility middleware"),
            "Groups middleware definitions referenced by routers.",
            "Middleware definitions are policy attachment points; unreviewed changes can remove or replace inspection.",
            lifecycle,
            default_source=host_source,
        )
    if re.fullmatch(r"http\.middlewares\.[^.]+", selected_path):
        mode = "forwardAuth compatibility" if compatibility else "native modsecurity"
        return _yaml_detail(
            "Traefik named middleware mapping",
            f"one {mode} middleware configuration mapping",
            _selected_template_default("named middleware", f"the selected {mode} mapping"),
            "Binds the router-visible middleware name to its plugin or forwardAuth configuration.",
            "The router reference must continue to point to this reviewed middleware name to avoid bypass.",
            lifecycle,
            default_source=host_source,
        )
    middleware_prefix = "http.middlewares."
    if selected_path.startswith(middleware_prefix):
        tail = selected_path.rsplit(".", 1)[-1]
        if tail == "plugin":
            return _yaml_detail(
                "Traefik plugin middleware mapping",
                "named local-plugin child mapping; selected child is modsecurityNative",
                _selected_template_default("plugin middleware mapping", "the modsecurityNative local plugin"),
                "Selects the local-plugin configuration for the named native middleware.",
                "The plugin reference chooses code that processes requests and responses; preserve the reviewed local plugin name.",
                native_lifecycle,
                default_source=host_source,
            )
        if tail == "modsecurityNative":
            return _yaml_detail(
                "Traefik local-plugin configuration mapping",
                "the seven native middleware Config fields documented from CreateConfig/normalizedConfig",
                "Plugin CreateConfig supplies bounded defaults; this template explicitly sets all seven selected fields.",
                "Groups limits, transaction ID, and engine connection fields passed to the repository native middleware.",
                "The UDS fields and bounds are enforcement-relevant; passthrough is not rule evaluation.",
                native_lifecycle,
                default_source="connectors/traefik/native_middleware/middleware.go:CreateConfig/normalizedConfig",
            )
        if tail == "forwardAuth":
            return _yaml_detail(
                "Traefik ForwardAuth middleware mapping (compatibility only)",
                "address and trustForwardHeader child fields",
                "No selected native default; compatibility template explicitly configures a local forwardAuth service.",
                "Groups the request-only external authorization service settings.",
                "Do not present forwardAuth as the native UDS rule-evaluating path; its service receives request authorization data.",
                compatibility_lifecycle,
                default_source="compatibility template and docs/connectors/traefik.md",
            )
        if tail == "address" and ".forwardAuth." in selected_path:
            return _yaml_detail(
                "Traefik ForwardAuth HTTP URL string (compatibility only)",
                "absolute HTTP/HTTPS authorization-service URL; selected value is http://127.0.0.1:9000/authorize",
                "No selected native default; compatibility template explicitly supplies the loopback authorization URL.",
                "Targets the external forwardAuth decision service before the app service is contacted.",
                "Use a trusted, private service and do not embed credentials in the URL; it is distinct from the native UDS engine.",
                compatibility_lifecycle,
                default_source="compatibility template",
            )
        if tail == "trustForwardHeader":
            return _yaml_detail(
                "Traefik ForwardAuth boolean (compatibility only)",
                "true | false",
                "No selected native default; compatibility template explicitly sets false.",
                "Controls whether forwarded request headers are trusted when calling the compatibility authorization service.",
                "false avoids trusting client-supplied forwarded identity/route headers by default; deploy explicit proxy trust boundaries if changing it.",
                compatibility_lifecycle,
                default_source="compatibility template",
            )
    if selected_path == "http.services":
        return _yaml_detail(
            "Traefik dynamic service registry mapping",
            "named service mappings; selected key is app",
            _selected_template_default("service registry", "the app load-balancer service"),
            "Groups upstream service definitions referenced by routers.",
            "Services define request destinations after middleware; review their endpoint URLs and credentials.",
            "The native middleware can receive the app response at P3/P4 after this service returns it; compatibility forwardAuth cannot.",
            default_source=host_source,
        )
    if selected_path == "http.services.app":
        return _yaml_detail(
            "Traefik named service mapping",
            "loadBalancer child mapping",
            _selected_template_default("app service", "one load-balancer with a loopback server"),
            "Binds the router's app service name to its load balancer.",
            "This mapping is an upstream routing target; do not confuse it with the ModSecurity engine service.",
            "Upstream service stage after request middleware; native response callbacks can observe returned headers/body at P3/P4.",
            default_source=host_source,
        )
    if selected_path == "http.services.app.loadBalancer":
        return _yaml_detail(
            "Traefik LoadBalancer service mapping",
            "servers child list",
            _selected_template_default("app load balancer", "one loopback app server"),
            "Groups the upstream server endpoints for the app service.",
            "Each server URL is a traffic destination; limit it to the intended upstream.",
            "After request middleware, the selected server response is available to native P3/P4 callbacks; not to compatibility forwardAuth.",
            default_source=host_source,
        )
    if selected_path == "http.services.app.loadBalancer.servers":
        return _yaml_detail(
            "repeated Traefik load-balancer server mapping",
            "one or more server URL mappings; selected example has one server",
            _selected_template_default("app server list", "one http://127.0.0.1:8081 endpoint"),
            "Defines the endpoint candidates for the app load balancer.",
            "Adding a server adds an upstream destination; review network scope and transport security.",
            "Native response lifecycle P3/P4 begins only after the selected server responds; compatibility forwardAuth remains request-only.",
            default_source=host_source,
        )
    if selected_path == "http.services.app.loadBalancer.servers[].url":
        return _yaml_detail(
            "Traefik upstream server URL string",
            "absolute backend URL; selected value is http://127.0.0.1:8081",
            _selected_template_default("app server URL", "http://127.0.0.1:8081"),
            "Targets the application server that receives requests after router middleware.",
            "Loopback keeps the example local; remote URLs require explicit TLS, identity, and egress controls.",
            "The returned upstream response is the native middleware's P3/P4 source; forwardAuth compatibility has no later response visibility.",
            default_source=host_source,
        )
    return None


def _yaml_option(connector: str, path: str, source_file: str, example_file: str, validation: str, example_value: str = "") -> dict[str, Any]:
    detail: dict[str, str] | None = None
    if connector == "envoy":
        detail = _envoy_yaml_detail(path, example_value)
    elif connector == "traefik":
        detail = _traefik_yaml_detail(path, example_value)
    if connector in {"envoy", "traefik"} and detail is None:
        raise ValueError(f"{connector} YAML path lacks source-backed metadata: {path}")
    if detail is None:
        detail = _yaml_detail(
            "YAML field",
            "explicit YAML value in the selected example",
            "No connector default; the host API validates the explicit example value.",
            "Selects host listener, routing, filter, service, or logging setup from the checked-in example.",
            "Keep listener, upstream, and administrative endpoints private unless an explicit deployment design authorizes exposure.",
            "See runtime effect; ext_proc processing_mode and native middleware fields determine lifecycle visibility.",
            default_source="selected template and connector validation code where stated",
        )
    source_symbol = f"YAML path {path}"
    return _option(
        connector, path, "host_connector_yaml", source_file, source_symbol,
        syntax=f"{path}: <value>", value_type=detail["value_type"], allowed_values=detail["allowed_values"], default=detail["default"],
        default_source=detail["default_source"], required=False,
        contexts="The YAML object path shown in the selected example.", inheritance="Host YAML/API defined; not a Common Runtime merge setting.",
        merge_behavior="Host YAML/API defined; checked-in static and dynamic configurations are separate layers.", validation=validation,
        phase_relevance=detail["phase_relevance"], security_relevance=detail["security_relevance"], runtime_effect=detail["runtime_effect"],
        example_file=example_file, description=detail["runtime_effect"], example_value=example_value,
    )


def _compatibility_yaml_options(
    root: Path,
    connector: str,
    source_file: str,
    compatibility_name: str,
    validation: str,
    *,
    deprecated_fragment: str = "",
) -> list[dict[str, Any]]:
    """Render every mapping path in a compatibility YAML separately.

    The prefix prevents a compatibility key from being mistaken for the
    identically named selected native configuration key in the inventory.
    """
    result: list[dict[str, Any]] = []
    example_values = extract_yaml_example_values(root / source_file)
    for path in extract_yaml_paths(root / source_file):
        option = _yaml_option(connector, f"compatibility.{compatibility_name}.{path}", source_file, source_file, validation, example_values.get(path, ""))
        option["source_symbol"] = f"compatibility YAML path {path}"
        option["configuration_layer"] = "compatibility"
        option["compatibility_only"] = True
        option["deprecated"] = bool(deprecated_fragment and deprecated_fragment in path)
        selected_mode = "ext_proc" if connector == "envoy" else "UDS middleware"
        selected_value = option["example_value"] or "the compatibility mapping shown in this file"
        option["default"] = (
            f"Absent from the selected native {selected_mode} configuration. The repository declares no connector-owned "
            f"compatibility default for this field; this compatibility template configures {selected_value}."
        )
        option["default_source"] = "compatibility template; selected/native classification"
        option["contexts"] = f"Compatibility YAML path only ({compatibility_name})"
        option["inheritance"] = "Compatibility-host API behavior; not native connector inheritance."
        option["merge_behavior"] = "Compatibility-host API behavior; not selected native configuration merge."
        if connector == "envoy":
            compatibility_phase = "Compatibility ext_authz path: request authorization/P1 only; no selected ext_proc P2 body, P3 response-header, or P4 response-body coverage."
        else:
            compatibility_phase = "Compatibility classification: do not infer selected native P3 response-header or P4 response-body coverage."
        option["phase_relevance"] = f"{option['phase_relevance']} {compatibility_phase}"
        option["security_relevance"] = (
            f"{option['security_relevance']} Compatibility-only: do not promote this setting as selected native full-lifecycle configuration."
        )
        option["runtime_effect"] = (
            f"{option['runtime_effect']} Compatibility-only host/service setup outside the selected native core path."
        )
        option["description"] = option["runtime_effect"]
        result.append(option)
    return result


def extract_envoy(root: Path) -> list[dict[str, Any]]:
    options: list[dict[str, Any]] = []
    yaml_source = "examples/envoy/safe/envoy-ext-proc-streaming.yaml.in"
    yaml_paths = extract_yaml_paths(root / yaml_source)
    if "static_resources.listeners[].filter_chains[].filters[].typed_config.http_filters[].typed_config.processing_mode.request_body_mode" not in yaml_paths:
        raise ValueError("Envoy YAML extractor did not find ext_proc request body mode")
    yaml_values = extract_yaml_example_values(root / yaml_source)
    for path in yaml_paths:
        options.append(_yaml_option("envoy", path, yaml_source, yaml_source, "Materialize outside the checkout, then run envoy --mode validate -c <generated-config>.", yaml_values.get(path, "")))
    minimal_yaml_source = "examples/envoy/minimal/envoy-ext-proc-streaming.yaml.in"
    if set(extract_yaml_paths(root / minimal_yaml_source)) != set(yaml_paths):
        raise ValueError("Envoy minimal ext_proc YAML fields drift from the documented selected template surface")

    config_source = "connectors/envoy/ext_proc/internal/processor/config.go"
    struct = _read(root, config_source)
    fields = re.findall(r'^\s*([A-Za-z][A-Za-z0-9]+)\s+([^`\n]+)\s+`json:"([a-z0-9_]+)"`', struct, flags=re.M)
    if len(fields) != 14:
        raise ValueError(f"Envoy Config struct extractor found {len(fields)}, expected 14")
    service_values = json.loads(_read(root, "examples/envoy/safe/envoy-ext-proc-service.json"))
    minimal_service_values = json.loads(_read(root, "examples/envoy/minimal/envoy-ext-proc-service.json"))
    if set(minimal_service_values) != set(service_values):
        raise ValueError("Envoy minimal service JSON fields drift from the documented service contract")
    for field, go_type, json_name in fields:
        allowed = "positive value"
        if json_name == "listen_address":
            allowed = "non-empty host:port"
        elif json_name == "transaction_id_header":
            allowed = "non-empty HTTP header name"
        elif json_name == "late_action_policy":
            allowed = "minimal | safe | strict"
        effect = "Sets one bounded ext_proc service control."
        if json_name == "late_action_policy":
            effect = "Selects late decision reporting; minimal and safe record late disruptive decisions as log_only, while strict records strict_abort_not_attempted rather than a fabricated status/reset."
        options.append(_option(
            "envoy", json_name, "service_json_field", config_source, f"processor.Config.{field} / Config.Validate",
            syntax=f'"{json_name}": <{go_type.strip()}>', value_type=go_type.strip(), allowed_values=allowed,
            default="none; JSON decoder/Config.Validate requires every selected field", default_source="processor.Config has no implicit field defaults",
            required=True, contexts="ext_proc service JSON object", inheritance="No inheritance; one JSON object is decoded with unknown fields rejected.",
            merge_behavior="No merge; a second JSON value is rejected after the one configuration object.",
            validation="Config.Validate rejects empty, non-positive, invalid enum, invalid host:port, and inconsistent gRPC/body limits.",
            phase_relevance="Limits and late policy affect P1–P4 processor behavior.", security_relevance="Bound all header, body, gRPC, and timeout values; keep service listen address private.",
            runtime_effect=effect, example_file="examples/envoy/safe/envoy-ext-proc-service.json", description=effect,
            example_value=json.dumps(service_values[json_name]),
        ))
    main_source = "connectors/envoy/ext_proc/cmd/msconnector-envoy-ext-proc/main.go"
    flags = re.findall(r'flag\.(StringVar|BoolVar)\(&[^,]+, "([^"]+)"', _read(root, main_source))
    if {name for _, name in flags} != {"config", "listen", "event-log", "runtime-config", "check-config"}:
        raise ValueError("Envoy CLI flag extractor/schema drift")
    for kind, flag in flags:
        required = flag == "config"
        options.append(_option(
            "envoy", f"--{flag}", "runtime_cli_flag", main_source, f"main / flag.{kind}",
            syntax=f"--{flag}" + (" PATH" if kind == "StringVar" else ""), value_type="CLI flag", allowed_values="see CLI usage; path/host:port where applicable",
            default="required" if required else "optional", default_source="main.go flag registration", required=required,
            contexts="msconnector_envoy_ext_proc command line", inheritance="not applicable", merge_behavior="--listen overrides listen_address after JSON decoding; other flags are direct process inputs.",
            validation="main validates JSON and, where selected, Common Runtime before serving.", phase_relevance="Runtime service setup; --runtime-config selects the actual engine path.",
            security_relevance="Use absolute controlled paths for runtime/event files and a private service listener.", runtime_effect="Controls ext_proc service startup/check behavior.",
            example_file="connectors/envoy/config/prepare_envoy_ext_proc_config.sh", description="ext_proc service CLI flag."))
    placeholders = sorted(set(re.findall(r"@([A-Z_]+)@", _read(root, yaml_source))))
    expected_placeholders = {"ENVOY_RELEASE", "LISTEN_PORT", "UPSTREAM_PORT", "EXT_PROC_PORT", "ADMIN_PORT"}
    if set(placeholders) != expected_placeholders:
        raise ValueError(f"Envoy template placeholder drift: {placeholders}")
    for placeholder in placeholders:
        options.append(_option(
            "envoy", f"@{placeholder}@", "example_placeholder", yaml_source, "prepare_envoy_ext_proc_config.sh materializer",
            syntax=f"@{placeholder}@", value_type="template placeholder", allowed_values="materializer-provided, validated value", default="none; must be materialized", default_source="template contains a required placeholder", required=True,
            contexts="Envoy YAML template before materialization", inheritance="not applicable", merge_behavior="substituted once by the repository materializer.",
            validation="The materializer rejects unresolved placeholders and invalid ports; output must be outside the checkout.", phase_relevance="Host bootstrap only.",
            security_relevance="Use private, non-conflicting ports; never place generated runtime output in the checkout.", runtime_effect="Supplies a release marker or local endpoint value to the generated Envoy configuration.",
            example_file=yaml_source, description="Template placeholder, not an Envoy configuration field."))
    options.extend(_compatibility_yaml_options(
        root, "envoy", "examples/envoy/compatibility-ext-authz/envoy-ext-authz.yaml", "ext_authz",
        "Validate as an Envoy ext_authz compatibility configuration.", deprecated_fragment="authorization_request.allowed_headers",
    ))
    options.append(_option(
        "envoy", "envoy.filters.http.ext_authz", "compatibility", "examples/envoy/compatibility-ext-authz/envoy-ext-authz.yaml", "ext_authz compatibility filter",
        syntax="name: envoy.filters.http.ext_authz", value_type="Envoy compatibility filter", allowed_values="ext_authz v3 configuration", default="not part of selected ext_proc path", default_source="compatibility template", required=False,
        contexts="Compatibility Envoy HTTP filter chain", inheritance="not part of ext_proc configuration", merge_behavior="not part of selected full-lifecycle configuration", validation="Separate ext_authz configuration validation.",
        phase_relevance="Request authorization compatibility path; no selected P3/P4 coverage.", security_relevance="Do not represent it as the native ext_proc full-lifecycle configuration.", runtime_effect="Routes to separate authorization compatibility service.",
        example_file="examples/envoy/compatibility-ext-authz/envoy-ext-authz.yaml", description="Compatibility-only ext_authz filter.", compatibility_only=True, deprecated=True))
    return options


def _traefik_plugin_option(path: str, source_file: str, example_file: str) -> dict[str, Any]:
    leaf = path.rsplit(".", 1)[-1]
    data = {
        "maxHeaderCount": {
            "type": "integer header-count bound",
            "values": "positive; uds maximum 128",
            "default": "128",
            "effect": "Caps the number of request and response headers passed to native middleware engine callbacks.",
            "phase": "P1 request-header and P3 response-header callback bound; it does not buffer body bytes.",
            "security": "A finite count limits header-flood work before data reaches the UDS engine.",
        },
        "maxHeaderBytes": {
            "type": "integer aggregate header-byte bound",
            "values": "positive; uds maximum 65536",
            "default": "65536",
            "effect": "Caps aggregate request and response header bytes passed to native middleware engine callbacks.",
            "phase": "P1 request-header and P3 response-header callback byte bound.",
            "security": "The UDS wire contract rejects values above 65536; retain a bounded header budget.",
        },
        "maxRequestChunkBytes": {
            "type": "integer request-body chunk-byte bound",
            "values": "positive; uds maximum 32768",
            "default": "32768",
            "effect": "Caps each streamed request-body chunk offered to the native middleware engine.",
            "phase": "P2 request-body callback bound; it is a per-chunk limit, not a total request-body limit.",
            "security": "The UDS wire contract rejects values above 32768 and prevents one callback from accepting an unbounded chunk.",
        },
        "maxResponseChunkBytes": {
            "type": "integer response-body chunk-byte bound",
            "values": "positive; uds maximum 32768",
            "default": "32768",
            "effect": "Caps each streamed response-body chunk offered to the native middleware engine.",
            "phase": "P4 response-body callback bound; a late disruptive result remains log-only after response commitment.",
            "security": "The UDS wire contract rejects values above 32768; retain the bound for response-stream resource control.",
        },
        "transactionIDHeader": {
            "type": "HTTP header-name string",
            "values": "non-empty non-whitespace header name",
            "default": "X-Request-Id",
            "effect": "Selects the incoming request header used to correlate middleware and engine transaction metadata.",
            "phase": "P1 request-header metadata selection; the value is carried through later lifecycle summaries, not used as a policy rule by itself.",
            "security": "Do not put credentials or arbitrary sensitive payload into a correlation header; event/log consumers must protect it.",
        },
        "engineMode": {
            "type": "native middleware engine-mode enum",
            "values": "passthrough | uds",
            "default": "passthrough",
            "effect": "Selects source-only passthrough or the persistent UDS engine; the selected rule-evaluating example uses uds.",
            "phase": "passthrough always allows and supplies no rule evaluation; uds is the engine transport for native P1/P2/P3/P4 callbacks.",
            "security": "Use uds for the selected rule-evaluating path; passthrough is intentionally not enforcement.",
        },
        "engineSocketPath": {
            "type": "absolute Unix-domain socket path",
            "values": "required for uds; absolute with no NUL or '..' segment",
            "default": "none (ignored outside uds; required and validated in uds mode)",
            "effect": "Names the private UDS path used by native middleware when engineMode is uds.",
            "phase": "Transport endpoint for native P1/P2/P3/P4 engine callbacks when uds mode is selected.",
            "security": "The socket directory and socket must be private to trusted processes; path traversal and NUL are rejected.",
        },
    }[leaf]
    return _option(
        "traefik", path, "host_connector_yaml", source_file, f"native_middleware.Config.{leaf} / normalizedConfig",
        syntax=f"{path}: <{leaf}>", value_type=data["type"], allowed_values=data["values"], default=data["default"],
        default_source="connectors/traefik/native_middleware/middleware.go:CreateConfig", required=False,
        contexts="http.middlewares.<name>.plugin.modsecurityNative", inheritance="Traefik dynamic configuration object; no Common Runtime merge.",
        merge_behavior="Traefik/plugin configuration is normalized once by the plugin.", validation="normalizedConfig rejects invalid values; Traefik parses the containing dynamic configuration.",
        phase_relevance=data["phase"], security_relevance=data["security"],
        runtime_effect=data["effect"], example_file=example_file, description=data["effect"],
    )


def extract_traefik(root: Path) -> list[dict[str, Any]]:
    options: list[dict[str, Any]] = []
    static_source = "examples/traefik/minimal/traefik-static.yaml"
    dynamic_source = "examples/traefik/safe/traefik-dynamic.yaml"
    paths = [(static_source, path) for path in extract_yaml_paths(root / static_source)] + [(dynamic_source, path) for path in extract_yaml_paths(root / dynamic_source)]
    seen: set[str] = set()
    plugin_leaves = {"maxHeaderCount", "maxHeaderBytes", "maxRequestChunkBytes", "maxResponseChunkBytes", "transactionIDHeader", "engineMode", "engineSocketPath"}
    values_by_source = {static_source: extract_yaml_example_values(root / static_source), dynamic_source: extract_yaml_example_values(root / dynamic_source)}
    for source, path in paths:
        if path in seen:
            continue
        seen.add(path)
        if path.rsplit(".", 1)[-1] in plugin_leaves:
            option = _traefik_plugin_option(path, "connectors/traefik/native_middleware/middleware.go", dynamic_source)
            option["example_value"] = values_by_source[source].get(path, "")
            options.append(option)
        else:
            options.append(_yaml_option("traefik", path, source, source, "traefik check --configFile=<static-config>; load the selected File Provider configuration.", values_by_source[source].get(path, "")))
    if not any(option["name"].endswith("engineMode") for option in options):
        raise ValueError("Traefik YAML extractor did not find native plugin config")
    normalize_profile_path = lambda path: re.sub(r"\.modsecurity-native-[^.]+", ".<native-middleware>", path)
    minimal_dynamic_paths = {normalize_profile_path(path) for path in extract_yaml_paths(root / "examples/traefik/minimal/traefik-dynamic.yaml")}
    safe_dynamic_paths = {normalize_profile_path(path) for path in extract_yaml_paths(root / dynamic_source)}
    if minimal_dynamic_paths != safe_dynamic_paths:
        raise ValueError("Traefik minimal dynamic YAML fields drift from the documented selected middleware surface")
    options.extend(_compatibility_yaml_options(
        root, "traefik", "examples/traefik/compatibility-forwardauth/traefik-static.yaml", "forwardauth-static",
        "Validate as a Traefik forwardAuth compatibility configuration.",
    ))
    options.extend(_compatibility_yaml_options(
        root, "traefik", "examples/traefik/compatibility-forwardauth/traefik-dynamic.yaml", "forwardauth-dynamic",
        "Validate as a Traefik forwardAuth compatibility configuration.",
    ))
    options.append(_option(
        "traefik", "forwardAuth", "compatibility", "examples/traefik/compatibility-forwardauth/traefik-dynamic.yaml", "forwardAuth compatibility middleware",
        syntax="forwardAuth: { address: <url>, trustForwardHeader: <bool> }", value_type="Traefik compatibility middleware", allowed_values="forwardAuth fields in the compatibility example",
        default="not part of selected native middleware path", default_source="compatibility template", required=False, contexts="Compatibility dynamic middleware", inheritance="not part of native middleware", merge_behavior="not part of native middleware", validation="Separate Traefik compatibility configuration validation.",
        phase_relevance="Request-authorization compatibility path; no selected P3/P4 configuration.", security_relevance="Do not present forwardAuth as the native UDS rule-evaluating path.", runtime_effect="Routes to separate authorization service.",
        example_file="examples/traefik/compatibility-forwardauth/traefik-dynamic.yaml", description="Compatibility-only forwardAuth middleware.", compatibility_only=True))
    return options


def _assert_source_default_contracts(root: Path, options: Iterable[dict[str, Any]]) -> None:
    """Reject generated defaults that no longer match source constants.

    This makes a default change fail the source-to-documentation check even if
    no parser name changed.  Values intentionally described as ``none`` or
    host-defined are not guessed here.
    """
    by_key = {(item["connector"], item["name"]): item["default"] for item in options}
    options_header = _read(root, "common/include/msconnector/options.h")
    config_header = _read(root, "common/include/msconnector/block_statuses.h")
    limits_header = _read(root, "common/include/msconnector/limits.h")
    expected_tokens = {
        "MSCONNECTOR_DEFAULT_ENABLE MSCONNECTOR_BOOL_OFF": "common enabled default",
        "MSCONNECTOR_DEFAULT_USE_ERROR_LOG MSCONNECTOR_BOOL_ON": "common error-log default",
        "MSCONNECTOR_DEFAULT_PHASE4_MODE MSCONNECTOR_PHASE4_MODE_SAFE": "common phase4 default",
        "MSCONNECTOR_DEFAULT_PHASE4_BODY_LIMIT 1048576": "common phase4 byte default",
    }
    for token, label in expected_tokens.items():
        if token not in options_header:
            raise ValueError(f"{label} source constant changed: expected {token!r}")
    for token in ("MSCONNECTOR_DEFAULT_BLOCK_STATUS 403", "MSCONNECTOR_DEFAULT_ERROR_STATUS 500"):
        if token not in config_header:
            raise ValueError(f"block-status default source constant changed: expected {token!r}")
    for token in (
        "MSCONNECTOR_MAX_HEADER_COUNT 256U", "MSCONNECTOR_MAX_HEADER_NAME_LENGTH 256U",
        "MSCONNECTOR_MAX_HEADER_VALUE_LENGTH 8192U", "MSCONNECTOR_MAX_TOTAL_HEADER_BYTES 65536U",
        "MSCONNECTOR_MAX_BODY_BUFFER_SIZE 1048576U", "MSCONNECTOR_MAX_RESPONSE_BODY_BUFFER_SIZE 1048576U",
        "MSCONNECTOR_MAX_EVENT_JSON_BYTES 16384U",
    ):
        if token not in limits_header:
            raise ValueError(f"resource-limit default source constant changed: expected {token!r}")
    expected_defaults = {
        ("common", "enabled"): "off", ("common", "use_error_log"): "on", ("common", "phase4_mode"): "safe",
        ("common", "request_body_limit"): "1048576", ("common", "response_body_limit"): "1048576",
        ("common", "body_limit_action"): "reject", ("common", "late_intervention_timeout"): "0",
        ("common", "default_block_status"): "403", ("common", "default_error_status"): "500",
        ("common", "max_header_count"): "256", ("common", "max_header_name_size"): "256",
        ("common", "max_header_value_size"): "8192", ("common", "max_total_header_bytes"): "65536",
        ("common", "max_event_json_bytes"): "16384",
        ("apache", "modsecurity"): "off", ("apache", "modsecurity_use_error_log"): "on",
        ("apache", "modsecurity_phase4_mode"): "safe", ("apache", "modsecurity_phase4_body_limit"): "1048576",
        ("nginx", "modsecurity"): "off", ("nginx", "modsecurity_use_error_log"): "on",
        ("nginx", "modsecurity_phase4_mode"): "safe", ("nginx", "modsecurity_phase4_body_limit"): "1048576",
        ("haproxy", "phase4-mode"): "safe",
    }
    for key, expected in expected_defaults.items():
        actual = by_key.get(key)
        if actual != expected:
            raise ValueError(f"documented default drift for {key[0]}:{key[1]}: {actual!r} != {expected!r}")
    traefik_source = _read(root, "connectors/traefik/native_middleware/middleware.go")
    for token in ("defaultMaxHeaderCount        = 128", "defaultMaxHeaderBytes        = 64 << 10", "defaultMaxRequestChunkBytes  = 32 << 10", "defaultMaxResponseChunkBytes = 32 << 10"):
        if token not in traefik_source:
            raise ValueError(f"Traefik plugin default source changed: expected {token!r}")
    for suffix, expected in {
        "maxHeaderCount": "128", "maxHeaderBytes": "65536", "maxRequestChunkBytes": "32768",
        "maxResponseChunkBytes": "32768", "transactionIDHeader": "X-Request-Id", "engineMode": "passthrough",
    }.items():
        matches = [value for (connector, name), value in by_key.items() if connector == "traefik" and name.endswith(suffix)]
        if not matches or any(value != expected for value in matches):
            raise ValueError(f"Traefik documented default drift for {suffix}: {matches!r}")


def build_inventory(root: Path = ROOT) -> list[dict[str, Any]]:
    """Build the complete source-backed, deterministic inventory."""
    options: list[dict[str, Any]] = []
    options.extend(extract_apache(root))
    options.extend(extract_nginx(root))
    options.extend(extract_haproxy(root))
    options.extend(extract_envoy(root))
    options.extend(extract_traefik(root))
    options.extend(extract_lighttpd(root))
    options.extend(extract_common_runtime(root))
    options.extend(extract_engine_directives(root))
    options.extend(extract_host_example_fields(root, options))
    # JSON inventory order is stable and deliberately puts primary/native rows
    # before compatibility rows when names compare equally.
    options = sorted(options, key=lambda option: (option["connector"], option["compatibility_only"], option["name"]))
    _assert_source_default_contracts(root, options)
    return options


def inventory_json(root: Path = ROOT) -> str:
    return json.dumps({"schema_version": 1, "options": build_inventory(root)}, indent=2, sort_keys=False) + "\n"


def _local_options(options: Iterable[dict[str, Any]], connector: str) -> list[dict[str, Any]]:
    return [option for option in options if option["connector"] == connector]


def _table_row(option: dict[str, Any], german: bool) -> str:
    if german:
        option = _german_option(option)
    description = option["description"]
    return "| [`{name}`](#{anchor}) | {layer} | {type} | {required} | {default} | {contexts} | {description} |".format(
        name=option["name"], anchor=_slug(option["name"]), layer=layer_name(option["configuration_layer"], german),
        type=_table_cell(option["value_type"]), required=("ja" if option["required"] else "nein") if german else ("yes" if option["required"] else "no"),
        default=_table_cell(option["default"]), contexts=_table_cell(option["contexts"]), description=_table_cell(description),
    )


def _table_cell(value: str) -> str:
    return value.replace("|", "\\|").replace("\n", "<br>")


def _inline_literal(value: str) -> str:
    delimiter = "``" if "`" in value else "`"
    return f"{delimiter}{value}{delimiter}"


GERMAN_TEXT: dict[str, str] = {
    # Types.  Identifiers, enum members, syntax, paths, and literal example
    # values deliberately stay unchanged; their surrounding explanations do
    # not.  Keeping this table at the rendering boundary leaves the JSON
    # inventory stable for machine consumers while making the German
    # companions genuinely German.
    "boolean": "Boolescher Wert",
    "string": "Zeichenkette",
    "string/expression": "Zeichenkette/Ausdruck",
    "two strings": "zwei Zeichenketten",
    "Apache string expression": "Apache-Zeichenausdruck",
    "path": "Pfad",
    "path alias": "Pfad-Alias",
    "URL": "URL",
    "enum": "Aufzählung",
    "header name": "Headername",
    "positive decimal byte count": "positive dezimale Byteanzahl",
    "positive decimal bytes": "positive dezimale Byteanzahl",
    "positive decimal count": "positive dezimale Anzahl",
    "non-negative decimal milliseconds": "nichtnegative dezimale Millisekundenanzahl",
    "HAProxy filter declaration": "HAProxy-Filterdeklaration",
    "compatibility filter": "Kompatibilitätsfilter",
    "compatibility host setup": "Kompatibilitäts-Hosteinrichtung",
    "compatibility policy string": "Kompatibilitäts-Policy-Zeichenkette",
    "historical configuration": "historische Konfiguration",
    "lighttpd boolean": "lighttpd-Boolean",
    "lighttpd compatibility host field": "lighttpd-Kompatibilitäts-Hostfeld",
    "host-owned configuration field": "hosteigenes Konfigurationsfeld",
    "YAML field": "YAML-Feld",
    "Envoy ext_proc BodySendMode": "Envoy-ext_proc-BodySendMode",
    "Envoy ext_proc HeaderSendMode": "Envoy-ext_proc-HeaderSendMode",
    "uint32 port": "uint32-Port",
    "int": "Ganzzahl",
    "int64": "64-Bit-Ganzzahl",
    "integer": "Ganzzahl",
    "integer bytes": "Ganzzahl in Byte",
    "absolute path": "absoluter Pfad",
    "absolute Unix socket path": "absoluter Unix-Socket-Pfad",
    "CLI flag": "Kommandozeilenoption",
    "template placeholder": "Template-Platzhalter",
    "service JSON field": "Service-JSON-Feld",
    "ModSecurity engine directive": "ModSecurity-Engine-Direktive",
    "HTTP status": "HTTP-Status",
    "HTTP error status": "HTTP-Fehlerstatus",
    "Traefik compatibility middleware": "Traefik-Kompatibilitäts-Middleware",
    "Envoy compatibility filter": "Envoy-Kompatibilitätsfilter",

    # Allowed values and defaults.
    "0 or positive integer": "0 oder positive Ganzzahl",
    "allowed blocking status": "zulässiger Sperrstatus",
    "audit log type": "Audit-Log-Typ",
    "audit part letters": "Audit-Log-Teilbuchstaben",
    "decimal integer": "dezimale Ganzzahl",
    "engine audit mode": "Engine-Auditmodus",
    "explicit YAML value in the selected example": "expliziter YAML-Wert im ausgewählten Beispiel",
    "explicit compatibility example value": "expliziter Wert des Kompatibilitätsbeispiels",
    "ext_authz v3 configuration": "ext_authz-v3-Konfiguration",
    "forwardAuth fields in the compatibility example": "forwardAuth-Felder im Kompatibilitätsbeispiel",
    "key and URL": "Schlüssel und URL",
    "lighttpd boolean values; examples use enable/disable": "lighttpd-Boolean-Werte; die Beispiele verwenden enable/disable",
    "materializer placeholder resolved to decimal 1..65535": "vom Materializer auf dezimal 1..65535 aufgelöster Platzhalter",
    "materializer-provided, validated value": "vom Materializer bereitgestellter und validierter Wert",
    "non-empty HTTP header name": "nichtleerer HTTP-Headername",
    "non-empty host-specific transaction identifier": "nichtleere hostspezifische Transaktionskennung",
    "non-empty host:port": "nichtleeres host:port",
    "non-empty non-whitespace header name": "nichtleerer Headername ohne Leerraum",
    "non-empty readable Common Runtime key=value file": "nichtleere lesbare Common-Runtime-key=value-Datei",
    "non-empty text": "nichtleerer Text",
    "not an active selected option": "keine aktive ausgewählte Option",
    "on/off-style compatibility boolean": "Kompatibilitäts-Boolean im on/off-Stil",
    "one configuration path": "ein Konfigurationspfad",
    "one connector JSONL event/intervention-log path": "ein Pfad für das Connector-JSONL-Ereignis-/Interventionslog",
    "one inline ModSecurity rule/configuration string": "eine Inline-Zeichenkette für ModSecurity-Regel/Konfiguration",
    "one inline rule/configuration string": "eine Inline-Zeichenkette für Regel/Konfiguration",
    "one non-empty Apache expression": "ein nichtleerer Apache-Ausdruck",
    "one or more MIME types": "ein oder mehrere MIME-Typen",
    "one readable file with MIME tokens": "eine lesbare Datei mit MIME-Token",
    "one readable rule/configuration file": "eine lesbare Regel-/Konfigurationsdatei",
    "one readable rules/configuration path": "ein lesbarer Regel-/Konfigurationspfad",
    "one required rules-file argument; optional phase4-mode": "ein erforderliches rules-file-Argument; phase4-mode ist optional",
    "ordinary lighttpd proxy fields": "normale lighttpd-Proxy-Felder",
    "parser-supported compatibility value": "vom Parser unterstützter Kompatibilitätswert",
    "path or glob": "Pfad oder Glob",
    "path without a parent-directory segment": "Pfad ohne übergeordnetes Verzeichnissegment",
    "positive byte count": "positive Byteanzahl",
    "positive integer": "positive Ganzzahl",
    "positive value": "positiver Wert",
    "positive; uds maximum 128": "positiv; UDS-Maximum 128",
    "positive; uds maximum 32768": "positiv; UDS-Maximum 32768",
    "positive; uds maximum 65536": "positiv; UDS-Maximum 65536",
    "readable ModSecurity configuration/rules file path": "lesbarer ModSecurity-Konfigurations-/Regeldateipfad",
    "reject | process_partial (accepted spelling variants are parser-specific)": "reject | process_partial (akzeptierte Schreibvarianten sind parserspezifisch)",
    "remote URL paired with rules_remote_key": "Remote-URL, die mit rules_remote_key gepaart wird",
    "remote key paired with rules_remote_url": "Remote-Schlüssel, der mit rules_remote_url gepaart wird",
    "required for uds; absolute with no NUL or '..' segment": "für uds erforderlich; absolut und ohne NUL- oder '..'-Segment",
    "rule expression": "Regelausdruck",
    "same grammar as event_path": "gleiche Grammatik wie event_path",
    "see CLI usage; path/host:port where applicable": "siehe CLI-Verwendung; gegebenenfalls Pfad/host:port",
    "the explicit value in the selected checked-in example": "der explizite Wert im ausgewählten eingecheckten Beispiel",
    "valid HTTP error status": "gültiger HTTP-Fehlerstatus",

    "Envoy proto default NONE; selected full-lifecycle template explicitly sets STREAMED.": "Envoy-Proto-Standard NONE; das ausgewählte Full-Lifecycle-Template setzt ausdrücklich STREAMED.",
    "Envoy proto default SKIP; selected template explicitly sets SEND for EOS handling.": "Envoy-Proto-Standard SKIP; das ausgewählte Template setzt für die EOS-Behandlung ausdrücklich SEND.",
    "Envoy proto default false; selected template explicitly sets false.": "Envoy-Proto-Standard false; das ausgewählte Template setzt ausdrücklich false.",
    "Envoy proto effective default SEND; selected template explicitly sets SEND.": "Effektiver Envoy-Proto-Standard SEND; das ausgewählte Template setzt ausdrücklich SEND.",
    "No connector default; the host API validates the explicit example value.": "Kein Connector-Standardwert; die Host-API validiert den expliziten Beispielwert.",
    "No connector default; this host field is explicit in the example.": "Kein Connector-Standardwert; dieses Hostfeld ist im Beispiel explizit gesetzt.",
    "No default is inferred from examples.": "Aus den Beispielen wird kein Standardwert abgeleitet.",
    "Not part of the selected native integration path; explicit compatibility example value.": "Nicht Teil des ausgewählten nativen Integrationspfads; expliziter Wert des Kompatibilitätsbeispiels.",
    "The used examples select On; no repository source establishes a global engine default.": "Die verwendeten Beispiele wählen On; keine Repository-Quelle legt einen globalen Engine-Standardwert fest.",
    "host defaults when omitted": "Host-Standardwerte bei Auslassung",
    "none; JSON decoder/Config.Validate requires every selected field": "kein Wert; JSON-Decoder/Config.Validate verlangt jedes ausgewählte Feld",
    "none; connector creates a fallback identifier": "kein Wert; der Connector erzeugt eine Ersatzkennung",
    "none; must be materialized": "kein Wert; muss materialisiert werden",
    "none; optional": "kein Wert; optional",
    "none; required": "kein Wert; erforderlich",
    "not a native connector option": "keine native Connector-Option",
    "not applicable; a filter is active only when declared": "nicht anwendbar; ein Filter ist nur aktiv, wenn er deklariert ist",
    "not available": "nicht verfügbar",
    "not part of native mod_msconnector": "nicht Teil von nativem mod_msconnector",
    "not part of selected ext_proc path": "nicht Teil des ausgewählten ext_proc-Pfads",
    "not part of selected native middleware path": "nicht Teil des ausgewählten nativen Middleware-Pfads",
    "not part of the native HTX path": "nicht Teil des nativen HTX-Pfads",
    "unset unless configured": "nicht gesetzt, sofern nicht konfiguriert",

    # Context, inheritance, and merge semantics.
    "Apache RSRC_CONF | ACCESS_CONF (server/vhost and per-directory contexts supported by Apache's context rules)": "Apache RSRC_CONF | ACCESS_CONF (Server-/VHost- und Verzeichnis-Kontexte gemäß den Apache-Kontextregeln)",
    "Common Runtime key=value file": "Common-Runtime-key=value-Datei",
    "Compatibility Envoy HTTP filter chain": "Kompatibilitäts-Envoy-HTTP-Filterkette",
    "Compatibility YAML path only": "nur YAML-Pfad der Kompatibilität",
    "Compatibility dynamic middleware": "dynamische Kompatibilitäts-Middleware",
    "Compatibility example": "Kompatibilitätsbeispiel",
    "Compatibility frontend only": "nur Kompatibilitäts-Frontend",
    "Envoy YAML template before materialization": "Envoy-YAML-Template vor der Materialisierung",
    "Historical compatibility documentation only": "nur historische Kompatibilitätsdokumentation",
    "Loaded ModSecurity configuration/rule file": "geladene ModSecurity-Konfigurations-/Regeldatei",
    "SPOE/SPOP compatibility agent key=value file": "SPOE/SPOP-Kompatibilitätsagent-key=value-Datei",
    "The YAML object path shown in the selected example.": "Der im ausgewählten Beispiel gezeigte YAML-Objektpfad.",
    "The context shown in the checked-in example; consult the pinned host documentation for all host-specific contexts.": "Der im eingecheckten Beispiel gezeigte Kontext; für alle hostspezifischen Kontexte ist die festgelegte Hostdokumentation maßgeblich.",
    "The selected and checked-in native use is a HAProxy frontend. The local parser does not assert additional host scopes.": "Die ausgewählte und eingecheckte native Nutzung ist ein HAProxy-Frontend. Der lokale Parser legt keine weiteren Host-Geltungsbereiche fest.",
    "ext_proc service JSON object": "ext_proc-Service-JSON-Objekt",
    "lighttpd sidecar compatibility configuration": "lighttpd-Sidecar-Kompatibilitätskonfiguration",
    "msconnector_envoy_ext_proc command line": "msconnector_envoy_ext_proc-Kommandozeile",

    "Compatibility-host API behavior; not native connector inheritance.": "Verhalten der Kompatibilitäts-Host-API; keine native Connector-Vererbung.",
    "Engine-specific; not a host connector merge setting.": "Engine-spezifisch; keine Merge-Einstellung des Hostconnectors.",
    "Host YAML/API defined; not a Common Runtime merge setting.": "Durch Host-YAML/API bestimmt; keine Common-Runtime-Merge-Einstellung.",
    "Host-defined compatibility behavior; not native plugin inheritance.": "Hostdefiniertes Kompatibilitätsverhalten; keine native Plugin-Vererbung.",
    "Host-defined; not implemented by this connector.": "Hostdefiniert; nicht durch diesen Connector implementiert.",
    "No connector-local inheritance callback is registered; each filter declaration owns one filter configuration.": "Es ist kein Connector-lokaler Vererbungs-Callback registriert; jede Filterdeklaration besitzt eine Filterkonfiguration.",
    "No file-level inheritance; host integrations may merge their own configuration before starting Common Runtime.": "Keine Vererbung auf Dateiebene; Hostintegrationen können ihre eigene Konfiguration vor dem Start der Common Runtime zusammenführen.",
    "No inheritance; one JSON object is decoded with unknown fields rejected.": "Keine Vererbung; ein JSON-Objekt wird dekodiert, unbekannte Felder werden abgewiesen.",
    "No native HTX inheritance; one compatibility-agent config file.": "Keine native HTX-Vererbung; eine Konfigurationsdatei des Kompatibilitätsagenten.",
    "Only defaults are loaded; no documented conditional request-time override.": "Es werden nur Standardwerte geladen; keine dokumentierte bedingte Überschreibung zur Request-Zeit.",
    "Only defaults are loaded; the module has no request-time conditional patch path.": "Es werden nur Standardwerte geladen; das Modul besitzt keinen bedingten Patch-Pfad zur Request-Zeit.",
    "Parent value is available to the child unless a child value is set; see the Apache directory-config merge function.": "Der Elternwert steht dem Kind zur Verfügung, sofern kein Kindwert gesetzt ist; siehe die Apache-Merge-Funktion für Verzeichniskonfigurationen.",
    "Traefik dynamic configuration object; no Common Runtime merge.": "Dynamisches Traefik-Konfigurationsobjekt; kein Common-Runtime-Merge.",
    "http → server → location; a child inherits if it does not set a value.": "http → server → location; ein Kind erbt, wenn es keinen Wert setzt.",
    "not applicable": "nicht anwendbar",
    "not applicable to native plugin": "nicht auf das native Plugin anwendbar",
    "not documented as native inheritance": "nicht als native Vererbung dokumentiert",
    "not part of ext_proc configuration": "nicht Teil der ext_proc-Konfiguration",
    "not part of native middleware": "nicht Teil der nativen Middleware",

    "--listen overrides listen_address after JSON decoding; other flags are direct process inputs.": "--listen überschreibt listen_address nach dem JSON-Dekodieren; andere Optionen sind direkte Prozesseingaben.",
    "Common scalar values use child-over-parent merge; rule sets are merged through msc_rules_merge. Transaction-id expression/static-id are mutually exclusive.": "Common-Skalarwerte verwenden einen Kind-vor-Eltern-Merge; Regelsätze werden über msc_rules_merge zusammengeführt. Transaktions-ID-Ausdruck und statische ID schließen sich gegenseitig aus.",
    "Compatibility-host API behavior; not selected native configuration merge.": "Verhalten der Kompatibilitäts-Host-API; kein Merge der ausgewählten nativen Konfiguration.",
    "Engine-specific; include order and rule configuration determine effective behavior.": "Engine-spezifisch; Include-Reihenfolge und Regelkonfiguration bestimmen das wirksame Verhalten.",
    "Host YAML/API defined; checked-in static and dynamic configurations are separate layers.": "Durch Host-YAML/API bestimmt; eingecheckte statische und dynamische Konfigurationen sind getrennte Ebenen.",
    "Host-defined compatibility behavior; not part of mod_msconnector.": "Hostdefiniertes Kompatibilitätsverhalten; nicht Teil von mod_msconnector.",
    "Host-defined; not implemented by this connector.": "Hostdefiniert; nicht durch diesen Connector implementiert.",
    "No connector-local merge; filter arguments initialise a per-filter common configuration.": "Kein Connector-lokaler Merge; Filterargumente initialisieren eine Common-Konfiguration pro Filter.",
    "No merge; a second JSON value is rejected after the one configuration object.": "Kein Merge; ein zweiter JSON-Wert wird nach dem einen Konfigurationsobjekt abgewiesen.",
    "No merge; config_set applies one parsed value.": "Kein Merge; config_set übernimmt einen geparsten Wert.",
    "Plugin defaults retain the configured string.": "Plugin-Standardwerte behalten die konfigurierte Zeichenkette.",
    "Traefik/plugin configuration is normalized once by the plugin.": "Die Traefik-/Plugin-Konfiguration wird einmalig durch das Plugin normalisiert.",
    "When a host uses msconnector_config, scalar child values override parent values; runtime files are parsed as one concrete configuration.": "Wenn ein Host msconnector_config verwendet, überschreiben Skalarkindwerte Elternwerte; Runtime-Dateien werden als eine konkrete Konfiguration geparst.",
    "config_plugin_values_init populates defaults; no documented per-request merge.": "config_plugin_values_init belegt Standardwerte; kein dokumentierter Merge pro Request.",
    "ngx_conf_merge_* combines scalar/pointer configuration, while msc_rules_merge combines parent and child rules.": "ngx_conf_merge_* führt Skalar-/Zeigerkonfiguration zusammen, während msc_rules_merge Eltern- und Kindregeln zusammenführt.",
    "not part of mod_msconnector": "nicht Teil von mod_msconnector",
    "not part of native HTX merge": "nicht Teil des nativen HTX-Merge",
    "not part of native middleware": "nicht Teil der nativen Middleware",
    "not part of selected full-lifecycle configuration": "nicht Teil der ausgewählten Full-Lifecycle-Konfiguration",
    "substituted once by the repository materializer.": "wird einmalig durch den Repository-Materializer ersetzt.",

    # Explicitly retained protocol literals and the remaining source-backed
    # value explanations.  Identity mappings make the no-fallback audit below
    # distinguish deliberately unchanged protocol vocabulary from prose that
    # still needs a translation.
    "LateActionPolicy": "LateActionPolicy",
    "string/path": "Zeichenkette/Pfad",
    "DEFAULT | SEND | SKIP": "DEFAULT | SEND | SKIP",
    "HAProxy SPOE syntax only": "nur HAProxy-SPOE-Syntax",
    "NONE | STREAMED | BUFFERED | BUFFERED_PARTIAL | FULL_DUPLEX_STREAMED | GRPC": "NONE | STREAMED | BUFFERED | BUFFERED_PARTIAL | FULL_DUPLEX_STREAMED | GRPC",
    "On | Off": "On | Off",
    "On | Off | DetectionOnly": "On | Off | DetectionOnly",
    "ProcessPartial | Reject": "ProcessPartial | Reject",
    "minimal | safe | strict": "minimal | safe | strict",
    "minimal | safe | strict; before commit all use deny_if_possible, after commit minimal/safe are log_only and strict is abort_connection": "minimal | safe | strict; vor dem Commit verwenden alle deny_if_possible, nach dem Commit verwenden minimal/safe log_only und strict abort_connection",
    "none | buffered | streaming": "none | buffered | streaming",
    "on | off": "on | off",
    "on | off (the shared parser additionally accepts true/false/1/0/yes/no where the host passes it through)": "on | off (der gemeinsame Parser akzeptiert zusätzlich true/false/1/0/yes/no, sofern der Host diese Werte durchreicht)",
    "on | off | true | false | 1 | 0 | yes | no": "on | off | true | false | 1 | 0 | yes | no",
    "one readable libmodsecurity configuration/rules path; absolute paths are recommended, while relative-path resolution is delegated to libmodsecurity": "ein lesbarer libmodsecurity-Konfigurations-/Regelpfad; absolute Pfade werden empfohlen, während die Auflösung relativer Pfade libmodsecurity überlassen wird",
    "passthrough | uds": "passthrough | uds",
    "true | false": "true | false",
    "-": "-",
    "0": "0",
    "1": "1",
    "1048576": "1048576",
    "127.0.0.1": "127.0.0.1",
    "128": "128",
    "16384": "16384",
    "2000": "2000",
    "256": "256",
    "32768": "32768",
    "403": "403",
    "4096": "4096",
    "500": "500",
    "65532": "65532",
    "65536": "65536",
    "8192": "8192",
    "X-Request-Id": "X-Request-Id",
    "block": "block",
    "buffered": "buffered",
    "closed": "closed",
    "false": "false",
    "none": "none",
    "off": "off",
    "on": "on",
    "optional": "optional",
    "passthrough": "passthrough",
    "production": "production",
    "reject": "reject",
    "required": "erforderlich",
    "safe": "safe",
    "x-request-id": "x-request-id",

    # Source anchors are normally code paths and stay recognizable.  Natural
    # language qualifiers around them are translated.
    "Apache parser registration has no default": "Die Apache-Parserregistrierung hat keinen Standardwert",
    "active example configuration": "aktive Beispielkonfiguration",
    "ck_calloc plugin_data allocation and default config": "ck_calloc-Allocation von plugin_data und Standardkonfiguration",
    "compatibility example": "Kompatibilitätsbeispiel",
    "compatibility template": "Kompatibilitäts-Template",
    "config_init() where stated; otherwise zero/empty initialization": "config_init(), sofern angegeben; andernfalls Initialisierung mit null/leeren Werten",
    "connector transaction creation path": "Connector-Pfad zur Transaktionserzeugung",
    "connector-specific default content-type loader": "connectorspezifischer Standard-Content-Type-Loader",
    "legacy example header": "Kopf des Legacy-Beispiels",
    "main.go flag registration": "Flag-Registrierung in main.go",
    "native HTX keyword parser": "nativer HTX-Schlüsselwortparser",
    "native HTX parser requires rules-file": "nativer HTX-Parser verlangt rules-file",
    "not inferred; only checked-in example usage is documented": "nicht abgeleitet; dokumentiert ist nur die Nutzung in eingecheckten Beispielen",
    "parser registration has no default": "Parserregistrierung hat keinen Standardwert",
    "plugin config_file defaults to NULL": "plugin config_file hat den Standardwert NULL",
    "processor.Config has no implicit field defaults": "processor.Config besitzt keine impliziten Feldstandardwerte",
    "runtime parser has no default": "Runtime-Parser hat keinen Standardwert",
    "selected template and connector validation code where stated": "ausgewähltes Template und Connector-Validierungscode, sofern angegeben",
    "template contains a required placeholder": "Template enthält einen erforderlichen Platzhalter",
    "common/include/msconnector/block_statuses.h:MSCONNECTOR_DEFAULT_BLOCK_STATUS": "common/include/msconnector/block_statuses.h:MSCONNECTOR_DEFAULT_BLOCK_STATUS",
    "common/include/msconnector/block_statuses.h:MSCONNECTOR_DEFAULT_ERROR_STATUS": "common/include/msconnector/block_statuses.h:MSCONNECTOR_DEFAULT_ERROR_STATUS",
    "common/include/msconnector/limits.h:MSCONNECTOR_MAX_BODY_BUFFER_SIZE": "common/include/msconnector/limits.h:MSCONNECTOR_MAX_BODY_BUFFER_SIZE",
    "common/include/msconnector/limits.h:MSCONNECTOR_MAX_EVENT_JSON_BYTES": "common/include/msconnector/limits.h:MSCONNECTOR_MAX_EVENT_JSON_BYTES",
    "common/include/msconnector/limits.h:MSCONNECTOR_MAX_HEADER_COUNT": "common/include/msconnector/limits.h:MSCONNECTOR_MAX_HEADER_COUNT",
    "common/include/msconnector/limits.h:MSCONNECTOR_MAX_HEADER_NAME_LENGTH": "common/include/msconnector/limits.h:MSCONNECTOR_MAX_HEADER_NAME_LENGTH",
    "common/include/msconnector/limits.h:MSCONNECTOR_MAX_HEADER_VALUE_LENGTH": "common/include/msconnector/limits.h:MSCONNECTOR_MAX_HEADER_VALUE_LENGTH",
    "common/include/msconnector/limits.h:MSCONNECTOR_MAX_RESPONSE_BODY_BUFFER_SIZE": "common/include/msconnector/limits.h:MSCONNECTOR_MAX_RESPONSE_BODY_BUFFER_SIZE",
    "common/include/msconnector/limits.h:MSCONNECTOR_MAX_TOTAL_HEADER_BYTES": "common/include/msconnector/limits.h:MSCONNECTOR_MAX_TOTAL_HEADER_BYTES",
    "common/include/msconnector/options.h:MSCONNECTOR_DEFAULT_ENABLE": "common/include/msconnector/options.h:MSCONNECTOR_DEFAULT_ENABLE",
    "common/include/msconnector/options.h:MSCONNECTOR_DEFAULT_PHASE4_BODY_LIMIT": "common/include/msconnector/options.h:MSCONNECTOR_DEFAULT_PHASE4_BODY_LIMIT",
    "common/include/msconnector/options.h:MSCONNECTOR_DEFAULT_PHASE4_MODE": "common/include/msconnector/options.h:MSCONNECTOR_DEFAULT_PHASE4_MODE",
    "common/include/msconnector/options.h:MSCONNECTOR_DEFAULT_USE_ERROR_LOG": "common/include/msconnector/options.h:MSCONNECTOR_DEFAULT_USE_ERROR_LOG",
    "common/runtime/msconnector_runtime.c:runtime_defaults": "common/runtime/msconnector_runtime.c:runtime_defaults",
    "common/src/config.c:msconnector_config_apply_defaults": "common/src/config.c:msconnector_config_apply_defaults",
    "connectors/traefik/native_middleware/middleware.go:CreateConfig": "connectors/traefik/native_middleware/middleware.go:CreateConfig",

    # Validation descriptions.  The command itself stays unchanged.
    "Config.Validate rejects empty, non-positive, invalid enum, invalid host:port, and inconsistent gRPC/body limits.": "Config.Validate weist leere, nichtpositive, ungültige Enum- und host:port-Werte sowie widersprüchliche gRPC-/Body-Limits ab.",
    "Do not use for native validation.": "Nicht für die native Validierung verwenden.",
    "Materialize outside the checkout, then run envoy --mode validate -c <generated-config>.": "Außerhalb des Checkouts materialisieren und anschließend envoy --mode validate -c <generated-config> ausführen.",
    "Missing argument or rule-load failure fails native filter initialisation.": "Ein fehlendes Argument oder ein Fehler beim Laden der Regeln lässt die native Filterinitialisierung fehlschlagen.",
    "Required only when msconnector.enabled is true; missing, unreadable, or invalid runtime configuration returns HANDLER_ERROR during startup.": "Nur bei msconnector.enabled=true erforderlich; eine fehlende, unlesbare oder ungültige Runtime-Konfiguration liefert beim Start HANDLER_ERROR.",
    "Separate Traefik compatibility configuration validation.": "Separate Validierung der Traefik-Kompatibilitätskonfiguration.",
    "Separate compatibility smoke/configuration only.": "Nur separater Kompatibilitäts-Smoke-/Konfigurationscheck.",
    "Separate ext_authz configuration validation.": "Separate Validierung der ext_authz-Konfiguration.",
    "The host/libmodsecurity rejects invalid engine syntax when loading the rule file.": "Der Host/libmodsecurity weist ungültige Engine-Syntax beim Laden der Regeldatei ab.",
    "The materializer rejects unresolved placeholders and invalid ports; output must be outside the checkout.": "Der Materializer weist unaufgelöste Platzhalter und ungültige Ports ab; die Ausgabe muss außerhalb des Checkouts liegen.",
    "The patched HAProxy parser rejects missing/unknown arguments; validate with haproxy -c -f <config>.": "Der gepatchte HAProxy-Parser weist fehlende/unbekannte Argumente ab; mit haproxy -c -f <config> validieren.",
    "Unknown keys fail compatibility-agent configuration parsing.": "Unbekannte Schlüssel lassen das Parsen der Konfiguration des Kompatibilitätsagenten fehlschlagen.",
    "Unknown keys, empty values, malformed assignments, and key-specific invalid values fail the runtime configuration check.": "Unbekannte Schlüssel, leere Werte, fehlerhafte Zuweisungen und schlüsselspezifisch ungültige Werte lassen die Runtime-Konfigurationsprüfung fehlschlagen.",
    "Unknown mode fails parsing. The selected host uses haproxy -c -f <config>.": "Ein unbekannter Modus lässt das Parsen fehlschlagen. Der ausgewählte Host verwendet haproxy -c -f <config>.",
    "Validate as a Traefik forwardAuth compatibility configuration.": "Als Traefik-forwardAuth-Kompatibilitätskonfiguration validieren.",
    "Validate as an Envoy ext_authz compatibility configuration.": "Als Envoy-ext_authz-Kompatibilitätskonfiguration validieren.",
    "Validate as ordinary lighttpd proxy configuration.": "Als normale lighttpd-Proxy-Konfiguration validieren.",
    "When enabled, lighttpd validates the runtime file during set-defaults; validate host syntax with lighttpd -tt -f <config>.": "Bei Aktivierung validiert lighttpd die Runtime-Datei während set-defaults; Hostsyntax mit lighttpd -tt -f <config> validieren.",
    "apachectl -t": "apachectl -t",
    "haproxy -c -f <config>": "haproxy -c -f <config>",
    "lighttpd -tt -f <config>": "lighttpd -tt -f <config>",
    "main validates JSON and, where selected, Common Runtime before serving.": "main validiert JSON und, sofern ausgewählt, die Common Runtime vor dem Bereitstellen.",
    "normalizedConfig rejects invalid values; Traefik parses the containing dynamic configuration.": "normalizedConfig weist ungültige Werte ab; Traefik parst die enthaltende dynamische Konfiguration.",
    "traefik check --configFile=<static-config>; load the selected File Provider configuration.": "traefik check --configFile=<static-config>; die ausgewählte File-Provider-Konfiguration laden.",

    # P1–P4 explanations.
    "Compatibility path only; do not infer selected native P3/P4 coverage.": "Nur Kompatibilitätspfad; keine Abdeckung von P3/P4 des ausgewählten nativen Pfads ableiten.",
    "Compatibility request path; it is not a native HTX P3/P4 configuration.": "Kompatibilitäts-Requestpfad; keine native HTX-P3/P4-Konfiguration.",
    "Compatibility request/response-header path only; no native response-body lifecycle claim.": "Nur Kompatibilitäts-Request-/Response-Headerpfad; keine Aussage zum nativen Response-Body-Lebenszyklus.",
    "Host bootstrap only.": "Nur Host-Bootstrap.",
    "Host setup/routing/logging; it does not itself configure ModSecurity rule-engine phases.": "Hosteinrichtung/Routing/Logging; konfiguriert selbst keine Phasen der ModSecurity-Regel-Engine.",
    "Limits and late policy affect P1–P4 processor behavior.": "Limits und späte Policy beeinflussen das Prozessorverhalten in P1–P4.",
    "No native connector lifecycle claim.": "Keine Aussage zum nativen Connector-Lebenszyklus.",
    "No native mod_msconnector lifecycle claim.": "Keine Aussage zum Lebenszyklus von nativem mod_msconnector.",
    "No selected response-body P4 path.": "Kein ausgewählter P4-Pfad für den Response-Body.",
    "P1 controls integration; rules and P4 controls affect the stated phase only.": "P1 steuert die Integration; Regeln und P4-Steuerungen betreffen nur die genannte Phase.",
    "P1/P2/P3/P4 middleware callback bounds and engine connection behavior.": "Grenzen der P1/P2/P3/P4-Middleware-Callbacks und Verhalten der Engine-Verbindung.",
    "P1–P4 native HTX callbacks are attached only when this filter is declared.": "Native HTX-Callbacks für P1–P4 werden nur angehängt, wenn dieser Filter deklariert ist.",
    "P4 only. The current HTX host action distinguishes strict from non-strict; minimal and safe share the non-strict late log-only path.": "Nur P4. Die aktuelle HTX-Hostaktion unterscheidet strict von nicht-strict; minimal und safe teilen den späten nicht-strict-log_only-Pfad.",
    "P4 only. The response-body filter accumulates bounded in-scope bytes and finishes the engine at EOS (last_buf/last_in_chain); header/body commitment determines whether a status or only a late transport action remains possible.": "Nur P4. Der Response-Body-Filter sammelt begrenzte Bytes im Geltungsbereich und beendet die Engine bei EOS (last_buf/last_in_chain); das Committen von Headern/Body bestimmt, ob ein Status oder nur noch eine späte Transportaktion möglich ist.",
    "Request authorization compatibility path; no selected P3/P4 coverage.": "Kompatibilitätspfad für Request-Autorisierung; keine Abdeckung von ausgewähltem P3/P4.",
    "Request-authorization compatibility path; no selected P3/P4 configuration.": "Kompatibilitätspfad für Request-Autorisierung; keine ausgewählte P3/P4-Konfiguration.",
    "Rules can evaluate P1–P4 through the declared HTX filter.": "Regeln können P1–P4 über den deklarierten HTX-Filter auswerten.",
    "Runtime service setup; --runtime-config selects the actual engine path.": "Runtime-Serviceeinrichtung; --runtime-config wählt den tatsächlichen Engine-Pfad.",
    "See directive runtime effect.": "Siehe Laufzeitwirkung der Direktive.",
    "See runtime effect; body modes/limits affect P2 and P4, header limits affect P1 and P3.": "Siehe Laufzeitwirkung; Body-Modi/-Limits betreffen P2 und P4, Header-Limits betreffen P1 und P3.",
    "See runtime effect; ext_proc processing_mode and native middleware fields determine lifecycle visibility.": "Siehe Laufzeitwirkung; ext_proc-processing_mode und native Middleware-Felder bestimmen die Sichtbarkeit im Lebenszyklus.",
    "The referenced Common Runtime file chooses body modes and P1–P4 policy.": "Die referenzierte Common-Runtime-Datei wählt Body-Modi und die P1–P4-Policy.",
    "off disables the module P1/P3 callbacks and any patched P2/P4 callbacks.": "off deaktiviert die P1/P3-Callbacks des Moduls und alle gepatchten P2/P4-Callbacks.",

    # Detailed runtime effects.  These are intentionally complete sentences:
    # configuration references must explain the actual lifecycle behavior,
    # rather than merely replace English headings with German headings.
    "Adds inline rule configuration.": "Fügt eine Inline-Regelkonfiguration hinzu.",
    "Alias for event_path.": "Alias für event_path.",
    "Appends metadata-only JSONL events when configured.": "Hängt bei Konfiguration JSONL-Ereignisse an, die nur Metadaten enthalten.",
    "Before response headers/body are committed, minimal, safe, and strict all resolve a P4 intervention as deny_if_possible, so NGINX can still return the requested engine status (or 403 fallback). Once headers are committed or the body started, minimal and safe both use the common log_only action; they record the late decision without a later status rewrite. Strict instead resolves to abort_connection: the native body filter marks the connection as errored, records connection_aborted, and returns NGX_ERROR. The known host boundary is that NGINX invokes the P4 engine finish only at last_buf/last_in_chain after bounded in-scope body accumulation, so a response may already be visible. Strict can therefore terminate a connection, but cannot guarantee a later 403 or replace an already-sent status line.": "Bevor Response-Header/-Body committet sind, lösen minimal, safe und strict eine P4-Intervention jeweils als deny_if_possible auf; NGINX kann daher noch den angeforderten Engine-Status (oder den Fallback 403) zurückgeben. Sobald Header committet sind oder der Body begonnen hat, verwenden minimal und safe beide die gemeinsame Aktion log_only; sie protokollieren die späte Entscheidung ohne nachträgliche Statusumschreibung. Strict löst dagegen zu abort_connection auf: Der native Body-Filter markiert die Verbindung als fehlerhaft, protokolliert connection_aborted und gibt NGX_ERROR zurück. Die bekannte Hostgrenze ist, dass NGINX das P4-Engine-Finish erst bei last_buf/last_in_chain nach der begrenzten Sammlung von Body-Bytes im Geltungsbereich aufruft; eine Antwort kann deshalb bereits sichtbar sein. Strict kann somit eine Verbindung beenden, aber keine spätere 403 garantieren oder eine bereits gesendete Statuszeile ersetzen.",
    "Binds or targets one local TCP endpoint in the checked-in host template.": "Bindet oder adressiert einen lokalen TCP-Endpunkt im eingecheckten Host-Template.",
    "Bounds accepted header count.": "Begrenzt die akzeptierte Headeranzahl.",
    "Bounds each header-name size.": "Begrenzt die Größe jedes Headernamens.",
    "Bounds each header-value size.": "Begrenzt die Größe jedes Headerwerts.",
    "Bounds request bytes offered to the engine.": "Begrenzt die der Engine angebotenen Request-Bytes.",
    "Bounds response bytes offered to P4 processing by the native connector.": "Begrenzt die vom nativen Connector der P4-Verarbeitung angebotenen Response-Bytes.",
    "Bounds response bytes offered to the engine.": "Begrenzt die der Engine angebotenen Response-Bytes.",
    "Bounds serialized metadata event size.": "Begrenzt die Größe serialisierter Metadatenereignisse.",
    "Bounds the native middleware's streaming callbacks.": "Begrenzt die Streaming-Callbacks der nativen Middleware.",
    "Bounds total header bytes.": "Begrenzt die gesamte Header-Byteanzahl.",
    "Caps engine response-body input.": "Begrenzt die Response-Body-Eingabe der Engine.",
    "Compatibility host/service setup outside the selected native core path.": "Kompatibilitäts-Host-/Serviceeinrichtung außerhalb des ausgewählten nativen Kernpfads.",
    "Compatibility response control. The selected SPOE messages do not supply a response body, so this is not native P4 support.": "Kompatibilitäts-Response-Steuerung. Die ausgewählten SPOE-Nachrichten liefern keinen Response-Body; dies ist daher keine native P4-Unterstützung.",
    "Compatibility-only proxy routing.": "Proxy-Routing nur für die Kompatibilität.",
    "Configures the retained sidecar compatibility example.": "Konfiguriert das beibehaltene Sidecar-Kompatibilitätsbeispiel.",
    "Controls ext_proc service startup/check behavior.": "Steuert Start- und Prüfverhalten des ext_proc-Service.",
    "Controls fail-open versus fail-closed behavior for processor errors.": "Steuert Fail-open- gegenüber Fail-closed-Verhalten bei Prozessorfehlern.",
    "Controls forwarding of libmodsecurity messages to the host error log; it does not switch rule evaluation.": "Steuert die Weiterleitung von libmodsecurity-Meldungen an das Host-Fehlerlog; die Regelauswertung wird dadurch nicht umgeschaltet.",
    "Controls rule execution/disruptive action inside libmodsecurity, independently of the host connector switch.": "Steuert Regelausführung/disruptive Aktion innerhalb von libmodsecurity, unabhängig vom Hostconnector-Schalter.",
    "Controls whether an over-limit chunk is rejected or truncated before engine input.": "Steuert, ob ein Chunk über dem Limit vor der Engine-Eingabe abgewiesen oder gekürzt wird.",
    "Defines a ModSecurity rule such as the local RESPONSE_BODY P4 illustration.": "Definiert eine ModSecurity-Regel wie die lokale RESPONSE_BODY-P4-Illustration.",
    "Defines engine behavior when the response body exceeds the engine limit.": "Definiert das Engine-Verhalten, wenn der Response-Body das Engine-Limit überschreitet.",
    "During NGINX configuration loading, ngx_conf_set_rules_file passes the supplied path to libmodsecurity's msc_rules_add_file. The NGINX setter neither canonicalizes nor requires an absolute path; use an absolute path to avoid a process-working-directory dependency. A missing, unreadable, or invalid top-level rule file returns the libmodsecurity loader error and fails the configuration check/reload. Include and IncludeOptional inside that file are then interpreted by libmodsecurity, not expanded by the NGINX parser. Unlike modsecurity_rules, which sends one inline configuration string to msc_rules_add, this directive sends a file path to msc_rules_add_file; both contribute to the configured rule set and its normal parent/child merge.": "Beim Laden der NGINX-Konfiguration übergibt ngx_conf_set_rules_file den bereitgestellten Pfad an msc_rules_add_file von libmodsecurity. Der NGINX-Setter kanonisiert den Pfad nicht und verlangt keinen absoluten Pfad; ein absoluter Pfad vermeidet eine Abhängigkeit vom Arbeitsverzeichnis des Prozesses. Eine fehlende, unlesbare oder ungültige Regeldatei der obersten Ebene liefert den Loader-Fehler von libmodsecurity und lässt Konfigurationsprüfung/Reload fehlschlagen. Include und IncludeOptional in dieser Datei werden anschließend von libmodsecurity interpretiert, nicht durch den NGINX-Parser expandiert. Anders als modsecurity_rules, das eine Inline-Konfigurationszeichenkette an msc_rules_add sendet, übergibt diese Direktive einen Dateipfad an msc_rules_add_file; beide tragen zum konfigurierten Regelsatz und seinem normalen Eltern-/Kind-Merge bei.",
    "Enables engine request-body access for P2 when the host supplies the body.": "Aktiviert den Engine-Zugriff auf den Request-Body für P2, wenn der Host den Body bereitstellt.",
    "Enables engine response-body access for P4 when the host supplies in-scope bytes.": "Aktiviert den Engine-Zugriff auf den Response-Body für P4, wenn der Host Bytes im Geltungsbereich bereitstellt.",
    "Enables the Common Runtime; enabled runtime requires an inline, file, or remote rule source.": "Aktiviert die Common Runtime; eine aktivierte Runtime benötigt eine Inline-, Datei- oder Remote-Regelquelle.",
    "Enables the selected audit-log policy.": "Aktiviert die ausgewählte Audit-Log-Policy.",
    "Evaluates an Apache expression per request for the transaction identifier.": "Wertet pro Request einen Apache-Ausdruck für die Transaktionskennung aus.",
    "Fallback status for runtime errors.": "Fallback-Status für Runtime-Fehler.",
    "Fallback status for supported pre-commit block actions.": "Fallback-Status für unterstützte Sperraktionen vor dem Commit.",
    "Gates connector transaction creation; it is not SecRuleEngine.": "Schaltet die Erstellung von Connector-Transaktionen frei; dies ist nicht SecRuleEngine.",
    "Initialises common_config.phase4_mode for the filter.": "Initialisiert common_config.phase4_mode für den Filter.",
    "Loads a local rule file through libmodsecurity during configuration loading.": "Lädt während des Konfigurationsladens eine lokale Regeldatei über libmodsecurity.",
    "Loads and creates the connector-neutral runtime before requests are served.": "Lädt und erzeugt die connectorneutrale Runtime, bevor Requests bedient werden.",
    "Loads inline content through libmodsecurity during configuration loading.": "Lädt während des Konfigurationsladens Inline-Inhalt über libmodsecurity.",
    "Loads optional engine configuration/rules if present.": "Lädt optionale Engine-Konfiguration/Regeln, sofern vorhanden.",
    "Loads rules from a local file.": "Lädt Regeln aus einer lokalen Datei.",
    "Loads rules with msc_rules_add_file during filter initialisation.": "Lädt bei der Filterinitialisierung Regeln mit msc_rules_add_file.",
    "Names the private UDS path used by native middleware when engineMode is uds.": "Benennt den privaten UDS-Pfad, den die native Middleware bei engineMode=uds verwendet.",
    "Passes the key/URL pair to libmodsecurity's remote-rule loader.": "Übergibt das Schlüssel-/URL-Paar an den Remote-Regel-Loader von libmodsecurity.",
    "Provides surrounding host setup used by the selected connector example.": "Stellt die umgebende Hosteinrichtung bereit, die vom ausgewählten Connector-Beispiel verwendet wird.",
    "Registers the repository's native HTX filter and creates the config passed to the lifecycle callbacks.": "Registriert den nativen HTX-Filter des Repositorys und erzeugt die an die Lebenszyklus-Callbacks übergebene Konfiguration.",
    "Retained solely to explain retired compatibility material.": "Nur zur Erklärung außer Dienst gestellten Kompatibilitätsmaterials beibehalten.",
    "Routes to separate authorization compatibility service.": "Leitet an den separaten Autorisierungs-Kompatibilitätsservice weiter.",
    "Routes to separate authorization service.": "Leitet an den separaten Autorisierungsservice weiter.",
    "Routes to the separate SPOE/SPOP compatibility service.": "Leitet an den separaten SPOE/SPOP-Kompatibilitätsservice weiter.",
    "SPOP compatibility-agent configuration; it is not a native HTX filter option.": "SPOP-Kompatibilitätsagent-Konfiguration; dies ist keine native HTX-Filteroption.",
    "Scopes P4 response-body inspection to configured MIME types.": "Beschränkt die P4-Response-Body-Inspektion auf konfigurierte MIME-Typen.",
    "Scopes engine response-body inspection by MIME type.": "Beschränkt die Engine-Response-Body-Inspektion nach MIME-Typ.",
    "Selects audit-log parts.": "Wählt Audit-Log-Teile aus.",
    "Selects body visibility for ext_proc. The repository Common bridge requires STREAMED for both directions in the selected full-lifecycle path.": "Wählt die Body-Sichtbarkeit für ext_proc. Die Common-Bridge des Repositorys verlangt im ausgewählten Full-Lifecycle-Pfad STREAMED für beide Richtungen.",
    "Selects host listener, routing, filter, service, or logging setup from the checked-in example.": "Wählt Listener-, Routing-, Filter-, Service- oder Logging-Einrichtung des eingecheckten Beispiels.",
    "Selects late decision reporting; minimal and safe record late disruptive decisions as log_only, while strict records strict_abort_not_attempted rather than a fabricated status/reset.": "Wählt die Protokollierung später Entscheidungen; minimal und safe erfassen späte disruptive Entscheidungen als log_only, während strict strict_abort_not_attempted statt eines erfundenen Status/Resets erfasst.",
    "Selects source-only passthrough or the persistent UDS engine; the selected rule-evaluating example uses uds.": "Wählt source-only-passthrough oder die persistente UDS-Engine; das ausgewählte regelauswertende Beispiel verwendet uds.",
    "Selects the Common request-body handling mode; a particular host may support only a subset.": "Wählt den Common-Modus zur Request-Body-Verarbeitung; ein bestimmter Host unterstützt möglicherweise nur eine Teilmenge.",
    "Selects the Common response-body handling mode; a particular host may support only a subset.": "Wählt den Common-Modus zur Response-Body-Verarbeitung; ein bestimmter Host unterstützt möglicherweise nur eine Teilmenge.",
    "Selects the fallback correlation-header name.": "Wählt den Fallback-Namen des Korrelations-Headers.",
    "Selects the requested late P4 policy. Before response commit a deny can be applied; after commit the current Apache/NGINX/HTX paths distinguish strict from non-strict only. Minimal and safe therefore share the current non-strict log-only path.": "Wählt die angeforderte späte P4-Policy. Vor dem Response-Commit kann ein deny angewendet werden; nach dem Commit unterscheiden die aktuellen Apache-/NGINX-/HTX-Pfade nur strict von nicht-strict. Minimal und safe teilen daher den aktuellen nicht-strict-log_only-Pfad.",
    "Selects whether ext_proc receives request or response headers.": "Wählt, ob ext_proc Request- oder Response-Header empfängt.",
    "Selects whether mod_msconnector initialises Common Runtime.": "Wählt, ob mod_msconnector die Common Runtime initialisiert.",
    "Sends trailers/EOS metadata to the ext_proc service.": "Sendet Trailer-/EOS-Metadaten an den ext_proc-Service.",
    "Sets a connector event path; current Apache and NGINX paths also use it for earlier rule/intervention metadata, not only P4.": "Setzt einen Connector-Ereignispfad; aktuelle Apache- und NGINX-Pfade verwenden ihn auch für frühere Regel-/Interventionsmetadaten, nicht nur für P4.",
    "Sets a static runtime transaction identifier.": "Setzt eine statische Runtime-Transaktionskennung.",
    "Sets one bounded ext_proc service control.": "Setzt eine begrenzte ext_proc-Service-Steuerung.",
    "Sets the engine audit-log path.": "Setzt den Engine-Audit-Log-Pfad.",
    "Sets the selected audit-log write mode.": "Setzt den ausgewählten Schreibmodus für das Audit-Log.",
    "Stores a content-type file path; consumption is connector-specific.": "Speichert einen Content-Type-Dateipfad; die Verwendung ist connectorspezifisch.",
    "Stores an optional late-intervention budget; Common owns no timer/cancellation primitive.": "Speichert ein optionales Budget für späte Interventionen; Common besitzt keine Timer-/Abbruchprimitive.",
    "Stores the Common logging preference. A connector must consume it before a host logging effect can be claimed.": "Speichert die Common-Logging-Präferenz. Ein Connector muss sie verwenden, bevor eine Logging-Wirkung beim Host behauptet werden kann.",
    "Stores the late P4 policy. Common alone owns no host abort primitive.": "Speichert die späte P4-Policy. Common allein besitzt keine Host-Abbruchprimitive.",
    "Supplies a release marker or local endpoint value to the generated Envoy configuration.": "Liefert der erzeugten Envoy-Konfiguration einen Release-Marker oder lokalen Endpunktwert.",
    "Supplies one half of a remote-rule pair.": "Liefert eine Hälfte eines Remote-Regelpaares.",
    "Supplies the engine and event correlation identifier for a transaction.": "Liefert die Engine- und Ereigniskorrelationskennung für eine Transaktion.",
    "Supplies the remote-rule endpoint; the selected examples do not exercise it.": "Liefert den Remote-Regelendpunkt; die ausgewählten Beispiele verwenden ihn nicht.",

    # Security and operational guidance.
    "A larger limit raises memory/CPU exposure; zero is invalid in the native setters.": "Ein größeres Limit erhöht die Speicher-/CPU-Exposition; null ist in den nativen Settern ungültig.",
    "A stock HAProxy binary does not provide this keyword; do not silently substitute SPOE.": "Ein ungepatchtes HAProxy-Binärprogramm bietet dieses Schlüsselwort nicht; SPOE nicht stillschweigend ersetzen.",
    "Body visibility increases resource and data-handling exposure; retain explicit limits.": "Body-Sichtbarkeit erhöht die Ressourcen- und Datenverarbeitungs-Exposition; explizite Limits beibehalten.",
    "Bound all header, body, gRPC, and timeout values; keep service listen address private.": "Alle Header-, Body-, gRPC- und Timeout-Werte begrenzen; die Listen-Adresse des Service privat halten.",
    "Compatibility logs, ports, rules, and fail policy require operator review; do not promote this path to the selected native core.": "Kompatibilitätslogs, Ports, Regeln und Fail-Policy benötigen eine Betreiberprüfung; diesen Pfad nicht zum ausgewählten nativen Kern hochstufen.",
    "Compatibility-only host routing; do not represent it as native ModSecurity configuration.": "Host-Routing nur für die Kompatibilität; nicht als native ModSecurity-Konfiguration darstellen.",
    "Compatibility-only setting. Do not promote it as selected native full-lifecycle configuration.": "Einstellung nur für die Kompatibilität. Nicht als ausgewählte native Full-Lifecycle-Konfiguration darstellen.",
    "Disabling the module bypasses connector processing even if a rule file exists.": "Das Deaktivieren des Moduls umgeht die Connector-Verarbeitung, auch wenn eine Regeldatei existiert.",
    "Do not present forwardAuth as the native UDS rule-evaluating path.": "forwardAuth nicht als nativen UDS-Pfad zur Regelauswertung darstellen.",
    "Do not promote this historical path as the selected native core.": "Diesen historischen Pfad nicht als ausgewählten nativen Kern hochstufen.",
    "Do not put credentials or sensitive request data in a correlation identifier.": "Keine Zugangsdaten oder sensiblen Request-Daten in eine Korrelationskennung aufnehmen.",
    "Do not represent it as the native ext_proc full-lifecycle configuration.": "Nicht als native ext_proc-Full-Lifecycle-Konfiguration darstellen.",
    "Do not treat a proxy endpoint as a configured native ModSecurity integration.": "Einen Proxy-Endpunkt nicht als konfigurierte native ModSecurity-Integration behandeln.",
    "Engine policy can inspect, log, detect, or disrupt traffic; protect rule and audit-log paths.": "Die Engine-Policy kann Traffic inspizieren, protokollieren, erkennen oder unterbrechen; Regel- und Audit-Log-Pfade schützen.",
    "Error logs can contain security metadata; protect and rotate them.": "Fehlerlogs können Sicherheitsmetadaten enthalten; sie schützen und rotieren.",
    "Inline rules are executable policy; restrict who may alter host configuration.": "Inline-Regeln sind ausführbare Policy; einschränken, wer die Hostkonfiguration ändern darf.",
    "Keep listener, upstream, and administrative endpoints private unless an explicit deployment design authorizes exposure.": "Listener-, Upstream- und administrative Endpunkte privat halten, sofern kein ausdrückliches Deployment-Design ihre Freigabe autorisiert.",
    "Keep the file and parent directories non-writable by untrusted identities.": "Die Datei und ihre übergeordneten Verzeichnisse für nicht vertrauenswürdige Identitäten nicht schreibbar halten.",
    "Keep the file, its parent directories, and any engine-included files non-writable by untrusted identities. Prefer an absolute path so a changed working directory cannot select unintended policy.": "Die Datei, ihre übergeordneten Verzeichnisse und alle von der Engine eingebundenen Dateien für nicht vertrauenswürdige Identitäten nicht schreibbar halten. Einen absoluten Pfad bevorzugen, damit ein geändertes Arbeitsverzeichnis keine unbeabsichtigte Policy wählen kann.",
    "Keep the scope narrow and validate that the host exposes the intended representation of response bytes.": "Den Geltungsbereich eng halten und validieren, dass der Host die beabsichtigte Repräsentation der Response-Bytes bereitstellt.",
    "Limits bound resource use. Adds inline rule configuration.": "Limits begrenzen den Ressourcenverbrauch. Fügt eine Inline-Regelkonfiguration hinzu.",
    "Limits bound resource use. Alias for event_path.": "Limits begrenzen den Ressourcenverbrauch. Alias für event_path.",
    "Limits bound resource use. Appends metadata-only JSONL events when configured.": "Limits begrenzen den Ressourcenverbrauch. Hängt bei Konfiguration JSONL-Ereignisse an, die nur Metadaten enthalten.",
    "Limits bound resource use. Bounds accepted header count.": "Limits begrenzen den Ressourcenverbrauch. Begrenzt die akzeptierte Headeranzahl.",
    "Limits bound resource use. Bounds each header-name size.": "Limits begrenzen den Ressourcenverbrauch. Begrenzt die Größe jedes Headernamens.",
    "Limits bound resource use. Bounds each header-value size.": "Limits begrenzen den Ressourcenverbrauch. Begrenzt die Größe jedes Headerwerts.",
    "Limits bound resource use. Bounds request bytes offered to the engine.": "Limits begrenzen den Ressourcenverbrauch. Begrenzt die der Engine angebotenen Request-Bytes.",
    "Limits bound resource use. Bounds response bytes offered to the engine.": "Limits begrenzen den Ressourcenverbrauch. Begrenzt die der Engine angebotenen Response-Bytes.",
    "Limits bound resource use. Bounds serialized metadata event size.": "Limits begrenzen den Ressourcenverbrauch. Begrenzt die Größe serialisierter Metadatenereignisse.",
    "Limits bound resource use. Bounds total header bytes.": "Limits begrenzen den Ressourcenverbrauch. Begrenzt die gesamte Header-Byteanzahl.",
    "Limits bound resource use. Controls whether an over-limit chunk is rejected or truncated before engine input.": "Limits begrenzen den Ressourcenverbrauch. Steuert, ob ein Chunk über dem Limit vor der Engine-Eingabe abgewiesen oder gekürzt wird.",
    "Limits bound resource use. Enables the Common Runtime; enabled runtime requires an inline, file, or remote rule source.": "Limits begrenzen den Ressourcenverbrauch. Aktiviert die Common Runtime; eine aktivierte Runtime benötigt eine Inline-, Datei- oder Remote-Regelquelle.",
    "Limits bound resource use. Fallback status for runtime errors.": "Limits begrenzen den Ressourcenverbrauch. Fallback-Status für Runtime-Fehler.",
    "Limits bound resource use. Fallback status for supported pre-commit block actions.": "Limits begrenzen den Ressourcenverbrauch. Fallback-Status für unterstützte Sperraktionen vor dem Commit.",
    "Limits bound resource use. Loads rules from a local file.": "Limits begrenzen den Ressourcenverbrauch. Lädt Regeln aus einer lokalen Datei.",
    "Limits bound resource use. Selects the Common request-body handling mode; a particular host may support only a subset.": "Limits begrenzen den Ressourcenverbrauch. Wählt den Common-Modus zur Request-Body-Verarbeitung; ein bestimmter Host unterstützt möglicherweise nur eine Teilmenge.",
    "Limits bound resource use. Selects the Common response-body handling mode; a particular host may support only a subset.": "Limits begrenzen den Ressourcenverbrauch. Wählt den Common-Modus zur Response-Body-Verarbeitung; ein bestimmter Host unterstützt möglicherweise nur eine Teilmenge.",
    "Limits bound resource use. Selects the fallback correlation-header name.": "Limits begrenzen den Ressourcenverbrauch. Wählt den Fallback-Namen des Korrelations-Headers.",
    "Limits bound resource use. Sets a static runtime transaction identifier.": "Limits begrenzen den Ressourcenverbrauch. Setzt eine statische Runtime-Transaktionskennung.",
    "Limits bound resource use. Stores a content-type file path; consumption is connector-specific.": "Limits begrenzen den Ressourcenverbrauch. Speichert einen Content-Type-Dateipfad; die Verwendung ist connectorspezifisch.",
    "Limits bound resource use. Stores an optional late-intervention budget; Common owns no timer/cancellation primitive.": "Limits begrenzen den Ressourcenverbrauch. Speichert ein optionales Budget für späte Interventionen; Common besitzt keine Timer-/Abbruchprimitive.",
    "Limits bound resource use. Stores the Common logging preference. A connector must consume it before a host logging effect can be claimed.": "Limits begrenzen den Ressourcenverbrauch. Speichert die Common-Logging-Präferenz. Ein Connector muss sie verwenden, bevor eine Logging-Wirkung beim Host behauptet werden kann.",
    "Limits bound resource use. Stores the late P4 policy. Common alone owns no host abort primitive.": "Limits begrenzen den Ressourcenverbrauch. Speichert die späte P4-Policy. Common allein besitzt keine Host-Abbruchprimitive.",
    "Limits bound resource use. Supplies one half of a remote-rule pair.": "Limits begrenzen den Ressourcenverbrauch. Liefert eine Hälfte eines Remote-Regelpaares.",
    "Limits bound resource use. Supplies the remote-rule endpoint; the selected examples do not exercise it.": "Limits begrenzen den Ressourcenverbrauch. Liefert den Remote-Regelendpunkt; die ausgewählten Beispiele verwenden ihn nicht.",
    "Limits protect resource use; UDS requires a private socket path.": "Limits schützen den Ressourcenverbrauch; UDS verlangt einen privaten Socket-Pfad.",
    "Network addresses, paths, and logging destinations must be selected and access-controlled by the operator.": "Netzwerkadressen, Pfade und Logging-Ziele müssen durch den Betreiber gewählt und zugriffsgesteuert werden.",
    "Never use as P4 or strict-abort evidence.": "Niemals als Nachweis für P4 oder einen strict-Abbruch verwenden.",
    "Protect policy-file ownership and permissions.": "Eigentümerschaft und Berechtigungen der Policy-Datei schützen.",
    "Remote policy is not exercised by the selected no-CRS examples; do not treat it as a local-file substitute.": "Remote-Policy wird von den ausgewählten no-CRS-Beispielen nicht verwendet; nicht als Ersatz für eine lokale Datei behandeln.",
    "The runtime file contains executable rule paths and limits; use trusted ownership and permissions.": "Die Runtime-Datei enthält ausführbare Regelpfade und Limits; vertrauenswürdige Eigentümerschaft und Berechtigungen verwenden.",
    "Treat JSONL metadata as sensitive operational data and set safe ownership/rotation.": "JSONL-Metadaten als sensible Betriebsdaten behandeln und sichere Eigentümerschaft/Rotation festlegen.",
    "Treat expression inputs as metadata; avoid exposing secrets in logs.": "Ausdruckseingaben als Metadaten behandeln; Geheimnisse nicht in Logs offenlegen.",
    "Use absolute controlled paths for runtime/event files and a private service listener.": "Absolute kontrollierte Pfade für Runtime-/Ereignisdateien und einen privaten Service-Listener verwenden.",
    "Use private, non-conflicting ports; never place generated runtime output in the checkout.": "Private, konfliktfreie Ports verwenden; erzeugte Runtime-Ausgabe nie im Checkout ablegen.",
    "false avoids silently allowing traffic when processor communication fails.": "false verhindert, dass Traffic bei fehlgeschlagener Prozessor-Kommunikation stillschweigend erlaubt wird.",
    "off bypasses connector P1–P4 processing even if a rule file is configured.": "off umgeht die Connector-Verarbeitung P1–P4, auch wenn eine Regeldatei konfiguriert ist.",
    "safe/minimal retain late-decision evidence without interrupting an already-started response. strict requests a connection abort after commit, which can expose clients to a partial response; it is not a reliable post-commit HTTP-status enforcement mode.": "safe/minimal bewahren Nachweise später Entscheidungen, ohne eine bereits gestartete Antwort zu unterbrechen. strict fordert nach dem Commit einen Verbindungsabbruch an, der Clients einer Teilantwort aussetzen kann; dies ist kein verlässlicher Modus zur Durchsetzung eines HTTP-Status nach dem Commit.",
    "strict must not be described as a guaranteed later 403; host-specific abort evidence is required.": "strict darf nicht als garantierte spätere 403 beschrieben werden; hostspezifische Nachweise für den Abbruch sind erforderlich.",
    "strict records an abort policy request but the native HTX path currently records host action not_attempted; it is not an abort guarantee.": "strict protokolliert eine Policy-Anforderung zum Abbruch, aber der native HTX-Pfad protokolliert derzeit die Hostaktion not_attempted; dies ist keine Abbruchgarantie.",

    # Further source-backed Engine details.  These are kept alongside the
    # connector metadata so updates to the actual rule examples cannot leave
    # their German companion with an English explanation.
    "NGX_HTTP_MAIN_CONF (http), NGX_HTTP_SRV_CONF (server), NGX_HTTP_LOC_CONF (location)": "NGX_HTTP_MAIN_CONF (http), NGX_HTTP_SRV_CONF (server), NGX_HTTP_LOC_CONF (location)",
    "T_CONFIG_SCOPE_SERVER": "T_CONFIG_SCOPE_SERVER",
    "http.middlewares.<name>.plugin.modsecurityNative": "http.middlewares.<name>.plugin.modsecurityNative",
    "nginx -t": "nginx -t",
    "ngx_conf_set_phase4_mode accepts only minimal|safe|strict during nginx -t. Runtime late behavior is source-defined: non-strict post-commit paths emit log_only; strict marks the connection errored and returns NGX_ERROR, without manufacturing a later 403.": "ngx_conf_set_phase4_mode akzeptiert während nginx -t nur minimal|safe|strict. Das späte Runtime-Verhalten ist quellendefiniert: Nicht-strict-Pfade nach dem Commit geben log_only aus; strict markiert die Verbindung als fehlerhaft und gibt NGX_ERROR zurück, ohne eine spätere 403 zu erfinden.",
    "ngx_conf_set_rules_file calls msc_rules_add_file while nginx -t/configuration loading runs. A missing, unreadable, or syntactically invalid top-level rule file (including an engine Include failure) returns the loader error and rejects the NGINX configuration.": "ngx_conf_set_rules_file ruft msc_rules_add_file während nginx -t/des Konfigurationsladens auf. Eine fehlende, unlesbare oder syntaktisch ungültige Regeldatei der obersten Ebene (einschließlich eines fehlgeschlagenen Engine-Include) liefert den Loader-Fehler und weist die NGINX-Konfiguration ab.",
    "The host/libmodsecurity rejects invalid engine syntax when loading the rule file. A syntactically valid On still cannot create P2 input when the selected host path does not expose a request body.": "Der Host/libmodsecurity weist beim Laden der Regeldatei ungültige Engine-Syntax ab. Ein syntaktisch gültiges On kann dennoch keine P2-Eingabe erzeugen, wenn der ausgewählte Hostpfad keinen Request-Body bereitstellt.",
    "The host/libmodsecurity rejects invalid engine syntax when loading the rule file. At runtime, an out-of-scope MIME type, disabled host body path, or exceeded limit can leave P4 without the expected complete body input.": "Der Host/libmodsecurity weist beim Laden der Regeldatei ungültige Engine-Syntax ab. Zur Laufzeit können ein MIME-Typ außerhalb des Geltungsbereichs, ein deaktivierter Host-Body-Pfad oder ein überschrittenes Limit P4 ohne die erwartete vollständige Body-Eingabe lassen.",
    "The host/libmodsecurity rejects malformed variable/operator/action syntax, duplicate or invalid identifiers, and invalid action combinations when loading the rule file.": "Der Host/libmodsecurity weist beim Laden der Regeldatei fehlerhafte Variablen-/Operator-/Action-Syntax, doppelte oder ungültige Kennungen und ungültige Action-Kombinationen ab.",
    "P2. On permits body inspection only after the connector has supplied request bytes; the selected host/runtime body mode and limit determine how many bytes can reach the engine.": "P2. On erlaubt Body-Inspektion erst, nachdem der Connector Request-Bytes bereitgestellt hat; ausgewählter Host-/Runtime-Body-Modus und Limit bestimmen, wie viele Bytes die Engine erreichen können.",
    "P4. On is necessary but not sufficient: the connector must expose response bytes, the MIME type must be in SecResponseBodyMimeType scope, and host/engine response limits apply.": "P4. On ist notwendig, aber nicht hinreichend: Der Connector muss Response-Bytes bereitstellen, der MIME-Typ muss im Geltungsbereich von SecResponseBodyMimeType liegen, und Host-/Engine-Response-Limits gelten.",
    "The phase action selects the evaluation point; the local RESPONSE_BODY example uses P4. A disruptive action can affect the visible HTTP result only while the host can still intervene.": "Die Phasen-Action wählt den Auswertungspunkt; das lokale RESPONSE_BODY-Beispiel verwendet P4. Eine disruptive Action kann das sichtbare HTTP-Ergebnis nur beeinflussen, solange der Host noch eingreifen kann.",
    "Request bodies may contain credentials or personal data. Use bounded body limits, appropriate MIME/parser policy, and protected audit/debug logs; no performance quantity is inferred here.": "Request-Bodys können Zugangsdaten oder personenbezogene Daten enthalten. Begrenzte Body-Limits, passende MIME-/Parser-Policy und geschützte Audit-/Debug-Logs verwenden; hier wird keine Leistungskennzahl abgeleitet.",
    "Response bodies can be large and sensitive. Keep MIME scope and response limits narrow, protect logs, and do not equate safe post-commit evidence with a client-visible later 403.": "Response-Bodys können groß und sensibel sein. MIME-Geltungsbereich und Response-Limits eng halten, Logs schützen und sichere Nachweise nach dem Commit nicht mit einer für Clients sichtbaren späteren 403 gleichsetzen.",
    "Rules are executable security policy. Give each rule a stable id, keep transformations explicit and minimal, protect rule-file ownership, and verify disruptive/redirect behavior on the selected host before relying on it.": "Regeln sind ausführbare Sicherheits-Policy. Jeder Regel eine stabile id geben, Transformationen explizit und minimal halten, Eigentümerschaft der Regeldatei schützen und disruptives/Redirect-Verhalten auf dem ausgewählten Host prüfen, bevor man sich darauf verlässt.",
    "Defines a rule from a variable, operator, and comma-separated actions. The local illustration uses RESPONSE_BODY, @contains, id, phase, deny, log, and status; redirect and transformations are separate action forms whose validity and observable effect remain engine/host- and commit-boundary dependent.": "Definiert eine Regel aus Variable, Operator und durch Komma getrennten Actions. Die lokale Illustration verwendet RESPONSE_BODY, @contains, id, phase, deny, log und status; redirect und Transformationen sind separate Action-Formen, deren Gültigkeit und beobachtbare Wirkung von Engine/Host und Commit-Grenze abhängen.",
    "On makes P4 possible only when the host supplies response bytes that are in scope; Off removes response-body input from P4. It does not widen SecResponseBodyMimeType, override SecResponseBodyLimit/SecResponseBodyLimitAction, or force a status change after headers commit. With the selected safe late-intervention policy, a post-commit disruptive result is recorded as log_only rather than a promised later 403; response capture can add bounded memory, CPU, and sensitive-data exposure.": "On ermöglicht P4 nur, wenn der Host Response-Bytes im Geltungsbereich bereitstellt; Off entfernt die Response-Body-Eingabe aus P4. Es erweitert SecResponseBodyMimeType nicht, überschreibt SecResponseBodyLimit/SecResponseBodyLimitAction nicht und erzwingt keine Statusänderung nach dem Header-Commit. Mit der ausgewählten sicheren Late-Intervention-Policy wird ein disruptives Ergebnis nach dem Commit als log_only statt als versprochene spätere 403 protokolliert; das Erfassen der Response kann begrenzte Speicher-, CPU- und Sensitivdaten-Exposition hinzufügen.",
    "On makes request-body input available to engine P2 only when the host supplies it; Off leaves P1 headers available but removes body input from P2. The directive itself sets neither a body-size limit nor a request MIME scope: those remain host/engine mapping choices and, where selected, Common Runtime request_body_limit/body mode controls. Enabling body handling can add buffering, memory, CPU, and logging exposure, so retain bounded host input.": "On stellt der Engine P2 eine Request-Body-Eingabe nur bereit, wenn der Host sie liefert; Off lässt P1-Header verfügbar, entfernt aber die Body-Eingabe aus P2. Die Direktive setzt weder ein Body-Größenlimit noch einen Request-MIME-Geltungsbereich: Diese bleiben Zuordnungsentscheidungen von Host/Engine und, sofern ausgewählt, Steuerungen über Common-Runtime-request_body_limit/Body-Modus. Das Aktivieren der Body-Verarbeitung kann Buffering-, Speicher-, CPU- und Logging-Exposition hinzufügen; daher Hosteingaben begrenzen.",
    "Compatibility-only SPOE filter.": "SPOE-Filter nur für die Kompatibilität.",
    "Compatibility-only ext_authz filter.": "ext_authz-Filter nur für die Kompatibilität.",
    "Compatibility-only forwardAuth middleware.": "forwardAuth-Middleware nur für die Kompatibilität.",
    "Compatibility-only lighttpd host field.": "lighttpd-Hostfeld nur für die Kompatibilität.",
    "Compatibility-only sidecar proxy setup.": "Sidecar-Proxy-Einrichtung nur für die Kompatibilität.",
    "Disabled historical compatibility material.": "Deaktiviertes historisches Kompatibilitätsmaterial.",
    "Enables the native lighttpd plugin.": "Aktiviert das native lighttpd-Plugin.",
    "Host-owned setting appearing in the checked-in example; it is not a connector directive.": "Hosteigenes Feld im eingecheckten Beispiel; keine Connector-Direktive.",
    "Native HTX full-lifecycle filter declaration.": "Native HTX-Filterdeklaration für den vollständigen Lebenszyklus.",
    "Native HTX late-P4 policy argument.": "Native HTX-Argument für die späte P4-Policy.",
    "Path to the Common Runtime configuration used by the native plugin.": "Pfad zur Common-Runtime-Konfiguration, die das native Plugin verwendet.",
    "Required native HTX rule-file argument.": "Erforderliches rules-file-Argument des nativen HTX.",
    "Template placeholder, not an Envoy configuration field.": "Template-Platzhalter, kein Envoy-Konfigurationsfeld.",
    "ext_proc service CLI flag.": "Kommandozeilenoption des ext_proc-Service.",
    "deprecated path": "veralteter Pfad",
    "one readable legacy file with MIME tokens": "eine lesbare Legacy-Datei mit MIME-Token",
    "none; deprecated Apache compatibility input": "kein Wert; veraltete Apache-Kompatibilitätseingabe",
    "Apache compatibility parser; deprecated": "Apache-Kompatibilitätsparser; veraltet",
    "Apache retains every normalized response brigade through first EOS and resolves the normal P4 decision before original output release. This mode selects only the defensive fallback for independently proven already-committed output: minimal/safe record log_only and strict requests abort_connection.": "Apache hält jede normalisierte Response-Brigade bis zum ersten EOS zurück und löst die normale P4-Entscheidung vor der Freigabe der ursprünglichen Ausgabe auf. Dieser Modus wählt nur den defensiven Fallback für unabhängig als bereits committed nachgewiesene Ausgabe: minimal/safe zeichnen log_only auf und strict fordert abort_connection an.",
    "A normal Phase-4 deny must not be reinterpreted as log_only: Apache discards the saved original brigade and emits one terminal error before release. strict is not a guaranteed later 403; host-specific abort evidence is still required.": "Ein normaler Phase-4-Deny darf nicht als log_only umgedeutet werden: Apache verwirft die gespeicherte ursprüngliche Brigade und gibt vor dem Release genau einen terminalen Fehler aus. strict ist keine garantierte spätere 403; hostspezifische Abort-Evidence ist weiterhin erforderlich.",
    "P4 only. Apache's EOS-only all-response gate resolves intervention before original output release; this setting applies only if independent commit proof already exists.": "Nur P4. Apaches EOS-only-All-Response-Gate löst die Intervention vor der Freigabe der ursprünglichen Ausgabe auf; diese Einstellung gilt nur, wenn ein unabhängiger Commit-Nachweis bereits existiert.",
    "Deprecated Apache compatibility parser for a legacy MIME list. It does not narrow the all-response Phase-4 gate; use SecResponseBodyMimeType to select libModSecurity inspection.": "Veralteter Apache-Kompatibilitätsparser für eine Legacy-MIME-Liste. Er schränkt das All-Response-Phase-4-Gate nicht ein; SecResponseBodyMimeType wählt die libModSecurity-Inspektion.",
    "Do not use this legacy list to permit a pass-through route. The connector cannot safely query libModSecurity's effective MIME selection, so every response remains gated through EOS.": "Diese Legacy-Liste darf keinen Pass-through-Pfad erlauben. Der Connector kann die wirksame MIME-Auswahl von libModSecurity nicht sicher abfragen, daher bleibt jede Response bis EOS gegatet.",
    "P4 only. The parser is retained for compatibility but cannot select which Apache responses bypass the EOS-only enforcement gate.": "Nur P4. Der Parser bleibt aus Kompatibilitätsgründen erhalten, kann aber nicht auswählen, welche Apache-Responses das EOS-only-Enforcement-Gate umgehen.",
    "Bounds Apache's saved all-response brigade before Phase-4 completion. The configurable default is 1048576 bytes; independently, a fixed non-configurable 4096-normalized-bucket ceiling applies across filter calls. An over-byte-limit or over-bucket-limit response fails closed before any original response byte is released.": "Begrenzt Apaches gespeicherte All-Response-Brigade vor dem Phase-4-Abschluss. Der konfigurierbare Standardwert ist 1048576 Byte; unabhängig davon gilt über Filter-Aufrufe hinweg eine feste, nicht konfigurierbare Obergrenze von 4096 normalisierten Buckets. Eine Response über dem Byte- oder Bucket-Limit schlägt fail-closed fehl, bevor ein ursprüngliches Response-Byte freigegeben wird.",
    "The byte and fixed bucket ceilings bound payload and retained APR-object/setaside memory/CPU exposure. Do not process a prefix and release an uninspected tail: exceeding either connector limit must fail closed.": "Die Byte- und feste Bucket-Obergrenze begrenzen Payload- sowie zurückgehaltene APR-Objekt-/Setaside-Speicher-/CPU-Exposition. Keinen Präfix verarbeiten und einen uninspektierten Tail freigeben: Das Überschreiten einer der Connector-Grenzen muss fail-closed fehlschlagen.",
    "P4 only. The byte limit and the fixed bucket ceiling apply while normalized brigades are retained through first EOS for the all-response enforcement decision; the bucket count spans filter calls and resets on release or discard.": "Nur P4. Das Byte-Limit und die feste Bucket-Obergrenze gelten, während normalisierte Brigades für die All-Response-Enforcement-Entscheidung bis zum ersten EOS zurückgehalten werden; der Bucket-Zähler gilt über Filter-Aufrufe hinweg und wird bei Release oder Discard zurückgesetzt.",
}


def _german_text(value: str) -> str:
    """Return the German rendering of explanatory metadata.

    Technical values that must remain byte-for-byte recognizable (for example
    ``safe``, ``STREAMED``, a source symbol, or a configuration path) are not
    explicitly identity-mapped.  Parameterized parser diagnostics use a
    small set of grammar-preserving templates so a changed handler name does
    not silently reintroduce English prose.
    """
    if value in GERMAN_TEXT:
        return GERMAN_TEXT[value]
    apache = re.fullmatch(
        r"([a-z0-9_]+) returns an Apache configuration error for its documented invalid input; "
        r"validate the installed configuration with apachectl -t\.",
        value,
    )
    if apache:
        return (
            f"{apache.group(1)} liefert für die dokumentierte ungültige Eingabe "
            "einen Apache-Konfigurationsfehler; die installierte Konfiguration "
            "mit apachectl -t validieren."
        )
    nginx = re.fullmatch(
        r"([a-z0-9_]+) rejects invalid values during nginx -t; (.+) is the registered context mask\.",
        value,
    )
    if nginx:
        return (
            f"{nginx.group(1)} weist ungültige Werte während nginx -t ab; "
            f"{nginx.group(2)} ist die registrierte Kontextmaske."
        )
    return value


def _has_german_rendering(value: str) -> bool:
    """Whether ``value`` has an explicit or parameterized German rendering."""
    return value in GERMAN_TEXT or _german_text(value) != value


def _is_yaml_backed_option(option: dict[str, Any]) -> bool:
    """Whether an option is emitted from an Envoy or Traefik YAML contract."""
    return (
        option["configuration_layer"] == "host_connector_yaml"
        or "YAML path" in option["source_symbol"]
    )


def _yaml_category(option: dict[str, Any]) -> tuple[str, str, str]:
    """Return German subject, effect, and safety text for a YAML path.

    The YAML inventory is intentionally closed and path-specific on the
    English side.  This classifier makes its German counterpart resilient to
    new checked-in paths: it retains the exact technical path in the rendered
    syntax/example sections while emitting complete German prose instead of
    falling back to the English metadata string.
    """
    path = _without_compatibility_prefix(option["name"]).lower()
    compatibility = option["compatibility_only"]
    if "processing_mode" in path or "ext_proc" in path and any(
        token in path for token in ("body", "header", "trailer", "message_timeout", "override")
    ):
        return (
            "die Sichtbarkeit und zeitliche Verarbeitung von P1–P4 im ext_proc-Pfad",
            "Sie bestimmt, welche Request-/Response-Daten der externe Prozessor im ausgewählten Lebenszyklus erhält.",
            "Body- und Header-Sichtbarkeit nur mit begrenzten Eingaben und geschützten Protokolldaten aktivieren.",
        )
    if "admin" in path:
        return (
            "die administrative Envoy-Schnittstelle",
            "Sie konfiguriert die administrative Listener- oder Protokollierungsseite außerhalb des Datenpfads.",
            "Administrative Endpunkte und Logs müssen privat bleiben und dürfen nicht ohne ausdrückliches Deployment-Konzept freigegeben werden.",
        )
    if any(token in path for token in ("listener", "entrypoints", "socket_address", ".address", "port_value")):
        return (
            "die Listener-Bindung und Netzwerk-Erreichbarkeit",
            "Sie legt fest, an welcher Adresse oder welchem Port der Host Verbindungen annimmt oder einen lokalen Dienst erreicht.",
            "Adresse und Port bestimmen die Erreichbarkeit vor der Regelverarbeitung; nur geprüfte private Bindungen verwenden.",
        )
    if any(token in path for token in ("cluster", "endpoint", "load_assignment", "services", "loadbalancer", "servers", "grpc_service", "server_uri")):
        return (
            "die Upstream- oder Service-Verbindung",
            "Sie wählt die Zielinstanz, den Transport oder das Zeitlimit für einen Upstream- beziehungsweise Prozessorservice.",
            "Upstream-Adressen, Zeitlimits und Service-Ziele sind sicherheitsrelevant und müssen auf vertrauenswürdige lokale oder freigegebene Ziele begrenzt sein.",
        )
    if any(token in path for token in ("route", "routers", "virtual_hosts", "domains", "prefix", "match", "route_config")):
        return (
            "die Request-Routing-Entscheidung",
            "Sie ordnet eingehende Requests einer Route, Middleware oder einem Upstream zu.",
            "Eine Änderung der Reihenfolge oder Zielzuordnung kann die Inspektion umgehen; nur geprüfte Routen und Zielservices verwenden.",
        )
    if any(token in path for token in ("http_filters", "filter_chains", "typed_config", "http_connection_manager", "ext_authz")):
        return (
            "die HTTP-Filterkette und deren Konfiguration",
            "Sie legt die Reihenfolge und Konfiguration der HTTP-Filter fest, über die Request und Response verarbeitet werden.",
            "Die Filterreihenfolge bestimmt, ob der ausgewählte Prüfpfad erreicht wird; keine unüberprüfte Umgehung vor dem Sicherheitsfilter einfügen.",
        )
    if any(token in path for token in ("middlewares", "forwardauth", "modsecuritynative")):
        return (
            "die Middleware-Anbindung",
            "Sie bindet die ausgewählte Middleware an den Request- und Response-Verarbeitungsweg.",
            "Middleware-Referenzen und ihre Reihenfolge müssen erhalten bleiben, damit die geprüfte Sicherheitsverarbeitung nicht umgangen wird.",
        )
    if any(token in path for token in ("providers", "filename", "watch", "file", "directory")):
        return (
            "das Laden der dynamischen Konfiguration",
            "Sie legt fest, aus welcher Datei oder welchem Provider dynamische Hostkonfiguration geladen wird.",
            "Konfigurationsdateien und Verzeichnisse müssen vor unbefugtem Schreiben geschützt sein.",
        )
    if any(token in path for token in ("plugin", "localplugins", "modulename", "settings", "envs", "module")):
        return (
            "die lokale Plugin-Konfiguration",
            "Sie verbindet den Host mit der ausgewählten lokalen Plugin-Implementierung und ihren Einstellungen.",
            "Nur überprüfte lokale Plugin-Pfade, Module und Einstellungen verwenden; Änderungen können den Prüfpfad ersetzen.",
        )
    if any(token in path for token in ("log", "access_log", "level")):
        return (
            "die Protokollierung",
            "Sie steuert, welche Host- oder Verwaltungsereignisse protokolliert werden.",
            "Logs können sensible Betriebs- und Sicherheitsdaten enthalten; Zugriff, Rotation und Zielpfad absichern.",
        )
    if compatibility:
        return (
            "die Kompatibilitätsintegration",
            "Sie konfiguriert einen getrennten Kompatibilitätspfad außerhalb des ausgewählten nativen Kernpfads.",
            "Diese Einstellung nicht als Nachweis einer nativen Full-Lifecycle-Integration verwenden.",
        )
    return (
        "die Host-/Connector-YAML-Konfiguration",
        "Sie konfiguriert einen quellenbasierten Teil des ausgewählten Host- und Connectorpfads.",
        "Die Auswirkung auf Netzwerk, Routing und Policy vor dem Einsatz mit dem dokumentierten Template und Quellanker prüfen.",
    )


def _yaml_field_kind(option: dict[str, Any]) -> str:
    """Return a German, readable type label without changing the YAML path."""
    leaf = _without_compatibility_prefix(option["name"]).rsplit(".", 1)[-1]
    list_item = leaf.endswith("[]")
    leaf = leaf.rstrip("[]")
    lower = leaf.lower()
    if "port" in lower:
        return "YAML-Portfeld"
    if "address" in lower or "url" in lower or lower in {"uri", "server_uri"}:
        return "YAML-Adressfeld"
    if "timeout" in lower or "duration" in lower:
        return "YAML-Zeitlimitfeld"
    if "limit" in lower or "bytes" in lower or lower.startswith("max"):
        return "YAML-Limitfeld"
    if "name" in lower or "prefix" in lower or "type" in lower:
        return "YAML-Kennungsfeld"
    if "mode" in lower or "action" in lower or "level" in lower:
        return "YAML-Steuerfeld"
    if list_item or lower in {"listeners", "clusters", "filters", "routes", "middlewares", "services", "servers", "envs", "endpoints", "domains"}:
        return "YAML-Liste oder -Zuordnung"
    return "YAML-Konfigurationsfeld"


def _yaml_german_fallback(option: dict[str, Any], field: str) -> str:
    """Produce a complete German sentence for unmapped YAML metadata.

    This deliberate fallback is preferable to an untranslated prose fragment.
    It is keyed by the field being rendered, so values/defaults/validation and
    operations continue to answer their distinct documentation questions even
    if a future selected template introduces a new YAML path.
    """
    subject, effect, safety = _yaml_category(option)
    path = option["name"]
    connector = option["connector"].capitalize()
    if field == "value_type":
        return _yaml_field_kind(option)
    if field == "allowed_values":
        return f"Die zulässige Ausprägung von `{path}` ergibt sich aus dem ausgewählten {connector}-Template und der Hostvalidierung."
    if field == "default":
        return f"Der Connector definiert für `{path}` keinen unabhängigen Standardwert; das ausgewählte Template legt den gezeigten Wert ausdrücklich fest."
    if field == "default_source":
        return f"Ausgewähltes {connector}-Template und der im Quellanker referenzierte Validierungscode."
    if field == "contexts":
        return f"YAML-Pfad `{path}` im ausgewählten {connector}-Template."
    if field == "inheritance":
        return "Die Vererbung wird durch die Host-YAML-Struktur bestimmt; dies ist keine Common-Runtime-Dateivererbung."
    if field == "merge_behavior":
        return "Die Zusammenführung folgt der Host-YAML- beziehungsweise API-Semantik der ausgewählten Konfigurationsschicht."
    if field == "validation":
        command = {
            "envoy": "envoy --mode validate -c <generated-config>",
            "traefik": "traefik check --configFile=<static-config>",
        }.get(option["connector"], "der dokumentierten Hostprüfung")
        return f"Den materialisierten oder ausgewählten YAML-Pfad mit {command} und der zugehörigen Connector-Prüfung validieren."
    if field == "phase_relevance":
        return f"Die P1–P4-Relevanz folgt daraus, wie `{path}` {subject} konfiguriert."
    if field == "security_relevance":
        return safety
    if field in {"runtime_effect", "description"}:
        return f"Das YAML-Feld `{path}` konfiguriert {subject}. {effect}"
    raise ValueError(f"unexpected YAML localization field: {field}")


def _german_option_text(option: dict[str, Any], field: str) -> str:
    """Localize one field, using the structured YAML fallback when needed."""
    value = option[field]
    if _has_german_rendering(value):
        return _german_text(value)
    if _is_yaml_backed_option(option):
        return _yaml_german_fallback(option, field)
    return value


def _has_german_option_rendering(option: dict[str, Any], field: str) -> bool:
    """Check explicit translations and the fully German YAML fallback path."""
    return _has_german_rendering(option[field]) or _is_yaml_backed_option(option)


def _uses_yaml_german_fallback(option: dict[str, Any], field: str) -> bool:
    """Whether German prose is synthesized for this YAML metadata field."""
    return _is_yaml_backed_option(option) and not _has_german_rendering(option[field])


GERMAN_OPTION_FIELDS = (
    "value_type",
    "allowed_values",
    "default",
    "default_source",
    "contexts",
    "inheritance",
    "merge_behavior",
    "validation",
    "phase_relevance",
    "security_relevance",
    "runtime_effect",
    "description",
)


def german_translation_errors(options: Iterable[dict[str, Any]]) -> list[str]:
    """Report English metadata that has no deliberate German rendering.

    This is a source-to-documentation guard, not a heuristic language checker:
    every free-text value emitted into a German option section must either have
    a translation or be explicitly listed as an unchanged technical literal.
    New YAML fields use the structured German fallback above; non-YAML prose
    still fails this gate until it receives an explicit counterpart.
    """
    errors: list[str] = []
    for option in options:
        for field in GERMAN_OPTION_FIELDS:
            if not _has_german_option_rendering(option, field):
                errors.append(f"{option['connector']}:{option['name']}:{field}: missing German rendering")
    return errors


def _german_option(option: dict[str, Any]) -> dict[str, Any]:
    """Localize free prose without changing source-derived technical values."""
    translated = dict(option)
    missing = [field for field in GERMAN_OPTION_FIELDS if not _has_german_option_rendering(option, field)]
    if missing:
        raise ValueError(
            f"German rendering missing for {option['connector']}:{option['name']}: {', '.join(missing)}"
    )
    for field in GERMAN_OPTION_FIELDS:
        translated[field] = _german_option_text(option, field)
    translated["_german_fallback_fields"] = tuple(
        field for field in GERMAN_OPTION_FIELDS if _uses_yaml_german_fallback(option, field)
    )
    return translated


def layer_name(layer: str, german: bool) -> str:
    names = {
        "host_connector_directive": ("Host / Connector", "Host / Connector"),
        "host_example_field": ("Host", "Host"),
        "host_connector_yaml": ("Host / Connector", "Host / Connector"),
        "service_json_field": ("Connector service", "Connector-Service"),
        "runtime_cli_flag": ("Environment / runtime", "Umgebung / Laufzeit"),
        "common_runtime": ("Common Runtime", "Common Runtime"),
        "modsecurity_engine": ("ModSecurity Engine", "ModSecurity Engine"),
        "example_placeholder": ("Example placeholder", "Beispielplatzhalter"),
        "compatibility": ("Compatibility", "Kompatibilität"),
    }
    return names[layer][1 if german else 0]


def _render_option(option: dict[str, Any], german: bool) -> list[str]:
    source_option = option
    if german:
        option = _german_option(option)
    fallback_fields = option.get("_german_fallback_fields", ())
    labels = {
        "short": "Kurzbeschreibung" if german else "Short description",
        "syntax": "Syntax",
        "contexts": "Gültige Kontexte" if german else "Valid contexts",
        "values": "Werte" if german else "Values",
        "default": "Standardwert" if german else "Default",
        "inheritance": "Vererbung und Zusammenführung" if german else "Inheritance and merge",
        "effect": "Phasen und Laufzeitwirkung" if german else "Phases and runtime effect",
        "validation": "Validierung und Fehler" if german else "Validation and errors",
        "example": "Beispiel" if german else "Example",
        "safety": "Sicherheit und Betrieb" if german else "Safety and operations",
    }
    intro = option["description"]
    phase = option["phase_relevance"]
    if german:
        phase = "P1–P4-Relevanz: " + option["phase_relevance"]
    if option.get("example_value"):
        literal = _inline_literal(option["example_value"])
        example_value_line = (f"Ausgewählter Beispielwert: {literal}." if german else f"Selected example value: {literal}.")
    else:
        example_value_line = ("Ausgewählter Wert: Syntax oben und quellenbasierte Datei unten verwenden." if german else "Selected value: use the syntax above and the source-backed file below.")
    source_example_line = (
        f"Quellenbasiertes Beispiel: [{option['example_file']}](../../{option['example_file'] if option['example_file'].startswith('examples/') else option['example_file']})."
        if german and option["example_file"].startswith("examples/")
        else f"Source-backed example: [{option['example_file']}](../../{option['example_file'] if option['example_file'].startswith('examples/') else option['example_file']})."
        if option["example_file"].startswith("examples/")
        else f"Quellenbasiertes Beispiel: `{option['example_file']}`." if german else f"Source-backed example: `{option['example_file']}`."
    )
    lines = [
        f'<a id="{_slug(option["name"])}"></a>',
        f"## `{option['name']}`",
        "",
        f"### {labels['short']}",
        "",
        intro,
        "",
        f"### {labels['syntax']}",
        "",
        "```text",
        option["syntax"],
        "```",
        "",
        f"### {labels['contexts']}",
        "",
        f"- {option['contexts']}",
        "",
        f"### {labels['values']}",
        "",
        "| Typ | Zulässige Werte | Erforderlich |" if german else "| Type | Allowed values | Required |",
        "| --- | --- | --- |",
        f"| {_table_cell(option['value_type'])} | {_table_cell(option['allowed_values'])} | {('ja' if option['required'] else 'nein') if german else ('yes' if option['required'] else 'no')} |",
        "",
        f"### {labels['default']}",
        "",
        option["default"],
        "",
        f"{'Quelle' if german else 'Source'}: `{option['default_source']}`.",
        "",
        f"### {labels['inheritance']}",
        "",
        option["inheritance"],
        "",
        f"{'Zusammenführung' if german else 'Merge'}: {option['merge_behavior']}",
        "",
        f"### {labels['effect']}",
        "",
        phase,
        "",
        option["runtime_effect"],
        "",
        f"### {labels['validation']}",
        "",
        option["validation"],
        "",
        f"### {labels['example']}",
        "",
        example_value_line,
        "",
        source_example_line,
        "",
        f"### {labels['safety']}",
        "",
        option["security_relevance"],
        "",
    ]
    if german and fallback_fields:
        lines.extend([
            "### Technische Quellmetadaten (unverändert)",
            "",
            "Die folgenden Quellwerte bewahren die technische, englische Originalmetadatenangabe für diesen YAML-Pfad; Namen, konkrete Werte, Defaults und Protokollbegriffe bleiben dadurch vollständig nachvollziehbar.",
            "",
            "```text",
        ])
        lines.extend(f"{field}: {source_option[field]}" for field in fallback_fields)
        lines.extend(["```", ""])
    return lines


def render_connector_reference(options: list[dict[str, Any]], connector: str, german: bool) -> str:
    local = _local_options(options, connector)
    title = {
        "apache": "Apache configuration reference",
        "nginx": "NGINX configuration reference",
        "haproxy": "HAProxy configuration reference",
        "envoy": "Envoy configuration reference",
        "traefik": "Traefik configuration reference",
        "lighttpd": "lighttpd configuration reference",
    }[connector]
    if german:
        title = {
            "apache": "Apache-Konfigurationsreferenz", "nginx": "NGINX-Konfigurationsreferenz",
            "haproxy": "HAProxy-Konfigurationsreferenz", "envoy": "Envoy-Konfigurationsreferenz",
            "traefik": "Traefik-Konfigurationsreferenz", "lighttpd": "lighttpd-Konfigurationsreferenz",
        }[connector]
    mode = integration_mode(connector)
    lines = [f"# {title}", "", _language_switch("configuration-reference", german), "", "## Scope and source of truth" if not german else "## Geltungsbereich und maßgebliche Quellen", ""]
    if german:
        lines.extend([
            f"Ausgewählter Integrationsmodus: `{mode}`. Diese Datei wird aus registrierten Parsern, Konfigurationsstrukturen, geprüften Service-Verträgen und aktiven Beispielen erzeugt.",
            "Kompatibilitätseinträge sind ausdrücklich als solche markiert und gehören nicht zum ausgewählten Kernpfad.",
        ])
    else:
        lines.extend([
            f"Selected integration mode: `{mode}`. This file is generated from registered parsers, configuration structures, checked service contracts, and active examples.",
            "Compatibility entries are explicitly labelled and are not part of the selected core path.",
        ])
    lines.extend(["", "## Configuration inventory" if not german else "## Konfigurationsinventar", "", "| Option | Layer | Type | Required | Default | Context | Short description |", "| --- | --- | --- | --- | --- | --- | --- |"])
    lines.extend(_table_row(option, german) for option in local)
    lines.extend(["", "## Layer separation" if not german else "## Trennung der Ebenen", ""])
    if german:
        lines.extend([
            "Host-/Connector-Schalter binden oder konfigurieren die Hostintegration. Sie sind nicht identisch mit `SecRuleEngine`.",
            "",
            "- [Common-Runtime-Konfiguration](../common/common-connector-configuration.de.md) beschreibt nur die `key=value`-Runtime-Datei und wird nicht als nicht registrierte Hostdirektive ausgegeben.",
            "- [ModSecurity-Engine-Direktiven](../common/modsecurity-directives.de.md) beschreibt die `Sec*`-Direktiven der geladenen Regeldatei.",
            "- [Regelbeispiele](../common/rule-examples.de.md) erklären DetectionOnly und das Abschalten der Engine.",
        ])
    else:
        lines.extend([
            "Host/connector switches bind or configure host integration. They are not the same setting as `SecRuleEngine`.",
            "",
            "- [Common Runtime configuration](../common/common-connector-configuration.md) covers only the `key=value` runtime file and is not presented as an unregistered host directive.",
            "- [ModSecurity Engine directives](../common/modsecurity-directives.md) covers `Sec*` directives in the loaded rule file.",
            "- [Rule examples](../common/rule-examples.md) explains DetectionOnly and engine Off.",
        ])
    runtime_keys = {
        "apache": (),
        "nginx": (),
        "haproxy": (),
        "envoy": ("enabled", "rules_file", "transaction_id_header", "request_body_mode", "response_body_mode", "request_body_limit", "response_body_limit", "body_limit_action", "phase4_mode", "default_block_status", "default_error_status", "use_error_log", "max_header_count", "max_header_name_size", "max_header_value_size", "max_total_header_bytes", "max_event_json_bytes"),
        "traefik": ("enabled", "rules_file", "transaction_id_header", "request_body_mode", "response_body_mode", "request_body_limit", "response_body_limit", "body_limit_action", "phase4_mode", "default_block_status", "default_error_status", "use_error_log", "max_header_count", "max_header_name_size", "max_header_value_size", "max_total_header_bytes", "max_event_json_bytes"),
        "lighttpd": tuple(COMMON_DETAILS),
    }[connector]
    lines.extend(["", "## Common Runtime relevance" if not german else "## Common-Runtime-Relevanz", ""])
    if not runtime_keys:
        lines.append("The selected native path does not parse a Common Runtime `key=value` file; shared model fields are exposed only through registered host directives." if not german else "Der ausgewählte native Pfad parst keine Common-Runtime-`key=value`-Datei; gemeinsame Modellfelder werden nur über registrierte Hostdirektiven angeboten.")
    else:
        common_reference = "../common/common-connector-configuration.de.md" if german else "../common/common-connector-configuration.md"
        lines.extend(["| Key | Local use | Detailed reference |" if not german else "| Schlüssel | Lokale Verwendung | Detailreferenz |", "| --- | --- | --- |"])
        for key in runtime_keys:
            local_use = "Selected runtime profile key" if not german else "Schlüssel des ausgewählten Runtime-Profils"
            lines.append(f"| `{key}` | {local_use} | [{key}]({common_reference}#{_slug(key)}) |")
    lines.extend(["", "## Engine directives used by profiles" if not german else "## Von Profilen verwendete Engine-Direktiven", ""])
    engine_reference = "../common/modsecurity-directives.de.md" if german else "../common/modsecurity-directives.md"
    lines.extend([
        "The local rule profiles use `SecRuleEngine` for On, DetectionOnly, and Off. Where body inspection is selected, `SecRequestBodyAccess`, `SecResponseBodyAccess`, MIME scope, limits, and `SecRule` remain ModSecurity Engine directives." if not german else "Die lokalen Regelprofile verwenden `SecRuleEngine` für On, DetectionOnly und Off. Wo Body-Inspektion gewählt wird, bleiben `SecRequestBodyAccess`, `SecResponseBodyAccess`, MIME-Scope, Limits und `SecRule` ModSecurity-Engine-Direktiven.",
        "",
        f"{'Siehe' if german else 'See'} [{ 'Engine reference' if not german else 'Engine-Referenz'}]({engine_reference}).",
    ])
    profile_files = {
        "apache": ("minimal/httpd.conf", "safe/httpd.conf", "README", "detection-only/httpd.conf", "disabled/httpd.conf"),
        "nginx": ("minimal/nginx.conf", "safe/nginx.conf", "strict/nginx.conf", "detection-only/nginx.conf", "disabled/nginx.conf"),
        "haproxy": ("minimal/haproxy-htx.cfg", "safe/haproxy-htx.cfg", "README", "detection-only/haproxy-htx.cfg", "disabled/haproxy-htx.cfg"),
        "envoy": ("minimal/envoy-ext-proc-streaming.yaml.in", "safe/envoy-ext-proc-streaming.yaml.in", "README", "detection-only/msconnector-runtime.conf", "disabled/msconnector-runtime.conf"),
        "traefik": ("minimal/traefik-static.yaml", "safe/traefik-dynamic.yaml", "README", "detection-only/traefik-engine-service.conf", "disabled/traefik-engine-service.conf"),
        "lighttpd": ("minimal/lighttpd.conf", "safe/lighttpd-http1-identity.conf", "README", "detection-only/msconnector-runtime.conf", "disabled/lighttpd.conf"),
    }[connector]
    labels = ("Minimal", "Safe full lifecycle", "Strict", "DetectionOnly", "Disabled")
    if german:
        labels = ("Minimal", "Sicherer vollständiger Lebenszyklus", "Strikt", "DetectionOnly", "Deaktiviert")
    lines.extend(["", "## Profiles" if not german else "## Profile", "", "| Profile | File | Status |" if not german else "| Profil | Datei | Status |", "| --- | --- | --- |"])
    statuses = (
        "Active starter configuration", "Selected bounded reference", "Parser-supported or explicitly optional boundary", "Engine evaluates/logs without disruptive action", "Connector or engine path disabled",
    )
    if german:
        statuses = (
            "Aktive Startkonfiguration", "Ausgewählte begrenzte Referenz", "Parserunterstützte oder ausdrücklich optionale Grenze", "Engine wertet aus/protokolliert ohne disruptive Aktion", "Connector- oder Engine-Pfad deaktiviert",
        )
    for label, file_name, status in zip(labels, profile_files, statuses):
        if file_name == "README":
            file_name = "README.de.md#strict-profilgrenze" if german else "README.md#strict-profile-boundary"
        elif file_name.endswith("/README"):
            file_name += ".de.md" if german else ".md"
        lines.append(f"| {label} | [{file_name}]({file_name}) | {status} |")
    lines.extend(["", "## Configuration combinations" if not german else "## Konfigurationskombinationen", "", "| Connector | Engine | Request body | Response body | Result |" if not german else "| Connector | Engine | Request-Body | Response-Body | Ergebnis |", "| --- | --- | --- | --- | --- |"])
    combination_rows = [
        ("off", "On", "any", "any", "No connector transaction; engine setting is not reached."),
        ("on", "Off", "any", "any", "Connector reaches the engine, but engine rule processing is disabled."),
        ("on", "DetectionOnly", "enabled", "enabled", "Rules can match/log without disruptive enforcement."),
        ("on", "On", "Off", "On", "P2 body is unavailable to the engine; P4 remains host/capability dependent."),
        ("on", "On", "On", "Off", "P4 body is unavailable to the engine."),
        ("on", "On", "On", "On + safe", "Late post-commit P4 results are recorded without a promised later status change."),
        ("on", "On", "On", "On + strict", "Only use a host-specific strict outcome where source/evidence supports it; no synthetic late 403."),
        ("on", "On", "over limit + process_partial", "over limit + reject", "The body policy determines bounded engine input; exact host response handling remains connector-specific."),
    ]
    if german:
        combination_rows = [
            ("off", "On", "beliebig", "beliebig", "Keine Connector-Transaktion; die Engine-Einstellung wird nicht erreicht."),
            ("on", "Off", "beliebig", "beliebig", "Der Connector erreicht die Engine, aber deren Regelauswertung ist deaktiviert."),
            ("on", "DetectionOnly", "aktiviert", "aktiviert", "Regeln können ohne disruptive Durchsetzung treffen/protokollieren."),
            ("on", "On", "Off", "On", "Der P2-Body steht der Engine nicht zur Verfügung; P4 bleibt host-/fähigkeitsabhängig."),
            ("on", "On", "On", "Off", "Der P4-Body steht der Engine nicht zur Verfügung."),
            ("on", "On", "On", "On + safe", "Späte P4-Ergebnisse nach dem Commit werden ohne zugesagte spätere Statusänderung aufgezeichnet."),
            ("on", "On", "On", "On + strict", "Ein hostspezifisches strict-Ergebnis nur verwenden, wenn Quelle/Nachweis es stützen; keine künstliche spätere 403."),
            ("on", "On", "über Limit + process_partial", "über Limit + reject", "Die Body-Policy bestimmt die begrenzte Engine-Eingabe; die genaue Host-Response-Behandlung bleibt connectorspezifisch."),
        ]
    for row in combination_rows:
        lines.append("| " + " | ".join(row) + " |")
    lines.extend(["", "## Validation" if not german else "## Validierung", ""])
    validation = {
        "apache": "apachectl -t", "nginx": "nginx -t", "haproxy": "haproxy -c -f <config>",
        "envoy": "envoy --mode validate -c <generated-config>", "traefik": "traefik check --configFile=<static-config>", "lighttpd": "lighttpd -tt -f <config>",
    }[connector]
    lines.extend(["```sh", validation, "```", "", "Repository targets: `make check-config-" + connector + "` and `make check-config-all-connectors`." if not german else "Repository-Ziele: `make check-config-" + connector + "` und `make check-config-all-connectors`.", ""])
    lines.extend(["## Option details" if not german else "## Optionsdetails", ""])
    for option in local:
        lines.extend(_render_option(option, german))
    return "\n".join(lines).rstrip() + "\n"


def render_common_configuration(options: list[dict[str, Any]], german: bool) -> str:
    local = _local_options(options, "common")
    title = "Common connector configuration" if not german else "Gemeinsame Connector-Konfiguration"
    lines = [f"# {title}", "", _language_switch("common-connector-configuration", german), "", "## Scope" if not german else "## Geltungsbereich", ""]
    lines.extend([
        "This is the complete current `key=value` parser surface of `common/runtime/msconnector_runtime.c`. It is not a claim that every host exposes every key as a host directive." if not german else "Dies ist die vollständige aktuelle `key=value`-Parseroberfläche von `common/runtime/msconnector_runtime.c`. Daraus folgt nicht, dass jeder Host jeden Schlüssel als Hostdirektive anbietet.",
        "",
        "| Option | Layer | Type | Required | Default | Context | Short description |", "| --- | --- | --- | --- | --- | --- | --- |",
    ])
    lines.extend(_table_row(option, german) for option in local)
    lines.extend(["", "## Option details" if not german else "## Optionsdetails", ""])
    for option in local:
        lines.extend(_render_option(option, german))
    return "\n".join(lines).rstrip() + "\n"


def render_engine_directives(options: list[dict[str, Any]], german: bool) -> str:
    local = _local_options(options, "engine")
    title = "ModSecurity engine directives used by examples" if not german else "Von Beispielen verwendete ModSecurity-Engine-Direktiven"
    lines = [f"# {title}", "", _language_switch("modsecurity-directives", german), "", "## Scope" if not german else "## Geltungsbereich", ""]
    lines.extend([
        "Only directives actually used in checked-in example rule files are listed. They belong to libmodsecurity, not to an Apache, NGINX, HAProxy, Envoy, Traefik, or lighttpd host parser." if not german else "Aufgeführt werden nur Direktiven, die tatsächlich in eingecheckten Beispielregeldateien verwendet werden. Sie gehören zu libmodsecurity und nicht zu einem Apache-, NGINX-, HAProxy-, Envoy-, Traefik- oder lighttpd-Hostparser.",
        "",
        "| Option | Layer | Type | Required | Default | Context | Short description |", "| --- | --- | --- | --- | --- | --- | --- |",
    ])
    lines.extend(_table_row(option, german) for option in local)
    lines.extend(["", "## Rule syntax walkthrough" if not german else "## Regel-Syntax im Detail", "", "```apache", "SecRule RESPONSE_BODY \"@contains response-attack\" \\", "    \"id:1100301,phase:4,deny,log,status:403\"", "```", ""])
    if german:
        lines.extend([
            "`RESPONSE_BODY` ist die Variable, `@contains` der Operator und `response-attack` dessen Argument. Die Actions setzen eine eindeutige `id`, wählen `phase:4`, verlangen `deny`, schreiben mit `log` ein Ereignis und wünschen `status:403` vor dem Host-Commit.",
            "Nach dem Response-Commit kann ein Connector die sichtbare Statuszeile nicht zuverlässig ersetzen. `SecResponseBodyAccess On` und eine P4-Regel bedeuten daher keine garantierte spätere 403-Antwort.",
            "`VARIABLE` wählt die zu prüfenden Daten, `OPERATOR` bestimmt den Vergleich und `ACTIONS` ist die durch Kommas getrennte Steuerliste. `id` identifiziert die Regel eindeutig, `phase` legt den Auswertungszeitpunkt fest, `deny` fordert eine disruptive Entscheidung an und `log` zeichnet den Treffer auf. `status` gilt nur, solange der Host den HTTP-Status noch ändern kann; `redirect` benötigt zusätzlich ein Ziel und ist an dieselbe Commit-Grenze gebunden. Transformationen sind explizite Actions, die Eingaben vor dem Operator verändern; sie sollten sparsam und nachvollziehbar eingesetzt werden. Das gezeigte Beispiel verwendet keine Redirect- oder Transformations-Action.",
        ])
    else:
        lines.extend([
            "`RESPONSE_BODY` is the variable, `@contains` is the operator, and `response-attack` is its argument. Actions assign a unique `id`, select `phase:4`, request `deny`, record `log`, and request `status:403` before host commit.",
            "After response commit a connector cannot reliably replace the visible status line. `SecResponseBodyAccess On` and a P4 rule therefore do not guarantee a later 403 response.",
            "`VARIABLE` selects the data to inspect, `OPERATOR` defines the comparison, and `ACTIONS` is the comma-separated control list. `id` uniquely identifies the rule, `phase` selects evaluation timing, `deny` requests a disruptive decision, and `log` records the match. `status` applies only while the host can still change the HTTP status; `redirect` additionally needs a target and has the same commit-boundary constraint. Transformations are explicit actions that alter input before the operator, so keep them minimal and reviewable. The illustrated rule does not use redirect or a transformation action.",
        ])
    lines.extend(["", "## Option details" if not german else "## Optionsdetails", ""])
    for option in local:
        lines.extend(_render_option(option, german))
    return "\n".join(lines).rstrip() + "\n"


def render_common_readme(german: bool) -> str:
    title = "Common example configuration reference" if not german else "Gemeinsame Beispiel-Konfigurationsreferenz"
    lines = [f"# {title}", "", _language_switch("README", german), ""]
    if german:
        lines.extend([
            "Diese zentrale Referenz trennt vier Ebenen: Host-/Connector-Konfiguration, Common Runtime, ModSecurity Engine und Beispielplatzhalter. Die sechs Connector-Referenzen verlinken hierher, ohne Common-Schlüssel als nicht registrierte Hostdirektiven auszugeben.",
            "",
            "| Material | Ebene | Zweck |",
            "| --- | --- | --- |",
            "| [Common-Runtime-Konfiguration](common-connector-configuration.de.md) | Common Runtime | Vollständige aktuelle `key=value`-Parseroptionen. |",
            "| [ModSecurity-Engine-Direktiven](modsecurity-directives.de.md) | ModSecurity Engine | Tatsächlich in Beispielregeldateien verwendete `Sec*`-Direktiven. |",
            "| [Regelbeispiele](rule-examples.de.md) | ModSecurity Engine | On, DetectionOnly, Off sowie P1/P4-Erklärung. |",
            "| [Zentrale Variablenreferenz](../../docs/reference/variables.de.md) | Umgebung/Laufzeit | Repository- und Harness-Variablen. |",
            "",
            "## Umgebungs- und Laufzeitwerte",
            "",
            "`BUILD_ROOT`, `NO_CRS_RUN_ID`, `EVIDENCE_ROOT`, `CACHE_ROOT` und connector-spezifische Materializerwerte gehören zur Laufzeit/CI, nicht in Hostdirektiven. Der Envoy-Template-Materializer verwendet die explizit dokumentierten `@...@`-Platzhalter; generierte Dateien müssen außerhalb des Checkouts liegen.",
        ])
    else:
        lines.extend([
            "This central reference separates four layers: host/connector configuration, Common Runtime, ModSecurity Engine, and example placeholders. The six connector references link here without presenting Common keys as unregistered host directives.",
            "",
            "| Material | Layer | Purpose |",
            "| --- | --- | --- |",
            "| [Common Runtime](common-connector-configuration.md) | Common Runtime | Complete current `key=value` parser options. |",
            "| [ModSecurity Engine](modsecurity-directives.md) | ModSecurity Engine | `Sec*` directives actually used by example rule files. |",
            "| [Rule examples](rule-examples.md) | ModSecurity Engine | On, DetectionOnly, Off, plus P1/P4 explanation. |",
            "| [Central variables reference](../../docs/reference/variables.md) | Environment/runtime | Repository and harness variables. |",
            "",
            "## Environment and runtime values",
            "",
            "`BUILD_ROOT`, `NO_CRS_RUN_ID`, `EVIDENCE_ROOT`, `CACHE_ROOT`, and connector-specific materializer inputs belong to runtime/CI, not host directives. The Envoy template materializer uses the explicitly documented `@...@` placeholders; generated files must remain outside the checkout.",
        ])
    return "\n".join(lines).rstrip() + "\n"


def render_rule_examples(german: bool) -> str:
    title = "ModSecurity rule examples" if not german else "ModSecurity-Regelbeispiele"
    comments = (
        "# Enforce an eligible pre-commit deny.",
        "# Match and log without a disruptive action.",
        "# Do not evaluate rules after they are loaded.",
    )
    if german:
        comments = (
            "# Einen zulässigen deny vor dem Commit durchsetzen.",
            "# Ohne disruptive Action treffen und protokollieren.",
            "# Regeln nach dem Laden nicht auswerten.",
        )
    lines = [f"# {title}", "", _language_switch("rule-examples", german), "", "## Rule-engine modes" if not german else "## Regel-Engine-Modi", "", "```apache", comments[0], "SecRuleEngine On", "", comments[1], "SecRuleEngine DetectionOnly", "", comments[2], "SecRuleEngine Off", "```", ""]
    if german:
        lines.extend([
            "`DetectionOnly` lädt und bewertet Regeln, protokolliert Treffer, führt disruptive Actions aber nicht durch. `Off` deaktiviert die Engine-Regelauswertung; ein Connector-Schalter kann dabei weiterhin aktiv sein. Umgekehrt erreicht `SecRuleEngine On` keinen Verkehr, wenn der Hostconnector abgeschaltet ist.",
            "",
            "## P1–P4-Beispiel",
            "",
            "```apache",
            "SecRequestBodyAccess On",
            "SecResponseBodyAccess On",
            "SecResponseBodyMimeType text/plain text/html application/json",
            "SecResponseBodyLimit 1048576",
            "SecResponseBodyLimitAction ProcessPartial",
            "SecRule RESPONSE_BODY \"@contains response-attack\" \\",
            "    \"id:1100301,phase:4,deny,log,status:403\"",
            "```",
            "",
            "P1 sind Request-Header, P2 der Request-Body, P3 Response-Header und P4 der Response-Body. Die P4-Regel wünscht vor Commit eine 403; nach Commit bleibt der sichtbare Status hostabhängig und darf nicht als garantiert dokumentiert werden.",
        ])
    else:
        lines.extend([
            "`DetectionOnly` loads and evaluates rules and logs matches without applying disruptive actions. `Off` disables engine rule evaluation; a connector switch may still be active. Conversely, `SecRuleEngine On` reaches no traffic when the host connector is disabled.",
            "",
            "## P1–P4 example",
            "",
            "```apache",
            "SecRequestBodyAccess On",
            "SecResponseBodyAccess On",
            "SecResponseBodyMimeType text/plain text/html application/json",
            "SecResponseBodyLimit 1048576",
            "SecResponseBodyLimitAction ProcessPartial",
            "SecRule RESPONSE_BODY \"@contains response-attack\" \\",
            "    \"id:1100301,phase:4,deny,log,status:403\"",
            "```",
            "",
            "P1 is request headers, P2 request body, P3 response headers, and P4 response body. The P4 rule requests a 403 before commit; after commit the visible status remains host-dependent and must not be documented as guaranteed.",
        ])
    return "\n".join(lines).rstrip() + "\n"


def rendered_files(root: Path = ROOT) -> dict[Path, str]:
    options = build_inventory(root)
    outputs: dict[Path, str] = {}
    for connector in CONNECTORS:
        outputs[root / f"examples/{connector}/configuration-reference.md"] = render_connector_reference(options, connector, False)
        outputs[root / f"examples/{connector}/configuration-reference.de.md"] = render_connector_reference(options, connector, True)
    outputs[root / "examples/common/README.md"] = render_common_readme(False)
    outputs[root / "examples/common/README.de.md"] = render_common_readme(True)
    outputs[root / "examples/common/common-connector-configuration.md"] = render_common_configuration(options, False)
    outputs[root / "examples/common/common-connector-configuration.de.md"] = render_common_configuration(options, True)
    outputs[root / "examples/common/modsecurity-directives.md"] = render_engine_directives(options, False)
    outputs[root / "examples/common/modsecurity-directives.de.md"] = render_engine_directives(options, True)
    outputs[root / "examples/common/rule-examples.md"] = render_rule_examples(False)
    outputs[root / "examples/common/rule-examples.de.md"] = render_rule_examples(True)
    outputs[root / "reports/connector-configuration-inventory.json"] = inventory_json(root)
    return outputs


def generated_file_paths(root: Path = ROOT) -> list[Path]:
    return sorted(rendered_files(root))


def write_rendered_files(root: Path = ROOT) -> list[Path]:
    outputs = rendered_files(root)
    changed: list[Path] = []
    for path, content in outputs.items():
        path.parent.mkdir(parents=True, exist_ok=True)
        if not path.exists() or path.read_text(encoding="utf-8") != content:
            path.write_text(content, encoding="utf-8")
            changed.append(path)
    return changed


def source_inventory_summary(root: Path = ROOT) -> dict[str, int]:
    return {connector: len(_local_options(build_inventory(root), connector)) for connector in (*CONNECTORS, "common", "engine")}
