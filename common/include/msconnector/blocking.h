#ifndef MSCONNECTOR_BLOCKING_H
#define MSCONNECTOR_BLOCKING_H

#include "msconnector/block_statuses.h"

#ifdef __cplusplus
extern "C" {
#endif

enum msconnector_block_action {
    MSCONNECTOR_BLOCK_ACTION_DENY = 0,
    MSCONNECTOR_BLOCK_ACTION_REDIRECT = 1,
    MSCONNECTOR_BLOCK_ACTION_DROP = 2,
    MSCONNECTOR_BLOCK_ACTION_LOG_ONLY = 3,
    MSCONNECTOR_BLOCK_ACTION_ABORT_CONNECTION = 4
};

typedef struct msconnector_blocking_policy {
    enum msconnector_block_action action;
    int status;
} msconnector_blocking_policy;

const char *msconnector_block_action_name(enum msconnector_block_action action);
int msconnector_block_action_is_disruptive(enum msconnector_block_action action);
msconnector_blocking_policy msconnector_blocking_policy_make(
    enum msconnector_block_action action,
    int requested_status);

#ifdef __cplusplus
}
#endif

#endif
