#ifndef MSCONNECTOR_RULE_LOAD_STATS_H
#define MSCONNECTOR_RULE_LOAD_STATS_H

#ifdef __cplusplus
extern "C" {
#endif

typedef struct msconnector_rule_load_stats {
    unsigned inline_rules;
    unsigned file_rules;
    unsigned remote_rules;
} msconnector_rule_load_stats;

#ifdef __cplusplus
}
#endif

#endif
