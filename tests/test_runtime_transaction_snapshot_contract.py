"""Static contract checks for the payload-free Common transaction snapshot."""

from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
HEADER = ROOT / "common/runtime/msconnector_runtime.h"
IMPLEMENTATION = ROOT / "common/runtime/msconnector_runtime.c"


class RuntimeTransactionSnapshotContractTest(unittest.TestCase):
    def test_snapshot_is_bounded_value_state(self) -> None:
        source = HEADER.read_text(encoding="utf-8")
        start = source.index("typedef struct msconnector_runtime_transaction_snapshot")
        end = source.index("} msconnector_runtime_transaction_snapshot;", start)
        snapshot = source[start:end]
        self.assertIn("msconnector_transaction_contract contract;", snapshot)
        self.assertIn("msconnector_runtime_body_progress request_body;", snapshot)
        self.assertIn("msconnector_runtime_body_progress response_body;", snapshot)
        self.assertNotIn("*", snapshot)
        self.assertIn("msconnector_runtime_transaction_snapshot_get", source)

    def test_accessor_copies_only_bounded_members(self) -> None:
        source = IMPLEMENTATION.read_text(encoding="utf-8")
        start = source.index("int msconnector_runtime_transaction_snapshot_get")
        end = source.index("int msconnector_runtime_transaction_process_response", start)
        function = source[start:end]
        self.assertIn("snapshot->contract = transaction->contract;", function)
        self.assertIn("snapshot->request_body = transaction->request_body;", function)
        self.assertIn("snapshot->response_body = transaction->response_body;", function)
        self.assertNotIn("event_file", function)
        self.assertNotIn("body.data", function)

    def test_finalizer_captures_only_the_completed_cleanup_state(self) -> None:
        source = IMPLEMENTATION.read_text(encoding="utf-8")
        start = source.index("int msconnector_runtime_transaction_finalize_and_snapshot")
        end = source.index("int msconnector_runtime_transaction_process_response", start)
        function = source[start:end]
        self.assertIn("runtime_transaction_cleanup_checked(transaction, error)", function)
        self.assertIn("msconnector_runtime_transaction_snapshot_get(transaction, snapshot)", function)
        self.assertIn("snapshot->contract.cleanup_complete", function)
        self.assertIn("MSCONNECTOR_TRANSACTION_STATUS_CLEANED", function)


if __name__ == "__main__":
    unittest.main()
