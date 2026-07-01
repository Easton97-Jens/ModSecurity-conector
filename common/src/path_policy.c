#include "msconnector/path_policy.h"
#include <string.h>

int msconnector_path_is_empty(const char *path) {
    return path == 0 || path[0] == '\0';
}

int msconnector_path_is_absolute(const char *path) {
    return path != 0 && (path[0] == '/' || (path[0] != '\0' && path[1] == ':'));
}

static int is_path_separator(char value) {
    return value == '/' || value == '\\';
}

int msconnector_path_has_parent_reference(const char *path) {
    size_t segment_start = 0U;

    if (path == 0) {
        return 0;
    }

    for (size_t index = 0U; ; ++index) {
        if (path[index] == '\0' || is_path_separator(path[index])) {
            const size_t segment_size = index - segment_start;
            if (segment_size == 2U &&
                path[segment_start] == '.' &&
                path[segment_start + 1U] == '.') {
                return 1;
            }
            if (path[index] == '\0') {
                break;
            }
            segment_start = index + 1U;
        }
    }

    return 0;
}
