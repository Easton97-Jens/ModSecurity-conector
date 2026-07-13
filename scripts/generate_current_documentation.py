#!/usr/bin/env python3
"""Generate the paired current-contract guides from one reviewed source."""

from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
GENERATED = "<!-- Generated from scripts/generate_current_documentation.py; do not edit directly. -->"


ARCHITECTURE = {
    "overview": (
        "Common architecture overview",
        "Überblick über die Common-Architektur",
        "The Common layer defines connector-neutral contracts. Host structures, host memory management, and host callbacks remain in each connector.",
        "Die Common-Schicht definiert connector-neutrale Verträge. Host-Strukturen, Host-Speicherverwaltung und Host-Callbacks bleiben im jeweiligen Connector.",
        "The selected core is HTTP/1.1 P1–P4. It borrows chunks from a host and never makes Common own host body storage.",
        "Der ausgewählte Kern ist HTTP/1.1 P1–P4. Er leiht Chunks vom Host und lässt Common niemals Host-Body-Speicher besitzen.",
    ),
    "sdk": (
        "Common SDK contract",
        "Common-SDK-Vertrag",
        "The SDK provides neutral configuration, request/response mapping contracts, event primitives, and validation helpers. It does not expose Apache, NGINX, HAProxy, Envoy, Traefik, or lighttpd types.",
        "Das SDK stellt neutrale Konfiguration, Request-/Response-Mapping-Verträge, Event-Primitiven und Validierungshelfer bereit. Es stellt keine Apache-, NGINX-, HAProxy-, Envoy-, Traefik- oder lighttpd-Typen bereit.",
        "An adapter validates host metadata before passing it to the SDK and keeps ownership at the adapter boundary.",
        "Ein Adapter validiert Host-Metadaten vor der Übergabe an das SDK und behält Ownership an der Adaptergrenze.",
    ),
    "runtime": (
        "Runtime contract",
        "Runtime-Vertrag",
        "Runtime roots are explicit and outside the checkout. Cache-v2 is reusable only for matching identity inputs; build, log, and evidence roots are run-local.",
        "Runtime-Roots sind explizit und außerhalb des Checkouts. Cache-v2 ist nur bei passenden Identity-Eingaben wiederverwendbar; Build-, Log- und Evidence-Roots sind lauflokal.",
        "Use `BUILD_ROOT`, `CACHE_ROOT`, and `EVIDENCE_ROOT` through Make targets; their defaults and safety rules are documented centrally.",
        "Verwende `BUILD_ROOT`, `CACHE_ROOT` und `EVIDENCE_ROOT` über Make-Targets; Defaults und Sicherheitsregeln sind zentral dokumentiert.",
    ),
    "transactions": (
        "Transaction lifecycle",
        "Transaktions-Lifecycle",
        "P1 processes request headers, P2 processes request body and ends at request EOS, P3 processes response headers, and P4 receives response body chunks and ends at response EOS.",
        "P1 verarbeitet Request-Header, P2 verarbeitet den Request-Body und endet bei Request-EOS, P3 verarbeitet Response-Header und P4 erhält Response-Body-Chunks und endet bei Response-EOS.",
        "Append and finish are distinct operations. A chunk is borrowed while it is forwarded; EOS performs the one guarded finalization for that body direction.",
        "Append und Finish sind getrennte Operationen. Ein Chunk wird während des Forwardings geliehen; EOS führt die einmalig geschützte Finalisierung für diese Body-Richtung aus.",
    ),
    "events": (
        "Event and evidence contract",
        "Event- und Evidence-Vertrag",
        "Events carry bounded metadata such as phase, rule ID, message ID, action, commit state, and lifecycle counters. They must not carry request or response payloads.",
        "Events tragen begrenzte Metadaten wie Phase, Rule-ID, Message-ID, Aktion, Commit-Status und Lifecycle-Zähler. Sie dürfen keine Request- oder Response-Payloads tragen.",
        "A result and an event are different evidence records; a result alone cannot infer a causal host event.",
        "Ein Result und ein Event sind unterschiedliche Evidence-Datensätze; ein Result allein darf kein kausales Host-Event ableiten.",
    ),
    "limits": (
        "Limits and buffering",
        "Limits und Buffering",
        "The selected core does not permit a connector-owned full response buffer. Hosts may apply their own bounded facilities, but evidence states the observed boundary rather than assuming it.",
        "Der ausgewählte Kern erlaubt keinen connector-eigenen vollständigen Response-Buffer. Hosts können eigene begrenzte Einrichtungen verwenden, aber Evidence beschreibt die beobachtete Grenze statt sie anzunehmen.",
        "Configure only existing host controls and record their effective configuration as hashes or safe metadata.",
        "Konfiguriere nur vorhandene Host-Controls und zeichne ihre effektive Konfiguration als Hashes oder sichere Metadaten auf.",
    ),
    "late-intervention": (
        "Late intervention",
        "Späte Intervention",
        "Before commitment a host may apply a supported deny action. After commitment, Safe mode records a `log_only` outcome; it must not be represented as a rewritten client status.",
        "Vor dem Commit kann ein Host eine unterstützte Deny-Aktion anwenden. Nach dem Commit zeichnet der Safe-Modus ein `log_only`-Ergebnis auf; es darf nicht als umgeschriebener Client-Status dargestellt werden.",
        "Strict behavior is a separate host capability and is not claimed for every connector.",
        "Strict-Verhalten ist eine getrennte Host-Capability und wird nicht für jeden Connector behauptet.",
    ),
    "ownership-and-memory": (
        "Ownership and memory",
        "Ownership und Speicher",
        "Adapters own host references, pools, allocators, and callback lifetime. Common receives validated neutral values and releases only memory it allocated itself.",
        "Adapter besitzen Host-Referenzen, Pools, Allokatoren und Callback-Lebensdauer. Common erhält validierte neutrale Werte und gibt nur Speicher frei, den es selbst allokiert hat.",
        "A borrowed body chunk cannot outlive its host callback; no evidence writer may retain it or serialize it.",
        "Ein geliehener Body-Chunk darf seinen Host-Callback nicht überleben; kein Evidence-Schreiber darf ihn behalten oder serialisieren.",
    ),
}


TESTING = {
    "test-levels": ("Test levels and statuses", "Testebenen und Status", "Build, configuration parsing, start smoke, runtime smoke, and full-lifecycle evidence are distinct levels. A successful build or start is not a rule-engine PASS.", "Build, Konfigurationsparsen, Start-Smoke, Runtime-Smoke und Full-Lifecycle-Evidence sind getrennte Ebenen. Ein erfolgreicher Build oder Start ist kein Rule-Engine-PASS."),
    "core-lifecycle": ("Six-connector core lifecycle", "Sechs-Connector-Kern-Lifecycle", "The selected current core covers HTTP/1.1 P1–P4, Safe post-commit P4 semantics, first byte before EOS evidence, and no connector-owned full response buffer for Apache, NGINX, HAProxy, Envoy, Traefik, and lighttpd.", "Der ausgewählte aktuelle Kern umfasst HTTP/1.1 P1–P4, Safe-Post-Commit-P4-Semantik, First-Byte-vor-EOS-Evidence und keinen connector-eigenen vollständigen Response-Buffer für Apache, NGINX, HAProxy, Envoy, Traefik und lighttpd."),
    "extended-catalog": ("Extended catalog", "Erweiterter Katalog", "The extended catalog is separate from the selected core. `NOT EXECUTED`, `BLOCKED`, and `UNSUPPORTED` are evidence states, not PASS values and not hidden failures.", "Der erweiterte Katalog ist vom ausgewählten Kern getrennt. `NOT EXECUTED`, `BLOCKED` und `UNSUPPORTED` sind Evidence-Zustände, keine PASS-Werte und keine versteckten Fehler."),
    "local-development": ("Local development", "Lokale Entwicklung", "Use a writable absolute build directory outside the checkout, for example `/srv/modsecurity-work/build`. This is an example value, not a repository default.", "Verwende ein beschreibbares absolutes Build-Verzeichnis außerhalb des Checkouts, zum Beispiel `/srv/modsecurity-work/build`. Dies ist ein Beispielwert, kein Repository-Default."),
    "ci": ("CI and local checks", "CI und lokale Prüfungen", "CI invokes the same structured Make targets where prerequisites exist. Workflow success means the invoked checks completed; it does not broaden the evidence boundary.", "CI ruft dieselben strukturierten Make-Targets auf, sofern Voraussetzungen vorhanden sind. Ein erfolgreicher Workflow bedeutet, dass die aufgerufenen Prüfungen beendet wurden; er erweitert nicht die Evidence-Grenze."),
}


EVIDENCE = {
    "artifact-layout": ("Evidence artifact layout", "Evidence-Artefaktlayout", "A canonical run may include `manifest.json`, `result.json`, `results.jsonl`, `events.jsonl`, `inventory.json`, first-byte records, transaction counts, lifecycle counters, and effective configuration metadata.", "Ein kanonischer Lauf kann `manifest.json`, `result.json`, `results.jsonl`, `events.jsonl`, `inventory.json`, First-Byte-Datensätze, Transaktionszählungen, Lifecycle-Zähler und effektive Konfigurationsmetadaten enthalten."),
    "promotion-policy": ("Evidence promotion policy", "Evidence-Promotion-Richtlinie", "Promotion requires the selected profile, attributable host evidence, valid normalization, and all required checks. Source shape or a successful command alone does not promote a capability.", "Promotion erfordert das ausgewählte Profil, zuordenbare Host-Evidence, gültige Normalisierung und alle erforderlichen Prüfungen. Source-Form oder ein erfolgreicher Befehl allein promoten keine Capability."),
    "privacy": ("Evidence privacy", "Evidence-Datenschutz", "Canonical evidence is payload-free. Do not copy request bodies, response bodies, cookies, authorization headers, tokens, private keys, or raw secrets into events, logs, or reports.", "Kanonische Evidence ist payloadfrei. Kopiere keine Request-Bodies, Response-Bodies, Cookies, Authorization-Header, Tokens, Private Keys oder Rohsecrets in Events, Logs oder Berichte."),
    "provenance": ("Evidence provenance", "Evidence-Provenienz", "A report records run ID, selected profile, generator, input records, and validation boundary. Relative repository links are portable; local machine paths are not provenance links.", "Ein Bericht zeichnet Run-ID, ausgewähltes Profil, Generator, Eingabedatensätze und Validierungsgrenze auf. Relative Repository-Links sind portabel; lokale Maschinenpfade sind keine Provenienz-Links."),
}


def render(title: str, partner: str, intro: str, detail: str, german: bool, include_status: bool, variable_prefix: str) -> str:
    language = f"**Sprache:** [English]({partner}) | Deutsch" if german else f"**Language:** English | [Deutsch]({partner})"
    scope = "Geltungsbereich" if german else "Scope"
    variables = "Variablen und Pfade" if german else "Variables and paths"
    validation = "Validierung" if german else "Validation"
    status = "Status- und Exit-Werte" if german else "Status and exit values"
    common = (
        "Dieser Leitfaden beschreibt den aktuellen ausgewählten Sechs-Connector-HTTP/1.1-Kern. Er behauptet keine Produktionsreife, vollständige CRS-, HTTP/2- oder HTTP/3-Verifikation und keine Strict-Verifikation für alle Connectoren."
        if german
        else "This guide describes the current selected six-connector HTTP/1.1 core. It does not claim production readiness, complete CRS, HTTP/2, or HTTP/3 verification, or Strict verification for every connector."
    )
    variable_text = (
        f"Wiederkehrende Werte wie `BUILD_ROOT`, `CACHE_ROOT`, `EVIDENCE_ROOT`, `FRAMEWORK_ROOT` und `NO_CRS_RUN_ID` stehen in der [zentralen Variablenreferenz]({variable_prefix}/configuration/variables.de.md). Repository-relative Pfade beginnen am Repository-Root; Lauf-, Cache- und Evidence-Pfade liegen außerhalb des Git-Worktrees."
        if german
        else f"Recurring values such as `BUILD_ROOT`, `CACHE_ROOT`, `EVIDENCE_ROOT`, `FRAMEWORK_ROOT`, and `NO_CRS_RUN_ID` are defined in the [central variables reference]({variable_prefix}/configuration/variables.md). Repository-relative paths start at the repository root; run, cache, and evidence paths are outside the Git worktree."
    )
    statuses = (
        "`PASS` bedeutet einen erfüllten geprüften Anspruch; `FAIL` einen negativen Prüfbefund; `BLOCKED` eine fehlende Voraussetzung; `NOT EXECUTED` keine Ausführung; `NOT APPLICABLE` keine Anwendbarkeit; `UNSUPPORTED` keine vom Host angebotene Fähigkeit. Prozesscode `0` bedeutet technische Beendigung, `1` allgemeinen Fehler, `2` Validierungs-/Aggregate-Fehler und `77` eine deklarierte fehlende optionale Voraussetzung."
        if german
        else "`PASS` means a checked claim was met; `FAIL` a negative check; `BLOCKED` a missing prerequisite; `NOT EXECUTED` no execution; `NOT APPLICABLE` no applicability; and `UNSUPPORTED` no host-provided capability. Process code `0` means technical completion, `1` a general error, `2` a validation/aggregate error, and `77` a declared missing optional prerequisite."
    )
    lines = [GENERATED, "", f"# {title}", "", language, "", f"## {scope}", "", intro, "", detail, "", common, "", f"## {variables}", "", variable_text]
    if include_status:
        lines += ["", f"## {status}", "", statuses]
    lines += ["", f"## {validation}", "", "Run the documented Make target from the repository root and keep the generated evidence boundary with the result." if not german else "Führe das dokumentierte Make-Target vom Repository-Root aus und bewahre die erzeugte Evidence-Grenze mit dem Ergebnis auf.", ""]
    return "\n".join(lines)


def write_group(directory: Path, topics: dict[str, tuple], include_status: bool, variable_prefix: str) -> None:
    directory.mkdir(parents=True, exist_ok=True)
    for stem, data in topics.items():
        english_title, german_title, english_intro, german_intro, *detail = data
        english_detail = detail[0] if detail else english_intro
        german_detail = detail[1] if len(detail) > 1 else german_intro
        (directory / f"{stem}.md").write_text(render(english_title, f"{stem}.de.md", english_intro, english_detail, False, include_status, variable_prefix), encoding="utf-8")
        (directory / f"{stem}.de.md").write_text(render(german_title, f"{stem}.md", german_intro, german_detail, True, include_status, variable_prefix), encoding="utf-8")


def main() -> None:
    write_group(ROOT / "docs" / "architecture" / "common", ARCHITECTURE, False, "../..")
    write_group(ROOT / "docs" / "testing", TESTING, True, "..")
    write_group(ROOT / "docs" / "evidence", EVIDENCE, True, "..")


if __name__ == "__main__":
    main()
