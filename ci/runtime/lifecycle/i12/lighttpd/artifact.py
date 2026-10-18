#!/usr/bin/env python3
"""Package explicitly selected lighttpd evidence and verify it without extraction.

The archive is content addressed. Absolute producer paths are manifest metadata;
they never become archive member names or local extraction destinations.
"""
from __future__ import annotations

import argparse
import gzip
import hashlib
import importlib.util
import io
import json
from pathlib import Path
import re
import tarfile


SPEC = importlib.util.spec_from_file_location(
    "lighttpd_artifact_qualification", Path(__file__).with_name("qualification.py"))
Q = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(Q)
SHA256 = re.compile(r"[0-9a-f]{64}\Z")
FILE_LIMIT = 128 * 1024 * 1024
TOTAL_LIMIT = 2 * 1024 * 1024 * 1024
MANIFEST_LIMIT = 32 * 1024 * 1024
ENTRY_LIMIT = 20000


def nested_references(value):
    if isinstance(value, dict):
        if isinstance(value.get("path"), str) and SHA256.fullmatch(str(value.get("sha256", ""))):
            yield value
        for child in value.values():
            yield from nested_references(child)
    elif isinstance(value, list):
        for child in value:
            yield from nested_references(child)


def document(raw):
    try:
        return json.loads(raw)
    except (UnicodeDecodeError, json.JSONDecodeError):
        return None


def checked_snapshot(ref, maximum):
    path = Path(ref["path"])
    if path.stat().st_size > maximum:
        raise ValueError("Evidence file exceeds the explicit per-file budget")
    actual = Q.reference(path)
    raw, stable = Q.SOURCES.snapshot(path)
    if actual != stable or actual["sha256"] != ref["sha256"]:
        raise ValueError("Evidence bytes differ from the selected immutable reference")
    if "bytes" in ref and actual["bytes"] != ref["bytes"]:
        raise ValueError("Evidence size differs from the selected immutable reference")
    return raw, actual


def add_member(archive, name, raw):
    info = tarfile.TarInfo(name)
    info.size = len(raw)
    info.mode = 0o444
    info.mtime = 0
    archive.addfile(info, io.BytesIO(raw))


def unavailable_key(ref):
    return ref["path"], ref["sha256"]


def collect(seed, staging, maximum, total_maximum):
    """Read only explicit SHA-bound references, including their JSON closure."""
    pending = list(seed["files"])
    approved_missing = {unavailable_key(ref): ref for ref in seed.get("unavailable_references", [])}
    if any(not item.get("reason") for item in approved_missing.values()):
        raise ValueError("Unavailable historical references require a separate explicit explanation")
    entries, objects, missing, seen = [], {}, [], set()
    used = 0
    while pending:
        ref = pending.pop()
        key = unavailable_key(ref)
        if key in seen:
            continue
        seen.add(key)
        if len(seen) > ENTRY_LIMIT:
            raise ValueError("Evidence reference closure exceeds its bounded entry budget")
        if key in approved_missing:
            missing.append(approved_missing[key])
            continue
        raw, actual = checked_snapshot(ref, maximum)
        digest = actual["sha256"]
        entries.append(actual)
        if digest not in objects:
            used += len(raw)
            if used > total_maximum:
                raise ValueError("Evidence closure exceeds its explicit total-byte budget")
            target = staging / digest
            with target.open("xb") as stream:
                stream.write(raw)
            target.chmod(0o444)
            objects[digest] = len(raw)
        if seed.get("follow_json_references") is True:
            pending.extend(nested_references(document(raw)))
    unknown_exceptions = set(approved_missing) - seen
    if unknown_exceptions:
        raise ValueError("Unused unavailable-reference exceptions are forbidden")
    return entries, objects, missing


def build(seed_path, output, *, maximum=FILE_LIMIT, total_maximum=TOTAL_LIMIT):
    seed, seed_ref = Q._read_physical(seed_path)
    if (seed.get("schema") != "lighttpd-i12-artifact-selection-v1"
            or seed.get("reviewed_by") != "root" or not seed.get("publication_review")):
        raise ValueError("Artifact selection requires explicit Root review")
    output = Path(output).absolute()
    if ".." in output.parts or not output.is_relative_to(Q.EXTERNAL_ROOT):
        raise ValueError("Raw evidence output must use the configured external storage root")
    Q.SOURCES.physical_path(output.parent)
    if output.exists() or output.is_symlink():
        raise ValueError("Use a fresh evidence artifact directory")
    output.mkdir(mode=0o700)
    staging = output / "objects"
    staging.mkdir(mode=0o700)
    entries, objects, missing = collect(seed, staging, maximum, total_maximum)
    seed_raw, seed_ref = checked_snapshot(seed_ref, maximum)
    entries.append(seed_ref)
    if seed_ref["sha256"] not in objects:
        if sum(objects.values()) + len(seed_raw) > total_maximum:
            raise ValueError("Artifact selection exceeds the total-byte budget")
        objects[seed_ref["sha256"]] = len(seed_raw)
        selection_copy = staging / seed_ref["sha256"]
        selection_copy.write_bytes(seed_raw)
        selection_copy.chmod(0o444)
    manifest = {
        "schema": "lighttpd-i12-raw-artifact-v1", "selection": seed_ref,
        "revision_binding": seed["revision_binding"],
        "publication_review": seed["publication_review"],
        "files": sorted(entries, key=lambda ref: (ref["path"], ref["sha256"])),
        "objects": objects, "unavailable_references": missing,
        "raw_complete": not missing,
        "unique_bytes": sum(objects.values()),
        "scope": "Selected physical evidence; packaging does not qualify any original case.",
    }
    raw_manifest = (json.dumps(manifest, sort_keys=True, indent=2) + "\n").encode()
    if len(raw_manifest) > MANIFEST_LIMIT:
        raise ValueError("Evidence manifest exceeds its bounded budget")
    manifest_path = output / "manifest.json"
    manifest_path.write_bytes(raw_manifest)
    archive_path = output / "lighttpd-i12-raw.tar.gz"
    with archive_path.open("xb") as stream:
        with gzip.GzipFile(filename="", mode="wb", fileobj=stream, mtime=0) as compressed:
            with tarfile.open(fileobj=compressed, mode="w|") as archive:
                add_member(archive, "manifest.json", raw_manifest)
                for digest in sorted(objects):
                    add_member(archive, "objects/" + digest, (staging / digest).read_bytes())
    archive_ref = Q.reference(archive_path)
    verification = verify(archive_path, archive_ref["sha256"], maximum=maximum,
                          total_maximum=total_maximum)
    receipt = {"archive": archive_ref, "manifest": Q.reference(manifest_path),
               "objects": len(objects), "physical_paths": len(entries),
               "unavailable_references": len(missing), "unique_bytes": sum(objects.values()),
               "verification": verification}
    Q._exclusive_json(output / "package-receipt.json", receipt)
    return receipt


def read_member(archive, member, maximum):
    if not member.isfile() or member.linkname or member.size > maximum:
        raise ValueError("Archive must contain only bounded regular file members")
    stream = archive.extractfile(member)
    if stream is None:
        raise ValueError("Missing archive member content")
    with stream:
        raw = stream.read(maximum + 1)
    if len(raw) != member.size or len(raw) > maximum:
        raise ValueError("Archive member has an invalid content length")
    return raw


def verify_manifest(manifest, measured):
    if manifest.get("schema") != "lighttpd-i12-raw-artifact-v1" or manifest.get("objects") != measured:
        raise ValueError("Archive objects differ from the embedded manifest")
    for ref in manifest["files"]:
        if measured.get(ref["sha256"]) != ref["bytes"]:
            raise ValueError("Original producer reference is absent from the content-addressed archive")
    if manifest["unique_bytes"] != sum(measured.values()):
        raise ValueError("Archive manifest byte count differs")
    if manifest.get("raw_complete") is not (not manifest["unavailable_references"]):
        raise ValueError("Unavailable references cannot be marked as complete raw evidence")
    return {"verified": True, "objects": len(measured), "physical_paths": len(manifest["files"]),
            "unique_bytes": sum(measured.values()), "raw_complete": manifest["raw_complete"],
            "unavailable_references": len(manifest["unavailable_references"])}


def verify(path, expected_sha256, *, maximum=FILE_LIMIT, total_maximum=TOTAL_LIMIT):
    """Check actual retrieved bytes and every member; never extract untrusted paths."""
    if SHA256.fullmatch(expected_sha256) is None:
        raise ValueError("Expected archive SHA256 must be explicit")
    actual = Q.reference(path)
    if actual["sha256"] != expected_sha256:
        raise ValueError("Retrieved archive SHA256 differs from the published manifest")
    measured, names, manifest = {}, set(), None
    used = 0
    with tarfile.open(path, mode="r|gz") as archive:
        for member in archive:
            if member.name in names or len(names) >= ENTRY_LIMIT:
                raise ValueError("Duplicate or excessive archive members")
            names.add(member.name)
            if member.name == "manifest.json":
                manifest = json.loads(read_member(archive, member, MANIFEST_LIMIT))
                continue
            prefix, separator, digest = member.name.partition("/")
            if prefix != "objects" or not separator or SHA256.fullmatch(digest) is None:
                raise ValueError("Unexpected archive member name")
            raw = read_member(archive, member, maximum)
            used += len(raw)
            if used > total_maximum or hashlib.sha256(raw).hexdigest() != digest:
                raise ValueError("Archive object differs from its name or exceeds total-byte budget")
            measured[digest] = len(raw)
    if manifest is None:
        raise ValueError("Archive is missing its evidence manifest")
    return {**verify_manifest(manifest, measured), "archive": actual}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    modes = parser.add_subparsers(dest="mode", required=True)
    packing = modes.add_parser("build")
    packing.add_argument("--selection", type=Path, required=True)
    packing.add_argument("--output", type=Path, required=True)
    checking = modes.add_parser("verify")
    checking.add_argument("--archive", type=Path, required=True)
    checking.add_argument("--expected-sha256", required=True)
    args = parser.parse_args()
    result = (build(args.selection, args.output) if args.mode == "build"
              else verify(args.archive, args.expected_sha256))
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
