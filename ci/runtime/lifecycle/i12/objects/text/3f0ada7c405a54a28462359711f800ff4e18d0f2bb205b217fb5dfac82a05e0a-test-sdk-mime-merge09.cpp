#include <modsecurity/rules_set.h>
#include <iostream>
#include <cstring>
int main() {
    const char *cases[] = {"SecResponseBodyMimeTypesClear\nSecResponseBodyMimeType text/plain\n", "SecResponseBodyMimeType text/plain\n", "SecResponseBodyMimeType text/plain\nSecResponseBodyMimeTypesClear\n"};
    for (unsigned int i = 0; i < 3; ++i) {
        modsecurity::RulesSet *rules = modsecurity::msc_create_rules_set();
        const char *error = nullptr;
        if (rules == nullptr) return 2;
        const int result = modsecurity::msc_rules_add(rules, cases[i], &error);
        const auto &mime = rules->m_responseBodyTypeToBeInspected;
        std::cout << "{\"case\":" << i << ",\"parse_return\":" << result << ",\"set\":" << mime.m_set << ",\"count\":" << mime.m_value.size() << ",\"has_text_plain\":" << mime.m_value.count("text/plain") << "}\n";
        const bool expected = result >= 0 && error == nullptr && mime.m_set && mime.m_value.size() == (i == 1 ? 1U : 0U) && mime.m_value.count("text/plain") == (i == 1 ? 1U : 0U);
        const int cleanup = modsecurity::msc_rules_cleanup(rules);
        if (!expected || cleanup != 1) return 3;
    }
    return 0;
}
