#ifndef MSCONNECTOR_RUNTIME_PATHS_H
#define MSCONNECTOR_RUNTIME_PATHS_H

#include <stddef.h>

#ifdef __cplusplus
extern "C" {
#endif

int msconnector_runtime_path_join(const char *root, const char *name, char *out, size_t out_len);

#ifdef __cplusplus
}
#endif

#endif
