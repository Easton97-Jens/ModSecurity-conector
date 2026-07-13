#ifndef MSCONNECTOR_CONFIG_PARSER_H
#define MSCONNECTOR_CONFIG_PARSER_H
#include "msconnector/options.h"
#include <stddef.h>
#ifdef __cplusplus
extern "C" {
#endif
int msconnector_parse_bool(const char *value, enum msconnector_bool_option *out);
int msconnector_parse_phase4_mode(const char *value, enum msconnector_phase4_mode *out);
int msconnector_parse_size(const char *value, size_t *out);
int msconnector_parse_nonnegative_size(const char *value, size_t *out);
int msconnector_parse_http_status(const char *value, int *out);
int msconnector_validate_content_type_token(const char *value);
#ifdef __cplusplus
}
#endif
#endif
