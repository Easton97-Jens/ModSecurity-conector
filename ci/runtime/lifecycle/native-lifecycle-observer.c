/* Test-only GNU ld --wrap observer. Never link into release artifacts.
 * A supervisor must retain and validate admission, paired calls and final
 * receipts for every participating PID. Absence is unknown, never zero.
 * invalid=false is measurement health, not lifecycle qualification: nonzero
 * final live_mappings means cleanup remains incomplete/unqualified.
 * Native MIME selection and host EOS are deliberately not inferred here. */
#define _GNU_SOURCE
#include "msconnector/transaction_contract.h"
#include <modsecurity/transaction.h>
#include <errno.h>
#include <fcntl.h>
#include <inttypes.h>
#include <pthread.h>
#include <stdatomic.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/mman.h>
#include <sys/stat.h>
#include <time.h>
#include <unistd.h>

#define MAP_CAPACITY 256U
#define BYTE_BUDGET (16U * 1024U * 1024U)
struct mapping {
    const void *key;
    int native;
    char id[MSCONNECTOR_MAX_TRANSACTION_ID_LENGTH];
    char canonical[64];
    char input_id[MSCONNECTOR_MAX_TRANSACTION_ID_LENGTH];
    const char *id_origin;
};
/* Undefined weak symbol keeps generic/fake-native builds fully opaque. */
extern int msconnector_lifecycle_sdk_transaction_id(void *, const void *, char *, size_t)
    __attribute__((weak));
struct budget { atomic_uint bytes; atomic_int invalid; };
struct observed_subject {
    const void *key;
    int native;
    int phase;
    int input_known;
    size_t input_size;
    int data_present;
};
static struct mapping mappings[MAP_CAPACITY];
static struct budget *budget;
static pthread_mutex_t lock = PTHREAD_MUTEX_INITIALIZER;
static int output_fd = -1;
static uint64_t sequence;
static unsigned int pending;
static dev_t admitted_device;
static ino_t admitted_inode;
static char run[400] = "null";
static char profile[400] = "null";
static char fixture[800] = "null";

static struct observed_subject subject(const void *key, int native, int phase) {
    const struct observed_subject value = {key, native, phase, 0, 0U, 0};
    return value;
}

static void invalid(void) {
    if (budget != NULL) atomic_store(&budget->invalid, 1);
}

/* Bounded JSON strings; control characters, quotes and slashes are escaped.
 * IDs and trusted fixture metadata are the only strings written. */
static int quoted(char *out, size_t capacity, const char *value, size_t limit) {
    size_t used = 0U;
    if (value == NULL) { (void)snprintf(out, capacity, "null"); return 0; }
    size_t length = strnlen(value, limit + 1U);
    if (length > limit || capacity < 3U) return -1;
    out[used++] = '"';
    for (size_t i = 0U; i < length; ++i) {
        unsigned char c = (unsigned char)value[i];
        if (c < 32U || c >= 127U || c == '"' || c == '\\') {
            if (capacity - used < 7U) return -1;
            (void)snprintf(out + used, capacity - used, "\\u%04x", (unsigned int)c);
            used += 6U;
        } else {
            if (capacity - used < 2U) return -1;
            out[used++] = (char)c;
        }
    }
    if (capacity - used < 2U) return -1;
    out[used++] = '"'; out[used] = '\0';
    return 0;
}

static struct mapping *lookup(const void *key, int native) {
    if (key == NULL) return NULL;
    for (size_t i = 0U; i < MAP_CAPACITY; ++i)
        if (mappings[i].key == key && mappings[i].native == native) return &mappings[i];
    return NULL;
}

static void remember(const void *key, int native, const char *id, const char *canonical) {
    if (key == NULL) return;
    if (lookup(key, native) != NULL) { invalid(); return; }
    for (size_t i = 0U; i < MAP_CAPACITY; ++i) {
        if (mappings[i].key != NULL) continue;
        mappings[i].key = key; mappings[i].native = native;
        mappings[i].id_origin = "common_public_contract";
        if (native) {
            mappings[i].id_origin = "unknown";
            if (id != NULL) mappings[i].id_origin = "caller_argument";
        }
        if (id != NULL && strnlen(id, sizeof(mappings[i].id)) < sizeof(mappings[i].id))
            (void)snprintf(mappings[i].id, sizeof(mappings[i].id), "%s", id);
        if (canonical != NULL && strnlen(canonical, sizeof(mappings[i].canonical)) < sizeof(mappings[i].canonical))
            (void)snprintf(mappings[i].canonical, sizeof(mappings[i].canonical), "%s", canonical);
        return;
    }
    invalid();
}

static void forget(const void *key, int native) {
    struct mapping *entry = lookup(key, native);
    if (entry != NULL) memset(entry, 0, sizeof(*entry));
}

struct serialized_identity {
    char id[6U * MSCONNECTOR_MAX_TRANSACTION_ID_LENGTH + 3U];
    char canonical[400];
    char input_id[6U * MSCONNECTOR_MAX_TRANSACTION_ID_LENGTH + 3U];
};

static void serialize_identity(const struct mapping *entry, struct serialized_identity *identity) {
    if (entry == NULL) return;
    if (entry->id[0] != '\0' &&
        quoted(identity->id, sizeof(identity->id), entry->id, sizeof(entry->id) - 1U) != 0) invalid();
    if (entry->canonical[0] != '\0' &&
        quoted(identity->canonical, sizeof(identity->canonical), entry->canonical, 63U) != 0) invalid();
    if (entry->input_id[0] != '\0' &&
        quoted(identity->input_id, sizeof(identity->input_id), entry->input_id, sizeof(entry->input_id) - 1U) != 0) invalid();
}

static int admitted_descriptor_still_valid(void) {
    struct stat descriptor_status;
    int descriptor_flags = fcntl(output_fd, F_GETFL);
    if (fstat(output_fd, &descriptor_status) != 0 ||
        descriptor_status.st_dev != admitted_device || descriptor_status.st_ino != admitted_inode ||
        descriptor_flags < 0 || (descriptor_flags & O_APPEND) == 0) {
        invalid();
        return 0;
    }
    return 1;
}

/* Caller holds process-local lock. One bounded O_APPEND write per record;
 * a partial/error write permanently invalidates the entire inherited run. */
static void event(const char *function, const char *edge, uint64_t call,
                  const struct observed_subject *observed, const char *result,
                  const char *argument_committed) {
    if (output_fd < 0 || budget == NULL) return;
    if (!admitted_descriptor_still_valid()) return;
    struct serialized_identity identity = {"null", "null", "null"};
    char record[8192];
    const struct mapping *entry = lookup(observed->key, observed->native);
    serialize_identity(entry, &identity);
    char state[512] = "null";
    /* Only an already admitted, successfully initialized Common object is
     * inspected. Native opaque handles and init's uninitialized entry are
     * never dereferenced. Each edge reports its own observed public state. */
    if (entry != NULL && observed->native == 0) {
        const msconnector_transaction_contract *contract = observed->key;
        (void)snprintf(state, sizeof(state),
            "{\"status\":%d,\"response_committed\":%d,\"active_phase\":%d,"
            "\"last_completed_phase\":%d,\"completed_phase_mask\":%u,"
            "\"cleanup_started\":%d,\"cleanup_complete\":%d,"
            "\"completed_at_ms\":%" PRIu64 ",\"cleanup_at_ms\":%" PRIu64 "}",
            (int)contract->status, contract->response_committed, contract->active_phase,
            contract->last_completed_phase, contract->completed_phase_mask,
            contract->cleanup_started, contract->cleanup_complete,
            contract->completed_at_ms, contract->cleanup_at_ms);
    }
    struct timespec now;
    uint64_t ns = 0U;
    if (clock_gettime(CLOCK_MONOTONIC, &now) == 0)
        ns = (uint64_t)now.tv_sec * UINT64_C(1000000000) + (uint64_t)now.tv_nsec;
    else invalid();
    unsigned int live = 0U;
    for (size_t i = 0U; i < MAP_CAPACITY; ++i) if (mappings[i].key != NULL) ++live;
    char input_size[32] = "null";
    const char *input_kind = "null";
    if (observed->input_known) {
        (void)snprintf(input_size, sizeof(input_size), "%zu", observed->input_size);
        input_kind = observed->data_present ? "\"non_null_buffer\"" : "\"null_buffer\"";
    }
    int length = snprintf(record, sizeof(record),
        "{\"schema\":\"native-lifecycle-v1\",\"pid\":%ld,\"uid\":%ld,\"gid\":%ld,"
        "\"sequence\":%" PRIu64 ",\"monotonic_ns\":%" PRIu64 ",\"call\":%" PRIu64 ","
        "\"run\":%s,\"profile\":%s,\"case\":%s,\"function\":\"%s\",\"edge\":\"%s\","
        "\"transaction_id\":%s,\"canonical_transaction_id\":%s,\"phase\":%d,\"result\":%s,\"invalid\":%s,"
        "\"transaction_id_origin\":\"%s\",\"input_transaction_id\":%s,"
        "\"argument_committed\":%s,\"contract_state\":%s,"
        "\"input_size\":%s,\"input_kind\":%s,\"argument_eos\":null,"
        "\"pending_calls\":%u,\"live_mappings\":%u,\"native_mime_selection\":null,\"host_eos\":null}\n",
        (long)getpid(), (long)geteuid(), (long)getegid(), ++sequence, ns, call,
        run, profile, fixture, function, edge, identity.id, identity.canonical, observed->phase, result,
        atomic_load(&budget->invalid) ? "true" : "false",
        entry == NULL ? "unknown" : entry->id_origin, identity.input_id,
        argument_committed == NULL ? "null" : argument_committed, state,
        input_size, input_kind, pending, live);
    if (length <= 0 || (size_t)length >= sizeof(record)) { invalid(); return; }
    unsigned int previous = atomic_load(&budget->bytes);
    do {
        if (previous > BYTE_BUDGET || (unsigned int)length > BYTE_BUDGET - previous) { invalid(); return; }
    } while (!atomic_compare_exchange_weak(&budget->bytes, &previous, previous + (unsigned int)length));
    if (write(output_fd, record, (size_t)length) != (ssize_t)length) invalid();
}

static uint64_t enter_subject(const char *name, const struct observed_subject *observed, const char *argument) {
    int saved = errno;
    (void)pthread_mutex_lock(&lock);
    uint64_t call = sequence + 1U;
    ++pending;
    event(name, "enter", call, observed, "null", argument);
    (void)pthread_mutex_unlock(&lock);
    errno = saved;
    return call;
}

static uint64_t enter_argument(const char *name, const void *key, int native, int phase, const char *argument) {
    const struct observed_subject observed = subject(key, native, phase);
    return enter_subject(name, &observed, argument);
}

static uint64_t enter(const char *name, const void *key, int native, int phase) {
    return enter_argument(name, key, native, phase, NULL);
}

static void returned_subject(const char *name, uint64_t call, const struct observed_subject *observed,
                     int result, int remove, const char *argument) {
    int saved = errno;
    char number[32];
    if (strcmp(name, "native_cleanup") == 0) (void)snprintf(number, sizeof(number), "null");
    else (void)snprintf(number, sizeof(number), "%d", result);
    (void)pthread_mutex_lock(&lock);
    event(name, "return", call, observed, number, argument);
    if (pending == 0U) invalid(); else --pending;
    if (remove) forget(observed->key, observed->native);
    (void)pthread_mutex_unlock(&lock);
    errno = saved;
}

static void returned(const char *name, uint64_t call, const void *key, int native,
                     int phase, int result, int remove) {
    const struct observed_subject observed = subject(key, native, phase);
    returned_subject(name, call, &observed, result, remove, NULL);
}

static void before_fork(void) { (void)pthread_mutex_lock(&lock); }
static void after_fork(void) { (void)pthread_mutex_unlock(&lock); }
static void child_fork(void) {
    /* In-flight calls in other parent threads cannot be completed in child.
     * Their absence is explicit rather than treated as child-owned calls. */
    if (pending != 0U) invalid();
    sequence = 0U; pending = 0U;
    const struct observed_subject observed = subject(NULL, 0, 0);
    event("observer", "fork", 0U, &observed, "null", NULL);
    (void)pthread_mutex_unlock(&lock);
}

__attribute__((constructor)) static void admission(void) {
    int saved = errno;
    const char *value = getenv("MSCONNECTOR_LIFECYCLE_FD");
    char *end = NULL;
    if (value == NULL || *value == '\0') { errno = saved; return; }
    errno = 0;
    long candidate = strtol(value, &end, 10);
    struct stat status;
    if (errno != 0 || end == value || *end != '\0' || candidate < 3L || candidate > 1048576L ||
        fstat((int)candidate, &status) != 0 || !S_ISREG(status.st_mode) ||
        (status.st_mode & 07777U) != 0600U || status.st_nlink != 1U ||
        status.st_uid != geteuid()) goto rejected;
    int flags = fcntl((int)candidate, F_GETFL);
    if (flags < 0 || (flags & O_APPEND) == 0 || (flags & O_ACCMODE) == O_RDONLY) goto rejected;
    budget = mmap(NULL, sizeof(*budget), PROT_READ | PROT_WRITE,
                  MAP_SHARED | MAP_ANONYMOUS, -1, 0);
    if (budget == MAP_FAILED) { budget = NULL; goto rejected; }
    atomic_init(&budget->bytes, 0U); atomic_init(&budget->invalid, 0);
    if (!atomic_is_lock_free(&budget->bytes) || !atomic_is_lock_free(&budget->invalid)) goto rejected;
    output_fd = (int)candidate;
    admitted_device = status.st_dev; admitted_inode = status.st_ino;
    if (quoted(run, sizeof(run), getenv("MSCONNECTOR_LIFECYCLE_RUN"), 64U) != 0 ||
        quoted(profile, sizeof(profile), getenv("MSCONNECTOR_LIFECYCLE_PROFILE"), 64U) != 0 ||
        quoted(fixture, sizeof(fixture), getenv("MSCONNECTOR_LIFECYCLE_CASE"), 128U) != 0) invalid();
    if (pthread_atfork(before_fork, after_fork, child_fork) != 0) invalid();
    const struct observed_subject observed = subject(NULL, 0, 0);
    event("observer", "admitted", 0U, &observed, "null", NULL);
    errno = saved;
    return;
rejected:
    output_fd = -1;
    static const char rejected_message[] = "native-lifecycle-observer: admission rejected\n";
    (void)write(STDERR_FILENO, rejected_message, sizeof(rejected_message) - 1U);
    errno = saved;
}

__attribute__((destructor)) static void final_receipt(void) {
    int saved = errno;
    (void)pthread_mutex_lock(&lock);
    if (pending != 0U) invalid();
    const struct observed_subject observed = subject(NULL, 0, 0);
    event("observer", "final", 0U, &observed, "null", NULL);
    if (budget != NULL && atomic_load(&budget->invalid)) {
        static const char invalid_message[] = "native-lifecycle-observer: evidence invalid\n";
        (void)write(STDERR_FILENO, invalid_message, sizeof(invalid_message) - 1U);
    }
    (void)pthread_mutex_unlock(&lock);
    errno = saved;
}

extern int __real_msconnector_transaction_contract_init(msconnector_transaction_contract *, const msconnector_transaction_profile *, const char *, const char *, const char *, msconnector_transaction_mode, uint64_t);
int __wrap_msconnector_transaction_contract_init(msconnector_transaction_contract *c, const msconnector_transaction_profile *p, const char *id, const char *connector, const char *host, msconnector_transaction_mode mode, uint64_t now) {
    uint64_t call = enter("common_init", NULL, 0, 0);
    int result = __real_msconnector_transaction_contract_init(c, p, id, connector, host, mode, now);
    int saved = errno;
    (void)pthread_mutex_lock(&lock);
    if (result == 0 && c != NULL) remember(c, 0, c->transaction_id, c->canonical_transaction_id);
    (void)pthread_mutex_unlock(&lock);
    errno = saved;
    returned("common_init", call, c, 0, 0, result, 0);
    return result;
}

#define COMMON_TIME_WRAPPER(suffix, label, remove) \
extern int __real_msconnector_transaction_contract_##suffix(msconnector_transaction_contract *, uint64_t); \
int __wrap_msconnector_transaction_contract_##suffix(msconnector_transaction_contract *c, uint64_t now) { \
    uint64_t call = enter(label, c, 0, 0); \
    int result = __real_msconnector_transaction_contract_##suffix(c, now); \
    returned(label, call, c, 0, 0, result, remove); return result; \
}
COMMON_TIME_WRAPPER(finish, "common_finish", 0)
COMMON_TIME_WRAPPER(cleanup, "common_cleanup", 1)

extern int __real_msconnector_transaction_contract_complete_phase(msconnector_transaction_contract *, enum msconnector_phase, uint64_t);
int __wrap_msconnector_transaction_contract_complete_phase(msconnector_transaction_contract *c, enum msconnector_phase phase, uint64_t now) {
    uint64_t call = enter("common_complete_phase", c, 0, (int)phase);
    int result = __real_msconnector_transaction_contract_complete_phase(c, phase, now);
    returned("common_complete_phase", call, c, 0, (int)phase, result, 0); return result;
}
extern int __real_msconnector_transaction_contract_set_response_committed(msconnector_transaction_contract *, int);
int __wrap_msconnector_transaction_contract_set_response_committed(msconnector_transaction_contract *c, int committed) {
    int saved = errno;
    char argument[32];
    (void)snprintf(argument, sizeof(argument), "%d", committed);
    errno = saved;
    uint64_t call = enter_argument("common_set_response_committed", c, 0, 0, argument);
    int result = __real_msconnector_transaction_contract_set_response_committed(c, committed);
    const struct observed_subject observed = subject(c, 0, 0);
    returned_subject("common_set_response_committed", call, &observed, result, 0, argument); return result;
}
extern int __real_msconnector_transaction_contract_record_response_metadata(msconnector_transaction_contract *, int, const char *, size_t, size_t);
int __wrap_msconnector_transaction_contract_record_response_metadata(msconnector_transaction_contract *c, int status, const char *type, size_t count, size_t bytes) {
    uint64_t call = enter("common_record_response_metadata", c, 0, 0);
    int result = __real_msconnector_transaction_contract_record_response_metadata(c, status, type, count, bytes);
    returned("common_record_response_metadata", call, c, 0, 0, result, 0); return result;
}

extern Transaction *__real_msc_new_transaction(ModSecurity *, RulesSet *, void *);
extern Transaction *__real_msc_new_transaction_with_id(ModSecurity *, RulesSet *, const char *, void *);
static Transaction *constructed(Transaction *transaction, const char *id, uint64_t call, const char *name, ModSecurity *engine) {
    int saved = errno;
    char actual_id[MSCONNECTOR_MAX_TRANSACTION_ID_LENGTH];
    int extracted = 0;
    if (transaction != NULL && &msconnector_lifecycle_sdk_transaction_id != NULL)
        extracted = msconnector_lifecycle_sdk_transaction_id(engine, transaction, actual_id, sizeof(actual_id));
    (void)pthread_mutex_lock(&lock);
    if (extracted < 0) invalid();
    const char *observed_id = id;
    if (extracted == 1) observed_id = actual_id;
    else if (extracted < 0) observed_id = NULL;
    remember(transaction, 1, observed_id, NULL);
    struct mapping *entry = lookup(transaction, 1);
    if (entry != NULL) {
        if (extracted == 1) entry->id_origin = "sdk_public_m_id";
        if (id != NULL && strnlen(id, sizeof(entry->input_id)) < sizeof(entry->input_id))
            (void)snprintf(entry->input_id, sizeof(entry->input_id), "%s", id);
        else if (id != NULL) invalid();
    }
    (void)pthread_mutex_unlock(&lock);
    errno = saved;
    returned(name, call, transaction, 1, 0, transaction != NULL, 0);
    return transaction;
}
Transaction *__wrap_msc_new_transaction(ModSecurity *m, RulesSet *r, void *data) {
    uint64_t call = enter("native_new", NULL, 1, 0);
    Transaction *transaction = __real_msc_new_transaction(m, r, data);
    return constructed(transaction, NULL, call, "native_new", m);
}
Transaction *__wrap_msc_new_transaction_with_id(ModSecurity *m, RulesSet *r, const char *id, void *data) {
    uint64_t call = enter("native_new_with_id", NULL, 1, 0);
    Transaction *transaction = __real_msc_new_transaction_with_id(m, r, id, data);
    return constructed(transaction, id, call, "native_new_with_id", m);
}
#define NATIVE_WRAPPER(suffix, phase) \
extern int __real_msc_##suffix(Transaction *); \
int __wrap_msc_##suffix(Transaction *transaction) { \
    uint64_t call = enter("native_" #suffix, transaction, 1, phase); \
    int result = __real_msc_##suffix(transaction); \
    returned("native_" #suffix, call, transaction, 1, phase, result, 0); return result; \
}
NATIVE_WRAPPER(process_request_body, 2)
NATIVE_WRAPPER(process_response_body, 4)
NATIVE_WRAPPER(process_logging, 0)

/* Native append APIs have a byte count, but no EOS argument. In particular
 * null/zero input is an actual append call, never evidence of host EOS. */
#define NATIVE_APPEND_WRAPPER(direction, phase_value) \
extern int __real_msc_append_##direction##_body(Transaction *, const unsigned char *, size_t); \
int __wrap_msc_append_##direction##_body(Transaction *transaction, const unsigned char *data, size_t size) { \
    struct observed_subject observed = subject(transaction, 1, phase_value); \
    observed.input_known = 1; observed.input_size = size; observed.data_present = data != NULL; \
    uint64_t call = enter_subject("native_append_" #direction "_body", &observed, NULL); \
    int result = __real_msc_append_##direction##_body(transaction, data, size); \
    returned_subject("native_append_" #direction "_body", call, &observed, result, 0, NULL); \
    return result; \
}
NATIVE_APPEND_WRAPPER(request, 2)
NATIVE_APPEND_WRAPPER(response, 4)
extern void __real_msc_transaction_cleanup(Transaction *);
void __wrap_msc_transaction_cleanup(Transaction *transaction) {
    uint64_t call = enter("native_cleanup", transaction, 1, 0);
    __real_msc_transaction_cleanup(transaction);
    returned("native_cleanup", call, transaction, 1, 0, 0, 1);
}
