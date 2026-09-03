/*
 * Focused private event-file descriptor control.
 *
 * Run from the repository root with an explicitly registered external test
 * root, for example:
 *
 *   MSCONNECTOR_EVENT_FILE_TEST_ROOT=/var/tmp/codex/... \
 *     cc -std=c17 -Wall -Wextra -Werror -Icommon/include \
 *     tests/private_event_file_smoke.c common/src/event.c \
 *     common/src/event_jsonl.c common/src/json_escape.c -o <external-bin> && \
 *     MSCONNECTOR_EVENT_FILE_TEST_ROOT=/var/tmp/codex/... <external-bin>
 */

#if !defined(_WIN32) && !defined(_POSIX_C_SOURCE)
#define _POSIX_C_SOURCE 200809L
#endif

#include "msconnector/event_jsonl.h"

#include <errno.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#if !defined(_WIN32)
#include <fcntl.h>
#include <sys/stat.h>
#include <sys/types.h>
#include <unistd.h>
#endif

#define TEST_PATH_SIZE 4096U

#if !defined(_WIN32)
static int join_path(char *destination, size_t destination_size,
    const char *parent, const char *name)
{
    int written = snprintf(destination, destination_size, "%s/%s", parent,
        name);

    return written >= 0 && (size_t)written < destination_size;
}

static int expect_rejected(const char *path)
{
    int fd = -1;

    if (msconnector_open_private_event_file(path, &fd)) {
        (void)close(fd);
        return 0;
    }
    return fd == -1;
}

static int create_permissive_fixture(const char *path)
{
    struct stat status;
    int fd = open(path, O_WRONLY | O_CREAT | O_TRUNC | O_CLOEXEC, 0600);
    int valid = fd >= 0 && fstat(fd, &status) == 0 &&
        S_ISREG(status.st_mode) && status.st_uid == geteuid() &&
        (status.st_mode & 0777) == 0600;

    if (!valid) {
        const int saved_errno = errno;
        if (fd >= 0) {
            (void)close(fd);
        }
        errno = saved_errno;
        return 0;
    }
    /* Deliberately make the isolated fixture group-readable so the production
     * opener's mode-repair path is exercised without process-wide umask or a
     * permissive create mode. */
    if (fchmod(fd, (status.st_mode & 0777) | S_IRGRP) != 0 ||
        fstat(fd, &status) != 0 || (status.st_mode & 0777) != 0640) {
        const int saved_errno = errno;
        (void)close(fd);
        errno = saved_errno;
        return 0;
    }
    if (close(fd) != 0) {
        return 0;
    }
    return 1;
}

static int check_regular_event_file(const char *path)
{
    struct stat status;
    int fd = -1;
    int valid = msconnector_open_private_event_file(path, &fd) &&
        fstat(fd, &status) == 0 && S_ISREG(status.st_mode) &&
        status.st_uid == geteuid() && (status.st_mode & 0777) == 0600 &&
        (fcntl(fd, F_GETFD) & FD_CLOEXEC) != 0 && write(fd, "{}\n", 3) == 3;

    if (fd >= 0 && close(fd) != 0) {
        valid = 0;
    }
    return valid;
}

static int check_repaired_event_file(const char *path)
{
    struct stat status;
    int fd = -1;
    int valid = msconnector_open_private_event_file(path, &fd) &&
        fstat(fd, &status) == 0 && (status.st_mode & 0777) == 0600 &&
        (fcntl(fd, F_GETFD) & FD_CLOEXEC) != 0;

    if (fd >= 0 && close(fd) != 0) {
        valid = 0;
    }
    return valid;
}

static int check_rejected_paths(const char *symlink_path,
    const char *ancestor_event_path, const char *fifo_path,
    const char *unsafe_path, const char *traversal_path,
    const char *private_directory)
{
    return expect_rejected(symlink_path) &&
        expect_rejected(ancestor_event_path) && expect_rejected(fifo_path) &&
        expect_rejected(unsafe_path) && expect_rejected(traversal_path) &&
        expect_rejected(private_directory);
}
#endif

int main(void)
{
#if defined(_WIN32)
    int fd = -1;

    if (msconnector_open_private_event_file("C:\\event.jsonl", &fd)) {
        return 1;
    }
    puts("private event-file Windows fail-closed control: passed");
    return 0;
#else
    const char *base = getenv("MSCONNECTOR_EVENT_FILE_TEST_ROOT");
    char root[TEST_PATH_SIZE];
    char private_directory[TEST_PATH_SIZE];
    char unsafe_directory[TEST_PATH_SIZE];
    char event_path[TEST_PATH_SIZE];
    char symlink_path[TEST_PATH_SIZE];
    char ancestor_symlink[TEST_PATH_SIZE];
    char ancestor_event_path[TEST_PATH_SIZE];
    char fifo_path[TEST_PATH_SIZE];
    char unsafe_path[TEST_PATH_SIZE];
    char traversal_path[TEST_PATH_SIZE];
    int result = 1;

    root[0] = '\0';
    private_directory[0] = '\0';
    unsafe_directory[0] = '\0';
    event_path[0] = '\0';
    symlink_path[0] = '\0';
    ancestor_symlink[0] = '\0';
    ancestor_event_path[0] = '\0';
    fifo_path[0] = '\0';
    unsafe_path[0] = '\0';
    traversal_path[0] = '\0';

    if (base == NULL || base[0] == '\0' ||
        strlen(base) + sizeof("/event-sink-XXXXXX") > sizeof(root)) {
        (void)fprintf(stderr,
            "MSCONNECTOR_EVENT_FILE_TEST_ROOT must be a bounded external root\n");
        return 2;
    }
    (void)snprintf(root, sizeof(root), "%s/event-sink-XXXXXX", base);
    if (mkdtemp(root) == NULL ||
        !join_path(private_directory, sizeof(private_directory), root,
            "private") ||
        !join_path(unsafe_directory, sizeof(unsafe_directory), root,
            "unsafe") ||
        !join_path(event_path, sizeof(event_path), private_directory,
            "events.jsonl") ||
        !join_path(symlink_path, sizeof(symlink_path), private_directory,
            "event-link.jsonl") ||
        !join_path(ancestor_symlink, sizeof(ancestor_symlink), root,
            "private-link") ||
        !join_path(ancestor_event_path, sizeof(ancestor_event_path),
            ancestor_symlink, "events.jsonl") ||
        !join_path(fifo_path, sizeof(fifo_path), private_directory,
            "event.fifo") ||
        !join_path(unsafe_path, sizeof(unsafe_path), unsafe_directory,
            "events.jsonl") ||
        !join_path(traversal_path, sizeof(traversal_path), private_directory,
            "../escape.jsonl")) {
        (void)fprintf(stderr, "private event-file test path setup failed\n");
        goto cleanup;
    }
    if (mkdir(private_directory, 0700) != 0 ||
        mkdir(unsafe_directory, 0700) != 0 ||
        chmod(unsafe_directory, 0770) != 0) {
        (void)fprintf(stderr, "private event-file test directory setup failed\n");
        goto cleanup;
    }

    if (!check_regular_event_file(event_path)) {
        (void)fprintf(stderr, "private regular event-file control failed\n");
        goto cleanup;
    }

    if (unlink(event_path) != 0 || !create_permissive_fixture(event_path) ||
        !check_repaired_event_file(event_path)) {
        (void)fprintf(stderr, "existing event-file permission repair failed\n");
        goto cleanup;
    }

    if (symlink("events.jsonl", symlink_path) != 0 ||
        symlink(private_directory, ancestor_symlink) != 0 ||
        mkfifo(fifo_path, 0600) != 0 || !check_rejected_paths(symlink_path,
            ancestor_event_path, fifo_path, unsafe_path, traversal_path,
            private_directory)) {
        (void)fprintf(stderr, "unsafe event-file path was accepted\n");
        goto cleanup;
    }

    result = 0;
    puts("private event-file descriptor controls: passed");

cleanup:
    if (symlink_path[0] != '\0') {
        (void)unlink(symlink_path);
    }
    if (ancestor_symlink[0] != '\0') {
        (void)unlink(ancestor_symlink);
    }
    if (fifo_path[0] != '\0') {
        (void)unlink(fifo_path);
    }
    if (event_path[0] != '\0') {
        (void)unlink(event_path);
    }
    if (unsafe_directory[0] != '\0') {
        (void)chmod(unsafe_directory, 0700);
        (void)rmdir(unsafe_directory);
    }
    if (private_directory[0] != '\0') {
        (void)rmdir(private_directory);
    }
    if (root[0] != '\0') {
        (void)rmdir(root);
    }
    return result;
#endif
}
