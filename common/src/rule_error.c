#include "msconnector/rule_error.h"
void msconnector_rule_error_set_parse_failed(msconnector_error *error, const char *source) { msconnector_error_set(error, MSCONNECTOR_ERROR_RULE_PARSE_FAILED, msconnector_error_default_message(MSCONNECTOR_ERROR_RULE_PARSE_FAILED), source); }
void msconnector_rule_error_set_load_failed(msconnector_error *error, const char *source) { msconnector_error_set(error, MSCONNECTOR_ERROR_RULE_LOAD_FAILED, msconnector_error_default_message(MSCONNECTOR_ERROR_RULE_LOAD_FAILED), source); }
void msconnector_rule_error_clear(msconnector_error *error) { msconnector_error_init(error); }
