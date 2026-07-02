#ifndef MSCONNECTOR_PATH_POLICY_H
#define MSCONNECTOR_PATH_POLICY_H
#ifdef __cplusplus
extern "C" {
#endif
/* Conservative path helpers for generated artifacts; no repository root policy is enforced here. */
int msconnector_path_is_absolute(const char *path);
int msconnector_path_is_empty(const char *path);
int msconnector_path_has_parent_reference(const char *path);
#ifdef __cplusplus
}
#endif
#endif
