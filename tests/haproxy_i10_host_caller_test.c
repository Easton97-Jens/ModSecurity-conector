#include <assert.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "haproxy_modsecurity_binding.h"
#include "response_companion_client.h"
#include "msconnector/block_statuses.h"
#include "msconnector/config.h"
#include "msconnector/late_intervention.h"
#include "msconnector/limits.h"
#define HAPROXY_MODSECURITY_HTX_RESPONSE_HANDLE_LENGTH 64U
#define HAPROXY_MODSECURITY_HTX_MAX_PROTOCOL_BYTES 32U
#define CF_ISRESP 1U
#define SF_ERR_KILLED 9U
struct channel { unsigned int flags; int buf; };
struct htx { int unused; };
struct htx_sl { int unused; };
struct ist { const char *ptr; size_t len; };
struct http_msg { struct channel *chn; };
struct http_txn { short status; };
struct stream { struct http_txn *txn; unsigned int replies, kills; };
struct filter { void *ctx; void *conf; };
#define FLT_CONF(f) ((f)->conf)
#define ha_warning(...) do { if (0) fprintf(stderr, __VA_ARGS__); } while (0)
/* PRODUCT_STRUCTS */
static int native_result, common_result, finish_result, commit_result;
static int open_result, claim_result, claim_calls, release_result, result_success;
static int decision_kind, append_calls, finish_calls, abort_calls, eos_calls;
static int close_result, close_calls, outcome_calls, release_calls, outcome_result, cancel_result, cancel_calls;
static struct stream *observed_stream;
static int register_calls, unregistered;
static void http_set_term_flags(struct stream *s) { (void)s; }
static void *http_error_message(struct stream *s) { (void)s; return NULL; }
static void http_reply_and_close(struct stream *s, short status, void *reply) {
    (void)reply; assert(status == s->txn->status); s->replies++;
}
static void stream_shutdown(struct stream *s, unsigned int reason) {
    assert(reason == SF_ERR_KILLED); s->kills++;
}
static void unregister_data_filter(struct stream *s, struct channel *c, struct filter *f) {
    (void)s; (void)c; (void)f; unregistered++;
}
static void register_data_filter(struct stream *s, struct channel *c, struct filter *f) {
    (void)s; (void)c; (void)f; register_calls++;
}
static void haproxy_modsecurity_htx_request_snapshot_free(struct haproxy_modsecurity_htx_filter_context *c) { (void)c; }

void haproxy_modsecurity_transaction_abort(haproxy_modsecurity_transaction *t) { (void)t; abort_calls++; }
int haproxy_modsecurity_transaction_finish(haproxy_modsecurity_transaction *t) { (void)t; finish_calls++; return finish_result; }
int haproxy_modsecurity_transaction_set_response_commit_state(haproxy_modsecurity_transaction *t, int headers, int body) {
    (void)t; assert(headers == 1 && body == 0); return commit_result;
}
int haproxy_modsecurity_transaction_finish_request_body(haproxy_modsecurity_transaction *t, haproxy_modsecurity_decision *d) {
    (void)t; memset(d, 0, sizeof(*d)); finish_calls++; return native_result;
}
int haproxy_modsecurity_transaction_finish_response_body(haproxy_modsecurity_transaction *t, haproxy_modsecurity_decision *d) {
    (void)t; memset(d, 0, sizeof(*d)); finish_calls++; return native_result;
}
static int haproxy_modsecurity_htx_append_request_payload(struct filter *f, struct http_msg *m, unsigned int o, unsigned int n) {
    (void)f; (void)m; (void)o; (void)n; append_calls++; return native_result;
}
static int haproxy_modsecurity_htx_append_response_payload(struct filter *f, struct http_msg *m, unsigned int o, unsigned int n) {
    return haproxy_modsecurity_htx_append_request_payload(f,m,o,n);
}
static int haproxy_modsecurity_htx_append_companion_response_payload(struct filter *f, struct http_msg *m, unsigned int o, unsigned int n) {
    return haproxy_modsecurity_htx_append_request_payload(f,m,o,n);
}
static int haproxy_modsecurity_htx_process_response_headers(struct stream *s, struct filter *f, struct http_msg *m) {
    (void)s; (void)m; ((struct haproxy_modsecurity_htx_filter_context *)f->ctx)->response.headers_seen = 1; return native_result;
}
static int haproxy_modsecurity_htx_companion_enabled(const struct haproxy_modsecurity_htx_filter_config *cfg) { (void)cfg; return 1; }
static int haproxy_modsecurity_htx_copy_response_handle(struct stream *s, struct haproxy_modsecurity_htx_filter_context *c) { (void)s; c->response.handle_present=1; return 0; }
int msconnector_response_companion_client_open(msconnector_response_companion_client *c, const char *path, uint64_t timeout, uid_t uid, gid_t gid, msconnector_error *e) {
    (void)path; (void)timeout; (void)uid; (void)gid; (void)e; c->opened=1; return open_result;
}
int msconnector_response_companion_client_claim(msconnector_response_companion_client *c, const char *handle, msconnector_response_companion_result *r, msconnector_error *e) {
    (void)handle; (void)e; c->claimed=1; claim_calls++; memset(r,0,sizeof(*r)); return claim_result;
}
static struct htx *htxbuf(int *b) { static struct htx h; (void)b; return &h; }
static struct htx_sl *http_get_stline(struct htx *h) { static struct htx_sl s; (void)h; return &s; }
static struct ist htx_sl_res_vsn(struct htx_sl *s) { (void)s; return (struct ist){"HTTP/1.1",8}; }
static int haproxy_modsecurity_htx_copy_headers(struct htx *h, struct haproxy_modsecurity_htx_owned_headers *out) {
    (void)h; memset(out,0,sizeof(*out)); return 0;
}
static int haproxy_modsecurity_htx_copy_common_headers(struct haproxy_modsecurity_htx_owned_headers *h, msconnector_header **out) {
    (void)h; *out=NULL; return 0;
}
static void haproxy_modsecurity_htx_owned_headers_free(struct haproxy_modsecurity_htx_owned_headers *h) { (void)h; }
static char *haproxy_modsecurity_htx_dup_ist(struct ist p, size_t max) {
    assert(p.len<=max); char *out=malloc(p.len+1); assert(out); memcpy(out,p.ptr,p.len); out[p.len]='\0'; return out;
}
static int haproxy_modsecurity_htx_handle_request_headers(struct stream *s, struct filter *f, struct http_msg *m) {
    (void)s; (void)f; (void)m; assert(0 && "terminal request was restarted"); return 1;
}
static void haproxy_modsecurity_htx_report_decision(const char *p, struct haproxy_modsecurity_htx_filter_context *c, haproxy_modsecurity_decision *d) { (void)p; (void)c; (void)d; }
static void haproxy_modsecurity_htx_report_late_decision(const struct haproxy_modsecurity_htx_filter_config *cfg, struct haproxy_modsecurity_htx_filter_context *c, haproxy_modsecurity_decision *d) { (void)cfg; (void)c; (void)d; }
static void haproxy_modsecurity_htx_companion_result_reset(msconnector_response_companion_result *r) { memset(r,0,sizeof(*r)); }
static int result(msconnector_response_companion_result *r) {
    r->success = result_success; r->decision = decision_kind; r->status = decision_kind == MSCONNECTOR_DECISION_KIND_DENY ? 403 : 200; return common_result;
}
int msconnector_response_companion_client_response_headers(msconnector_response_companion_client *c, const msconnector_response *response, msconnector_response_companion_result *r, msconnector_error *e) {
    (void)c; (void)response; (void)e; return result(r);
}
int msconnector_response_companion_client_body_eos(msconnector_response_companion_client *c, msconnector_response_companion_result *r, msconnector_error *e) {
    (void)e; eos_calls++; c->response_eos = 1; return result(r);
}
int msconnector_response_companion_client_body_chunk(msconnector_response_companion_client *c, const unsigned char *d, size_t n, msconnector_response_companion_result *r, msconnector_error *e) {
    (void)c; (void)d; (void)n; (void)e; append_calls++; return result(r);
}
int msconnector_response_companion_client_commit(msconnector_response_companion_client *c, int h, int b, msconnector_response_companion_result *r, msconnector_error *e) {
    (void)c; (void)h; (void)b; (void)e; return result(r);
}
int msconnector_response_companion_client_outcome(msconnector_response_companion_client *c, msconnector_decision_action a, int s, int aborted, msconnector_response_companion_result *r, msconnector_error *e) {
    (void)c; (void)s; (void)e; outcome_calls++; assert(!aborted && "requested kill is not observed abort");
    if (a == MSCONNECTOR_DECISION_ACTION_DENY) assert(observed_stream->replies == 1);
    (void)result(r); return outcome_result;
}
int msconnector_response_companion_client_release(msconnector_response_companion_client *c, msconnector_response_companion_result *r, msconnector_error *e) {
    (void)c; (void)e; release_calls++; (void)result(r); return release_result;
}
int msconnector_response_companion_client_close(msconnector_response_companion_client *c, msconnector_error *e) {
    (void)e; close_calls++; c->opened=0; c->claimed=0; c->closed=1; return close_result;
}
int msconnector_response_companion_client_cancel_with_cause(msconnector_response_companion_client *c, msconnector_response_companion_cancel_cause cause, msconnector_response_companion_result *r, msconnector_error *e) {
    (void)c; (void)cause; (void)e; cancel_calls++; (void)result(r); return cancel_result;
}
/* PRODUCT_FUNCTIONS */
static void reset(struct haproxy_modsecurity_htx_filter_context *c, struct stream *s) {
    memset(c,0,sizeof(*c)); c->transaction = (haproxy_modsecurity_transaction *)c;
    c->request.headers_seen = 1; c->response.headers_seen = 1;
    c->request.finished = 1; c->companion.client.claimed = 1; c->companion.client.opened=1;
    s->txn->status = 200; s->replies = 0; s->kills = 0;
    native_result = 1; common_result = 1; finish_result = 0; commit_result = 0;
    open_result=claim_result=release_result=result_success=1; claim_calls=0;
    observed_stream = s; outcome_result = 1; cancel_result = 1; cancel_calls = 0;
    close_result = 1; decision_kind = MSCONNECTOR_DECISION_KIND_ALLOW;
    append_calls = finish_calls = abort_calls = eos_calls = close_calls = 0;
    outcome_calls = release_calls = register_calls = unregistered = 0;
}
int main(void) {
    struct haproxy_modsecurity_htx_filter_context c;
    struct haproxy_modsecurity_htx_filter_config config = {0};
    struct filter f = {&c,&config}; struct http_txn txn = {200};
    struct stream s = {&txn,0,0}, neighbour = {&txn,0,0};
    struct channel request_channel = {0,0}, response_channel = {CF_ISRESP,0};
    struct http_msg req = {&request_channel}, res = {&response_channel};
    const int modes[] = {MSCONNECTOR_PHASE4_MODE_OFF, MSCONNECTOR_PHASE4_MODE_SAFE, MSCONNECTOR_PHASE4_MODE_STRICT};
    const int invalid[] = {0,-1,2};
    msconnector_response_companion_result forwardable={0};
    forwardable.decision=MSCONNECTOR_DECISION_KIND_ALLOW;
    for(size_t bad=0;bad<3;bad++) {
        forwardable.success=invalid[bad];
        assert(!haproxy_modsecurity_htx_companion_result_is_forwardable(&forwardable));
    }
    forwardable.success=1;
    assert(haproxy_modsecurity_htx_companion_result_is_forwardable(&forwardable));
    for (size_t mode = 0; mode < 3; mode++) {
        config.common_config.phase4_mode = modes[mode];
        for (int companion = 0; companion < 2; companion++) {
            for (int commitment = 0; commitment < 3; commitment++) {
                reset(&c,&s); c.companion.mode = companion;
                c.response.headers_committed = commitment != 0;
                c.response.body_started = commitment == 2;
                haproxy_modsecurity_htx_fail_closed_request_phase(&s,&c,"technical failure");
                assert(c.lifecycle.fail_closed && c.lifecycle.disabled);
                assert(s.replies == (unsigned int)(commitment == 0));
                assert(s.kills == (unsigned int)(commitment != 0));
                assert(commitment == 0 ? txn.status == 503 : txn.status == 200);
                haproxy_modsecurity_htx_fail_closed_request_phase(&s,&c,"second failure");
                assert(s.replies + s.kills == 1 && abort_calls == 1);
                assert(haproxy_modsecurity_htx_filter_http_headers(&s,&f,&req) == -1);
                assert(haproxy_modsecurity_htx_filter_request_payload(&s,&f,&req,0,4) == -1);
                assert(haproxy_modsecurity_htx_filter_http_payload(&s,&f,&res,0,4) == -1);
                assert(haproxy_modsecurity_htx_filter_http_end(&s,&f,&res) == -1);
                assert(append_calls == 0 && eos_calls == 0 && finish_calls == 0);
                assert(neighbour.replies == 0 && neighbour.kills == 0);
            }
        }
        reset(&c,&s); c.response.headers_committed = 1;
        haproxy_modsecurity_htx_handle_response_headers(&s,&f,&res);
        assert(s.kills == 1 && s.replies == 0 && txn.status == 200);
        /* Binding failures reach the actual direct payload/EOS host caller. */
        reset(&c,&s); c.request.finished = 0;
        assert(haproxy_modsecurity_htx_filter_http_payload(&s,&f,&req,0,4) == -1);
        assert(s.replies == 1 && append_calls == 1 && abort_calls == 1);
        reset(&c,&s); c.response.headers_committed = 1;
        assert(haproxy_modsecurity_htx_filter_http_payload(&s,&f,&res,0,4) == -1);
        assert(s.kills == 1 && s.replies == 0 && append_calls == 1);
        reset(&c,&s); c.response.headers_committed = 1;
        haproxy_modsecurity_htx_filter_http_end(&s,&f,&res);
        assert(s.kills == 1 && s.replies == 0 && finish_calls == 1);
        /* Failed terminal Common completion may never turn into success. */
        reset(&c,&s); native_result = 0; finish_result = 1;
        haproxy_modsecurity_htx_filter_http_end(&s,&f,&res);
        assert(s.kills == 1 && s.replies == 0 && finish_calls == 2);
        /* Header commit ack failure remains precommit. */
        reset(&c,&s); native_result = 0; commit_result = 1;
        haproxy_modsecurity_htx_handle_response_headers(&s,&f,&res);
        assert(s.replies == 1 && s.kills == 0 && !c.response.headers_committed && register_calls == 0);
        for (size_t bad = 0; bad < 3; bad++) {
            reset(&c,&s); c.companion.mode=1; c.transaction=NULL;
            result_success=invalid[bad];
            assert(haproxy_modsecurity_htx_process_companion_response_headers(&s,&f,&res)==-1);
            assert(s.replies==1 && txn.status==503 && outcome_calls==0);
            reset(&c,&s); c.companion.mode=1; c.transaction=NULL;
            result_success=invalid[bad];
            haproxy_modsecurity_htx_filter_http_end(&s,&f,&res);
            assert(s.kills==1 && release_calls==0 && outcome_calls==0);
            reset(&c,&s); open_result=invalid[bad];
            assert(!haproxy_modsecurity_htx_companion_open_and_claim(&s,&config,&c));
            assert(claim_calls==0 && close_calls==1);
            reset(&c,&s); claim_result=invalid[bad];
            assert(!haproxy_modsecurity_htx_companion_open_and_claim(&s,&config,&c));
            assert(claim_calls==1 && close_calls==1);
            reset(&c,&s); c.companion.mode=1; c.transaction=NULL;
            release_result=invalid[bad];
            assert(haproxy_modsecurity_htx_filter_http_end(&s,&f,&res)==1);
            assert(s.kills==1 && s.replies==0 && release_calls==1 && close_calls==1 && outcome_calls==0);
            assert(haproxy_modsecurity_htx_filter_http_end(&s,&f,&res)==-1);
            assert(release_calls==1 && close_calls==1);
            reset(&c,&s); c.companion.mode = 1; c.transaction = NULL;
            common_result = invalid[bad];
            assert(!haproxy_modsecurity_htx_companion_commit(&c));
            reset(&c,&s); c.companion.mode = 1; c.transaction = NULL;
            common_result = invalid[bad];
            assert(haproxy_modsecurity_htx_send_companion_response_chunk(&c,"x",1) == -1);
            reset(&c,&s); c.companion.mode = 1; c.transaction = NULL;
            common_result = invalid[bad]; c.response.headers_committed = 1;
            haproxy_modsecurity_htx_filter_http_end(&s,&f,&res);
            assert(s.kills == 1 && s.replies == 0 && eos_calls == 1);
            assert(haproxy_modsecurity_htx_filter_http_end(&s,&f,&res) == -1);
            assert(eos_calls == 1 && close_calls == 1 && outcome_calls == 0 && release_calls == 0);
        }
        /* Actual P3 caller: error results are technical, failed host outcome
         * acknowledgement occurs after its single reply and kills the stream. */
        reset(&c,&s); c.companion.mode = 1; c.transaction = NULL;
        decision_kind = MSCONNECTOR_DECISION_KIND_ERROR;
        assert(haproxy_modsecurity_htx_process_companion_response_headers(&s,&f,&res) == -1);
        assert(s.replies == 1 && txn.status == 503 && outcome_calls == 0);
        reset(&c,&s); c.companion.mode = 1; c.transaction = NULL;
        decision_kind = MSCONNECTOR_DECISION_KIND_DENY; outcome_result = -1;
        assert(haproxy_modsecurity_htx_process_companion_response_headers(&s,&f,&res) == -1);
        assert(s.replies == 1 && txn.status == 403 && s.kills == 1 && outcome_calls == 1);
        assert(c.lifecycle.fail_closed);
        for (int bad_cleanup = 0; bad_cleanup < 2; bad_cleanup++) {
            reset(&c,&s); c.companion.mode=1; c.transaction=NULL;
            decision_kind=MSCONNECTOR_DECISION_KIND_DENY;
            if (bad_cleanup) close_result=-1; else cancel_result=-1;
            assert(haproxy_modsecurity_htx_process_companion_response_headers(&s,&f,&res) == -1);
            assert(s.replies==1 && s.kills==1 && outcome_calls==1);
            assert(cancel_calls==1 && close_calls==1 && c.lifecycle.fail_closed);
            assert(haproxy_modsecurity_htx_filter_http_end(&s,&f,&res)==-1);
            assert(cancel_calls==1 && close_calls==1);
        }
        /* Successful EOS containing a technical error is still terminal,
         * independently of Off/Safe rule downgrade. No fabricated observation. */
        reset(&c,&s); c.companion.mode = 1; c.transaction = NULL;
        decision_kind = MSCONNECTOR_DECISION_KIND_ERROR;
        haproxy_modsecurity_htx_filter_http_end(&s,&f,&res);
        assert(s.kills == 1 && s.replies == 0 && outcome_calls == 0);
        reset(&c,&s); c.companion.mode = 1; c.transaction = NULL;
        close_result = -1;
        haproxy_modsecurity_htx_filter_http_end(&s,&f,&res);
        assert(s.kills == 1 && s.replies == 0);
        /* Legitimate allow completes, with no host kill or synthetic reply. */
        reset(&c,&s); c.companion.mode = 1; c.transaction = NULL;
        haproxy_modsecurity_htx_filter_http_end(&s,&f,&res);
        assert(s.kills == 0 && s.replies == 0 && eos_calls == 1 && release_calls == 1);
    }
    puts("HAProxy HTX direct/companion: Off/Safe/Strict config x pre/header/body x terminal reentry; native, commit, EOS, close, checked OPEN/CLAIM/RELEASE and nested success");
    return 0;
}
