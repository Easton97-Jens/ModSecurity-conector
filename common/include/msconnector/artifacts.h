#ifndef MSCONNECTOR_ARTIFACTS_H
#define MSCONNECTOR_ARTIFACTS_H
#ifdef __cplusplus
extern "C" {
#endif
/* Relative artifact file-name defaults only; no absolute paths or file I/O. */
typedef struct msconnector_artifact_paths { const char *result_json; const char *decision_jsonl; const char *audit_log; const char *error_log; const char *runtime_stdout_log; const char *runtime_stderr_log; } msconnector_artifact_paths;
void msconnector_artifact_paths_init(msconnector_artifact_paths *paths);
const char *msconnector_artifact_default_result_json(void);
const char *msconnector_artifact_default_decision_jsonl(void);
#ifdef __cplusplus
}
#endif
#endif
