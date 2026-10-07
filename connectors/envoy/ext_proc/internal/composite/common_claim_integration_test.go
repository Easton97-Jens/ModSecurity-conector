//go:build libmodsecurity

package composite

import (
	"context"
	"fmt"
	"os"
	"path/filepath"
	"testing"
	"time"

	"github.com/Easton97-Jens/ModSecurity-conector/connectors/envoy/ext_proc/internal/processor"
)

func nativeCompositeCoordinator(t *testing.T, mode processor.CompositeMode, bodyLimit int) (*Coordinator, *processor.CommonRuntimeEngine) {
	t.Helper()
	directory := t.TempDir()
	rulesPath := filepath.Join(directory, "rules.conf")
	configPath := filepath.Join(directory, "runtime.conf")
	if err := os.WriteFile(rulesPath, []byte("SecRuleEngine On\nSecRequestBodyAccess On\nSecResponseBodyAccess On\n"), 0o600); err != nil {
		t.Fatal(err)
	}
	config := fmt.Sprintf("enabled=on\nrules_file=%s\nrequest_body_mode=buffered\nresponse_body_mode=streaming\nphase4_mode=safe\nrequest_body_limit=%d\nevent_path=%s\nuse_error_log=off\n", rulesPath, bodyLimit, filepath.Join(directory, "events.jsonl"))
	if err := os.WriteFile(configPath, []byte(config), 0o600); err != nil {
		t.Fatal(err)
	}
	engine, err := processor.NewCompositeRuntimeEngine(configPath, mode)
	if err != nil {
		t.Fatal(err)
	}
	connector := "envoy"
	if mode == processor.CompositeModeTraefik {
		connector = "traefik"
	}
	c, err := New(connector, []byte("01234567890123456789012345678901"), Limits{TTL: time.Minute, IdleTTL: time.Minute, MaxRequestBody: 1024}, engine, &eventLog{})
	if err != nil {
		_ = engine.Close(context.Background())
		t.Fatal(err)
	}
	t.Cleanup(func() {
		c.Close()
		if err := engine.Close(context.Background()); err != nil {
			t.Error(err)
		}
	})
	return c, engine
}

func nativeAdmission(t *testing.T, c *Coordinator, body []byte) (*Admission, processor.Decision) {
	t.Helper()
	metadata := reservationMetadata("POST", "/")
	metadata.Request.ClientAddress, metadata.Request.ClientPort = "127.0.0.1", 49152
	a, decision, err := c.BeginRequest(context.Background(), metadata, nil, false)
	if err != nil || decision.Action != processor.ActionAllow {
		t.Fatalf("P1: %v/%v", decision, err)
	}
	decision, err = a.ProcessBody(context.Background(), body, true)
	if err != nil {
		t.Fatal(err)
	}
	return a, decision
}

func completeNativeResponse(t *testing.T, a *Admission) {
	t.Helper()
	token, err := a.Lease()
	if err != nil {
		t.Fatal(err)
	}
	r, err := a.e.c.ClaimContext(context.Background(), token, "trusted-response")
	if err != nil {
		t.Fatal(err)
	}
	decision, err := r.Headers(context.Background(), []processor.Header{{Name: ":status", Value: []byte("200")}}, true)
	if err != nil || decision.Action != processor.ActionAllow {
		t.Fatalf("P3/P4: %v/%v", decision, err)
	}
	r.Finish(context.Background(), "response_eos")
	if err := a.e.tx.(processor.CleanupFailureReporter).CleanupFailure(); err != nil {
		t.Fatal(err)
	}
}

func TestNativeCoordinatorClaimExtendsCompanionBeforeSlowUpstream(t *testing.T) {
	for _, mode := range []processor.CompositeMode{processor.CompositeModeEnvoy, processor.CompositeModeTraefik} {
		t.Run(fmt.Sprint(mode), func(t *testing.T) {
			c, _ := nativeCompositeCoordinator(t, mode, 1024)
			a, decision := nativeAdmission(t, c, []byte("allow"))
			if decision.Action != processor.ActionAllow {
				t.Fatal(decision)
			}
			token, err := a.Lease()
			if err != nil {
				t.Fatal(err)
			}
			r, err := c.ClaimContext(context.Background(), token, "trusted-response")
			if err != nil {
				t.Fatal(err)
			}
			// Native must now have the claimed 30s lifetime, not the 5s
			// preclaim cap, while a real upstream has not delivered P3 yet.
			time.Sleep(5100 * time.Millisecond)
			decision, err = r.Headers(context.Background(), []processor.Header{{Name: ":status", Value: []byte("200")}}, true)
			if err != nil || decision.Action != processor.ActionAllow {
				t.Fatalf("slow upstream P3/P4: %v/%v", decision, err)
			}
			r.Finish(context.Background(), "response_eos")
			if err := a.e.tx.(processor.CleanupFailureReporter).CleanupFailure(); err != nil {
				t.Fatal(err)
			}
			fresh, decision := nativeAdmission(t, c, []byte("allow"))
			if decision.Action != processor.ActionAllow {
				t.Fatal(decision)
			}
			completeNativeResponse(t, fresh)
		})
	}
}

func TestNativeCoordinatorBodyLimitBelowHostLimitKeepsEngineUsable(t *testing.T) {
	for _, mode := range []processor.CompositeMode{processor.CompositeModeEnvoy, processor.CompositeModeTraefik} {
		t.Run(fmt.Sprint(mode), func(t *testing.T) {
			c, _ := nativeCompositeCoordinator(t, mode, 2) // host budget remains 1024
			a, decision := nativeAdmission(t, c, []byte("too-large"))
			if decision.Action != processor.ActionDeny || decision.Status != 413 || decision.RuleID != "" {
				t.Fatalf("typed Common limit: %v", decision)
			}
			if err := a.RecordHostAction(context.Background(), processor.HostAction{Action: processor.AppliedActionDeny, VisibleStatus: 413, TransportResult: "http_status"}); err != nil {
				t.Fatal(err)
			}
			a.Finish(context.Background(), "request_block")
			if err := a.e.tx.(processor.CleanupFailureReporter).CleanupFailure(); err != nil {
				t.Fatal(err)
			}
			fresh, decision := nativeAdmission(t, c, []byte("ok"))
			if decision.Action != processor.ActionAllow {
				t.Fatal(decision)
			}
			completeNativeResponse(t, fresh)
		})
	}
}
