#!/usr/bin/env python3
"""Apply only the fixed apache-current capture closure with shared contracts.

This verifies selected Apache objects, including recursive delta bases. It does
not verify the complete cross-connector manifest. Source identity, disposable
export inventory, base bytes, modes, writes and application receipt retain the
unchanged shared capture_sources.apply contract. No runtime claim is made.
"""
import argparse
import importlib.util
import json
from pathlib import Path


SHARED_PATH = Path(__file__).resolve().parents[2] / "i12/capture_sources.py"
SPEC = importlib.util.spec_from_file_location("apache_i12_shared_capture_sources", SHARED_PATH)
SHARED = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(SHARED)
PROFILE = "apache-current"


class ApacheRegistry(SHARED.Registry):
    """Retain the shared resolver, limiting verification to Apache's closure."""

    def verify(self):
        profile = self.manifest["profiles"][PROFILE]
        if profile.get("required_source_identity_format") != "i12-disposable-source-copy-v2":
            raise ValueError("apache-current requires the complete v2 export identity")
        # Never reuse content from an earlier verification after files changed.
        self.cache.clear()
        for mapping in (profile["source_targets"], profile["capture_files"]):
            for name, entry in mapping.items():
                SHARED.relative(name)
                self.content(entry["sha256"])
        self.verification = {
            "profile": PROFILE,
            "scope": "selected_profile_transitive_object_closure",
            "verified_object_sha256": sorted(self.cache),
            "objects": len(self.cache),
            "profiles": 1,
            "global_manifest_verified": False,
            "capture_manifest_sha256": SHARED.digest(SHARED.plain(self.root / "manifest.json")),
            "source_only": True,
            "runtime_qualified": False,
        }
        return self.verification


def apply_apache(target, *, root=SHARED.HERE, repository=SHARED.REPOSITORY):
    """Use shared application and receipt unchanged for the sole admitted profile."""
    registry = ApacheRegistry(root, repository)
    receipt = SHARED.apply(registry, PROFILE, target)
    return {"application_receipt": receipt, "capture_verification": registry.verification}


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=("verify", "apply"))
    parser.add_argument("--source-copy", type=Path)
    args = parser.parse_args(argv)
    try:
        if args.action == "verify":
            result = ApacheRegistry().verify()
        elif args.source_copy is None:
            raise ValueError("apply needs --source-copy")
        else:
            result = apply_apache(args.source_copy)
        print(json.dumps(result, sort_keys=True))
    except (ValueError, KeyError, OSError, TypeError) as error:
        parser.exit(2, "Apache capture source rejected: " + str(error) + "\n")


if __name__ == "__main__":
    main()
