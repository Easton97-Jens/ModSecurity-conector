#ifndef MSCONNECTOR_ADAPTER_CONTRACT_H
#define MSCONNECTOR_ADAPTER_CONTRACT_H

#include "msconnector/adapter.h"

#ifdef __cplusplus
extern "C" {
#endif

typedef struct msconnector_adapter_contract_result {
    int ok;
    const char *message;
} msconnector_adapter_contract_result;

void msconnector_adapter_contract_result_init(msconnector_adapter_contract_result *result);
int msconnector_adapter_contract_validate(const msconnector_adapter *adapter, msconnector_adapter_contract_result *result);

#ifdef __cplusplus
}
#endif

#endif
