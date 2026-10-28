#ifndef MSCONNECTOR_NATIVE_RESULT_H
#define MSCONNECTOR_NATIVE_RESULT_H

#ifdef __cplusplus
extern "C" {
#endif

/* Only for the direct libModSecurity byte-append APIs:
 * msc_append_request_body() and msc_append_response_body().
 *
 * Their zero result also represents the engine's configured ProcessPartial
 * limit action. It is not a failed Common callback, an APR status, a host
 * return value, an HTTP status, or proof that the request was allowed.
 * In particular, engine Reject can return one and leave an intervention
 * pending. The caller must still collect the intervention and finish each
 * phase at its existing, exactly-once boundary.
 *
 * Do not apply this contract to msc_request_body_from_file(): zero there can
 * also denote an I/O/allocation failure. No macro shadows a native API.
 */
typedef enum msconnector_native_body_result {
    MSCONNECTOR_NATIVE_BODY_FAILURE = -1,
    MSCONNECTOR_NATIVE_BODY_PARTIAL = 0,
    MSCONNECTOR_NATIVE_BODY_SUCCESS = 1
} msconnector_native_body_result;

static inline msconnector_native_body_result
msconnector_native_body_result_classify(int result)
{
    if (result == 0) {
        return MSCONNECTOR_NATIVE_BODY_PARTIAL;
    }
    if (result == 1) {
        return MSCONNECTOR_NATIVE_BODY_SUCCESS;
    }
    /* Negative and unexpected positive results are not accepted silently. */
    return MSCONNECTOR_NATIVE_BODY_FAILURE;
}

static inline int msconnector_native_body_append_can_continue(int result)
{
    return msconnector_native_body_result_classify(result) !=
        MSCONNECTOR_NATIVE_BODY_FAILURE;
}

/* Phase evaluation has a different contract: only one is success. Never
 * turn a failed EOS evaluation into a partial/allow/log-only result. */
static inline int msconnector_native_phase_succeeded(int result)
{
    return result == 1;
}

#ifdef __cplusplus
}
#endif

#endif
