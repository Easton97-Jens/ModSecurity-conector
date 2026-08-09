"""Regression contract for Phase 2 when request-body buffering is disabled."""

from pathlib import Path


SOURCE = (
    Path(__file__).resolve().parents[1]
    / "common"
    / "runtime"
    / "msconnector_runtime.c"
).read_text(encoding="utf-8")


def test_body_mode_none_finishes_modsecurity_request_body_phase() -> None:
    none_branch = SOURCE.index(
        "runtime->body_policy.request_body_mode == MSCONNECTOR_BODY_MODE_NONE",
        SOURCE.index("static int begin_request_body_processing"),
    )
    buffered_branch = SOURCE.index(
        "runtime->body_policy.request_body_mode == MSCONNECTOR_BODY_MODE_BUFFERED",
        none_branch,
    )
    branch = SOURCE[none_branch:buffered_branch]

    assert "msconnector_runtime_transaction_finish_request_body" in branch
    assert "mark_flow(transaction, MSCONNECTOR_PHASE_REQUEST_BODY" not in branch


def test_finish_request_body_does_not_skip_none_mode() -> None:
    start = SOURCE.index("int msconnector_runtime_transaction_finish_request_body(")
    end = SOURCE.index(
        "int msconnector_runtime_transaction_process_response_headers(", start
    )
    finish_body = SOURCE[start:end]

    assert "msconnector_modsecurity_finish_request_body" in finish_body
    assert "request_body_mode == MSCONNECTOR_BODY_MODE_NONE" not in finish_body
