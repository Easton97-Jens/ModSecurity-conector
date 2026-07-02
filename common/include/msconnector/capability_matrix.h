#ifndef MSCONNECTOR_CAPABILITY_MATRIX_H
#define MSCONNECTOR_CAPABILITY_MATRIX_H

#include "msconnector/capabilities.h"

#ifdef __cplusplus
extern "C" {
#endif

const char *msconnector_capability_required_test(enum msconnector_capability_flag flag);
int msconnector_capability_has_required_test(enum msconnector_capability_flag flag);

#ifdef __cplusplus
}
#endif

#endif
