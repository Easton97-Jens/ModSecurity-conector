#ifndef MSCONNECTOR_RULE_ERROR_H
#define MSCONNECTOR_RULE_ERROR_H
#include "msconnector/error.h"
#ifdef __cplusplus
extern "C" {
#endif
void msconnector_rule_error_set_parse_failed(msconnector_error *error, const char *source);
void msconnector_rule_error_set_load_failed(msconnector_error *error, const char *source);
void msconnector_rule_error_clear(msconnector_error *error);
#ifdef __cplusplus
}
#endif
#endif
