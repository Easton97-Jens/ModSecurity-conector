"""Fresh ordinary or source-observed NGX module; no hosts or old-output writes."""
import argparse, ast, hashlib, json, re, shlex, subprocess, shutil, os, threading
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

def sha(path): return hashlib.sha256(Path(path).read_bytes()).hexdigest()
def build(a):
    w=Path(a.source); base=Path(a.base); out=Path(a.output)
    out.mkdir(mode=0o700); steps=[]; receipt_lock=threading.Lock()
    receipt={"scope":"fresh current Parent33TU module, no host/runtime qualification", "source_snapshot": str(w), "build_recipe_sha256": sha(__file__), "parent_sha":a.parent_sha,"instrumented":a.instrumented,"steps":steps}
    def run(label,argv,cwd=out):
        cmd=["rtk","proxy",*map(str,argv)]; r=subprocess.run(cmd,cwd=cwd,capture_output=True)
        (out/(label+".stdout")).write_bytes(r.stdout);(out/(label+".stderr")).write_bytes(r.stderr)
        with receipt_lock:
            steps.append({"argv":cmd,"cwd":str(cwd),"exit":r.returncode})
            (out/"receipt.json").write_text(json.dumps(receipt,indent=2)+"\n")
        if r.returncode: raise RuntimeError(label+" failed; retained logs")
        return r.stdout.decode()
    if run("head",["git","rev-parse","HEAD"],Path(a.checkout)).strip()!=a.parent_sha: raise ValueError("fresh merged head differs")
    build=base/"nginx-src"; makefile=build/"objs/Makefile"; text=makefile.read_text()
    receipt["makefile_sha256"]=sha(makefile)
    receipt["sdk_library_sha256"]=sha(base/"sdk/lib/libmodsecurity.so.3.0.14")
    if receipt["sdk_library_sha256"]!="32257230b8f378987ba1204049dcc1e23927fd44c8778e09d41805ad705c3407": raise ValueError("reviewed SDK3.0.14 library pin differs")
    receipt["sdk_version"]="3.0.14"
    receipt["nginx_binary_sha256"]=sha(base/"prefix/sbin/nginx")
    if receipt["nginx_binary_sha256"]!="0d2287b344a1af4c6cc986dd915c09c60f3c942ec8ae76f8bdc5456506939746": raise ValueError("reviewed native NGX1.31.6 host pin differs")
    receipt["old_baseline_module_sha256"]=sha(base/"prefix/modules/ngx_http_modsecurity_module.so")
    cflags=shlex.split(re.search(r"^CFLAGS = (.*)$",text,re.M).group(1))
    if "-Werror" not in cflags or "-std=c17" not in cflags: raise ValueError("native warning/C17 contract absent")
    inc=shlex.split(re.search(r"^ALL_INCS = (.*?)\n\n",text,re.M|re.S).group(1).replace("\\\n"," "))
    inc=[str(w/Path(item).relative_to(base/"source-inputs")) if item.startswith(str(base/"source-inputs")) else item for item in inc]
    match=re.search(r"\t\$\(LINK\) -o objs/ngx_http_modsecurity_module\.so ([\s\S]*?)\n\n",text)
    if not match: raise ValueError("native link recipe absent")
    original=shlex.split("cc -o objs/ngx_http_modsecurity_module.so "+match.group(1).replace("\\\n"," "))
    objects=[item for item in original if item.endswith(".o")]
    if len(objects)!=34: raise ValueError("expected exact33 Parent TUs plus one generated NGX registration TU")
    overlays=None; own=w/".i12-capture/nginx"
    observer=w/"ci/runtime/lifecycle"
    if a.instrumented:
        receipt["source_application_receipt"] = json.loads((w/"i12-source-application-receipt.json").read_text())
    inputs={}; fresh={}; rows=[]
    frozen_headers={}
    for directory in [w/"common/include",w/"connectors/nginx/src",w/"ci/runtime/lifecycle",base/"sdk/include",build/"src",build/"objs",own]:
        for header in directory.rglob("*.h"):
            if header.is_file() and not header.is_symlink(): frozen_headers[str(header.resolve())]=sha(header)
    for header in observer.glob("*.h"): frozen_headers[str(header.resolve())]=sha(header)
    receipt["frozen_headers_sha256"]=frozen_headers
    receipt["observer_source"]=str(observer)

    compilation_jobs=[]
    for i,obj in enumerate(objects):
        # Parse the actual generated native compile recipe, retaining full diagnostics.
        block=re.search(r"^"+re.escape(obj)+r":.*?\n\t\$\(CC\) (.*?)(?:\n\n|\Z)",text,re.M|re.S)
        if not block: raise ValueError("object native compiler recipe absent: "+obj)
        args=shlex.split(block.group(1).replace("\\\n"," "))
        src=args[-1]
        if src.startswith(str(base/"connector-src")):
            current=w/"connectors/nginx"/Path(src).relative_to(base/"connector-src")
        elif src.startswith(str(base/"source-inputs")):
            current=w/Path(src).relative_to(base/"source-inputs")
        else: current=(build/src).resolve()
        inputs[str(current)]=sha(current)
        chosen=overlays/current.name if overlays is not None and (overlays/current.name).exists() else current
        target=out/(f"{i:02d}-"+Path(obj).name)
        command=["cc","-c","-fPIC",*cflags,*inc,"-I"+str(w/"connectors/nginx/src"),"-I"+str(own),"-I"+str(observer),"-MMD","-MF",str(target)+".d","-o",target,chosen]
        compilation_jobs.append((f"compile-{i:02d}",command))
        fresh[obj]=str(target); rows.append({"source":str(current),"source_sha256":inputs[str(current)],"compiled_source":str(chosen),"compiled_source_sha256":sha(chosen),"object":str(target)})
    receipt["compile_jobs"]=min(len(compilation_jobs),a.jobs)
    with ThreadPoolExecutor(max_workers=receipt["compile_jobs"]) as executor:
        futures=[executor.submit(run,label,command,build) for label,command in compilation_jobs]
        failures=[]
        for future in futures:
            try: future.result()
            except Exception as error: failures.append(str(error))
    if failures: raise RuntimeError("; ".join(failures))
    for row in rows: row["object_sha256"]=sha(row["object"])
    generated=[row for row in rows if row["source"].endswith("ngx_http_modsecurity_module_modules.c")]
    parent=[row for row in rows if row not in generated]
    if len(parent)!=33 or len(generated)!=1: raise ValueError("Parent/generated translation-unit scope mismatch")
    receipt["compiled_parent_units"]=parent
    receipt["compiled_nginx_generated_units"]=generated
    # Retain each actual preprocessor dependency hash; includes are not inferred from a build label.
    dependencies={}
    for dep in out.glob("*.o.d"):
        tokens=shlex.split(dep.read_text().replace("\\\n"," ").split(":",1)[1])
        for token in tokens:
            path=Path(token); path=path if path.is_absolute() else build/path
            dependencies[str(path.resolve())]=sha(path)
    receipt["dependencies_sha256"]=dependencies
    link=[fresh.get(x,x) for x in original]; link[2]=str(out/"ngx_http_modsecurity_module.so")
    if a.instrumented:
        symboltree=ast.parse((w/"tests/test_native_lifecycle_observer.py").read_text())
        symbols=next(ast.literal_eval(n.value) for n in symboltree.body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=="SYMBOLS" for t in n.targets))
        # The exact capture observer predates finalize_and_snapshot (current shared tests:38).
        symbols=tuple(symbol for symbol in symbols if symbol != "msconnector_runtime_transaction_finalize_and_snapshot")
        if len(symbols)!=37 or len(set(symbols))!=37: raise ValueError("reviewed current37 wrapper surface changed")
        receipt["wrapped_symbols"]=symbols
        for src,name,compiler,standard in [(observer/"native-lifecycle-observer.c","observer","cc","c17"),(observer/"native-lifecycle-sdk.cpp","sdk-observer","c++","c++17")]:
            inputs[str(src)]=sha(src)
            run(name+"-compile",[compiler,"-std="+standard,"-Wall","-Wextra","-Werror","-fPIC","-pthread","-I"+str(w/"common/include"),"-isystem",base/"sdk/include","-c",src,"-o",out/(name+".o")])
            link.append(str(out/(name+".o")))
        link.extend(["-lstdc++","-pthread",*("-Wl,--wrap="+s for s in symbols)])
    run("module-link",link,build)
    dynamic=run("dynamic-symbols",["nm","-D",out/"ngx_http_modsecurity_module.so"])
    run("relocations",["readelf","-Wr",out/"ngx_http_modsecurity_module.so"])
    disassembly=run("disassembly",["objdump","-dr",out/"ngx_http_modsecurity_module.so"])
    run("dynamic-section",["readelf","-d",out/"ngx_http_modsecurity_module.so"])
    relocations={}
    for i,row in enumerate(rows): relocations[row["source"]]=run(f"object-{i:02d}-relocations",["objdump","-r",row["object"]])
    if a.instrumented:
        if not all(re.search(r"\bT __wrap_"+re.escape(symbol)+r"$",dynamic,re.M) for symbol in symbols): raise ValueError("wrapper export absent")
        mandatory={"ngx_http_modsecurity_module.c":["msconnector_transaction_contract_init","msc_new_transaction_with_id","msconnector_transaction_contract_cleanup","msc_transaction_cleanup"],
            "ngx_http_modsecurity_access.c":["msc_process_request_headers","msc_append_request_body","msc_process_request_body"],
            "ngx_http_modsecurity_header_filter.c":["msc_process_response_headers"],
            "ngx_http_modsecurity_body_filter.c":["msc_append_response_body","msc_process_response_body"],
            "ngx_http_modsecurity_log.c":["msconnector_transaction_contract_finish","msc_process_logging"]}
        coverage=[]
        for name,required in mandatory.items():
            sources=[path for path in relocations if Path(path).name==name]
            if len(sources)!=1: raise ValueError("exact caller TU absent")
            for symbol in required:
                pre=[line.strip() for line in relocations[sources[0]].splitlines() if re.search(r"\b"+re.escape(symbol)+r"(?:[-+]|\s|$)",line)]
                calls=[line.strip() for line in disassembly.splitlines() if re.search(r"\bcall\b.*<__wrap_"+re.escape(symbol)+r"(?:@plt)?>",line)]
                if not pre or not calls: raise ValueError("genuine native caller/wrapped relocation absent: "+symbol)
                coverage.append({"caller_source":sources[0],"symbol":symbol,"genuine_object_relocations":pre,"linked_wrapped_calls":calls})
        receipt["mandatory_native_call_coverage"]=coverage
        receipt["coverage_limit"]="Static source/object/caller wiring only; actual per-case calls/returns require independent host raws. Same-object Common internal calls can remain unwrapped and cannot become synthetic API counts."
    if any(sha(path)!=value for path,value in {**frozen_headers,**inputs,**dependencies}.items()): raise ValueError("build input changed during compilation")
    if sha(base/"prefix/modules/ngx_http_modsecurity_module.so")!=receipt["old_baseline_module_sha256"]: raise ValueError("old module modified")
    if run("head-after",["git","rev-parse","HEAD"],Path(a.checkout)).strip()!=a.parent_sha: raise ValueError("merged head changed during build")
    receipt["module_sha256"]=sha(out/"ngx_http_modsecurity_module.so")
    prefix=out/"prefix"
    (prefix/"sbin").mkdir(parents=True,mode=0o700);(prefix/"modules").mkdir(mode=0o700)
    shutil.copyfile(base/"prefix/sbin/nginx",prefix/"sbin/nginx");(prefix/"sbin/nginx").chmod(0o500)
    shutil.copyfile(out/"ngx_http_modsecurity_module.so",prefix/"modules/ngx_http_modsecurity_module.so");(prefix/"modules/ngx_http_modsecurity_module.so").chmod(0o400)
    if sha(prefix/"sbin/nginx")!=receipt["nginx_binary_sha256"] or sha(prefix/"modules/ngx_http_modsecurity_module.so")!=receipt["module_sha256"]: raise ValueError("fresh prefix sealing differs")
    receipt["fresh_prefix"]=str(prefix)
    receipt["library_binding"]="Use separately pinned SDK3.0.14 read-only library directory; no old module/source relabeling."
    receipt["status"]="BUILD_PASS_RUNTIME_NOT_EXECUTED"
    receipt["full_lifecycle_qualified"]=False
    (out/"receipt.json").write_text(json.dumps(receipt,indent=2)+"\n")
    print(json.dumps({"status":receipt["status"],"module_sha256":receipt["module_sha256"]}))



def main():
    parser = argparse.ArgumentParser(description=__doc__)
    for name in ("source", "base", "output", "parent-sha"):
        parser.add_argument("--" + name, required=True)
    parser.add_argument("--jobs", type=int, default=8)
    args = parser.parse_args()
    checkout = Path(args.source).resolve(strict=True)
    output = Path(args.output).resolve()
    storage = Path("/var/tmp/codex/ModSecurity-conector")
    if storage not in output.parents or output.exists() or not 1 <= args.jobs <= 8:
        parser.error("fresh external output and 1..8 jobs required")
    output.mkdir(parents=True, mode=0o755)
    def git(*argv):
        result = subprocess.run(["rtk", "proxy", "git", *argv], cwd=checkout,
                                check=True, capture_output=True)
        return result.stdout
    if git("rev-parse", "HEAD").decode().strip() != args.parent_sha:
        raise ValueError("checkout HEAD differs from required exact head")
    scope = ["common", "connectors/nginx", "connectors/profile_registry.h", "connectors/profile_registry.c",
             "ci/runtime/lifecycle", "tests/test_native_lifecycle_observer.py", "tests/fixtures/nginx_worker_self_maps.c",
             "tests/fixtures/nginx_common_input_fault.c", "tests/fixtures/nginx_engine_budget_fault.c",
             "tests/fixtures/nginx_transaction_fault.c"]
    # Evidence records the real checkout state; source scopes must remain clean.
    tracked = git("ls-files", "-z", "--", *scope).decode().split("\0")
    diff = git("diff", "HEAD", "--", *scope)
    (output / "checkout-source.diff").write_bytes(diff)
    (output / "checkout-status.txt").write_bytes(git("status", "--porcelain=v1"))
    # NGINX-owned untracked harnesses are allowed, never copied as product input.
    if diff:
        raise ValueError("tracked build inputs differ from exact checkout HEAD")
    manifest = checkout / "ci/runtime/lifecycle/i12/manifest.json"
    baseline = json.loads(manifest.read_text())["delivery_product_baseline"]
    snapshots = {}
    for variant in ("ordinary", "observed"):
        snapshot = output / ("source-" + variant)
        snapshot.mkdir()
        for name in filter(None, tracked):
            source = checkout / name
            if source.is_symlink() or not source.is_file():
                raise ValueError("source must be a physical regular file: " + name)
            target = snapshot / name
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(source, target)
        marker = {"format": "i12-disposable-source-copy-v1", "path": str(snapshot),
                  "disposable": True, "parent_sha": baseline}
        (snapshot / ".i12-disposable-source-copy.json").write_text(json.dumps(marker) + "\n")
        if variant == "observed":
            command = ["rtk", "proxy", "python3", str(checkout / "ci/runtime/lifecycle/i12/capture_sources.py"),
                       "apply", "--profile", "nginx", "--source-copy", str(snapshot)]
            applied = subprocess.run(command, capture_output=True)
            (output / "source-application.stdout").write_bytes(applied.stdout)
            (output / "source-application.stderr").write_bytes(applied.stderr)
            if applied.returncode:
                raise RuntimeError("source capture failed; retained logs")
            # Additional NGINX-only state capture is separate from shared capture.
            extra = {"shared_capture_receipt_sha256": sha(snapshot / "i12-source-application-receipt.json"),
                     "header_sha256": sha(checkout / "ci/runtime/lifecycle/i12/nginx/host_state.h"), "files": {}}
            shutil.copyfile(checkout / "ci/runtime/lifecycle/i12/nginx/host_state.h",
                            snapshot / "connectors/nginx/src/i12-nginx-host-state.h")
            patches = {
                "ngx_http_modsecurity_access.c": [
                    ("    ret = msc_process_request_body(ctx->modsec_transaction);",
                     '    ngxi12_body_state(ctx, "request_before_native_finalize", NULL);\n    ret = msc_process_request_body(ctx->modsec_transaction);'),
                    ("    if (r->request_body != NULL && r->request_body->temp_file != NULL) {",
                     '    ngxi12_body_state(ctx, "request_body_path", NULL);\n    if (r->request_body != NULL && r->request_body->temp_file != NULL) {')],
                "ngx_http_modsecurity_body_filter.c": [
                    ("    return ngx_http_modsecurity_append_response_body_buffer(r, ctx, mcf,",
                     '    ngxi12_body_state(ctx, "response_buffer", chain->buf);\n    return ngx_http_modsecurity_append_response_body_buffer(r, ctx, mcf,')]
            }
            for filename, changes in patches.items():
                target = snapshot / "connectors/nginx/src" / filename
                before = sha(target)
                text = target.read_text()
                text = '#include "ngx_http_modsecurity_common.h"\n#include "i12-nginx-host-state.h"\n' + text
                for old, new in changes:
                    if text.count(old) != 1:
                        raise ValueError("exact NGINX state capture site differs: " + filename)
                    text = text.replace(old, new)
                target.write_text(text)
                extra["files"][filename] = {"before_sha256": before, "after_sha256": sha(target)}
            (output / "nginx-extra-capture-receipt.json").write_text(json.dumps(extra, indent=2) + "\n")
        snapshots[variant] = str(snapshot)
    provenance = {"checkout_sha": args.parent_sha, "manifest_sha256": sha(manifest),
                  "capture_helper_sha256": sha(checkout / "ci/runtime/lifecycle/i12/capture_sources.py"),
                  "capture_product_baseline": baseline, "source_snapshots": snapshots,
                  "checkout_source_diff_sha256": sha(output / "checkout-source.diff")}
    (output / "provenance.json").write_text(json.dumps(provenance, indent=2) + "\n")
    fixtures = output / "fixtures"
    fixtures.mkdir()
    fixture_receipt = {}
    for name in ("nginx_worker_self_maps", "nginx_common_input_fault",
                 "nginx_engine_budget_fault", "nginx_transaction_fault"):
        source = Path(snapshots["ordinary"]) / "tests/fixtures" / (name + ".c")
        target = fixtures / (name + ".so")
        command = ["rtk", "proxy", "cc", "-std=c17", "-D_DEFAULT_SOURCE", "-Wall", "-Wextra", "-Werror",
                   "-shared", "-fPIC", "-I" + str(Path(snapshots["ordinary"]) / "common/include"),
                   str(source), "-ldl", "-o", str(target)]
        result = subprocess.run(command, capture_output=True)
        (fixtures / (name + ".stdout")).write_bytes(result.stdout)
        (fixtures / (name + ".stderr")).write_bytes(result.stderr)
        fixture_receipt[name] = {"argv": command, "exit": result.returncode, "source_sha256": sha(source)}
        if result.returncode:
            raise RuntimeError("fixture build failed: " + name)
        fixture_receipt[name]["library_sha256"] = sha(target)
    (fixtures / "receipt.json").write_text(json.dumps(fixture_receipt, indent=2) + "\n")
    for variant in ("ordinary", "observed"):
        build(argparse.Namespace(source=snapshots[variant], checkout=str(checkout),
                                 base=args.base, output=str(output / variant),
                                 parent_sha=args.parent_sha, instrumented=variant == "observed",
                                 observer_source=None, jobs=args.jobs))
    if git("diff", "HEAD", "--", *scope) != diff:
        raise ValueError("checkout build inputs changed during build")
    print(json.dumps(provenance))


if __name__ == "__main__":
    main()
