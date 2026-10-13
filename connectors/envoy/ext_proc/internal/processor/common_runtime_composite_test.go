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
	"sync/atomic"
	"testing"
	"time"
)

func TestCompositeRuntimeEngineUsesReviewedRouteIdentity(t *testing.T) {
	for _, tc := range []struct {
		name        string
		mode        CompositeMode
		integration string
		profileID   uint
	}{
		// IDs are the canonical registry enum, not the selector enum.
		{name: "envoy", mode: CompositeModeEnvoy, integration: "ext_authz", profileID: 5},
		{name: "traefik", mode: CompositeModeTraefik, integration: "forwardAuth", profileID: 7},
	} {
		t.Run(tc.name, func(t *testing.T) {
			configPath, eventPath := compositeRuntimeConfigForTest(t, "buffered", "streaming")
			engine, err := NewCompositeRuntimeEngine(configPath, tc.mode)
			if err != nil {
				t.Fatalf("NewCompositeRuntimeEngine(%s) error = %v, want nil", tc.name, err)
			}
			if got := engine.transactionProfileID(); got != tc.profileID {
				t.Errorf("composite installed profile ID = %d, want %d", got, tc.profileID)
			}
			t.Cleanup(func() {
				if err := engine.Close(context.Background()); err != nil {
					t.Errorf("Close(%s) error = %v, want nil", tc.name, err)
				}
			})
			transaction, err := engine.Open(context.Background(), commonTestStreamMetadata(tc.name+"-companion"))
			if err != nil {
				t.Fatal(err)
			}
			defer transaction.Close(context.Background(), Summary{CloseReason: CloseImmediateResponse})
			decision, err := transaction.ProcessHeaders(context.Background(), DirectionRequest, nil, false)
			assertCommonDecision(t, "composite request headers", decision, err, ActionAllow, 0)
			decision, err = transaction.ProcessBody(context.Background(), DirectionRequest, []byte("bounded-allow"), true)
			assertCommonDecision(t, "composite buffered P2", decision, err, ActionAllow, 0)
			decision, err = transaction.ProcessHeaders(context.Background(), DirectionResponse, []Header{
				{Name: ":status", Value: []byte("200")},
				{Name: "x-ms-p3", Value: []byte("block")},
			}, false)
			assertCommonDecision(t, "composite P3 companion", decision, err, ActionDeny, 403)
			if decision.RuleID != "1200003" {
				t.Fatalf("composite P3 RuleID = %q, want 1200003", decision.RuleID)
			}
			recorder, ok := transaction.(HostActionRecorder)
			if !ok {
				t.Fatal("composite transaction has no host-action recorder")
			}
			if err := recorder.RecordHostAction(context.Background(), HostAction{
				Action: AppliedActionDeny, VisibleStatus: 403, TransportResult: "http_status",
			}); err != nil {
				t.Fatal(err)
			}
			transaction.Close(context.Background(), Summary{CloseReason: CloseImmediateResponse})
			raw, err := os.ReadFile(eventPath)
			if err != nil {
				t.Fatal(err)
			}
			if strings.TrimSpace(string(raw)) == "" {
				t.Fatal("composite lifecycle emitted no observable events")
			}
			for _, line := range strings.Split(strings.TrimSpace(string(raw)), "\n") {
				var event map[string]any
				if err := json.Unmarshal([]byte(line), &event); err != nil {
					t.Fatal(err)
				}
				if event["connector"] != tc.name || event["integration_mode"] != tc.integration {
					t.Errorf("composite event identity = %v/%v, want %s/%s", event["connector"], event["integration_mode"], tc.name, tc.integration)
				}
			}
		})
	}
}

func TestCompositeRuntimeEngineRejectsUnreviewedInputs(t *testing.T) {
	for _, mode := range []CompositeMode{0, -1, 99} {
		if engine, err := NewCompositeRuntimeEngine("/not-opened.conf", mode); err == nil || engine != nil {
			t.Errorf("NewCompositeRuntimeEngine(invalid %d) = %v/%v, want nil/error", mode, engine, err)
		}
	}
	for _, mode := range []CompositeMode{CompositeModeEnvoy, CompositeModeTraefik} {
		for _, bodyModes := range [][2]string{
			{"streaming", "streaming"}, {"none", "streaming"},
			{"buffered", "buffered"}, {"buffered", "none"},
		} {
			t.Run(fmt.Sprintf("%d-%s-%s", mode, bodyModes[0], bodyModes[1]), func(t *testing.T) {
				configPath, _ := compositeRuntimeConfigForTest(t, bodyModes[0], bodyModes[1])
				engine, err := NewCompositeRuntimeEngine(configPath, mode)
				if engine != nil {
					_ = engine.Close(context.Background())
				}
				if err == nil || engine != nil {
					t.Errorf("NewCompositeRuntimeEngine(%d,%v) = %v/%v, want nil/error", mode, bodyModes, engine, err)
				}
			})
		}
	}
}

func TestCommonRuntimeRequestBodyLimitKeepsEngineUsable(t *testing.T) {
	for _, mode := range []CompositeMode{0, CompositeModeEnvoy, CompositeModeTraefik} {
		t.Run(fmt.Sprintf("route-%d", mode), func(t *testing.T) {
			requestMode := "buffered"
			if mode == 0 {
				requestMode = "streaming"
			}
			configPath, eventPath := compositeRuntimeConfigForTest(t, requestMode, "streaming")
			config, err := os.ReadFile(configPath)
			if err != nil {
				t.Fatal(err)
			}
			if err := os.WriteFile(configPath, append(config, []byte("request_body_limit=2\n")...), 0o600); err != nil {
				t.Fatal(err)
			}
			var engine *CommonRuntimeEngine
			if mode == 0 {
				engine, err = NewCommonRuntimeEngine(configPath)
			} else {
				engine, err = NewCompositeRuntimeEngine(configPath, mode)
			}
			if err != nil {
				t.Fatal(err)
			}
			t.Cleanup(func() {
				if err := engine.Close(context.Background()); err != nil {
					t.Error(err)
				}
			})
			tx, err := engine.Open(context.Background(), commonTestStreamMetadata("native-body-limit"))
			if err != nil {
				t.Fatal(err)
			}
			defer tx.Close(context.Background(), Summary{CloseReason: CloseContextCanceled})
			decision, err := tx.ProcessHeaders(context.Background(), DirectionRequest, nil, false)
			assertCommonDecision(t, "P1", decision, err, ActionAllow, 0)
			decision, err = tx.ProcessBody(context.Background(), DirectionRequest, []byte("over-limit"), true)
			assertCommonDecision(t, "native body limit", decision, err, ActionDeny, 413)
			if decision.RuleID != "" {
				t.Fatalf("native host limit invented RuleID: %q", decision.RuleID)
			}
			if err := tx.(HostActionRecorder).RecordHostAction(context.Background(), HostAction{Action: AppliedActionDeny, VisibleStatus: 413, TransportResult: "http_status"}); err != nil {
				t.Fatal(err)
			}
			tx.Close(context.Background(), Summary{CloseReason: CloseImmediateResponse})
			if err := tx.(*commonRuntimeTransaction).CleanupFailure(); err != nil {
				t.Fatal(err)
			}
			raw, err := os.ReadFile(eventPath)
			if err != nil || !strings.Contains(string(raw), "body_limit") || !strings.Contains(string(raw), "413") {
				t.Fatalf("missing bounded body-limit/host event: %s/%v", raw, err)
			}
			fresh, err := engine.Open(context.Background(), commonTestStreamMetadata("fresh-after-native-limit"))
			if err != nil {
				t.Fatal(err)
			}
			defer fresh.Close(context.Background(), Summary{CloseReason: CloseContextCanceled})
			decision, err = fresh.ProcessHeaders(context.Background(), DirectionRequest, nil, true)
			assertCommonDecision(t, "fresh request", decision, err, ActionAllow, 0)
			decision, err = fresh.ProcessHeaders(context.Background(), DirectionResponse, []Header{{Name: ":status", Value: []byte("200")}}, true)
			assertCommonDecision(t, "fresh response", decision, err, ActionAllow, 0)
			fresh.Close(context.Background(), Summary{CloseReason: CloseResponseEOS})
			if err := fresh.(*commonRuntimeTransaction).CleanupFailure(); err != nil {
				t.Fatal(err)
			}
		})
	}
}

func TestCompositeRuntimeConcurrentCloseDoesNotRequiesceFreedRegistry(t *testing.T) {
	configPath, _ := compositeRuntimeConfigForTest(t, "buffered", "streaming")
	engine, err := NewCompositeRuntimeEngine(configPath, CompositeModeEnvoy)
	if err != nil {
		t.Fatal(err)
	}
	started, release := make(chan struct{}), make(chan struct{})
	original := engine.destructor
	var calls atomic.Int32
	engine.destructor = func() { calls.Add(1); original(); close(started); <-release }
	first := make(chan error, 1)
	go func() { first <- engine.Close(context.Background()) }()
	select {
	case <-started:
	case <-time.After(time.Second):
		t.Fatal("native destructor did not run")
	}
	ctx, cancel := context.WithTimeout(context.Background(), 20*time.Millisecond)
	err = engine.Close(ctx)
	cancel()
	close(release)
	if !errors.Is(err, ErrCommonRuntimeShutdownTimeout) {
		t.Fatalf("second Close = %v", err)
	}
	if err := <-first; err != nil {
		t.Fatal(err)
	}
	if err := engine.Close(context.Background()); err != nil {
		t.Fatal(err)
	}
	if calls.Load() != 1 {
		t.Fatalf("destructor calls = %d", calls.Load())
	}
}

func TestCompositeRuntimeEngineRecoversAfterPreclaimExpiry(t *testing.T) {
	for _, mode := range []CompositeMode{CompositeModeEnvoy, CompositeModeTraefik} {
		for _, claimBeforeClose := range []bool{false, true} {
			t.Run(fmt.Sprintf("%d/claim-%t", mode, claimBeforeClose), func(t *testing.T) {
				engine, eventPath := newBufferedCompositeRuntimeEngineForTest(t, mode)
				tx, err := engine.Open(context.Background(), commonTestStreamMetadata("expired-companion"))
				if err != nil {
					t.Fatal(err)
				}
				defer tx.Close(context.Background(), Summary{CloseReason: CloseContextCanceled})
				decision, err := tx.ProcessHeaders(context.Background(), DirectionRequest, nil, false)
				assertCommonDecision(t, "P1", decision, err, ActionAllow, 0)
				decision, err = tx.ProcessBody(context.Background(), DirectionRequest, []byte("allow"), true)
				assertCommonDecision(t, "P2 handoff", decision, err, ActionAllow, 0)
				// Common caps an unclaimed handoff at 5000 ms independently of
				// the route's 30000-ms claimed lifetime. Exercise real expiry.
				time.Sleep(5100 * time.Millisecond)
				if claimBeforeClose {
					if _, err := tx.ProcessHeaders(context.Background(), DirectionResponse, []Header{{Name: ":status", Value: []byte("200")}}, true); err == nil {
						t.Fatal("expired companion unexpectedly accepted P3")
					}
				}
				tx.Close(context.Background(), Summary{CloseReason: CloseContextCanceled})
				if err := tx.(*commonRuntimeTransaction).CleanupFailure(); err != nil {
					t.Fatal(err)
				}
				raw, err := os.ReadFile(eventPath)
				if err != nil || len(strings.TrimSpace(string(raw))) == 0 {
					t.Fatalf("expiry emitted no native event: %v", err)
				}
				fresh, err := engine.Open(context.Background(), commonTestStreamMetadata("fresh-after-expiry"))
				if err != nil {
					t.Fatalf("expiry poisoned engine: %v", err)
				}
				defer fresh.Close(context.Background(), Summary{CloseReason: CloseContextCanceled})
				decision, err = fresh.ProcessHeaders(context.Background(), DirectionRequest, nil, true)
				assertCommonDecision(t, "fresh P1/P2", decision, err, ActionAllow, 0)
				decision, err = fresh.ProcessHeaders(context.Background(), DirectionResponse, []Header{{Name: ":status", Value: []byte("200")}}, true)
				assertCommonDecision(t, "fresh companion P3/P4", decision, err, ActionAllow, 0)
				fresh.Close(context.Background(), Summary{CloseReason: CloseResponseEOS})
				if err := fresh.(*commonRuntimeTransaction).CleanupFailure(); err != nil {
					t.Fatal(err)
				}
			})
		}
	}
}

func TestCompositeRuntimeEngineOwnsCompanionUntilCleanup(t *testing.T) {
	for _, mode := range []CompositeMode{CompositeModeEnvoy, CompositeModeTraefik} {
		for _, stage := range []string{"body-limit", "headers-cancel", "handoff-cancel", "claimed-cancel", "response-eos"} {
			t.Run(fmt.Sprintf("%d/%s", mode, stage), func(t *testing.T) {
				engine, eventPath := newBufferedCompositeRuntimeEngineForTest(t, mode)
				tx, err := engine.Open(context.Background(), commonTestStreamMetadata(stage))
				if err != nil {
					t.Fatal(err)
				}
				defer tx.Close(context.Background(), Summary{CloseReason: CloseContextCanceled})
				decision, err := tx.ProcessHeaders(context.Background(), DirectionRequest, nil, false)
				assertCommonDecision(t, "headers", decision, err, ActionAllow, 0)
				if stage != "body-limit" && stage != "headers-cancel" {
					decision, err = tx.ProcessBody(context.Background(), DirectionRequest, []byte("allow"), true)
					assertCommonDecision(t, "handoff with default zero late deadline", decision, err, ActionAllow, 0)
				}
				if stage == "claimed-cancel" || stage == "response-eos" {
					decision, err = tx.ProcessHeaders(context.Background(), DirectionResponse, []Header{{Name: ":status", Value: []byte("200")}, {Name: "content-type", Value: []byte("text/plain")}}, false)
					assertCommonDecision(t, "claimed P3", decision, err, ActionAllow, 0)
				}
				reason := CloseContextCanceled
				if stage == "body-limit" {
					reason = CloseReason("request_block")
				}
				if stage == "response-eos" {
					decision, err = tx.ProcessBody(context.Background(), DirectionResponse, []byte("p4-observe"), true)
					assertCommonDecision(t, "session P4 engine intent", decision, err, ActionDeny, 403)
					if decision.RuleID != "1200004" {
						t.Fatalf("safe companion P4 RuleID = %q", decision.RuleID)
					}
					if err := tx.(HostActionRecorder).RecordHostAction(context.Background(), HostAction{
						Action: AppliedActionLogOnly, VisibleStatus: 200, TransportResult: "log_only",
					}); err != nil {
						t.Fatal(err)
					}
					reason = CloseResponseEOS
				}
				tx.Close(context.Background(), Summary{CloseReason: reason})
				tx.Close(context.Background(), Summary{CloseReason: reason}) // idempotent; no second native free
				if err := tx.(*commonRuntimeTransaction).CleanupFailure(); err != nil {
					t.Fatal(err)
				}
				raw, err := os.ReadFile(eventPath)
				if err != nil {
					t.Fatal(err)
				}
				if len(strings.TrimSpace(string(raw))) == 0 {
					t.Fatal("cleanup emitted no event")
				}
				if stage == "body-limit" && !strings.Contains(string(raw), "body_limit") {
					t.Fatalf("missing observed body-limit event: %s", raw)
				}
				if strings.HasSuffix(stage, "cancel") && !strings.Contains(string(raw), "client_cancel") {
					t.Fatalf("cancellation was not recorded: %s", raw)
				}
			})
		}
	}
}

func TestDirectCommonRuntimeEngineKeepsStreamingGuard(t *testing.T) {
	engine, _ := newCommonRuntimeEngineForTest(t)
	if got := engine.transactionProfileID(); got != 6 {
		t.Errorf("direct ext_proc installed profile ID = %d, want 6", got)
	}
	for _, modes := range [][2]string{{"buffered", "streaming"}, {"streaming", "buffered"}, {"none", "streaming"}} {
		configPath, _ := compositeRuntimeConfigForTest(t, modes[0], modes[1])
		engine, err := NewCommonRuntimeEngine(configPath)
		if engine != nil {
			_ = engine.Close(context.Background())
		}
		if err == nil || engine != nil {
			t.Errorf("NewCommonRuntimeEngine(%v) = %v/%v, want nil/error", modes, engine, err)
		}
	}
}

func newBufferedCompositeRuntimeEngineForTest(t *testing.T, mode CompositeMode) (*CommonRuntimeEngine, string) {
	t.Helper()
	configPath, eventPath := compositeRuntimeConfigForTest(t, "buffered", "streaming")
	engine, err := NewCompositeRuntimeEngine(configPath, mode)
	if err != nil {
		t.Fatal(err)
	}
	t.Cleanup(func() {
		if err := engine.Close(context.Background()); err != nil {
			t.Error(err)
		}
	})
	return engine, eventPath
}

func compositeRuntimeConfigForTest(t *testing.T, requestMode, responseMode string) (string, string) {
	t.Helper()
	directory := t.TempDir()
	rulesPath := filepath.Join(directory, "rules.conf")
	configPath := filepath.Join(directory, "runtime.conf")
	eventPath := filepath.Join(directory, "events.jsonl")
	rules := "SecRuleEngine On\nSecRequestBodyAccess On\nSecResponseBodyAccess On\nSecResponseBodyMimeType text/plain\nSecRule RESPONSE_HEADERS:X-Ms-P3 \"@streq block\" \"id:1200003,phase:3,deny,status:403,log,t:none\"\nSecRule RESPONSE_BODY \"@contains p4-observe\" \"id:1200004,phase:4,deny,status:403,log,t:none\"\n"
	if err := os.WriteFile(rulesPath, []byte(rules), 0o600); err != nil {
		t.Fatal(err)
	}
	config := fmt.Sprintf("enabled=on\nrules_file=%s\nrequest_body_mode=%s\nresponse_body_mode=%s\nphase4_mode=safe\nuse_error_log=off\nevent_path=%s\n", rulesPath, requestMode, responseMode, eventPath)
	if err := os.WriteFile(configPath, []byte(config), 0o600); err != nil {
		t.Fatal(err)
	}
	return configPath, eventPath
}
