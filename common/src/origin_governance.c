#include "msconnector/origin_governance.h"
#include <string.h>
static int nonempty(const char *v) { return v != 0 && v[0] != '\0'; }
void msconnector_origin_governance_init(msconnector_origin_governance *g) { if (g != 0) { memset(g, 0, sizeof(*g)); } }
int msconnector_origin_governance_is_complete(const msconnector_origin_governance *g) { return g != 0 && nonempty(g->source_repository) && nonempty(g->source_branch) && nonempty(g->source_commit) && nonempty(g->source_describe) && nonempty(g->license) && nonempty(g->imported_path) && nonempty(g->source_kind); }
int msconnector_origin_governance_from_metadata(msconnector_origin_governance *out, const msconnector_adapter_metadata *m) { if (out == 0 || m == 0) { return 0; } out->source_repository = m->origin.source_repository; out->source_branch = m->origin.source_branch; out->source_commit = m->origin.source_commit; out->source_describe = m->origin.source_describe; out->license = m->origin.license; out->imported_path = m->imported_path; out->source_kind = m->source_kind; out->upstream_base = 0; out->local_modifications = 0; out->patches_applied = 0; return msconnector_origin_governance_is_complete(out); }
