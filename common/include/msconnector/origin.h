#ifndef MSCONNECTOR_ORIGIN_H
#define MSCONNECTOR_ORIGIN_H

#ifdef __cplusplus
extern "C" {
#endif

typedef struct msconnector_origin {
    const char *component;
    const char *source_repository;
    const char *source_branch;
    const char *source_commit;
    const char *source_describe;
    const char *license;
} msconnector_origin;

msconnector_origin msconnector_origin_make(
    const char *component,
    const char *source_repository,
    const char *source_branch,
    const char *source_commit,
    const char *source_describe,
    const char *license);
int msconnector_origin_is_empty(const msconnector_origin *origin);

#ifdef __cplusplus
}
#endif

#endif
