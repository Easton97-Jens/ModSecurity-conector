"""Fresh external source with one genuine zero-body branch observation."""
import hashlib
import json
from pathlib import Path
import shutil

BASE=Path(__file__).resolve().parent
RUN=BASE.parent
OLD=RUN/'apache-lifecycle/lighttpd-preparation'
SOURCE=BASE/'compile-source'
shutil.copytree(OLD/'source-04',SOURCE)
def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()
assert sha(SOURCE/'ci/runtime/lifecycle/native-lifecycle-observer.c')=='270245fedf253e4ef502fc1aedcac5406ee516b85c90002cb7deaff69fb91736'
assert sha(SOURCE/'ci/runtime/lifecycle/native-lifecycle-observer.h')=='5a34307b4d52927f36573fcf1caf4f63e3e0ce7adffc522e462128148bec7060'
module=SOURCE/'connectors/lighttpd/module/mod_msconnector.c'
original=module.read_text()
before='    if (r->reqbody_length == 0) {\n        return mod_msconnector_finish_request_body(r, p, ctx);\n    }'
after='    if (r->reqbody_length == 0) {\n        lighttpd_observe_empty_request_boundary(ctx->transaction, (int64_t)r->reqbody_length);\n        return mod_msconnector_finish_request_body(r, p, ctx);\n    }'
assert original.count(before)==1
module.chmod(0o600);module.write_text(original.replace(before,after))
logger=SOURCE/'lighttpd-host-observer.c'
code=logger.read_text()
code=code.replace('void lighttpd_observe_body(', 'static void observe(').replace('size_t input_size, int eos) {','size_t input_size, int eos, int empty_boundary) {')
code=code.replace('    char record[1000];','    char eos_literal[16];\n    if (empty_boundary) memcpy(eos_literal, "null", 5U);\n    else (void)snprintf(eos_literal, sizeof(eos_literal), "%d", eos);\n    char record[1000];')
code=code.replace('\\"actual_eos_argument\\":%d,\\"invalid\\":%s', '\\"actual_eos_argument\\":%s,\\"empty_request_boundary\\":%s,\\"invalid\\":%s')
code=code.replace('entity_length,stream_offset,input_size,eos,invalid?', 'entity_length,stream_offset,input_size,eos_literal,empty_boundary?"true":"false",invalid?')
assert '\\"actual_eos_argument\\":%s' in code
code += '\nvoid lighttpd_observe_body(const char *kind, const msconnector_runtime_transaction *transaction,\n    int64_t entity_length, int64_t stream_offset, size_t input_size, int eos) {\n    observe(kind, transaction, entity_length, stream_offset, input_size, eos, 0);\n}\nvoid lighttpd_observe_empty_request_boundary(const msconnector_runtime_transaction *transaction,\n    int64_t actual_entity_length) {\n    observe("patched_empty_request_boundary", transaction, actual_entity_length, 0, 0U, 0, 1);\n}\n'
logger.chmod(0o600);logger.write_text(code)
header=SOURCE/'lighttpd-host-observer.h'
text=header.read_text().replace('#endif','void lighttpd_observe_empty_request_boundary(const msconnector_runtime_transaction *transaction,\n    int64_t actual_entity_length);\n#endif')
header.chmod(0o600);header.write_text(text)
changes={}
for path in SOURCE.rglob('*'):
    if path.is_file():
        relative=path.relative_to(SOURCE);old=OLD/'source-04'/relative
        if sha(path)!=sha(old):changes[str(relative)]={'original_sha256':sha(old),'new_sha256':sha(path)}
assert set(changes)=={'connectors/lighttpd/module/mod_msconnector.c','lighttpd-host-observer.c','lighttpd-host-observer.h'}
(BASE/'source-overlay.json').write_text(json.dumps({'changes':changes,'shared_observer_revision':'C270/H5a unchanged38 wraps','product_logic_change':False,'zero_body_observation':'Actual reqbody_length==0 branch, actual_eos_argument null; not a body hook EOS argument.'},indent=2,sort_keys=True)+'\n')
print(json.dumps(changes))
