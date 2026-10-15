#include <modsecurity/modsecurity.h>
#include <modsecurity/rules_set.h>
#include <modsecurity/transaction.h>
#include <stdio.h>
#include <string.h>
static int matches;
static void callback(void *context, const void *data) {
    (void)context;
    if (data != NULL && strstr((const char *)data, "[id \"91041002\"]") != NULL) matches++;
}
int main(int argc, char **argv) {
    if (argc != 4) return 2;
    ModSecurity *engine = msc_init();
    RulesSet *rules = msc_create_rules_set();
    const char *error = NULL;
    msc_set_log_cb(engine, callback);
    int loaded = msc_rules_add_file(rules, argv[1], &error);
    if (loaded < 0) { fprintf(stderr, "%s\n", error != NULL ? error : "rules failed"); return 3; }
    Transaction *tx = msc_new_transaction(engine, rules, NULL);
    if (tx == NULL) return 4;
    int connection = msc_process_connection(tx, "127.0.0.1", 17001, "127.0.0.1", 18140);
    int uri = msc_process_uri(tx, argv[3], argv[2], "1.1");
    int p1 = msc_process_request_headers(tx);
    printf("{\"loaded_rules\":%d,\"connection_result\":%d,\"uri_result\":%d,\"p1_result\":%d,\"genuine_sdk_marker_count\":%d}\n", loaded, connection, uri, p1, matches);
    msc_transaction_cleanup(tx);
    msc_rules_cleanup(rules);
    msc_cleanup(engine);
    return connection == 1 && uri == 1 && p1 == 1 ? 0 : 5;
}
