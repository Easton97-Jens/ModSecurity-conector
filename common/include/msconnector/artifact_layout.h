#ifndef MSCONNECTOR_ARTIFACT_LAYOUT_H
#define MSCONNECTOR_ARTIFACT_LAYOUT_H

#ifdef __cplusplus
extern "C" {
#endif

typedef struct msconnector_artifact_layout {
    const char *result_json;
    const char *decision_jsonl;
    const char *audit_log;
    const char *error_log;
    const char *runtime_stdout_log;
    const char *runtime_stderr_log;
    const char *server_config;
    const char *connector_config;
} msconnector_artifact_layout;

void msconnector_artifact_layout_init(msconnector_artifact_layout *layout);
const char *msconnector_artifact_name_result_json(void);
const char *msconnector_artifact_name_decision_jsonl(void);
const char *msconnector_artifact_name_audit_log(void);
const char *msconnector_artifact_name_error_log(void);
const char *msconnector_artifact_name_runtime_stdout_log(void);
const char *msconnector_artifact_name_runtime_stderr_log(void);
const char *msconnector_artifact_name_server_config(void);
const char *msconnector_artifact_name_connector_config(void);

#ifdef __cplusplus
}
#endif

#endif
