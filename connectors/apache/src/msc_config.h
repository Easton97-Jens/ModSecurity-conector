
#ifndef _SRC_MSC_CONFIG__
#define _SRC_MSC_CONFIG__

void *msc_hook_create_config_directory(apr_pool_t *mp, char *path);

void *msc_hook_merge_config_directory(apr_pool_t *mp, void *parent,
    void *child);



#endif  /* _SRC_MSC_CONFIG__ */
