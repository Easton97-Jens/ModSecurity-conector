#define _GNU_SOURCE
#include "traefik_provenance.h"
#include "msconnector/memory.h"

#include <errno.h>
#include <fcntl.h>
#include <poll.h>
#include <pthread.h>
#include <stdatomic.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <strings.h>
#include <sys/random.h>
#include <sys/socket.h>
#include <sys/stat.h>
#include <sys/un.h>
#include <time.h>
#include <unistd.h>

/* MTP1 v1 is Traefik-only and deliberately separate from MRC1. One UDS
 * session owns one reservation. Three u16-length ASCII identifiers plus a
 * zero reuse byte are accepted. The result is status(1), random hex token(64).
 * No positive reuse assertion is supported without a host connection hook. */
#define PROVENANCE_SLOTS 128U
#define PROVENANCE_MAX_PAYLOAD (3U * (2U + 128U) + 1U)
#define PROVENANCE_TTL_MS 5000U
typedef struct reservation {
    int fd;
    int used;
    int consumed;
    int complete;
    int reply_status;
    int queried;
    char response_handle[MSCONNECTOR_RUNTIME_RESPONSE_COMPANION_HANDLE_SIZE];
    uint64_t expires;
    char token[65];
    msconnector_http_authorization_provenance_storage provenance;
} reservation;

static struct {
    pthread_mutex_t lock;
    pthread_t thread;
    atomic_int stopping;
    int running;
    int listener;
    char path[sizeof(((struct sockaddr_un *)0)->sun_path)];
    dev_t device;
    ino_t inode;
    msconnector_traefik_provenance_confirm confirm;
    void *confirm_userdata;
    reservation slots[PROVENANCE_SLOTS];
} server = {.lock = PTHREAD_MUTEX_INITIALIZER, .listener = -1};

static uint64_t now_ms(void) {
    struct timespec now;
    if (clock_gettime(CLOCK_MONOTONIC, &now) != 0) return 0U;
    return (uint64_t)now.tv_sec * 1000U + (uint64_t)now.tv_nsec / 1000000U;
}

static int transfer(int fd, unsigned char *data, size_t size, int writing) {
    const uint64_t deadline = now_ms() + 1000U;
    while (size != 0U) {
        uint64_t now = now_ms();
        struct pollfd item = {.fd = fd, .events = writing ? POLLOUT : POLLIN};
        ssize_t count;
        if (now == 0U || now >= deadline ||
            poll(&item, 1U, (int)(deadline - now)) != 1) return 0;
        count = writing ? send(fd, data, size, MSG_NOSIGNAL | MSG_DONTWAIT) :
            recv(fd, data, size, MSG_DONTWAIT);
        if (count < 0 && (errno == EINTR || errno == EAGAIN)) continue;
        if (count <= 0) return 0;
        data += (size_t)count;
        size -= (size_t)count;
    }
    return 1;
}

static int text_field(const unsigned char *payload, size_t size, size_t *offset,
    char output[MSCONNECTOR_RUNTIME_PROVENANCE_TEXT_SIZE]) {
    size_t length;
    if (*offset > size || size - *offset < 2U) return 0;
    length = (size_t)payload[*offset] * 256U + payload[*offset + 1U];
    *offset += 2U;
    if (length == 0U || length >= MSCONNECTOR_RUNTIME_PROVENANCE_TEXT_SIZE ||
        size - *offset < length) return 0;
    for (size_t i = 0U; i < length; ++i) {
        unsigned char c = payload[*offset + i];
        if (!((c >= 'a' && c <= 'z') || (c >= 'A' && c <= 'Z') ||
            (c >= '0' && c <= '9') || c == '_' || c == '-' || c == '.' || c == ':')) return 0;
    }
    memcpy(output, payload + *offset, length);
    output[length] = '\0';
    *offset += length;
    return 1;
}

static int read_reservation(int fd, msconnector_http_authorization_provenance_storage *provenance) {
    unsigned char header[12], payload[PROVENANCE_MAX_PAYLOAD];
    size_t size, offset = 0U;
    if (!transfer(fd, header, sizeof(header), 0) ||
        memcmp(header, "MTP1\1\1\0\0", 8U) != 0) return 0;
    size = (size_t)header[8] * 16777216U + (size_t)header[9] * 65536U +
        (size_t)header[10] * 256U + header[11];
    if (size > sizeof(payload) || !transfer(fd, payload, size, 0)) return 0;
    if (!text_field(payload, size, &offset, provenance->run_id) ||
        !text_field(payload, size, &offset, provenance->transport_case_id) ||
        !text_field(payload, size, &offset, provenance->connection_id) ||
        offset + 1U != size || payload[offset] != 0U) return 0;
    provenance->connection_reused = 0;
    return 1;
}

static int random_token(char token[65]) {
    unsigned char random[32];
    static const char hex[] = "0123456789abcdef";
    size_t offset = 0U;
    while (offset < sizeof(random)) {
        ssize_t count = getrandom(random + offset, sizeof(random) - offset, 0);
        if (count < 0 && errno == EINTR) continue;
        if (count <= 0) return 0;
        offset += (size_t)count;
    }
    for (size_t i = 0U; i < sizeof(random); ++i) {
        token[i * 2U] = hex[random[i] >> 4];
        token[i * 2U + 1U] = hex[random[i] & 15U];
    }
    token[64] = '\0';
    msconnector_secure_zero(random, sizeof(random));
    return 1;
}

static void discard(reservation *slot) {
    if (slot->used) close(slot->fd);
    msconnector_secure_zero(slot, sizeof(*slot));
}

static void accept_reservation(void) {
    struct ucred peer;
    socklen_t peer_size = sizeof(peer);
    msconnector_http_authorization_provenance_storage provenance = {0};
    unsigned char response[77] = {'M','T','P','1',1,128,0,0,0,0,0,65,0};
    char token[65];
    int fd = accept4(server.listener, NULL, NULL, SOCK_CLOEXEC | SOCK_NONBLOCK);
    if (fd < 0) return;
    if (getsockopt(fd, SOL_SOCKET, SO_PEERCRED, &peer, &peer_size) != 0 ||
        peer_size != sizeof(peer) || peer.uid != geteuid() || peer.gid != getegid() ||
        !read_reservation(fd, &provenance) || !random_token(token)) {
        close(fd); return;
    }
    pthread_mutex_lock(&server.lock);
    reservation *slot = NULL;
    for (size_t i = 0U; i < PROVENANCE_SLOTS; ++i)
        if (!server.slots[i].used && slot == NULL) slot = &server.slots[i];
    if (slot != NULL) {
        slot->fd = fd;
        slot->used = 1;
        slot->expires = now_ms() + PROVENANCE_TTL_MS;
        slot->provenance = provenance;
        memcpy(slot->token, token, sizeof(token));
        memcpy(response + 13U, token, 64U);
        if (!transfer(fd, response, sizeof(response), 1)) discard(slot);
    } else close(fd);
    pthread_mutex_unlock(&server.lock);
    msconnector_secure_zero(&provenance, sizeof(provenance));
    msconnector_secure_zero(token, sizeof(token));
    msconnector_secure_zero(response, sizeof(response));
}

static void *serve(void *unused) {
    (void)unused;
    while (!atomic_load(&server.stopping)) {
        struct pollfd listener = {.fd = server.listener, .events = POLLIN};
        if (poll(&listener, 1U, 100) == 1 && (listener.revents & POLLIN)) accept_reservation();
        pthread_mutex_lock(&server.lock);
        uint64_t now = now_ms();
        for (size_t i = 0U; i < PROVENANCE_SLOTS; ++i) {
            reservation *slot = &server.slots[i];
            unsigned char byte;
            ssize_t count;
            if (!slot->used) continue;
            count = recv(slot->fd, &byte, 1U, MSG_PEEK | MSG_DONTWAIT);
            if (count > 0 && now != 0U && now < slot->expires &&
                slot->consumed && slot->complete && !slot->queried) {
                unsigned char query[12], response[79] = {'M','T','P','1',1,128,0,0,0,0,0,67,0};
                if (!transfer(slot->fd, query, sizeof(query), 0) ||
                    memcmp(query, "MTP1\1\2\0\0\0\0\0\0", sizeof(query)) != 0) {
                    discard(slot); continue;
                }
                /* Lock order is MTP1 reservation -> Common registry. The
                 * Common callback never enters MTP1 or performs native work.
                 * A terminal Deny has no companion capability to refresh. */
                if (slot->response_handle[0] != '\0') {
                    msconnector_error error;
                    msconnector_error_init(&error);
                    if (atomic_load(&server.stopping) || slot->reply_status < 200 ||
                        slot->reply_status >= 300 || server.confirm == NULL ||
                        !server.confirm(server.confirm_userdata,
                            slot->response_handle, &error)) {
                        discard(slot); continue;
                    }
                }
                response[13] = (unsigned char)(slot->reply_status >> 8);
                response[14] = (unsigned char)slot->reply_status;
                memcpy(response + 15U, slot->response_handle, 64U);
                if (!transfer(slot->fd, response, sizeof(response), 1)) {
                    discard(slot); continue;
                }
                slot->queried = 1;
                continue;
            }
            /* A query before completion or any second query is ambiguous.
             * Closed or expired sessions invalidate remaining capability. */
            if (now == 0U || now >= slot->expires || count >= 0 ||
                (errno != EAGAIN && errno != EWOULDBLOCK && errno != EINTR)) discard(slot);
        }
        pthread_mutex_unlock(&server.lock);
    }
    return NULL;
}

static int safe_parent(const char *path) {
    char parent[sizeof(server.path)];
    char canonical[4096];
    struct stat info;
    if (path == NULL || path[0] != '/' || strlen(path) >= sizeof(parent)) return 0;
    strcpy(parent, path);
    char *separator = strrchr(parent, '/');
    if (separator == parent) return 0;
    *separator = '\0';
    return realpath(parent, canonical) != NULL && strcmp(parent, canonical) == 0 &&
        lstat(parent, &info) == 0 && S_ISDIR(info.st_mode) && info.st_uid == geteuid() &&
        (info.st_mode & 0777U) == 0700U &&
        msconnector_runtime_private_directory_ancestors_are_safe(parent);
}

int msconnector_traefik_provenance_start(const char *path) {
    return msconnector_traefik_provenance_start_with_confirmation(path, NULL, NULL);
}

int msconnector_traefik_provenance_start_with_confirmation(const char *path,
    msconnector_traefik_provenance_confirm confirm, void *userdata) {
    struct sockaddr_un address = {.sun_family = AF_UNIX};
    struct stat info;
    if (server.running || !safe_parent(path) || lstat(path, &info) == 0 || errno != ENOENT) return 0;
    server.confirm = confirm;
    server.confirm_userdata = userdata;
    server.listener = socket(AF_UNIX, SOCK_STREAM | SOCK_CLOEXEC | SOCK_NONBLOCK, 0);
    if (server.listener < 0) return 0;
    strcpy(address.sun_path, path);
    if (bind(server.listener, (struct sockaddr *)&address, sizeof(address)) != 0) {
        close(server.listener); server.listener = -1; return 0;
    }
    /* The mode-0700 parent prevents a race before chmod. Never unlink an
     * existing pathname or an inode replaced after this bind. */
    if (lstat(path, &info) != 0 || !S_ISSOCK(info.st_mode) || info.st_uid != geteuid()) {
        close(server.listener); server.listener = -1; return 0;
    }
    strcpy(server.path, path); server.device = info.st_dev; server.inode = info.st_ino;
    if (chmod(path, 0600U) != 0 || listen(server.listener, PROVENANCE_SLOTS) != 0) {
        msconnector_traefik_provenance_stop(); return 0;
    }
    atomic_store(&server.stopping, 0);
    if (pthread_create(&server.thread, NULL, serve, NULL) != 0) {
        msconnector_traefik_provenance_stop(); return 0;
    }
    server.running = 1;
    return 1;
}

void msconnector_traefik_provenance_stop(void) {
    struct stat info;
    atomic_store(&server.stopping, 1);
    if (server.running) pthread_join(server.thread, NULL);
    server.running = 0;
    if (server.listener >= 0) close(server.listener);
    server.listener = -1;
    pthread_mutex_lock(&server.lock);
    for (size_t i = 0U; i < PROVENANCE_SLOTS; ++i) discard(&server.slots[i]);
    pthread_mutex_unlock(&server.lock);
    if (server.path[0] != '\0' && lstat(server.path, &info) == 0 &&
        S_ISSOCK(info.st_mode) && info.st_dev == server.device && info.st_ino == server.inode)
        unlink(server.path);
    server.path[0] = '\0';
    server.confirm = NULL;
    server.confirm_userdata = NULL;
}

int msconnector_traefik_provenance_claim(void *unused,
    const msconnector_request *request,
    msconnector_http_authorization_provenance_storage *storage,
    msconnector_error *error) {
    const msconnector_header *header = NULL;
    int success = 0;
    (void)unused;
    if (request == NULL || storage == NULL ||
        request->header_count > MSCONNECTOR_MAX_HEADER_COUNT ||
        (request->header_count != 0U && request->headers == NULL)) return 0;
    memset(storage, 0, sizeof(*storage));
    for (size_t i = 0U; i < request->header_count; ++i) {
        const msconnector_header *candidate = &request->headers[i];
        if (candidate->name != NULL && candidate->name_size == sizeof(MSCONNECTOR_TRAEFIK_PROVENANCE_HEADER)-1U &&
            strncasecmp(candidate->name, MSCONNECTOR_TRAEFIK_PROVENANCE_HEADER,
                candidate->name_size) == 0) {
            if (header != NULL) goto failed;
            header = candidate;
        }
    }
    if (header == NULL || header->value == NULL || header->value_size != 64U) goto failed;
    pthread_mutex_lock(&server.lock);
    uint64_t now = now_ms();
    for (size_t i = 0U; i < PROVENANCE_SLOTS; ++i) {
        reservation *slot = &server.slots[i];
        if (slot->used && !slot->consumed && now != 0U && now < slot->expires &&
            memcmp(slot->token, header->value, 64U) == 0) {
            unsigned char extra;
            ssize_t count = recv(slot->fd, &extra, 1U, MSG_PEEK | MSG_DONTWAIT);
            if (count < 0 && (errno == EAGAIN || errno == EWOULDBLOCK)) {
                *storage = slot->provenance;
                slot->consumed = 1;
                msconnector_secure_zero(&slot->provenance, sizeof(slot->provenance));
                success = 1;
            } else discard(slot);
            break;
        }
    }
    pthread_mutex_unlock(&server.lock);
failed:
    if (!success) msconnector_error_set(error, MSCONNECTOR_ERROR_HOST_API_FAILURE,
        "trusted private reservation required", "traefik_provenance");
    return success;
}

int msconnector_traefik_provenance_complete(void *unused,
    const msconnector_request *request, int status, const char *response_handle,
    msconnector_error *error) {
    const msconnector_header *header = NULL;
    int success = 0;
    (void)unused;
    if (request == NULL || request->header_count > MSCONNECTOR_MAX_HEADER_COUNT ||
        (request->header_count != 0U && request->headers == NULL) || status < 100 || status > 599 ||
        (response_handle != NULL && strlen(response_handle) != 64U)) goto failed;
    for (size_t i = 0U; i < request->header_count; ++i) {
        const msconnector_header *candidate = &request->headers[i];
        if (candidate->name != NULL && candidate->name_size == sizeof(MSCONNECTOR_TRAEFIK_PROVENANCE_HEADER)-1U &&
            strncasecmp(candidate->name, MSCONNECTOR_TRAEFIK_PROVENANCE_HEADER,
                candidate->name_size) == 0) {
            if (header != NULL) goto failed;
            header = candidate;
        }
    }
    if (header == NULL || header->value == NULL || header->value_size != 64U) goto failed;
    pthread_mutex_lock(&server.lock);
    uint64_t now = now_ms();
    for (size_t i = 0U; i < PROVENANCE_SLOTS; ++i) {
        reservation *slot = &server.slots[i];
        if (slot->used && slot->consumed && !slot->complete && now != 0U &&
            now < slot->expires && memcmp(slot->token, header->value, 64U) == 0) {
            unsigned char extra;
            ssize_t count = recv(slot->fd, &extra, 1U, MSG_PEEK | MSG_DONTWAIT);
            if (count >= 0 || (errno != EAGAIN && errno != EWOULDBLOCK)) {
                discard(slot); break;
            }
            slot->reply_status = status;
            if (response_handle != NULL) memcpy(slot->response_handle, response_handle, 65U);
            slot->complete = 1;
            success = 1;
            break;
        }
    }
    pthread_mutex_unlock(&server.lock);
failed:
    if (!success) msconnector_error_set(error, MSCONNECTOR_ERROR_HOST_API_FAILURE,
        "trusted private reply binding failed", "traefik_provenance");
    return success;
}
