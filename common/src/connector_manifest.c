#include "msconnector/connector_manifest.h"
#include "msconnector/json_escape.h"
#include <stdio.h>
#include <string.h>

#define FIELD_SIZE 128U

static int nonempty(const char *value)
{
    return value != 0 && value[0] != '\0';
}

static void escape_manifest_field(const char *src, char *dst, size_t dst_size, int *truncated)
{
    const size_t needed = msconnector_json_escape(src, dst, dst_size);

    if (truncated != 0 && (dst_size == 0U || needed >= dst_size)) {
        *truncated = 1;
    }
}

void msconnector_connector_manifest_init(msconnector_connector_manifest *manifest)
{
    if (manifest != 0) {
        memset(manifest, 0, sizeof(*manifest));
    }
}

int msconnector_connector_manifest_from_metadata(
    msconnector_connector_manifest *out,
    const msconnector_adapter_metadata *metadata)
{
    if (out == 0 || !msconnector_adapter_metadata_is_complete(metadata)) {
        return 0;
    }

    out->connector = metadata->connector_name;
    out->server_family = metadata->server_family;
    out->source_kind = metadata->source_kind;
    out->build_status = metadata->build_status;
    out->runtime_status = metadata->runtime_status;
    out->verification_status = metadata->verification_status;
    out->capabilities = metadata->capabilities.flags;
    return 1;
}

int msconnector_connector_manifest_write_json(
    const msconnector_connector_manifest *manifest,
    char *dst,
    size_t dst_size,
    int *truncated)
{
    char connector[FIELD_SIZE];
    char server_family[FIELD_SIZE];
    char source_kind[FIELD_SIZE];
    char build_status[FIELD_SIZE];
    char runtime_status[FIELD_SIZE];
    char verification_status[FIELD_SIZE];
    int was_truncated = 0;
    int written;

    if (truncated != 0) {
        *truncated = 0;
    }
    if (dst != 0 && dst_size > 0U) {
        dst[0] = '\0';
    }
    if (manifest == 0 || dst == 0 || dst_size == 0U || !nonempty(manifest->connector)) {
        return 0;
    }

    escape_manifest_field(manifest->connector, connector, FIELD_SIZE, &was_truncated);
    escape_manifest_field(manifest->server_family, server_family, FIELD_SIZE, &was_truncated);
    escape_manifest_field(manifest->source_kind, source_kind, FIELD_SIZE, &was_truncated);
    escape_manifest_field(manifest->build_status, build_status, FIELD_SIZE, &was_truncated);
    escape_manifest_field(manifest->runtime_status, runtime_status, FIELD_SIZE, &was_truncated);
    escape_manifest_field(manifest->verification_status, verification_status, FIELD_SIZE, &was_truncated);

    written = snprintf(
        dst,
        dst_size,
        "{\"connector\":\"%s\",\"server_family\":\"%s\",\"source_kind\":\"%s\",\"build_status\":\"%s\",\"runtime_status\":\"%s\",\"verification_status\":\"%s\",\"capabilities\":%llu}",
        connector,
        server_family,
        source_kind,
        build_status,
        runtime_status,
        verification_status,
        (unsigned long long)manifest->capabilities);
    if (written < 0 || (size_t)written >= dst_size) {
        was_truncated = 1;
    }
    if (truncated != 0) {
        *truncated = was_truncated;
    }
    return was_truncated ? 0 : 1;
}
