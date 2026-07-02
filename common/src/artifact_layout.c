#include "msconnector/artifact_layout.h"

const char *msconnector_artifact_name_result_json(void) { return "result.json"; }
const char *msconnector_artifact_name_decision_jsonl(void) { return "decision.jsonl"; }
const char *msconnector_artifact_name_audit_log(void) { return "audit.log"; }
const char *msconnector_artifact_name_error_log(void) { return "error.log"; }
const char *msconnector_artifact_name_runtime_stdout_log(void) { return "runtime.stdout.log"; }
const char *msconnector_artifact_name_runtime_stderr_log(void) { return "runtime.stderr.log"; }
const char *msconnector_artifact_name_server_config(void) { return "server-config.conf"; }
const char *msconnector_artifact_name_connector_config(void) { return "connector-config.conf"; }

void msconnector_artifact_layout_init(msconnector_artifact_layout *layout) {
    if (layout == 0) { return; }
    layout->result_json = msconnector_artifact_name_result_json();
    layout->decision_jsonl = msconnector_artifact_name_decision_jsonl();
    layout->audit_log = msconnector_artifact_name_audit_log();
    layout->error_log = msconnector_artifact_name_error_log();
    layout->runtime_stdout_log = msconnector_artifact_name_runtime_stdout_log();
    layout->runtime_stderr_log = msconnector_artifact_name_runtime_stderr_log();
    layout->server_config = msconnector_artifact_name_server_config();
    layout->connector_config = msconnector_artifact_name_connector_config();
}
