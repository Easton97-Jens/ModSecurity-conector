#include "msconnector/path_policy.h"
#include <string.h>

int msconnector_path_is_empty(const char *path) {
    return path == 0 || path[0] == '\0';
}

int msconnector_path_is_absolute(const char *path) {
    return path != 0 && (path[0] == '/' || (path[0] != '\0' && path[1] == ':'));
}

int msconnector_path_has_parent_reference(const char *path) {
    const char *last_segment;

    if (path == 0) {
        return 0;
    }

    if (strcmp(path, "..") == 0) {
        return 1;
    }

    if (strncmp(path, "../", 3U) == 0) {
        return 1;
    }

    if (strstr(path, "/../") != 0) {
        return 1;
    }

    last_segment = path + strlen(path);
    return last_segment >= path + 3 && strcmp(last_segment - 3, "/..") == 0;
}
