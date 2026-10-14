"""Test the test-only observer against real Common and a deterministic native ABI.

These controls qualify the measurement seam, not a hosted connector lifecycle.
"""
import json
import hashlib
import os
from pathlib import Path
import subprocess
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = None
SYMBOLS = (
    "msconnector_transaction_contract_init", "msconnector_transaction_contract_finish",
    "msconnector_transaction_contract_cleanup", "msconnector_transaction_contract_complete_phase",
    "msconnector_transaction_contract_set_response_committed",
    "msconnector_transaction_contract_record_response_metadata", "msc_new_transaction",
    "msc_new_transaction_with_id", "msc_transaction_cleanup", "msc_process_request_body",
    "msc_process_response_body", "msc_process_logging",
)
FIXTURE = r'''
#include "msconnector/transaction_contract.h"
#include <modsecurity/transaction.h>
#include <errno.h>
#include <pthread.h>
#include <signal.h>
#include <stdlib.h>
#include <string.h>
#include <sys/resource.h>
#include <sys/stat.h>
#include <sys/wait.h>
#include <unistd.h>
extern _Thread_local unsigned int native_calls[6];
static _Thread_local int token;
_Thread_local unsigned int native_calls[6];
Transaction *msc_new_transaction(ModSecurity *m, RulesSet *r, void *d) {
    (void)m;(void)r;(void)d; ++native_calls[5];errno = EDOM; return (Transaction *)&token;
}
Transaction *msc_new_transaction_with_id(ModSecurity *m, RulesSet *r, const char *id, void *d) {
    (void)m;(void)r;(void)d; ++native_calls[0];errno = EDOM;
    return strcmp(id,"failure") == 0 ? NULL : (Transaction *)&token;
}
int msc_process_request_body(Transaction *t) {(void)t;++native_calls[2];errno=ERANGE;return -7;}
int msc_process_response_body(Transaction *t) {(void)t;++native_calls[3];errno=ERANGE;return 9;}
int msc_process_logging(Transaction *t) {(void)t;++native_calls[4];errno=ERANGE;return 1;}
void msc_transaction_cleanup(Transaction *t) {(void)t;++native_calls[1];errno=EILSEQ;}
static void *cycle(void *argument) {
    const char *id = argument;
    unsigned int before[5];memcpy(before,native_calls,sizeof(before));
    msconnector_transaction_contract c;
    if (msconnector_transaction_contract_init(&c,NULL,id,"test","test",0,1) != 0) abort();
    Transaction *t=msc_new_transaction_with_id(NULL,NULL,id,NULL);
    if (!t || errno != EDOM) abort();
    if (msc_process_request_body(t) != -7 || errno != ERANGE) abort();
    if (msc_process_response_body(t) != 9 || errno != ERANGE) abort();
    if (msc_process_logging(t) != 1 || errno != ERANGE) abort();
    if (msconnector_transaction_contract_record_response_metadata(&c,200,"text/plain",1,10) != 0) abort();
    const enum msconnector_phase phases[]={MSCONNECTOR_PHASE_REQUEST_HEADERS,MSCONNECTOR_PHASE_REQUEST_BODY,MSCONNECTOR_PHASE_RESPONSE_HEADERS};
    for(size_t i=0;i<3U;++i) {
        if(msconnector_transaction_contract_begin_phase(&c,phases[i],2)!=0)abort();
        if(msconnector_transaction_contract_complete_phase(&c,phases[i],2)!=0)abort();
    }
    (void)msconnector_transaction_contract_set_response_committed(&c,0);
    (void)msconnector_transaction_contract_set_response_committed(&c,1);
    (void)msconnector_transaction_contract_set_response_committed(&c,1);
    (void)msconnector_transaction_contract_complete_phase(&c,MSCONNECTOR_PHASE_REQUEST_BODY,2);
    (void)msconnector_transaction_contract_finish(&c,3);
    (void)msconnector_transaction_contract_finish(&c,4);
    (void)msconnector_transaction_contract_cleanup(&c,5);
    msc_transaction_cleanup(t);
    if (errno != EILSEQ) abort();
    for(size_t i=0;i<5U;++i) if(native_calls[i]!=before[i]+1U)abort();
    return NULL;
}
int main(int argc,char **argv) {
    if (argc != 2) return 2;
    if (strcmp(argv[1],"live") == 0) {
        msconnector_transaction_contract *c=malloc(sizeof(*c));if(!c)return 11;
        if(msconnector_transaction_contract_init(c,NULL,"live","test","test",0,1)!=0)return 12;
        return 0; /* Intentionally retain live object: missing cleanup control. */
    }
    if (strcmp(argv[1],"terminal") == 0) {
        msconnector_transaction_contract c;
        if(msconnector_transaction_contract_init(&c,NULL,"terminal","test","test",0,1)!=0)return 13;
        if(msconnector_transaction_contract_fail(&c,MSCONNECTOR_TRANSACTION_ERROR_CONNECTOR,2)!=0)return 14;
        if(msconnector_transaction_contract_finish(&c,3)!=0)return 15;
        if(msconnector_transaction_contract_finish(&c,4)!=0)return 16;
        (void)msconnector_transaction_contract_cleanup(&c,5);return 0;
    }
    if (strcmp(argv[1],"closed") == 0) close(atoi(getenv("MSCONNECTOR_LIFECYCLE_FD")));
    if (strcmp(argv[1],"partial") == 0) {
        struct stat st;int fd=atoi(getenv("MSCONNECTOR_LIFECYCLE_FD"));
        if(fstat(fd,&st)!=0)return 9;
        struct rlimit limit={(rlim_t)st.st_size+100U,(rlim_t)st.st_size+100U};
        if(signal(SIGXFSZ,SIG_IGN)==SIG_ERR || setrlimit(RLIMIT_FSIZE,&limit)!=0)return 10;
    }
    if (strcmp(argv[1],"overflow") == 0 || strcmp(argv[1],"duplicate") == 0) {
        size_t count = strcmp(argv[1],"duplicate") == 0 ? 1U : 257U;
        msconnector_transaction_contract *c=calloc(count,sizeof(*c));if(!c)return 7;
        for(size_t i=0;i<count;++i)
            if(msconnector_transaction_contract_init(&c[i],NULL,"map","test","test",0,1)!=0)return 8;
        if(count==1U) (void)msconnector_transaction_contract_init(c,NULL,"again","test","test",0,1);
        for(size_t i=0;i<count;++i) (void)msconnector_transaction_contract_cleanup(&c[i],2);
        free(c);return 0;
    }
    if (strcmp(argv[1],"threads") == 0) {
        pthread_t a,b;
        if (pthread_create(&a,NULL,cycle,"one") || pthread_create(&b,NULL,cycle,"two")) return 3;
        pthread_join(a,NULL);pthread_join(b,NULL);
    } else if (strcmp(argv[1],"fork") == 0) {
        pid_t child=fork();if(child<0)return 4;
        if(child==0){cycle("child");exit(0);}int status;waitpid(child,&status,0);
        if(status!=0)return 5;
        cycle("parent");
    } else {
        cycle("quote\"id");cycle("reuse");
        if (msc_new_transaction_with_id(NULL,NULL,"failure",NULL) != NULL || errno != EDOM) return 6;
        Transaction *t=msc_new_transaction(NULL,NULL,NULL);msc_transaction_cleanup(t);
    }
    return 0;
}
'''


class NativeLifecycleObserverTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        global OUTPUT
        required = ("NATIVE_OBSERVER_TEST_OUT", "MODSECURITY_INCLUDE_DIR", "MODSECURITY_LIB_DIR")
        missing = [name for name in required if not os.environ.get(name)]
        if missing:
            raise unittest.SkipTest("native observer unqualified: explicit configuration missing: " + ", ".join(missing))
        OUTPUT = Path(os.environ["NATIVE_OBSERVER_TEST_OUT"]).resolve()
        cls.include = Path(os.environ["MODSECURITY_INCLUDE_DIR"]).resolve()
        cls.library_directory = Path(os.environ["MODSECURITY_LIB_DIR"]).resolve()
        cls.library = cls.library_directory / "libmodsecurity.so"
        if not (cls.include / "modsecurity/transaction.h").is_file() or not cls.library.is_file():
            raise RuntimeError("explicit selected SDK is missing transaction.h or libmodsecurity.so; no system fallback")
        OUTPUT.mkdir(parents=True, exist_ok=True)
        cls.directory = tempfile.TemporaryDirectory(prefix="observer-", dir=OUTPUT)
        cls.work = Path(cls.directory.name)
        fixture = cls.work / "fixture.c"
        native = cls.work / "native.c"
        declarations, implementation = FIXTURE.split("static _Thread_local int token;", 1)
        native_implementation, main = implementation.split("static void *cycle", 1)
        native.write_text(declarations + "static _Thread_local int token;" + native_implementation, encoding="utf-8")
        fixture.write_text(declarations + "static void *cycle" + main, encoding="utf-8")
        cls.binary = cls.work / "fixture"
        command = ["cc", "-std=c17", "-D_POSIX_C_SOURCE=200809L", "-Wall", "-Wextra", "-Werror",
                   "-pthread", "-I", str(ROOT / "common/include"), "-I", str(cls.include),
                   str(ROOT / "ci/runtime/lifecycle/native-lifecycle-observer.c"), str(fixture), str(native),
                   str(ROOT / "common/src/transaction_state.c"),
                   str(ROOT / "common/src/decision_action.c"), "-o", str(cls.binary)]
        command.extend(f"-Wl,--wrap={symbol}" for symbol in SYMBOLS)
        result = subprocess.run(command, capture_output=True, text=True, check=False)
        (OUTPUT / "compile.json").write_text(json.dumps({"argv": command, "returncode": result.returncode,
                                                         "stdout": result.stdout, "stderr": result.stderr,
                                                         "selected_sdk_include": str(cls.include),
                                                         "selected_sdk_library": str(cls.library.resolve()),
                                                         "selected_sdk_library_sha256": hashlib.sha256(cls.library.read_bytes()).hexdigest()}), encoding="utf-8")
        if result.returncode:
            raise RuntimeError(result.stderr)

    @classmethod
    def tearDownClass(cls):
        cls.directory.cleanup()

    def run_fixture(self, mode="normal", configured=True, permissions=0o600):
        path = self.work / f"{self._testMethodName}.jsonl"
        descriptor = os.open(path, os.O_CREAT | os.O_WRONLY | os.O_APPEND | os.O_EXCL, permissions)
        environment = os.environ.copy()
        environment["LD_LIBRARY_PATH"] = str(self.library_directory)
        environment.pop("MSCONNECTOR_LIFECYCLE_FD", None)
        if configured:
            environment.update(MSCONNECTOR_LIFECYCLE_FD=str(descriptor), MSCONNECTOR_LIFECYCLE_RUN="control",
                               MSCONNECTOR_LIFECYCLE_PROFILE="unit", MSCONNECTOR_LIFECYCLE_CASE='escape"case')
        try:
            result = subprocess.run([str(self.binary), mode], env=environment, pass_fds=(descriptor,),
                                    capture_output=True, text=True, check=False)
        finally:
            os.close(descriptor)
        self.assertEqual(result.returncode, 0, result.stderr)
        raw_lines = path.read_text(encoding="utf-8").splitlines()
        if mode == "partial":
            self.assertGreater(len(raw_lines), 1)
            with self.assertRaises(json.JSONDecodeError):
                json.loads(raw_lines[-1])
            raw_lines = raw_lines[:-1]
        events = [json.loads(line) for line in raw_lines]
        (OUTPUT / f"{self._testMethodName}.json").write_text(json.dumps({"mode": mode, "events": events,
                                                                       "stderr": result.stderr,
                                                                       "partial_record": path.read_text(encoding="utf-8").splitlines()[-1] if mode == "partial" else None}), encoding="utf-8")
        return events, result.stderr

    def assert_pairs(self, events):
        enters = {(e["pid"], e["call"]): e for e in events if e["edge"] == "enter"}
        returns = {(e["pid"], e["call"]): e for e in events if e["edge"] == "return"}
        self.assertEqual(set(enters), set(returns))
        for key, entry in enters.items():
            self.assertEqual(entry["function"], returns[key]["function"])
        self.assertTrue(all(not e["invalid"] for e in events))
        self.assertTrue(all(e["host_eos"] is None and e["native_mime_selection"] is None for e in events))

    def test_real_common_failures_attempts_id_reuse_and_native_passthrough(self):
        events, stderr = self.run_fixture()
        self.assertEqual(stderr, "")
        self.assert_pairs(events)
        body = [e for e in events if e["function"] == "native_process_request_body" and e["edge"] == "return"]
        self.assertEqual([e["result"] for e in body], [-7, -7])
        self.assertEqual([e["transaction_id"] for e in body], ['quote"id', "reuse"])
        finishes = [e for e in events if e["function"] == "common_finish" and e["edge"] == "return"]
        self.assertEqual(len(finishes), 4)
        self.assertTrue(any(e["result"] != 0 for e in finishes))
        anonymous = [e for e in events if e["function"] == "native_new" and e["edge"] == "return"]
        self.assertIsNone(anonymous[0]["transaction_id"])
        failure = [e for e in events if e["function"] == "native_new_with_id" and e["edge"] == "return" and e["result"] == 0]
        self.assertEqual(len(failure), 1)

    def test_concurrent_ids(self):
        events, _ = self.run_fixture("threads")
        self.assert_pairs(events)
        ids = {e["transaction_id"] for e in events if e["function"] == "native_process_logging"}
        self.assertEqual(ids, {"one", "two"})

    def test_map_overflow_invalidates_receipt(self):
        events, stderr = self.run_fixture("overflow")
        self.assertTrue(events[-1]["invalid"])
        self.assertIn("evidence invalid", stderr)

    def test_reinitialization_without_cleanup_invalidates_receipt(self):
        events, stderr = self.run_fixture("duplicate")
        self.assertTrue(events[-1]["invalid"])
        self.assertIn("evidence invalid", stderr)

    def test_common_canonical_key_is_not_inferred_from_native_id(self):
        events, _ = self.run_fixture()
        common = [e for e in events if e["function"] == "common_init" and e["edge"] == "return"]
        self.assertTrue(all(e["canonical_transaction_id"] for e in common))
        self.assertNotEqual(common[0]["canonical_transaction_id"], common[1]["canonical_transaction_id"])
        native = [e for e in events if e["function"].startswith("native_")]
        self.assertTrue(all(e["canonical_transaction_id"] is None for e in native))

    def test_commit_arguments_and_observed_states_distinguish_attempts(self):
        events, _ = self.run_fixture()
        commits = [e for e in events if e["function"] == "common_set_response_committed"]
        entries = [e for e in commits if e["edge"] == "enter"]
        returns = [e for e in commits if e["edge"] == "return"]
        self.assertEqual([e["argument_committed"] for e in entries], [0, 1, 1, 0, 1, 1])
        self.assertEqual([e["contract_state"]["response_committed"] for e in entries], [0, 0, 1, 0, 0, 1])
        self.assertEqual([e["contract_state"]["response_committed"] for e in returns], [0, 1, 1, 0, 1, 1])

    def test_successful_finish_on_terminal_state_is_not_a_completion_transition(self):
        events, _ = self.run_fixture("terminal")
        finishes = [e for e in events if e["function"] == "common_finish"]
        self.assertEqual(len(finishes), 4)
        self.assertEqual([e["result"] for e in finishes if e["edge"] == "return"], [0, 0])
        statuses = [e["contract_state"]["status"] for e in finishes]
        self.assertTrue(all(status == statuses[0] for status in statuses))

    def test_final_live_mapping_does_not_prove_cleanup(self):
        events, _ = self.run_fixture("live")
        self.assertFalse(events[-1]["invalid"])
        self.assertEqual(events[-1]["live_mappings"], 1)
        self.assertFalse(any(e["function"] == "common_cleanup" for e in events))

    def test_genuine_sdk_constructor_and_physical_cleanup(self):
        source = self.work / "genuine.c"
        source.write_text(r'''
#include <modsecurity/modsecurity.h>
#include <modsecurity/rules_set.h>
#include <modsecurity/transaction.h>
int main(void) {
    ModSecurity *m=msc_init();RulesSet *r=msc_create_rules_set();
    if(!m || !r)return 2;
    Transaction *t=msc_new_transaction_with_id(m,r,"genuine-sdk",0);
    if(!t)return 3;
    msc_transaction_cleanup(t);msc_rules_cleanup(r);msc_cleanup(m);return 0;
}
''', encoding="utf-8")
        binary = self.work / "genuine"
        command = ["cc", "-std=c17", "-D_POSIX_C_SOURCE=200809L", "-Wall", "-Wextra", "-Werror",
                   "-pthread", "-I", str(ROOT / "common/include"), "-I", str(self.include),
                   str(ROOT / "ci/runtime/lifecycle/native-lifecycle-observer.c"), str(source),
                   str(ROOT / "common/src/transaction_state.c"), str(ROOT / "common/src/decision_action.c"),
                   str(self.library), f"-Wl,-rpath,{self.library_directory}", "-o", str(binary)]
        command.extend(f"-Wl,--wrap={symbol}" for symbol in SYMBOLS)
        result = subprocess.run(command, capture_output=True, text=True, check=False)
        self.assertEqual(result.returncode, 0, result.stderr)
        previous = self.binary
        try:
            self.binary = binary
            events, stderr = self.run_fixture()
        finally:
            self.binary = previous
        self.assertEqual(stderr, "")
        self.assert_pairs(events)
        cleanup = [e for e in events if e["function"] == "native_cleanup" and e["edge"] == "return"]
        self.assertEqual(len(cleanup), 1)
        self.assertEqual(cleanup[0]["transaction_id"], "genuine-sdk")
        self.assertIsNone(cleanup[0]["result"])

    def test_fork_receipts(self):
        events, _ = self.run_fixture("fork")
        self.assert_pairs(events)
        self.assertEqual(len({e["pid"] for e in events if e["edge"] == "final"}), 2)

    def test_write_failure_is_invalid_without_changing_real_results(self):
        events, stderr = self.run_fixture("closed")
        self.assertEqual(len(events), 1)
        self.assertIn("evidence invalid", stderr)

    def test_partial_write_invalidates_evidence_without_changing_real_results(self):
        events, stderr = self.run_fixture("partial")
        self.assertEqual(len(events), 1)
        self.assertIn("evidence invalid", stderr)

    def test_missing_descriptor_produces_no_qualified_evidence(self):
        events, _ = self.run_fixture(configured=False)
        self.assertEqual(events, [])

    def test_public_descriptor_rejected(self):
        events, stderr = self.run_fixture(permissions=0o644)
        self.assertEqual(events, [])
        self.assertIn("admission rejected", stderr)


if __name__ == "__main__":
    unittest.main()
