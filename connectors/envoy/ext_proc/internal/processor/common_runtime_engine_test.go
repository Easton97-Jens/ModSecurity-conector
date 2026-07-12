//go:build libmodsecurity

package processor

import (
	"context"
	"encoding/json"
	"fmt"
	"os"
	"path/filepath"
	"strings"
	"sync"
	"testing"
)

func TestCommonRuntimeEngineEvaluatesIncrementalLifecycle(t *testing.T) {
	engine, _ := newCommonRuntimeEngineForTest(t)
	contextValue := context.Background()

	testCases := []struct {
		name string
		run  func(t *testing.T, transaction Transaction)
	}{
		{
			name: "phase1_request_headers",
			run: func(t *testing.T, transaction Transaction) {
				decision, err := transaction.ProcessHeaders(contextValue, DirectionRequest, []Header{{Name: "x-ms-p1", Value: []byte("block")}}, true)
				if err != nil || decision.Action != ActionDeny || decision.Status != 403 {
					t.Fatalf("phase-1 decision=%#v err=%v", decision, err)
				}
				recorder, ok := transaction.(HostActionRecorder)
				if !ok {
					t.Fatal("Common transaction does not expose host-action recording")
				}
				if err := recorder.RecordHostAction(contextValue, HostAction{
					Action: AppliedActionDeny, VisibleStatus: 403, TransportResult: "http_status",
				}); err != nil {
					t.Fatalf("RecordHostAction() error = %v", err)
				}
			},
		},
		{
			name: "phase2_request_body_eos",
			run: func(t *testing.T, transaction Transaction) {
				if decision, err := transaction.ProcessHeaders(contextValue, DirectionRequest, []Header{{Name: "host", Value: []byte("example.test")}}, false); err != nil || decision.Action != ActionAllow {
					t.Fatalf("request headers decision=%#v err=%v", decision, err)
				}
				decision, err := transaction.ProcessBody(contextValue, DirectionRequest, []byte("envoy-phase2-marker"), true)
				if err != nil || decision.Action != ActionDeny || decision.Status != 403 {
					t.Fatalf("phase-2 decision=%#v err=%v", decision, err)
				}
			},
		},
		{
			name: "phase3_response_headers_before_commit",
			run: func(t *testing.T, transaction Transaction) {
				if decision, err := transaction.ProcessHeaders(contextValue, DirectionRequest, nil, true); err != nil || decision.Action != ActionAllow {
					t.Fatalf("request headers decision=%#v err=%v", decision, err)
				}
				decision, err := transaction.ProcessHeaders(contextValue, DirectionResponse, []Header{
					{Name: ":status", Value: []byte("200")},
					{Name: "x-ms-p3", Value: []byte("block")},
				}, false)
				if err != nil || decision.Action != ActionDeny || decision.Status != 403 {
					t.Fatalf("phase-3 decision=%#v err=%v", decision, err)
				}
			},
		},
		{
			name: "phase4_response_body_eos",
			run: func(t *testing.T, transaction Transaction) {
				if decision, err := transaction.ProcessHeaders(contextValue, DirectionRequest, nil, true); err != nil || decision.Action != ActionAllow {
					t.Fatalf("request headers decision=%#v err=%v", decision, err)
				}
				if decision, err := transaction.ProcessHeaders(contextValue, DirectionResponse, []Header{
					{Name: ":status", Value: []byte("200")},
					{Name: "content-type", Value: []byte("text/plain")},
				}, false); err != nil || decision.Action != ActionAllow {
					t.Fatalf("response headers decision=%#v err=%v", decision, err)
				}
				committer, ok := transaction.(ResponseCommitter)
				if !ok {
					t.Fatal("Common transaction does not expose response commit bookkeeping")
				}
				if err := committer.MarkResponseCommitted(contextValue); err != nil {
					t.Fatalf("MarkResponseCommitted() error = %v", err)
				}
				decision, err := transaction.ProcessBody(contextValue, DirectionResponse, []byte("envoy-phase4-marker"), true)
				if err != nil || decision.Action != ActionDeny || decision.Status != 403 {
					t.Fatalf("phase-4 decision=%#v err=%v", decision, err)
				}
				if err := committer.(HostActionRecorder).RecordHostAction(contextValue, HostAction{
					Action: AppliedActionLogOnly, VisibleStatus: 200, TransportResult: "log_only",
				}); err != nil {
					t.Fatalf("RecordHostAction() error = %v", err)
				}
			},
		},
	}

	for _, testCase := range testCases {
		t.Run(testCase.name, func(t *testing.T) {
			transaction, err := engine.Open(contextValue, commonTestStreamMetadata(testCase.name))
			if err != nil {
				t.Fatalf("Open() error = %v", err)
			}
			defer transaction.Close(contextValue, Summary{CloseReason: ClosePeerEOF})
			testCase.run(t, transaction)
		})
	}
}

func TestCommonRuntimeEngineSerializesParallelStreams(t *testing.T) {
	engine, _ := newCommonRuntimeEngineForTest(t)
	const streamCount = 12
	errors := make(chan error, streamCount)
	var workers sync.WaitGroup
	for index := 0; index < streamCount; index++ {
		workers.Add(1)
		go func(index int) {
			defer workers.Done()
			transaction, err := engine.Open(context.Background(), commonTestStreamMetadata(fmt.Sprintf("parallel-%d", index)))
			if err != nil {
				errors <- err
				return
			}
			defer transaction.Close(context.Background(), Summary{CloseReason: CloseResponseEOS})
			if decision, err := transaction.ProcessHeaders(context.Background(), DirectionRequest, nil, true); err != nil || decision.Action != ActionAllow {
				errors <- fmt.Errorf("request %d: decision=%#v err=%w", index, decision, err)
				return
			}
			if decision, err := transaction.ProcessHeaders(context.Background(), DirectionResponse, []Header{{Name: ":status", Value: []byte("200")}}, true); err != nil || decision.Action != ActionAllow {
				errors <- fmt.Errorf("response %d: decision=%#v err=%w", index, decision, err)
			}
		}(index)
	}
	workers.Wait()
	close(errors)
	for err := range errors {
		if err != nil {
			t.Fatal(err)
		}
	}
}

func TestCommonRuntimeEngineUsesCanonicalEnvoyEventIdentity(t *testing.T) {
	engine, eventPath := newCommonRuntimeEngineForTest(t)
	contextValue := context.Background()
	transaction, err := engine.Open(contextValue, commonTestStreamMetadata("canonical-event-identity"))
	if err != nil {
		t.Fatalf("Open() error = %v", err)
	}
	decision, err := transaction.ProcessHeaders(contextValue, DirectionRequest, []Header{{Name: "x-ms-p1", Value: []byte("block")}}, true)
	if err != nil || decision.Action != ActionDeny {
		t.Fatalf("request decision=%#v err=%v", decision, err)
	}
	recorder, ok := transaction.(HostActionRecorder)
	if !ok {
		t.Fatal("Common transaction does not expose host-action recording")
	}
	if err := recorder.RecordHostAction(contextValue, HostAction{
		Action: AppliedActionDeny, VisibleStatus: 403, TransportResult: "http_status",
	}); err != nil {
		t.Fatalf("RecordHostAction() error = %v", err)
	}
	transaction.Close(contextValue, Summary{CloseReason: CloseImmediateResponse})

	raw, err := os.ReadFile(eventPath)
	if err != nil {
		t.Fatalf("ReadFile(%s): %v", eventPath, err)
	}
	for _, line := range strings.Split(strings.TrimSpace(string(raw)), "\n") {
		if line == "" {
			continue
		}
		var event map[string]any
		if err := json.Unmarshal([]byte(line), &event); err != nil {
			t.Fatalf("unmarshal Common event: %v", err)
		}
		if event["connector"] != "envoy" || event["integration_mode"] != "ext_proc" {
			t.Fatalf("Common event identity = connector=%#v integration_mode=%#v, want envoy/ext_proc", event["connector"], event["integration_mode"])
		}
	}
}

func newCommonRuntimeEngineForTest(t *testing.T) (*CommonRuntimeEngine, string) {
	t.Helper()
	directory := t.TempDir()
	rulesPath := filepath.Join(directory, "rules.conf")
	configPath := filepath.Join(directory, "runtime.conf")
	eventPath := filepath.Join(directory, "events.jsonl")
	rules := `SecRuleEngine On
SecRequestBodyAccess On
SecResponseBodyAccess On
SecResponseBodyMimeType text/plain
SecRule REQUEST_HEADERS:X-Ms-P1 "@streq block" "id:1200001,phase:1,deny,status:403,log,t:none"
SecRule REQUEST_BODY "@contains envoy-phase2-marker" "id:1200002,phase:2,deny,status:403,log,t:none"
SecRule RESPONSE_HEADERS:X-Ms-P3 "@streq block" "id:1200003,phase:3,deny,status:403,log,t:none"
SecRule RESPONSE_BODY "@contains envoy-phase4-marker" "id:1200004,phase:4,deny,status:403,log,t:none"
`
	if err := os.WriteFile(rulesPath, []byte(rules), 0o600); err != nil {
		t.Fatalf("write rules: %v", err)
	}
	config := fmt.Sprintf(`enabled=on
rules_file=%s
transaction_id_header=x-request-id
request_body_mode=streaming
response_body_mode=streaming
request_body_limit=1048576
response_body_limit=1048576
body_limit_action=reject
phase4_mode=safe
default_block_status=403
default_error_status=500
use_error_log=off
max_header_count=128
max_header_name_size=256
max_header_value_size=8192
max_total_header_bytes=32768
max_event_json_bytes=16384
event_path=%s
`, rulesPath, eventPath)
	if err := os.WriteFile(configPath, []byte(config), 0o600); err != nil {
		t.Fatalf("write runtime config: %v", err)
	}
	engine, err := NewCommonRuntimeEngine(configPath)
	if err != nil {
		t.Fatalf("NewCommonRuntimeEngine() error = %v", err)
	}
	t.Cleanup(func() {
		if err := engine.Close(); err != nil {
			t.Errorf("Common runtime close: %v", err)
		}
	})
	return engine, eventPath
}

func commonTestStreamMetadata(transactionID string) StreamMetadata {
	return StreamMetadata{
		TransactionID: transactionID,
		Request: RequestMetadata{
			Method:        "POST",
			URI:           "/common-bridge-test",
			Protocol:      "HTTP/1.1",
			Hostname:      "example.test",
			ClientAddress: "127.0.0.1",
			ClientPort:    49152,
			ServerAddress: "127.0.0.1",
			ServerPort:    18080,
		},
	}
}
