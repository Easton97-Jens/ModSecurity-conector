package response_observer

import (
	"encoding/json"
	"os"
	"path/filepath"
	"testing"
)

func TestI12PrivateObserverRecordsOnlyActualSyntheticMetadata(t *testing.T) {
	previous := i12ObserverPath
	i12ObserverPath = filepath.Join(t.TempDir(), "host.jsonl")
	defer func() { i12ObserverPath = previous }()
	if err := os.WriteFile(i12ObserverPath, nil, 0600); err != nil {
		t.Fatal(err)
	}
	i12Observe("unknown-id", "must-not-record", map[string]interface{}{"bytes": 99})
	i12Observe("tf-fa-req-target-6c428a1e", "writer_write_body_return", map[string]interface{}{"bytes": 3, "error": false})
	raw, err := os.ReadFile(i12ObserverPath)
	if err != nil {
		t.Fatal(err)
	}
	var record map[string]interface{}
	if err := json.Unmarshal(raw, &record); err != nil {
		t.Fatal(err)
	}
	if record["operation"] != "writer_write_body_return" || record["transaction_id"] != "tf-fa-req-target-6c428a1e" {
		t.Fatalf("unobserved operation or ID recorded: %v", record)
	}
	if record["wall_ns"].(float64) <= 0 || record["elapsed_monotonic_ns"].(float64) < 0 {
		t.Fatalf("clock observation invalid: %v", record)
	}
	if record["fields"].(map[string]interface{})["bytes"].(float64) != 3 {
		t.Fatalf("observed count changed: %v", record)
	}
}

func TestI12PrivateObserverRejectsUnprotectedOutput(t *testing.T) {
	previous := i12ObserverPath
	i12ObserverPath = filepath.Join(t.TempDir(), "bad.jsonl")
	defer func() { i12ObserverPath = previous }()
	if err := os.WriteFile(i12ObserverPath, nil, 0644); err != nil {
		t.Fatal(err)
	}
	i12Observe("tf-fa-req-target-6c428a1e", "must-not-record", map[string]interface{}{})
	raw, err := os.ReadFile(i12ObserverPath)
	if err != nil || len(raw) != 0 {
		t.Fatalf("invalid output admitted: bytes=%d error=%v", len(raw), err)
	}
}

func TestI12PrivateObserverRejectsSymlinkOutput(t *testing.T) {
	previous := i12ObserverPath
	dir := t.TempDir()
	i12ObserverPath = filepath.Join(dir, "link.jsonl")
	defer func() { i12ObserverPath = previous }()
	target := filepath.Join(dir, "real.jsonl")
	if err := os.WriteFile(target, nil, 0600); err != nil {
		t.Fatal(err)
	}
	if err := os.Symlink(target, i12ObserverPath); err != nil {
		t.Fatal(err)
	}
	i12Observe("tf-fa-req-target-6c428a1e", "must-not-record", map[string]interface{}{})
	raw, err := os.ReadFile(target)
	if err != nil || len(raw) != 0 {
		t.Fatalf("symlink output admitted: bytes=%d error=%v", len(raw), err)
	}
}
