//go:build libmodsecurity && linux

package processor

import (
	"context"
	"os"
	"os/exec"
	"os/signal"
	"syscall"
	"testing"
	"time"
)

func TestCompositeConsumedCleanupFailureDoesNotRetryFreedNative(t *testing.T) {
	const childMarker = "MSCONNECTOR_TEST_CONSUMED_CLEANUP_CHILD"
	if os.Getenv(childMarker) != "1" {
		ctx, cancel := context.WithTimeout(context.Background(), 15*time.Second)
		defer cancel()
		command := exec.CommandContext(ctx, os.Args[0], "-test.run=^TestCompositeConsumedCleanupFailureDoesNotRetryFreedNative$", "-test.v")
		command.Env = append(os.Environ(), childMarker+"=1")
		if output, err := command.CombinedOutput(); err != nil {
			t.Fatalf("isolated native cleanup failure: %v\n%s", err, output)
		}
		return
	}
	configPath, _ := compositeRuntimeConfigForTest(t, "buffered", "streaming")
	engine, err := NewCompositeRuntimeEngine(configPath, CompositeModeEnvoy)
	if err != nil {
		t.Fatal(err)
	}
	defer engine.destructor() // native state is quiescent; process is isolated
	tx, err := engine.Open(context.Background(), commonTestStreamMetadata("event-write-failure"))
	if err != nil {
		t.Fatal(err)
	}
	decision, err := tx.ProcessHeaders(context.Background(), DirectionRequest, nil, true)
	assertCommonDecision(t, "P1/P2", decision, err, ActionAllow, 0)
	if err := tx.(ResponseCompanionClaimer).ClaimResponseCompanion(context.Background()); err != nil {
		t.Fatal(err)
	}
	other, err := engine.Open(context.Background(), commonTestStreamMetadata("other-active-stream"))
	if err != nil {
		t.Fatal(err)
	}
	decision, err = other.ProcessHeaders(context.Background(), DirectionRequest, nil, true)
	assertCommonDecision(t, "other P1/P2", decision, err, ActionAllow, 0)
	// Limit only this isolated test process. The already-open task-owned event
	// file can no longer grow; no shared file, signal policy or limit is changed.
	signal.Ignore(syscall.SIGXFSZ)
	if err := syscall.Setrlimit(syscall.RLIMIT_FSIZE, &syscall.Rlimit{Cur: 0, Max: 0}); err != nil {
		t.Fatal(err)
	}
	tx.Close(context.Background(), Summary{CloseReason: CloseContextCanceled})
	native := tx.(*commonRuntimeTransaction)
	if native.CleanupFailure() == nil {
		t.Fatal("event-write failure was hidden")
	}
	if native.native != nil || !native.closed {
		t.Fatal("consumed native pointer retained for retry")
	}
	tx.Close(context.Background(), Summary{CloseReason: CloseContextCanceled})
	if err := other.(ResponseCompanionClaimer).ClaimResponseCompanion(context.Background()); err == nil {
		t.Fatal("other stream claimed after engine terminal failure")
	}
	if _, err := other.ProcessHeaders(context.Background(), DirectionResponse, nil, true); err == nil {
		t.Fatal("other stream processed P3 after engine terminal failure")
	}
	other.Close(context.Background(), Summary{CloseReason: CloseContextCanceled})
	if len(engine.transactions) != 0 {
		t.Fatal("consumed transactions remained registered")
	}
	if _, err := engine.Open(context.Background(), commonTestStreamMetadata("after-failure")); err == nil {
		t.Fatal("engine reused after terminal cleanup failure")
	}
	if err := engine.Close(context.Background()); err == nil {
		t.Fatal("engine shutdown concealed cleanup failure")
	}
}
