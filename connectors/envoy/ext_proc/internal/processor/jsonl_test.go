package processor

import (
	"os"
	"path/filepath"
	"strings"
	"testing"
)

func TestJSONLObserverWritesMetadataOnlyCompletionRecord(t *testing.T) {
	path := filepath.Join(t.TempDir(), "events.jsonl")
	observer, err := NewJSONLObserver(path)
	if err != nil {
		t.Fatalf("NewJSONLObserver() error = %v", err)
	}
	defer observer.Close()
	if err := observer.Record(Summary{
		TransactionID:      "test-transaction",
		RequestHeaderCount: 3,
		ResponseBodyBytes:  17,
		LateAction:         LateActionNone,
		CloseReason:        CloseResponseEOS,
	}); err != nil {
		t.Fatalf("Record() error = %v", err)
	}
	content, err := os.ReadFile(path)
	if err != nil {
		t.Fatalf("ReadFile() error = %v", err)
	}
	line := string(content)
	for _, expected := range []string{
		`"integration_mode":"ext_proc"`,
		`"evaluation_mode":"passthrough_nonpromoted"`,
		`"rule_evaluation":"not_wired"`,
		`"transaction_id":"test-transaction"`,
	} {
		if !strings.Contains(line, expected) {
			t.Fatalf("event record missing %s: %s", expected, line)
		}
	}
	for _, forbidden := range []string{`"headers"`, `"body":"`, `"request_body":"`, `"response_body":"`} {
		if strings.Contains(line, forbidden) {
			t.Fatalf("event record contains payload-bearing field %s: %s", forbidden, line)
		}
	}
}

func TestJSONLObserverRejectsRelativePath(t *testing.T) {
	if _, err := NewJSONLObserver("events.jsonl"); err == nil {
		t.Fatal("NewJSONLObserver() accepted relative path")
	}
}
