#ifndef MSCONNECTOR_LIFECYCLE_STATUS_H
#define MSCONNECTOR_LIFECYCLE_STATUS_H
#ifdef __cplusplus
extern "C" {
#endif
/* Status vocabulary only; no current connector status is implied by these enums. */
typedef enum msconnector_build_status { MSCONNECTOR_BUILD_STATUS_NOT_STARTED = 0, MSCONNECTOR_BUILD_STATUS_STARTER = 1, MSCONNECTOR_BUILD_STATUS_COMPILES = 2, MSCONNECTOR_BUILD_STATUS_LINKS = 3, MSCONNECTOR_BUILD_STATUS_RUNTIME_READY = 4 } msconnector_build_status;
typedef enum msconnector_runtime_status { MSCONNECTOR_RUNTIME_STATUS_NOT_VERIFIED = 0, MSCONNECTOR_RUNTIME_STATUS_SELF_TEST_ONLY = 1, MSCONNECTOR_RUNTIME_STATUS_SMOKE_VERIFIED = 2, MSCONNECTOR_RUNTIME_STATUS_MATRIX_VERIFIED = 3 } msconnector_runtime_status;
typedef enum msconnector_verification_status { MSCONNECTOR_VERIFICATION_STATUS_NONE = 0, MSCONNECTOR_VERIFICATION_STATUS_STATIC_ONLY = 1, MSCONNECTOR_VERIFICATION_STATUS_SELF_TEST = 2, MSCONNECTOR_VERIFICATION_STATUS_RUNTIME_SMOKE = 3, MSCONNECTOR_VERIFICATION_STATUS_FULL_MATRIX = 4 } msconnector_verification_status;
const char *msconnector_build_status_name(msconnector_build_status status);
const char *msconnector_runtime_status_name(msconnector_runtime_status status);
const char *msconnector_verification_status_name(msconnector_verification_status status);
#ifdef __cplusplus
}
#endif
#endif
