#include "msconnector/build_contract.h"
#include <string.h>
static const char *targets[] = {"build-metadata","build-starter","build-runtime","self-test","self-test-runtime","smoke","clean"};
const char *msconnector_build_contract_target_name(unsigned int index) { return index < (unsigned int)(sizeof(targets)/sizeof(targets[0])) ? targets[index] : 0; }
size_t msconnector_build_contract_target_count(void) { return sizeof(targets)/sizeof(targets[0]); }
int msconnector_build_contract_target_is_standard(const char *name) { if (name == 0) { return 0; } for (size_t i = 0; i < msconnector_build_contract_target_count(); ++i) { if (strcmp(name, targets[i]) == 0) { return 1; } } return 0; }
