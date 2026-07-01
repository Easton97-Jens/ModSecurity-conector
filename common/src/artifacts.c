#include "msconnector/artifacts.h"
void msconnector_artifact_paths_init(msconnector_artifact_paths *p) { if (p) { p->result_json = "result.json"; p->decision_jsonl = "decision.jsonl"; p->audit_log = "audit.log"; p->error_log = "error.log"; p->runtime_stdout_log = "runtime.stdout.log"; p->runtime_stderr_log = "runtime.stderr.log"; } }
const char *msconnector_artifact_default_result_json(void) { return "result.json"; }
const char *msconnector_artifact_default_decision_jsonl(void) { return "decision.jsonl"; }
