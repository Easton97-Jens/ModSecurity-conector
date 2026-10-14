#define _GNU_SOURCE
#include <dlfcn.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <modsecurity/modsecurity.h>
#include <modsecurity/rules_set.h>
#include <modsecurity/transaction.h>

int main(int argc, char **argv) {
    if (argc != 2 || (strcmp(argv[1], "empty") != 0 &&
        strcmp(argv[1], "single") != 0 && strcmp(argv[1], "absent_length") != 0 && strcmp(argv[1], "single_zero_length") != 0)) return 2;
    ModSecurity *engine = msc_init();
    RulesSet *rules = msc_create_rules_set();
    Transaction *transaction = NULL;
    ModSecurityIntervention intervention = {0};
    const char *error = NULL;
    int result = 1;
    const char *rule =
        "SecRuleEngine On\nSecRequestBodyAccess On\n"
        "SecRule REQUEST_METHOD \"@streq POST\" \"id:91042002,phase:2,deny,status:451,log,t:none,chain\"\n"
        "SecRule REQUEST_HEADERS:Content-Length \"@streq 0\" \"t:none,chain\"\n"
        "SecRule REQUEST_BODY \"@rx ^$\" \"t:none\"\n";
    if (engine == NULL || rules == NULL || msc_rules_add(rules, rule, &error) < 0) {
        fprintf(stderr, "%s\n", error != NULL ? error : "native initialization failed");
        goto done;
    }
    transaction = msc_new_transaction(engine, rules, NULL);
    if (transaction == NULL || msc_process_connection(transaction,"127.0.0.1",1111,"127.0.0.1",2222) != 1 ||
        msc_process_uri(transaction,"/i12/lighttpd/empty","POST","1.1") != 1 ||
        msc_add_request_header(transaction,(const unsigned char *)"Content-Type",(const unsigned char *)"text/plain") != 1) goto done;
    if (strcmp(argv[1],"absent_length") != 0 &&
        msc_add_request_header(transaction,(const unsigned char *)"Content-Length",
            (const unsigned char *)(strcmp(argv[1],"single")==0 ? "1" : "0")) != 1) goto done;
    int headers = msc_process_request_headers(transaction);
    int has_body = strcmp(argv[1],"single")==0 || strcmp(argv[1],"single_zero_length")==0;
    int appended = has_body ?
        msc_append_request_body(transaction,(const unsigned char *)"x",1U) : 0;
    int body = msc_process_request_body(transaction);
    intervention.status = 200;
    int intervened = msc_intervention(transaction,&intervention);
    Dl_info sdk = {0};
    if (headers != 1 || body != 1 || (has_body && appended != 1) ||
        (intervened != 0 && intervened != 1) || !dladdr((const void *)msc_init,&sdk)) goto done;
    printf("{\"mode\":\"%s\",\"native_headers_result\":%d,\"native_body_result\":%d,"
        "\"native_append_calls\":%d,\"native_append_result\":%d,\"native_intervention_result\":%d,"
        "\"disruptive\":%d,\"status\":%d,\"sdk_image\":\"%s\"}\n",
        argv[1],headers,body,has_body,appended,intervened,
        intervention.disruptive,intervention.status,sdk.dli_fname);
    result = 0;
done:
    msc_intervention_cleanup(&intervention);
    if (transaction != NULL) msc_transaction_cleanup(transaction);
    if (rules != NULL) msc_rules_cleanup(rules);
    if (engine != NULL) msc_cleanup(engine);
    return result;
}
