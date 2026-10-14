#!/usr/bin/env python3
"""Materialize exact test capture sources in an explicitly disposable copy only."""
import argparse
import hashlib
import json
from pathlib import Path
import re

HERE = Path(__file__).resolve().parent
REPOSITORY = HERE.parents[3]
MARKER = ".i12-disposable-source-copy.json"


def digest(data):
    return hashlib.sha256(data).hexdigest()


def relative(value):
    path = Path(value)
    if (not value or path.is_absolute() or any(part in ("", ".", "..", ".git") for part in value.split("/"))
            or "\\" in value):
        raise ValueError("Expected a bounded relative source path")
    return path


def plain(path):
    if path.resolve(strict=True) != path or not path.is_file():
        raise ValueError("Expected physical regular source file: " + str(path))
    info = path.stat()
    if info.st_nlink != 1:
        raise ValueError("Hard-linked source/evidence files are forbidden")
    if info.st_size > 2 * 1024 * 1024:
        raise ValueError("Only bounded text source is permitted")
    data = path.read_bytes()
    if len(data) > 2 * 1024 * 1024 or b"\0" in data:
        raise ValueError("Only bounded text source is permitted")
    data.decode("utf-8")
    return data


def exact_patch(original, patch):
    """Apply a single-file unified diff without fuzz, execution or path selection."""
    rows = patch.decode("utf-8").splitlines(keepends=True)
    if rows[:2] != ["--- a/payload\n", "+++ b/payload\n"]:
        raise ValueError("Only the exact payload delta format is permitted")
    source = original.decode("utf-8").splitlines(keepends=True)
    output, cursor, index = [], 0, 2
    while index < len(rows):
        match = re.fullmatch(r"@@ -(\d+)(?:,(\d+))? \+(\d+)(?:,(\d+))? @@\n", rows[index])
        if match is None:
            raise ValueError("Invalid payload hunk")
        start, old_count = int(match[1]), int(match[2] or 1)
        new_start, new_count = int(match[3]), int(match[4] or 1)
        start = start - 1 if old_count else start
        if start < cursor or start > len(source):
            raise ValueError("Overlapping or out-of-range payload hunk")
        output.extend(source[cursor:start])
        if new_start != len(output) + (1 if new_count else 0):
            raise ValueError("Unexpected new payload offset")
        cursor, old_seen, new_seen = start, 0, 0
        index += 1
        while index < len(rows) and not rows[index].startswith("@@ "):
            row = rows[index]
            if not row or row[0] not in " +-":
                raise ValueError("Invalid payload hunk line")
            if row[0] in " -":
                if cursor >= len(source) or source[cursor] != row[1:]:
                    raise ValueError("Payload context/base bytes differ")
                cursor += 1
                old_seen += 1
            if row[0] in " +":
                output.append(row[1:])
                new_seen += 1
            index += 1
        if (old_seen, new_seen) != (old_count, new_count):
            raise ValueError("Payload hunk lengths differ")
    output.extend(source[cursor:])
    return "".join(output).encode()


class Registry:
    def __init__(self, root=HERE, repository=REPOSITORY):
        self.root, self.repository = root, repository
        self.manifest = json.loads(plain(root / "manifest.json"))
        self.cache = {}

    def content(self, identity, trail=()):
        if identity in trail:
            raise ValueError("Cyclic source delta")
        if identity in self.cache:
            return self.cache[identity]
        item = self.manifest["objects"][identity]
        kind = item["kind"]
        if kind == "repository":
            result = plain(self.repository / relative(item["path"]))
        elif kind == "text":
            result = plain(self.root / relative(item["file"]))
        elif kind == "text_lines":
            rows = json.loads(plain(self.root / relative(item["file"])))
            if not isinstance(rows, list) or any(not isinstance(row, str) for row in rows):
                raise ValueError("Invalid lossless text-line object")
            result = "".join(rows).encode("utf-8")
        elif kind == "delta":
            patch = plain(self.root / relative(item["patch"]))
            if digest(patch) != item["patch_sha256"]:
                raise ValueError("Source delta hash mismatch")
            result = exact_patch(self.content(item["base"], (*trail, identity)), patch)
        else:
            raise ValueError("Unknown source object kind")
        if digest(result) != identity:
            raise ValueError("Source byte hash mismatch: " + identity)
        self.cache[identity] = result
        return result

    def verify(self):
        for identity in self.manifest["objects"]:
            self.content(identity)
        for profile in self.manifest["profiles"].values():
            for mapping in (profile["source_targets"], profile["capture_files"]):
                for name, entry in mapping.items():
                    relative(name)
                    self.content(entry["sha256"])
        return {"objects": len(self.cache), "profiles": len(self.manifest["profiles"]),
                "source_only": True, "runtime_qualified": False}


def disposable(path, parent_sha, storage_root):
    if not path.is_absolute() or path.resolve(strict=True) != path or not path.is_dir():
        raise ValueError("Source copy must be a physical absolute directory")
    if storage_root not in path.parents:
        raise ValueError("Source copy must be below the declared external storage root")
    # The storage control plane may itself have Git metadata. Only its declared
    # external subtree is authorized; a checkout nested within it is forbidden.
    for ancestor in (path, *path.parents):
        if ancestor == storage_root:
            break
        if (ancestor / ".git").exists():
            raise ValueError("Git checkout/metadata is forbidden")
    for child in path.rglob("*"):
        if child.name == ".git" or child.is_symlink():
            raise ValueError("Git metadata or symlink inside source copy")
    marker = json.loads(plain(path / MARKER))
    if marker != {"format": "i12-disposable-source-copy-v1", "path": str(path),
                  "disposable": True, "parent_sha": parent_sha}:
        raise ValueError("Explicit disposable source-copy identity is missing or differs")


def apply(registry, profile_name, target):
    profile = registry.manifest["profiles"][profile_name]
    disposable(target, registry.manifest["delivery_product_baseline"], Path(registry.manifest["authorized_storage_root"]))
    receipt_path = target / "i12-source-application-receipt.json"
    if receipt_path.exists():
        raise ValueError("Source application receipt already exists")
    registry.verify()
    writes = []
    for name, entry in profile["source_targets"].items():
        path = target / relative(name)
        expected = entry["before_sha256"]
        if (expected is None and path.exists()) or (expected is not None and
                (not path.is_file() or digest(plain(path)) != expected)):
            raise ValueError("Source-copy base differs: " + name)
        writes.append((path, registry.content(entry["sha256"]), entry.get("mode", 420)))
    fixture_root = target / ".i12-capture" / profile_name
    if fixture_root.exists():
        raise ValueError("Capture destination already exists")
    for name, entry in profile["capture_files"].items():
        writes.append((fixture_root / relative(name), registry.content(entry["sha256"]), entry.get("mode", 420)))
    # Validate the entire plan before any write; parent components were checked above.
    for path, data, mode in writes:
        if not path.is_relative_to(target) or mode not in (420, 493):
            raise ValueError("Invalid source-copy write")
        for parent in path.parents:
            if parent == target:
                break
            if parent.exists() and not parent.is_dir():
                raise ValueError("Source-copy parent is not a directory")
    for path, data, mode in writes:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(data)
        path.chmod(mode)
    receipt = {"profile": profile_name, "source_copy": str(target),
               "exact_written_sha256": {str(p.relative_to(target)): digest(data) for p, data, _ in writes},
               "source_copy_only": True, "runtime_qualified": False}
    with receipt_path.open("x", encoding="utf-8") as output:
        output.write(json.dumps(receipt, indent=2) + "\n")
    return receipt


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=("verify", "apply"))
    parser.add_argument("--profile")
    parser.add_argument("--source-copy", type=Path)
    args = parser.parse_args()
    try:
        registry = Registry()
        if args.action == "verify":
            result = registry.verify()
        elif args.profile is None or args.source_copy is None:
            raise ValueError("apply needs --profile and --source-copy")
        else:
            result = apply(registry, args.profile, args.source_copy)
        print(json.dumps(result, sort_keys=True))
    except (ValueError, KeyError, OSError, TypeError) as exc:
        parser.exit(2, "Capture source rejected: " + str(exc) + "\n")


if __name__ == "__main__":
    main()
