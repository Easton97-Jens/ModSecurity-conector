"""Compiled HTX host-control and SPOP owner bridge regression seams."""
import os
from pathlib import Path
import shlex
import subprocess
import tempfile
import unittest

from tests.c_source_contract import function_definition

ROOT = Path(__file__).resolve().parents[1]
PREAMBLE = r'''
#include "connectors/haproxy/src/haproxy_modsecurity_binding.h"
#include "connectors/haproxy/src/haproxy_spop_response_companion_backend.h"
#include "msconnector/event_jsonl.h"
#include "msconnector/error.h"
#include <pthread.h>
#include <unistd.h>
#include <stdarg.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
static int replies,shutdowns,cleanups,events,phase_result,decisions,native_calls;
static msconnector_transaction_error_class failure=MSCONNECTOR_TRANSACTION_ERROR_INVALID_ENGINE_RESPONSE;
struct stream {struct {short status;} *txn;};
struct haproxy_modsecurity_htx_filter_context {
 haproxy_modsecurity_transaction *transaction;
 struct {char transaction_id[128];int disabled,fail_closed,error_emitted;haproxy_modsecurity_decision error;} lifecycle;
 struct {int headers_seen,finished;} request;
 struct {int headers_seen,headers_committed;} response;
};
#define SF_ERR_KILLED 1
static void ha_warning(const char *format,...) {if(strcmp(format,"%s")==0){events++;}}
static void http_set_term_flags(struct stream *s){(void)s;}
static void *http_error_message(struct stream *s){(void)s;return NULL;}
static void http_reply_and_close(struct stream *s,short status,void *m){(void)s;(void)status;(void)m;replies++;}
static void stream_shutdown(struct stream *s,int flag){(void)s;(void)flag;shutdowns++;}
static void haproxy_modsecurity_htx_companion_cancel_and_close(struct haproxy_modsecurity_htx_filter_context *ctx,const msconnector_error *e){(void)ctx;(void)e;}
static void haproxy_modsecurity_htx_request_snapshot_free(struct haproxy_modsecurity_htx_filter_context *ctx){(void)ctx;}
void haproxy_modsecurity_transaction_abort(haproxy_modsecurity_transaction *t){(void)t;cleanups++;}
void haproxy_modsecurity_transaction_abort_with_error(haproxy_modsecurity_transaction *t,msconnector_transaction_error_class e){(void)t;failure=e;cleanups++;}
msconnector_transaction_error_class haproxy_modsecurity_transaction_error(const haproxy_modsecurity_transaction *t){(void)t;return failure;}
const char *haproxy_modsecurity_transaction_id(const haproxy_modsecurity_transaction *t){(void)t;return "test-id";}
int haproxy_modsecurity_transaction_error_event_write_checked(haproxy_modsecurity_transaction *t,haproxy_modsecurity_decision *d,char *line,size_t n,msconnector_error *e){(void)t;return haproxy_modsecurity_error_event_write_checked(d,"test-id",line,n,e);}
int haproxy_modsecurity_transaction_finish_with_decision(haproxy_modsecurity_transaction *t,haproxy_modsecurity_decision *d){(void)t;native_calls++;d->error_class=failure;d->phase=5;return phase_result;}
int haproxy_modsecurity_transaction_claim_response_companion(haproxy_modsecurity_transaction *t){(void)t;native_calls++;return phase_result;}
int haproxy_modsecurity_transaction_process_response_headers(haproxy_modsecurity_transaction *t,const haproxy_modsecurity_response *r,haproxy_modsecurity_decision *d){(void)t;(void)r;native_calls++;d->error_class=failure;return phase_result;}
int haproxy_modsecurity_transaction_append_response_body_chunk(haproxy_modsecurity_transaction *t,const unsigned char *b,unsigned int n,haproxy_modsecurity_decision *d){(void)t;(void)b;(void)n;native_calls++;d->error_class=failure;return phase_result;}
int haproxy_modsecurity_transaction_finish_response_body(haproxy_modsecurity_transaction *t,haproxy_modsecurity_decision *d){(void)t;native_calls++;d->error_class=failure;return phase_result;}
int haproxy_modsecurity_transaction_set_response_commit_state(haproxy_modsecurity_transaction *t,int h,int b){(void)t;(void)h;(void)b;native_calls++;return phase_result;}
int haproxy_modsecurity_transaction_record_response_companion_outcome(haproxy_modsecurity_transaction *t,msconnector_decision_action a,const char *r,int s,int b){(void)t;(void)a;(void)r;(void)s;(void)b;native_calls++;return phase_result;}
#define SPOP_BRIDGE_MAX_HEADERS 4
typedef struct {FILE *decision_log;pthread_mutex_t decision_log_lock;int decision_log_lock_initialized;msconnector_error decision_log_error;struct {char decision_log[128];} config;} agent_state;
typedef struct {
 haproxy_spop_response_companion_owner_command command;
 haproxy_modsecurity_transaction *transaction;
 haproxy_modsecurity_header headers[4];
 agent_state *state;
 int success,transaction_consumed,error_event_attempted;
 msconnector_error error;
 msconnector_decision decision;
 char transaction_id[128];
} spop_bridge_task_context;

static int set_bridge_native_decision(spop_bridge_task_context *c,const haproxy_modsecurity_decision *d){(void)c;(void)d;decisions++;return 1;}
'''
MAIN = r'''
#define CHECK(x) do{if(!(x)){fprintf(stderr,"failure line %d: %s\n",__LINE__,#x);return 1;}}while(0)
int main(int argc,char **argv) {
 (void)argc;
 struct {short status;} host={0};struct stream stream={.txn=(void *)&host};
 struct haproxy_modsecurity_htx_filter_context ctx={0};
 ctx.transaction=(void *)1;ctx.lifecycle.error.error_class=failure;
 CHECK(haproxy_modsecurity_htx_fail_closed_precommit(&stream,&ctx,"native")==-1);
 CHECK(haproxy_modsecurity_htx_fail_closed_precommit(&stream,&ctx,"native")==-1);
 CHECK(replies==1 && events==1 && cleanups==1);
 ctx=(struct haproxy_modsecurity_htx_filter_context){0};ctx.transaction=(void *)1;
 haproxy_modsecurity_htx_fail_closed_postcommit(&stream,&ctx,"native");
 haproxy_modsecurity_htx_fail_closed_postcommit(&stream,&ctx,"native");
 CHECK(shutdowns==1 && events==2 && cleanups==2);
 ctx=(struct haproxy_modsecurity_htx_filter_context){0};ctx.transaction=(void *)1;phase_result=1;
 CHECK(haproxy_modsecurity_htx_finish_context(&ctx)==1 && ctx.transaction==NULL && ctx.lifecycle.error.phase==5);
 agent_state state={0};state.decision_log=fopen(argv[1],"w+");CHECK(state.decision_log);CHECK(pthread_mutex_init(&state.decision_log_lock,NULL)==0);state.decision_log_lock_initialized=1;
 msconnector_response response={0};
 for(int kind=0;kind<2;kind++) {
  failure=kind?MSCONNECTOR_TRANSACTION_ERROR_BODY_LIMIT:MSCONNECTOR_TRANSACTION_ERROR_INVALID_ENGINE_RESPONSE;
  for(int op=HAPROXY_SPOP_RESPONSE_COMPANION_RESPONSE_HEADERS;op<=HAPROXY_SPOP_RESPONSE_COMPANION_RESPONSE_EOS;op++) {
   spop_bridge_task_context context={0};context.state=&state;context.transaction=(void *)1;context.command.operation=op;context.command.response=&response;
   int before=native_calls;run_spop_bridge_task(&context);
   CHECK(!context.success && native_calls==before+1 && decisions==0);
   CHECK(context.error.code==(kind?MSCONNECTOR_ERROR_BODY_TOO_LARGE:MSCONNECTOR_ERROR_MODSECURITY_FAILURE));
  }
 }
 spop_bridge_task_context context={0};context.state=&state;context.transaction=(void *)1;context.command.operation=HAPROXY_SPOP_RESPONSE_COMPANION_FAIL;context.command.error_class=MSCONNECTOR_TRANSACTION_ERROR_PROTOCOL;
 run_spop_bridge_task(&context);CHECK(context.success && context.transaction_consumed && failure==MSCONNECTOR_TRANSACTION_ERROR_PROTOCOL);
 phase_result=0;context=(spop_bridge_task_context){0};context.state=&state;context.transaction=(void *)1;context.command.operation=HAPROXY_SPOP_RESPONSE_COMPANION_RESPONSE_HEADERS;context.command.response=&response;
 run_spop_bridge_task(&context);CHECK(context.success && decisions==2);
 /* Real terminal caller must propagate a real buffered flush failure once. */
 int descriptor=fileno(state.decision_log),saved=dup(descriptor);CHECK(saved>=0);
 CHECK(close(descriptor)==0);context=(spop_bridge_task_context){0};context.state=&state;context.transaction=(void *)1;
 context.command.operation=HAPROXY_SPOP_RESPONSE_COMPANION_FAIL;context.command.error_class=MSCONNECTOR_TRANSACTION_ERROR_PROTOCOL;
 int before_cleanups=cleanups;run_spop_bridge_task(&context);
 CHECK(!context.success && context.transaction_consumed && cleanups==before_cleanups+1);
 CHECK(context.error.code==MSCONNECTOR_ERROR_IO && state.decision_log_error.code==MSCONNECTOR_ERROR_IO);
 CHECK(dup2(saved,descriptor)==descriptor);CHECK(close(saved)==0);clearerr(state.decision_log);
 long failed_size=ftell(state.decision_log);CHECK(failed_size>=0);
 haproxy_modsecurity_decision d={.error_class=MSCONNECTOR_TRANSACTION_ERROR_PROTOCOL};
 CHECK(!spop_bridge_error_event_write(&context,&d));CHECK(ftell(state.decision_log)==failed_size);
 context=(spop_bridge_task_context){0};context.state=&state;context.transaction=(void *)1;
 context.command.operation=HAPROXY_SPOP_RESPONSE_COMPANION_RESPONSE_HEADERS;context.command.response=&response;
 int before_native=native_calls,before_decisions=decisions;run_spop_bridge_task(&context);
 CHECK(!context.success && context.error.code==MSCONNECTOR_ERROR_IO && native_calls==before_native && decisions==before_decisions);
 context.command.operation=HAPROXY_SPOP_RESPONSE_COMPANION_RELEASE;before_cleanups=cleanups;run_spop_bridge_task(&context);
 CHECK(!context.success && context.transaction_consumed && cleanups==before_cleanups+1 && native_calls==before_native);
 CHECK(ftell(state.decision_log)==failed_size);
 CHECK(fclose(state.decision_log)==0);CHECK(pthread_mutex_destroy(&state.decision_log_lock)==0);
 FILE *persisted=fopen(argv[1],"r");CHECK(persisted && fseek(persisted,0,SEEK_END)==0);
 CHECK(ftell(persisted)==failed_size);CHECK(fclose(persisted)==0);
 return 0;
}
'''


class HaproxyHostNativeResultsTests(unittest.TestCase):
    def test_host_error_reentry_and_bridge_error_classification(self):
        with tempfile.TemporaryDirectory(prefix="haproxy-host-native-", dir=os.environ.get("TMPDIR") or os.environ.get("RUNNER_TEMP")) as temporary:
            directory = Path(temporary)
            htx = (ROOT / "connectors/haproxy/htx-overlay/haproxy_modsecurity_htx_filter.c").read_text()
            spop = (ROOT / "connectors/haproxy/src/haproxy_spop_diagnostic_runtime.c").read_text()
            binding = (ROOT / "connectors/haproxy/src/haproxy_modsecurity_binding.c").read_text()
            functions = [function_definition(binding, name) for name in ("contract_phase_from_decision", "haproxy_modsecurity_error_event_write_checked", "haproxy_modsecurity_error_event_write")]
            functions += [function_definition(htx, name) for name in ("haproxy_modsecurity_htx_abort_context", "haproxy_modsecurity_htx_finish_context", "haproxy_modsecurity_htx_error_phase", "haproxy_modsecurity_htx_report_error", "haproxy_modsecurity_htx_fail_closed_precommit", "haproxy_modsecurity_htx_fail_closed_postcommit")]
            functions += [function_definition(spop, name) for name in ("spop_bridge_error_event_flush", "spop_bridge_error_event_write", "spop_bridge_terminal_error", "run_spop_bridge_native_operation", "spop_bridge_operation_error", "spop_bridge_error_code", "record_spop_bridge_operation_failure", "spop_bridge_sink_ready", "run_spop_bridge_task")]
            fixture = directory / "fixture.c"
            fixture.write_text(PREAMBLE + "\n".join(functions) + MAIN)
            binary = directory / "fixture"
            args = shlex.split(os.environ.get("CC", "cc")) + ["-D_POSIX_C_SOURCE=200809L", "-pthread", "-std=c17", "-Wall", "-Wextra", "-Werror", "-ffunction-sections", "-Wl,--gc-sections", "-I", str(ROOT), "-I", str(ROOT / "common/include"), "-I", str(ROOT / "common/runtime"), str(fixture)] + [str(ROOT / "common/src" / name) for name in ("error.c", "decision.c", "intervention.c", "event.c", "event_jsonl.c", "json_escape.c", "http_status.c", "status.c", "transaction_state.c")] + ["-o", str(binary)]
            compiled = subprocess.run(args, capture_output=True, text=True, timeout=90)
            self.assertEqual(compiled.returncode, 0, compiled.stderr)
            observed = subprocess.run([str(binary), str(directory / "events.jsonl")], capture_output=True, text=True, timeout=10)
            self.assertEqual(observed.returncode, 0, observed.stderr)
