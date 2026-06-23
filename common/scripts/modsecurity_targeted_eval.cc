#include "modsecurity/modsecurity.h"
#include "modsecurity/rules_set.h"
#include "modsecurity/transaction.h"

#include <cstdlib>
#include <cstring>
#include <fstream>
#include <iostream>
#include <map>
#include <string>

namespace {

constexpr const char *kTargetedRuleId = "1000001";

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
                      << " [--ruleset targeted|crs] [--header-value <value>] [--uri <uri>]\n";
            std::exit(2);
        }
        args[key.substr(2)] = argv[++i];
    }
    return args;
}

std::string bracket_value(const std::string &log, const std::string &key) {
    const std::string marker = "[" + key + " \"";
    const std::size_t start = log.find(marker);
    if (start == std::string::npos) {
        return "";
    }
    const std::size_t value_start = start + marker.size();
    const std::size_t end = log.find("\"]", value_start);
    if (end == std::string::npos || end <= value_start) {
        return "";
    }
    return log.substr(value_start, end - value_start);
}

void append_decision_log(
    const std::string &path,
    const std::string &ruleset,
    const std::string &whoami,
    const std::string &rule_file,
    const std::string &header_value,
    bool rule_loaded,
    bool disruptive,
    int intervention_status,
    const std::string &intervention_log,
    const std::string &rule_id,
    const std::string &rule_message) {
    if (path.empty()) {
        return;
    }
    std::ofstream out(path, std::ios::app);
    out << "decision_backend=libmodsecurity\n";
    out << "modsecurity_ruleset=" << ruleset << "\n";
    out << "libmodsecurity=" << whoami << "\n";
    out << "rule_file=" << rule_file << "\n";
    out << "rule_id=" << rule_id << "\n";
    if (ruleset == "crs") {
        out << "crs_rule_id=" << rule_id << "\n";
        out << "crs_rule_message=" << rule_message << "\n";
    }
    out << "rule_loaded=" << (rule_loaded ? "true" : "false") << "\n";
    out << "request_header_x_modsec_smoke=" << header_value << "\n";
    out << "intervention_disruptive=" << (disruptive ? "true" : "false") << "\n";
    out << "intervention_status=" << intervention_status << "\n";
    if (!intervention_log.empty()) {
        out << "intervention_log=" << intervention_log << "\n";
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
    const std::string header_value = args.count("header-value") ? args.at("header-value") : "";
    const std::string uri = args.count("uri") ? args.at("uri") : "/targeted";

    if (rule_file.empty()) {
        return fail_json("missing --rule-file");
    }
    if (ruleset != "targeted" && ruleset != "crs") {
        return fail_json("unsupported --ruleset: " + ruleset);
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
    modsecurity::msc_process_uri(tx, uri.c_str(), "GET", "1.1");
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
    modsecurity::msc_process_request_headers(tx);

    modsecurity::ModSecurityIntervention intervention;
    modsecurity::intervention::clean(&intervention);
    int intervention_rc = modsecurity::msc_intervention(tx, &intervention);
    bool disruptive = intervention.disruptive != 0 || intervention_rc != 0;
    if (!disruptive) {
        modsecurity::msc_process_request_body(tx);
        intervention_rc = modsecurity::msc_intervention(tx, &intervention);
        disruptive = intervention.disruptive != 0 || intervention_rc != 0;
    }
    const int intervention_status = disruptive ? intervention.status : 200;
    const std::string intervention_log = intervention.log == nullptr ? "" : intervention.log;
    const std::string observed_rule_id = ruleset == "crs" ? bracket_value(intervention_log, "id") : kTargetedRuleId;
    const std::string observed_rule_message = ruleset == "crs" ? bracket_value(intervention_log, "msg") : "";

    modsecurity::msc_process_logging(tx);
    append_decision_log(
        decision_log,
        ruleset,
        whoami,
        rule_file,
        header_value,
        rule_loaded,
        disruptive,
        intervention_status,
        intervention_log,
        observed_rule_id,
        observed_rule_message);

    std::cout << "{";
    json_bool(std::cout, "ok", true);
    json_string(std::cout, "decision_backend", "libmodsecurity");
    json_string(std::cout, "modsecurity_ruleset", ruleset);
    json_string(std::cout, "libmodsecurity", whoami);
    json_bool(std::cout, "modsecurity_rule_loaded", rule_loaded);
    json_string(std::cout, "modsecurity_rule_file", rule_file);
    json_string(std::cout, "modsecurity_rule_id", observed_rule_id);
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
