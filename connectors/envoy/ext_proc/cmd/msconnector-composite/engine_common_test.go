//go:build libmodsecurity

package main

import (
	"context"
	"os"
	"path/filepath"
	"strings"
	"testing"
)

func TestConfiguredEngineAcceptsCompositeBufferedRequest(t *testing.T) {
	directory := t.TempDir()
	configPath := filepath.Join(directory, "runtime.conf")
	config := "enabled=on\nrules_inline=SecRuleEngine On\nrequest_body_mode=buffered\nresponse_body_mode=streaming\nphase4_mode=safe\nuse_error_log=off\n"
	if err := os.WriteFile(configPath, []byte(config), 0o600); err != nil {
		t.Fatal(err)
	}
	runtime, err := configuredEngine(configPath, "envoy")
	if err != nil {
		t.Fatalf("configuredEngine(buffered/streaming composite) error = %v, want nil", err)
	}
	if err := runtime.close(context.Background()); err != nil {
		t.Fatalf("composite close error = %v, want nil", err)
	}
}

func TestConfiguredEngineRejectsModeBeforeConfig(t *testing.T) {
	for _, mode := range []string{"", "invalid", "ext_proc", "forwardAuth", "Envoy", "envoy\x00traefik"} {
		if _, err := configuredEngine("", mode); err == nil || !strings.Contains(err.Error(), "unsupported composite mode") {
			t.Errorf("configuredEngine(empty,%q) error = %v, want unsupported mode", mode, err)
		}
	}
}
