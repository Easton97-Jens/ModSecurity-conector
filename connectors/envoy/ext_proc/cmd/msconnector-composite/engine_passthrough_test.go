//go:build !libmodsecurity

package main

import "testing"

func TestSourceOnlyBuildRefusesServingEngine(t *testing.T) {
	t.Parallel()
	if _, err := configuredEngine("", "envoy"); err == nil {
		t.Fatal("source-only composite command unexpectedly exposed a serving engine")
	}
	if _, err := configuredEngine("/runtime.conf", "traefik"); err == nil {
		t.Fatal("source-only composite command accepted a runtime configuration")
	}
}
