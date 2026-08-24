//go:build libmodsecurity

package processor

import (
	"context"
	"encoding/json"
	"errors"
	"fmt"
	"os"
	"path/filepath"
	"strings"
	"sync"
	"testing"
	"time"
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

func TestCommonRuntimeEngineRejectsStrictPolicyBeforeStreamAdmission(t *testing.T) {
	engine, _ := newCommonRuntimeEngineForTest(t)
	_, err := NewService(testConfig(LateActionStrict), engine)
	if err == nil || !strings.Contains(err.Error(), "phase4_mode=safe") {
		t.Fatalf("NewService() error = %v, want strict/safe admission rejection", err)
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
	if decision.RuleID != "1200001" {
		t.Fatalf("phase-1 rule ID=%q, want 1200001", decision.RuleID)
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
	if decision.RuleID != "1200002" {
		t.Fatalf("phase-2 rule ID=%q, want 1200002", decision.RuleID)
	}
}

func testCommonRuntimePhase3(t *testing.T, contextValue context.Context, transaction Transaction) {
	decision, err := transaction.ProcessHeaders(contextValue, DirectionRequest, nil, true)
	assertCommonDecision(t, "request headers", decision, err, ActionAllow, 0)
	decision, err = transaction.ProcessHeaders(contextValue, DirectionResponse, []Header{{Name: ":status", Value: []byte("200")}, {Name: "x-ms-p3", Value: []byte("block")}}, false)
	assertCommonDecision(t, "phase-3", decision, err, ActionDeny, 403)
	if decision.RuleID != "1200003" {
		t.Fatalf("phase-3 rule ID=%q, want 1200003", decision.RuleID)
	}
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
	if decision.RuleID != "1200004" {
		t.Fatalf("phase-4 rule ID=%q, want 1200004", decision.RuleID)
	}
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

func TestCommonRuntimeEngineCloseHonorsShutdownContext(t *testing.T) {
	engine := &CommonRuntimeEngine{transactions: make(map[*commonRuntimeTransaction]struct{})}
	engine.mu.Lock()
	ctx, cancel := context.WithTimeout(context.Background(), 20*time.Millisecond)
	defer cancel()

	started := time.Now()
	err := engine.Close(ctx)
	elapsed := time.Since(started)
	engine.mu.Unlock()

	if !errors.Is(err, ErrCommonRuntimeShutdownTimeout) {
		t.Fatalf("Close() error = %v, want ErrCommonRuntimeShutdownTimeout", err)
	}
	if elapsed > 500*time.Millisecond {
		t.Fatalf("Close() blocked for %s", elapsed)
	}
}

func TestCommonRuntimeTransactionCleanupHonorsContext(t *testing.T) {
	engine := &CommonRuntimeEngine{transactions: make(map[*commonRuntimeTransaction]struct{})}
	transaction := &commonRuntimeTransaction{engine: engine}
	engine.transactions[transaction] = struct{}{}
	engine.mu.Lock()
	ctx, cancel := context.WithTimeout(context.Background(), 20*time.Millisecond)
	defer cancel()
	started := time.Now()
	transaction.Close(ctx, Summary{CloseReason: CloseContextCanceled})
	elapsed := time.Since(started)
	engine.mu.Unlock()

	if elapsed > 500*time.Millisecond {
		t.Fatalf("transaction Close() blocked for %s", elapsed)
	}
	if err := transaction.CleanupFailure(); !errors.Is(err, context.DeadlineExceeded) {
		t.Fatalf("CleanupFailure() = %v, want context deadline", err)
	}
	if transaction.closed {
		t.Fatal("transaction marked closed after bounded mutex cleanup failure")
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

func TestCommonRuntimeEngineClassifiesModSecurityBodyLimitWithoutRuleID(t *testing.T) {
	const body = "envoy-body-limit-payload-must-not-be-an-event-field"
	engine, eventPath := newCommonRuntimeEngineForRulesTest(t, `SecRuleEngine On
SecRequestBodyAccess On
SecRequestBodyLimit 32
SecRequestBodyLimitAction Reject
`)
	contextValue := context.Background()
	transaction, err := engine.Open(contextValue, commonTestStreamMetadata("body-limit-without-rule-id"))
	if err != nil {
		t.Fatalf("Open() error = %v", err)
	}
	defer transaction.Close(contextValue, Summary{CloseReason: CloseImmediateResponse})

	decision, err := transaction.ProcessHeaders(contextValue, DirectionRequest,
		[]Header{{Name: "host", Value: []byte("example.test")}}, false)
	assertCommonDecision(t, "request headers", decision, err, ActionAllow, 0)
	decision, err = transaction.ProcessBody(contextValue, DirectionRequest, []byte(body), true)
	assertCommonDecision(t, "body limit", decision, err, ActionDeny, 413)
	if decision.RuleID != "" {
		t.Fatalf("body-limit rule ID=%q, want empty", decision.RuleID)
	}
	recorder, ok := transaction.(HostActionRecorder)
	if !ok {
		t.Fatal("Common transaction does not expose host-action recording")
	}
	if err := recorder.RecordHostAction(contextValue, HostAction{
		Action: AppliedActionRedirect, VisibleStatus: 302, TransportResult: "http_status",
	}); err == nil {
		t.Fatal("RecordHostAction() accepted a non-413 body-limit action")
	}
	if err := recorder.RecordHostAction(contextValue, HostAction{
		Action: AppliedActionDeny, VisibleStatus: 413, TransportResult: "http_status",
	}); err != nil {
		t.Fatalf("RecordHostAction() error = %v", err)
	}

	raw, err := os.ReadFile(eventPath)
	if err != nil {
		t.Fatalf("ReadFile(%s): %v", eventPath, err)
	}
	if strings.Contains(string(raw), body) {
		t.Fatal("event JSONL retained a request-body payload")
	}
	foundBodyLimit := false
	for _, line := range strings.Split(strings.TrimSpace(string(raw)), "\n") {
		if line == "" {
			continue
		}
		var event map[string]any
		if err := json.Unmarshal([]byte(line), &event); err != nil {
			t.Fatalf("unmarshal Common event: %v", err)
		}
		if event["message_id"] != "MSCONN_EVENT_BODY_LIMIT" {
			continue
		}
		foundBodyLimit = true
		if status, ok := event["http_status"].(float64); !ok || int(status) != 413 {
			t.Fatalf("body-limit event status=%#v, want 413", event["http_status"])
		}
		if ruleID, present := event["rule_id"]; present && ruleID != nil && ruleID != "" {
			t.Fatalf("body-limit event rule ID=%#v, want absent or empty", ruleID)
		}
	}
	if !foundBodyLimit {
		t.Fatal("body-limit event was not emitted")
	}
}

func TestCommonRuntimeEngineMapsP3RedirectLocation(t *testing.T) {
	const redirectTarget = "/msconnector-p3-redirect-target"
	engine, _ := newCommonRuntimeEngineForRulesTest(t, `SecRuleEngine On
SecRequestBodyAccess On
SecResponseBodyAccess On
SecRule RESPONSE_HEADERS:X-Msconnector-Vector "@streq msconnector-p3-redirect" "id:1203002,phase:3,redirect:/msconnector-p3-redirect-target,status:302,log,t:none"
`)
	contextValue := context.Background()
	transaction, err := engine.Open(contextValue, commonTestStreamMetadata("p3-redirect-location"))
	if err != nil {
		t.Fatalf("Open() error = %v", err)
	}
	defer transaction.Close(contextValue, Summary{CloseReason: CloseImmediateResponse})

	decision, err := transaction.ProcessHeaders(contextValue, DirectionRequest, nil, true)
	assertCommonDecision(t, "request headers", decision, err, ActionAllow, 0)
	decision, err = transaction.ProcessHeaders(contextValue, DirectionResponse, []Header{
		{Name: ":status", Value: []byte("200")},
		{Name: "x-msconnector-vector", Value: []byte("msconnector-p3-redirect")},
	}, false)
	if err != nil || decision.Action != ActionRedirect || decision.Status != 302 || decision.RedirectURL != redirectTarget {
		t.Fatalf("phase-3 redirect decision=%#v err=%v", decision, err)
	}
	recorder, ok := transaction.(HostActionRecorder)
	if !ok {
		t.Fatal("Common transaction does not expose host-action recording")
	}
	if err := recorder.RecordHostAction(contextValue, HostAction{
		Action: AppliedActionRedirect, VisibleStatus: 302, TransportResult: "http_status",
	}); err != nil {
		t.Fatalf("RecordHostAction() error = %v", err)
	}
}

func newCommonRuntimeEngineForTest(t *testing.T) (*CommonRuntimeEngine, string) {
	return newCommonRuntimeEngineForRulesTest(t, `SecRuleEngine On
SecRequestBodyAccess On
SecResponseBodyAccess On
SecResponseBodyMimeType text/plain
SecRule REQUEST_HEADERS:X-Ms-P1 "@streq block" "id:1200001,phase:1,deny,status:403,log,t:none"
SecRule REQUEST_BODY "@contains envoy-phase2-marker" "id:1200002,phase:2,deny,status:403,log,t:none"
SecRule RESPONSE_HEADERS:X-Ms-P3 "@streq block" "id:1200003,phase:3,deny,status:403,log,t:none"
SecRule RESPONSE_BODY "@contains envoy-phase4-marker" "id:1200004,phase:4,deny,status:403,log,t:none"
`)
}

func newCommonRuntimeEngineForRulesTest(t *testing.T, rules string) (*CommonRuntimeEngine, string) {
	t.Helper()
	directory := t.TempDir()
	rulesPath := filepath.Join(directory, "rules.conf")
	configPath := filepath.Join(directory, "runtime.conf")
	eventPath := filepath.Join(directory, "events.jsonl")
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
		if err := engine.Close(context.Background()); err != nil {
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
