//go:build libmodsecurity

package composite

import (
	"context"
	"encoding/json"
	"github.com/Easton97-Jens/ModSecurity-conector/connectors/envoy/ext_proc/internal/processor"
	"os"
	"path/filepath"
	"strings"
	"testing"
)

func TestI12PrivateEnvoyClaimUsesActualRetainedNativeScope(t *testing.T) {
	root := t.TempDir()
	trace := filepath.Join(root, "physical.jsonl")
	if err := os.WriteFile(trace, nil, 0600); err != nil {
		t.Fatal(err)
	}
	t.Setenv("I12_ENVOY_HOST_TRACE_PATH", trace)
	rules := filepath.Join(root, "native.rules")
	if err := os.WriteFile(rules, []byte("SecRuleEngine On\nSecRequestBodyAccess On\nSecResponseBodyAccess On\nSecResponseBodyMimeType text/plain\n"), 0600); err != nil {
		t.Fatal(err)
	}
	config := filepath.Join(root, "native.conf")
	if err := os.WriteFile(config, []byte("enabled=on\nrequest_body_mode=streaming\nresponse_body_mode=streaming\nphase4_mode=safe\nrules_file="+rules+"\n"), 0600); err != nil {
		t.Fatal(err)
	}
	engine, err := processor.NewCommonRuntimeEngine(config)
	if err != nil {
		t.Fatal(err)
	}
	coordinator, err := New("envoy", make([]byte, 32), Limits{Capacity: 2}, engine, nil)
	if err != nil {
		t.Fatal(err)
	}
	defer func() {
		coordinator.Close()
		if err := engine.Close(context.Background()); err != nil {
			t.Error(err)
		}
	}()
	ctx := context.Background()
	meta := processor.StreamMetadata{Request: processor.RequestMetadata{Method: "POST", URI: "/claim-control", Protocol: "HTTP/1.1", Hostname: "example.test", ClientAddress: "127.0.0.1", ClientPort: 12345, ServerAddress: "127.0.0.1", ServerPort: 443}}
	admission, decision, err := coordinator.BeginRequest(ctx, meta, []processor.Header{{Name: "host", Value: []byte("example.test")}}, false)
	if err != nil || decision.Action != processor.ActionAllow {
		t.Fatalf("begin %v %v", decision, err)
	}
	decision, err = admission.ProcessBody(ctx, []byte("abc"), true)
	if err != nil || decision.Action != processor.ActionAllow {
		t.Fatalf("body %v %v", decision, err)
	}
	token, err := admission.Lease()
	if err != nil {
		t.Fatal(err)
	}
	if _, err = coordinator.Claim("invalid", "private-session"); err == nil {
		t.Fatal("invalid claim accepted")
	}
	before, _ := os.ReadFile(trace)
	response, err := coordinator.Claim(token, "private-session")
	if err != nil {
		t.Fatal(err)
	}
	after, _ := os.ReadFile(trace)
	var rows []map[string]interface{}
	for _, line := range strings.Split(strings.TrimSpace(string(after[len(before):])), "\n") {
		var row map[string]interface{}
		if err := json.Unmarshal([]byte(line), &row); err != nil {
			t.Fatal(err)
		}
		rows = append(rows, row)
	}
	if len(rows) != 1 || rows[0]["operation"] != float64(12) || rows[0]["companion_claim_succeeded"] != true || rows[0]["allocation_scope_call"].(float64) <= 0 || rows[0]["body_end_of_stream_argument"] != nil {
		t.Fatalf("claim receipt %v", rows)
	}
	decision, err = response.Headers(ctx, []processor.Header{{Name: ":status", Value: []byte("200")}, {Name: "content-type", Value: []byte("text/plain")}}, false)
	if err != nil || decision.Action != processor.ActionAllow {
		t.Fatalf("response headers %v %v", decision, err)
	}
	if err := response.MarkResponseCommitted(ctx); err != nil {
		t.Fatal(err)
	}
	decision, err = response.Body(ctx, []byte("xyz"), true)
	if err != nil || decision.Action != processor.ActionAllow {
		t.Fatalf("response body %v %v", decision, err)
	}
	if err := response.RecordNeutralOutcome(ctx, 200, "response_allow"); err != nil {
		t.Fatal(err)
	}
	response.Finish(ctx, "response_allow")
}
