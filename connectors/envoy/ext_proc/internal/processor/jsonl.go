package processor

import (
	"encoding/json"
	"fmt"
	"os"
	"path/filepath"
	"sync"
)

// JSONLObserver writes one payload-free completion record per ext_proc stream.
// The record is intentionally limited to transport/lifecycle counters and
// action metadata so it is safe to archive as connector runtime evidence.
type JSONLObserver struct {
	mu             sync.Mutex
	file           *os.File
	evaluationMode string
	ruleEvaluation string
}

type jsonlCompletionRecord struct {
	Event               string            `json:"event"`
	IntegrationMode     string            `json:"integration_mode"`
	EvaluationMode      string            `json:"evaluation_mode"`
	RuleEvaluation      string            `json:"rule_evaluation"`
	TransactionID       string            `json:"transaction_id,omitempty"`
	RequestHeaderCount  uint64            `json:"request_header_count"`
	ResponseHeaderCount uint64            `json:"response_header_count"`
	RequestBodyChunks   uint64            `json:"request_body_chunks"`
	ResponseBodyChunks  uint64            `json:"response_body_chunks"`
	RequestBodyBytes    int64             `json:"request_body_bytes"`
	ResponseBodyBytes   int64             `json:"response_body_bytes"`
	LateAction          LateActionOutcome `json:"late_action"`
	CloseReason         CloseReason       `json:"close_reason"`
}

// NewJSONLObserver opens an absolute, owner-readable event path. The caller
// controls the enclosing runtime directory; this package does not create any
// evidence inside the checkout.
func NewJSONLObserver(path string) (*JSONLObserver, error) {
	return NewJSONLObserverWithMode(path, "passthrough_nonpromoted", "not_wired")
}

// NewJSONLObserverWithMode writes stream-completion metadata for the concrete
// engine selected by the executable. It does not create rule decision events;
// Common Runtime remains the only source of any configured decision event.
func NewJSONLObserverWithMode(path, evaluationMode, ruleEvaluation string) (*JSONLObserver, error) {
	if path == "" {
		return nil, fmt.Errorf("event log path is required")
	}
	if evaluationMode == "" || ruleEvaluation == "" {
		return nil, fmt.Errorf("event evaluation mode is required")
	}
	if !filepath.IsAbs(path) {
		return nil, fmt.Errorf("event log path must be absolute")
	}
	if err := os.MkdirAll(filepath.Dir(path), 0o750); err != nil {
		return nil, fmt.Errorf("create event log directory: %w", err)
	}
	file, err := os.OpenFile(path, os.O_APPEND|os.O_CREATE|os.O_WRONLY, 0o600)
	if err != nil {
		return nil, fmt.Errorf("open event log: %w", err)
	}
	return &JSONLObserver{
		file:           file,
		evaluationMode: evaluationMode,
		ruleEvaluation: ruleEvaluation,
	}, nil
}

func (observer *JSONLObserver) Record(summary Summary) error {
	if observer == nil || observer.file == nil {
		return fmt.Errorf("event observer is closed")
	}
	record := jsonlCompletionRecord{
		Event:               "ext_proc_stream_complete",
		IntegrationMode:     "ext_proc",
		EvaluationMode:      observer.evaluationMode,
		RuleEvaluation:      observer.ruleEvaluation,
		TransactionID:       summary.TransactionID,
		RequestHeaderCount:  summary.RequestHeaderCount,
		ResponseHeaderCount: summary.ResponseHeaderCount,
		RequestBodyChunks:   summary.RequestBodyChunks,
		ResponseBodyChunks:  summary.ResponseBodyChunks,
		RequestBodyBytes:    summary.RequestBodyBytes,
		ResponseBodyBytes:   summary.ResponseBodyBytes,
		LateAction:          summary.LateAction,
		CloseReason:         summary.CloseReason,
	}
	encoded, err := json.Marshal(record)
	if err != nil {
		return fmt.Errorf("encode event: %w", err)
	}
	observer.mu.Lock()
	defer observer.mu.Unlock()
	if _, err := observer.file.Write(append(encoded, '\n')); err != nil {
		return fmt.Errorf("write event: %w", err)
	}
	return nil
}

func (observer *JSONLObserver) Close() error {
	if observer == nil || observer.file == nil {
		return nil
	}
	observer.mu.Lock()
	defer observer.mu.Unlock()
	err := observer.file.Close()
	observer.file = nil
	return err
}
