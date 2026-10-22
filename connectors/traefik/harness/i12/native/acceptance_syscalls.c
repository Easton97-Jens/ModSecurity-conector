#define _GNU_SOURCE
/* Test-only own-child observer. Never attach to a supplied PID, change a
 * register/syscall/result, read payload buffers, or link into product code. */
#include <sys/ptrace.h>
#include <linux/ptrace.h>
#include <linux/audit.h>
#include <sys/syscall.h>
#include <sys/socket.h>
#include <sys/stat.h>
#include <sys/wait.h>
#include <sys/prctl.h>
#include <sys/uio.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <dirent.h>
#include <errno.h>
#include <fcntl.h>
#include <limits.h>
#include <signal.h>
#include <stdint.h>
#include <stddef.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include <unistd.h>
#include <pthread.h>

#define MAX_THREADS 128
#define MAX_SOCKETS 128
#define MAX_RECORDS 4096
#define MAX_OUTPUT (2U * 1024U * 1024U)
#define TEST_BYTES (1024U * 1024U)
#define HOST_BINARY "/task/cache/traefik"
#define HOST_CONFIG "/task/runtime/effective-config/traefik-native-static.yaml"
#define AUTH_CASE_SHORT "ac-ef73876b3c669e899482-syscall"
#define AUTH_CASE_BLOCK "ac-9528a3f086fca6429a67-syscall"
#define OBSERVER_MODULE "github.com/Easton97-Jens/ModSecurity-conector/connectors/traefik/response_observer"

struct endpoint { unsigned long long inode; unsigned local, peer; };
struct pending { int active, fd; uint64_t started, requested; long number; struct endpoint socket; };
struct thread { pid_t id; int newborn; struct pending pending; };
struct flow { unsigned long long inode; int blocked; unsigned short_writes, would_block, resumed; };
struct capture {
    FILE *output;
    const char *nonce;
    const char *mode, *image;
    dev_t image_device;
    ino_t image_inode;
    unsigned local, peer, records;
    size_t bytes;
    int failed, exited, exit_code, signal, test_client, drain, pidfd, test_writev_started;
    pid_t child;
    struct thread threads[MAX_THREADS];
    struct flow flows[MAX_SOCKETS];
};
static volatile sig_atomic_t interrupted;

static uint64_t now_ns(void) {
    struct timespec value;
    if (clock_gettime(CLOCK_MONOTONIC, &value) != 0) { return 0; }
    return (uint64_t)value.tv_sec * 1000000000U + (uint64_t)value.tv_nsec;
}

static void on_signal(int number) { interrupted = number; }

static int auth_case_allowed(const char *value) {
    return value != NULL && (strcmp(value, AUTH_CASE_SHORT) == 0 || strcmp(value, AUTH_CASE_BLOCK) == 0);
}

static int number(const char *text, unsigned minimum, unsigned maximum, unsigned *out) {
    char *end = NULL;
    unsigned long value;
    if (text == NULL || *text == '\0' || strspn(text, "0123456789") != strlen(text)) { return 0; }
    errno = 0;
    value = strtoul(text, &end, 10);
    if (errno != 0 || *end != '\0' || value < minimum || value > maximum) { return 0; }
    *out = (unsigned)value;
    return 1;
}

static int private_path(const char *path, int leaf_required, int require_owned_parent) {
    char copy[PATH_MAX];
    struct stat info;
    char *part;
    size_t length = strlen(path);
    if (length == 0 || length >= sizeof(copy) || path[0] != '/' || strstr(path, "//") != NULL) { return 0; }
    memcpy(copy, path, length + 1U);
    for (part = copy + 1; ; ++part) {
        char saved;
        int leaf;
        if (*part != '/' && *part != '\0') { continue; }
        saved = *part; leaf = saved == '\0'; *part = '\0';
        if (strcmp(strrchr(copy, '/') + 1, ".") == 0 || strcmp(strrchr(copy, '/') + 1, "..") == 0) { return 0; }
        if (lstat(copy, &info) != 0) {
            if (!(leaf && !leaf_required && errno == ENOENT)) { return 0; }
        } else {
            int sticky = strcmp(copy, "/var/tmp") == 0 && info.st_uid == 0 && (info.st_mode & S_ISVTX);
            if (S_ISLNK(info.st_mode) || (info.st_uid != 0 && info.st_uid != getuid()) ||
                    ((info.st_mode & 0022) && !sticky) || (!leaf && !S_ISDIR(info.st_mode))) { return 0; }
        }
        if (leaf) { break; }
        *part = saved;
    }
    if (require_owned_parent) {
        char *last = strrchr(copy, '/');
        if (last == copy) { return 0; }
        *last = '\0';
        if (lstat(copy, &info) != 0 || info.st_uid != getuid() || (info.st_mode & 0077)) { return 0; }
    }
    return 1;
}

static int admitted_identity(void) {
    FILE *stream;
    char line[256];
    int masks = 0, no_new_privileges = 0;
    if (getuid() == 0 || getuid() != geteuid() || getgid() != getegid()) { return 0; }
    stream = fopen("/proc/self/status", "re");
    if (stream == NULL) { return 0; }
    while (fgets(line, sizeof(line), stream) != NULL) {
        if (strncmp(line, "Cap", 3) == 0 && strchr(line, ':') != NULL) {
            char *end;
            unsigned long long value = strtoull(strchr(line, ':') + 1, &end, 16);
            if (value != 0 || end == strchr(line, ':') + 1) { (void)fclose(stream); return 0; }
            ++masks;
        }
        if (sscanf(line, "NoNewPrivs: %d", &no_new_privileges) == 1) { continue; }
    }
    (void)fclose(stream);
    return masks == 5 && no_new_privileges == 1;
}

static int same_process(pid_t id, pid_t leader) {
    char path[64], line[256];
    FILE *stream;
    int tgid = -1, matched_uid = 0;
    (void)snprintf(path, sizeof(path), "/proc/%ld/status", (long)id);
    stream = fopen(path, "re");
    if (stream == NULL) { return 0; }
    while (fgets(line, sizeof(line), stream) != NULL) {
        unsigned a, b, c, d;
        (void)sscanf(line, "Tgid: %d", &tgid);
        if (sscanf(line, "Uid: %u %u %u %u", &a, &b, &c, &d) == 4) {
            matched_uid = a == getuid() && b == getuid() && c == getuid() && d == getuid();
        }
    }
    (void)fclose(stream);
    return matched_uid && tgid == leader;
}

static unsigned long long socket_inode(pid_t id, int fd) {
    char path[80], link[128], tail;
    ssize_t length;
    unsigned long long inode;
    (void)snprintf(path, sizeof(path), "/proc/%ld/fd/%d", (long)id, fd);
    length = readlink(path, link, sizeof(link) - 1U);
    if (length <= 0 || (size_t)length >= sizeof(link) - 1U) { return 0; }
    link[length] = '\0';
    return sscanf(link, "socket:[%llu]%c", &inode, &tail) == 1 ? inode : 0;
}

static int tcp_endpoint(pid_t id, int fd, struct endpoint *out) {
    char path[80], line[1024];
    FILE *stream;
    unsigned long long inode = socket_inode(id, fd);
    int found = 0;
    if (inode == 0) { return 0; }
    (void)snprintf(path, sizeof(path), "/proc/%ld/net/tcp", (long)id);
    stream = fopen(path, "re");
    if (stream == NULL) { return 0; }
    while (fgets(line, sizeof(line), stream) != NULL) {
        unsigned local_ip, remote_ip, local_port, peer_port;
        unsigned long long row_inode;
        if (sscanf(line, "%*u: %8x:%x %8x:%x %*x %*x:%*x %*x:%*x %*x %*u %*u %llu",
                &local_ip, &local_port, &remote_ip, &peer_port, &row_inode) == 5 &&
                row_inode == inode && local_ip == 0x0100007fU && remote_ip == 0x0100007fU) {
            *out = (struct endpoint){inode, local_port, peer_port}; found = 1; break;
        }
    }
    (void)fclose(stream);
    return found;
}

static const char *operation(long syscall) {
    switch (syscall) {
        case SYS_write: return "write";
        case SYS_writev: return "writev";
        case SYS_sendto: return "sendto";
        case SYS_sendmsg: return "sendmsg";
        case SYS_sendfile: return "sendfile";
        default: return NULL;
    }
}

static uint64_t requested_size(pid_t id, const struct ptrace_syscall_info *info) {
    if (info->entry.nr == SYS_write || info->entry.nr == SYS_sendto) {
        return info->entry.args[2] <= SSIZE_MAX ? info->entry.args[2] : UINT64_MAX;
    }
    if (info->entry.nr == SYS_sendfile) {
        return info->entry.args[3] <= SSIZE_MAX ? info->entry.args[3] : UINT64_MAX;
    }
    if (info->entry.nr == SYS_writev) {
        uint64_t sum = 0, i;
        uint64_t base = info->entry.args[1], count = info->entry.args[2];
        const uint64_t user_last = 0x00007fffffffffffULL;
        /* Conservative x86-64 lower canonical user addresses only. Alignment
         * is an observer policy, not a claim about kernel writev validity.
         * Validate the WHOLE iovec metadata span before any remote read.
         * Zero iovcnt requires no pointer and no read. */
        if (count == 0) { return 0; }
        if (count > 64U || base < 4096U || base > user_last || base % 8U != 0 ||
                count * 16U - 1U > user_last - base) { return UINT64_MAX; }
        /* Read only each iov_len metadata word, never its payload pointer/data. */
        for (i = 0; i < count; ++i) {
            unsigned long address = (unsigned long)(base + i * 16U + 8U);
            unsigned long length;
            errno = 0;
            length = (unsigned long)ptrace(PTRACE_PEEKDATA, id, (void *)address, NULL);
            if (errno != 0 || length > (uint64_t)SSIZE_MAX - sum) { return UINT64_MAX; }
            sum += length;
        }
        return sum;
    }
    return UINT64_MAX; /* sendmsg length is deliberately unknown, not guessed. */
}

static struct thread *thread_slot(struct capture *capture, pid_t id, int create) {
    unsigned i;
    struct thread *empty = NULL;
    for (i = 0; i < MAX_THREADS; ++i) {
        if (capture->threads[i].id == id) { return &capture->threads[i]; }
        if (capture->threads[i].id == 0 && empty == NULL) { empty = &capture->threads[i]; }
    }
    if (!create || empty == NULL) { return NULL; }
    empty->id = id; empty->newborn = 1; return empty;
}

static struct flow *flow_slot(struct capture *capture, unsigned long long inode) {
    unsigned i;
    struct flow *empty = NULL;
    for (i = 0; i < MAX_SOCKETS; ++i) {
        if (capture->flows[i].inode == inode) { return &capture->flows[i]; }
        if (capture->flows[i].inode == 0 && empty == NULL) { empty = &capture->flows[i]; }
    }
    if (empty != NULL) { empty->inode = inode; }
    return empty;
}

static void syscall_exit(struct capture *capture, struct thread *thread, long long result) {
    struct pending *pending = &thread->pending;
    struct flow *flow;
    int identity, length;
    char row[1024];
    if (!pending->active) { return; }
    pending->active = 0;
    identity = socket_inode(thread->id, pending->fd) == pending->socket.inode;
    flow = flow_slot(capture, pending->socket.inode);
    if (!identity || flow == NULL || capture->records >= MAX_RECORDS) { capture->failed = 1; return; }
    /* Synthetic reader only: create independent backpressure for writev after
     * the write phase. Host mode never owns a client and never takes this path. */
    if (capture->test_client >= 0 && pending->number == SYS_writev && result > 0 &&
            pending->requested != UINT64_MAX && !capture->test_writev_started) {
        capture->test_writev_started = 1; capture->drain = 0;
    }
    if (result == -EAGAIN) { ++flow->would_block; flow->blocked = 1; capture->drain = 1; }
    if (result > 0 && pending->requested != UINT64_MAX && (uint64_t)result < pending->requested) { ++flow->short_writes; }
    if (result > 0 && flow->blocked) { ++flow->resumed; flow->blocked = 0; }
    length = snprintf(row, sizeof(row),
        "{\"schema\":\"traefik-own-child-syscall-v1\",\"nonce\":\"%s\",\"pid\":%ld,\"tid\":%ld,"
        "\"fd\":%d,\"socket_inode\":%llu,\"local_address\":\"127.0.0.1\",\"local_port\":%u,"
        "\"peer_address\":\"127.0.0.1\",\"peer_port\":%u,\"operation\":\"%s\","
        "\"requested_bytes\":%lld,\"requested_size_known\":%s,\"kernel_result\":%lld,\"errno\":%lld,"
        "\"entry_monotonic_ns\":%llu,\"exit_monotonic_ns\":%llu,\"fd_identity_unchanged\":true}\n",
        capture->nonce, (long)capture->child, (long)thread->id, pending->fd, pending->socket.inode,
        pending->socket.local, pending->socket.peer, operation(pending->number),
        pending->requested == UINT64_MAX ? -1LL : (long long)pending->requested,
        pending->requested == UINT64_MAX ? "false" : "true", result,
        result < 0 ? -result : 0LL, (unsigned long long)pending->started, (unsigned long long)now_ns());
    if (length <= 0 || (size_t)length >= sizeof(row) || capture->bytes + (size_t)length > MAX_OUTPUT ||
            fwrite(row, 1, (size_t)length, capture->output) != (size_t)length || fflush(capture->output) != 0) {
        capture->failed = 1; return;
    }
    capture->bytes += (size_t)length; ++capture->records;
}

static int syscall_stop(struct capture *capture, struct thread *thread) {
    struct ptrace_syscall_info info;
    long length;
    memset(&info, 0, sizeof(info));
    length = ptrace(PTRACE_GET_SYSCALL_INFO, thread->id, sizeof(info), &info);
    if (length < 0 || info.arch != AUDIT_ARCH_X86_64) { return 0; }
    if (info.op == PTRACE_SYSCALL_INFO_ENTRY) {
        const char *name = operation((long)info.entry.nr);
        thread->pending.active = 0;
        if (name != NULL && info.entry.args[0] <= INT_MAX) {
            struct endpoint endpoint;
            int fd = (int)info.entry.args[0];
            if (tcp_endpoint(thread->id, fd, &endpoint) && endpoint.local == capture->local &&
                    (capture->peer == 0 || endpoint.peer == capture->peer)) {
                thread->pending = (struct pending){1, fd, now_ns(), requested_size(thread->id, &info),
                    (long)info.entry.nr, endpoint};
            }
        }
    } else if (info.op == PTRACE_SYSCALL_INFO_EXIT) {
        syscall_exit(capture, thread, info.exit.rval);
    } else { return 0; }
    return !capture->failed;
}

static void reap_owned(struct capture *capture) {
    uint64_t deadline = now_ns() + 3000000000ULL;
    unsigned i;
    /* pidfd binds the exact forked process even after numeric PID reuse. */
    if (capture->pidfd >= 0) { (void)syscall(SYS_pidfd_send_signal, capture->pidfd, SIGKILL, NULL, 0); }
    for (i = 0; i < MAX_THREADS; ++i) {
        if (capture->threads[i].id > 0) { (void)ptrace(PTRACE_CONT, capture->threads[i].id, NULL, (void *)(long)SIGKILL); }
    }
    while (now_ns() < deadline) {
        int status;
        pid_t id = waitpid(-1, &status, __WALL | WNOHANG);
        if (id < 0 && errno == ECHILD) { return; }
        if (id > 0 && WIFSTOPPED(status)) { (void)ptrace(PTRACE_CONT, id, NULL, (void *)(long)SIGKILL); }
        if (id <= 0) { struct timespec pause = {0, 1000000}; (void)nanosleep(&pause, NULL); }
    }
    capture->failed = 1;
}

static void observe(struct capture *capture, unsigned seconds) {
    uint64_t deadline = now_ns() + (uint64_t)seconds * 1000000000ULL;
    unsigned long options = PTRACE_O_TRACESYSGOOD | PTRACE_O_TRACECLONE | PTRACE_O_TRACEFORK |
        PTRACE_O_TRACEVFORK | PTRACE_O_TRACEEXEC | PTRACE_O_EXITKILL;
    int status;
    for (;;) {
        pid_t stopped;
        if (interrupted || now_ns() >= deadline) { capture->failed = 1; return; }
        stopped = waitpid(capture->child, &status, WNOHANG);
        if (stopped == capture->child) { break; }
        if (stopped < 0 && errno != EINTR) { capture->failed = 1; return; }
        { struct timespec pause = {0, 1000000}; (void)nanosleep(&pause, NULL); }
    }
    if (!WIFSTOPPED(status) || WSTOPSIG(status) != SIGSTOP ||
            !same_process(capture->child, capture->child) || getpgid(capture->child) != capture->child ||
            ptrace(PTRACE_SETOPTIONS, capture->child, NULL, (void *)options) != 0) { capture->failed = 1; return; }
    thread_slot(capture, capture->child, 1)->newborn = 0;
    if (interrupted || now_ns() >= deadline) { capture->failed = 1; return; }
    if (ptrace(PTRACE_SYSCALL, capture->child, NULL, NULL) != 0) { capture->failed = 1; return; }
    while (!capture->failed && !capture->exited) {
        pid_t id;
        struct thread *thread;
        int delivered = 0;
        unsigned event;
        if (interrupted || now_ns() >= deadline) { capture->failed = 1; break; }
        if (capture->drain && capture->test_client >= 0) {
            char buffer[32768];
            while (read(capture->test_client, buffer, sizeof(buffer)) > 0) { /* discard synthetic bytes */ }
        }
        id = waitpid(-1, &status, __WALL | WNOHANG);
        if (id == 0) { struct timespec pause = {0, 1000000}; (void)nanosleep(&pause, NULL); continue; }
        if (id < 0) { if (errno == EINTR) { continue; } capture->failed = 1; break; }
        thread = thread_slot(capture, id, 0);
        /* A clone's initial stop may be reported before its parent's event.
         * This admits only our automatically traced same-process thread. */
        if (thread == NULL && WIFSTOPPED(status) && WSTOPSIG(status) == SIGSTOP &&
                same_process(id, capture->child)) { thread = thread_slot(capture, id, 1); }
        if (thread == NULL) { capture->failed = 1; break; }
        if (WIFEXITED(status) || WIFSIGNALED(status)) {
            if (id == capture->child) {
                capture->exited = 1; capture->exit_code = WIFEXITED(status) ? WEXITSTATUS(status) : -1;
                capture->signal = WIFSIGNALED(status) ? WTERMSIG(status) : 0;
            }
            memset(thread, 0, sizeof(*thread)); continue;
        }
        if (!WIFSTOPPED(status)) { capture->failed = 1; break; }
        event = (unsigned)status >> 16;
        if (event == PTRACE_EVENT_CLONE) {
            unsigned long child_id = 0;
            if (ptrace(PTRACE_GETEVENTMSG, id, NULL, &child_id) != 0 || child_id > INT_MAX ||
                    !same_process((pid_t)child_id, capture->child) || thread_slot(capture, (pid_t)child_id, 1) == NULL) {
                capture->failed = 1; break;
            }
        } else if (event == PTRACE_EVENT_FORK || event == PTRACE_EVENT_VFORK) {
            unsigned long rejected = 0;
            if (ptrace(PTRACE_GETEVENTMSG, id, NULL, &rejected) == 0 && rejected <= INT_MAX) { (void)kill((pid_t)rejected, SIGKILL); }
            capture->failed = 1; break;
        } else if (event == PTRACE_EVENT_EXEC) {
            char path[64], row[768];
            struct stat image;
            int length;
            /* Only the parent's exact initial fexecve is admitted. */
            if (id != capture->child || thread->newborn == -1) { capture->failed = 1; break; }
            (void)snprintf(path, sizeof(path), "/proc/%ld/exe", (long)id);
            if (stat(path, &image) != 0 || image.st_dev != capture->image_device || image.st_ino != capture->image_inode) {
                capture->failed = 1; break;
            }
            length = snprintf(row, sizeof(row), "{\"schema\":\"traefik-own-child-exec-v1\",\"nonce\":\"%s\",\"child_pid\":%ld,\"image\":\"%s\",\"mode\":\"%s\",\"opened_image_identity_verified\":true,\"runtime_qualified\":false}\n",
                capture->nonce, (long)id, capture->image, capture->mode);
            if (length <= 0 || (size_t)length >= sizeof(row) || capture->bytes + (size_t)length > MAX_OUTPUT ||
                    fwrite(row, 1, (size_t)length, capture->output) != (size_t)length || fflush(capture->output) != 0) {
                capture->failed = 1; break;
            }
            capture->bytes += (size_t)length;
            thread->newborn = -1;
        } else if (WSTOPSIG(status) == (SIGTRAP | 0x80)) {
            if (!syscall_stop(capture, thread)) { capture->failed = 1; break; }
        } else if (thread->newborn == 1 && WSTOPSIG(status) == SIGSTOP) { thread->newborn = 0; }
        else { delivered = WSTOPSIG(status); }
        if (ptrace(PTRACE_SYSCALL, id, NULL, (void *)(long)delivered) != 0) { capture->failed = 1; }
    }
}

static int test_connection(unsigned *local, unsigned *peer, int *client) {
    struct sockaddr_in address = { .sin_family = AF_INET, .sin_addr.s_addr = htonl(INADDR_LOOPBACK) };
    socklen_t length = sizeof(address);
    int listener = socket(AF_INET, SOCK_STREAM | SOCK_CLOEXEC, 0), accepted;
    if (listener < 0 || bind(listener, (struct sockaddr *)&address, sizeof(address)) != 0 ||
            getsockname(listener, (struct sockaddr *)&address, &length) != 0 || listen(listener, 1) != 0) { return -1; }
    *local = ntohs(address.sin_port);
    *client = socket(AF_INET, SOCK_STREAM | SOCK_CLOEXEC, 0);
    if (*client < 0 || connect(*client, (struct sockaddr *)&address, sizeof(address)) != 0) { (void)close(listener); return -1; }
    accepted = accept4(listener, NULL, NULL, 0);
    (void)close(listener);
    length = sizeof(address);
    if (accepted < 0 || getsockname(*client, (struct sockaddr *)&address, &length) != 0) { return -1; }
    *peer = ntohs(address.sin_port);
    (void)fcntl(*client, F_SETFL, O_NONBLOCK);
    return accepted;
}

static int test_writer(int fd) {
    char data[65536];
    unsigned total = 0, phase;
    int size = 4096;
    uint64_t deadline = now_ns() + 12000000000ULL;
    memset(data, 'T', sizeof(data));
    if (setsockopt(fd, SOL_SOCKET, SO_SNDBUF, &size, sizeof(size)) != 0 || fcntl(fd, F_SETFL, O_NONBLOCK) != 0) { return 77; }
    {
        struct iovec vectors[65] = {{0}};
        vectors[0].iov_base = data;
        /* Execute the original invalid syscalls unchanged. The observer must
         * neither follow these addresses nor invent requested byte counts. */
        (void)syscall(SYS_writev, fd, NULL, 1);
        (void)syscall(SYS_writev, fd, (void *)(uintptr_t)(UINT64_MAX - 7U), 2);
        (void)syscall(SYS_writev, fd, (void *)(uintptr_t)0x0000800000000000ULL, 1);
        (void)syscall(SYS_writev, fd, (void *)(uintptr_t)0x00007ffffffffff8ULL, 2);
        (void)syscall(SYS_writev, fd, (void *)(uintptr_t)0x10000U, 1);
        (void)syscall(SYS_writev, fd, vectors, UINT64_MAX);
        (void)syscall(SYS_writev, fd, vectors, 65);
        (void)syscall(SYS_writev, fd, (char *)vectors + 1, 1);
        vectors[0].iov_base = NULL;
        vectors[0].iov_len = (size_t)SSIZE_MAX;
        vectors[1].iov_len = 1;
        (void)syscall(SYS_writev, fd, vectors, 2);
        vectors[0].iov_len = (size_t)SSIZE_MAX + 1U;
        (void)syscall(SYS_writev, fd, vectors, 1);
        (void)syscall(SYS_writev, fd, NULL, 0);
    }
    for (phase = 0; phase < 2; ++phase) {
      total = 0;
      while (total < TEST_BYTES && now_ns() < deadline) {
        size_t wanted = TEST_BYTES - total < sizeof(data) ? TEST_BYTES - total : sizeof(data);
        struct iovec vectors[2] = {{data, wanted / 2}, {data + wanted / 2, wanted - wanted / 2}};
        ssize_t result = phase == 0 ? write(fd, data, wanted) : writev(fd, vectors, 2);
        if (result > 0) { total += (unsigned)result; }
        else if (result < 0 && (errno == EAGAIN || errno == EINTR)) { struct timespec pause = {0, 1000000}; (void)nanosleep(&pause, NULL); }
        else { return 77; }
      }
      if (total != TEST_BYTES) { return 77; }
    }
    (void)close(fd);
    return total == TEST_BYTES ? 0 : 77;
}

static void *test_thread(void *argument) {
    return (void *)(intptr_t)test_writer((int)(intptr_t)argument);
}

static int threaded_test_writer(int fd) {
    pthread_t thread;
    void *result = NULL;
    if (pthread_create(&thread, NULL, test_thread, (void *)(intptr_t)fd) != 0 ||
            pthread_join(thread, &result) != 0) { return 77; }
    return (int)(intptr_t)result;
}

static int executable(const char *path) {
    struct stat info;
    int fd;
    if (!private_path(path, 1, 0)) { return -1; }
    fd = open(path, O_RDONLY | O_NOFOLLOW | O_CLOEXEC);
    if (fd < 0) { return -1; }
    if (fstat(fd, &info) != 0 || !S_ISREG(info.st_mode) || info.st_uid != getuid() ||
            info.st_nlink != 1 || !(info.st_mode & S_IXUSR) || (info.st_mode & (S_ISUID | S_ISGID | 0022))) {
        (void)close(fd); return -1;
    }
    return fd;
}

int main(int argc, char **argv) {
    struct capture capture = { .test_client = -1, .pidfd = -1 };
    const char *output = NULL, *nonce = NULL;
    const char *auth_case = NULL;
    unsigned seconds = 30, i;
    int self_test = 0, binary = -1, test_fd = -1, out_fd, seconds_seen = 0, peer_seen = 0;
    char self[PATH_MAX];
    char auth_config[320], auth_cwd[256], auth_output[256], auth_log[320], auth_access[320], auth_entry[80], auth_file[384];
    struct stat opened_image;
    if (!admitted_identity()) { return 77; }
    if (argc == 3 && strcmp(argv[1], "--self-test-child") == 0) {
        unsigned fd;
        return number(argv[2], 3, 4095, &fd) ? threaded_test_writer((int)fd) : 77;
    }
    for (i = 1; i < (unsigned)argc; ++i) {
        if (strcmp(argv[i], "--self-test") == 0 && !self_test) { self_test = 1; continue; }
        if (i + 1U >= (unsigned)argc) { return 77; }
        if (strcmp(argv[i], "--output") == 0 && output == NULL) { output = argv[++i]; }
        else if (strcmp(argv[i], "--auth-case") == 0 && auth_case == NULL) { auth_case = argv[++i]; }
        else if (strcmp(argv[i], "--nonce") == 0 && nonce == NULL) { nonce = argv[++i]; }
        else if (strcmp(argv[i], "--host-port") == 0 && capture.local == 0) { if (!number(argv[++i], 1, 65535, &capture.local)) { return 77; } }
        else if (strcmp(argv[i], "--peer-port") == 0 && !peer_seen++) { if (!number(argv[++i], 0, 65535, &capture.peer)) { return 77; } }
        else if (strcmp(argv[i], "--seconds") == 0 && !seconds_seen++) { if (!number(argv[++i], 1, 300, &seconds)) { return 77; } }
        else { return 77; }
    }
    if (output == NULL || nonce == NULL || strlen(nonce) < 8 || strlen(nonce) > 64 ||
            strspn(nonce, "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-_") != strlen(nonce) ||
            !private_path(output, 0, 1) || (!self_test && (strncmp(output, "/task/", 6) != 0 || capture.local == 0))) { return 77; }
    if (auth_case != NULL) {
        if (!auth_case_allowed(auth_case) || strcmp(nonce, auth_case) != 0) { return 77; }
        (void)snprintf(auth_cwd, sizeof(auth_cwd), "/task/cases/%s/runtime", auth_case);
        (void)snprintf(auth_config, sizeof(auth_config), "%s/effective-config/traefik-dynamic.yaml", auth_cwd);
        (void)snprintf(auth_output, sizeof(auth_output), "/task/cases/%s/host-syscalls.jsonl", auth_case);
        (void)snprintf(auth_log, sizeof(auth_log), "I12_ACCEPTANCE_HOST_LOG=%s/logs/host-lifecycle.jsonl", auth_cwd);
        (void)snprintf(auth_access, sizeof(auth_access), "--accesslog.filepath=%s/logs/traefik-access.log", auth_cwd);
        (void)snprintf(auth_file, sizeof(auth_file), "--providers.file.filename=%s", auth_config);
        if (!self_test && strcmp(output, auth_output) != 0) { return 77; }
    }
    if (self_test) {
        if (realpath(argv[0], self) == NULL || strcmp(argv[0], self) != 0) { return 77; }
        binary = executable(self);
        test_fd = test_connection(&capture.local, &capture.peer, &capture.test_client);
        if (test_fd < 0 || binary < 0) { return 77; }
    } else {
        struct stat config;
        const char *config_path = auth_case == NULL ? HOST_CONFIG : auth_config;
        if (chdir(auth_case == NULL ? "/task/runtime" : auth_cwd) != 0 || !private_path(config_path, 1, 0) ||
                stat(config_path, &config) != 0 || !S_ISREG(config.st_mode) || config.st_uid != getuid()) { return 77; }
        if (auth_case != NULL && !private_path(auth_log + strlen("I12_ACCEPTANCE_HOST_LOG="), 1, 0)) { return 77; }
        binary = executable(HOST_BINARY);
        if (binary < 0) { return 77; }
    }
    if (fstat(binary, &opened_image) != 0) { (void)close(binary); return 77; }
    capture.image_device = opened_image.st_dev; capture.image_inode = opened_image.st_ino;
    capture.image = self_test ? self : HOST_BINARY;
    capture.mode = self_test ? (auth_case == NULL ? "synthetic-native" : "synthetic-auth") : (auth_case == NULL ? "native" : "auth");
    (void)snprintf(auth_entry, sizeof(auth_entry), "--entryPoints.web.address=127.0.0.1:%u", capture.local);
    out_fd = open(output, O_WRONLY | O_CREAT | O_EXCL | O_NOFOLLOW | O_CLOEXEC, 0600);
    if (out_fd < 0) { return 77; }
    capture.output = fdopen(out_fd, "w"); capture.nonce = nonce;
    if (capture.output == NULL) { (void)close(out_fd); return 77; }
    (void)signal(SIGTERM, on_signal); (void)signal(SIGINT, on_signal);
    capture.child = fork();
    if (capture.child == 0) {
        char fd[16];
        char *const test_env[] = {"PATH=/usr/bin:/bin", "LC_ALL=C", "TZ=UTC", NULL};
        char *const host_env[] = {"PATH=/opt/controller:/usr/local/bin:/usr/bin:/usr/sbin:/bin", "HOME=/task", "TMPDIR=/task/tmp", "TMP_ROOT=/task/tmp", "XDG_CACHE_HOME=/task/cache", "XDG_DATA_HOME=/task/rtk-data", "LC_ALL=C", "TZ=UTC", "PYTHONDONTWRITEBYTECODE=1", "CONNECTOR_ROOT=/mnt/src", "BUILD_ROOT=/task/build", "GOTOOLCHAIN=local", "GOPROXY=off", "GOSUMDB=off", "GOMODCACHE=/task/go-mod", "GOCACHE=/task/go-cache", "GO=/usr/local/go/bin/go", "GOFLAGS=-mod=readonly", "TRAEFIK_NATIVE_RUNTIME_ROOT=/task/runtime", "TRAEFIK_ENGINE_SOCKET_PARENT=/task/sockets", "TRAEFIK_BIN=" HOST_BINARY, "MSCONNECTOR_RULES_FILE=/task/rules.conf", NULL};
        char *const auth_env[] = {"PATH=/opt/controller:/usr/local/bin:/usr/bin:/usr/sbin:/bin", "HOME=/task", "TMPDIR=/task/tmp", "TMP_ROOT=/task/tmp", "XDG_CACHE_HOME=/task/cache", "XDG_DATA_HOME=/task/rtk-data", "LC_ALL=C", "TZ=UTC", "PYTHONDONTWRITEBYTECODE=1", "CONNECTOR_ROOT=/mnt/src", auth_log, NULL};
        (void)snprintf(fd, sizeof(fd), "%d", test_fd);
        char *const test_argv[] = {self, "--self-test-child", fd, NULL};
        char *const host_argv[] = {HOST_BINARY, "--configFile=" HOST_CONFIG, NULL};
        char *const auth_argv[] = {HOST_BINARY, auth_entry,
            "--experimental.localPlugins.modsecurityResponseObserver.moduleName=" OBSERVER_MODULE,
            "--experimental.localPlugins.modsecurityResponseObserver.settings.useUnsafe=true",
            "--experimental.abortOnPluginFailure=true", auth_file, "--providers.file.watch=false", "--api=false", "--log.level=INFO",
            "--global.sendAnonymousUsage=false", "--global.checkNewVersion=false", "--accesslog=true", auth_access, NULL};
        (void)close(out_fd);
        if (capture.test_client >= 0) { (void)close(capture.test_client); }
        if (setpgid(0, 0) != 0 || ptrace(PTRACE_TRACEME, 0, NULL, NULL) != 0) { _exit(77); }
        (void)raise(SIGSTOP);
        fexecve(binary, self_test ? test_argv : (auth_case == NULL ? host_argv : auth_argv),
                self_test ? test_env : (auth_case == NULL ? host_env : auth_env));
        _exit(77);
    }
    (void)close(binary);
    if (test_fd >= 0) { (void)close(test_fd); }
    if (capture.child <= 0) { (void)fclose(capture.output); return 77; }
    capture.pidfd = (int)syscall(SYS_pidfd_open, capture.child, 0);
    if (capture.pidfd < 0) {
        /* Child is still our unreaped initial stop; numeric identity cannot
         * have been recycled. Fail without ever running candidate code. */
        (void)kill(capture.child, SIGKILL);
        (void)waitpid(capture.child, NULL, 0);
        (void)fclose(capture.output);
        return 77;
    }
    observe(&capture, seconds);
    reap_owned(&capture);
    (void)close(capture.pidfd);
    if (capture.test_client >= 0) { (void)close(capture.test_client); }
    {
        unsigned shorts = 0, blocked = 0, resumed = 0;
        int complete;
        for (i = 0; i < MAX_SOCKETS; ++i) { shorts += capture.flows[i].short_writes; blocked += capture.flows[i].would_block; resumed += capture.flows[i].resumed; }
        complete = !capture.failed && capture.exited && capture.exit_code == 0 && capture.signal == 0 && capture.records > 0;
        if (self_test && (!shorts || !blocked || !resumed)) { complete = 0; }
        if (fprintf(capture.output, "{\"schema\":\"traefik-own-child-final-v1\",\"nonce\":\"%s\",\"child_pid\":%ld,\"uid\":%ld,\"capture_complete\":%s,\"kernel_records\":%u,\"short_writes\":%u,\"would_block\":%u,\"resumed_same_inode\":%u,\"child_exit\":%d,\"child_signal\":%d,\"known_target_peer_port\":%u,\"client_receipt_join_required\":true,\"runtime_qualified\":false}\n",
                nonce, (long)capture.child, (long)getuid(), complete ? "true" : "false", capture.records,
                shorts, blocked, resumed, capture.exit_code, capture.signal, capture.peer) < 0 || fclose(capture.output) != 0) { return 77; }
        return complete ? 0 : 77;
    }
}
