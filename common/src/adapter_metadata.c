#include "msconnector/adapter_metadata.h"

static int string_is_nonempty(const char *value) { return value != 0 && value[0] != '\0'; }

void msconnector_adapter_metadata_init(msconnector_adapter_metadata *metadata) {
    if (metadata == 0) { return; }
    metadata->origin.component = 0; metadata->origin.source_repository = 0; metadata->origin.source_branch = 0; metadata->origin.source_commit = 0; metadata->origin.source_describe = 0; metadata->origin.license = 0;
    metadata->capabilities.flags = MSCONNECTOR_CAPABILITY_NONE; metadata->capabilities.connector_name = 0; metadata->capabilities.connector_version = 0; metadata->capabilities.server_family = 0; metadata->capabilities.notes = 0;
    metadata->connector_name = 0; metadata->server_family = 0; metadata->source_kind = 0; metadata->imported_path = 0; metadata->integration_path = 0; metadata->build_status = 0; metadata->runtime_status = 0; metadata->verification_status = 0;
}

int msconnector_adapter_metadata_is_complete(const msconnector_adapter_metadata *metadata) {
    return metadata != 0 &&
        string_is_nonempty(metadata->connector_name) &&
        string_is_nonempty(metadata->server_family) &&
        string_is_nonempty(metadata->source_kind) &&
        string_is_nonempty(metadata->imported_path) &&
        string_is_nonempty(metadata->build_status) &&
        string_is_nonempty(metadata->runtime_status) &&
        string_is_nonempty(metadata->verification_status);
}
