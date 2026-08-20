#include "msconnector_rule_match_observer.h"

#include "modsecurity/modsecurity.h"
#include "modsecurity/rule_message.h"

#include "msconnector/transaction_id.h"

#include <cstring>

namespace {

constexpr int64_t kMaximumRuleId = 999999999999LL;

bool map_rule_message_phase(
    int libmodsecurity_phase,
    enum msconnector_phase *phase) noexcept {
    if (phase == nullptr) {
        return false;
    }
    switch (libmodsecurity_phase) {
      case 0:
        *phase = MSCONNECTOR_PHASE_REQUEST_HEADERS;
        return true;
      case 1:
        *phase = MSCONNECTOR_PHASE_REQUEST_BODY;
        return true;
      case 2:
        *phase = MSCONNECTOR_PHASE_RESPONSE_HEADERS;
        return true;
      case 3:
        *phase = MSCONNECTOR_PHASE_RESPONSE_BODY;
        return true;
      case 4:
        *phase = MSCONNECTOR_PHASE_LOGGING;
        return true;
      default:
        return false;
    }
}

bool format_rule_id(
    int64_t value,
    char output[MSCONNECTOR_RULE_MATCH_OBSERVER_RULE_ID_SIZE]) noexcept {
    char reversed[MSCONNECTOR_RULE_MATCH_OBSERVER_RULE_ID_SIZE - 1U];
    size_t count = 0U;

    if (value <= 0 || value > kMaximumRuleId) {
        return false;
    }
    do {
        if (count >= sizeof(reversed)) {
            return false;
        }
        reversed[count++] = static_cast<char>('0' + (value % 10));
        value /= 10;
    } while (value != 0);
    for (size_t index = 0U; index < count; ++index) {
        output[index] = reversed[count - index - 1U];
    }
    output[count] = '\0';
    return true;
}

void rule_message_callback(void *data, const void *value) noexcept {
    auto *observer = static_cast<msconnector_rule_match_observer *>(data);

    try {
        if (observer == nullptr || value == nullptr) {
            msconnector_rule_match_observer_fail(observer);
            return;
        }
        const auto &message = *static_cast<const modsecurity::RuleMessage *>(value);
        const auto &transaction_id = message.m_transaction.m_id;
        msconnector_rule_match_observer_capture(
            observer,
            transaction_id.data(),
            transaction_id.size(),
            message.m_rule.m_ruleId,
            message.getPhase());
    } catch (...) {
        msconnector_rule_match_observer_fail(observer);
    }
}

}  // namespace

extern "C" void msconnector_rule_match_observer_init(
    msconnector_rule_match_observer *observer,
    int enabled,
    const char *expected_transaction_id) {
    size_t transaction_id_length;

    if (observer == nullptr) {
        return;
    }
    std::memset(observer, 0, sizeof(*observer));
    if (enabled == 0) {
        return;
    }
    if (expected_transaction_id == nullptr ||
        !msconnector_transaction_id_validate(expected_transaction_id)) {
        observer->failed = 1;
        return;
    }
    transaction_id_length = std::strlen(expected_transaction_id);
    if (transaction_id_length == 0U ||
        transaction_id_length >= sizeof(observer->expected_transaction_id)) {
        observer->failed = 1;
        return;
    }
    std::memcpy(observer->expected_transaction_id, expected_transaction_id,
        transaction_id_length);
    observer->expected_transaction_id[transaction_id_length] = '\0';
    observer->expected_transaction_id_length = transaction_id_length;
    observer->enabled = 1;
}

extern "C" int msconnector_rule_match_observer_install(void *modsecurity) {
    try {
        if (modsecurity == nullptr) {
            return 0;
        }
        static_cast<modsecurity::ModSecurity *>(modsecurity)->setServerLogCb(
            rule_message_callback,
            modsecurity::RuleMessageLogProperty);
        return 1;
    } catch (...) {
        return 0;
    }
}

extern "C" void msconnector_rule_match_observer_capture(
    msconnector_rule_match_observer *observer,
    const char *transaction_id,
    size_t transaction_id_length,
    int64_t rule_id,
    int libmodsecurity_phase) {
    char decimal_rule_id[MSCONNECTOR_RULE_MATCH_OBSERVER_RULE_ID_SIZE];
    enum msconnector_phase phase;

    if (observer == nullptr || observer->enabled == 0 || observer->failed != 0) {
        return;
    }
    if (transaction_id == nullptr ||
        transaction_id_length != observer->expected_transaction_id_length ||
        std::memcmp(transaction_id, observer->expected_transaction_id,
            transaction_id_length) != 0 ||
        !format_rule_id(rule_id, decimal_rule_id) ||
        !map_rule_message_phase(libmodsecurity_phase, &phase)) {
        observer->failed = 1;
        return;
    }
    for (size_t index = 0U; index < observer->match_count; ++index) {
        if (observer->matches[index].phase == phase &&
            std::strcmp(observer->matches[index].rule_id, decimal_rule_id) == 0) {
            return;
        }
    }
    if (observer->match_count >= MSCONNECTOR_RULE_MATCH_OBSERVER_MAX_MATCHES) {
        observer->failed = 1;
        return;
    }
    std::memcpy(observer->matches[observer->match_count].rule_id,
        decimal_rule_id, sizeof(decimal_rule_id));
    observer->matches[observer->match_count].phase = phase;
    observer->matches[observer->match_count].emitted = 0;
    ++observer->match_count;
}

extern "C" void msconnector_rule_match_observer_fail(
    msconnector_rule_match_observer *observer) {
    if (observer != nullptr) {
        observer->failed = 1;
    }
}

extern "C" int msconnector_rule_match_observer_failed(
    const msconnector_rule_match_observer *observer) {
    return observer == nullptr || observer->failed != 0;
}

extern "C" int msconnector_rule_match_observer_next(
    msconnector_rule_match_observer *observer,
    enum msconnector_phase phase,
    const char **rule_id) {
    if (observer == nullptr || rule_id == nullptr) {
        msconnector_rule_match_observer_fail(observer);
        return -1;
    }
    *rule_id = nullptr;
    if (observer->enabled == 0) {
        return 0;
    }
    if (observer->failed != 0) {
        return -1;
    }
    if (phase < MSCONNECTOR_PHASE_REQUEST_HEADERS ||
        phase > MSCONNECTOR_PHASE_LOGGING) {
        observer->failed = 1;
        return -1;
    }
    for (size_t index = 0U; index < observer->match_count; ++index) {
        if (observer->matches[index].phase == phase &&
            observer->matches[index].emitted == 0) {
            observer->matches[index].emitted = 1;
            *rule_id = observer->matches[index].rule_id;
            return 1;
        }
    }
    return 0;
}
