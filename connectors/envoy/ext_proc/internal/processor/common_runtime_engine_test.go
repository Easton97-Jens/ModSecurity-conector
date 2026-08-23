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
	testCases := []commonRuntimeLifecycleTestCase{
		{name: "phase1_request_headers", run: testCommonRuntimePhase1},
		{name: "phase2_request_body_eos", run: testCommonRuntimePhase2},
		{name: "phase3_response_headers_before_commit", run: testCommonRuntimePhase3},
		{name: "phase4_response_body_eos", run: testCommonRuntimePhase4},
	}

	for _, testCase := range testCases {
		t.Run(testCase.name, func(t *testing.T) {
			transaction, err := engine.Open(contextValue, commonTestStreamMetadata(testCase.name))
			if err != nil {
				t.Fatalf("Open() error = %v", err)
			}
			defer transaction.Close(contextValue, Summary{CloseReason: ClosePeerEOF})
			testCase.run(t, contextValue, transaction)
		})
	}
}

func TestRequestHeadersForCommonRestoresOnlyValidatedAuthority(t *testing.T) {
	t.Run("authority becomes Host when absent", testRequestHeadersForCommonAddsValidatedHost)
	t.Run("ordinary Host wins without duplicate", testRequestHeadersForCommonRetainsOrdinaryHost)
	t.Run("missing authority is rejected", testRequestHeadersForCommonRejectsMissingAuthority)
	t.Run("control characters in authority are rejected", testRequestHeadersForCommonRejectsInjectedAuthority)
}

func testRequestHeadersForCommonAddsValidatedHost(t *testing.T) {
	headers, err := requestHeadersForCommon([]Header{
		{Name: ":method", Value: []byte("GET")},
		{Name: ":authority", Value: []byte("example.test:8443")},
		{Name: "x-request-id", Value: []byte("authority-host")},
	})
	if err != nil {
		t.Fatalf("requestHeadersForCommon() error = %v", err)
	}
	if got, want := len(headers), 4; got != want {
		t.Fatalf("header count = %d, want %d", got, want)
	}
	last := headers[len(headers)-1]
	if last.Name != "Host" || string(last.Value) != "example.test:8443" {
		t.Fatalf("injected Host = %#v, want validated authority", last)
	}
}

func testRequestHeadersForCommonRetainsOrdinaryHost(t *testing.T) {
	headers, err := requestHeadersForCommon([]Header{
		{Name: ":authority", Value: []byte("authority.example")},
		{Name: "Host", Value: []byte("header.example")},
	})
	if err != nil {
		t.Fatalf("requestHeadersForCommon() error = %v", err)
	}
	hostCount := 0
	for _, header := range headers {
		if strings.EqualFold(header.Name, "host") {
			hostCount++
			if got, want := string(header.Value), "header.example"; got != want {
				t.Fatalf("ordinary Host = %q, want %q", got, want)
			}
		}
	}
	if got, want := hostCount, 1; got != want {
		t.Fatalf("Host header count = %d, want %d", got, want)
	}
}

func testRequestHeadersForCommonRejectsMissingAuthority(t *testing.T) {
	assertRequestHeadersForCommonRejectsAuthority(t, nil)
}

func testRequestHeadersForCommonRejectsInjectedAuthority(t *testing.T) {
	assertRequestHeadersForCommonRejectsAuthority(t, []byte("example.test\r\ninjected: true"))
}

func assertRequestHeadersForCommonRejectsAuthority(t *testing.T, authority []byte) {
	t.Helper()
	if _, err := requestHeadersForCommon([]Header{{Name: ":authority", Value: authority}}); err == nil {
		t.Fatalf("requestHeadersForCommon() accepted invalid authority %q", authority)
	}
}

type commonRuntimeLifecycleTestCase struct {
	name string
	run  func(*testing.T, context.Context, Transaction)
}

func testCommonRuntimePhase1(t *testing.T, contextValue context.Context, transaction Transaction) {
	decision, err := transaction.ProcessHeaders(contextValue, DirectionRequest, []Header{{Name: "x-ms-p1", Value: []byte("block")}}, true)
	if err != nil || decision.Action != ActionDeny || decision.Status != 403 {
		t.Fatalf("phase-1 decision=%#v err=%v", decision, err)
	}
	recorder, ok := transaction.(HostActionRecorder)
	if !ok {
		t.Fatal("Common transaction does not expose host-action recording")
	}
	if err := recorder.RecordHostAction(contextValue, HostAction{Action: AppliedActionDeny, VisibleStatus: 403, TransportResult: "http_status"}); err != nil {
		t.Fatalf("RecordHostAction() error = %v", err)
	}
}

func testCommonRuntimePhase2(t *testing.T, contextValue context.Context, transaction Transaction) {
	decision, err := transaction.ProcessHeaders(contextValue, DirectionRequest, []Header{{Name: "host", Value: []byte("example.test")}}, false)
	assertCommonDecision(t, "request headers", decision, err, ActionAllow, 0)
	decision, err = transaction.ProcessBody(contextValue, DirectionRequest, []byte("envoy-phase2-marker"), true)
	assertCommonDecision(t, "phase-2", decision, err, ActionDeny, 403)
}

func testCommonRuntimePhase3(t *testing.T, contextValue context.Context, transaction Transaction) {
	decision, err := transaction.ProcessHeaders(contextValue, DirectionRequest, nil, true)
	assertCommonDecision(t, "request headers", decision, err, ActionAllow, 0)
	decision, err = transaction.ProcessHeaders(contextValue, DirectionResponse, []Header{{Name: ":status", Value: []byte("200")}, {Name: "x-ms-p3", Value: []byte("block")}}, false)
	assertCommonDecision(t, "phase-3", decision, err, ActionDeny, 403)
}

func testCommonRuntimePhase4(t *testing.T, contextValue context.Context, transaction Transaction) {
	decision, err := transaction.ProcessHeaders(contextValue, DirectionRequest, nil, true)
	assertCommonDecision(t, "request headers", decision, err, ActionAllow, 0)
	decision, err = transaction.ProcessHeaders(contextValue, DirectionResponse, []Header{{Name: ":status", Value: []byte("200")}, {Name: "content-type", Value: []byte("text/plain")}}, false)
	assertCommonDecision(t, "response headers", decision, err, ActionAllow, 0)
	committer, ok := transaction.(ResponseCommitter)
	if !ok {
		t.Fatal("Common transaction does not expose response commit bookkeeping")
	}
	if err := committer.MarkResponseCommitted(contextValue); err != nil {
		t.Fatalf("MarkResponseCommitted() error = %v", err)
	}
	decision, err = transaction.ProcessBody(contextValue, DirectionResponse, []byte("envoy-phase4-marker"), true)
	assertCommonDecision(t, "phase-4", decision, err, ActionDeny, 403)
	recorder, ok := transaction.(HostActionRecorder)
	if !ok {
		t.Fatal("Common transaction does not expose host-action recording")
	}
	if err := recorder.RecordHostAction(contextValue, HostAction{Action: AppliedActionLogOnly, VisibleStatus: 200, TransportResult: "log_only"}); err != nil {
		t.Fatalf("RecordHostAction() error = %v", err)
	}
}

func assertCommonDecision(t *testing.T, phase string, decision Decision, err error, action Action, status int) {
	t.Helper()
	if err != nil || decision.Action != action || decision.Status != status {
		t.Fatalf("%s decision=%#v err=%v", phase, decision, err)
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
		if event["message_id"] == "MSCONN_EVENT_RULE_MATCHED" {
			t.Fatal("ordinary config unexpectedly enabled DetectionOnly rule-match evidence")
		}
	}
}

func TestCommonRuntimeEngineEmitsDetectionOnlyRuleMatchEvidence(t *testing.T) {
	engine, eventPath := newDetectionOnlyRuntimeEngineForTest(t)
	ctx := context.Background()
	// The adapter-supplied host ID and ordinary x-request-id are deliberately
	// different: sealed MRTS evidence must use only x-mrts-transaction-id.
	metadata := commonTestStreamMetadata("host-id-must-not-be-used")
	metadata.Request.Method = "GET"
	metadata.Request.URI = "/?foo=attack"
	transaction, err := engine.Open(ctx, metadata)
	if err != nil {
		t.Fatalf("Open() error = %v", err)
	}
	decision, err := transaction.ProcessHeaders(ctx, DirectionRequest, []Header{
		{Name: "x-mrts-transaction-id", Value: []byte("detection-only-transaction")},
		{Name: "x-request-id", Value: []byte("must-not-be-used")},
	}, true)
	assertCommonDecision(t, "DetectionOnly request", decision, err, ActionAllow, 0)
	transaction.Close(ctx, Summary{CloseReason: CloseResponseEOS})

	events := readCommonEvents(t, eventPath)
	if len(events) != 1 {
		t.Fatalf("DetectionOnly match emitted %d events, want exactly one: %#v", len(events), events)
	}
	assertDetectionOnlyRuleMatchEvent(t, events[0])

	// A control/bypass transaction must not inherit the selected match from a
	// previous stream. This also exercises transaction-local callback state.
	controlMetadata := commonTestStreamMetadata("control-host-id-must-not-be-used")
	controlMetadata.Request.Method = "GET"
	controlMetadata.Request.URI = "/?foo=benign"
	control, err := engine.Open(ctx, controlMetadata)
	if err != nil {
		t.Fatalf("Open(control) error = %v", err)
	}
	decision, err = control.ProcessHeaders(ctx, DirectionRequest, []Header{
		{Name: "x-mrts-transaction-id", Value: []byte("detection-only-control")},
		{Name: "x-request-id", Value: []byte("must-not-be-used")},
	}, true)
	assertCommonDecision(t, "DetectionOnly control", decision, err, ActionAllow, 0)
	control.Close(ctx, Summary{CloseReason: CloseResponseEOS})
	if events := readCommonEvents(t, eventPath); len(events) != 1 {
		t.Fatalf("control/bypass emitted or inherited rule-match evidence: %#v", events)
	}

	missingHeader, err := engine.Open(ctx, commonTestStreamMetadata("host-id-must-not-fallback"))
	if err != nil {
		t.Fatalf("Open(missing-header) error = %v", err)
	}
	defer missingHeader.Close(ctx, Summary{CloseReason: ClosePeerEOF})
	if _, err := missingHeader.ProcessHeaders(ctx, DirectionRequest, []Header{
		{Name: "x-request-id", Value: []byte("must-not-fallback")},
	}, true); err == nil {
		t.Fatal("MRTS evidence mode accepted a missing x-mrts-transaction-id")
	}
}

func assertDetectionOnlyRuleMatchEvent(t *testing.T, event map[string]any) {
	t.Helper()
	for field, want := range map[string]string{
		"event":            "request_rule_match",
		"message_id":       "MSCONN_EVENT_RULE_MATCHED",
		"connector":        "envoy",
		"integration_mode": "ext_proc",
		"transaction_id":   "detection-only-transaction",
		"rule_id":          "1200010",
		"status":           "ok",
		"action":           "allow",
		"requested_action": "allow",
		"actual_action":    "allow",
		"uri":              "/?foo=attack",
	} {
		if event[field] != want {
			t.Errorf("DetectionOnly event[%q] = %#v, want %q", field, event[field], want)
		}
	}
	if phase, ok := event["phase"].(string); !ok || phase != "request_body" {
		t.Errorf("DetectionOnly event phase = %#v, want request_body", event["phase"])
	}
	for _, field := range []string{"message", "reason", "client_ip", "content_type"} {
		if value, ok := event[field].(string); !ok || value != "" {
			t.Errorf("DetectionOnly event[%q] = %#v, want empty string", field, event[field])
		}
	}
	for _, field := range []string{"run_id", "transport_case_id"} {
		if _, present := event[field]; present {
			t.Errorf("DetectionOnly event unexpectedly contains %q", field)
		}
	}
	for _, field := range []string{"body_bytes_seen", "body_bytes_inspected"} {
		if value, ok := event[field].(float64); !ok || value != 0 {
			t.Errorf("DetectionOnly event[%q] = %#v, want zero", field, event[field])
		}
	}
	for _, forbidden := range []string{
		"rule_message", "message_data", "matched_data", "request_headers", "request_body", "response_body",
	} {
		if _, present := event[forbidden]; present {
			t.Errorf("DetectionOnly event contains payload-bearing field %q", forbidden)
		}
	}
}

func TestCommonRuntimeEngineRejectsRuleMatchEvidenceWithoutEventPath(t *testing.T) {
	directory := t.TempDir()
	rulesPath := filepath.Join(directory, "rules.conf")
	configPath := filepath.Join(directory, "runtime.conf")
	if err := os.WriteFile(rulesPath, []byte("SecRuleEngine DetectionOnly\n"), 0o600); err != nil {
		t.Fatalf("write rules: %v", err)
	}
	config := fmt.Sprintf(`enabled=on
rules_file=%s
transaction_id_header=x-mrts-transaction-id
emit_rule_match_evidence=on
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
`, rulesPath)
	if err := os.WriteFile(configPath, []byte(config), 0o600); err != nil {
		t.Fatalf("write config: %v", err)
	}
	if _, err := NewCommonRuntimeEngine(configPath); err == nil {
		t.Fatal("rule-match evidence without event_path was accepted")
	}
}

func TestCommonRuntimeEngineRejectsSymlinkRuleMatchEventPath(t *testing.T) {
	directory := t.TempDir()
	rulesPath := filepath.Join(directory, "rules.conf")
	configPath := filepath.Join(directory, "runtime.conf")
	realEventPath := filepath.Join(directory, "real-events.jsonl")
	eventPath := filepath.Join(directory, "events.jsonl")
	if err := os.WriteFile(rulesPath, []byte("SecRuleEngine DetectionOnly\n"), 0o600); err != nil {
		t.Fatalf("write rules: %v", err)
	}
	if err := os.WriteFile(realEventPath, nil, 0o600); err != nil {
		t.Fatalf("write real event path: %v", err)
	}
	if err := os.Symlink(realEventPath, eventPath); err != nil {
		t.Fatalf("create event-path symlink: %v", err)
	}
	config := fmt.Sprintf(`enabled=on
rules_file=%s
transaction_id_header=x-mrts-transaction-id
emit_rule_match_evidence=on
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
		t.Fatalf("write config: %v", err)
	}
	if _, err := NewCommonRuntimeEngine(configPath); err == nil {
		t.Fatal("rule-match evidence accepted a symlink event path")
	}
}

func TestCommonRuntimeEngineRejectsSymlinkedRuleMatchEventParent(t *testing.T) {
	directory := t.TempDir()
	externalDirectory := t.TempDir()
	rulesPath := filepath.Join(directory, "rules.conf")
	configPath := filepath.Join(directory, "runtime.conf")
	symlinkedParent := filepath.Join(directory, "linked-events")
	eventPath := filepath.Join(symlinkedParent, "events.jsonl")
	externalEventPath := filepath.Join(externalDirectory, "events.jsonl")
	if err := os.WriteFile(rulesPath, []byte("SecRuleEngine DetectionOnly\n"), 0o600); err != nil {
		t.Fatalf("write rules: %v", err)
	}
	if err := os.Symlink(externalDirectory, symlinkedParent); err != nil {
		t.Fatalf("create event-parent symlink: %v", err)
	}
	config := fmt.Sprintf(`enabled=on
rules_file=%s
transaction_id_header=x-mrts-transaction-id
emit_rule_match_evidence=on
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
		t.Fatalf("write config: %v", err)
	}
	if _, err := NewCommonRuntimeEngine(configPath); err == nil {
		t.Fatal("rule-match evidence accepted a symlinked event parent")
	}
	if _, err := os.Lstat(externalEventPath); !os.IsNotExist(err) {
		t.Fatalf("symlinked evidence parent received an event file: %v", err)
	}
}

func readCommonEvents(t *testing.T, path string) []map[string]any {
	t.Helper()
	raw, err := os.ReadFile(path)
	if err != nil {
		t.Fatalf("ReadFile(%s): %v", path, err)
	}
	var events []map[string]any
	for _, line := range strings.Split(strings.TrimSpace(string(raw)), "\n") {
		if line == "" {
			continue
		}
		var event map[string]any
		if err := json.Unmarshal([]byte(line), &event); err != nil {
			t.Fatalf("unmarshal Common event: %v", err)
		}
		events = append(events, event)
	}
	return events
}

func newDetectionOnlyRuntimeEngineForTest(t *testing.T) (*CommonRuntimeEngine, string) {
	t.Helper()
	directory := t.TempDir()
	rulesPath := filepath.Join(directory, "rules.conf")
	configPath := filepath.Join(directory, "runtime.conf")
	eventPath := filepath.Join(directory, "events.jsonl")
	rules := `SecRuleEngine DetectionOnly
SecRequestBodyAccess On
SecRule ARGS:foo "@streq attack" "id:1200010,phase:1,pass,log,t:none"
`
	if err := os.WriteFile(rulesPath, []byte(rules), 0o600); err != nil {
		t.Fatalf("write DetectionOnly rules: %v", err)
	}
	config := fmt.Sprintf(`enabled=on
rules_file=%s
transaction_id_header=x-mrts-transaction-id
emit_rule_match_evidence=on
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
		t.Fatalf("write DetectionOnly config: %v", err)
	}
	engine, err := NewCommonRuntimeEngine(configPath)
	if err != nil {
		t.Fatalf("NewCommonRuntimeEngine(DetectionOnly): %v", err)
	}
	t.Cleanup(func() {
		if err := engine.Close(); err != nil {
			t.Errorf("DetectionOnly Common runtime close: %v", err)
		}
	})
	return engine, eventPath
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
