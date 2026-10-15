#include "haproxy_modsecurity_binding.h"
#include "msconnector/block_statuses.h"
#include "msconnector/config.h"
#include "msconnector/late_intervention.h"
#include "msconnector/limits.h"
#include "response_companion_client.h"
#include <assert.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

/* Real ABI declarations above; controlled readonly hooks below. */
#define haproxy_modsecurity_transaction_abort                                  \
  fixture_haproxy_modsecurity_transaction_abort
#define haproxy_modsecurity_transaction_finish_with_decision                   \
  fixture_haproxy_modsecurity_transaction_finish_with_decision
#define haproxy_modsecurity_transaction_set_response_commit_state              \
  fixture_haproxy_modsecurity_transaction_set_response_commit_state
#define haproxy_modsecurity_transaction_finish_request_body                    \
  fixture_haproxy_modsecurity_transaction_finish_request_body
#define haproxy_modsecurity_transaction_finish_response_body                   \
  fixture_haproxy_modsecurity_transaction_finish_response_body
#define msconnector_response_companion_client_open                             \
  fixture_msconnector_response_companion_client_open
#define msconnector_response_companion_client_claim                            \
  fixture_msconnector_response_companion_client_claim
#define msconnector_response_companion_client_response_headers                 \
  fixture_msconnector_response_companion_client_response_headers
#define msconnector_response_companion_client_body_eos                         \
  fixture_msconnector_response_companion_client_body_eos
#define msconnector_response_companion_client_body_chunk                       \
  fixture_msconnector_response_companion_client_body_chunk
#define msconnector_response_companion_client_commit                           \
  fixture_msconnector_response_companion_client_commit
#define msconnector_response_companion_client_outcome                          \
  fixture_msconnector_response_companion_client_outcome
#define msconnector_response_companion_client_release                          \
  fixture_msconnector_response_companion_client_release
#define msconnector_response_companion_client_close                            \
  fixture_msconnector_response_companion_client_close
#define msconnector_response_companion_client_cancel_with_cause                \
  fixture_msconnector_response_companion_client_cancel_with_cause
#define HAPROXY_MODSECURITY_HTX_RESPONSE_HANDLE_LENGTH 64U
#define HAPROXY_MODSECURITY_HTX_MAX_PROTOCOL_BYTES 32U
#define CF_ISRESP 1U
#define SF_ERR_KILLED 9U
#define SC_FL_NOLINGER 4U
struct channel {
  unsigned int flags;
  int buf;
  size_t output;
};
struct htx {
  int unused;
};
struct htx_sl {
  int unused;
};
struct ist {
  const char *ptr;
  size_t len;
};
struct http_msg {
  struct channel *chn;
};
struct http_txn {
  short status;
};
struct stconn { unsigned int flags, aborts, shutdowns; };
struct stream {
  struct http_txn *txn;
  unsigned int replies;
  unsigned int kills;
  unsigned int stream_aborts;
  struct channel res;
  struct stconn frontend;
  struct stconn *scf;
  size_t delivered_bytes;
};
struct filter {
  void *ctx;
  void *conf;
};
#define FLT_CONF(f) ((f)->conf)
#define ha_warning(...)                                                        \
  do {                                                                         \
    if (0)                                                                     \
      fprintf(stderr, __VA_ARGS__);                                            \
  } while (0)
#define haproxy_modsecurity_transaction_error fixture_haproxy_modsecurity_transaction_error
#define haproxy_modsecurity_error_event_write fixture_haproxy_modsecurity_error_event_write
static msconnector_transaction_error_class fixture_haproxy_modsecurity_transaction_error(
    const haproxy_modsecurity_transaction *t) {
  (void)t;
  return MSCONNECTOR_TRANSACTION_ERROR_CONNECTOR;
}
static int fixture_haproxy_modsecurity_error_event_write(
    const haproxy_modsecurity_decision *d, const char *id, char *line, size_t capacity) {
  assert(d->error_class != MSCONNECTOR_TRANSACTION_ERROR_NONE);
  (void)id;
  return snprintf(line, capacity, "typed technical error\n") > 0;
}
/* PRODUCT_STRUCTS */
static int native_result;
static int native_disruptive;
static int common_result;
static int finish_result;
static int commit_result;
static int open_result;
static int claim_result;
static int claim_calls;
static int release_result;
static int result_success;
static int decision_kind;
static int append_calls;
static int finish_calls;
static int abort_calls;
static int eos_calls;
static int close_result;
static int close_calls;
static int outcome_calls;
static int release_calls;
static int outcome_result;
static int cancel_result;
static int cancel_calls;
static struct stream *observed_stream;
static int register_calls;
static int unregistered;
static void http_set_term_flags(const struct stream *s) { (void)s; }
static void *http_error_message(const struct stream *s) {
  (void)s;
  return NULL;
}
static void http_reply_and_close(struct stream *s, short status, void *reply) {
  (void)reply;
  assert(status == s->txn->status);
  s->replies++;
}
void channel_htx_erase(struct channel *channel, struct htx *htx) {
  (void)htx;
  channel->output = 0;
  channel->buf = 0;
}
void stream_abort(struct stream *s) { s->stream_aborts++; }
void sc_abort(struct stconn *sc) { sc->aborts++; }
void sc_shutdown(struct stconn *sc) { sc->shutdowns++; }
static void stream_shutdown(struct stream *s, unsigned int reason) {
  assert(reason == SF_ERR_KILLED);
  s->kills++;
}
static void unregister_data_filter(const struct stream *s,
                                   const struct channel *c,
                                   const struct filter *f) {
  (void)s;
  (void)c;
  (void)f;
  unregistered++;
}
static void register_data_filter(const struct stream *s,
                                 const struct channel *c,
                                 const struct filter *f) {
  (void)s;
  (void)c;
  (void)f;
  register_calls++;
}
static void haproxy_modsecurity_htx_request_snapshot_free(
    const struct haproxy_modsecurity_htx_filter_context *c) {
  (void)c;
}

static void fixture_haproxy_modsecurity_transaction_abort(
    const haproxy_modsecurity_transaction *t) {
  (void)t;
  abort_calls++;
}
static int fixture_haproxy_modsecurity_transaction_finish_with_decision(
    const haproxy_modsecurity_transaction *t, haproxy_modsecurity_decision *d) {
  if (finish_result != 0) d->error_class = MSCONNECTOR_TRANSACTION_ERROR_CLEANUP_INCOMPLETE;
  (void)t;
  finish_calls++;
  return finish_result;
}
static int fixture_haproxy_modsecurity_transaction_set_response_commit_state(
    const haproxy_modsecurity_transaction *t, int headers, int body) {
  (void)t;
  assert(headers == 1 && body == 0);
  return commit_result;
}
static int fixture_haproxy_modsecurity_transaction_finish_request_body(
    const haproxy_modsecurity_transaction *t, haproxy_modsecurity_decision *d) {
  (void)t;
  memset(d, 0, sizeof(*d));
  finish_calls++;
  return native_result;
}
static int fixture_haproxy_modsecurity_transaction_finish_response_body(
    const haproxy_modsecurity_transaction *t, haproxy_modsecurity_decision *d) {
  (void)t;
  memset(d, 0, sizeof(*d));
  d->disruptive = native_disruptive;
  d->status = native_disruptive ? 403 : 200;
  finish_calls++;
  return native_result;
}
static int
haproxy_modsecurity_htx_append_request_payload(const struct filter *f,
                                               const struct http_msg *m,
                                               unsigned int o, unsigned int n) {
  (void)f;
  (void)m;
  (void)o;
  (void)n;
  append_calls++;
  return native_result;
}
static int haproxy_modsecurity_htx_append_response_payload(
    const struct filter *f, const struct http_msg *m, unsigned int o,
    unsigned int n) {
  return haproxy_modsecurity_htx_append_request_payload(f, m, o, n);
}
static int haproxy_modsecurity_htx_append_companion_response_payload(
    const struct filter *f, const struct http_msg *m, unsigned int o,
    unsigned int n) {
  return haproxy_modsecurity_htx_append_request_payload(f, m, o, n);
}
static int haproxy_modsecurity_htx_process_response_headers(
    const struct stream *s, struct filter *f, const struct http_msg *m) {
  (void)s;
  (void)m;
  ((struct haproxy_modsecurity_htx_filter_context *)f->ctx)
      ->response.headers_seen = 1;
  return native_result;
}
static int haproxy_modsecurity_htx_companion_enabled(
    const struct haproxy_modsecurity_htx_filter_config *cfg) {
  (void)cfg;
  return 1;
}
static int haproxy_modsecurity_htx_copy_response_handle(
    const struct stream *s, struct haproxy_modsecurity_htx_filter_context *c) {
  (void)s;
  c->response.handle_present = 1;
  return 0;
}
static int fixture_msconnector_response_companion_client_open(
    msconnector_response_companion_client *c, const char *path,
    uint64_t timeout, uid_t uid, gid_t gid, const msconnector_error *e) {
  (void)path;
  (void)timeout;
  (void)uid;
  (void)gid;
  (void)e;
  c->opened = 1;
  return open_result;
}
static int fixture_msconnector_response_companion_client_claim(
    msconnector_response_companion_client *c, const char *handle,
    msconnector_response_companion_result *r, const msconnector_error *e) {
  (void)handle;
  (void)e;
  c->claimed = 1;
  claim_calls++;
  memset(r, 0, sizeof(*r));
  return claim_result;
}
static struct htx *htxbuf(const int *b) {
  static struct htx h;
  (void)b;
  return &h;
}
static struct htx_sl *http_get_stline(const struct htx *h) {
  static struct htx_sl s;
  (void)h;
  return &s;
}
static struct ist htx_sl_res_vsn(const struct htx_sl *s) {
  (void)s;
  return (struct ist){"HTTP/1.1", 8};
}
static int haproxy_modsecurity_htx_copy_headers(
    const struct htx *h, struct haproxy_modsecurity_htx_owned_headers *out) {
  (void)h;
  memset(out, 0, sizeof(*out));
  return 0;
}
static int haproxy_modsecurity_htx_copy_common_headers(
    const struct haproxy_modsecurity_htx_owned_headers *h,
    msconnector_header **out) {
  (void)h;
  *out = NULL;
  return 0;
}
static void haproxy_modsecurity_htx_owned_headers_free(
    const struct haproxy_modsecurity_htx_owned_headers *h) {
  (void)h;
}
static char *haproxy_modsecurity_htx_dup_ist(struct ist p, size_t max) {
  assert(p.len <= max);
  char *out = malloc(p.len + 1);
  assert(out);
  memcpy(out, p.ptr, p.len);
  out[p.len] = '\0';
  return out;
}
static int haproxy_modsecurity_htx_handle_request_headers(
    const struct stream *s, const struct filter *f, const struct http_msg *m) {
  (void)s;
  (void)f;
  (void)m;
  assert(0 && "terminal request was restarted");
  return 1;
}
static void haproxy_modsecurity_htx_report_decision(
    const char *p, const struct haproxy_modsecurity_htx_filter_context *c,
    const haproxy_modsecurity_decision *d) {
  (void)p;
  (void)c;
  (void)d;
}
static void haproxy_modsecurity_htx_report_late_decision(
    const struct haproxy_modsecurity_htx_filter_config *cfg,
    const struct haproxy_modsecurity_htx_filter_context *c,
    const haproxy_modsecurity_decision *d) {
  (void)cfg;
  (void)c;
  (void)d;
}
static void haproxy_modsecurity_htx_companion_result_reset(
    msconnector_response_companion_result *r) {
  memset(r, 0, sizeof(*r));
}
static int result(msconnector_response_companion_result *r) {
  r->success = result_success;
  r->decision = decision_kind;
  r->status = decision_kind == MSCONNECTOR_DECISION_KIND_DENY ? 403 : 200;
  return common_result;
}
static int fixture_msconnector_response_companion_client_response_headers(
    const msconnector_response_companion_client *c,
    const msconnector_response *response,
    msconnector_response_companion_result *r, const msconnector_error *e) {
  (void)c;
  (void)response;
  (void)e;
  return result(r);
}
static int fixture_msconnector_response_companion_client_body_eos(
    msconnector_response_companion_client *c,
    msconnector_response_companion_result *r, const msconnector_error *e) {
  (void)e;
  eos_calls++;
  c->response_eos = 1;
  return result(r);
}
static int fixture_msconnector_response_companion_client_body_chunk(
    const msconnector_response_companion_client *c, const unsigned char *d,
    size_t n, msconnector_response_companion_result *r,
    const msconnector_error *e) {
  (void)c;
  (void)d;
  (void)n;
  (void)e;
  append_calls++;
  return result(r);
}
static int fixture_msconnector_response_companion_client_commit(
    const msconnector_response_companion_client *c, int h, int b,
    msconnector_response_companion_result *r, const msconnector_error *e) {
  (void)c;
  (void)h;
  (void)b;
  (void)e;
  return result(r);
}
static int fixture_msconnector_response_companion_client_outcome(
    const msconnector_response_companion_client *c,
    msconnector_decision_action a, int s, int aborted,
    msconnector_response_companion_result *r, const msconnector_error *e) {
  (void)c;
  (void)s;
  (void)e;
  outcome_calls++;
  assert(!aborted && "requested kill is not observed abort");
  if (a == MSCONNECTOR_DECISION_ACTION_DENY)
    assert(observed_stream->replies == 1);
  (void)result(r);
  return outcome_result;
}
static int fixture_msconnector_response_companion_client_release(
    const msconnector_response_companion_client *c,
    msconnector_response_companion_result *r, const msconnector_error *e) {
  (void)c;
  (void)e;
  release_calls++;
  (void)result(r);
  return release_result;
}
static int fixture_msconnector_response_companion_client_close(
    msconnector_response_companion_client *c, const msconnector_error *e) {
  (void)e;
  close_calls++;
  c->opened = 0;
  c->claimed = 0;
  c->closed = 1;
  return close_result;
}
static int fixture_msconnector_response_companion_client_cancel_with_cause(
    const msconnector_response_companion_client *c,
    msconnector_response_companion_cancel_cause cause,
    msconnector_response_companion_result *r, const msconnector_error *e) {
  (void)c;
  (void)cause;
  (void)e;
  cancel_calls++;
  (void)result(r);
  return cancel_result;
}
/* PRODUCT_FUNCTIONS */
static void reset(struct haproxy_modsecurity_htx_filter_context *c,
                  struct stream *s) {
  memset(c, 0, sizeof(*c));
  c->transaction = (haproxy_modsecurity_transaction *)c;
  c->request.headers_seen = 1;
  c->response.headers_seen = 1;
  c->request.finished = 1;
  c->companion.client.claimed = 1;
  c->companion.client.opened = 1;
  s->txn->status = 200;
  s->replies = 0;
  s->kills = 0;
  s->stream_aborts = 0;
  s->res.output = 0;
  s->delivered_bytes = 0;
  memset(&s->frontend, 0, sizeof(s->frontend));
  s->scf = &s->frontend;
  native_disruptive = 0;
  native_result = 1;
  common_result = 1;
  finish_result = 0;
  commit_result = 0;
  open_result = 1;
  claim_result = 1;
  release_result = 1;
  result_success = 1;
  claim_calls = 0;
  observed_stream = s;
  outcome_result = 1;
  cancel_result = 1;
  cancel_calls = 0;
  close_result = 1;
  decision_kind = MSCONNECTOR_DECISION_KIND_ALLOW;
  append_calls = 0;
  finish_calls = 0;
  abort_calls = 0;
  eos_calls = 0;
  close_calls = 0;
  outcome_calls = 0;
  release_calls = 0;
  register_calls = 0;
  unregistered = 0;
}
struct fixture_environment {
  struct haproxy_modsecurity_htx_filter_context c;
  struct haproxy_modsecurity_htx_filter_config config;
  struct filter f;
  struct http_txn txn;
  struct stream s;
  struct stream neighbour;
  struct channel request_channel;
  struct channel response_channel;
  struct http_msg req;
  struct http_msg res;
};
static void initialize_environment(struct fixture_environment *e) {
  memset(e, 0, sizeof(*e));
  e->f = (struct filter){&e->c, &e->config};
  e->s.txn = &e->txn;
  e->neighbour.txn = &e->txn;
  e->response_channel.flags = CF_ISRESP;
  e->req.chn = &e->request_channel;
  e->res.chn = &e->response_channel;
}
static void check_forwardable(void) {
  const int invalid[] = {0, -1, 2};
  msconnector_response_companion_result forwardable = {0};
  forwardable.decision = MSCONNECTOR_DECISION_KIND_ALLOW;
  for (size_t bad = 0; bad < 3; bad++) {
    forwardable.success = invalid[bad];
    assert(
        !haproxy_modsecurity_htx_companion_result_is_forwardable(&forwardable));
  }
  forwardable.success = 1;
  assert(haproxy_modsecurity_htx_companion_result_is_forwardable(&forwardable));
}
static void check_terminal(struct fixture_environment *e, int companion,
                           int commitment) {
  reset(&e->c, &e->s);
  e->c.companion.mode = companion;
  e->c.response.headers_committed = commitment != 0;
  e->c.response.body_started = commitment == 2;
  haproxy_modsecurity_htx_fail_closed_request_phase(&e->s, &e->c,
                                                    "technical failure");
  assert(e->c.lifecycle.fail_closed && e->c.lifecycle.disabled);
  assert(e->s.replies == (unsigned int)(commitment == 0));
  assert(e->s.kills == (unsigned int)(commitment != 0));
  assert(commitment == 0 ? e->txn.status == 503 : e->txn.status == 200);
  haproxy_modsecurity_htx_fail_closed_request_phase(&e->s, &e->c,
                                                    "second failure");
  assert(e->s.replies + e->s.kills == 1 && abort_calls == 1);
  assert(haproxy_modsecurity_htx_filter_http_headers(&e->s, &e->f, &e->req) ==
         -1);
  assert(haproxy_modsecurity_htx_filter_request_payload(&e->s, &e->f, &e->req,
                                                        0, 4) == -1);
  assert(haproxy_modsecurity_htx_filter_http_payload(&e->s, &e->f, &e->res, 0,
                                                     4) == -1);
  assert(haproxy_modsecurity_htx_filter_http_end(&e->s, &e->f, &e->res) == -1);
  assert(append_calls == 0 && eos_calls == 0 && finish_calls == 0);
  assert(e->neighbour.replies == 0 && e->neighbour.kills == 0);
}
static void check_direct(struct fixture_environment *e) {
  reset(&e->c, &e->s);
  e->c.response.headers_committed = 1;
  haproxy_modsecurity_htx_handle_response_headers(&e->s, &e->f, &e->res);
  assert(e->s.kills == 1 && e->s.replies == 0 && e->txn.status == 200);
  /* Binding failures reach the actual direct payload/EOS host caller. */
  reset(&e->c, &e->s);
  e->c.request.finished = 0;
  assert(haproxy_modsecurity_htx_filter_http_payload(&e->s, &e->f, &e->req, 0,
                                                     4) == -1);
  assert(e->s.replies == 1 && append_calls == 1 && abort_calls == 1);
  reset(&e->c, &e->s);
  e->c.response.headers_committed = 1;
  assert(haproxy_modsecurity_htx_filter_http_payload(&e->s, &e->f, &e->res, 0,
                                                     4) == -1);
  assert(e->s.kills == 1 && e->s.replies == 0 && append_calls == 1);
  reset(&e->c, &e->s);
  e->c.response.headers_committed = 1;
  haproxy_modsecurity_htx_filter_http_end(&e->s, &e->f, &e->res);
  assert(e->s.kills == 1 && e->s.replies == 0 && finish_calls == 1);
  /* Failed terminal Common completion may never turn into success. */
  reset(&e->c, &e->s);
  native_result = 0;
  finish_result = 1;
  haproxy_modsecurity_htx_filter_http_end(&e->s, &e->f, &e->res);
  assert(e->s.kills == 1 && e->s.replies == 0 && finish_calls == 2);
  /* Header commit ack failure remains precommit. */
  reset(&e->c, &e->s);
  native_result = 0;
  commit_result = 1;
  haproxy_modsecurity_htx_handle_response_headers(&e->s, &e->f, &e->res);
  assert(e->s.replies == 1 && e->s.kills == 0 &&
         !e->c.response.headers_committed && register_calls == 0);
}
static void check_invalid(struct fixture_environment *e, int invalid_result) {
  reset(&e->c, &e->s);
  e->c.companion.mode = 1;
  e->c.transaction = NULL;
  result_success = invalid_result;
  assert(haproxy_modsecurity_htx_process_companion_response_headers(
             &e->s, &e->f, &e->res) == -1);
  assert(e->s.replies == 1 && e->txn.status == 503 && outcome_calls == 0);
  reset(&e->c, &e->s);
  e->c.companion.mode = 1;
  e->c.transaction = NULL;
  result_success = invalid_result;
  haproxy_modsecurity_htx_filter_http_end(&e->s, &e->f, &e->res);
  assert(e->s.kills == 1 && release_calls == 0 && outcome_calls == 0);
  reset(&e->c, &e->s);
  open_result = invalid_result;
  assert(!haproxy_modsecurity_htx_companion_open_and_claim(&e->s, &e->config,
                                                           &e->c));
  assert(claim_calls == 0 && close_calls == 1);
  reset(&e->c, &e->s);
  claim_result = invalid_result;
  assert(!haproxy_modsecurity_htx_companion_open_and_claim(&e->s, &e->config,
                                                           &e->c));
  assert(claim_calls == 1 && close_calls == 1);
  reset(&e->c, &e->s);
  e->c.companion.mode = 1;
  e->c.transaction = NULL;
  release_result = invalid_result;
  assert(haproxy_modsecurity_htx_filter_http_end(&e->s, &e->f, &e->res) == -1);
  assert(e->s.kills == 1 && e->s.replies == 0 && release_calls == 1 &&
         close_calls == 1 && outcome_calls == 0);
  assert(haproxy_modsecurity_htx_filter_http_end(&e->s, &e->f, &e->res) == -1);
  assert(release_calls == 1 && close_calls == 1);
  reset(&e->c, &e->s);
  e->c.companion.mode = 1;
  e->c.transaction = NULL;
  common_result = invalid_result;
  assert(!haproxy_modsecurity_htx_companion_commit(&e->c));
  reset(&e->c, &e->s);
  e->c.companion.mode = 1;
  e->c.transaction = NULL;
  common_result = invalid_result;
  assert(haproxy_modsecurity_htx_send_companion_response_chunk(&e->c, "x", 1) ==
         -1);
  reset(&e->c, &e->s);
  e->c.companion.mode = 1;
  e->c.transaction = NULL;
  common_result = invalid_result;
  e->c.response.headers_committed = 1;
  haproxy_modsecurity_htx_filter_http_end(&e->s, &e->f, &e->res);
  assert(e->s.kills == 1 && e->s.replies == 0 && eos_calls == 1);
  assert(haproxy_modsecurity_htx_filter_http_end(&e->s, &e->f, &e->res) == -1);
  assert(eos_calls == 1 && close_calls == 1 && outcome_calls == 0 &&
         release_calls == 0);
}
static void check_precommit_cleanup_failure(struct fixture_environment *e,
                                           int bad_close) {
  reset(&e->c, &e->s);
  e->c.companion.mode = 1;
  e->c.transaction = NULL;
  decision_kind = MSCONNECTOR_DECISION_KIND_DENY;
  if (bad_close)
    close_result = -1;
  else
    release_result = -1;
  assert(haproxy_modsecurity_htx_process_companion_response_headers(
             &e->s, &e->f, &e->res) == -1);
  assert(e->s.replies == 1 && e->s.kills == 1 && outcome_calls == 1);
  assert(cancel_calls == (bad_close ? 0 : 1) && release_calls == 1 &&
         close_calls == 1 && e->c.lifecycle.fail_closed);
  assert(haproxy_modsecurity_htx_filter_http_end(&e->s, &e->f, &e->res) == -1);
  assert(cancel_calls == (bad_close ? 0 : 1) && close_calls == 1);
}
static void check_precommit(struct fixture_environment *e) {
  /* A real precommit deny is normal terminal policy cleanup after its
   * acknowledged host outcome, never a typed technical cancellation. */
  reset(&e->c, &e->s);
  e->c.companion.mode = 1;
  e->c.transaction = NULL;
  decision_kind = MSCONNECTOR_DECISION_KIND_DENY;
  assert(haproxy_modsecurity_htx_process_companion_response_headers(
             &e->s, &e->f, &e->res) == 1);
  assert(e->s.replies == 1 && e->txn.status == 403 && e->s.kills == 0);
  assert(outcome_calls == 1 && release_calls == 1 && cancel_calls == 0 && close_calls == 1);
  /* Actual P3 caller: error results are technical, failed host outcome
   * acknowledgement occurs after its single reply and kills the stream. */
  reset(&e->c, &e->s);
  e->c.companion.mode = 1;
  e->c.transaction = NULL;
  decision_kind = MSCONNECTOR_DECISION_KIND_ERROR;
  assert(haproxy_modsecurity_htx_process_companion_response_headers(
             &e->s, &e->f, &e->res) == -1);
  assert(e->s.replies == 1 && e->txn.status == 503 && outcome_calls == 0);
  reset(&e->c, &e->s);
  e->c.companion.mode = 1;
  e->c.transaction = NULL;
  decision_kind = MSCONNECTOR_DECISION_KIND_DENY;
  outcome_result = -1;
  assert(haproxy_modsecurity_htx_process_companion_response_headers(
             &e->s, &e->f, &e->res) == -1);
  assert(e->s.replies == 1 && e->txn.status == 403 && e->s.kills == 1 &&
         outcome_calls == 1);
  assert(cancel_calls == 1 && release_calls == 0);
  assert(e->c.lifecycle.fail_closed);
  for (int bad_cleanup = 0; bad_cleanup < 2; bad_cleanup++) {
    check_precommit_cleanup_failure(e, bad_cleanup);
  }
}
static void check_eos(struct fixture_environment *e) {
  /* Successful EOS containing a technical error is still terminal,
   * independently of Off/Safe rule downgrade. No fabricated observation. */
  reset(&e->c, &e->s);
  e->c.companion.mode = 1;
  e->c.transaction = NULL;
  decision_kind = MSCONNECTOR_DECISION_KIND_ERROR;
  haproxy_modsecurity_htx_filter_http_end(&e->s, &e->f, &e->res);
  assert(e->s.kills == 1 && e->s.replies == 0 && outcome_calls == 0);
  reset(&e->c, &e->s);
  e->c.companion.mode = 1;
  e->c.transaction = NULL;
  close_result = -1;
  haproxy_modsecurity_htx_filter_http_end(&e->s, &e->f, &e->res);
  assert(e->s.kills == 1 && e->s.replies == 0);
  /* Legitimate allow completes, with no host kill or synthetic reply. */
  reset(&e->c, &e->s);
  e->c.companion.mode = 1;
  e->c.transaction = NULL;
  haproxy_modsecurity_htx_filter_http_end(&e->s, &e->f, &e->res);
  assert(e->s.kills == 0 && e->s.replies == 0 && eos_calls == 1 &&
         release_calls == 1);
}
static void check_strict_queued_response(struct fixture_environment *e) {
  const size_t queued[] = {0, 33, 65537};
  for (int companion = 0; companion < 2; companion++) {
    for (size_t n = 0; n < sizeof(queued) / sizeof(queued[0]); n++) {
      for (int committed = 0; committed < 2; committed++) {
        for (int strict = 0; strict < 2; strict++) {
          reset(&e->c, &e->s);
          e->config.common_config.phase4_mode = strict ? MSCONNECTOR_PHASE4_MODE_STRICT : MSCONNECTOR_PHASE4_MODE_SAFE;
          e->c.companion.mode = companion;
          if (companion) e->c.transaction = NULL;
          e->c.response.headers_committed = 1;
          e->s.res.output = queued[n];
          e->s.delivered_bytes = committed ? 177 : 0;
          native_result = 0;
          native_disruptive = 1;
          decision_kind = MSCONNECTOR_DECISION_KIND_DENY;
          int result = haproxy_modsecurity_htx_filter_http_end(&e->s, &e->f, &e->res);
          assert(e->s.delivered_bytes == (committed ? 177U : 0U));
          if (strict) {
            /* Positive http_end lets HAProxy advance/forward queued output. */
            assert(result == -1);
            assert(e->s.res.output == 0 && e->s.stream_aborts == 1);
            assert(e->s.frontend.aborts == 1 && e->s.frontend.shutdowns == 1);
            assert(e->s.frontend.flags & SC_FL_NOLINGER);
            assert(outcome_calls == 0); /* shutdown is not invented wire observation */
            int terminal_calls = abort_calls + release_calls;
            assert(haproxy_modsecurity_htx_filter_http_end(&e->s, &e->f, &e->res) == -1);
            assert(abort_calls + release_calls == terminal_calls);
          } else {
            assert(result == 1 && e->s.res.output == queued[n]);
            assert(e->s.stream_aborts == 0);
            assert(e->s.frontend.aborts == 0 && e->s.frontend.shutdowns == 0);
          }
          assert(e->neighbour.kills == 0 && e->neighbour.replies == 0);
        }
      }
    }
  }
}
static void check_request_version(void) {
  char version[4];
  const char *valid[] = {"HTTP/1.0", "HTTP/1.1", "HTTP/2.0"};
  const char *invalid[] = {"", "HTTP/2", "HTTP/3.0", "HTTP/1.9", "http/1.1", "HTTP/1.1x"};
  for (size_t i = 0; i < sizeof(valid) / sizeof(valid[0]); ++i) {
    assert(haproxy_modsecurity_htx_request_version((struct ist){(char *)valid[i], strlen(valid[i])}, version) == 0);
    assert(strcmp(version, valid[i] + 5) == 0);
  }
  for (size_t i = 0; i < sizeof(invalid) / sizeof(invalid[0]); ++i) {
    assert(haproxy_modsecurity_htx_request_version((struct ist){(char *)invalid[i], strlen(invalid[i])}, version) == -1);
    assert(version[0] == 0);
  }
  assert(haproxy_modsecurity_htx_request_version((struct ist){NULL, 8}, version) == -1);
}

int main(void) {
  check_request_version();
  struct fixture_environment e;
  const int modes[] = {MSCONNECTOR_PHASE4_MODE_OFF,
                       MSCONNECTOR_PHASE4_MODE_SAFE,
                       MSCONNECTOR_PHASE4_MODE_STRICT};
  const int invalid[] = {0, -1, 2};
  initialize_environment(&e);
  check_forwardable();
  for (size_t mode = 0; mode < 3; mode++) {
    e.config.common_config.phase4_mode = modes[mode];
    for (int companion = 0; companion < 2; companion++) {
      for (int commitment = 0; commitment < 3; commitment++)
        check_terminal(&e, companion, commitment);
    }
    check_direct(&e);
    for (size_t bad = 0; bad < 3; bad++)
      check_invalid(&e, invalid[bad]);
    check_precommit(&e);
    check_eos(&e);
  }
  check_strict_queued_response(&e);
  puts("HAProxy HTX direct/companion: Off/Safe/Strict config x pre/header/body "
       "x terminal reentry; native, commit, EOS, close, checked "
       "OPEN/CLAIM/RELEASE and nested success");
  return 0;
}
