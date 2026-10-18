/* Apache I12 test-only public-SDK multipart observation; never changes SDK calls. */
#include <modsecurity/transaction.h>
#include <cerrno>
#include <cstdint>
#include <cstdlib>
#include <cstring>
#include <fcntl.h>
#include <iomanip>
#include <limits.h>
#include <map>
#include <mutex>
#include <sstream>
#include <string>
#include <sys/stat.h>
#include <sys/syscall.h>
#include <time.h>
#include <unistd.h>
#include <vector>

namespace {
constexpr std::size_t max_files = 16, max_transactions = 128, max_records = 4096;
constexpr off_t max_output = 1024 * 1024;
struct Saved { std::string id; std::vector<std::string> paths; bool complete; };
std::mutex lock;
std::map<void *, Saved> saved;
pid_t owner = 0;
std::size_t records = 0;

std::string quoted(const std::string &value) {
    std::ostringstream out; out << '"';
    for (unsigned char c : value.substr(0, 256)) {
        if (c == '"' || c == '\\') out << '\\' << c;
        else if (c < 32 || c >= 127) out << "\\u00" << std::hex << std::setw(2) << std::setfill('0') << static_cast<unsigned>(c);
        else out << c;
    }
    out << '"'; return out.str();
}
std::string fingerprint(const std::string &value) {
    // Correlation only: explicitly not an integrity or cryptographic hash.
    uint64_t hash = UINT64_C(14695981039346656037);
    for (unsigned char c : value) { hash ^= c; hash *= UINT64_C(1099511628211); }
    std::ostringstream out; out << std::hex << std::setw(16) << std::setfill('0') << hash;
    return out.str();
}
bool private_file(const struct stat &info) {
    return S_ISREG(info.st_mode) && info.st_uid == geteuid() &&
        (info.st_mode & 0777) == 0600 && info.st_nlink == 1;
}
int root_fd(std::string &path) {
    const char *configured = std::getenv("I12_APACHE_MULTIPART_ROOT");
    if (!configured || configured[0] != '/' || std::strlen(configured) >= PATH_MAX) return -1;
    char canonical[PATH_MAX];
    if (!realpath(configured, canonical) || std::strcmp(canonical, configured)) return -1;
    path = configured;
    int fd = open(configured, O_RDONLY | O_DIRECTORY | O_NOFOLLOW | O_CLOEXEC);
    struct stat info;
    if (fd < 0) return -1;
    if (fstat(fd, &info) || info.st_uid != geteuid() || (info.st_mode & 0777) != 0700) { close(fd); return -1; }
    int marker = openat(fd, "multipart.enable", O_RDONLY | O_NOFOLLOW | O_CLOEXEC);
    const char expected[] = "I12_APACHE_MULTIPART_V1\n";
    char text[sizeof(expected) + 1] = {};
    bool admitted = marker >= 0 && !fstat(marker, &info) && private_file(info) &&
        read(marker, text, sizeof(text)) == static_cast<ssize_t>(sizeof(expected) - 1) &&
        !std::memcmp(text, expected, sizeof(expected) - 1);
    if (marker >= 0) close(marker);
    if (!admitted) { close(fd); return -1; }
    return fd;
}
void output(int root, const std::string &row) {
    if (records >= max_records) return;
    int fd = openat(root, "multipart.jsonl", O_WRONLY | O_APPEND | O_CREAT | O_NOFOLLOW | O_CLOEXEC, 0600);
    if (fd < 0) return;
    struct stat info;
    if (!fstat(fd, &info) && private_file(info) && info.st_size <= max_output - static_cast<off_t>(row.size() + 1)) {
        std::string line = row + '\n';
        ssize_t count = write(fd, line.data(), line.size());
        if (count == static_cast<ssize_t>(line.size())) ++records;
    }
    close(fd);
}
std::string common(void *key, const std::string &id, const char *kind) {
    timespec clock = {}; clock_gettime(CLOCK_MONOTONIC, &clock);
    std::ostringstream out;
    out << "{\"kind\":" << quoted(kind) << ",\"transaction_key\":\"" << key << "\",\"transaction_id\":" << quoted(id)
        << ",\"transaction_id_source\":\"sdk_public_m_id\",\"pid\":" << getpid()
        << ",\"tid\":" << syscall(SYS_gettid) << ",\"euid\":" << geteuid()
        << ",\"monotonic_ns\":" << (static_cast<uint64_t>(clock.tv_sec) * 1000000000 + clock.tv_nsec);
    return out.str();
}
std::string path_metadata(int root, const std::string &directory, const std::string &path) {
    std::ostringstream out; out << "{\"path_fingerprint_fnv1a64\":" << quoted(fingerprint(path));
    std::string prefix = directory + "/";
    bool inside = path.compare(0, prefix.size(), prefix) == 0;
    std::string leaf = inside ? path.substr(prefix.size()) : "";
    bool accepted = !leaf.empty() && leaf != "." && leaf != ".." && leaf.find('/') == std::string::npos;
    out << ",\"direct_private_child\":" << (accepted ? "true" : "false");
    if (!accepted) return out.str() + ",\"exists\":null,\"stat_errno\":null}";
    struct stat info = {};
    int result = fstatat(root, leaf.c_str(), &info, AT_SYMLINK_NOFOLLOW);
    int error = result ? errno : 0;
    out << ",\"stat_result\":" << result << ",\"stat_errno\":" << error;
    if (result == 0) {
        out << ",\"exists\":true,\"regular\":" << (S_ISREG(info.st_mode) ? "true" : "false")
            << ",\"symlink\":" << (S_ISLNK(info.st_mode) ? "true" : "false")
            << ",\"device\":" << info.st_dev << ",\"inode\":" << info.st_ino
            << ",\"size\":" << info.st_size << ",\"uid\":" << info.st_uid
            << ",\"mode\":" << (info.st_mode & 0777) << ",\"nlink\":" << info.st_nlink;
    } else out << ",\"exists\":" << (error == ENOENT ? "false" : "null");
    return out.str() + "}";
}
std::string files(int root, const std::string &directory, const std::vector<std::string> &paths) {
    std::ostringstream out; out << '[';
    for (std::size_t i = 0; i < paths.size(); ++i) { if (i) out << ','; out << path_metadata(root, directory, paths[i]); }
    out << ']'; return out.str();
}
std::string names(const modsecurity::AnchoredSetVariable &collection) {
    std::ostringstream out; out << '['; std::size_t count = 0;
    for (const auto &entry : collection) {
        if (count == max_files) break;
        if (count++) out << ',';
        out << "{\"key_fingerprint_fnv1a64\":" << quoted(fingerprint(entry.first))
            << ",\"value_fingerprint_fnv1a64\":";
        out << (entry.second ? quoted(fingerprint(entry.second->getValue())) : "null") << '}';
    }
    return out.str() + ']';
}
void reset_process() {
    if (owner != getpid()) { saved.clear(); records = 0; owner = getpid(); }
}
}  // namespace

extern "C" void i12_apache_observe_multipart(void *opaque) noexcept {
    int previous_errno = errno;
    try {
        std::lock_guard<std::mutex> guard(lock); reset_process();
        std::string directory; int root = root_fd(directory);
        if (root >= 0) {
            if (opaque && (saved.count(opaque) || saved.size() < max_transactions)) {
                auto *transaction = static_cast<modsecurity::Transaction *>(opaque);
                Saved snapshot{transaction->m_id, {}, transaction->m_variableFilesTmpNames.size() <= max_files};
                for (const auto &entry : transaction->m_variableFilesTmpNames) {
                    if (snapshot.paths.size() == max_files) break;
                    if (entry.second) snapshot.paths.push_back(entry.second->getValue());
                    else snapshot.complete = false;
                }
                std::ostringstream row;
                row << common(opaque, snapshot.id, "native_multipart_after_request_body")
                    << ",\"files_count\":" << transaction->m_variableFiles.size()
                    << ",\"files_names_count\":" << transaction->m_variableFilesNames.size()
                    << ",\"files_sizes_count\":" << transaction->m_variableFilesSizes.size()
                    << ",\"filename_fingerprints\":" << names(transaction->m_variableFiles)
                    << ",\"filename_fingerprints_complete\":" << (transaction->m_variableFiles.size() <= max_files ? "true" : "false")
                    << ",\"files_tmpnames_count\":" << transaction->m_variableFilesTmpNames.size()
                    << ",\"files_combined_size\":" << quoted(transaction->m_variableFilesCombinedSize.m_value)
                    << ",\"native_tmpfile_objects_count\":" << transaction->m_multipartPartTmpFiles.size()
                    << ",\"path_snapshot_complete\":" << (snapshot.complete ? "true" : "false")
                    << ",\"max_observed_files\":" << max_files << ",\"files\":" << files(root, directory, snapshot.paths) << '}';
                saved[opaque] = snapshot; output(root, row.str());
            }
            close(root);
        }
    } catch (...) { /* An observer must not throw across the native C boundary. */ }
    errno = previous_errno;
}

extern "C" void i12_apache_observe_multipart_cleanup(void *opaque) noexcept {
    int previous_errno = errno;
    try {
        std::lock_guard<std::mutex> guard(lock); reset_process();
        auto found = saved.find(opaque);
        if (found != saved.end()) {
            std::string directory; int root = root_fd(directory);
            if (root >= 0) {
                std::string row = common(opaque, found->second.id, "native_multipart_after_actual_cleanup");
                row += ",\"dead_transaction_dereferenced\":false,\"path_snapshot_complete\":";
                row += found->second.complete ? "true" : "false";
                output(root, row + ",\"files\":" + files(root, directory, found->second.paths) + "}"); close(root);
            }
            saved.erase(found);
        }
    } catch (...) { }
    errno = previous_errno;
}
