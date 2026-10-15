//go:build libmodsecurity

package processor

import (
	"context"
	"encoding/json"
	"os"
	"path/filepath"
	"strings"
	"testing"
)

func TestI12PrivateEnvoyPhysicalTypedScopeAndEOS(t *testing.T) {
	path := filepath.Join(t.TempDir(), "physical-host.jsonl")
	if err := os.WriteFile(path, nil, 0600); err != nil {
		t.Fatal(err)
	}
	t.Setenv("I12_ENVOY_HOST_TRACE_PATH", path)
	engine, _ := newCommonRuntimeEngineForTest(t, 1048576, "Reject", 1048576, "Reject")
	ctx := context.Background()
	value, err := engine.Open(ctx, commonTestStreamMetadata("i12-private-control"))
	if err != nil {
		t.Fatal(err)
	}
	transaction := value.(*commonRuntimeTransaction)
	transaction.I12Observe(11, 0, 1, 3, 3, true)
	raw, _ := os.ReadFile(path)
	if len(raw) != 0 {
		t.Fatal("unbegun transaction invented a live scope")
	}
	decision, err := transaction.ProcessHeaders(ctx, DirectionRequest, []Header{{Name: "host", Value: []byte("example.test")}}, false)
	assertCommonDecision(t, "headers", decision, err, ActionAllow, 0)
	decision, err = transaction.ProcessBody(ctx, DirectionRequest, []byte("abc"), false)
	assertCommonDecision(t, "partial", decision, err, ActionAllow, 0)
	decision, err = transaction.ProcessBody(ctx, DirectionRequest, nil, true)
	assertCommonDecision(t, "EOS", decision, err, ActionAllow, 0)
	raw, err = os.ReadFile(path)
	if err != nil {
		t.Fatal(err)
	}
	var inputs, finishes int
	var scope float64
	for _, line := range strings.Split(strings.TrimSpace(string(raw)), "\n") {
		var row map[string]interface{}
		if err := json.Unmarshal([]byte(line), &row); err != nil {
			t.Fatal(err)
		}
		if row["allocation_scope_call"].(float64) <= 0 || row["wall_ns"].(float64) <= 0 || row["monotonic_ns"].(float64) <= 0 {
			t.Fatalf("missing actual scope/clock: %v", row)
		}
		if scope == 0 {
			scope = row["allocation_scope_call"].(float64)
		}
		if row["allocation_scope_call"] != scope {
			t.Fatal("typed scope changed within transaction")
		}
		op := int(row["operation"].(float64))
		if op == 1 {
			inputs++
			if inputs == 1 && row["body_end_of_stream_argument"] != false {
				t.Fatal("partial append manufactured EOS")
			}
		}
		if op == 3 {
			finishes++
			if row["body_end_of_stream_argument"] != true {
				t.Fatal("actual finish lost EOS argument")
			}
		}
	}
	if inputs != 2 || finishes != 1 {
		t.Fatalf("input/finish counts %d/%d", inputs, finishes)
	}
	before := len(raw)
	decision, err = transaction.ProcessBody(ctx, DirectionRequest, nil, true)
	if err == nil {
		t.Fatalf("duplicate EOS unexpectedly succeeded: %v", decision)
	}
	raw, _ = os.ReadFile(path)
	if len(raw) != before {
		t.Fatal("rejected duplicate manufactured accepted EOS trace")
	}
	transaction.Close(ctx, Summary{CloseReason: ClosePeerEOF})
	before = len(raw)
	transaction.I12Observe(5, 1, 0, 0, 0, true)
	raw, _ = os.ReadFile(path)
	if len(raw) != before {
		t.Fatal("closed transaction produced live typed scope")
	}
}
