# Configuration, Shell, Make, and Path Injection Check

Trace externally influenced values through environment variables, Make variables, shell commands, Python/config generators, YAML/JSON/TOML serialization, host configuration, paths, addresses, ports, rule files, event/log paths, plugin/module paths, and option parsing.

Assess shell/command substitution, option injection, Make evaluation, YAML scalar/anchor/tag issues where applicable, path traversal, symlink escape, control/newline characters, inconsistent validation versus later serialization, and silent fallback to another binary/path/configuration.

Prefer argument vectors and explicit validated paths. Do not infer safety from quoting alone.
