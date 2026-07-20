#define _POSIX_C_SOURCE 200809L

#include <arpa/inet.h>
#include <errno.h>
#include <fcntl.h>
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

#include "haproxy_modsecurity_binding.h"
#include "msconnector/event.h"
#include "msconnector/event_jsonl.h"
#include "msconnector/late_intervention.h"

#define SPOP_FRAME_MAX 65536U
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
#define SPOP_DATA_BIN 9U
#define SPOP_BOOL_TRUE 0x10U
#define SPOP_DATA_TYPE_MASK 0x0fU

#define SPOP_ACT_SET_VAR 1U
#define SPOP_SCOPE_TXN 2U
#define RUNTIME_PATH_LIMIT 4096U
#define RUNTIME_TEXT_LIMIT 65536U

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

typedef struct runtime_header {
    char *name;
    char *value;
} runtime_header;

typedef struct notify_request {
    char message_name[64];
    char request_id[128];
    char client_ip[64];
    char server_ip[64];
    char method[32];
    char path[1024];
    char uri[1024];
    char host[256];
    char test_header[1024];
    unsigned int client_port;
    unsigned int server_port;
    unsigned int response_status;
    runtime_header *headers;
    unsigned int header_count;
    unsigned char *body;
    size_t body_len;
    int has_notify;
    int has_request_id;
    int has_client_ip;
    int has_client_port;
    int has_server_ip;
    int has_server_port;
    int has_method;
    int has_path;
    int has_uri;
    int has_host;
    int has_test_header;
    int has_headers_bin;
    int has_headers_text;
    int has_body;
    int has_body_len_arg;
    int has_response_status;
    int is_response;
    int is_response_body;
} notify_request;

typedef struct agent_config {
    char host[128];
    unsigned int port;
    char ready_file[4096];
    char pid_file[4096];
    char port_file[4096];
    char log_file[4096];
    char decision_log[4096];
    char audit_log[4096];
    char modsecurity_conf[4096];
    char crs_root[4096];
    char rules_file[4096];
    char rules_dir[4096];
    char mode[32];
    char fail_mode[32];
    char runtime_mode[32];
    char variant[64];
    char case_name[256];
    unsigned int expected_status;
    unsigned int request_body_limit;
    unsigned int response_body_limit;
    unsigned int response_body_timeout_ms;
    unsigned int spoe_timeout_ms;
    unsigned int worker_count;
    unsigned int max_transactions;
    int debug;
    int response_phases_enabled;
} agent_config;

typedef struct transaction_slot {
    char request_id[128];
    haproxy_modsecurity_transaction *transaction;
    time_t updated;
} transaction_slot;

typedef struct agent_state {
    agent_config config;
    haproxy_modsecurity_engine *engine;
    transaction_slot *transactions;
    size_t transaction_capacity;
    FILE *log;
    FILE *decision_log;
} agent_state;

static volatile sig_atomic_t stop_requested = 0;
static const unsigned char empty_value[1] = {0};

static void on_signal(int signum) {
    (void)signum;
    stop_requested = 1;
}

static int install_signal_handlers(void) {
    struct sigaction action;

    memset(&action, 0, sizeof(action));
    action.sa_handler = on_signal;
    sigemptyset(&action.sa_mask);
    action.sa_flags = 0;
    if (sigaction(SIGTERM, &action, 0) != 0) {
        return -1;
    }
    if (sigaction(SIGINT, &action, 0) != 0) {
        return -1;
    }
    return 0;
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

static int bounded_cstring_length(const char *value, size_t max_len, size_t *out_len) {
    if (value == 0 || out_len == 0 || max_len == 0) {
        return -1;
    }
    for (size_t len = 0; len < max_len; ++len) {
        if (value[len] == '\0') {
            *out_len = len;
            return 0;
        }
    }
    return -1;
}

static size_t safe_cstring_length(const char *value, size_t max_len) {
    size_t len = 0;

    if (bounded_cstring_length(value, max_len, &len) != 0) {
        return 0;
    }
    return len;
}

static int close_owned_stream(FILE **stream, int owns_stream) {
    int rc = 0;

    if (stream == 0 || *stream == 0) {
        return 0;
    }
    if (owns_stream) {
        rc = fclose(*stream);
    }
    *stream = 0;
    return rc;
}

static FILE *open_private_file(const char *path, int append) {
    int flags = O_WRONLY | O_CREAT | (append ? O_APPEND : O_TRUNC);
    int fd;
    FILE *file;

    if (path == 0 || path[0] == '\0') {
        return 0;
    }
    fd = open(path, flags, S_IRUSR | S_IWUSR);
    if (fd < 0) {
        return 0;
    }
    file = fdopen(fd, append ? "a" : "w");
    if (file == 0) {
        close(fd);
        return 0;
    }
    return file;
}

static int mkdir_p(const char *path) {
    char tmp[4096];
    size_t len;

    if (path == 0 || path[0] == '\0') {
        return -1;
    }
    if (bounded_cstring_length(path, sizeof(tmp), &len) != 0) {
        return -1;
    }
    if (len == 0) {
        return -1;
    }
    memcpy(tmp, path, len + 1);
    if (tmp[len - 1] == '/') {
        tmp[len - 1] = '\0';
    }
    for (char *p = tmp + 1; *p != '\0'; ++p) {
        if (*p == '/') {
            *p = '\0';
            if (mkdir(tmp, S_IRWXU) != 0 && errno != EEXIST) {
                return -1;
            }
            *p = '/';
        }
    }
    if (mkdir(tmp, S_IRWXU) != 0 && errno != EEXIST) {
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
        out[0] = '.';
        out[1] = '\0';
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
    int write_rc;
    int close_rc;

    if (dirname_to_buffer(path, dir, sizeof(dir)) != 0 || mkdir_p(dir) != 0) {
        return -1;
    }
    file = open_private_file(path, 0);
    if (file == 0) {
        return -1;
    }
    va_start(args, fmt);
    write_rc = vfprintf(file, fmt, args);
    va_end(args);
    close_rc = fclose(file);
    if (write_rc < 0 || close_rc != 0) {
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

static int append_bytes(spop_buffer *buf, const void *data, size_t data_len, size_t len) {
    if (buf == 0) {
        return -1;
    }
    if (len > data_len || buf->len > sizeof(buf->data) || len > sizeof(buf->data) - buf->len) {
        return -1;
    }
    if (len == 0U) {
        return 0;
    }
    if (data == 0) {
        return -1;
    }
    memcpy(buf->data + buf->len, data, len);
    buf->len += len;
    return 0;
}

static int append_uint32(spop_buffer *buf, uint32_t value) {
    uint32_t net = htonl(value);
    return append_bytes(buf, &net, sizeof(net), sizeof(net));
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
    size_t len;

    if (bounded_cstring_length(value, SPOP_FRAME_MAX, &len) != 0) {
        return -1;
    }
    if (append_varint(buf, len) != 0) {
        return -1;
    }
    return append_bytes(buf, value, len, len);
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

static int key_equals_literal(const unsigned char *key, size_t key_len, const unsigned char *expected, size_t expected_len) {
    if ((key == 0 && key_len > 0U) || (expected == 0 && expected_len > 0U)) {
        return 0;
    }
    if (key_len != expected_len) {
        return 0;
    }
    return expected_len == 0 || memcmp(key, expected, expected_len) == 0;
}

#define KEY_EQUALS_LITERAL(key, key_len, expected) \
    key_equals_literal((key), (key_len), (const unsigned char *)(expected), sizeof(expected) - 1U)

static int contains_bytes(const unsigned char *value, size_t value_len, const char *needle) {
    size_t needle_len;

    if (bounded_cstring_length(needle, RUNTIME_TEXT_LIMIT, &needle_len) != 0) {
        return 0;
    }
    if ((value == 0 && value_len > 0U) || needle_len == 0 || value_len < needle_len) {
        return 0;
    }
    for (size_t i = 0; i <= value_len - needle_len; ++i) {
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

static void copy_spop_string(char *out, size_t out_len, const unsigned char *value, size_t value_len) {
    size_t copy_len;

    if (out == 0 || out_len == 0) {
        return;
    }
    if (value == 0 && value_len > 0U) {
        out[0] = '\0';
        return;
    }
    copy_len = value_len;
    if (copy_len >= out_len) {
        copy_len = out_len - 1U;
    }
    if (copy_len > 0 && value != 0) {
        for (size_t i = 0; i < copy_len; ++i) {
            out[i] = (char)value[i];
        }
    }
    out[copy_len] = '\0';
}

static void copy_cstring(char *out, size_t out_len, const char *value) {
    size_t len = 0;

    if (out == 0 || out_len == 0) {
        return;
    }
    if (value == 0 || bounded_cstring_length(value, out_len, &len) != 0) {
        out[0] = '\0';
        return;
    }
    copy_spop_string(out, out_len, (const unsigned char *)value, len);
}

static char *dup_bytes_as_cstring(const unsigned char *value, size_t value_len) {
    char *out = (char *)calloc(value_len + 1U, 1U);
    if (out == 0) {
        return 0;
    }
    if (value_len > 0) {
        memcpy(out, value, value_len);
    }
    out[value_len] = '\0';
    return out;
}

static char *dup_header_name(const unsigned char *value, size_t value_len) {
    char *out = dup_bytes_as_cstring(value, value_len);
    int word_start = 1;

    if (out == 0) {
        return 0;
    }
    for (size_t i = 0; i < value_len; ++i) {
        unsigned char ch = (unsigned char)out[i];
        if (ch == '-') {
            word_start = 1;
            continue;
        }
        if (ch >= 'a' && ch <= 'z' && word_start) {
            out[i] = (char)(ch - ('a' - 'A'));
        } else if (ch >= 'A' && ch <= 'Z' && !word_start) {
            out[i] = (char)(ch + ('a' - 'A'));
        }
        word_start = 0;
    }
    return out;
}

static int copy_bytes(unsigned char **out, size_t *out_len, const unsigned char *value, size_t value_len) {
    unsigned char *copy;

    if (out == 0 || out_len == 0 || (value == 0 && value_len > 0U)) {
        return -1;
    }
    copy = 0;
    if (value_len > 0) {
        copy = (unsigned char *)malloc(value_len);
        if (copy == 0) {
            return -1;
        }
        memcpy(copy, value, value_len);
    }
    free(*out);
    *out = copy;
    *out_len = value_len;
    return 0;
}

static void free_notify_request(notify_request *request) {
    if (request == 0) {
        return;
    }
    for (unsigned int i = 0; i < request->header_count; ++i) {
        free(request->headers[i].name);
        free(request->headers[i].value);
    }
    free(request->headers);
    request->headers = 0;
    request->header_count = 0;
    free(request->body);
    request->body = 0;
    request->body_len = 0;
}

static void clear_request_headers(notify_request *request) {
    if (request == 0) {
        return;
    }
    for (unsigned int i = 0; i < request->header_count; ++i) {
        free(request->headers[i].name);
        free(request->headers[i].value);
    }
    free(request->headers);
    request->headers = 0;
    request->header_count = 0;
}

static int add_request_header(
        notify_request *request,
        const unsigned char *name,
        size_t name_len,
        const unsigned char *value,
        size_t value_len) {
    runtime_header *headers;

    if (name_len == 0) {
        return 0;
    }
    headers = (runtime_header *)realloc(request->headers,
        sizeof(*request->headers) * (request->header_count + 1U));
    if (headers == 0) {
        return -1;
    }
    request->headers = headers;
    request->headers[request->header_count].name = dup_header_name(name, name_len);
    request->headers[request->header_count].value = dup_bytes_as_cstring(value, value_len);
    if (request->headers[request->header_count].name == 0 ||
            request->headers[request->header_count].value == 0) {
        return -1;
    }
    request->header_count++;
    return 0;
}

static int parse_headers_bin(notify_request *request, const unsigned char *value, size_t value_len) {
    size_t pos = 0;

    while (pos < value_len) {
        const unsigned char *name;
        const unsigned char *header_value;
        size_t name_len;
        size_t header_value_len;

        if (read_string_ref(value, value_len, &pos, &name, &name_len) != 0 ||
                read_string_ref(value, value_len, &pos, &header_value, &header_value_len) != 0) {
            return -1;
        }
        if (name_len == 0 && header_value_len == 0) {
            request->has_headers_bin = 1;
            return 0;
        }
        if (add_request_header(request, name, name_len, header_value, header_value_len) != 0) {
            return -1;
        }
    }
    request->has_headers_bin = 1;
    return 0;
}

static int parse_headers_text(notify_request *request, const unsigned char *value, size_t value_len) {
    size_t start = 0;

    while (start < value_len) {
        size_t end = start;
        size_t colon;
        size_t name_len;
        size_t header_value_start;

        while (end < value_len && value[end] != '\n') {
            end++;
        }
        if (end > start && value[end - 1U] == '\r') {
            end--;
        }
        if (end == start) {
            break;
        }
        colon = start;
        while (colon < end && value[colon] != ':') {
            colon++;
        }
        if (colon < end) {
            name_len = colon - start;
            header_value_start = colon + 1U;
            while (header_value_start < end &&
                    (value[header_value_start] == ' ' || value[header_value_start] == '\t')) {
                header_value_start++;
            }
            if (add_request_header(request, value + start, name_len,
                    value + header_value_start, end - header_value_start) != 0) {
                return -1;
            }
        }
        start = end + 1U;
    }
    request->has_headers_text = 1;
    return 0;
}

static int read_typed_bytes_ref(
        const unsigned char *data,
        size_t len,
        size_t *pos,
        const unsigned char **value,
        size_t *value_len,
        unsigned int *typed_type) {
    size_t value_pos = *pos;
    unsigned int type;

    if (*pos >= len) {
        return -1;
    }
    type = data[(*pos)++] & SPOP_DATA_TYPE_MASK;
    if (type == 0U) {
        *value = empty_value;
        *value_len = 0;
        if (typed_type != 0) {
            *typed_type = type;
        }
        return 0;
    }
    if (type != SPOP_DATA_STR && type != SPOP_DATA_BIN) {
        *pos = value_pos;
        return skip_typed_data(data, len, pos);
    }
    if (read_string_ref(data, len, pos, value, value_len) != 0) {
        return -1;
    }
    if (typed_type != 0) {
        *typed_type = type;
    }
    return 0;
}

static int read_typed_string_to_buffer(
        const unsigned char *data,
        size_t len,
        size_t *pos,
        char *out,
        size_t out_len,
        int *present) {
    size_t value_pos = *pos;
    unsigned int type;
    const unsigned char *value;
    size_t value_len;

    if (*pos >= len) {
        return -1;
    }
    type = data[(*pos)++] & SPOP_DATA_TYPE_MASK;
    if (type == 0U) {
        copy_spop_string(out, out_len, (const unsigned char *)"", 0);
        *present = 1;
        return 0;
    }
    if (type != SPOP_DATA_STR) {
        *pos = value_pos;
        return skip_typed_data(data, len, pos);
    }
    if (read_string_ref(data, len, pos, &value, &value_len) != 0) {
        return -1;
    }
    copy_spop_string(out, out_len, value, value_len);
    *present = 1;
    return 0;
}

static int read_typed_uint32_value(
        const unsigned char *data,
        size_t len,
        size_t *pos,
        unsigned int *out,
        int *present) {
    unsigned int type;
    uint64_t value;

    if (*pos >= len) {
        return -1;
    }
    type = data[(*pos)++] & SPOP_DATA_TYPE_MASK;
    if (type != SPOP_DATA_UINT32) {
        return -1;
    }
    if (read_varint(data, len, pos, &value) != 0) {
        return -1;
    }
    *out = (unsigned int)value;
    *present = 1;
    return 0;
}

static int read_typed_uint32_loose(
        const unsigned char *data,
        size_t len,
        size_t *pos,
        unsigned int *out,
        int *present) {
    size_t value_pos = *pos;
    unsigned int type;
    uint64_t value;

    if (*pos >= len) {
        return -1;
    }
    type = data[(*pos)++] & SPOP_DATA_TYPE_MASK;
    switch (type) {
        case 2U:
        case SPOP_DATA_UINT32:
        case 4U:
        case 5U:
            if (read_varint(data, len, pos, &value) != 0) {
                return -1;
            }
            *out = value > 0xffffffffULL ? 0xffffffffU : (unsigned int)value;
            *present = 1;
            return 0;
        case SPOP_DATA_BOOL:
            *out = (data[value_pos] & SPOP_BOOL_TRUE) != 0 ? 1U : 0U;
            *present = 1;
            return 0;
        default:
            *pos = value_pos;
            return skip_typed_data(data, len, pos);
    }
}

static void parse_disconnect_payload(
        const unsigned char *data,
        size_t len,
        unsigned int *status_code,
        char *message,
        size_t message_len) {
    size_t pos = 0;
    int status_present = 0;
    int message_present = 0;

    if (status_code != 0) {
        *status_code = 0;
    }
    if (message != 0 && message_len > 0) {
        message[0] = '\0';
    }
    while (pos < len) {
        const unsigned char *key;
        size_t key_len;

        if (read_string_ref(data, len, &pos, &key, &key_len) != 0) {
            return;
        }
        if (KEY_EQUALS_LITERAL(key, key_len, "status-code") && status_code != 0) {
            if (read_typed_uint32_value(data, len, &pos, status_code, &status_present) != 0) {
                return;
            }
            continue;
        }
        if (KEY_EQUALS_LITERAL(key, key_len, "message") && message != 0) {
            if (read_typed_string_to_buffer(data, len, &pos, message,
                    message_len, &message_present) != 0) {
                return;
            }
            continue;
        }
        if (skip_typed_data(data, len, &pos) != 0) {
            return;
        }
    }
    (void)status_present;
    (void)message_present;
}

static int parse_notify_payload(const unsigned char *data, size_t len, notify_request *request) {
    size_t pos = 0;

    memset(request, 0, sizeof(*request));
    while (pos < len) {
        const unsigned char *message_name;
        size_t message_name_len;
        unsigned int nb_args;

        if (read_string_ref(data, len, &pos, &message_name, &message_name_len) != 0 ||
                pos >= len) {
            return -1;
        }
        copy_spop_string(request->message_name, sizeof(request->message_name),
            message_name, message_name_len);
        request->is_response =
            KEY_EQUALS_LITERAL(message_name, message_name_len, "check-response") ||
            KEY_EQUALS_LITERAL(message_name, message_name_len, "check-response-body");
        request->is_response_body =
            KEY_EQUALS_LITERAL(message_name, message_name_len, "check-response-body");
        nb_args = data[pos++];
        request->has_notify = 1;
        for (unsigned int i = 0; i < nb_args; ++i) {
            const unsigned char *arg_name;
            size_t arg_name_len;

            if (read_string_ref(data, len, &pos, &arg_name, &arg_name_len) != 0) {
                return -1;
            }
            if (KEY_EQUALS_LITERAL(arg_name, arg_name_len, "request_id")) {
                if (read_typed_string_to_buffer(data, len, &pos, request->request_id,
                        sizeof(request->request_id), &request->has_request_id) != 0) {
                    return -1;
                }
                continue;
            }
            if (KEY_EQUALS_LITERAL(arg_name, arg_name_len, "client_ip")) {
                if (read_typed_string_to_buffer(data, len, &pos, request->client_ip,
                        sizeof(request->client_ip), &request->has_client_ip) != 0) {
                    return -1;
                }
                continue;
            }
            if (KEY_EQUALS_LITERAL(arg_name, arg_name_len, "client_port")) {
                if (read_typed_uint32_loose(data, len, &pos, &request->client_port,
                        &request->has_client_port) != 0) {
                    return -1;
                }
                continue;
            }
            if (KEY_EQUALS_LITERAL(arg_name, arg_name_len, "server_ip")) {
                if (read_typed_string_to_buffer(data, len, &pos, request->server_ip,
                        sizeof(request->server_ip), &request->has_server_ip) != 0) {
                    return -1;
                }
                continue;
            }
            if (KEY_EQUALS_LITERAL(arg_name, arg_name_len, "server_port")) {
                if (read_typed_uint32_loose(data, len, &pos, &request->server_port,
                        &request->has_server_port) != 0) {
                    return -1;
                }
                continue;
            }
            if (KEY_EQUALS_LITERAL(arg_name, arg_name_len, "method")) {
                if (read_typed_string_to_buffer(data, len, &pos, request->method,
                        sizeof(request->method), &request->has_method) != 0) {
                    return -1;
                }
                continue;
            }
            if (KEY_EQUALS_LITERAL(arg_name, arg_name_len, "path")) {
                if (read_typed_string_to_buffer(data, len, &pos, request->path,
                        sizeof(request->path), &request->has_path) != 0) {
                    return -1;
                }
                continue;
            }
            if (KEY_EQUALS_LITERAL(arg_name, arg_name_len, "uri")) {
                if (read_typed_string_to_buffer(data, len, &pos, request->uri,
                        sizeof(request->uri), &request->has_uri) != 0) {
                    return -1;
                }
                continue;
            }
            if (KEY_EQUALS_LITERAL(arg_name, arg_name_len, "host")) {
                if (read_typed_string_to_buffer(data, len, &pos, request->host,
                        sizeof(request->host), &request->has_host) != 0) {
                    return -1;
                }
                continue;
            }
            if (KEY_EQUALS_LITERAL(arg_name, arg_name_len, "test_header")) {
                if (read_typed_string_to_buffer(data, len, &pos, request->test_header,
                        sizeof(request->test_header), &request->has_test_header) != 0) {
                    return -1;
                }
                continue;
            }
            if (KEY_EQUALS_LITERAL(arg_name, arg_name_len, "response_status")) {
                if (read_typed_uint32_loose(data, len, &pos, &request->response_status,
                        &request->has_response_status) != 0) {
                    return -1;
                }
                continue;
            }
            if (KEY_EQUALS_LITERAL(arg_name, arg_name_len, "headers_bin")) {
                const unsigned char *value = 0;
                size_t value_len = 0;
                unsigned int typed_type = 0;
                if (read_typed_bytes_ref(data, len, &pos, &value, &value_len, &typed_type) != 0) {
                    return -1;
                }
                if ((typed_type == SPOP_DATA_STR || typed_type == SPOP_DATA_BIN) &&
                        parse_headers_bin(request, value, value_len) != 0) {
                    return -1;
                }
                continue;
            }
            if (KEY_EQUALS_LITERAL(arg_name, arg_name_len, "response_headers_bin")) {
                const unsigned char *value = 0;
                size_t value_len = 0;
                unsigned int typed_type = 0;
                if (read_typed_bytes_ref(data, len, &pos, &value, &value_len, &typed_type) != 0) {
                    return -1;
                }
                if ((typed_type == SPOP_DATA_STR || typed_type == SPOP_DATA_BIN) &&
                        parse_headers_bin(request, value, value_len) != 0) {
                    return -1;
                }
                request->is_response = 1;
                continue;
            }
            if (KEY_EQUALS_LITERAL(arg_name, arg_name_len, "headers")) {
                const unsigned char *value = 0;
                size_t value_len = 0;
                unsigned int typed_type = 0;
                if (read_typed_bytes_ref(data, len, &pos, &value, &value_len, &typed_type) != 0) {
                    return -1;
                }
                if (typed_type == SPOP_DATA_STR || typed_type == SPOP_DATA_BIN) {
                    notify_request text_request;
                    memset(&text_request, 0, sizeof(text_request));
                    if (parse_headers_text(&text_request, value, value_len) != 0) {
                        free_notify_request(&text_request);
                        return -1;
                    }
                    if (text_request.header_count >= request->header_count && text_request.header_count > 0) {
                        clear_request_headers(request);
                        request->headers = text_request.headers;
                        request->header_count = text_request.header_count;
                        request->has_headers_text = 1;
                        text_request.headers = 0;
                        text_request.header_count = 0;
                    }
                    free_notify_request(&text_request);
                }
                continue;
            }
            if (KEY_EQUALS_LITERAL(arg_name, arg_name_len, "response_headers")) {
                const unsigned char *value = 0;
                size_t value_len = 0;
                unsigned int typed_type = 0;
                if (read_typed_bytes_ref(data, len, &pos, &value, &value_len, &typed_type) != 0) {
                    return -1;
                }
                if (typed_type == SPOP_DATA_STR || typed_type == SPOP_DATA_BIN) {
                    notify_request text_request;
                    memset(&text_request, 0, sizeof(text_request));
                    if (parse_headers_text(&text_request, value, value_len) != 0) {
                        free_notify_request(&text_request);
                        return -1;
                    }
                    if (text_request.header_count >= request->header_count && text_request.header_count > 0) {
                        clear_request_headers(request);
                        request->headers = text_request.headers;
                        request->header_count = text_request.header_count;
                        request->has_headers_text = 1;
                        text_request.headers = 0;
                        text_request.header_count = 0;
                    }
                    free_notify_request(&text_request);
                }
                request->is_response = 1;
                continue;
            }
            if (KEY_EQUALS_LITERAL(arg_name, arg_name_len, "response_header_last_modified") ||
                    KEY_EQUALS_LITERAL(arg_name, arg_name_len, "response_header_content_type") ||
                    KEY_EQUALS_LITERAL(arg_name, arg_name_len, "response_header_location") ||
                    KEY_EQUALS_LITERAL(arg_name, arg_name_len, "response_header_set_cookie") ||
                    KEY_EQUALS_LITERAL(arg_name, arg_name_len, "response_header_server")) {
                char header_value[2048];
                const char *header_name = "";
                int present = 0;
                if (read_typed_string_to_buffer(data, len, &pos, header_value,
                        sizeof(header_value), &present) != 0) {
                    return -1;
                }
                if (KEY_EQUALS_LITERAL(arg_name, arg_name_len, "response_header_last_modified")) {
                    header_name = "Last-Modified";
                } else if (KEY_EQUALS_LITERAL(arg_name, arg_name_len, "response_header_content_type")) {
                    header_name = "Content-Type";
                } else if (KEY_EQUALS_LITERAL(arg_name, arg_name_len, "response_header_location")) {
                    header_name = "Location";
                } else if (KEY_EQUALS_LITERAL(arg_name, arg_name_len, "response_header_set_cookie")) {
                    header_name = "Set-Cookie";
                } else if (KEY_EQUALS_LITERAL(arg_name, arg_name_len, "response_header_server")) {
                    header_name = "Server";
                }
                if (present && header_value[0] != '\0') {
                    size_t header_name_len = 0;
                    size_t header_value_len = 0;

                    if (bounded_cstring_length(header_name, RUNTIME_TEXT_LIMIT, &header_name_len) != 0 ||
                            bounded_cstring_length(header_value, sizeof(header_value), &header_value_len) != 0 ||
                            add_request_header(request,
                                (const unsigned char *)header_name,
                                header_name_len,
                                (const unsigned char *)header_value,
                                header_value_len) != 0) {
                        return -1;
                    }
                }
                request->is_response = 1;
                continue;
            }
            if (KEY_EQUALS_LITERAL(arg_name, arg_name_len, "body")) {
                const unsigned char *value = 0;
                size_t value_len = 0;
                unsigned int typed_type = 0;
                if (read_typed_bytes_ref(data, len, &pos, &value, &value_len, &typed_type) != 0) {
                    return -1;
                }
                if ((typed_type == SPOP_DATA_STR || typed_type == SPOP_DATA_BIN) &&
                        copy_bytes(&request->body, &request->body_len, value, value_len) != 0) {
                    return -1;
                }
                if (typed_type == SPOP_DATA_STR || typed_type == SPOP_DATA_BIN) {
                    request->has_body = 1;
                }
                continue;
            }
            if (KEY_EQUALS_LITERAL(arg_name, arg_name_len, "response_body")) {
                const unsigned char *value = 0;
                size_t value_len = 0;
                unsigned int typed_type = 0;
                if (read_typed_bytes_ref(data, len, &pos, &value, &value_len, &typed_type) != 0) {
                    return -1;
                }
                if ((typed_type == SPOP_DATA_STR || typed_type == SPOP_DATA_BIN) &&
                        copy_bytes(&request->body, &request->body_len, value, value_len) != 0) {
                    return -1;
                }
                if (typed_type == SPOP_DATA_STR || typed_type == SPOP_DATA_BIN) {
                    request->has_body = 1;
                    request->is_response = 1;
                    request->is_response_body = 1;
                }
                continue;
            }
            if (KEY_EQUALS_LITERAL(arg_name, arg_name_len, "body_len") ||
                    KEY_EQUALS_LITERAL(arg_name, arg_name_len, "response_body_len")) {
                unsigned int ignored_body_len = 0;
                if (read_typed_uint32_loose(data, len, &pos, &ignored_body_len,
                        &request->has_body_len_arg) != 0) {
                    return -1;
                }
                continue;
            }
            if (skip_typed_data(data, len, &pos) != 0) {
                return -1;
            }
        }
    }
    return 0;
}

static int build_notify_request_payload(
        spop_buffer *payload,
        const char *method,
        const char *path,
        const char *uri,
        const char *host,
        const char *test_header) {
    payload->len = 0;
    if (append_string(payload, "check-request") != 0 ||
            append_byte(payload, 5U) != 0 ||
            append_string(payload, "method") != 0 ||
            append_typed_string(payload, method) != 0 ||
            append_string(payload, "path") != 0 ||
            append_typed_string(payload, path) != 0 ||
            append_string(payload, "uri") != 0 ||
            append_typed_string(payload, uri) != 0 ||
            append_string(payload, "host") != 0 ||
            append_typed_string(payload, host) != 0 ||
            append_string(payload, "test_header") != 0 ||
            append_typed_string(payload, test_header) != 0) {
        return -1;
    }
    return 0;
}

static int append_set_var_bool(spop_buffer *payload, const char *name, int value) {
    if (append_byte(payload, SPOP_ACT_SET_VAR) != 0 ||
            append_byte(payload, 3U) != 0 ||
            append_byte(payload, SPOP_SCOPE_TXN) != 0 ||
            append_string(payload, name) != 0 ||
            append_typed_bool(payload, value) != 0) {
        return -1;
    }
    return 0;
}

static int append_set_var_uint32(spop_buffer *payload, const char *name, unsigned int value) {
    if (append_byte(payload, SPOP_ACT_SET_VAR) != 0 ||
            append_byte(payload, 3U) != 0 ||
            append_byte(payload, SPOP_SCOPE_TXN) != 0 ||
            append_string(payload, name) != 0 ||
            append_typed_uint32(payload, value) != 0) {
        return -1;
    }
    return 0;
}

static int append_set_var_string(spop_buffer *payload, const char *name, const char *value) {
    if (append_byte(payload, SPOP_ACT_SET_VAR) != 0 ||
            append_byte(payload, 3U) != 0 ||
            append_byte(payload, SPOP_SCOPE_TXN) != 0 ||
            append_string(payload, name) != 0 ||
            append_typed_string(payload, value != 0 ? value : "") != 0) {
        return -1;
    }
    return 0;
}

static int build_set_var_blocked_payload(spop_buffer *payload) {
    payload->len = 0;
    return append_set_var_bool(payload, "blocked", 1);
}

static int build_decision_ack_payload(
        spop_buffer *payload,
        const haproxy_modsecurity_decision *decision,
        const char *error_text,
        int enforce_disruptive) {
    const char *action;
    int blocked;
    unsigned int status;

    payload->len = 0;
    if (decision == 0) {
        return 0;
    }
    blocked = enforce_disruptive && decision->disruptive != 0;
    action = blocked && decision->action[0] != '\0' ? decision->action : "pass";
    status = decision->status > 0 ? (unsigned int)decision->status : 0U;
    if (append_set_var_bool(payload, "blocked", blocked) != 0 ||
            append_set_var_string(payload, "action", action) != 0 ||
            append_set_var_uint32(payload, "status", status) != 0 ||
            append_set_var_uint32(payload, "phase", decision->phase > 0 ?
                (unsigned int)decision->phase : 0U) != 0 ||
            append_set_var_uint32(payload, "rule_id", decision->rule_id > 0 ?
                (unsigned int)decision->rule_id : 0U) != 0 ||
            append_set_var_string(payload, "redirect_url",
                decision->redirect_url) != 0 ||
            append_set_var_string(payload, "error",
                error_text != 0 ? error_text : "") != 0) {
        return -1;
    }
    return 0;
}

static int payload_has_set_var_blocked_true(const spop_buffer *payload) {
    size_t pos = 0;
    const unsigned char *name;
    size_t name_len;

    if (payload->len < 4U) {
        return 0;
    }
    if (payload->data[pos] != SPOP_ACT_SET_VAR) {
        return 0;
    }
    ++pos;
    if (payload->data[pos] != 3U) {
        return 0;
    }
    ++pos;
    if (payload->data[pos] != SPOP_SCOPE_TXN) {
        return 0;
    }
    ++pos;
    if (read_string_ref(payload->data, payload->len, &pos, &name, &name_len) != 0) {
        return 0;
    }
    if (!KEY_EQUALS_LITERAL(name, name_len, "blocked") || pos >= payload->len) {
        return 0;
    }
    return payload->data[pos] == (SPOP_DATA_BOOL | SPOP_BOOL_TRUE);
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
        if (KEY_EQUALS_LITERAL(key, key_len, "supported-versions") && type == SPOP_DATA_STR) {
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
        if (KEY_EQUALS_LITERAL(key, key_len, "max-frame-size") && type == SPOP_DATA_UINT32) {
            uint64_t value;
            if (read_varint(data, len, &pos, &value) != 0 || value < SPOP_MIN_FRAME_SIZE) {
                return -1;
            }
            hello->max_frame_size = value < SPOP_FRAME_MAX ? (unsigned int)value : SPOP_FRAME_MAX;
            hello->has_max_frame_size = 1;
            continue;
        }
        if (KEY_EQUALS_LITERAL(key, key_len, "capabilities") && type == SPOP_DATA_STR) {
            const unsigned char *value;
            size_t value_len;
            if (read_string_ref(data, len, &pos, &value, &value_len) != 0) {
                return -1;
            }
            hello->has_capabilities = 1;
            continue;
        }
        if (KEY_EQUALS_LITERAL(key, key_len, "healthcheck") && type == SPOP_DATA_BOOL) {
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
    if (payload != 0 && append_bytes(frame, payload->data, sizeof(payload->data), payload->len) != 0) {
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
    if (append_kv_string(&payload, "version", "2.0") != 0 ||
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
    if (append_kv_string(&payload, "supported-versions", "2.0,1.2") != 0 ||
        append_kv_uint32(&payload, "max-frame-size", SPOP_FRAME_MAX) != 0 ||
        append_kv_string(&payload, "capabilities", "") != 0 ||
        append_kv_bool(&payload, "healthcheck", healthcheck) != 0) {
        return -1;
    }
    return send_frame(fd, SPOP_FRM_HAPROXY_HELLO, 0, 0, &payload);
}

static void config_init(agent_config *config) {
    memset(config, 0, sizeof(*config));
    copy_spop_string(config->host, sizeof(config->host),
        (const unsigned char *)"127.0.0.1", sizeof("127.0.0.1") - 1U);
    copy_spop_string(config->mode, sizeof(config->mode),
        (const unsigned char *)"block", sizeof("block") - 1U);
    copy_spop_string(config->fail_mode, sizeof(config->fail_mode),
        (const unsigned char *)"closed", sizeof("closed") - 1U);
    copy_spop_string(config->runtime_mode, sizeof(config->runtime_mode),
        (const unsigned char *)"production", sizeof("production") - 1U);
    copy_spop_string(config->variant, sizeof(config->variant),
        (const unsigned char *)"-", sizeof("-") - 1U);
    copy_spop_string(config->log_file, sizeof(config->log_file),
        (const unsigned char *)"-", sizeof("-") - 1U);
    config->request_body_limit = 65532U;
    config->response_body_limit = 0U;
    config->response_body_timeout_ms = 0U;
    config->spoe_timeout_ms = 2000U;
    config->worker_count = 1U;
    config->max_transactions = 4096U;
}

static int parse_listen(agent_config *config, const char *listen_value) {
    const char *colon;
    size_t host_len;
    unsigned long port;

    if (listen_value == 0 || listen_value[0] == '\0') {
        return -1;
    }
    colon = strrchr(listen_value, ':');
    if (colon == 0 || colon == listen_value || colon[1] == '\0') {
        return -1;
    }
    host_len = (size_t)(colon - listen_value);
    if (host_len >= sizeof(config->host)) {
        return -1;
    }
    memcpy(config->host, listen_value, host_len);
    config->host[host_len] = '\0';
    port = strtoul(colon + 1, 0, 10);
    if (port > 65535UL) {
        return -1;
    }
    config->port = (unsigned int)port;
    return 0;
}

static int config_set(agent_config *config, const char *key, const char *value) {
    if (strcmp(key, "listen") == 0) {
        return parse_listen(config, value);
    }
    if (strcmp(key, "host") == 0) {
        copy_spop_string(config->host, sizeof(config->host),
            (const unsigned char *)value, safe_cstring_length(value, RUNTIME_TEXT_LIMIT));
        return 0;
    }
    if (strcmp(key, "port") == 0) {
        config->port = (unsigned int)strtoul(value, 0, 10);
        return 0;
    }
#define SET_STRING_FIELD(name, field) \
    if (strcmp(key, name) == 0) { \
        copy_spop_string(config->field, sizeof(config->field), \
            (const unsigned char *)value, safe_cstring_length(value, RUNTIME_TEXT_LIMIT)); \
        return 0; \
    }
    SET_STRING_FIELD("ready-file", ready_file)
    SET_STRING_FIELD("pid-file", pid_file)
    SET_STRING_FIELD("port-file", port_file)
    SET_STRING_FIELD("log-file", log_file)
    SET_STRING_FIELD("decision-log", decision_log)
    SET_STRING_FIELD("audit-log", audit_log)
    SET_STRING_FIELD("modsecurity-conf", modsecurity_conf)
    SET_STRING_FIELD("crs-root", crs_root)
    SET_STRING_FIELD("rules-file", rules_file)
    SET_STRING_FIELD("rules-dir", rules_dir)
    SET_STRING_FIELD("mode", mode)
    SET_STRING_FIELD("fail-mode", fail_mode)
    SET_STRING_FIELD("runtime-mode", runtime_mode)
    SET_STRING_FIELD("variant", variant)
    SET_STRING_FIELD("case", case_name)
#undef SET_STRING_FIELD
    if (strcmp(key, "expected-status") == 0) {
        config->expected_status = (unsigned int)strtoul(value, 0, 10);
        return 0;
    }
    if (strcmp(key, "request-body-limit") == 0) {
        config->request_body_limit = (unsigned int)strtoul(value, 0, 10);
        return 0;
    }
    if (strcmp(key, "response-body-limit") == 0) {
        config->response_body_limit = (unsigned int)strtoul(value, 0, 10);
        if (config->response_body_limit > 0U) {
            config->response_phases_enabled = 1;
        }
        return 0;
    }
    if (strcmp(key, "response-body-timeout") == 0) {
        config->response_body_timeout_ms = (unsigned int)strtoul(value, 0, 10);
        return 0;
    }
    if (strcmp(key, "spoe-timeout") == 0) {
        config->spoe_timeout_ms = (unsigned int)strtoul(value, 0, 10);
        return 0;
    }
    if (strcmp(key, "worker-count") == 0) {
        config->worker_count = (unsigned int)strtoul(value, 0, 10);
        return 0;
    }
    if (strcmp(key, "max-transactions") == 0) {
        config->max_transactions = (unsigned int)strtoul(value, 0, 10);
        return 0;
    }
    if (strcmp(key, "debug") == 0) {
        config->debug = strcmp(value, "1") == 0 || strcmp(value, "true") == 0 ||
            strcmp(value, "yes") == 0 || strcmp(value, "on") == 0;
        return 0;
    }
    if (strcmp(key, "enable-response-headers") == 0 ||
            strcmp(key, "response-phases") == 0) {
        config->response_phases_enabled = strcmp(value, "0") != 0 &&
            strcmp(value, "false") != 0 && strcmp(value, "off") != 0 &&
            strcmp(value, "no") != 0;
        return 0;
    }
    return -1;
}

static char *trim_in_place(char *value) {
    char *end;
    size_t len;

    while (*value == ' ' || *value == '\t' || *value == '\r' || *value == '\n') {
        value++;
    }
    if (bounded_cstring_length(value, RUNTIME_TEXT_LIMIT, &len) != 0) {
        return value;
    }
    end = value + len;
    while (end > value && (end[-1] == ' ' || end[-1] == '\t' ||
            end[-1] == '\r' || end[-1] == '\n')) {
        *--end = '\0';
    }
    return value;
}

static int load_config_file(agent_config *config, const char *path) {
    char line[8192];
    FILE *file;

    if (path == 0 || path[0] == '\0') {
        return 0;
    }
    file = fopen(path, "r");
    if (file == 0) {
        return -1;
    }
    while (fgets(line, sizeof(line), file) != 0) {
        char *key;
        char *value;
        char *equals;
        key = trim_in_place(line);
        if (key[0] == '\0' || key[0] == '#') {
            continue;
        }
        equals = strchr(key, '=');
        if (equals == 0) {
            fclose(file);
            return -1;
        }
        *equals = '\0';
        value = trim_in_place(equals + 1);
        key = trim_in_place(key);
        if (config_set(config, key, value) != 0) {
            fclose(file);
            return -1;
        }
    }
    fclose(file);
    return 0;
}

static int fail_mode_closed(const agent_config *config) {
    return strcmp(config->fail_mode, "closed") == 0;
}

static int mode_enforces(const agent_config *config) {
    return strcmp(config->mode, "detect-only") != 0;
}

static void json_write_string(FILE *file, const char *value) {
    const unsigned char *cursor;
    size_t value_len;

    fputc('"', file);
    if (value == 0 || bounded_cstring_length(value, RUNTIME_TEXT_LIMIT, &value_len) != 0) {
        fputc('"', file);
        return;
    }
    if (*value == '\0') {
        fputc('"', file);
        return;
    }
    cursor = (const unsigned char *)value;
    for (size_t remaining = value_len; remaining > 0U; --remaining) {
        unsigned char ch = *cursor++;
        switch (ch) {
            case '\\':
                fputs("\\\\", file);
                break;
            case '"':
                fputs("\\\"", file);
                break;
            case '\b':
                fputs("\\b", file);
                break;
            case '\f':
                fputs("\\f", file);
                break;
            case '\n':
                fputs("\\n", file);
                break;
            case '\r':
                fputs("\\r", file);
                break;
            case '\t':
                fputs("\\t", file);
                break;
            default:
                if (ch < 0x20U) {
                    fprintf(file, "\\u%04x", ch);
                } else {
                    fputc(ch, file);
                }
                break;
        }
    }
    fputc('"', file);
}

static const char *safe_decision_name(
        const char *decision_text,
        const haproxy_modsecurity_decision *decision) {
    static const char *const allowed[] = {
        "pass", "deny", "redirect", "drop", "fail-closed", "fail-open"
    };
    if (decision_text != 0) {
        for (size_t index = 0U; index < sizeof(allowed) / sizeof(allowed[0]); ++index) {
            if (strcmp(decision_text, allowed[index]) == 0) {
                return allowed[index];
            }
        }
    }
    if (decision != 0 && decision->disruptive != 0) {
        return decision->redirect_url[0] != '\0' ? "redirect" : "deny";
    }
    return "pass";
}

static const char *phase4_requested_action(
        const haproxy_modsecurity_decision *decision,
        const char *decision_text) {
    const char *name = safe_decision_name(decision_text, decision);

    return strcmp(name, "redirect") == 0 ? "redirect" : "deny";
}

static const char *phase4_actual_action(void) {
    msconnector_late_intervention_policy policy;
    msconnector_late_intervention_action action;
    const char *name;

    /* SPOE response rules run before HAProxy commits the response.  This is a
     * host-model property, not a runtime-verification claim. */
    msconnector_late_intervention_policy_init(&policy);
    action = msconnector_late_intervention_resolve(&policy, 0, 0, 0);
    name = msconnector_late_intervention_action_name(action);
    return strcmp(name, "deny_if_possible") == 0 ? "deny" : name;
}

static void phase4_common_event_write(
        FILE *file,
        const notify_request *request,
        const haproxy_modsecurity_decision *decision,
        const char *requested_action,
        const char *actual_action,
        int original_status,
        const char *reason_code) {
    msconnector_event event;
    char line[4096];
    char rule_id[32];
    int json_truncated = 0;

    if (file == 0 || request == 0 || decision == 0 ||
            requested_action == 0 || actual_action == 0) {
        return;
    }

    (void)snprintf(rule_id, sizeof(rule_id), "%u", decision->rule_id);
    msconnector_event_init(&event);
    event.meta.message_id = strcmp(actual_action, "abort_connection") == 0
        ? MSCONN_EVENT_PHASE4_HARD_ABORT_AFTER_200
        : (strcmp(actual_action, "log_only") == 0
            ? MSCONN_EVENT_PHASE4_LATE_INTERVENTION
            : MSCONN_EVENT_RESPONSE_BLOCKED);
    event.meta.level = msconnector_event_default_level(event.meta.message_id);
    event.meta.message = msconnector_event_default_message(event.meta.message_id);
    event.meta.event = "phase4_intervention";
    event.meta.connector = "haproxy";
    event.meta.transaction_id = request->request_id;
    event.decision.phase = MSCONNECTOR_PHASE_RESPONSE_BODY;
    event.decision.status = MSCONNECTOR_STATUS_BLOCKED;
    event.decision.action = actual_action;
    event.decision.requested_action = requested_action;
    event.decision.actual_action = actual_action;
    event.decision.rule_id = rule_id;
    event.decision.reason = reason_code;
    event.http.http_status = decision->status;
    event.http.original_http_status = original_status;
    event.http.visible_http_status = strcmp(actual_action, "deny") == 0
        ? decision->status : original_status;
    event.http.transport_result = strcmp(actual_action, "abort_connection") == 0
        ? "connection_aborted" : (strcmp(actual_action, "log_only") == 0
            ? "log_only" : "http_status");
    /* The SPOE response rules execute before HAProxy forwards this response.
     * This is source-level host-model metadata only; capability promotion still
     * requires the harness to independently observe the client outcome. */
    event.flags.late_intervention = 0;
    event.flags.response_started = 0;
    event.flags.response_committed = 0;
    event.flags.headers_sent = 0;
    event.flags.body_started = 0;
    event.flags.connection_aborted = 0;

    if (msconnector_event_write_jsonl_line(&event, line, sizeof(line),
            &json_truncated)) {
        fputs(line, file);
    }
}

static const char *safe_decision_reason_code(
        const haproxy_modsecurity_decision *decision,
        int modsecurity_processed,
        const char *decision_text) {
    const char *safe_decision = safe_decision_name(decision_text, decision);

    if (strcmp(safe_decision, "fail-closed") == 0) {
        return "modsecurity_processing_failed_closed";
    }
    if (strcmp(safe_decision, "fail-open") == 0) {
        return "modsecurity_processing_failed_open";
    }
    if (!modsecurity_processed) {
        return "modsecurity_not_processed";
    }
    if (decision != 0 && decision->disruptive != 0) {
        return strcmp(safe_decision, "redirect") == 0
            ? "modsecurity_redirect_intervention"
            : "modsecurity_disruptive_intervention";
    }
    if (decision != 0 && decision->rule_id > 0) {
        return "modsecurity_rule_observed";
    }
    return "modsecurity_allow";
}

static void decision_log_write(
        agent_state *state,
        const notify_request *request,
        const haproxy_modsecurity_decision *decision,
        int modsecurity_processed,
        const char *decision_text) {
    /*
     * Canonical evidence is metadata-only.  Do not serialize request values,
     * redirect targets, matched data, or libmodsecurity intervention messages:
     * those strings can contain bodies, credentials, cookies, or other input.
     */
    FILE *file;
    const char *reason_code;
    const char *decision_name;
    const char *requested_action = 0;
    const char *actual_action = 0;
    int phase4_disruptive;
    int original_status;
    time_t now;

    if (state == 0 || state->decision_log == 0 || request == 0 || decision == 0) {
        return;
    }
    file = state->decision_log;
    decision_name = safe_decision_name(decision_text, decision);
    reason_code = safe_decision_reason_code(
        decision, modsecurity_processed, decision_name);
    phase4_disruptive = request->is_response_body && decision->phase == 4 &&
        decision->disruptive != 0;
    original_status = request->has_response_status ?
        (int)request->response_status : 200;
    if (phase4_disruptive) {
        requested_action = phase4_requested_action(decision, decision_text);
        actual_action = phase4_actual_action();
    }
    now = time(0);
    fputc('{', file);
#define JSON_FIELD_STRING(name, value) \
    fputs("\"" name "\":", file); \
    json_write_string(file, value); \
    fputc(',', file)
#define JSON_FIELD_UINT(name, value) \
    fprintf(file, "\"" name "\":%u,", (unsigned int)(value))
#define JSON_FIELD_INT(name, value) \
    fprintf(file, "\"" name "\":%d,", (int)(value))
#define JSON_FIELD_BOOL(name, value) \
    fprintf(file, "\"" name "\":%s,", (value) ? "true" : "false")
    JSON_FIELD_UINT("timestamp", (unsigned int)now);
    JSON_FIELD_STRING("connector", "haproxy");
    JSON_FIELD_STRING("mode", state->config.mode);
    JSON_FIELD_STRING("runtime_mode", state->config.runtime_mode);
    JSON_FIELD_STRING("variant", state->config.variant);
    JSON_FIELD_STRING("case", state->config.case_name);
    JSON_FIELD_STRING("request_id", request->request_id);
    JSON_FIELD_STRING("transaction_id", request->request_id);
    JSON_FIELD_INT("phase", decision->phase);
    JSON_FIELD_BOOL("live_executed", 1);
    JSON_FIELD_BOOL("modsecurity_processed", modsecurity_processed);
    JSON_FIELD_BOOL("request_headers_seen", !request->is_response && request->header_count > 0U);
    JSON_FIELD_BOOL("request_body_seen", !request->is_response && request->has_body);
    JSON_FIELD_BOOL("response_headers_seen", request->is_response && request->header_count > 0U);
    JSON_FIELD_BOOL("response_body_seen", request->is_response_body && request->has_body);
    JSON_FIELD_UINT("expected_status", state->config.expected_status);
    JSON_FIELD_STRING("observed_status", "");
    JSON_FIELD_STRING("result", "");
    JSON_FIELD_STRING("decision", decision_name);
    JSON_FIELD_BOOL("disruptive", decision->disruptive != 0);
    JSON_FIELD_INT("intervention_status", decision->status);
    JSON_FIELD_INT("http_status", decision->status);
    if (phase4_disruptive) {
        JSON_FIELD_STRING("requested_action", requested_action);
        JSON_FIELD_STRING("actual_action", actual_action);
        JSON_FIELD_INT("original_http_status", original_status);
        JSON_FIELD_INT("visible_http_status", strcmp(actual_action, "deny") == 0 ?
            decision->status : original_status);
        JSON_FIELD_BOOL("late_intervention", 0);
        JSON_FIELD_BOOL("headers_sent", 0);
        JSON_FIELD_BOOL("body_started", 0);
        JSON_FIELD_BOOL("response_committed", 0);
        JSON_FIELD_BOOL("connection_aborted", 0);
        JSON_FIELD_STRING("transport_result", "http_status");
    }
    JSON_FIELD_BOOL("redirect_present", decision->redirect_url[0] != '\0');
    JSON_FIELD_INT("rule_id", decision->rule_id);
    JSON_FIELD_INT("anomaly_score", decision->anomaly_score);
    JSON_FIELD_STRING("audit_log_path", state->config.audit_log);
    JSON_FIELD_STRING("haproxy_log_path", "");
    JSON_FIELD_STRING("spoa_log_path", state->config.log_file);
    JSON_FIELD_STRING("reason_code", reason_code);
    fputs("\"reason\":", file);
    json_write_string(file, reason_code);
    fputs("}\n", file);
    if (phase4_disruptive) {
        phase4_common_event_write(file, request, decision, requested_action,
            actual_action, original_status, reason_code);
    }
#undef JSON_FIELD_STRING
#undef JSON_FIELD_UINT
#undef JSON_FIELD_INT
#undef JSON_FIELD_BOOL
    fflush(file);
}

static int transaction_cache_init(agent_state *state) {
    size_t capacity;

    capacity = state->config.max_transactions > 0U ?
        state->config.max_transactions : 4096U;
    state->transactions = (transaction_slot *)calloc(capacity, sizeof(*state->transactions));
    if (state->transactions == 0) {
        return -1;
    }
    state->transaction_capacity = capacity;
    return 0;
}

static transaction_slot *transaction_slot_find(agent_state *state, const char *request_id) {
    if (state == 0 || request_id == 0 || request_id[0] == '\0') {
        return 0;
    }
    for (size_t i = 0; i < state->transaction_capacity; ++i) {
        if (state->transactions[i].transaction != 0 &&
                strcmp(state->transactions[i].request_id, request_id) == 0) {
            return &state->transactions[i];
        }
    }
    return 0;
}

static void transaction_slot_clear(transaction_slot *slot, int finish) {
    if (slot == 0) {
        return;
    }
    if (slot->transaction != 0) {
        if (finish) {
            haproxy_modsecurity_transaction_finish(slot->transaction);
        } else {
            haproxy_modsecurity_transaction_abort(slot->transaction);
        }
    }
    memset(slot, 0, sizeof(*slot));
}

static transaction_slot *transaction_slot_for_store(agent_state *state) {
    size_t oldest = 0U;

    for (size_t i = 0; i < state->transaction_capacity; ++i) {
        if (state->transactions[i].transaction == 0) {
            return &state->transactions[i];
        }
        if (state->transactions[i].updated < state->transactions[oldest].updated) {
            oldest = i;
        }
    }
    transaction_slot_clear(&state->transactions[oldest], 1);
    return &state->transactions[oldest];
}

static int transaction_cache_store(
        agent_state *state,
        const char *request_id,
        haproxy_modsecurity_transaction *transaction) {
    transaction_slot *slot;

    if (state == 0 || request_id == 0 || request_id[0] == '\0' || transaction == 0) {
        return -1;
    }
    slot = transaction_slot_find(state, request_id);
    if (slot != 0) {
        transaction_slot_clear(slot, 1);
    } else {
        slot = transaction_slot_for_store(state);
    }
    copy_spop_string(slot->request_id, sizeof(slot->request_id),
        (const unsigned char *)request_id,
        safe_cstring_length(request_id, RUNTIME_TEXT_LIMIT));
    slot->transaction = transaction;
    slot->updated = time(0);
    return 0;
}

static haproxy_modsecurity_transaction *transaction_cache_take(
        agent_state *state,
        const char *request_id) {
    transaction_slot *slot;
    haproxy_modsecurity_transaction *transaction;

    slot = transaction_slot_find(state, request_id);
    if (slot == 0) {
        return 0;
    }
    transaction = slot->transaction;
    memset(slot, 0, sizeof(*slot));
    return transaction;
}

static void transaction_cache_destroy(agent_state *state) {
    if (state == 0 || state->transactions == 0) {
        return;
    }
    for (size_t i = 0; i < state->transaction_capacity; ++i) {
        transaction_slot_clear(&state->transactions[i], 1);
    }
    free(state->transactions);
    state->transactions = 0;
    state->transaction_capacity = 0;
}

static void runtime_init_decision(
        haproxy_modsecurity_decision *decision,
        int phase,
        const char *action,
        int status,
        const char *message) {
    const char *safe_action = action != 0 ? action : "pass";
    const char *safe_message = message != 0 ? message : "";

    memset(decision, 0, sizeof(*decision));
    decision->phase = phase;
    decision->status = status;
    copy_cstring(decision->action, sizeof(decision->action), safe_action);
    copy_cstring(decision->log_message, sizeof(decision->log_message), safe_message);
}

static int handle_connection(int fd, agent_state *state, FILE *log, const char *rules_file, const char *crs_preamble_file) {
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
            notify_request request;
            haproxy_modsecurity_decision decision;
            spop_buffer ack_payload;
            int modsec_rc;

            ack_payload.len = 0;
            log_line(log, "NOTIFY received stream=%llu frame=%llu", (unsigned long long)frame.stream_id, (unsigned long long)frame.frame_id);
            if (parse_notify_payload(frame.payload, frame.payload_len, &request) != 0) {
                log_line(log, "NOTIFY request argument extraction failed");
                if (send_frame(fd, SPOP_FRM_ACK, frame.stream_id, frame.frame_id, &ack_payload) != 0) {
                    free_notify_request(&request);
                    return -1;
                }
                free_notify_request(&request);
                continue;
            }
            log_line(log,
                "NOTIFY request metadata method_present=%d path_present=%d uri_present=%d host_present=%d test_header_present=%d headers=%u body_len=%lu",
                request.has_method, request.has_path, request.has_uri,
                request.has_host, request.has_test_header,
                request.header_count, (unsigned long)request.body_len);
            if (state != 0 && state->engine != 0) {
                const char *decision_text = "pass";
                const char *reason = "";
                int modsec_processed = 0;
                int enforce = mode_enforces(&state->config);

                if (!request.has_request_id || request.request_id[0] == '\0') {
                    snprintf(request.request_id, sizeof(request.request_id),
                        "stream-%llu-frame-%llu",
                        (unsigned long long)frame.stream_id,
                        (unsigned long long)frame.frame_id);
                    request.has_request_id = 1;
                }
                if (request.is_response) {
                    haproxy_modsecurity_transaction *transaction;
                    haproxy_modsecurity_response response;

                    memset(&response, 0, sizeof(response));
                    response.status = request.has_response_status ?
                        (int)request.response_status : 200;
                    response.protocol = "HTTP/1.1";
                    response.headers = (const haproxy_modsecurity_header *)request.headers;
                    response.header_count = request.header_count;
                    response.body = request.body;
                    response.body_len = request.body_len <= 0xffffffffUL ?
                        (unsigned int)request.body_len : 0U;
                    if (state->config.response_body_limit > 0U &&
                            response.body_len > state->config.response_body_limit) {
                        response.body_len = state->config.response_body_limit;
                        reason = "response body truncated to response-body-limit";
                    }
                    transaction = transaction_cache_take(state, request.request_id);
                    if (transaction == 0) {
                        runtime_init_decision(&decision, request.is_response_body ? 4 : 3,
                            "pass", 200, "transaction_resumed=false");
                        decision_log_write(state, &request, &decision, 0,
                            "pass");
                    } else {
                        if (request.is_response_body) {
                            modsec_rc = haproxy_modsecurity_transaction_process_response_body(
                                transaction, &response, &decision);
                        } else {
                            modsec_rc = haproxy_modsecurity_transaction_process_response_headers(
                                transaction, &response, &decision);
                        }
                        if (modsec_rc != 0) {
                            modsec_processed = 0;
                            reason = decision.log_message[0] != '\0' ?
                                decision.log_message : "ModSecurity response processing failed";
                            if (fail_mode_closed(&state->config)) {
                                runtime_init_decision(&decision,
                                    request.is_response_body ? 4 : 3,
                                    "deny", 503, reason);
                                decision.disruptive = 1;
                                decision_text = "fail-closed";
                            } else {
                                runtime_init_decision(&decision,
                                    request.is_response_body ? 4 : 3,
                                    "pass", 200, reason);
                                decision_text = "fail-open";
                            }
                        } else {
                            modsec_processed = 1;
                            decision_text = decision.disruptive != 0 ?
                                decision.action : "pass";
                        }
                        if (!request.is_response_body &&
                                state->config.response_body_limit > 0U &&
                                decision.disruptive == 0) {
                            transaction_cache_store(state, request.request_id, transaction);
                        } else {
                            haproxy_modsecurity_transaction_finish(transaction);
                        }
                        decision_log_write(state, &request, &decision,
                            modsec_processed, decision_text);
                    }
                } else {
                    haproxy_modsecurity_transaction *transaction = 0;
                    haproxy_modsecurity_request modsec_request;
                    unsigned int body_len;

                    body_len = request.body_len <= 0xffffffffUL ?
                        (unsigned int)request.body_len : 0U;
                    if (body_len > state->config.request_body_limit) {
                        body_len = state->config.request_body_limit;
                        reason = "request body truncated to request-body-limit";
                    }
                    memset(&modsec_request, 0, sizeof(modsec_request));
                    modsec_request.request_id = request.request_id;
                    modsec_request.client_ip = request.has_client_ip ?
                        request.client_ip : "127.0.0.1";
                    modsec_request.client_port = request.has_client_port ?
                        (int)request.client_port : 49152;
                    modsec_request.server_ip = request.has_server_ip ?
                        request.server_ip : "127.0.0.1";
                    modsec_request.server_port = request.has_server_port ?
                        (int)request.server_port : 80;
                    modsec_request.method = request.has_method ? request.method : "GET";
                    modsec_request.uri = request.has_uri ? request.uri :
                        (request.has_path ? request.path : "/");
                    modsec_request.headers = (const haproxy_modsecurity_header *)request.headers;
                    modsec_request.header_count = request.header_count;
                    modsec_request.body = request.body;
                    modsec_request.body_len = body_len;
                    modsec_rc = haproxy_modsecurity_transaction_begin(
                        state->engine, &modsec_request, &decision, &transaction);
                    if (modsec_rc != 0) {
                        reason = decision.log_message[0] != '\0' ?
                            decision.log_message : "ModSecurity request processing failed";
                        if (transaction != 0) {
                            haproxy_modsecurity_transaction_abort(transaction);
                            transaction = 0;
                        }
                        if (fail_mode_closed(&state->config)) {
                            runtime_init_decision(&decision, 2, "deny", 503, reason);
                            decision.disruptive = 1;
                            decision_text = "fail-closed";
                        } else {
                            runtime_init_decision(&decision, 2, "pass", 200, reason);
                            decision_text = "fail-open";
                        }
                    } else {
                        modsec_processed = 1;
                        decision_text = decision.disruptive != 0 ?
                            decision.action : "pass";
                    }
                    if (transaction != 0) {
                        if (decision.disruptive != 0 ||
                                !state->config.response_phases_enabled) {
                            haproxy_modsecurity_transaction_finish(transaction);
                        } else if (transaction_cache_store(state, request.request_id, transaction) != 0) {
                            haproxy_modsecurity_transaction_finish(transaction);
                            if (fail_mode_closed(&state->config)) {
                                runtime_init_decision(&decision, 2, "deny", 503,
                                    "transaction cache store failed");
                                decision.disruptive = 1;
                                decision_text = "fail-closed";
                            } else {
                                runtime_init_decision(&decision, 2, "pass", 200,
                                    "transaction cache store failed");
                                decision_text = "fail-open";
                            }
                            reason = "transaction cache store failed";
                        }
                    }
                    decision_log_write(state, &request, &decision,
                        modsec_processed, decision_text);
                }
                if (build_decision_ack_payload(&ack_payload, &decision,
                        safe_decision_reason_code(
                            &decision, modsec_processed, decision_text),
                        enforce) != 0) {
                    log_line(log, "ACK decision variable encoding failed");
                    free_notify_request(&request);
                    return -1;
                }
                log_line(log,
                    "MODSECURITY production decision message=%s request_id=%s phase=%d disruptive=%d status=%d action=%s enforce=%d reason_code=%s",
                    request.message_name,
                    request.request_id,
                    decision.phase,
                    decision.disruptive,
                    decision.status,
                    safe_decision_name(decision_text, &decision),
                    enforce,
                    safe_decision_reason_code(
                        &decision, modsec_processed, decision_text));
                if (send_frame(fd, SPOP_FRM_ACK, frame.stream_id, frame.frame_id, &ack_payload) != 0) {
                    free_notify_request(&request);
                    return -1;
                }
                free_notify_request(&request);
                continue;
            }
            if (rules_file != 0 && rules_file[0] != '\0') {
                haproxy_modsecurity_request modsec_request;
                memset(&modsec_request, 0, sizeof(modsec_request));
                modsec_request.method = request.has_method ? request.method : "GET";
                modsec_request.uri = request.has_uri ? request.uri :
                    (request.has_path ? request.path : "/");
                modsec_request.headers = (const haproxy_modsecurity_header *)request.headers;
                modsec_request.header_count = request.header_count;
                modsec_request.body = request.body;
                modsec_request.body_len = request.body_len <= 0xffffffffUL ?
                    (unsigned int)request.body_len : 0U;
                modsec_request.rules_file = rules_file;
                log_line(log, "rules file loaded path=%s", rules_file);
                modsec_rc = haproxy_modsecurity_eval_request(&modsec_request, &decision);
            } else if ((!request.has_test_header || request.test_header[0] == '\0') &&
                    crs_preamble_file != 0 && crs_preamble_file[0] != '\0') {
                log_line(log, "CRS loaded preamble=%s", crs_preamble_file);
                modsec_rc = haproxy_modsecurity_crs_sqli_eval(
                    request.has_method ? request.method : "GET",
                    request.has_uri ? request.uri :
                        (request.has_path ? request.path : "/"),
                    request.has_host ? request.host : "localhost",
                    crs_preamble_file,
                    &decision);
                if (modsec_rc == 0) {
                    log_line(log, "CRS live decision disruptive=%d status=%d rule_id=%d",
                        decision.disruptive, decision.status, decision.rule_id);
                }
            } else {
                modsec_rc = haproxy_modsecurity_phase1_header_eval(
                    request.has_method ? request.method : "GET",
                    request.has_path ? request.path : "/",
                    request.has_test_header ? request.test_header : "",
                    &decision);
            }
            if (modsec_rc != 0) {
                log_line(log, "MODSECURITY live binding failed status=%d rule_id=%d",
                    decision.status, decision.rule_id);
                if (send_frame(fd, SPOP_FRM_ACK, frame.stream_id, frame.frame_id, &ack_payload) != 0) {
                    free_notify_request(&request);
                    return -1;
                }
                free_notify_request(&request);
                continue;
            }
            log_line(log, "MODSECURITY live decision disruptive=%d status=%d",
                decision.disruptive, decision.status);
            if (decision.disruptive != 0 && decision.status == 403) {
                if (build_set_var_blocked_payload(&ack_payload) != 0) {
                    log_line(log, "ACK set-var txn.blocked true encoding failed");
                    free_notify_request(&request);
                    return -1;
                }
                log_line(log, "ACK set-var txn.blocked true sent");
            } else {
                log_line(log, "ACK empty sent");
            }
            if (send_frame(fd, SPOP_FRM_ACK, frame.stream_id, frame.frame_id, &ack_payload) != 0) {
                free_notify_request(&request);
                return -1;
            }
            free_notify_request(&request);
            continue;
        }
        if (frame.type == SPOP_FRM_HAPROXY_DISCONNECT) {
            unsigned int status_code = 0;
            char message[256];
            parse_disconnect_payload(frame.payload, frame.payload_len,
                &status_code, message, sizeof(message));
            log_line(log, "DISCONNECT received status=%u message_present=%d",
                status_code, message[0] != '\0');
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

    if (host == 0 || host[0] == '\0') {
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

static int accept_loop(int listen_fd, agent_state *state, FILE *log, int max_connections, const char *rules_file, const char *crs_preamble_file) {
    int handled = 0;

    stop_requested = 0;
    if (install_signal_handlers() != 0) {
        log_line(log, "failed to install signal handlers errno=%d", errno);
        return 1;
    }
    while (!stop_requested && (max_connections <= 0 || handled < max_connections)) {
        int fd = accept(listen_fd, 0, 0);
        if (fd < 0) {
            if (errno == EINTR) {
                if (stop_requested) {
                    break;
                }
                continue;
            }
            log_line(log, "accept failed errno=%d", errno);
            return 1;
        }
        handle_connection(fd, state, log, rules_file, crs_preamble_file);
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

static int client_expect_ack_set_var(int fd, uint64_t stream_id, uint64_t frame_id) {
    spop_frame frame;
    spop_buffer payload;

    if (recv_frame(fd, &frame) != 0 || frame.type != SPOP_FRM_ACK ||
            frame.stream_id != stream_id || frame.frame_id != frame_id ||
            frame.payload_len > sizeof(payload.data)) {
        return -1;
    }
    payload.len = frame.payload_len;
    memcpy(payload.data, frame.payload, payload.len);
    return payload_has_set_var_blocked_true(&payload) ? 0 : -1;
}

static int run_client_self_test(unsigned int port, FILE *log) {
    int fd;
    spop_buffer empty;
    spop_buffer notify_payload;

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
    if (build_notify_request_payload(&notify_payload, "GET",
            "/haproxy-binding-self-test", "/haproxy-binding-self-test",
            "localhost", "block") != 0) {
        close(fd);
        return -1;
    }
    if (send_haproxy_hello(fd, 0) != 0 ||
        client_expect_frame(fd, SPOP_FRM_AGENT_HELLO, 0, 0) != 0 ||
        send_frame(fd, SPOP_FRM_NOTIFY, 1, 1, &notify_payload) != 0 ||
        client_expect_ack_set_var(fd, 1, 1) != 0 ||
        send_frame(fd, SPOP_FRM_HAPROXY_DISCONNECT, 0, 0, &empty) != 0 ||
        client_expect_frame(fd, SPOP_FRM_AGENT_DISCONNECT, 0, 0) != 0) {
        close(fd);
        return -1;
    }
    log_line(log, "client notify set-var ack disconnect PASS");
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
    log = open_private_file(log_path, 0);
    if (log == 0) {
        fprintf(stderr, "failed to open log: %s\n", log_path);
        return 77;
    }
    listen_fd = bind_localhost("127.0.0.1", 0, &port);
    if (listen_fd < 0) {
        fprintf(stderr, "failed to bind SPOP protocol self-test listener\n");
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
        exit(accept_loop(listen_fd, 0, log, 2, 0, 0));
    }
    close(listen_fd);
    if (run_client_self_test(port, log) != 0) {
        kill(child, SIGTERM);
        waitpid(child, &status, 0);
        fclose(log);
        fprintf(stderr, "SPOP protocol self-test failed\n");
        return 1;
    }
    waitpid(child, &status, 0);
    fclose(log);
    if (!WIFEXITED(status) || WEXITSTATUS(status) != 0) {
        fprintf(stderr, "SPOP protocol self-test child failed\n");
        return 1;
    }
    printf("haproxy_modsecurity_spoa_protocol_self_test: PASS\n");
    printf("scope: SPOP handshake and typed set-var ACK compatibility; production ModSecurity coverage is verified by live HAProxy smoke tests\n");
    printf("log: %s\n", log_path);
    printf("port_file: %s\n", port_path);
    return 0;
}

static int run_server(
        const char *host,
        unsigned int port,
        const char *ready_file,
        const char *pid_file,
        const char *port_file,
        const char *log_file,
        const char *rules_file,
        const char *crs_preamble_file) {
    int listen_fd;
    unsigned int bound_port;
    FILE *log;

    log = open_private_file(log_file, 1);
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
    log_line(log, "legacy SPOP compatibility server listening on %s:%u rules_file=%s", host, bound_port, rules_file != 0 ? rules_file : "");
    accept_loop(listen_fd, 0, log, 0, rules_file, crs_preamble_file);
    close(listen_fd);
    fclose(log);
    return 0;
}

static FILE *open_append_file_or_standard(const char *path, FILE *standard_file) {
    char dir[4096];

    if (path == 0 || path[0] == '\0') {
        return 0;
    }
    if (strcmp(path, "-") == 0) {
        return standard_file;
    }
    if (dirname_to_buffer(path, dir, sizeof(dir)) != 0 || mkdir_p(dir) != 0) {
        return 0;
    }
    return open_private_file(path, 1);
}

static int run_agent_server(const agent_config *config) {
    int listen_fd;
    unsigned int bound_port;
    FILE *log;
    FILE *decision_log = 0;
    int log_owned;
    int decision_log_owned = 0;
    agent_state state;
    haproxy_modsecurity_engine_config engine_config;
    haproxy_modsecurity_decision decision;
    int rc;

    memset(&state, 0, sizeof(state));
    state.config = *config;
    log = open_append_file_or_standard(config->log_file, stderr);
    if (log == 0) {
        if (stderr != NULL) {
            fprintf(stderr, "failed to open log: %s\n", config->log_file);
        }
        return 77;
    }
    log_owned = log != stderr;
    if (config->decision_log[0] != '\0') {
        decision_log = open_append_file_or_standard(config->decision_log, stdout);
        if (decision_log == 0) {
            if (stderr != NULL) {
                fprintf(stderr, "failed to open decision log: %s\n",
                    config->decision_log);
            }
            close_owned_stream(&log, log_owned);
            return 77;
        }
        decision_log_owned = decision_log != stdout;
    }
    state.log = log;
    state.decision_log = decision_log;

    memset(&engine_config, 0, sizeof(engine_config));
    engine_config.connector_info = "HAProxy ModSecurity SPOA production agent";
    engine_config.modsecurity_conf = config->modsecurity_conf;
    engine_config.crs_root = config->crs_root;
    engine_config.rules_file = config->rules_file;
    engine_config.rules_dir = config->rules_dir;
    if (haproxy_modsecurity_engine_create(&engine_config, &state.engine, &decision) != 0) {
        fprintf(stderr, "failed to initialize ModSecurity engine: %s\n",
            decision.log_message[0] != '\0' ? decision.log_message : "unknown");
        close_owned_stream(&decision_log, decision_log_owned);
        close_owned_stream(&log, log_owned);
        return 77;
    }
    if (transaction_cache_init(&state) != 0) {
        fprintf(stderr, "failed to allocate transaction cache\n");
        haproxy_modsecurity_engine_destroy(state.engine);
        close_owned_stream(&decision_log, decision_log_owned);
        close_owned_stream(&log, log_owned);
        return 77;
    }

    listen_fd = bind_localhost(config->host, config->port, &bound_port);
    if (listen_fd < 0) {
        fprintf(stderr, "failed to bind %s:%u\n", config->host, config->port);
        transaction_cache_destroy(&state);
        haproxy_modsecurity_engine_destroy(state.engine);
        close_owned_stream(&decision_log, decision_log_owned);
        close_owned_stream(&log, log_owned);
        return 77;
    }
    if ((config->pid_file[0] != '\0' && write_text_file(config->pid_file, "%ld\n", (long)getpid()) != 0) ||
        (config->port_file[0] != '\0' && write_text_file(config->port_file, "%u\n", bound_port) != 0) ||
        (config->ready_file[0] != '\0' && write_text_file(config->ready_file, "ready\n") != 0)) {
        close(listen_fd);
        transaction_cache_destroy(&state);
        haproxy_modsecurity_engine_destroy(state.engine);
        close_owned_stream(&decision_log, decision_log_owned);
        close_owned_stream(&log, log_owned);
        return 77;
    }
    log_line(log,
        "HAProxy ModSecurity SPOA production agent listening on %s:%u rules_file=%s rules_dir=%s modsecurity_conf=%s crs_root=%s mode=%s fail_mode=%s response_phases=%d response_body_limit=%u",
        config->host, bound_port, config->rules_file, config->rules_dir,
        config->modsecurity_conf, config->crs_root, config->mode,
        config->fail_mode, config->response_phases_enabled,
        config->response_body_limit);
    rc = accept_loop(listen_fd, &state, log, 0, 0, 0);
    close(listen_fd);
    transaction_cache_destroy(&state);
    haproxy_modsecurity_engine_destroy(state.engine);
    close_owned_stream(&decision_log, decision_log_owned);
    close_owned_stream(&log, log_owned);
    return rc;
}

static void print_usage(const char *program) {
    fprintf(stderr, "usage: %s --describe|--runtime-self-test --tmp-root PATH --log-root PATH|--serve --host 127.0.0.1 --port PORT --ready-file PATH --pid-file PATH --port-file PATH --log-file PATH [--rules-file PATH] [--crs-preamble-file PATH]|--listen HOST:PORT [--config PATH] [--rules-file PATH] [--rules-dir PATH] [--modsecurity-conf PATH] [--crs-root PATH] [--decision-log PATH] [--log-file -|PATH] [--mode block|detect-only] [--fail-mode open|closed]\n", program);
}

int main(int argc, char **argv) {
    if (argc == 2 && strcmp(argv[1], "--describe") == 0) {
        printf("HAProxy ModSecurity SPOA production agent\n");
        printf("features: startup-loaded libmodsecurity rules, request phases, response headers, audit/decision logs; selected SPOP response-body inspection disabled\n");
        printf("compatibility: --runtime-self-test exercises only SPOP handshake and typed set-var ACK behavior\n");
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

    if (argc >= 2 && strcmp(argv[1], "--serve") != 0) {
        agent_config config;
        int i;
        int production_args = 0;

        config_init(&config);
        for (i = 1; i < argc; ++i) {
            if (strcmp(argv[i], "--config") == 0 && i + 1 < argc) {
                if (load_config_file(&config, argv[++i]) != 0) {
                    fprintf(stderr, "failed to load config file: %s\n", argv[i]);
                    return 2;
                }
                production_args = 1;
            }
        }
        for (i = 1; i < argc; ++i) {
            const char *key = 0;
            const char *value = 0;
            if (strcmp(argv[i], "--config") == 0 && i + 1 < argc) {
                i++;
                continue;
            }
            if (strcmp(argv[i], "--debug") == 0) {
                config.debug = 1;
                production_args = 1;
                continue;
            }
            if (strcmp(argv[i], "--enable-response-headers") == 0) {
                config.response_phases_enabled = 1;
                production_args = 1;
                continue;
            }
            if (strncmp(argv[i], "--", 2) != 0) {
                print_usage(argv[0]);
                return 2;
            }
            if (i + 1 >= argc) {
                print_usage(argv[0]);
                return 2;
            }
            key = argv[i] + 2;
            value = argv[++i];
            if (config_set(&config, key, value) != 0) {
                print_usage(argv[0]);
                return 2;
            }
            production_args = 1;
        }
        if (production_args) {
            if (config.port == 0U ||
                    (config.rules_file[0] == '\0' &&
                     config.rules_dir[0] == '\0' &&
                     config.modsecurity_conf[0] == '\0' &&
                     config.crs_root[0] == '\0')) {
                print_usage(argv[0]);
                return 2;
            }
            return run_agent_server(&config);
        }
    }

    if (argc >= 2 && strcmp(argv[1], "--serve") == 0) {
        const char *host = "127.0.0.1";
        const char *ready_file = 0;
        const char *pid_file = 0;
        const char *port_file = 0;
        const char *log_file = 0;
        const char *rules_file = 0;
        const char *crs_preamble_file = 0;
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
            } else if (strcmp(argv[i], "--rules-file") == 0 && i + 1 < argc) {
                rules_file = argv[++i];
            } else if (strcmp(argv[i], "--crs-preamble-file") == 0 && i + 1 < argc) {
                crs_preamble_file = argv[++i];
            } else {
                print_usage(argv[0]);
                return 2;
            }
        }
        if (ready_file == 0 || pid_file == 0 || port_file == 0 || log_file == 0) {
            print_usage(argv[0]);
            return 2;
        }
        return run_server(host, port, ready_file, pid_file, port_file, log_file, rules_file, crs_preamble_file);
    }

    print_usage(argv[0]);
    return 2;
}
