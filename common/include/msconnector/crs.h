#ifndef MSCONNECTOR_CRS_H
#define MSCONNECTOR_CRS_H

#include <stddef.h>

#ifdef __cplusplus
extern "C" {
#endif

/* Neutral CRS/ruleset setup convention. Validation only checks configuration
 * consistency; it does not load CRS, verify a runtime, or create CRS pass,
 * production, or full-matrix claims for any connector.
 */
typedef enum msconnector_crs_mode {
    MSCONNECTOR_CRS_DISABLED = 0,
    MSCONNECTOR_CRS_EXTERNAL_PATH,
    MSCONNECTOR_CRS_BUNDLED_PATH,
    MSCONNECTOR_CRS_TEST_FIXTURE
} msconnector_crs_mode;

typedef struct msconnector_crs_config {
    msconnector_crs_mode mode;
    const char *setup_conf_path;
    const char *rules_dir;
    const char *preamble_inline;
    int include_recommended_setup;
} msconnector_crs_config;

void msconnector_crs_config_init(msconnector_crs_config *cfg);
int msconnector_crs_config_validate(const msconnector_crs_config *cfg, char *error, size_t error_len);
const char *msconnector_crs_mode_name(msconnector_crs_mode mode);

#ifdef __cplusplus
}
#endif

#endif
