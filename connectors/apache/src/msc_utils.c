
#include "msc_utils.h"


int id(const char *fn, const char *format, ...)
{
    int rc = -1;
    FILE *f = NULL;
    va_list args;

    if (fn == NULL || format == NULL)
    {
        return -1;
    }

    f = fopen(fn, "a");
    if (f == NULL)
    {
        return -1;
    }

    va_start(args, format);
    rc = vfprintf(f, format, args);
    va_end(args);

    if (fclose(f) != 0)
    {
        return -1;
    }

    return rc;
}



/*
 * The primary request owns a native transaction for the lifetime of its
 * request pool.  Redirect and subrequest lookup updates msr->r, so cleanup
 * must use the captured owner_request rather than the mutable current
 * request.  Clear every stored native reference before the non-idempotent
 * libmodsecurity destroy call so repeated cleanup cannot double free it.
 */
apr_status_t msc_cleanup_request_transaction(void *data)
{
    msc_t *msr = (msc_t *)data;
    Transaction *transaction;
    request_rec *owner_request;

    if (msr == NULL)
    {
        return APR_SUCCESS;
    }

    transaction = msr->t;
    owner_request = msr->owner_request;
    msr->t = NULL;
    msr->owner_request = NULL;

    if (owner_request != NULL && owner_request->notes != NULL)
    {
        apr_table_unset(owner_request->notes, NOTE_MSR);
    }

    if (transaction != NULL)
    {
        msc_transaction_cleanup(transaction);
    }

    return APR_SUCCESS;
}


/*
 * Build an error brigade and send it to an explicitly selected output
 * destination.  Input and output filters have distinct chains in Apache;
 * callers must never pass an input-filter `next` pointer to
 * ap_pass_brigade().
 */
static apr_status_t pass_error_bucket(ap_filter_t *f, int status,
    ap_filter_t *destination)
{
    apr_bucket_brigade *brigade = NULL;
    apr_bucket *bucket = NULL;

    /* Keep Apache's request state consistent with the error bucket.  An
     * input-filter failure is otherwise reduced to the core's generic 400
     * while it drains the body, even though libmodsecurity selected a
     * concrete disruptive status (for example the Phase-2 403). */
    f->r->status = status;
    f->r->status_line = ap_get_status_line(status);

    brigade = apr_brigade_create(f->r->pool, f->r->connection->bucket_alloc);
    if (brigade == NULL)
    {
        return APR_EGENERAL;
    }

    bucket = ap_bucket_error_create(status, NULL, f->r->pool,
        f->r->connection->bucket_alloc);
    if (bucket == NULL)
    {
        return APR_EGENERAL;
    }

    APR_BRIGADE_INSERT_TAIL(brigade, bucket);

    bucket = apr_bucket_eos_create(f->r->connection->bucket_alloc);
    if (bucket == NULL)
    {
        return APR_EGENERAL;
    }

    APR_BRIGADE_INSERT_TAIL(brigade, bucket);

    return ap_pass_brigade(destination, brigade);
}


/**
 * Sends a brigade with an error bucket down an output filter's remaining
 * output chain.
 */
apr_status_t send_error_bucket(msc_t *msr, ap_filter_t *f, int status)
{
    (void)msr;

    (void)pass_error_bucket(f, status, f->next);

    /* NOTE:
     * It may not matter what we do from the filter as it may be too
     * late to even generate an error (already sent to client).  Nick Kew
     * recommends to return APR_EGENERAL in hopes that the handler in control
     * will notice and do The Right Thing.  So, that is what we do now.
     */
    return APR_EGENERAL;
}


/**
 * Send an input-filter failure through the request output chain.  Returning
 * the output-chain result preserves Apache's AP_FILTER_ERROR signal, so
 * ap_discard_request_body() does not remap a Phase-2 intervention to its
 * generic HTTP 400 fallback.
 */
apr_status_t send_input_error_bucket(msc_t *msr, ap_filter_t *f, int status)
{
    (void)msr;

    return pass_error_bucket(f, status, f->r->output_filters);
}
