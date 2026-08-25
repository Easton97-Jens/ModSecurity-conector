package processor

import (
	"os"
	"path/filepath"
	"strings"
	"sync"
	"testing"

	"golang.org/x/sys/unix"
)

func TestJSONLObserverWritesMetadataOnlyCompletionRecord(t *testing.T) {
	path := filepath.Join(t.TempDir(), "events.jsonl")
	observer, err := NewJSONLObserver(path)
	if err != nil {
		t.Fatalf("NewJSONLObserver() error = %v", err)
	}
	defer observer.Close()
	if err := observer.Record(Summary{
		TransactionID:      "test-transaction",
		RequestHeaderCount: 3,
		ResponseBodyBytes:  17,
		LateAction:         LateActionNone,
		CloseReason:        CloseResponseEOS,
	}); err != nil {
		t.Fatalf("Record() error = %v", err)
	}
	content, err := os.ReadFile(path)
	if err != nil {
		t.Fatalf("ReadFile() error = %v", err)
	}
	line := string(content)
	for _, expected := range []string{
		`"integration_mode":"ext_proc"`,
		`"evaluation_mode":"passthrough_nonpromoted"`,
		`"rule_evaluation":"not_wired"`,
		`"transaction_id":"test-transaction"`,
	} {
		if !strings.Contains(line, expected) {
			t.Fatalf("event record missing %s: %s", expected, line)
		}
	}
	for _, forbidden := range []string{`"headers"`, `"body":"`, `"request_body":"`, `"response_body":"`} {
		if strings.Contains(line, forbidden) {
			t.Fatalf("event record contains payload-bearing field %s: %s", forbidden, line)
		}
	}
}

func TestJSONLObserverRecordCloseConcurrent(t *testing.T) {
	for iteration := 0; iteration < 128; iteration++ {
		path := filepath.Join(t.TempDir(), "events.jsonl")
		observer, err := NewJSONLObserver(path)
		if err != nil {
			t.Fatalf("NewJSONLObserver() error = %v", err)
		}

		start := make(chan struct{})
		var group sync.WaitGroup
		var recordErr error
		group.Add(2)
		go func() {
			defer group.Done()
			<-start
			recordErr = observer.Record(Summary{TransactionID: "concurrent"})
		}()
		go func() {
			defer group.Done()
			<-start
			if err := observer.Close(); err != nil {
				t.Errorf("Close() error = %v", err)
			}
		}()
		close(start)
		group.Wait()

		if recordErr != nil && recordErr.Error() != "event observer is closed" {
			t.Fatalf("Record() unexpected concurrent error = %v", recordErr)
		}
	}
}

func TestJSONLObserverRejectsRelativePath(t *testing.T) {
	if _, err := NewJSONLObserver("events.jsonl"); err == nil {
		t.Fatal("NewJSONLObserver() accepted relative path")
	}
}

func TestJSONLObserverRejectsNormalizedPathWithTraversal(t *testing.T) {
	path := t.TempDir() + "/nested/../events.jsonl"
	if _, err := NewJSONLObserver(path); err == nil {
		t.Fatal("NewJSONLObserver() accepted non-normalized path")
	}
}

func TestJSONLObserverRejectsFinalSymlink(t *testing.T) {
	dir := t.TempDir()
	target := filepath.Join(dir, "target.jsonl")
	link := filepath.Join(dir, "events.jsonl")
	if err := os.WriteFile(target, nil, 0o600); err != nil {
		t.Fatal(err)
	}
	if err := os.Symlink(target, link); err != nil {
		t.Fatal(err)
	}
	if _, err := NewJSONLObserver(link); err == nil {
		t.Fatal("NewJSONLObserver() followed final symlink")
	}
}

func TestJSONLObserverRejectsAncestorSymlink(t *testing.T) {
	dir := t.TempDir()
	target := filepath.Join(dir, "target")
	if err := os.Mkdir(target, 0o700); err != nil {
		t.Fatal(err)
	}
	link := filepath.Join(dir, "link")
	if err := os.Symlink(target, link); err != nil {
		t.Fatal(err)
	}
	path := filepath.Join(link, "nested", "events.jsonl")
	if _, err := NewJSONLObserver(path); err == nil {
		t.Fatal("NewJSONLObserver() followed ancestor symlink")
	}
}

func TestJSONLObserverRejectsUnexpectedExistingFileTypes(t *testing.T) {
	dir := t.TempDir()
	directory := filepath.Join(dir, "events.jsonl")
	if err := os.Mkdir(directory, 0o700); err != nil {
		t.Fatal(err)
	}
	if _, err := NewJSONLObserver(directory); err == nil {
		t.Fatal("NewJSONLObserver() accepted directory")
	}

	fifo := filepath.Join(dir, "events.fifo")
	if err := unix.Mkfifo(fifo, 0o600); err != nil {
		t.Fatal(err)
	}
	if _, err := NewJSONLObserver(fifo); err == nil {
		t.Fatal("NewJSONLObserver() accepted FIFO")
	}
}

func TestJSONLObserverRejectsExistingFileWithUnsafePermissions(t *testing.T) {
	dir := t.TempDir()
	path := filepath.Join(dir, "events.jsonl")
	if err := os.WriteFile(path, nil, 0o666); err != nil {
		t.Fatal(err)
	}
	if _, err := NewJSONLObserver(path); err == nil {
		t.Fatal("NewJSONLObserver() accepted owner-readable file with unsafe permissions")
	}
	info, err := os.Stat(path)
	if err != nil {
		t.Fatal(err)
	}
	if got := info.Mode().Perm(); got != 0o644 {
		t.Fatalf("rejected event log mode changed to %o", got)
	}
}
