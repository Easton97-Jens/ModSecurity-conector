#!/usr/bin/env python3
"""Update explicitly reviewed V3.2 inheritance digests; dry-run by default.
Caller must complete selected-file Secrets preflight before invocation.
Writes require caller-coordinated exclusive ownership of the selected files.
Input checks are optimistic; atomic replacement is not a kernel compare-and-swap.
No policy-content, authentication, scanner, hook, trust or Git writes.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import stat
import subprocess
import sys
import tempfile
import tomllib
PARENT = Path(__file__).absolute().parents[2]
LIMIT = 1_048_576
HASH = re.compile(r"[0-9a-f]{64}\Z")
TARGETS = {
 "parent-catalog": ("parent", ".codex/inheritance-manifest.toml"),
 "framework-template": ("framework", ".codex/inheritance-templates/framework-inheritance-manifest.toml"),
 "mrts-template": ("mrts", ".codex/inheritance-templates/mrts-inheritance-manifest.toml"),
 "framework": ("framework", ".codex/inheritance-manifest.toml"),
 "mrts": ("mrts", ".codex/inheritance-manifest.toml"),
}
REPOSITORIES = {"parent": "Easton97-Jens/ModSecurity-conector", "framework": "Easton97-Jens/ModSecurity-test-Framework", "mrts": "Easton97-Jens/MRTS"}
class Refused(ValueError):
 """Review, identity, source or filesystem precondition failed."""
def digest(data):
 return hashlib.sha256(data).hexdigest()
def safe_path(path):
 path = Path(os.path.abspath(path))
 for part in [*reversed(path.parents), path]:
  if part.is_symlink():
   raise Refused("symlink path is not permitted")
 return path
def read_regular(path):
 safe_path(path)
 fd = os.open(path, os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK)
 try:
  before = os.fstat(fd)
  if not stat.S_ISREG(before.st_mode) or before.st_size > LIMIT or before.st_nlink != 1:
   raise Refused("input must be a bounded, singly linked regular file")
  with os.fdopen(fd, "rb", closefd=False) as stream:
   data = stream.read(LIMIT + 1)
  after = os.fstat(fd)
  signature = lambda s: (s.st_dev, s.st_ino, s.st_mode, s.st_size, s.st_mtime_ns, s.st_ctime_ns)
  if signature(before) != signature(after) or len(data) != before.st_size:
   raise Refused("input changed during read")
  return data, signature(after)
 finally:
  os.close(fd)
def git_identity(root, role):
 safe_path(root)
 def query(*args):
  result = subprocess.run(["rtk", "bypass", "git", "-C", str(root), *args], stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, check=False)
  if result.returncode:
   raise Refused("repository identity cannot be verified")
  return result.stdout.decode("utf-8").strip()
 if query("rev-parse", "--show-toplevel") != str(root):
  raise Refused("selected root is not the repository top-level")
 identity = REPOSITORIES[role]
 allowed = {f"https://github.com/{identity}", f"https://github.com/{identity}.git", f"git@github.com:{identity}", f"git@github.com:{identity}.git", f"ssh://git@github.com/{identity}", f"ssh://git@github.com/{identity}.git"}
 if query("remote", "get-url", "origin") not in allowed:
  raise Refused("repository origin does not match the selected role")
def parse(data):
 try:
  return tomllib.loads(data.decode("utf-8"))
 except (ValueError, UnicodeError) as exc:
  raise Refused("invalid UTF-8 TOML") from exc
def policies(data, table):
 rows = data.get(table)
 if not isinstance(rows, list) or not rows:
  raise Refused("required policy table is absent")
 result = {}
 for row in rows:
  if not isinstance(row, dict) or not isinstance(row.get("id"), str) or row["id"] in result:
   raise Refused("invalid or duplicate policy ID")
  result[row["id"]] = row
 return result
def replace_pins(data, table, field, changes):
 text = data.decode("utf-8")
 starts = list(re.finditer(r"(?m)^\[\[" + re.escape(table) + r"\]\][ \t]*(?:\r?\n|$)", text))
 found = set()
 for match in reversed(starts):
  end_match = re.search(r"(?m)^\[", text[match.end():])
  end = match.end() + end_match.start() if end_match else len(text)
  block = text[match.start():end]
  policy_id = parse(block.encode())[table][0].get("id")
  if policy_id not in changes:
   continue
  expression = re.compile(r'(?m)^(?P<prefix>' + re.escape(field) + r'[ \t]*=[ \t]*")(?P<sha>[0-9a-f]{64})(?P<suffix>"[ \t]*(?:#[^\r\n]*)?\r?$)')
  slots = list(expression.finditer(block))
  if len(slots) != 1:
   raise Refused("selected digest is not a unique canonical quoted SHA-256")
  slot = slots[0]
  changed = block[:slot.start("sha")] + changes[policy_id] + block[slot.end("sha"):]
  text = text[:match.start()] + changed + text[end:]
  found.add(policy_id)
 if found != set(changes):
  raise Refused("reviewed policy absent from selected target")
 return text.encode("utf-8")
def reviewed_values(values):
 result = {}
 for value in values:
  policy_id, separator, sha = value.partition("=")
  if not separator or not policy_id.startswith("PARENT-") or not HASH.fullmatch(sha) or policy_id in result:
   raise Refused("reviewed policies require unique PARENT-ID=lowercase-SHA256 values")
  result[policy_id] = sha
 if not result:
  raise Refused("at least one explicitly reviewed policy is required")
 return result
def prepare(parent, target_name, child_root, expected_manifest, reviewed):
 if not HASH.fullmatch(expected_manifest):
  raise Refused("expected manifest SHA-256 required")
 parent = safe_path(parent)
 git_identity(parent, "parent")
 role, relative = TARGETS[target_name]
 if target_name in {"framework", "mrts"}:
  if child_root is None:
   raise Refused("child target requires explicit repository root")
  root = safe_path(child_root)
  git_identity(root, role)
 else:
  if child_root is not None:
   raise Refused("child root forbidden for Parent-owned targets")
  root = parent
 target = root / relative
 catalog_path = parent / ".codex/inheritance-manifest.toml"
 catalog_bytes, catalog_stat = read_regular(catalog_path)
 catalog_data = parse(catalog_bytes)
 if catalog_data.get("schema_version") != 2 or catalog_data.get("repository") != "parent":
  raise Refused("unsupported Parent catalog schema/role")
 catalog = policies(catalog_data, "policies")
 original, target_stat = read_regular(target)
 if digest(original) != expected_manifest:
  raise Refused("manifest does not match reviewed input SHA-256")
 data = parse(original)
 if data.get("schema_version") != 2 or data.get("repository") != role:
  raise Refused("target schema/repository role does not match")
 table, field = ("policies", "sha256") if target_name == "parent-catalog" else ("inherit", "parent_sha256")
 target_policies = policies(data, table)
 snapshots = {catalog_path: (catalog_bytes, catalog_stat), target: (original, target_stat)}
 changes = []
 for policy_id, approved_sha in reviewed.items():
  if policy_id not in catalog or policy_id not in target_policies:
   raise Refused("reviewed policy unknown or absent from target")
  row = catalog[policy_id]
  if target_name != "parent-catalog" and row.get("inheritable") is not True:
   raise Refused("selected canonical policy is not inheritable")
  source = row.get("source")
  if not isinstance(source, str) or not source.startswith(".codex/context/") or ".." in Path(source).parts:
   raise Refused("canonical policy source outside fixed context root")
  source_path = safe_path(parent / source)
  source_bytes, source_stat = read_regular(source_path)
  observed = digest(source_bytes)
  if observed != approved_sha:
   raise Refused("source bytes do not match explicitly reviewed SHA-256")
  if target_name != "parent-catalog" and row.get("sha256") != observed:
   raise Refused("canonical source/catalog disagree; review Parent catalog first")
  old = target_policies[policy_id].get(field)
  if not isinstance(old, str) or not HASH.fullmatch(old):
   raise Refused("target digest invalid")
  snapshots[source_path] = (source_bytes, source_stat)
  changes.append({"id": policy_id, "source": source, "before": old, "after": observed})
 replacement = replace_pins(original, table, field, reviewed)
 expected = {key: dict(value) for key, value in target_policies.items()}
 for policy_id, sha in reviewed.items():
  expected[policy_id][field] = sha
 if policies(parse(replacement), table) != expected:
  raise Refused("replacement changes unselected policy semantics")
 return {"target": target, "original": original, "replacement": replacement, "snapshots": snapshots, "changes": changes, "mode": stat.S_IMODE(target_stat[2])}
def verify_unchanged(plan):
 for path, expected in plan["snapshots"].items():
  if read_regular(path) != expected:
   raise Refused("reviewed input changed before writing")
def apply(plan):
 verify_unchanged(plan)
 if plan["replacement"] == plan["original"]:
  return
 target = plan["target"]
 temporary = None
 try:
  fd, name = tempfile.mkstemp(prefix=".inheritance-update-", dir=target.parent)
  temporary = Path(name)
  with os.fdopen(fd, "wb") as stream:
   os.fchmod(stream.fileno(), plan["mode"])
   stream.write(plan["replacement"])
   stream.flush()
   os.fsync(stream.fileno())
  verify_unchanged(plan)
  os.replace(temporary, target)
  temporary = None
  if read_regular(target)[0] != plan["replacement"]:
   raise Refused("post-write verification failed; inspect target before follow-up")
 finally:
  if temporary is not None:
   temporary.unlink(missing_ok=True)
def main(argv=None):
 parser = argparse.ArgumentParser(description=__doc__)
 parser.add_argument("--target", required=True, choices=sorted(TARGETS))
 parser.add_argument("--child-root", type=Path)
 parser.add_argument("--expected-manifest-sha256", required=True)
 parser.add_argument("--reviewed-policy", action="append", default=[], metavar="PARENT-ID=SHA256")
 parser.add_argument("--write", action="store_true", help="write reviewed digest fields; default dry-run")
 args = parser.parse_args(argv)
 try:
  plan = prepare(PARENT, args.target, args.child_root, args.expected_manifest_sha256, reviewed_values(args.reviewed_policy))
  verify_unchanged(plan)
  if args.write:
   apply(plan)
  print(json.dumps({"status": "written" if args.write else "dry_run", "target": str(plan["target"]), "before_sha256": digest(plan["original"]), "after_sha256": digest(plan["replacement"]), "changed": plan["replacement"] != plan["original"], "policies": plan["changes"]}, sort_keys=True))
  return 0
 except (Refused, OSError, UnicodeError, KeyError) as exc:
  print(json.dumps({"status": "refused", "reason": str(exc) if isinstance(exc, Refused) else type(exc).__name__}), file=sys.stderr)
  return 1
if __name__ == "__main__":
 raise SystemExit(main())
