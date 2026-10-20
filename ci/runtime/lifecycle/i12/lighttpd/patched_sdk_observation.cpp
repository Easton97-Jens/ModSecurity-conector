/* Test-only public SDK3.0.14 MIME accessor for the existing I12 collector.
 * No opaque offsets, decision changes, API replacement or body data capture. */
#include <modsecurity/modsecurity.h>
#include <modsecurity/rules_set.h>
#include <modsecurity/transaction.h>
#include <cerrno>
#include <cstdio>
#include <cstring>
#include <string>

static bool quoted_metadata(const std::string& value, std::string& output) {
    if (value.size() > 256U) return false;
    output = "\"";
    for (unsigned char byte : value) {
        if (byte < 32U || byte >= 127U || byte == '"' || byte == '\\') {
            char escaped[7];
            (void)std::snprintf(escaped, sizeof(escaped), "\\u%04x", byte);
            output += escaped;
        } else {
            output += static_cast<char>(byte);
        }
    }
    output += '"';
    return true;
}

extern "C" int msconnector_lifecycle_sdk_mime_selection(
        void* engine, const void* transaction, char* output, size_t capacity) {
    const int saved = errno;
    int result = -1;
    if (engine == nullptr || transaction == nullptr || output == nullptr || capacity < 2U) {
        errno = saved;
        return result;
    }
    output[0] = '\0';
    const char* identity = modsecurity::msc_who_am_i(static_cast<modsecurity::ModSecurity*>(engine));
    constexpr char expected[] = "ModSecurity v3.0.14";
    constexpr size_t length = sizeof(expected) - 1U;
    const char* version = identity == nullptr ? nullptr : std::strstr(identity, expected);
    if (version == nullptr || (version[length] != '\0' && version[length] != ' ' && version[length] != '(')) {
        errno = saved;
        return -2;
    }
    /* Runtime version rejection precedes every native Transaction dereference. */
    const auto* native = static_cast<const modsecurity::Transaction*>(transaction);
    if (native->m_rules != nullptr) {
        const std::string& mime = native->m_variableResponseContentType.m_value;
        auto response_header = native->m_variableResponseHeaders.find("Content-Type");
        auto request_header = native->m_variableRequestHeaders.find("Content-Type");
        const std::string raw_response = response_header == native->m_variableResponseHeaders.end()
            ? "" : response_header->second->getValue();
        const std::string raw_request = request_header == native->m_variableRequestHeaders.end()
            ? "" : request_header->second->getValue();
        const auto& policy = native->m_rules->m_responseBodyTypeToBeInspected;
        std::string types = "[";
        bool first = true;
        for (const auto& value : policy.m_value) {
            std::string encoded;
            if (!quoted_metadata(value, encoded) || types.size() + encoded.size() > 1024U) {
                errno = saved;
                return -1;
            }
            if (!first) types += ',';
            first = false;
            types += encoded;
        }
        types += ']';
        std::string qmime, qresponse, qrequest;
        if (quoted_metadata(mime, qmime) && quoted_metadata(raw_response, qresponse)
                && quoted_metadata(raw_request, qrequest)) {
            const bool selected = policy.m_value.find(mime) != policy.m_value.end();
            const int count = std::snprintf(output, capacity,
                "{\"sdk_version\":\"3.0.14\",\"response_content_type\":%s,"
                "\"response_header_content_type\":%s,\"request_header_content_type\":%s,"
                "\"request_body_type\":%d,\"request_body_processor\":%d,"
                "\"response_body_access\":%d,\"mime_policy_set\":%s,"
                "\"mime_policy_clear\":%s,\"mime_types\":%s,\"mime_selected\":%s}",
                qmime.c_str(), qresponse.c_str(), qrequest.c_str(),
                static_cast<int>(native->m_requestBodyType), static_cast<int>(native->m_requestBodyProcessor),
                static_cast<int>(native->m_rules->m_secResponseBodyAccess),
                policy.m_set ? "true" : "false", policy.m_clear ? "true" : "false",
                types.c_str(), selected ? "true" : "false");
            if (count > 0 && static_cast<size_t>(count) < capacity) result = 1;
        }
    }
    errno = saved;
    return result;
}
