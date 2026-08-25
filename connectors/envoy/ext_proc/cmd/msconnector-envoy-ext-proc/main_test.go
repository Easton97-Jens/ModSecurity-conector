package main

import (
	"errors"
	"net"
	"testing"
	"time"

	"google.golang.org/grpc"
)

func TestWaitForServerTerminationStopsOnFatalCleanupFailure(t *testing.T) {
	listener, err := net.Listen("tcp", "127.0.0.1:0")
	if err != nil {
		t.Fatalf("Listen() error = %v", err)
	}
	address := listener.Addr().String()
	server := grpc.NewServer()
	fatalErrors := make(chan error, 1)
	fatalErr := errors.New("native transaction cleanup timed out")
	fatalErrors <- fatalErr

	started := time.Now()
	exitCode, err := waitForServerTermination(server, listener, 100, fatalErrors)
	if elapsed := time.Since(started); elapsed > time.Second {
		t.Fatalf("waitForServerTermination() blocked for %s", elapsed)
	}
	if exitCode != 1 {
		t.Fatalf("exit code = %d, want 1", exitCode)
	}
	if !errors.Is(err, fatalErr) {
		t.Fatalf("waitForServerTermination() error = %v, want fatal cleanup error", err)
	}

	replacement, err := net.Listen("tcp", address)
	if err != nil {
		t.Fatalf("fatal stop retained listener %s: %v", address, err)
	}
	if err := replacement.Close(); err != nil {
		t.Fatalf("replacement listener Close() error = %v", err)
	}
}
