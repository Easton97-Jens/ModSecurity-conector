/* Independent real APR merge and libModSecurity rule evaluation. No httpd or
 * Common lifecycle is inferred from this bounded native primitive test. */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <dlfcn.h>
#include <apr_general.h>
#include <apr_tables.h>
#include <apr_version.h>
#include <modsecurity/modsecurity.h>
#include <modsecurity/rules_set.h>
#include <modsecurity/transaction.h>

int main(int argc, char **argv) {
    apr_pool_t *pool = NULL;
    ModSecurity *engine = NULL;
    RulesSet *rules = NULL;
    Transaction *transaction = NULL;
    ModSecurityIntervention intervention = {0};
    const char *diagnostic = NULL;
    int result = 1;
    if (argc < 3 || (argc - 3) % 2 != 0) return 2;
    if (apr_initialize() != APR_SUCCESS) return 3;
    if (apr_pool_create(&pool, NULL) != APR_SUCCESS) goto cleanup;
    apr_table_t *headers = apr_table_make(pool, argc);
    for (int i = 3; i < argc; i += 2) apr_table_add(headers, argv[i], argv[i + 1]);
    if (strcmp(argv[1], "merge") == 0) {
        apr_table_compress(headers, APR_OVERLAP_TABLES_MERGE);
    } else if (strcmp(argv[1], "raw") != 0) {
        result = 2;
        goto cleanup;
    }
    engine = msc_init();
    rules = msc_create_rules_set();
    if (engine == NULL || rules == NULL) goto cleanup;
    const char *rule = strcmp(argv[2], "original") == 0 ?
        "SecRuleEngine On\n"
        "SecRule &REQUEST_HEADERS:X-No-Crs-Duplicate \"@eq 2\" "
        "\"id:1100504,phase:1,deny,status:451,log,t:none,chain\"\n"
        "SecRule REQUEST_HEADERS:X-No-Crs-Duplicate \"@streq one\" \"t:none,chain\"\n"
        "SecRule REQUEST_HEADERS:X-No-Crs-Duplicate \"@streq two\" \"t:none\"\n" :
        "SecRuleEngine On\n"
        "SecRule &REQUEST_HEADERS:X-No-Crs-Duplicate \"@eq 1\" "
        "\"id:1100504,phase:1,deny,status:451,log,t:none,chain\"\n"
        "SecRule REQUEST_HEADERS:X-No-Crs-Duplicate \"@streq one, two\" \"t:none\"\n";
    if (strcmp(argv[2], "original") != 0 && strcmp(argv[2], "corrected") != 0) {
        result = 2;
        goto cleanup;
    }
    if (msc_rules_add(rules, rule, &diagnostic) < 0) {
        fprintf(stderr, "%s\n", diagnostic != NULL ? diagnostic : "rule load failed");
        goto cleanup;
    }
    transaction = msc_new_transaction(engine, rules, NULL);
    if (transaction == NULL ||
        msc_process_connection(transaction, "127.0.0.1", 1111, "127.0.0.1", 2222) != 1 ||
        msc_process_uri(transaction, "/header-semantics", "GET", "1.1") != 1) goto cleanup;
    const apr_array_header_t *array = apr_table_elts(headers);
    const apr_table_entry_t *entries = (const apr_table_entry_t *)array->elts;
    for (int i = 0; i < array->nelts; ++i) {
        if (msc_add_request_header(transaction, (const unsigned char *)entries[i].key,
                (const unsigned char *)entries[i].val) != 1) goto cleanup;
    }
    if (msc_process_request_headers(transaction) != 1) goto cleanup;
    intervention.status = 200;
    int native_result = msc_intervention(transaction, &intervention);
    if (native_result != 0 && native_result != 1) goto cleanup;
    printf("apr=%s\nsdk=%s\ncount=%d\n", apr_version_string(), msc_who_am_i(engine), array->nelts);
    Dl_info sdk_image = {0}, apr_image = {0};
    if (!dladdr((const void *)msc_init, &sdk_image) ||
        !dladdr((const void *)apr_table_compress, &apr_image)) goto cleanup;
    printf("sdk_image=%s\napr_image=%s\n", sdk_image.dli_fname, apr_image.dli_fname);
    for (int i = 0; i < array->nelts; ++i) {
        printf("header=%s\t%s\n", entries[i].key, entries[i].val);
    }
    printf("matched=%d\nstatus=%d\n", intervention.disruptive != 0, intervention.status);
    result = 0;
cleanup:
    /* The public C ABI transfers these allocated strings to the caller.
     * Free directly so this probe also supports SDKs without the later helper. */
    free(intervention.url);
    free(intervention.log);
    if (transaction != NULL) msc_transaction_cleanup(transaction);
    if (rules != NULL) msc_rules_cleanup(rules);
    if (engine != NULL) msc_cleanup(engine);
    if (pool != NULL) apr_pool_destroy(pool);
    apr_terminate();
    return result;
}
