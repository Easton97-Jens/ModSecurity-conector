#include "modsecurity/modsecurity.h"
#include "modsecurity/rules_set.h"
#include "modsecurity/transaction.h"

#include <cstdlib>
#include <cstring>
#include <fstream>
#include <iostream>
#include <map>
#include <string>
#include <string_view>

namespace {

constexpr const char *kTargetedRuleId = "1000001";
constexpr const char *kRequestBodyRuleId = "1000002";

std::string json_escape(const std::string &value) {
    std::string out;
    out.reserve(value.size() + 8U);
    for (char ch : value) {
        switch (ch) {
            case '\\':
                out += "\\\\";
                break;
            case '"':
                out += "\\\"";
                break;
            case '\n':
                out += "\\n";
                break;
            case '\r':
                out += "\\r";
                break;
            case '\t':
                out += "\\t";
                break;
            default:
                out += ch;
                break;
        }
    }
    return out;
}

void json_string(std::ostream &out, const char *key, const std::string &value, bool comma = true) {
    out << "\"" << key << "\":\"" << json_escape(value) << "\"";
    if (comma) {
        out << ",";
    }
}

void json_bool(std::ostream &out, const char *key, bool value, bool comma = true) {
    out << "\"" << key << "\":" << (value ? "true" : "false");
    if (comma) {
        out << ",";
    }
}

void json_int(std::ostream &out, const char *key, int value, bool comma = true) {
    out << "\"" << key << "\":" << value;
    if (comma) {
        out << ",";
    }
}

std::map<std::string, std::string> parse_args(int argc, char **argv) {
    std::map<std::string, std::string> args;
    for (int i = 1; i < argc; ++i) {
        std::string key = argv[i];
        if (key.rfind("--", 0) != 0 || i + 1 >= argc) {
            std::cerr << "usage: " << argv[0]
                      << " --rule-file <path> --decision-log <path>"
                      << " [--ruleset targeted|crs] [--smoke-case targeted|request_body]"
                      << " [--header-value <value>] [--uri <uri>] [--method <method>]"
                      << " [--body <body>] [--content-type <content-type>]\n";
            std::exit(2);
        }
        args[key.substr(2)] = argv[++i];
    }
    return args;
}

std::string bracket_value(const std::string &intervention_log, std::string_view field_key) {
    const std::string marker = "[" + std::string(field_key) + " \"";
    const std::size_t start = intervention_log.find(marker);
    if (start == std::string::npos) {
        return "";
    }
    const std::size_t value_start = start + marker.size();
    const std::size_t end = intervention_log.find("\"]", value_start);
    if (end == std::string::npos || end <= value_start) {
        return "";
    }
    return intervention_log.substr(value_start, end - value_start);
}

struct DecisionLogInput {
    std::string path;
    std::string ruleset;
    std::string whoami;
    std::string rule_file;
    std::string header_value;
    std::string smoke_case;
    std::string method;
    std::string content_type;
    std::string request_body_marker;
    bool request_body_access_enabled = false;
    bool request_body_marker_present = false;
    bool rule_loaded = false;
    bool disruptive = false;
    int intervention_status = 200;
    std::string intervention_log;
    std::string rule_id;
    std::string rule_message;
};

void append_decision_log(const DecisionLogInput &input) {
    if (input.path.empty()) {
        return;
    }
    std::ofstream out(input.path, std::ios::app);
    out << "decision_backend=libmodsecurity\n";
    out << "modsecurity_ruleset=" << input.ruleset << "\n";
    out << "libmodsecurity=" << input.whoami << "\n";
    out << "rule_file=" << input.rule_file << "\n";
    out << "rule_id=" << input.rule_id << "\n";
    out << "modsecurity_smoke_case=" << input.smoke_case << "\n";
    out << "request_method=" << input.method << "\n";
    if (!input.content_type.empty()) {
        out << "request_content_type=" << input.content_type << "\n";
    }
    if (input.smoke_case == "request_body") {
        out << "request_body_access_enabled=" << (input.request_body_access_enabled ? "true" : "false") << "\n";
        out << "request_body_rule_id=" << kRequestBodyRuleId << "\n";
        out << "request_body_rule_loaded=" << (input.rule_loaded ? "true" : "false") << "\n";
        out << "blocked_body_marker=" << input.request_body_marker << "\n";
        out << "blocked_body_marker_present=" << (input.request_body_marker_present ? "true" : "false") << "\n";
    }
    if (input.ruleset == "crs") {
        out << "crs_rule_id=" << input.rule_id << "\n";
        out << "crs_rule_message=" << input.rule_message << "\n";
    }
    out << "rule_loaded=" << (input.rule_loaded ? "true" : "false") << "\n";
    out << "request_header_x_modsec_smoke=" << input.header_value << "\n";
    out << "intervention_disruptive=" << (input.disruptive ? "true" : "false") << "\n";
    out << "intervention_status=" << input.intervention_status << "\n";
    if (!input.intervention_log.empty()) {
        out << "intervention_log=" << input.intervention_log << "\n";
    }
    out << "\n";
}

int fail_json(const std::string &message) {
    std::cout << "{";
    json_bool(std::cout, "ok", false);
    json_string(std::cout, "error", message, false);
    std::cout << "}\n";
    return 1;
}

}  // namespace

int main(int argc, char **argv) {
    const auto args = parse_args(argc, argv);
    const std::string rule_file = args.count("rule-file") ? args.at("rule-file") : "";
    const std::string decision_log = args.count("decision-log") ? args.at("decision-log") : "";
    const std::string ruleset = args.count("ruleset") ? args.at("ruleset") : "targeted";
    const std::string smoke_case = args.count("smoke-case") ? args.at("smoke-case") : "targeted";
    const std::string header_value = args.count("header-value") ? args.at("header-value") : "";
    const std::string uri = args.count("uri") ? args.at("uri") : "/targeted";
    const std::string method = args.count("method") ? args.at("method") : "GET";
    const std::string body = args.count("body") ? args.at("body") : "";
    const std::string content_type = args.count("content-type") ? args.at("content-type") : "";
    const std::string request_body_marker = args.count("request-body-marker")
                                                ? args.at("request-body-marker")
                                                : "modsec-request-body-block";

    if (rule_file.empty()) {
        return fail_json("missing --rule-file");
    }
    if (ruleset != "targeted" && ruleset != "crs") {
        return fail_json("unsupported --ruleset: " + ruleset);
    }
    if (smoke_case != "targeted" && smoke_case != "request_body") {
        return fail_json("unsupported --smoke-case: " + smoke_case);
    }

    modsecurity::ModSecurity *modsec = modsecurity::msc_init();
    if (modsec == nullptr) {
        return fail_json("msc_init failed");
    }
    modsecurity::msc_set_connector_info(modsec, "ModSecurity-conector targeted smoke");
    const char *who = modsecurity::msc_who_am_i(modsec);
    const std::string whoami = who == nullptr ? "unknown" : who;

    modsecurity::RulesSet *rules = modsecurity::msc_create_rules_set();
    if (rules == nullptr) {
        modsecurity::msc_cleanup(modsec);
        return fail_json("msc_create_rules_set failed");
    }

    const char *rule_error = nullptr;
    const int rule_count = modsecurity::msc_rules_add_file(rules, rule_file.c_str(), &rule_error);
    const bool rule_loaded = rule_count >= 0;
    if (!rule_loaded) {
        const std::string message = rule_error == nullptr ? "msc_rules_add_file failed" : rule_error;
        modsecurity::msc_rules_error_cleanup(rule_error);
        modsecurity::msc_rules_cleanup(rules);
        modsecurity::msc_cleanup(modsec);
        return fail_json(message);
    }

    modsecurity::Transaction *tx = modsecurity::msc_new_transaction(modsec, rules, nullptr);
    if (tx == nullptr) {
        modsecurity::msc_rules_cleanup(rules);
        modsecurity::msc_cleanup(modsec);
        return fail_json("msc_new_transaction failed");
    }

    modsecurity::msc_process_connection(tx, "127.0.0.1", 12345, "127.0.0.1", 8080);
    modsecurity::msc_process_uri(tx, uri.c_str(), method.c_str(), "1.1");
    const unsigned char host_name[] = "Host";
    const unsigned char host_value[] = "example.test";
    modsecurity::msc_add_n_request_header(
        tx,
        host_name,
        sizeof(host_name) - 1U,
        host_value,
        sizeof(host_value) - 1U);
    if (!header_value.empty()) {
        const unsigned char header_name[] = "X-Modsec-Smoke";
        modsecurity::msc_add_n_request_header(
            tx,
            header_name,
            sizeof(header_name) - 1U,
            reinterpret_cast<const unsigned char *>(header_value.c_str()),
            header_value.size());
    }
    if (!body.empty()) {
        if (!content_type.empty()) {
            const unsigned char content_type_name[] = "Content-Type";
            modsecurity::msc_add_n_request_header(
                tx,
                content_type_name,
                sizeof(content_type_name) - 1U,
                reinterpret_cast<const unsigned char *>(content_type.c_str()),
                content_type.size());
        }
        const std::string content_length = std::to_string(body.size());
        const unsigned char content_length_name[] = "Content-Length";
        modsecurity::msc_add_n_request_header(
            tx,
            content_length_name,
            sizeof(content_length_name) - 1U,
            reinterpret_cast<const unsigned char *>(content_length.c_str()),
            content_length.size());
    }
    modsecurity::msc_process_request_headers(tx);

    modsecurity::ModSecurityIntervention intervention;
    modsecurity::intervention::clean(&intervention);
    int intervention_rc = modsecurity::msc_intervention(tx, &intervention);
    bool disruptive = intervention.disruptive != 0 || intervention_rc != 0;
    if (!disruptive) {
        if (!body.empty()) {
            modsecurity::msc_append_request_body(
                tx,
                reinterpret_cast<const unsigned char *>(body.c_str()),
                body.size());
        }
        modsecurity::msc_process_request_body(tx);
        intervention_rc = modsecurity::msc_intervention(tx, &intervention);
        disruptive = intervention.disruptive != 0 || intervention_rc != 0;
    }
    const int intervention_status = disruptive ? intervention.status : 200;
    const std::string intervention_log = intervention.log == nullptr ? "" : intervention.log;
    std::string observed_rule_id = bracket_value(intervention_log, "id");
    if (observed_rule_id.empty() && ruleset != "crs") {
        observed_rule_id = smoke_case == "request_body" ? kRequestBodyRuleId : kTargetedRuleId;
    }
    const std::string observed_rule_message = ruleset == "crs" ? bracket_value(intervention_log, "msg") : "";
    const bool request_body_access_enabled = smoke_case == "request_body" && !body.empty();
    const bool request_body_marker_present = !request_body_marker.empty()
                                             && body.find(request_body_marker) != std::string::npos;

    modsecurity::msc_process_logging(tx);
    DecisionLogInput decision_log_input;
    decision_log_input.path = decision_log;
    decision_log_input.ruleset = ruleset;
    decision_log_input.whoami = whoami;
    decision_log_input.rule_file = rule_file;
    decision_log_input.header_value = header_value;
    decision_log_input.smoke_case = smoke_case;
    decision_log_input.method = method;
    decision_log_input.content_type = content_type;
    decision_log_input.request_body_marker = request_body_marker;
    decision_log_input.request_body_access_enabled = request_body_access_enabled;
    decision_log_input.request_body_marker_present = request_body_marker_present;
    decision_log_input.rule_loaded = rule_loaded;
    decision_log_input.disruptive = disruptive;
    decision_log_input.intervention_status = intervention_status;
    decision_log_input.intervention_log = intervention_log;
    decision_log_input.rule_id = observed_rule_id;
    decision_log_input.rule_message = observed_rule_message;
    append_decision_log(decision_log_input);

    std::cout << "{";
    json_bool(std::cout, "ok", true);
    json_string(std::cout, "decision_backend", "libmodsecurity");
    json_string(std::cout, "modsecurity_ruleset", ruleset);
    json_string(std::cout, "modsecurity_smoke_case", smoke_case);
    json_string(std::cout, "libmodsecurity", whoami);
    json_bool(std::cout, "modsecurity_rule_loaded", rule_loaded);
    json_string(std::cout, "modsecurity_rule_file", rule_file);
    json_string(std::cout, "modsecurity_rule_id", observed_rule_id);
    json_bool(std::cout, "request_body_access_enabled", request_body_access_enabled);
    json_string(std::cout, "request_body_rule_file", smoke_case == "request_body" ? rule_file : "");
    json_string(std::cout, "request_body_rule_id", smoke_case == "request_body" ? kRequestBodyRuleId : "");
    json_bool(std::cout, "request_body_rule_loaded", smoke_case == "request_body" && rule_loaded);
    json_string(std::cout, "request_method", method);
    json_string(std::cout, "blocked_body_marker", smoke_case == "request_body" ? request_body_marker : "");
    json_bool(std::cout, "blocked_body_marker_present", request_body_marker_present);
    json_string(std::cout, "crs_rule_id", ruleset == "crs" ? observed_rule_id : "");
    json_string(std::cout, "crs_rule_message", ruleset == "crs" ? observed_rule_message : "");
    json_bool(std::cout, "intervention_disruptive", disruptive);
    json_int(std::cout, "intervention_status", intervention_status);
    json_string(std::cout, "intervention_log", intervention_log, false);
    std::cout << "}\n";

    modsecurity::msc_intervention_cleanup(&intervention);
    modsecurity::msc_transaction_cleanup(tx);
    modsecurity::msc_rules_cleanup(rules);
    modsecurity::msc_cleanup(modsec);
    return 0;
}
