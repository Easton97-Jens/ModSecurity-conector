/* Actual APR bucket classification control; host scope APIs are explicit stubs.
 * This protects the callback collector, not hosted native/Common lifetime. */
#include "apache-host-observer.h"
#include <assert.h>
#include <errno.h>
#include <stdlib.h>
#include <string.h>

static int unknown_scope;
static int failed_retirement;
uint64_t msconnector_lifecycle_host_scope_call(const void *host) {
    return host != NULL && !unknown_scope ? UINT64_C(17) : UINT64_C(0);
}
int msconnector_lifecycle_host_retire(const void *host) {
    return host != NULL && !failed_retirement;
}
int main(int argc, char **argv) {
    apr_pool_t *pool=NULL;
    request_rec request;
    msc_t context;
    assert(argc==3);
    assert(setenv("MSCONNECTOR_APACHE_HOST_OBSERVER",argv[1],1)==0);
    assert(apr_initialize()==APR_SUCCESS);
    assert(apr_pool_create(&pool,NULL)==APR_SUCCESS);
    apr_bucket_alloc_t *allocator=apr_bucket_alloc_create(pool);
    assert(allocator!=NULL);
    memset(&request,0,sizeof(request));
    memset(&context,0,sizeof(context));
    context.owner_request=&request;
    unknown_scope=strcmp(argv[2],"unknown_scope")==0;
    failed_retirement=strcmp(argv[2],"failed_retirement")==0;
    apr_bucket *eos=apr_bucket_eos_create(allocator);
    apr_bucket *data=apr_bucket_heap_create("safe",4,NULL,allocator);
    assert(eos!=NULL && data!=NULL);
    errno=EDOM;
    apache_lifecycle_observe("actual_request_apr_eos",&context,&request,eos);
    assert(errno==EDOM);
    apache_lifecycle_observe("data_bucket_negative",&context,&request,data);
    assert(errno==EDOM);
    if (strcmp(argv[2],"duplicate_eos")==0) {
        apache_lifecycle_observe("actual_request_apr_eos",&context,&request,eos);
        assert(errno==EDOM);
    }
    context.contract.cleanup_complete=1;
    apache_lifecycle_retire(&context,&request);
    assert(errno==EDOM);
    apr_bucket_destroy(data);apr_bucket_destroy(eos);
    apr_pool_destroy(pool);apr_terminate();
    return 0;
}
