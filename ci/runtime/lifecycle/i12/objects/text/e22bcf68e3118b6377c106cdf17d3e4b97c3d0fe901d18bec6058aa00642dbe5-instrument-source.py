"""Create immutable exact-anchor NGX test source overlays only; no host run."""
import argparse, hashlib, json
from pathlib import Path

def sha(data): return hashlib.sha256(data).hexdigest()
def replace(text, anchor, replacement, count=1):
    if text.count(anchor) != count: raise ValueError("source anchor count differs: " + anchor[:80])
    return text.replace(anchor,replacement)

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--source",required=True); p.add_argument("--output",required=True)
    p.add_argument("--parent-sha",required=True)
    a = p.parse_args(); source = Path(a.source); output = Path(a.output)
    output.mkdir(mode=0o700)
    receipt = {"scope":"NGX external source-copy observations only", "parent_sha":a.parent_sha,"files":[]}
    names = ["ngx_http_modsecurity_module.c","ngx_http_modsecurity_access.c","ngx_http_modsecurity_body_filter.c"]
    for name in names:
        path = source/"connectors/nginx/src"/name
        original = path.read_bytes(); text = original.decode()
        text = replace(text, '#include "ngx_http_modsecurity_common.h"', '#include "ngx_http_modsecurity_common.h"\n#include "nginx-host-observation.h"')
        if name.endswith("module.c"):
            text = replace(text, "    const msconnector_transaction_profile *profile;", "    const msconnector_transaction_profile *profile;\n    uint64_t ngxi12_allocation_call;")
            text = replace(text, "    ctx = ngx_pcalloc(r->pool, sizeof(ngx_http_modsecurity_ctx_t));", "    ngxi12_allocation_call = ngxi12_host_begin();\n    ctx = ngx_pcalloc(r->pool, sizeof(ngx_http_modsecurity_ctx_t));")
            begin = text.index("ngx_http_modsecurity_create_ctx(ngx_http_request_t *r)")
            finish = text.index("ngx_inline ngx_http_modsecurity_ctx_t *", begin)
            ctor = text[begin:finish]
            if ctor.count("return NULL;") != 10 or ctor.count("return ctx;") != 1:
                raise ValueError("exact actual constructor exit surface changed")
            ctor = ctor.replace("return NULL;", "(void)ngxi12_host_end(ngxi12_allocation_call, ctx, ctx != NULL ? &ctx->contract : NULL, ctx != NULL ? ctx->modsec_transaction : NULL, 0);\n        return NULL;")
            ctor = ctor.replace("return ctx;", "(void)ngxi12_host_end(ngxi12_allocation_call, ctx, &ctx->contract, ctx->modsec_transaction, 1);\n    ngxi12_host_note(ctx, \"context_join\", 0U, 0U, -1);\n    return ctx;")
            text = text[:begin] + ctor + text[finish:]
            text = replace(text, '    observed_contract = ctx->contract_initialized;', '    ngxi12_host_note(ctx, "cleanup_enter", 0U, 0U, -1);\n    observed_contract = ctx->contract_initialized;')
            text = replace(text, '        ngx_http_modsecurity_cleanup_log_event(ctx, common_return,\n            native_cleanup_completed);', '        ngx_http_modsecurity_cleanup_log_event(ctx, common_return,\n            native_cleanup_completed);\n        ngxi12_host_note(ctx, "cleanup_native_common_complete", 0U, 0U, -1);\n        (void)ngxi12_host_retire(ctx);')
        elif name.endswith("access.c"):
            text = replace(text, '        if (chain->buf->last_buf) {\n            break;', '        if (chain->buf->last_buf) {\n            ngxi12_host_note(ctx, "request_eos", (unsigned int)chain->buf->last_buf, (unsigned int)chain->buf->last_in_chain, r->request_body != NULL ? (int64_t)r->request_body->rest : -1);\n            break;')
        else:
            text = replace(text, '        ret = ngx_http_modsecurity_forward_response_body_prefix(r,', '        ngxi12_host_note(ctx, "response_eos", (unsigned int)chain->buf->last_buf, (unsigned int)chain->buf->last_in_chain, -1);\n        ret = ngx_http_modsecurity_forward_response_body_prefix(r,')
        changed = text.encode(); (output/name).write_bytes(changed)
        if path.read_bytes()!=original: raise ValueError("input changed while preparing overlay")
        receipt["files"].append({"path":str(path),"input_sha256":sha(original),"overlay_sha256":sha(changed)})
    (output/"receipt.json").write_text(json.dumps(receipt,indent=2)+"\n")
    print(json.dumps(receipt,sort_keys=True))
if __name__ == "__main__": main()
