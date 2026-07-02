#include "msconnector/runtime_paths.h"
#include "msconnector/path_policy.h"
#include <stdio.h>
#include <string.h>

int msconnector_runtime_path_join(const char *root, const char *name, char *out, size_t out_len) {
    int written;
    size_t root_len;
    const char *separator;
    if (out != 0 && out_len > 0) { out[0] = '\0'; }
    if (root == 0 || root[0] == '\0' || name == 0 || name[0] == '\0' || out == 0 || out_len == 0) { return 0; }
    if (msconnector_path_is_absolute(name) || msconnector_path_has_parent_reference(name)) { return 0; }
    root_len = strlen(root);
    separator = (root_len > 0U && (root[root_len - 1U] == '/' || root[root_len - 1U] == '\\')) ? "" : "/";
    written = snprintf(out, out_len, "%s%s%s", root, separator, name);
    if (written < 0 || (size_t)written >= out_len) { out[out_len - 1U] = '\0'; return 0; }
    return 1;
}
