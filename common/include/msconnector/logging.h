#ifndef MSCONNECTOR_LOGGING_H
#define MSCONNECTOR_LOGGING_H

#ifdef __cplusplus
extern "C" {
#endif

enum msconnector_log_level {
    MSCONNECTOR_LOG_TRACE = 0,
    MSCONNECTOR_LOG_DEBUG = 1,
    MSCONNECTOR_LOG_INFO = 2,
    MSCONNECTOR_LOG_WARN = 3,
    MSCONNECTOR_LOG_ERROR = 4
};

typedef struct msconnector_log_record {
    enum msconnector_log_level level;
    const char *transaction_id;
    const char *message;
    const char *source;
} msconnector_log_record;

typedef void (*msconnector_log_callback)(
    void *userdata,
    const msconnector_log_record *record);

typedef struct msconnector_logger {
    msconnector_log_callback callback;
    void *userdata;
} msconnector_logger;

static inline void msconnector_log(
    const msconnector_logger *logger,
    const msconnector_log_record *record) {
    if (logger != 0 && logger->callback != 0 && record != 0) {
        logger->callback(logger->userdata, record);
    }
}

#ifdef __cplusplus
}
#endif

#endif
