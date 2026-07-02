#include "msconnector/connector_manifest.h"
#include "msconnector/json_escape.h"
#include <stdio.h>
#include <string.h>
#define F 128U
static int nonempty(const char *v) { return v != 0 && v[0] != '\0'; }
static void esc(const char *s, char *d, size_t n, int *t) { size_t need = msconnector_json_escape(s, d, n); if ((n == 0U || need >= n) && t != 0) { *t = 1; } }
void msconnector_connector_manifest_init(msconnector_connector_manifest *manifest) { if (manifest != 0) { memset(manifest, 0, sizeof(*manifest)); } }
int msconnector_connector_manifest_from_metadata(msconnector_connector_manifest *out, const msconnector_adapter_metadata *metadata) {
    if (out == 0 || !msconnector_adapter_metadata_is_complete(metadata)) { return 0; }
    out->connector = metadata->connector_name; out->server_family = metadata->server_family; out->source_kind = metadata->source_kind; out->build_status = metadata->build_status; out->runtime_status = metadata->runtime_status; out->verification_status = metadata->verification_status; out->capabilities = metadata->capabilities.flags; return 1;
}
int msconnector_connector_manifest_write_json(const msconnector_connector_manifest *m, char *dst, size_t size, int *truncated) {
    char c[F], s[F], k[F], b[F], r[F], v[F]; int was = 0; int written;
    if (truncated != 0) { *truncated = 0; } if (dst != 0 && size > 0U) { dst[0] = '\0'; }
    if (m == 0 || dst == 0 || size == 0U || !nonempty(m->connector)) { return 0; }
    esc(m->connector,c,F,&was); esc(m->server_family,s,F,&was); esc(m->source_kind,k,F,&was); esc(m->build_status,b,F,&was); esc(m->runtime_status,r,F,&was); esc(m->verification_status,v,F,&was);
    written = snprintf(dst,size,"{\"connector\":\"%s\",\"server_family\":\"%s\",\"source_kind\":\"%s\",\"build_status\":\"%s\",\"runtime_status\":\"%s\",\"verification_status\":\"%s\",\"capabilities\":%llu}",c,s,k,b,r,v,(unsigned long long)m->capabilities);
    if (written < 0 || (size_t)written >= size) { was = 1; } if (truncated != 0) { *truncated = was; } return !was;
}
