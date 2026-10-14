/* Optional test-artifact-only accessor; compile against the explicitly
 * selected SDK and qualify both real constructors before host use. This uses
 * the SDK's public member, never an assumed offset into an opaque C handle. */
#include <modsecurity/modsecurity.h>
#include <modsecurity/transaction.h>
#include <cerrno>
#include <cstring>

#ifndef MSCONNECTOR_LIFECYCLE_SDK_EXPECTED_VERSION
#define MSCONNECTOR_LIFECYCLE_SDK_EXPECTED_VERSION MODSECURITY_VERSION
#endif

static int restore_errno(int saved, int result) {
    errno = saved;
    return result;
}

extern "C" int msconnector_lifecycle_sdk_transaction_id(
    void *engine, const void *transaction, char *output, size_t capacity) {
    const int saved = errno;
    constexpr size_t maximum_capacity = 256U;
    if (engine == nullptr || transaction == nullptr || output == nullptr ||
        capacity == 0U || capacity > maximum_capacity)
        return restore_errno(saved, -1);
    output[0] = '\0';
    const char *identity = modsecurity::msc_who_am_i(static_cast<modsecurity::ModSecurity *>(engine));
    const char *prefix = identity == nullptr ? nullptr : std::strstr(identity, "ModSecurity v");
    if (prefix == nullptr) return restore_errno(saved, -2);
    const char *version = prefix + std::strlen("ModSecurity v");
    constexpr const char *expected = MSCONNECTOR_LIFECYCLE_SDK_EXPECTED_VERSION;
    const size_t expected_length = std::strlen(expected);
    if (std::strncmp(version, expected, expected_length) != 0 ||
        (version[expected_length] != '\0' && version[expected_length] != ' ' && version[expected_length] != '('))
        return restore_errno(saved, -2);
    /* The version rejection above precedes every Transaction dereference. */
    const auto *native = static_cast<const modsecurity::Transaction *>(transaction);
    const std::string &id = native->m_id;
    if (id.empty() || id.size() >= capacity || id.find('\0') != std::string::npos)
        return restore_errno(saved, -1);
    std::memcpy(output, id.data(), id.size());
    output[id.size()] = '\0';
    return restore_errno(saved, 1);
}
