"""Execute patched entity hooks with controlled Common failures, without a host."""
from pathlib import Path
import os
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "tests"))
from c_source_contract import function_definition, matching_delimiter


class PatchedAPIResults(unittest.TestCase):
    def test_stock_strict_abort_requires_successful_shutdown(self):
        source = (ROOT / "connectors/lighttpd/stock_sidecar/stock_sidecar.c").read_text()
        start = source.index("if (action == MSCONNECTOR_LATE_INTERVENTION_ABORT_CONNECTION)", source.index("static int sidecar_exchange_response"))
        opening = source.index("{", start)
        branch = source[start:matching_delimiter(source, opening, "{", "}") + 1]
        harness = r'''
#include <assert.h>
#include <sys/socket.h>
#include "common/runtime/msconnector_runtime.h"
#include "msconnector/late_intervention.h"
typedef struct {int client,handled;msconnector_runtime_transaction *transaction;msconnector_decision decision;msconnector_error error;} state_t;
static int shutdown_result,actions,failures;
int shutdown(int fd,int how) {(void)fd;assert(how==SHUT_RDWR);return shutdown_result;}
int msconnector_runtime_transaction_record_host_action(msconnector_runtime_transaction *t,const msconnector_decision *d,msconnector_decision_action a,int h,const char *s,int b,msconnector_error *e) {(void)t;(void)d;(void)h;(void)s;(void)e;assert(a==MSCONNECTOR_DECISION_ACTION_ABORT_CONNECTION);assert(b==1);++actions;return 1;}
static void sidecar_record_decision_delivery_failure(msconnector_runtime_transaction *t,const msconnector_decision *d,msconnector_error *e) {(void)t;(void)d;(void)e;++failures;}
int msconnector_runtime_transaction_finish(msconnector_runtime_transaction *t,msconnector_error *e) {(void)t;(void)e;return 1;}
static int exercise(state_t *state,msconnector_late_intervention_action action) {__BRANCH__;return 1;}
int main(void) {state_t state={0};assert(exercise(&state,MSCONNECTOR_LATE_INTERVENTION_ABORT_CONNECTION)==0);assert(actions==1);assert(failures==0);shutdown_result=-1;assert(exercise(&state,MSCONNECTOR_LATE_INTERVENTION_ABORT_CONNECTION)==0);assert(actions==1);assert(failures==1);return 0;}
'''.replace("__BRANCH__", branch)
        self.compile_and_run(harness)

    def test_stock_failed_delivery_does_not_fabricate_abort(self):
        source = (ROOT / "connectors/lighttpd/stock_sidecar/stock_sidecar.c").read_text()
        functions = "\n".join(function_definition(source, name) for name in (
            "sidecar_record_decision_delivery_failure", "sidecar_record_failure_action"))
        harness = r'''
#include <assert.h>
#include "common/runtime/msconnector_runtime.h"
static int actions,failures;
int msconnector_runtime_transaction_record_host_action(msconnector_runtime_transaction *t,const msconnector_decision *d,msconnector_decision_action a,int h,const char *s,int b,msconnector_error *e) {(void)t;(void)d;(void)a;(void)h;(void)s;(void)b;(void)e;++actions;return 1;}
int msconnector_runtime_transaction_record_failure_host_action(msconnector_runtime_transaction *t,int h,int b,msconnector_error *e) {(void)t;(void)e;assert(h==500);assert(b==0);++actions;return 1;}
int msconnector_runtime_transaction_fail(msconnector_runtime_transaction *t,msconnector_transaction_error_class c,msconnector_error *e) {(void)t;(void)e;assert(c==MSCONNECTOR_TRANSACTION_ERROR_CONNECTOR);++failures;return 1;}
__FUNCTIONS__
int main(void) {
 msconnector_runtime_transaction *t=(void*)1;msconnector_error e={0};msconnector_decision d={0};
 sidecar_record_failure_action(t,500,0,&e);assert(actions==0);
 sidecar_record_decision_delivery_failure(t,&d,&e);assert(actions==0);assert(failures==1);
 sidecar_record_failure_action(t,500,1,&e);assert(actions==1);return 0;
}
'''.replace("__FUNCTIONS__", functions)
        self.compile_and_run(harness)

    def test_stock_native_failed_begin_is_not_reopened_by_uri_reentry(self):
        source = (ROOT / "connectors/lighttpd/module/mod_msconnector.c").read_text()
        start = source.index("REQUEST_FUNC(mod_msconnector_handle_uri_clean) {")
        opening = source.index("{", start)
        body = source[opening:matching_delimiter(source, opening, "{", "}") + 1]
        harness = r'''
#include <assert.h>
#include <stdlib.h>
#include <string.h>
#include "common/runtime/msconnector_runtime.h"
typedef int handler_t;
enum {HANDLER_GO_ON=0,HANDLER_ERROR=-1};
typedef struct {void *plugin_ctx[1];struct {void *errh;} conf;} request_st;
typedef struct {int id;struct {int enabled;} defaults;msconnector_runtime *runtime;size_t header_count_limit,total_header_limit;} plugin_data;
typedef struct {msconnector_runtime_transaction *transaction;msconnector_request request;int request_storage;char host_request_id[96];int request_intervened,api_failed;} handler_ctx;
static int begins,cleanups;
#define log_error(...) ((void)0)
void msconnector_error_init(msconnector_error *e) {memset(e,0,sizeof(*e));}
void msconnector_decision_init(msconnector_decision *d) {memset(d,0,sizeof(*d));}
const char *msconnector_error_code_name(msconnector_error_code c) {(void)c;return "invalid-engine";}
void msconnector_runtime_request_contract(const msconnector_runtime *r,msconnector_request_mapper_contract *c) {(void)r;memset(c,0,sizeof(*c));}
static handler_ctx *handler_ctx_create(plugin_data *p) {(void)p;return calloc(1,sizeof(handler_ctx));}
static void handler_ctx_destroy(handler_ctx **p) {if (*p) {++cleanups;free(*p);*p=0;}}
static handler_t mod_msconnector_error_response(request_st *r,const msconnector_runtime *v,msconnector_error_code c) {(void)r;(void)v;(void)c;return HANDLER_ERROR;}
static int lighttpd_modsecurity_map_request(request_st *r,...) {(void)r;return 1;}
int msconnector_runtime_transaction_begin(msconnector_runtime *r,const msconnector_request *q,const char *id,msconnector_runtime_transaction **t,msconnector_decision *d,msconnector_error *e) {(void)r;(void)q;(void)id;(void)t;(void)d;e->code=MSCONNECTOR_ERROR_MODSECURITY_FAILURE;++begins;return 0;}
int msconnector_decision_is_disruptive(const msconnector_decision *d) {(void)d;return 0;}
static handler_t mod_msconnector_apply_decision(request_st *r,plugin_data *p,handler_ctx *c,const msconnector_decision *d) {(void)r;(void)p;(void)c;(void)d;return HANDLER_GO_ON;}
static handler_t uri_clean(request_st *r,void *p_d) __BODY__
int main(void) {
 request_st r={0};plugin_data p={.defaults={.enabled=1},.runtime=(void*)1};
 assert(uri_clean(&r,&p)==HANDLER_ERROR);assert(begins==1);assert(r.plugin_ctx[0]!=0);
 assert(uri_clean(&r,&p)==HANDLER_ERROR);assert(begins==1);
 handler_ctx_destroy((handler_ctx**)&r.plugin_ctx[0]);handler_ctx_destroy((handler_ctx**)&r.plugin_ctx[0]);assert(cleanups==1);return 0;
}
'''.replace("__BODY__", body)
        self.compile_and_run(harness)

    def test_stock_safe_outcome_return_is_propagated(self):
        source = (ROOT / "connectors/lighttpd/stock_sidecar/stock_sidecar.c").read_text()
        start = source.index("if (action == MSCONNECTOR_LATE_INTERVENTION_LOG_ONLY)", source.index("static int sidecar_exchange_response"))
        branch = source[start:source.index("\n    }\n    return 1;", start)]
        harness = r'''
#include <assert.h>
#include "common/runtime/msconnector_runtime.h"
#include "msconnector/late_intervention.h"
typedef struct {msconnector_runtime_transaction *transaction;msconnector_decision decision;msconnector_error error;struct {struct {int status_code;} response_headers;} payload;} state_t;
static int result=1,calls;
int msconnector_runtime_transaction_record_host_action(msconnector_runtime_transaction *t,const msconnector_decision *d,msconnector_decision_action a,int h,const char *s,int b,msconnector_error *e) {(void)t;(void)d;(void)a;(void)h;(void)s;(void)b;(void)e;++calls;return result;}
static void sidecar_record_action(msconnector_runtime_transaction *t,const msconnector_decision *d,msconnector_error *e) {(void)t;(void)d;(void)e;}
static int exercise(state_t *state,msconnector_late_intervention_action action) {__BRANCH__;return 1;}
int main(void) {state_t state={0};assert(exercise(&state,MSCONNECTOR_LATE_INTERVENTION_LOG_ONLY)==1);result=0;assert(exercise(&state,MSCONNECTOR_LATE_INTERVENTION_LOG_ONLY)==0);assert(calls==2);return 0;}
'''
        self.compile_and_run(harness.replace("__BRANCH__", branch))
        mutation = branch.replace("return msconnector_runtime_transaction_record_host_action(", "(void)msconnector_runtime_transaction_record_host_action(")
        self.assertNotEqual(mutation, branch)
        self.compile_and_run(harness.replace("__BRANCH__", mutation), should_fail=True)

    def test_stock_response_accounting_bound_matches_all_modes(self):
        source = (ROOT / "connectors/lighttpd/stock_sidecar/stock_sidecar.c").read_text()
        start = source.index("if (!state->payload.response_headers.no_body &&", source.index("static int sidecar_exchange_response"))
        condition = source[start + 4:source.index(") {", start)]
        harness = r'''
#include <assert.h>
#include <stdint.h>
#include "msconnector/phase4_budget.h"
struct state_t {struct {struct {int no_body;size_t content_length;} response_headers;} payload;struct {int runtime;} dependencies;};
static enum msconnector_phase4_mode msconnector_runtime_phase4_mode(int mode) {return (enum msconnector_phase4_mode)mode;}
static int rejected(struct state_t *state) {return __CONDITION__;}
int main(void) {
 struct state_t state={0};state.payload.response_headers.content_length=SIZE_MAX;
 const int modes[]={MSCONNECTOR_PHASE4_MODE_OFF,MSCONNECTOR_PHASE4_MODE_SAFE,MSCONNECTOR_PHASE4_MODE_STRICT};
 for (unsigned i=0;i<sizeof(modes)/sizeof(modes[0]);++i) {state.dependencies.runtime=modes[i];assert(!rejected(&state));}
 state.dependencies.runtime=-1;state.payload.response_headers.content_length=1;assert(rejected(&state));
 state.payload.response_headers.content_length=0;assert(!rejected(&state));
 state.payload.response_headers.content_length=SIZE_MAX;state.payload.response_headers.no_body=1;assert(!rejected(&state));
 return 0;
}
'''.replace("__CONDITION__", condition)
        self.compile_and_run(harness)

    def compile_and_run(self, harness, should_fail=False):
        with tempfile.TemporaryDirectory(prefix="i09-lighttpd-") as tmp:
            path = Path(tmp)
            (path / "test.c").write_text(harness)
            result = subprocess.run([os.environ.get("CC", "cc"), "-std=c17", "-Wall", "-Wextra", "-Werror", "-I", str(ROOT), "-I", str(ROOT / "common/include"), str(path / "test.c"), "-o", str(path / "test")], capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, result.stderr)
            result = subprocess.run([str(path / "test")], cwd=path, capture_output=True, text=True)
            if should_fail:
                self.assertNotEqual(result.returncode, 0, "ignored-result mutation escaped the regression")
            else:
                self.assertEqual(result.returncode, 0, result.stderr)

    def test_checked_commit_stops_append_eos_and_reentry(self):
        source = (ROOT / "connectors/lighttpd/module/mod_msconnector.c").read_text()
        functions = "\n".join(function_definition(source, name) for name in (
            "mod_msconnector_record_api_failure", "mod_msconnector_apply_decision", "mod_msconnector_finish_response_body", "mod_msconnector_handle_response_body", "mod_msconnector_handle_response_abort"))
        harness = r'''
#include <assert.h>
#include <stdint.h>
#include <stdio.h>
#include <string.h>
#include <sys/types.h>
#include "common/runtime/msconnector_runtime.h"
#include "msconnector/late_intervention.h"
typedef int handler_t;
typedef int plugin_body_hook_result;
typedef int plugin_response_abort_reason;
enum {PLUGIN_RESPONSE_ABORT_UPSTREAM_EOF=1};
enum {HANDLER_GO_ON=0,HANDLER_ERROR=-1,PLUGIN_BODY_HOOK_CONTINUE=0,PLUGIN_BODY_HOOK_ERROR=-1,PLUGIN_BODY_HOOK_ABORT=1};
typedef struct { void *plugin_ctx[1]; struct {void *errh;} conf; int http_status; } request_st;
typedef struct {int id,response_body_hooks_enabled; msconnector_runtime *runtime;} plugin_data;
typedef struct {msconnector_runtime_transaction *transaction; int request_intervened,response_body_finished,response_processed,api_failed,response_body_aborted; off_t response_body_next_offset;} handler_ctx;
static int commit_result=1,appends,finishes,commits,failures,disruptive,outcome_result=1,cancellations;
static int mod_msconnector_response_headers_committed(const request_st *r) {(void)r;return 0;}
static int mod_msconnector_response_body_committed(const request_st *r) {(void)r;return 0;}
static handler_t mod_msconnector_handle_response_start(request_st *r,plugin_data *p) {(void)r;(void)p;return HANDLER_GO_ON;}
#define log_error(...) ((void)0)
void msconnector_error_init(msconnector_error *e) {memset(e,0,sizeof(*e));}
void msconnector_decision_init(msconnector_decision *d) {memset(d,0,sizeof(*d));}
const char *msconnector_error_code_name(msconnector_error_code c) {(void)c;return "host-api";}
enum msconnector_phase4_mode msconnector_runtime_phase4_mode(const msconnector_runtime *r) {(void)r;return MSCONNECTOR_PHASE4_MODE_OFF;}
int msconnector_runtime_transaction_set_response_commit_state_checked(msconnector_runtime_transaction *t,int h,int b,msconnector_error *e) {(void)t;(void)h;(void)b;++commits;e->code=MSCONNECTOR_ERROR_HOST_API_FAILURE;return commit_result;}
void msconnector_runtime_transaction_set_response_commit_state(msconnector_runtime_transaction *t,int h,int b) {msconnector_error e;(void)msconnector_runtime_transaction_set_response_commit_state_checked(t,h,b,&e);}
int msconnector_runtime_transaction_append_response_body_chunk(msconnector_runtime_transaction *t,const unsigned char *b,size_t n,msconnector_error *e) {(void)t;(void)b;(void)n;(void)e;++appends;return 1;}
int msconnector_runtime_transaction_finish_response_body(msconnector_runtime_transaction *t,msconnector_decision *d,msconnector_error *e) {(void)t;(void)d;(void)e;++finishes;return 1;}
int msconnector_decision_is_disruptive(const msconnector_decision *d) {(void)d;return disruptive;}
int msconnector_decision_http_status(const msconnector_decision *d) {(void)d;return 403;}
static handler_t http_status_set_err(request_st *r,int status) {r->http_status=status;return HANDLER_GO_ON;}
void msconnector_late_intervention_policy_init(msconnector_late_intervention_policy *p) {memset(p,0,sizeof(*p));}
msconnector_late_intervention_action msconnector_late_intervention_resolve(const msconnector_late_intervention_policy *p,int h,int b,int s) {(void)p;(void)h;(void)b;(void)s;return MSCONNECTOR_LATE_INTERVENTION_LOG_ONLY;}
int msconnector_runtime_transaction_record_host_action(msconnector_runtime_transaction *t,const msconnector_decision *d,msconnector_decision_action a,int h,const char *s,int b,msconnector_error *e) {(void)t;(void)d;(void)a;(void)h;(void)s;(void)b;(void)e;return outcome_result;}
int msconnector_runtime_transaction_fail(msconnector_runtime_transaction *t,msconnector_transaction_error_class c,msconnector_error *e) {(void)t;(void)e;assert(c==MSCONNECTOR_TRANSACTION_ERROR_CONNECTOR);++failures;return 1;}
int msconnector_runtime_transaction_cancel(msconnector_runtime_transaction *t,int upstream,msconnector_error *e) {(void)t;(void)e;assert(upstream==1);++cancellations;return 1;}
__FUNCTIONS__
int main(void) {
 handler_ctx ctx={.transaction=(void*)1,.response_processed=1};
 request_st r={.plugin_ctx={&ctx},.http_status=200};plugin_data p={.response_body_hooks_enabled=1};
 const unsigned char bytes[]={42};
 assert(mod_msconnector_handle_response_body(&r,bytes,1,0,0,&p)==PLUGIN_BODY_HOOK_CONTINUE);assert(appends==1);assert(finishes==0);
 commit_result=0;
 assert(mod_msconnector_handle_response_body(&r,bytes,1,1,1,&p)==PLUGIN_BODY_HOOK_ERROR);assert(appends==1);assert(finishes==0);
 int before=commits;
 assert(mod_msconnector_handle_response_body(&r,bytes,1,1,1,&p)==PLUGIN_BODY_HOOK_ERROR);assert(commits==before);assert(appends==1);assert(failures==1);
 memset(&ctx,0,sizeof(ctx));ctx.transaction=(void*)1;ctx.response_processed=1;
 assert(mod_msconnector_finish_response_body(&r,&p,&ctx)==PLUGIN_BODY_HOOK_ERROR);assert(finishes==0);
 memset(&ctx,0,sizeof(ctx));ctx.transaction=(void*)1;disruptive=1;outcome_result=0;
 msconnector_decision d={0};assert(mod_msconnector_apply_decision(&r,&p,&ctx,&d)==HANDLER_ERROR);assert(ctx.api_failed);
 memset(&ctx,0,sizeof(ctx));ctx.transaction=(void*)1;
 assert(mod_msconnector_handle_response_abort(&r,PLUGIN_RESPONSE_ABORT_UPSTREAM_EOF,&p)==PLUGIN_BODY_HOOK_CONTINUE);assert(cancellations==1);assert(ctx.api_failed);
 assert(mod_msconnector_handle_response_abort(&r,PLUGIN_RESPONSE_ABORT_UPSTREAM_EOF,&p)==PLUGIN_BODY_HOOK_CONTINUE);assert(cancellations==1);
 return 0;
}
'''.replace("__FUNCTIONS__", functions)
        self.compile_and_run(harness)

if __name__ == "__main__":
    unittest.main()
