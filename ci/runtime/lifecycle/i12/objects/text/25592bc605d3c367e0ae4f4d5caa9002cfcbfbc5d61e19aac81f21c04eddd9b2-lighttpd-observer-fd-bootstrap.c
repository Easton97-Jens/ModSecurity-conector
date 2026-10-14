/* External test-only module-local descriptor bootstrap. No guard weakening.
 * The native collector's original constructor still admits the actual FD.
 * Low constructor priority opens before admission; low destructor priority
 * closes after the original collector emitted its final physical counters. */
#define _POSIX_C_SOURCE 200809L
#include <errno.h>
#include <fcntl.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/stat.h>
#include <unistd.h>

static int owned_observer_fd = -1;
static int bootstrap_failed;

static int private_observer_file(const char *path) {
    char components[4096];
    if ((strncmp(path, "/task/", 6U) != 0 &&
         strncmp(path, "/var/tmp/codex/ModSecurity-conector/", sizeof("/var/tmp/codex/ModSecurity-conector/")-1U) != 0) ||
            strlen(path) >= sizeof(components) || path[strlen(path)-1U] == '/') return -1;
    (void)snprintf(components, sizeof(components), "%s", path + 1);
    int directory = open("/", O_RDONLY | O_DIRECTORY | O_NOFOLLOW | O_CLOEXEC);
    if (directory < 0) return -1;
    char *state = NULL;
    char *component = strtok_r(components, "/", &state);
    unsigned int depth = 0U;
    while (component != NULL) {
        char *next = strtok_r(NULL, "/", &state);
        if (strcmp(component, ".") == 0 || strcmp(component, "..") == 0) {
            (void)close(directory);
            return -1;
        }
        if (next == NULL) {
            int fd = openat(directory, component,
                O_WRONLY | O_APPEND | O_CREAT | O_NOFOLLOW | O_CLOEXEC, 0600);
            (void)close(directory);
            return fd;
        }
        int child = openat(directory, component, O_RDONLY | O_DIRECTORY | O_NOFOLLOW | O_CLOEXEC);
        struct stat details;
        int sticky_root_tmp = child >= 0 && fstat(child, &details) == 0 &&
            depth == 1U && details.st_uid == 0 && (details.st_mode & 01000U) != 0 &&
            strcmp(component, "tmp") == 0;
        if (child < 0 || fstat(child, &details) != 0 ||
                (details.st_uid != 0 && details.st_uid != geteuid()) ||
                ((details.st_mode & 022U) != 0 && !sticky_root_tmp)) {
            if (child >= 0) (void)close(child);
            (void)close(directory);
            return -1;
        }
        (void)close(directory);
        directory = child;
        component = next;
        ++depth;
    }
    (void)close(directory);
    return -1;
}

__attribute__((constructor(101))) static void prepare_observer_descriptor(void) {
    int saved = errno;
    const char *path = getenv("MSCONNECTOR_LIGHTTPD_NATIVE_OBSERVER");
    if (path == NULL) { errno = saved; return; }
    if (unsetenv("MSCONNECTOR_LIFECYCLE_FD") != 0) { bootstrap_failed = 1; goto done; }
    if (path[0] != '/') { bootstrap_failed = 1; goto done; }
    int fd = private_observer_file(path);
    struct stat details;
    if (fd < 0) { bootstrap_failed = 1; goto done; }
    if (fstat(fd, &details) != 0 || !S_ISREG(details.st_mode) ||
            details.st_uid != geteuid() || (details.st_mode & 07777U) != 0600U || details.st_nlink != 1) {
        (void)close(fd);
        bootstrap_failed = 1;
        goto done;
    }
    char descriptor[32];
    int length = snprintf(descriptor, sizeof(descriptor), "%d", fd);
    if (length <= 0 || (size_t)length >= sizeof(descriptor) ||
            setenv("MSCONNECTOR_LIFECYCLE_FD", descriptor, 1) != 0) {
        (void)close(fd);
        bootstrap_failed = 1;
        goto done;
    }
    owned_observer_fd = fd;
done:
    if (bootstrap_failed) {
        static const char error[] = "lighttpd-observer-fd-bootstrap: observation admission unavailable\n";
        (void)write(STDERR_FILENO, error, sizeof(error)-1U);
    }
    errno = saved;
}

__attribute__((destructor(101))) static void release_observer_descriptor(void) {
    int saved = errno;
    if (owned_observer_fd >= 0 && close(owned_observer_fd) != 0) {
        static const char error[] = "lighttpd-observer-fd-bootstrap: descriptor close failed\n";
        (void)write(STDERR_FILENO, error, sizeof(error)-1U);
    }
    errno = saved;
}
