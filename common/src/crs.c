#include "msconnector/crs.h"

#include <stdio.h>

static void set_error(char *error, size_t error_len, const char *message) { if (error != 0 && error_len > 0U) { (void)snprintf(error, error_len, "%s", message); } }
static int empty(const char *value) { return value == 0 || value[0] == '\0'; }

void msconnector_crs_config_init(msconnector_crs_config *cfg) {
    if (cfg == 0) { return; }
    cfg->mode = MSCONNECTOR_CRS_DISABLED;
    cfg->setup_conf_path = 0;
    cfg->rules_dir = 0;
    cfg->preamble_inline = 0;
    cfg->include_recommended_setup = 0;
}

const char *msconnector_crs_mode_name(msconnector_crs_mode mode) {
    switch (mode) {
    case MSCONNECTOR_CRS_DISABLED: return "disabled";
    case MSCONNECTOR_CRS_EXTERNAL_PATH: return "external_path";
    case MSCONNECTOR_CRS_BUNDLED_PATH: return "bundled_path";
    case MSCONNECTOR_CRS_TEST_FIXTURE: return "test_fixture";
    }
    return "unknown";
}

int msconnector_crs_config_validate(const msconnector_crs_config *cfg, char *error, size_t error_len) {
    if (cfg == 0) { set_error(error, error_len, "missing config"); return 0; }
    if (cfg->mode < MSCONNECTOR_CRS_DISABLED || cfg->mode > MSCONNECTOR_CRS_TEST_FIXTURE) { set_error(error, error_len, "invalid mode"); return 0; }
    if (cfg->mode == MSCONNECTOR_CRS_DISABLED) {
        if (!empty(cfg->setup_conf_path) || !empty(cfg->rules_dir) || cfg->include_recommended_setup) { set_error(error, error_len, "disabled has paths"); return 0; }
        return 1;
    }
    if ((cfg->mode == MSCONNECTOR_CRS_EXTERNAL_PATH || cfg->mode == MSCONNECTOR_CRS_BUNDLED_PATH) &&
        empty(cfg->setup_conf_path) &&
        empty(cfg->rules_dir)) { set_error(error, error_len, "missing crs path"); return 0; }
    if (cfg->mode == MSCONNECTOR_CRS_TEST_FIXTURE &&
        empty(cfg->setup_conf_path) &&
        empty(cfg->rules_dir) &&
        empty(cfg->preamble_inline)) { set_error(error, error_len, "missing fixture rules"); return 0; }
    return 1;
}
