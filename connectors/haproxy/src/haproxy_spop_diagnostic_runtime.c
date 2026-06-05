#define _POSIX_C_SOURCE 200809L

#include <arpa/inet.h>
#include <errno.h>
#include <netinet/in.h>
#include <signal.h>
#include <stdarg.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/socket.h>
#include <sys/stat.h>
#include <sys/time.h>
#include <sys/types.h>
#include <sys/wait.h>
#include <time.h>
#include <unistd.h>

#define SPOP_FRAME_MAX 16384U
#define SPOP_MIN_FRAME_SIZE 256U
#define SPOP_FIN_FLAG 0x00000001U

#define SPOP_FRM_HAPROXY_HELLO 1U
#define SPOP_FRM_HAPROXY_DISCONNECT 2U
#define SPOP_FRM_NOTIFY 3U
#define SPOP_FRM_AGENT_HELLO 101U
#define SPOP_FRM_AGENT_DISCONNECT 102U
#define SPOP_FRM_ACK 103U

#define SPOP_DATA_BOOL 1U
#define SPOP_DATA_UINT32 3U
#define SPOP_DATA_STR 8U
#define SPOP_BOOL_TRUE 0x10U

typedef struct spop_buffer {
    unsigned char data[SPOP_FRAME_MAX];
    size_t len;
} spop_buffer;

typedef struct spop_frame {
    unsigned int type;
    uint32_t flags;
    uint64_t stream_id;
    uint64_t frame_id;
    unsigned char payload[SPOP_FRAME_MAX];
    size_t payload_len;
} spop_frame;

typedef struct hello_info {
    unsigned int max_frame_size;
    int has_supported_versions;
    int has_max_frame_size;
    int has_capabilities;
    int healthcheck;
} hello_info;

static volatile sig_atomic_t stop_requested = 0;

static void on_signal(int signum) {
    (void)signum;
    stop_requested = 1;
}

static void log_line(FILE *log, const char *fmt, ...) {
    va_list args;
    time_t now = time(0);

    if (log == 0) {
        return;
    }
    fprintf(log, "%ld ", (long)now);
    va_start(args, fmt);
    vfprintf(log, fmt, args);
    va_end(args);
    fputc('\n', log);
    fflush(log);
}

static int mkdir_p(const char *path) {
    char tmp[4096];
    char *p;
    size_t len;

    if (path == 0 || path[0] == '\0') {
        return -1;
    }
    len = strlen(path);
    if (len >= sizeof(tmp)) {
        return -1;
    }
    memcpy(tmp, path, len + 1);
    if (tmp[len - 1] == '/') {
        tmp[len - 1] = '\0';
    }
    for (p = tmp + 1; *p != '\0'; ++p) {
        if (*p == '/') {
            *p = '\0';
            if (mkdir(tmp, 0755) != 0 && errno != EEXIST) {
                return -1;
            }
            *p = '/';
        }
    }
    if (mkdir(tmp, 0755) != 0 && errno != EEXIST) {
        return -1;
    }
    return 0;
}

static int dirname_to_buffer(const char *path, char *out, size_t out_len) {
    const char *slash;
    size_t len;

    slash = strrchr(path, '/');
    if (slash == 0) {
        if (out_len < 2) {
            return -1;
        }
        strcpy(out, ".");
        return 0;
    }
    len = (size_t)(slash - path);
    if (len == 0) {
        len = 1;
    }
    if (len + 1 > out_len) {
        return -1;
    }
    memcpy(out, path, len);
    out[len] = '\0';
    return 0;
}

static int write_text_file(const char *path, const char *fmt, ...) {
    char dir[4096];
    FILE *file;
    va_list args;

    if (dirname_to_buffer(path, dir, sizeof(dir)) != 0 || mkdir_p(dir) != 0) {
        return -1;
    }
    file = fopen(path, "w");
    if (file == 0) {
        return -1;
    }
    va_start(args, fmt);
    vfprintf(file, fmt, args);
    va_end(args);
    if (fclose(file) != 0) {
        return -1;
    }
    return 0;
}

static int read_full(int fd, void *buf, size_t len) {
    unsigned char *p = (unsigned char *)buf;
    while (len > 0) {
        ssize_t rc = read(fd, p, len);
        if (rc == 0) {
            return -1;
        }
        if (rc < 0) {
            if (errno == EINTR) {
                continue;
            }
            return -1;
        }
        p += rc;
        len -= (size_t)rc;
    }
    return 0;
}

static int write_full(int fd, const void *buf, size_t len) {
    const unsigned char *p = (const unsigned char *)buf;
    while (len > 0) {
        ssize_t rc = write(fd, p, len);
        if (rc < 0) {
            if (errno == EINTR) {
                continue;
            }
            return -1;
        }
        p += rc;
        len -= (size_t)rc;
    }
    return 0;
}

static int append_byte(spop_buffer *buf, unsigned int value) {
    if (buf->len >= sizeof(buf->data)) {
        return -1;
    }
    buf->data[buf->len++] = (unsigned char)value;
    return 0;
}

static int append_bytes(spop_buffer *buf, const void *data, size_t len) {
    if (len > sizeof(buf->data) - buf->len) {
        return -1;
    }
    memcpy(buf->data + buf->len, data, len);
    buf->len += len;
    return 0;
}

static int append_uint32(spop_buffer *buf, uint32_t value) {
    uint32_t net = htonl(value);
    return append_bytes(buf, &net, sizeof(net));
}

static int append_varint(spop_buffer *buf, uint64_t value) {
    if (value < 240U) {
        return append_byte(buf, (unsigned int)value);
    }
    if (append_byte(buf, ((unsigned int)value & 0xffU) | 240U) != 0) {
        return -1;
    }
    value = (value - 240U) >> 4;
    while (value >= 128U) {
        if (append_byte(buf, ((unsigned int)value & 0xffU) | 128U) != 0) {
            return -1;
        }
        value = (value - 128U) >> 7;
    }
    return append_byte(buf, (unsigned int)value);
}

static int read_varint(const unsigned char *data, size_t len, size_t *pos, uint64_t *value) {
    unsigned int shift;

    if (*pos >= len) {
        return -1;
    }
    *value = data[(*pos)++];
    if (*value < 240U) {
        return 0;
    }
    shift = 4U;
    do {
        unsigned int byte;
        if (*pos >= len) {
            return -1;
        }
        byte = data[(*pos)++];
        *value += (uint64_t)byte << shift;
        shift += 7U;
        if (byte < 128U) {
            break;
        }
    } while (shift < 64U);
    return 0;
}

static int append_string(spop_buffer *buf, const char *value) {
    size_t len = strlen(value);
    if (append_varint(buf, len) != 0) {
        return -1;
    }
    return append_bytes(buf, value, len);
}

static int append_typed_string(spop_buffer *buf, const char *value) {
    if (append_byte(buf, SPOP_DATA_STR) != 0) {
        return -1;
    }
    return append_string(buf, value);
}

static int append_typed_uint32(spop_buffer *buf, unsigned int value) {
    if (append_byte(buf, SPOP_DATA_UINT32) != 0) {
        return -1;
    }
    return append_varint(buf, value);
}

static int append_typed_bool(spop_buffer *buf, int value) {
    return append_byte(buf, SPOP_DATA_BOOL | (value ? SPOP_BOOL_TRUE : 0U));
}

static int append_kv_string(spop_buffer *buf, const char *key, const char *value) {
    return append_string(buf, key) == 0 && append_typed_string(buf, value) == 0 ? 0 : -1;
}

static int append_kv_uint32(spop_buffer *buf, const char *key, unsigned int value) {
    return append_string(buf, key) == 0 && append_typed_uint32(buf, value) == 0 ? 0 : -1;
}

static int append_kv_bool(spop_buffer *buf, const char *key, int value) {
    return append_string(buf, key) == 0 && append_typed_bool(buf, value) == 0 ? 0 : -1;
}

static int read_string_ref(const unsigned char *data, size_t len, size_t *pos, const unsigned char **str, size_t *str_len) {
    uint64_t value_len;

    if (read_varint(data, len, pos, &value_len) != 0 || value_len > len - *pos) {
        return -1;
    }
    *str = data + *pos;
    *str_len = (size_t)value_len;
    *pos += (size_t)value_len;
    return 0;
}

static int key_equals(const unsigned char *key, size_t key_len, const char *expected) {
    size_t expected_len = strlen(expected);
    return key_len == expected_len && memcmp(key, expected, expected_len) == 0;
}

static int contains_bytes(const unsigned char *value, size_t value_len, const char *needle) {
    size_t needle_len = strlen(needle);
    size_t i;

    if (needle_len == 0 || value_len < needle_len) {
        return 0;
    }
    for (i = 0; i <= value_len - needle_len; ++i) {
        if (memcmp(value + i, needle, needle_len) == 0) {
            return 1;
        }
    }
    return 0;
}

static int skip_typed_data(const unsigned char *data, size_t len, size_t *pos) {
    unsigned int type;
    uint64_t n;

    if (*pos >= len) {
        return -1;
    }
    type = data[(*pos)++] & 0x0fU;
    switch (type) {
        case SPOP_DATA_BOOL:
            return 0;
        case 2U:
        case SPOP_DATA_UINT32:
        case 4U:
        case 5U:
            return read_varint(data, len, pos, &n);
        case 6U:
            if (len - *pos < 4U) {
                return -1;
            }
            *pos += 4U;
            return 0;
        case 7U:
            if (len - *pos < 16U) {
                return -1;
            }
            *pos += 16U;
            return 0;
        case SPOP_DATA_STR:
        case 9U:
            if (read_varint(data, len, pos, &n) != 0 || n > len - *pos) {
                return -1;
            }
            *pos += (size_t)n;
            return 0;
        case 0U:
            return 0;
        default:
            return -1;
    }
}

static int parse_hello_payload(const unsigned char *data, size_t len, hello_info *hello) {
    size_t pos = 0;

    memset(hello, 0, sizeof(*hello));
    hello->max_frame_size = SPOP_FRAME_MAX;

    while (pos < len) {
        const unsigned char *key;
        size_t key_len;
        unsigned int type;
        size_t value_pos;

        if (read_string_ref(data, len, &pos, &key, &key_len) != 0 || pos >= len) {
            return -1;
        }
        value_pos = pos;
        type = data[pos++] & 0x0fU;
        if (key_equals(key, key_len, "supported-versions") && type == SPOP_DATA_STR) {
            const unsigned char *value;
            size_t value_len;
            if (read_string_ref(data, len, &pos, &value, &value_len) != 0) {
                return -1;
            }
            if (contains_bytes(value, value_len, "1.") || contains_bytes(value, value_len, "2.")) {
                hello->has_supported_versions = 1;
            }
            continue;
        }
        if (key_equals(key, key_len, "max-frame-size") && type == SPOP_DATA_UINT32) {
            uint64_t value;
            if (read_varint(data, len, &pos, &value) != 0 || value < SPOP_MIN_FRAME_SIZE) {
                return -1;
            }
            hello->max_frame_size = value < SPOP_FRAME_MAX ? (unsigned int)value : SPOP_FRAME_MAX;
            hello->has_max_frame_size = 1;
            continue;
        }
        if (key_equals(key, key_len, "capabilities") && type == SPOP_DATA_STR) {
            const unsigned char *value;
            size_t value_len;
            if (read_string_ref(data, len, &pos, &value, &value_len) != 0) {
                return -1;
            }
            hello->has_capabilities = 1;
            continue;
        }
        if (key_equals(key, key_len, "healthcheck") && type == SPOP_DATA_BOOL) {
            hello->healthcheck = (data[value_pos] & SPOP_BOOL_TRUE) != 0;
            continue;
        }
        pos = value_pos;
        if (skip_typed_data(data, len, &pos) != 0) {
            return -1;
        }
    }
    return hello->has_supported_versions && hello->has_max_frame_size && hello->has_capabilities ? 0 : -1;
}

static int build_frame(unsigned int type, uint64_t stream_id, uint64_t frame_id, const spop_buffer *payload, spop_buffer *frame) {
    frame->len = 0;
    if (append_byte(frame, type) != 0 ||
        append_uint32(frame, SPOP_FIN_FLAG) != 0 ||
        append_varint(frame, stream_id) != 0 ||
        append_varint(frame, frame_id) != 0) {
        return -1;
    }
    if (payload != 0 && append_bytes(frame, payload->data, payload->len) != 0) {
        return -1;
    }
    return 0;
}

static int send_frame(int fd, unsigned int type, uint64_t stream_id, uint64_t frame_id, const spop_buffer *payload) {
    spop_buffer frame;
    uint32_t net_len;

    if (build_frame(type, stream_id, frame_id, payload, &frame) != 0) {
        return -1;
    }
    net_len = htonl((uint32_t)frame.len);
    return write_full(fd, &net_len, sizeof(net_len)) == 0 && write_full(fd, frame.data, frame.len) == 0 ? 0 : -1;
}

static int recv_frame(int fd, spop_frame *frame) {
    uint32_t net_len;
    uint32_t len;
    unsigned char data[SPOP_FRAME_MAX];
    size_t pos;

    if (read_full(fd, &net_len, sizeof(net_len)) != 0) {
        return -1;
    }
    len = ntohl(net_len);
    if (len == 0 || len > SPOP_FRAME_MAX || read_full(fd, data, len) != 0) {
        return -1;
    }
    pos = 0;
    frame->type = data[pos++];
    if (len - pos < 4U) {
        return -1;
    }
    frame->flags = ((uint32_t)data[pos] << 24) | ((uint32_t)data[pos + 1] << 16) | ((uint32_t)data[pos + 2] << 8) | data[pos + 3];
    pos += 4U;
    if (read_varint(data, len, &pos, &frame->stream_id) != 0 ||
        read_varint(data, len, &pos, &frame->frame_id) != 0 ||
        len - pos > sizeof(frame->payload)) {
        return -1;
    }
    frame->payload_len = len - pos;
    memcpy(frame->payload, data + pos, frame->payload_len);
    return 0;
}

static int send_agent_hello(int fd, unsigned int max_frame_size) {
    spop_buffer payload;

    payload.len = 0;
    if (append_kv_string(&payload, "version", "1.2") != 0 ||
        append_kv_uint32(&payload, "max-frame-size", max_frame_size) != 0 ||
        append_kv_string(&payload, "capabilities", "") != 0) {
        return -1;
    }
    return send_frame(fd, SPOP_FRM_AGENT_HELLO, 0, 0, &payload);
}

static int send_agent_disconnect(int fd, unsigned int code, const char *message) {
    spop_buffer payload;

    payload.len = 0;
    if (append_kv_uint32(&payload, "status-code", code) != 0 ||
        append_kv_string(&payload, "message", message) != 0) {
        return -1;
    }
    return send_frame(fd, SPOP_FRM_AGENT_DISCONNECT, 0, 0, &payload);
}

static int send_haproxy_hello(int fd, int healthcheck) {
    spop_buffer payload;

    payload.len = 0;
    if (append_kv_string(&payload, "supported-versions", "1.2") != 0 ||
        append_kv_uint32(&payload, "max-frame-size", SPOP_FRAME_MAX) != 0 ||
        append_kv_string(&payload, "capabilities", "") != 0 ||
        append_kv_bool(&payload, "healthcheck", healthcheck) != 0) {
        return -1;
    }
    return send_frame(fd, SPOP_FRM_HAPROXY_HELLO, 0, 0, &payload);
}

static int handle_connection(int fd, FILE *log) {
    spop_frame frame;
    hello_info hello;

    if (recv_frame(fd, &frame) != 0 || frame.type != SPOP_FRM_HAPROXY_HELLO ||
        parse_hello_payload(frame.payload, frame.payload_len, &hello) != 0) {
        log_line(log, "connection rejected during HELLO");
        send_agent_disconnect(fd, 4, "invalid hello");
        return -1;
    }
    log_line(log, "HELLO received healthcheck=%d max_frame_size=%u", hello.healthcheck, hello.max_frame_size);
    if (send_agent_hello(fd, hello.max_frame_size) != 0) {
        return -1;
    }
    if (hello.healthcheck) {
        log_line(log, "healthcheck completed");
        return 0;
    }

    while (!stop_requested) {
        if (recv_frame(fd, &frame) != 0) {
            return 0;
        }
        if (frame.type == SPOP_FRM_NOTIFY) {
            spop_buffer empty;
            empty.len = 0;
            log_line(log, "NOTIFY received stream=%llu frame=%llu", (unsigned long long)frame.stream_id, (unsigned long long)frame.frame_id);
            if (send_frame(fd, SPOP_FRM_ACK, frame.stream_id, frame.frame_id, &empty) != 0) {
                return -1;
            }
            continue;
        }
        if (frame.type == SPOP_FRM_HAPROXY_DISCONNECT) {
            log_line(log, "DISCONNECT received");
            send_agent_disconnect(fd, 0, "normal");
            return 0;
        }
        log_line(log, "unsupported frame type=%u", frame.type);
        send_agent_disconnect(fd, 4, "unsupported frame");
        return -1;
    }
    return 0;
}

static int bind_localhost(const char *host, unsigned int port, unsigned int *bound_port) {
    int fd;
    int yes = 1;
    struct sockaddr_in addr;
    socklen_t addr_len = sizeof(addr);

    if (strcmp(host, "127.0.0.1") != 0) {
        return -1;
    }
    fd = socket(AF_INET, SOCK_STREAM, 0);
    if (fd < 0) {
        return -1;
    }
    setsockopt(fd, SOL_SOCKET, SO_REUSEADDR, &yes, sizeof(yes));
    memset(&addr, 0, sizeof(addr));
    addr.sin_family = AF_INET;
    addr.sin_port = htons((uint16_t)port);
    if (inet_pton(AF_INET, host, &addr.sin_addr) != 1 ||
        bind(fd, (struct sockaddr *)&addr, sizeof(addr)) != 0 ||
        listen(fd, 16) != 0 ||
        getsockname(fd, (struct sockaddr *)&addr, &addr_len) != 0) {
        close(fd);
        return -1;
    }
    *bound_port = ntohs(addr.sin_port);
    return fd;
}

static int connect_localhost(unsigned int port) {
    int fd;
    struct sockaddr_in addr;
    struct timeval tv;

    fd = socket(AF_INET, SOCK_STREAM, 0);
    if (fd < 0) {
        return -1;
    }
    tv.tv_sec = 3;
    tv.tv_usec = 0;
    setsockopt(fd, SOL_SOCKET, SO_RCVTIMEO, &tv, sizeof(tv));
    setsockopt(fd, SOL_SOCKET, SO_SNDTIMEO, &tv, sizeof(tv));
    memset(&addr, 0, sizeof(addr));
    addr.sin_family = AF_INET;
    addr.sin_port = htons((uint16_t)port);
    if (inet_pton(AF_INET, "127.0.0.1", &addr.sin_addr) != 1 ||
        connect(fd, (struct sockaddr *)&addr, sizeof(addr)) != 0) {
        close(fd);
        return -1;
    }
    return fd;
}

static int accept_loop(int listen_fd, FILE *log, int max_connections) {
    int handled = 0;

    signal(SIGTERM, on_signal);
    signal(SIGINT, on_signal);
    while (!stop_requested && (max_connections <= 0 || handled < max_connections)) {
        int fd = accept(listen_fd, 0, 0);
        if (fd < 0) {
            if (errno == EINTR) {
                continue;
            }
            log_line(log, "accept failed errno=%d", errno);
            return 1;
        }
        handle_connection(fd, log);
        close(fd);
        handled++;
    }
    return 0;
}

static int client_expect_frame(int fd, unsigned int type, uint64_t stream_id, uint64_t frame_id) {
    spop_frame frame;
    if (recv_frame(fd, &frame) != 0 || frame.type != type ||
        frame.stream_id != stream_id || frame.frame_id != frame_id) {
        return -1;
    }
    return 0;
}

static int run_client_self_test(unsigned int port, FILE *log) {
    int fd;
    spop_buffer empty;

    fd = connect_localhost(port);
    if (fd < 0) {
        return -1;
    }
    if (send_haproxy_hello(fd, 1) != 0 ||
        client_expect_frame(fd, SPOP_FRM_AGENT_HELLO, 0, 0) != 0) {
        close(fd);
        return -1;
    }
    log_line(log, "client healthcheck handshake PASS");
    close(fd);

    fd = connect_localhost(port);
    if (fd < 0) {
        return -1;
    }
    empty.len = 0;
    if (send_haproxy_hello(fd, 0) != 0 ||
        client_expect_frame(fd, SPOP_FRM_AGENT_HELLO, 0, 0) != 0 ||
        send_frame(fd, SPOP_FRM_NOTIFY, 1, 1, &empty) != 0 ||
        client_expect_frame(fd, SPOP_FRM_ACK, 1, 1) != 0 ||
        send_frame(fd, SPOP_FRM_HAPROXY_DISCONNECT, 0, 0, &empty) != 0 ||
        client_expect_frame(fd, SPOP_FRM_AGENT_DISCONNECT, 0, 0) != 0) {
        close(fd);
        return -1;
    }
    log_line(log, "client notify ack disconnect PASS");
    close(fd);
    return 0;
}

static int run_self_test(const char *tmp_root, const char *log_root) {
    char log_path[4096];
    char ready_path[4096];
    char pid_path[4096];
    char port_path[4096];
    unsigned int port = 0;
    int listen_fd;
    pid_t child;
    int status;
    FILE *log;

    if (mkdir_p(tmp_root) != 0 || mkdir_p(log_root) != 0) {
        fprintf(stderr, "failed to create tmp/log roots\n");
        return 77;
    }
    snprintf(log_path, sizeof(log_path), "%s/spop-diagnostic-runtime.log", log_root);
    snprintf(ready_path, sizeof(ready_path), "%s/spop-diagnostic-runtime.ready", tmp_root);
    snprintf(pid_path, sizeof(pid_path), "%s/spop-diagnostic-runtime.pid", tmp_root);
    snprintf(port_path, sizeof(port_path), "%s/spop-diagnostic-runtime.port", tmp_root);
    log = fopen(log_path, "w");
    if (log == 0) {
        fprintf(stderr, "failed to open log: %s\n", log_path);
        return 77;
    }
    listen_fd = bind_localhost("127.0.0.1", 0, &port);
    if (listen_fd < 0) {
        fprintf(stderr, "failed to bind diagnostic SPOP listener\n");
        fclose(log);
        return 77;
    }
    write_text_file(port_path, "%u\n", port);
    child = fork();
    if (child < 0) {
        close(listen_fd);
        fclose(log);
        return 77;
    }
    if (child == 0) {
        write_text_file(pid_path, "%ld\n", (long)getpid());
        write_text_file(ready_path, "ready\n");
        exit(accept_loop(listen_fd, log, 2));
    }
    close(listen_fd);
    if (run_client_self_test(port, log) != 0) {
        kill(child, SIGTERM);
        waitpid(child, &status, 0);
        fclose(log);
        fprintf(stderr, "diagnostic SPOP runtime self-test failed\n");
        return 1;
    }
    waitpid(child, &status, 0);
    fclose(log);
    if (!WIFEXITED(status) || WEXITSTATUS(status) != 0) {
        fprintf(stderr, "diagnostic SPOP runtime child failed\n");
        return 1;
    }
    printf("haproxy_spop_diagnostic_runtime_self_test: PASS\n");
    printf("scope: minimal diagnostic SPOP handshake subset; no ModSecurity binding, no CRS, no RESPONSE_BODY\n");
    printf("log: %s\n", log_path);
    printf("port_file: %s\n", port_path);
    return 0;
}

static int run_server(const char *host, unsigned int port, const char *ready_file, const char *pid_file, const char *port_file, const char *log_file) {
    int listen_fd;
    unsigned int bound_port;
    FILE *log;

    log = fopen(log_file, "a");
    if (log == 0) {
        fprintf(stderr, "failed to open log: %s\n", log_file);
        return 77;
    }
    listen_fd = bind_localhost(host, port, &bound_port);
    if (listen_fd < 0) {
        fprintf(stderr, "failed to bind %s:%u\n", host, port);
        fclose(log);
        return 77;
    }
    if ((pid_file != 0 && write_text_file(pid_file, "%ld\n", (long)getpid()) != 0) ||
        (port_file != 0 && write_text_file(port_file, "%u\n", bound_port) != 0) ||
        (ready_file != 0 && write_text_file(ready_file, "ready\n") != 0)) {
        close(listen_fd);
        fclose(log);
        return 77;
    }
    log_line(log, "minimal diagnostic SPOP handshake subset listening on %s:%u", host, bound_port);
    accept_loop(listen_fd, log, 0);
    close(listen_fd);
    fclose(log);
    return 0;
}

static void print_usage(const char *program) {
    fprintf(stderr, "usage: %s --describe|--runtime-self-test --tmp-root PATH --log-root PATH|--serve --host 127.0.0.1 --port PORT --ready-file PATH --pid-file PATH --port-file PATH --log-file PATH\n", program);
}

int main(int argc, char **argv) {
    if (argc == 2 && strcmp(argv[1], "--describe") == 0) {
        printf("HAProxy minimal diagnostic SPOP handshake subset\n");
        printf("limitations: no full SPOA agent implementation, no ModSecurity binding, no CRS loading, no RESPONSE_BODY verification\n");
        return 0;
    }

    if (argc >= 2 && strcmp(argv[1], "--runtime-self-test") == 0) {
        const char *tmp_root = 0;
        const char *log_root = 0;
        int i;
        for (i = 2; i < argc; ++i) {
            if (strcmp(argv[i], "--tmp-root") == 0 && i + 1 < argc) {
                tmp_root = argv[++i];
            } else if (strcmp(argv[i], "--log-root") == 0 && i + 1 < argc) {
                log_root = argv[++i];
            } else {
                print_usage(argv[0]);
                return 2;
            }
        }
        if (tmp_root == 0 || log_root == 0) {
            print_usage(argv[0]);
            return 2;
        }
        return run_self_test(tmp_root, log_root);
    }

    if (argc >= 2 && strcmp(argv[1], "--serve") == 0) {
        const char *host = "127.0.0.1";
        const char *ready_file = 0;
        const char *pid_file = 0;
        const char *port_file = 0;
        const char *log_file = 0;
        unsigned int port = 0;
        int i;
        for (i = 2; i < argc; ++i) {
            if (strcmp(argv[i], "--host") == 0 && i + 1 < argc) {
                host = argv[++i];
            } else if (strcmp(argv[i], "--port") == 0 && i + 1 < argc) {
                port = (unsigned int)strtoul(argv[++i], 0, 10);
            } else if (strcmp(argv[i], "--ready-file") == 0 && i + 1 < argc) {
                ready_file = argv[++i];
            } else if (strcmp(argv[i], "--pid-file") == 0 && i + 1 < argc) {
                pid_file = argv[++i];
            } else if (strcmp(argv[i], "--port-file") == 0 && i + 1 < argc) {
                port_file = argv[++i];
            } else if (strcmp(argv[i], "--log-file") == 0 && i + 1 < argc) {
                log_file = argv[++i];
            } else {
                print_usage(argv[0]);
                return 2;
            }
        }
        if (ready_file == 0 || pid_file == 0 || port_file == 0 || log_file == 0) {
            print_usage(argv[0]);
            return 2;
        }
        return run_server(host, port, ready_file, pid_file, port_file, log_file);
    }

    print_usage(argv[0]);
    return 2;
}
