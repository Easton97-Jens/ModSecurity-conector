#!/usr/bin/env python3
"""Capture successful real GCC/Clang invocations, without rewriting source paths.

Build producers select this launcher as CC/CXX using an executable shim that
supplies --compiler. SONAR_NATIVE_CAPTURE_ROOT must be a private external run
directory. This helper does not invoke Sonar or claim complete target coverage.
"""

import argparse
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import re
import shlex
import shutil
import subprocess
import sys
import uuid


MAP_SPEC = importlib.util.spec_from_file_location("sonar_source_mapping", Path(__file__).with_name("source_mapping.py"))
SOURCE_MAPPING = importlib.util.module_from_spec(MAP_SPEC)
MAP_SPEC.loader.exec_module(SOURCE_MAPPING)


IMPLICIT_COMPILER_ENV = {
    "CPATH", "C_INCLUDE_PATH", "CPLUS_INCLUDE_PATH", "OBJC_INCLUDE_PATH", "INCLUDE",
    "COMPILER_PATH", "GCC_EXEC_PREFIX", "LIBRARY_PATH", "GCC_SPECS", "SDKROOT",
    "MACOSX_DEPLOYMENT_TARGET", "LD_PRELOAD", "LD_AUDIT", "LD_LIBRARY_PATH", "LD_RUN_PATH",
    "DEPENDENCIES_OUTPUT", "SUNPRO_DEPENDENCIES", "SOURCE_DATE_EPOCH",
    "CCC_OVERRIDE_OPTIONS",
}


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def absolute(value, cwd):
    path = Path(value)
    return (cwd / path).resolve() if not path.is_absolute() else path.resolve()


def expand(arguments, cwd, responses, stack=()):
    result = []
    for argument in arguments:
        if not argument.startswith("@"):
            result.append(argument)
            continue
        path = absolute(argument[1:], cwd)
        if path in stack or len(stack) >= 8:
            raise ValueError("recursive or deeply nested compiler response file")
        responses[str(path)] = digest(path)
        result.extend(expand(shlex.split(path.read_text()), cwd, responses, (*stack, path)))
    return result


def dependencies(path, cwd):
    text = path.read_text().replace("\\\n", " ")
    _, separator, values = text.partition(":")
    if not separator:
        raise ValueError("compiler dependency output has no target")
    return {str(absolute(value, cwd)): digest(absolute(value, cwd))
            for value in shlex.split(values)}


def capture(compiler, arguments, root):
    if any(value and (name in IMPLICIT_COMPILER_ENV or name.startswith("DYLD_"))
           for name, value in os.environ.items()):
        raise ValueError("undeclared implicit compiler environment is forbidden")
    cwd = Path.cwd().resolve()
    executable = shutil.which(compiler)
    if executable is None:
        raise ValueError("real compiler is unavailable")
    executable = str(Path(executable).resolve())
    root = root.resolve(strict=True)
    SOURCE_MAPPING.verify_trusted_directory(root)
    if root.stat().st_mode & 0o077:
        raise ValueError("capture root must have private permissions")
    responses = {}
    expanded = expand(arguments, cwd, responses)
    if any(arg.startswith(("-Wp,", "-Xpreprocessor", "-specs=", "--specs="))
           for arg in expanded):
        raise ValueError("indirect compiler input/options require a dedicated producer contract")
    mapping_receipt = None
    if os.environ.get("SONAR_NATIVE_SOURCE_MAP"):
        manifest_path = Path(os.environ["SONAR_NATIVE_SOURCE_MAP"]).resolve(strict=True)
        arguments, mapping_receipt = SOURCE_MAPPING.prepare(executable, arguments, cwd, root, manifest_path)
        if mapping_receipt is None:
            manifest = json.loads(manifest_path.read_text())
            if any(str(absolute(argument, cwd)) in manifest["files"]
                   for argument in expanded if not argument.startswith("-")):
                raise ValueError("mapped source hidden inside response files is not supported")
        expanded = expand(arguments, cwd, responses)
    sources = [absolute(arg, cwd) for arg in expanded
               if not arg.startswith("-") and Path(arg).suffix in {".c", ".cc", ".cpp", ".cxx", ".C"}]
    output = None
    for index, argument in enumerate(expanded):
        if argument == "-o" and index + 1 < len(expanded):
            output = absolute(expanded[index + 1], cwd)
        elif argument.startswith("-o") and len(argument) > 2:
            output = absolute(argument[2:], cwd)
    # Compiler feature probes remain real invocations but cannot establish a
    # product translation unit. Unsupported compile/link shapes fail at export.
    record_id = uuid.uuid4().hex
    depfile = root / (record_id + ".d")
    executed = [executable, *arguments]
    tracked_compile = len(sources) == 1 and "-c" in expanded and output is not None
    tracked_link = not sources and output is not None and not any(
        flag in expanded for flag in ("-c", "-E", "-S"))
    linkmap = root / (record_id + ".map")
    if tracked_compile:
        executed += ["-MD", "-MF", str(depfile)]
    elif tracked_link:
        executed += ["-Wl,-Map=" + str(linkmap)]
    before = {str(path): digest(path) for path in sources if path.is_file()}
    status = subprocess.run(executed, check=False).returncode
    if status:
        return status
    if output is None or not output.is_file():
        return 0
    headers = dependencies(depfile, cwd) if tracked_compile else {}
    if any(digest(path) != value for path, value in before.items()):
        raise ValueError("source changed during compilation")
    if any(digest(path) != value for path, value in responses.items()):
        raise ValueError("response file changed during compilation")
    if not tracked_compile and any(
            arg in {"-T", "--script", "-Xlinker"}
            or arg.startswith(("-Wl,@", "-Wl,-T", "-Wl,--script"))
            or (arg.startswith("-Wl,") and any(suffix in arg for suffix in (".o", ".a", ".lo")))
            for arg in expanded):
        raise ValueError("indirect link inputs require a dedicated producer contract")
    input_paths = {absolute(arg, cwd) for arg in expanded
                   if not arg.startswith("-") and Path(arg).suffix in {".o", ".a", ".so", ".lo"}
                   and absolute(arg, cwd) != output}
    if any(not path.is_file() for path in input_paths):
        raise ValueError("original explicit compiler input is no longer available")
    inputs = {str(path): digest(path) for path in input_paths}
    loaded = {}
    internal_transients = {}
    lto_context = None
    if (tracked_link and os.environ.get("SONAR_NATIVE_LTO_CONTEXT") == "apache-gcc-native-driver"
            and any(argument.startswith("-flto") for argument in expanded)):
        if (not re.search(r"(?:^|-)gcc(?:-\d+)?$", Path(executable).name)
                or not any(argument.startswith("-flto") for argument in expanded)):
            raise ValueError("Apache internal LTO context requires its actual GCC driver/LTO flags")
        manifest_path = Path(os.environ["SONAR_NATIVE_SOURCE_MAP"]).resolve(strict=True)
        manifest = json.loads(manifest_path.read_text())
        SOURCE_MAPPING.verify_manifest(manifest)
        producer = Path(manifest["checkout"]) / "connectors/apache/build/apxs-wrapper.in"
        temporary = Path(os.environ["TMPDIR"]).resolve(strict=True)
        if (manifest["producer"]["path"] != str(producer)
                or temporary != root.parent / "compiler-tmp" or temporary.is_relative_to(Path(manifest["checkout"]))):
            raise ValueError("internal LTO context is not the admitted private Apache native seam")
        lto_context = {"mode": "apache-gcc-native-driver", "compiler_tmpdir": str(temporary),
                       "source_map": str(manifest_path), "source_map_sha256": digest(manifest_path),
                       "producer": manifest["producer"]}
    if tracked_link:
        for line in linkmap.read_text().splitlines():
            if line.startswith("LOAD "):
                path = absolute(line[5:], cwd)
                if not path.is_file():
                    reason = None
                    if re.fullmatch(r"[^/]+\.ltrans[0-9]+\.ltrans\.o", path.name):
                        reason = "gcc-lto-intermediate-not-retained"
                    elif re.fullmatch(r"cc[A-Za-z0-9]+\.debug\.temp\.o", path.name):
                        reason = "gcc-lto-debug-auxiliary-not-retained"
                    if (lto_context and path.is_relative_to(Path(lto_context["compiler_tmpdir"]))
                            and reason is not None
                            and str(path) not in inputs):
                        internal_transients[str(path)] = reason
                        continue
                    raise ValueError("link map refers to an unavailable input")
                loaded[str(path)] = digest(path)
    retained = {}
    if tracked_link:
        destination = root / "retained" / record_id
        destination.mkdir(parents=True, mode=0o700)
        # Go's external linker deletes numbered objects and moves/postprocesses
        # a.out after this compiler returns. Preserve the actual bytes now;
        # export still requires an explicit, validated producer relationship.
        for index, path in enumerate([output, *(Path(name) for name in inputs)]):
            copy = destination / str(index)
            shutil.copyfile(path, copy)
            if digest(copy) != digest(path):
                raise ValueError("link input/output changed while retained")
            retained[str(path)] = str(copy)
    record = {"schema": 1, "directory": str(cwd), "arguments": executed,
              "expanded_arguments": [executable, *expanded], "compiler_sha256": digest(executable),
              "sources": before, "dependencies": headers, "response_files": responses,
              "inputs": inputs, "output": str(output), "output_sha256": digest(output),
              "library_options": [arg for arg in expanded if arg.startswith(("-l", "-L"))],
              "linker_inputs": loaded,
              "retained_files": retained,
              "source_mapping": mapping_receipt,
              "compiler_internal_transients": internal_transients,
              "lto_context": lto_context,
              "link_map": {str(linkmap): digest(linkmap)} if tracked_link else {},
              "kind": "compile" if tracked_compile else "link" if tracked_link else "unsupported"}
    temporary = root / (record_id + ".pending")
    temporary.write_text(json.dumps(record, sort_keys=True) + "\n")
    temporary.rename(root / (record_id + ".json"))
    return 0


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--compiler", required=True)
    parser.add_argument("arguments", nargs=argparse.REMAINDER)
    args = parser.parse_args()
    arguments = args.arguments[1:] if args.arguments[:1] == ["--"] else args.arguments
    try:
        return capture(args.compiler, arguments, Path(os.environ["SONAR_NATIVE_CAPTURE_ROOT"]))
    except (OSError, ValueError, KeyError, subprocess.SubprocessError) as error:
        print(f"native compiler capture failed: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
