#define main haproxy_spop_program_main
#include "PRODUCT_RUNTIME"
#undef main
#include <assert.h>
extern const char *native_failure;
extern int native_failure_result;
extern unsigned int native_calls, native_cleanups;
int main(void) {
    const char *modes[] = {"detect-only","enforce"};
    const char *fail_modes[] = {"closed","open"};
    const char *failures[] = {"msc_process_connection","msc_process_request_headers", "msc_append_request_body","msc_process_request_body"};
    for(size_t mode=0;mode<2;mode++) for(size_t fail_mode=0;fail_mode<2;fail_mode++) {
        agent_state state;
        memset(&state,0,sizeof(state));
        copy_cstring(state.config.mode,sizeof(state.config.mode),modes[mode]);
        copy_cstring(state.config.fail_mode,sizeof(state.config.fail_mode),fail_modes[fail_mode]);
        state.config.request_body_limit=1024;
        haproxy_modsecurity_engine_config cfg;
        memset(&cfg,0,sizeof(cfg));
        msconnector_config_init(&cfg.common_config);
        msconnector_config_apply_defaults(&cfg.common_config);
        cfg.rules_file = "PRODUCT_RULES";
        haproxy_modsecurity_decision d;
        assert(haproxy_modsecurity_engine_create(&cfg,&state.engine,&d) == 0);
        for(size_t failure=0;failure<4;failure++) {
            notify_request request;
            memset(&request,0,sizeof(request));
            copy_cstring(request.client_ip,sizeof(request.client_ip),"192.0.2.1");
            copy_cstring(request.server_ip,sizeof(request.server_ip),"198.51.100.1");
            copy_cstring(request.method,sizeof(request.method),"POST");
            copy_cstring(request.uri,sizeof(request.uri),"/");
            copy_cstring(request.request_id,sizeof(request.request_id),"i10-spop-request");
            request.client_port=1234;request.server_port=443;
            request.has_client_ip=request.has_server_ip=request.has_client_port=request.has_server_port=1;
            runtime_header headers[]={{"Host","example.test"}};
            request.headers=headers;request.header_count=1;
            request.body=(unsigned char *)"x";request.body_len=1;
            int processed=0;
            spop_ack_decision_origin origin=SPOP_ACK_FAILURE_DECISION;
            const char *text="pass";
            char handle[HAPROXY_SPOP_RESPONSE_COMPANION_HANDLE_STORAGE]={0};
            native_failure=failures[failure];native_failure_result=failure==2 ? 2 : 0;
            unsigned int cleanup_before=native_cleanups;
            process_production_request_notify(&state,&request,&d,&processed,&origin,&text,handle);
            assert(d.disruptive && d.status == 503 && strcmp(d.action,"deny") == 0);
            assert(d.rule_id == 0 && d.redirect_url[0] == '\0' && d.log_message[0] != '\0');
            assert(origin == SPOP_ACK_FAILURE_DECISION && strcmp(text,"fail-closed") == 0);
            assert(native_cleanups == cleanup_before+1);
            spop_buffer payload={0};
            assert(build_decision_ack_payload(&payload,&d,safe_decision_reason_code(&d,processed,text),
                production_ack_enforces(&state.config,origin),NULL) == 0);
            assert(payload_has_set_var_blocked_true(&payload));
        }
        native_failure=NULL;
        /* Missing companion completion is a real rejected Common finish,
         * never a successful request-only terminal acknowledgement. */
        haproxy_modsecurity_request terminal_request={0};
        haproxy_modsecurity_header terminal_headers[]={ {"Host","example.test"} };
        terminal_request.method="GET";terminal_request.uri="/";
        terminal_request.client_ip="192.0.2.1";terminal_request.server_ip="198.51.100.1";
        terminal_request.client_port=1234;terminal_request.server_port=443;
        terminal_request.request_id="i10-missing-companion";
        terminal_request.headers=terminal_headers;terminal_request.header_count=1;
        haproxy_modsecurity_transaction *unfinished=NULL;
        assert(haproxy_modsecurity_transaction_begin(state.engine,&terminal_request,&d,&unfinished)==0);
        spop_ack_decision_origin terminal_origin=SPOP_ACK_ENGINE_DECISION;
        const char *terminal_text="pass"; notify_request unused_request={0};
        finish_or_store_request_transaction(&state,&unused_request,unfinished,&d,&terminal_origin,&terminal_text);
        assert(terminal_origin==SPOP_ACK_FAILURE_DECISION && d.disruptive && d.status==503);
        /* Real response-owner dispatcher uses the same productive binding;
         * failed P3/P4/commit/release never become successful decisions. */
        for (int operation=0;operation<6;operation++) {
            haproxy_modsecurity_request r={0};
            haproxy_modsecurity_header h[]={ {"Host","example.test"} };
            r.method="GET";r.uri="/";r.client_ip="192.0.2.1";r.server_ip="198.51.100.1";
            r.client_port=1234;r.server_port=443;r.request_id="i10-spop-companion";
            r.headers=h;r.header_count=1;
            haproxy_modsecurity_transaction *t=NULL;
            native_failure=NULL;
            assert(haproxy_modsecurity_transaction_begin(state.engine,&r,&d,&t)==0);
            assert(haproxy_modsecurity_transaction_handoff_response_companion(t)==0);
            assert(haproxy_modsecurity_transaction_claim_response_companion(t)==0);
            spop_bridge_task_context context={0};
            context.state=&state;context.transaction=t;
            context.command.decision_storage=&context.decision_storage;
            msconnector_response response={0};response.status=200;
            msconnector_header bridge_headers[]={{.name="Content-Type",.name_size=12,.value="text/plain",.value_size=10}};
            response.http_version="HTTP/1.1";
            context.command.response=&response;
            if(operation==0 || operation==5) {
                context.command.operation=HAPROXY_SPOP_RESPONSE_COMPANION_RESPONSE_HEADERS;
                response.headers=bridge_headers;response.header_count=1;
                native_failure=operation==5 ? "msc_add_response_header" : "msc_process_response_headers";
                native_failure_result=operation==5 ? -1 : 0;
                assert(prepare_spop_bridge_headers(&context,&context.command,&context.error)==0);
            } else {
                haproxy_modsecurity_response native_response={0};native_response.status=200;
                native_response.protocol="HTTP/1.1";
                assert(haproxy_modsecurity_transaction_process_response_headers(t,&native_response,&d)==0);
                if(operation==1) {
                    context.command.operation=HAPROXY_SPOP_RESPONSE_COMPANION_RESPONSE_BODY;
                    context.command.body=(const unsigned char *)"x";context.command.body_size=1;
                    native_failure="msc_append_response_body";native_failure_result=2;
                } else if(operation==2) {
                    context.command.operation=HAPROXY_SPOP_RESPONSE_COMPANION_RESPONSE_EOS;
                    native_failure="msc_process_response_body";native_failure_result=0;
                } else if(operation==3) {
                    context.command.operation=HAPROXY_SPOP_RESPONSE_COMPANION_COMMIT;
                    context.command.headers_sent=0;context.command.body_started=1;
                } else context.command.operation=HAPROXY_SPOP_RESPONSE_COMPANION_RELEASE;
            }
            run_spop_bridge_task(&context);
            assert(context.success==0 && context.error.code != MSCONNECTOR_ERROR_NONE);
            if(operation < 3) assert(context.error.code==MSCONNECTOR_ERROR_MODSECURITY_FAILURE);
            if(operation==5) assert(context.error.code==MSCONNECTOR_ERROR_HOST_API_FAILURE);
            if(operation==4) assert(context.transaction_consumed==1);
            else haproxy_modsecurity_transaction_abort(t);
        }
        native_failure=NULL;
        /* Engine rule observer mode still differs; failure origin always enforces. */
        assert(production_ack_enforces(&state.config,SPOP_ACK_FAILURE_DECISION));
        assert(production_ack_enforces(&state.config,SPOP_ACK_ENGINE_DECISION) == (mode != 0));
        haproxy_modsecurity_engine_destroy(state.engine);
    }
    puts("full SPOP request TU: P1/P2 native failure -> disruptive503 -> serialized blocked ACK; detect/enforce x open/closed; cleanup and stale fields");
    return 0;
}
