#ifndef MSCONNECTOR_BUILD_CONTRACT_H
#define MSCONNECTOR_BUILD_CONTRACT_H
#include <stddef.h>
#ifdef __cplusplus
extern "C" {
#endif
const char *msconnector_build_contract_target_name(unsigned int index);
size_t msconnector_build_contract_target_count(void);
int msconnector_build_contract_target_is_standard(const char *name);
#ifdef __cplusplus
}
#endif
#endif
