/* Attempt-local native boundary fixture, never installed in a product build.
 * Fail exactly one native transaction allocation in the worker selected by
 * the fixture invocation. No global memory exhaustion, fabricated event, or
 * foreign process mutation is involved.
 */
#define _GNU_SOURCE
#include <dlfcn.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>

typedef void *(*new_transaction_fn)(void *, void *, char *, void *);
static pid_t owned_master;
static char owned_transaction[33];
static int armed;

__attribute__((constructor)) static void bind_owned_master(void)
{
    if (getuid() == 0) {
        const char *mode = getenv("MSCONNECTOR_OWNED_BEGIN_FAULT");
        const char *id = getenv("MSCONNECTOR_OWNED_BEGIN_TXID");
        owned_master = getpid();
        if (mode != NULL && strcmp(mode, "one-native-allocation-failure") == 0 &&
            id != NULL && strlen(id) == 32U && strspn(id, "0123456789abcdef") == 32U) {
            memcpy(owned_transaction, id, 33U);
            armed = 1;
        }
    }
}

void *msc_new_transaction_with_id(void *engine, void *rules, char *id,
                                  void *opaque)
{
    static int failed;
    new_transaction_fn original;

    if (!failed && getuid() == 65534 && owned_master > 0 &&
        getppid() == owned_master && id != NULL && armed &&
        strcmp(id, owned_transaction) == 0) {
        failed = 1;
        return NULL;
    }
    /* POSIX specifies this dlsym function-pointer conversion. */
    *(void **)(&original) = dlsym(RTLD_NEXT, "msc_new_transaction_with_id");
    if (original == NULL) {
        _exit(126);
    }
    return original(engine, rules, id, opaque);
}
