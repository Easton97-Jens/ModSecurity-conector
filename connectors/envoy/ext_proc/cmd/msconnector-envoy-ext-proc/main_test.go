package main

import (
	"context"
	"encoding/json"
	"errors"
	"net"
	"os"
	"path/filepath"
	"strings"
	"testing"

	"github.com/Easton97-Jens/ModSecurity-conector/connectors/envoy/ext_proc/internal/processor"
)

func TestServeRejectsUnprovenStrictPolicyBeforeListenerAdmission(t *testing.T) {
	occupied, err := net.Listen("tcp", "127.0.0.1:0")
	if err != nil {
		t.Fatalf("reserve test listener: %v", err)
	}
	defer occupied.Close()

	config := processor.Config{
		ListenAddress:        occupied.Addr().String(),
		TransactionIDHeader:  "x-request-id",
		MaxHeaderCount:       128,
		MaxHeaderNameBytes:   256,
		MaxHeaderValueBytes:  8192,
		MaxTotalHeaderBytes:  32768,
		MaxBodyChunkBytes:    1024,
		MaxRequestBodyBytes:  4096,
		MaxResponseBodyBytes: 4096,
		MaxGRPCMessageBytes:  2048,
		EngineTimeoutMS:      100,
		MaxConcurrentStreams: 8,
		CleanupTimeoutMS:     100,
		ShutdownTimeoutMS:    100,
		StreamIdleTimeoutMS:  100,
		LateActionPolicy:     processor.LateActionStrict,
	}
	code, err := serve(config, engineRuntime{engine: rejectingPolicyEngine{}}, "")
	if code != 1 || err == nil || !strings.Contains(err.Error(), "unproven strict policy") {
		t.Fatalf("serve() = (%d, %v), want policy rejection before listener bind", code, err)
	}
}

func TestCheckConfigAdmissionRejectsUnprovenStrictPolicy(t *testing.T) {
	config := strictTestConfig("127.0.0.1:18083")
	err := validateServiceAdmission(config, engineRuntime{engine: rejectingPolicyEngine{}})
	if err == nil || !strings.Contains(err.Error(), "unproven strict policy") {
		t.Fatalf("validateServiceAdmission() error = %v, want strict policy rejection", err)
	}
}

func TestCheckConfigWithoutRuntimeDoesNotBypassStrictAdmission(t *testing.T) {
	configBytes, err := json.Marshal(strictTestConfig("127.0.0.1:18083"))
	if err != nil {
		t.Fatalf("marshal strict config: %v", err)
	}
	configPath := filepath.Join(t.TempDir(), "strict-service.json")
	if err := os.WriteFile(configPath, configBytes, 0o600); err != nil {
		t.Fatalf("write strict config: %v", err)
	}

	code, err := runWithOptions(commandLineOptions{
		configPath:  configPath,
		checkConfig: true,
	})
	if code != 2 || err == nil {
		t.Fatalf("runWithOptions() = (%d, %v), want nonzero strict-admission rejection", code, err)
	}
	if !strings.Contains(err.Error(), "late_action_policy=strict") && !strings.Contains(err.Error(), "--runtime-config") {
		t.Fatalf("runWithOptions() error = %v, want runtime or strict-admission rejection", err)
	}
}

func strictTestConfig(listenAddress string) processor.Config {
	return processor.Config{
		ListenAddress:        listenAddress,
		TransactionIDHeader:  "x-request-id",
		MaxHeaderCount:       128,
		MaxHeaderNameBytes:   256,
		MaxHeaderValueBytes:  8192,
		MaxTotalHeaderBytes:  32768,
		MaxBodyChunkBytes:    1024,
		MaxRequestBodyBytes:  4096,
		MaxResponseBodyBytes: 4096,
		MaxGRPCMessageBytes:  2048,
		EngineTimeoutMS:      100,
		MaxConcurrentStreams: 8,
		CleanupTimeoutMS:     100,
		ShutdownTimeoutMS:    100,
		StreamIdleTimeoutMS:  100,
		LateActionPolicy:     processor.LateActionStrict,
	}
}

type rejectingPolicyEngine struct{}

func (rejectingPolicyEngine) Open(context.Context, processor.StreamMetadata) (processor.Transaction, error) {
	return nil, errors.New("unexpected stream admission")
}

func (rejectingPolicyEngine) ValidateLateActionPolicy(processor.LateActionPolicy) error {
	return errors.New("unproven strict policy")
}
