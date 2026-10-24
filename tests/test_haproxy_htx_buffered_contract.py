"""Compiled header-stage branch checks; hosted zero-dispatch remains separate."""
from pathlib import Path
import json
import re
import subprocess
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / 'connectors/haproxy/htx-overlay/haproxy_modsecurity_htx_filter.c'


class BufferedContract(unittest.TestCase):
    def test_companion_p3_receipt_owns_canonical_rule_id(self):
        text = SOURCE.read_text()
        match = re.search(r'static int haproxy_modsecurity_htx_companion_p3_rule_id\(.*?\n}\n', text, re.S)
        self.assertIsNotNone(match)
        program = r'''
#include <assert.h>
#include <limits.h>
#include <stddef.h>
#include <stdlib.h>
#include <string.h>
#define MSCONNECTOR_MAX_RULE_ID_LENGTH 128U
#define MSCONNECTOR_DECISION_KIND_DENY 1
#define MSCONNECTOR_DECISION_KIND_REDIRECT 2
typedef struct { int success, decision; char *rule_id; } msconnector_response_companion_result;
''' + match.group(0) + r'''
int main(void) {
 char *owned=malloc(8); assert(owned); memcpy(owned,"1100201",8);
 msconnector_response_companion_result r={1,1,owned}; int id=0;
 assert(haproxy_modsecurity_htx_companion_p3_rule_id(&r,&id));
 free(owned); assert(id==1100201);
 r.rule_id="2147483647"; r.decision=2;
 assert(haproxy_modsecurity_htx_companion_p3_rule_id(&r,&id) && id==INT_MAX);
 char too_long[129]; memset(too_long,'1',128); too_long[128]=0;
 char *invalid[]={NULL,"","0","01100201","1100 201","1100\n201",
   "1100/201","1100x201","-1","2147483648",too_long};
 for (size_t i=0;i<sizeof(invalid)/sizeof(invalid[0]);i++) {
   r.rule_id=invalid[i]; id=42;
   assert(!haproxy_modsecurity_htx_companion_p3_rule_id(&r,&id)); assert(id==42);
 }
 r.rule_id="1100201"; r.decision=3;
 assert(!haproxy_modsecurity_htx_companion_p3_rule_id(&r,&id));
 r.decision=1; r.success=0;
 assert(!haproxy_modsecurity_htx_companion_p3_rule_id(&r,&id));
 assert(!haproxy_modsecurity_htx_companion_p3_rule_id(NULL,&id));
 return 0;
}
'''
        with tempfile.TemporaryDirectory(dir='/var/tmp/codex/ModSecurity-conector') as raw:
            path = Path(raw)
            (path / 'receipt.c').write_text(program)
            subprocess.run(['rtk', 'proxy', 'cc', '-std=c11', '-Wall', '-Wextra', '-Werror', '-fsanitize=address,undefined', str(path/'receipt.c'), '-o', str(path/'receipt')], check=True)
            subprocess.run(['rtk', 'proxy', str(path/'receipt')], check=True)
        start = text.index('static int haproxy_modsecurity_htx_process_companion_response_headers(')
        end = text.index('static int haproxy_modsecurity_htx_send_companion_response_chunk(', start)
        body = text[start:end]
        validation = body.index('!haproxy_modsecurity_htx_companion_p3_rule_id(&result, &rule_id)')
        reset = body.index('haproxy_modsecurity_htx_companion_result_reset(&result);', validation)
        self.assertLess(validation, reset)
        self.assertIn('response-companion phase-3 uncorrelated decision', body)
        self.assertIn('host_decision.rule_id = rule_id;', body)
        applied = body.index('if (haproxy_modsecurity_htx_apply_precommit_deny(')
        receipt = body.index('response-companion phase-3 intervention;')
        self.assertLess(applied, receipt)
        self.assertIn('requested_status=%d host_action=%s host_status=%d', body)
        self.assertIn('actual_status = s->txn->status;', body)
        self.assertIn('actual_action, actual_status);', body)
        self.assertLess(applied, body.index('actual_status = s->txn->status;'))
        self.assertNotIn('result.rule_id', body[reset:])

    def test_companion_p3_render_fallback_records_observed_error(self):
        text = SOURCE.read_text()
        match = re.search(r'static msconnector_decision_action haproxy_modsecurity_htx_companion_p3_host_action\(.*?\n}\n', text, re.S)
        self.assertIsNotNone(match)
        program = r'''
#include <assert.h>
typedef enum { MSCONNECTOR_DECISION_ACTION_DENY=1,
 MSCONNECTOR_DECISION_ACTION_ERROR=7 } msconnector_decision_action;
''' + match.group(0) + r'''
int main(void) {
 assert(haproxy_modsecurity_htx_companion_p3_host_action(403,403)==1);
 assert(haproxy_modsecurity_htx_companion_p3_host_action(503,503)==1);
 assert(haproxy_modsecurity_htx_companion_p3_host_action(403,500)==7);
 assert(haproxy_modsecurity_htx_companion_p3_host_action(503,500)==7);
 assert(haproxy_modsecurity_htx_companion_p3_host_action(403,200)==7);
 return 0;
}
'''
        with tempfile.TemporaryDirectory(dir='/var/tmp/codex/ModSecurity-conector') as raw:
            path = Path(raw)
            (path / 'fallback.c').write_text(program)
            subprocess.run(['rtk', 'proxy', 'cc', '-std=c11', '-Wall', '-Wextra', '-Werror', str(path/'fallback.c'), '-o', str(path/'fallback')], check=True)
            subprocess.run(['rtk', 'proxy', str(path/'fallback')], check=True)

    def test_native_buffered_scope_and_timeout_are_frontend_owned(self):
        text = SOURCE.read_text()
        match = re.search(r'static int haproxy_modsecurity_htx_buffered_profile_is_valid\(.*?\n}\n', text, re.S)
        self.assertIsNotNone(match, 'frontend-owned buffered configuration guard missing')
        program = r'''
#include <assert.h>
#include <stddef.h>
#define PR_CAP_FE 1
#define PR_CAP_BE 2
#define PR_MODE_HTTP 2
#define PR_O_WREQ_BODY 4
#define TICK_ETERNITY 0xffffffffU
struct proxy { unsigned cap, mode, options; struct { unsigned httpreq; } timeout; };
'''+match.group(0)+r'''
int main(void) {
 struct proxy p={PR_CAP_FE,PR_MODE_HTTP,PR_O_WREQ_BODY,{5000}};
 assert(haproxy_modsecurity_htx_buffered_profile_is_valid(&p));
 p.cap=PR_CAP_FE|PR_CAP_BE;
 assert(!haproxy_modsecurity_htx_buffered_profile_is_valid(&p));
 p.cap=PR_CAP_BE;
 assert(!haproxy_modsecurity_htx_buffered_profile_is_valid(&p));
 p.cap=PR_CAP_FE; p.mode=0;
 assert(!haproxy_modsecurity_htx_buffered_profile_is_valid(&p));
 p.mode=PR_MODE_HTTP; p.options=0;
 assert(!haproxy_modsecurity_htx_buffered_profile_is_valid(&p));
 p.options=PR_O_WREQ_BODY; p.timeout.httpreq=5001;
 assert(!haproxy_modsecurity_htx_buffered_profile_is_valid(&p));
 p.timeout.httpreq=0;
 assert(!haproxy_modsecurity_htx_buffered_profile_is_valid(&p));
 p.timeout.httpreq=TICK_ETERNITY;
 assert(!haproxy_modsecurity_htx_buffered_profile_is_valid(&p));
 p.timeout.httpreq=1;
 assert(haproxy_modsecurity_htx_buffered_profile_is_valid(&p));
 assert(!haproxy_modsecurity_htx_buffered_profile_is_valid(NULL));
 return 0;
}
'''
        with tempfile.TemporaryDirectory(dir='/var/tmp/codex/ModSecurity-conector') as raw:
            path = Path(raw)
            (path / 'scope.c').write_text(program)
            subprocess.run(['rtk', 'proxy', 'cc', '-std=c11', '-Wall', '-Wextra', '-Werror', str(path/'scope.c'), '-o', str(path/'scope')], check=True)
            subprocess.run(['rtk', 'proxy', str(path/'scope')], check=True)
        init = text[text.index('static int haproxy_modsecurity_htx_filter_init('):text.index('static void haproxy_modsecurity_htx_filter_deinit(')]
        self.assertIn('!haproxy_modsecurity_htx_buffered_profile_is_valid(px)', init)

    def test_native_parser_preserves_default_and_rejects_duplicate_unknown_mode(self):
        text = SOURCE.read_text()
        match = re.search(r'static int parse_request_mode_option\(.*?\n}\n', text, re.S)
        self.assertIsNotNone(match, 'explicit mode parser missing')
        program = r'''
#include <assert.h>
#include <stddef.h>
#include <string.h>
#define HAPROXY_MODSECURITY_HTX_BUFFERED_REQUEST_LIMIT 65536U
#define HAPROXY_MODSECURITY_HTX_PARSE_UNHANDLED 0
#define HAPROXY_MODSECURITY_HTX_PARSE_HANDLED 1
#define HAPROXY_MODSECURITY_HTX_PARSE_ERROR 2
#define memprintf(...) ((void)0)
struct haproxy_modsecurity_htx_filter_config {
 int host_buffered_request;
 struct { unsigned request_body_limit; } common_config;
};
'''+match.group(0)+r'''
int main(void) {
 struct haproxy_modsecurity_htx_filter_config c={0}; int seen=0;
 char *args[]={"request-body-mode","host-buffered",NULL};
 assert(parse_request_mode_option(&c,args,0,NULL,0,&seen)==1);
 assert(c.host_buffered_request && c.common_config.request_body_limit==65536 && seen);
 assert(parse_request_mode_option(&c,args,0,NULL,0,&seen)==2);
 seen=0; args[1]="unknown";
 assert(parse_request_mode_option(&c,args,0,NULL,0,&seen)==2);
 args[1]=NULL;
 assert(parse_request_mode_option(&c,args,0,NULL,0,&seen)==2);
 c.host_buffered_request=0; args[1]="streaming";
 assert(parse_request_mode_option(&c,args,0,NULL,0,&seen)==1);
 assert(!c.host_buffered_request);
 args[0]="another-option"; seen=0;
 assert(parse_request_mode_option(&c,args,0,NULL,0,&seen)==0);
 return 0;
}
'''
        with tempfile.TemporaryDirectory(dir='/var/tmp/codex/ModSecurity-conector') as raw:
            path = Path(raw)
            (path / 'parser.c').write_text(program)
            subprocess.run(['rtk', 'proxy', 'cc', '-std=c11', '-Wall', '-Wextra', '-Werror', '-Wno-unused-parameter', str(path/'parser.c'), '-o', str(path/'parser')], check=True)
            subprocess.run(['rtk', 'proxy', str(path/'parser')], check=True)

    def test_native_helper_rejects_incomplete_and_evaluates_before_forwarding(self):
        text = SOURCE.read_text()
        match = re.search(r'static int haproxy_modsecurity_htx_inspect_buffered_request\(.*?\n}\n', text, re.S)
        self.assertIsNotNone(match, 'bounded header-stage inspection helper missing')
        program = r'''
#include <assert.h>
#include <stddef.h>
#define ha_warning(...) ((void)0)
#define HTX_FL_EOM 1
#define FLT_CONF(f) ((f)->conf)
struct htx { unsigned flags; unsigned data; };
struct channel { struct htx buf; };
struct http_msg { struct channel *chn; };
struct stream { int unused; };
struct haproxy_modsecurity_htx_filter_context {
 struct { int disabled; char transaction_id[128]; } lifecycle;
 struct { int finished; size_t payload_bytes_seen; } request;
};
struct filter { void *ctx; };
static int calls, failures, append_error;
static struct htx *htxbuf(struct htx *b) { return b; }
static void haproxy_modsecurity_htx_fail_closed_request_phase(
 struct stream *s, struct haproxy_modsecurity_htx_filter_context *c, const char *reason) {
 (void)s; (void)reason; failures++; c->lifecycle.disabled=1;
}
static int haproxy_modsecurity_htx_append_request_payload(
 struct filter *f, struct http_msg *m, unsigned offset, unsigned len) {
 (void)f; assert(offset==0); assert(len==m->chn->buf.data); calls=calls*10+1; return append_error;
}
static int haproxy_modsecurity_htx_finish_request(
 struct stream *s, struct filter *f, struct http_msg *m,
 struct haproxy_modsecurity_htx_filter_context *c) {
 (void)s; (void)f; (void)m; calls=calls*10+2; c->request.finished=1; return 1;
}
'''+match.group(0)+r'''
int main(void) {
 struct stream s={0}; struct channel ch={{0,24}}; struct http_msg m={&ch};
 struct haproxy_modsecurity_htx_filter_context c={0}; struct filter f={&c};
 assert(haproxy_modsecurity_htx_inspect_buffered_request(&s,&f,&m)==1);
 assert(failures==1 && calls==0);
 c.lifecycle.disabled=0; ch.buf.flags=HTX_FL_EOM; append_error=1;
 haproxy_modsecurity_htx_inspect_buffered_request(&s,&f,&m);
 assert(failures==2 && calls==1 && !c.request.finished);
 c.lifecycle.disabled=0; calls=0; append_error=0;
 haproxy_modsecurity_htx_inspect_buffered_request(&s,&f,&m);
 assert(failures==2 && calls==12 && c.request.finished);
 return 0;
}
'''
        with tempfile.TemporaryDirectory(dir='/var/tmp/codex/ModSecurity-conector') as raw:
            path = Path(raw)
            (path / 'branch.c').write_text(program)
            subprocess.run(['rtk', 'proxy', 'cc', '-std=c11', '-Wall', '-Wextra', '-Werror', str(path/'branch.c'), '-o', str(path/'branch')], check=True)
            subprocess.run(['rtk', 'proxy', str(path/'branch')], check=True)

    def test_header_branch_is_explicit_and_never_registers_request_data_filter(self):
        text = SOURCE.read_text()
        start = text.index('static int haproxy_modsecurity_htx_handle_request_headers(')
        end = text.index('static int haproxy_modsecurity_htx_filter_http_headers(', start)
        body = text[start:end]
        self.assertIn('config->host_buffered_request', body)
        self.assertIn('return haproxy_modsecurity_htx_inspect_buffered_request(s, filter, msg);', body)
        self.assertIn('HAPROXY_MODSECURITY_HTX_BUFFERED_REQUEST_LIMIT 65536U', text)

    def test_versioned_profile_agrees_with_native_bounds_and_order(self):
        contract = json.loads(SOURCE.with_name('request-profile-contract.json').read_text())
        text = SOURCE.read_text()
        self.assertEqual(contract['haproxy_version'], json.loads(SOURCE.with_name('version-contract.json').read_text())['version'])
        self.assertEqual(contract['default_request_mode'], 'streaming')
        self.assertEqual(contract['request_body_limit_bytes'], 65536)
        self.assertTrue(contract['host_buffer_full_is_not_eom'])
        self.assertFalse(contract['full_b_acceptance'])
        self.assertEqual(contract['filter_config_scope'], 'pure_http_frontend')
        self.assertFalse(contract['listen_filter_allowed'])
        self.assertFalse(contract['backend_only_filter_allowed'])
        self.assertIn('px->timeout.httpreq > 5000', text)
        self.assertIn('!(px->options & PR_O_WREQ_BODY)', text)
        self.assertIn('config->host_buffered_request && config->response_companion_socket != NULL', text)


if __name__ == '__main__':
    unittest.main()
