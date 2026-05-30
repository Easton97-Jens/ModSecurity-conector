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

static inline void
msconnector_rule_load_stats_init(msconnector_rule_load_stats *stats)
{
    stats->inline_rules = 0;
    stats->file_rules = 0;
    stats->remote_rules = 0;
}

static inline void
msconnector_rule_load_stats_add(msconnector_rule_load_stats *dst,
    const msconnector_rule_load_stats *src)
{
    dst->inline_rules += src->inline_rules;
    dst->file_rules += src->file_rules;
    dst->remote_rules += src->remote_rules;
}

static inline void
msconnector_rule_load_stats_add_inline(msconnector_rule_load_stats *stats,
    unsigned count)
{
    stats->inline_rules += count;
}

static inline void
msconnector_rule_load_stats_add_file(msconnector_rule_load_stats *stats,
    unsigned count)
{
    stats->file_rules += count;
}

static inline void
msconnector_rule_load_stats_add_remote(msconnector_rule_load_stats *stats,
    unsigned count)
{
    stats->remote_rules += count;
}

#ifdef __cplusplus
}
#endif

#endif
