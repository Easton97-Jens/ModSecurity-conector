#include "msconnector/origin.h"

static int field_is_empty(const char *field) {
    return field == 0 || field[0] == '\0';
}

msconnector_origin msconnector_origin_make(
    const char *component,
    const char *source_repository,
    const char *source_branch,
    const char *source_commit,
    const char *source_describe,
    const char *license) {
    msconnector_origin origin;
    origin.component = component;
    origin.source_repository = source_repository;
    origin.source_branch = source_branch;
    origin.source_commit = source_commit;
    origin.source_describe = source_describe;
    origin.license = license;
    return origin;
}

int msconnector_origin_is_empty(const msconnector_origin *origin) {
    return origin == 0 ||
        (field_is_empty(origin->component) &&
         field_is_empty(origin->source_repository) &&
         field_is_empty(origin->source_branch) &&
         field_is_empty(origin->source_commit) &&
         field_is_empty(origin->source_describe) &&
         field_is_empty(origin->license));
}
