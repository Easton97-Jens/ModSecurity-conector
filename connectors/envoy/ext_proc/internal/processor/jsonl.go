package processor

import (
	"encoding/json"
	"errors"
	"fmt"
	"os"
	"path/filepath"
	"strings"
	"sync"

	"golang.org/x/sys/unix"
)

// JSONLObserver writes one payload-free completion record per ext_proc stream.
// The record is intentionally limited to transport/lifecycle counters and
// action metadata so it is safe to archive as connector runtime evidence.
type JSONLObserver struct {
	mu             sync.Mutex
	file           *os.File
	evaluationMode string
	ruleEvaluation string
}

type jsonlCompletionRecord struct {
	Event               string            `json:"event"`
	IntegrationMode     string            `json:"integration_mode"`
	EvaluationMode      string            `json:"evaluation_mode"`
	RuleEvaluation      string            `json:"rule_evaluation"`
	TransactionID       string            `json:"transaction_id,omitempty"`
	RequestHeaderCount  uint64            `json:"request_header_count"`
	ResponseHeaderCount uint64            `json:"response_header_count"`
	RequestBodyChunks   uint64            `json:"request_body_chunks"`
	ResponseBodyChunks  uint64            `json:"response_body_chunks"`
	RequestBodyBytes    int64             `json:"request_body_bytes"`
	ResponseBodyBytes   int64             `json:"response_body_bytes"`
	LateAction          LateActionOutcome `json:"late_action"`
	CloseReason         CloseReason       `json:"close_reason"`
}

// NewJSONLObserver opens an absolute, owner-readable event path. The caller
// controls the enclosing runtime directory; this package does not create any
// evidence inside the checkout.
func NewJSONLObserver(path string) (*JSONLObserver, error) {
	return NewJSONLObserverWithMode(path, "passthrough_nonpromoted", "not_wired")
}

// NewJSONLObserverWithMode writes stream-completion metadata for the concrete
// engine selected by the executable. It does not create rule decision events;
// Common Runtime remains the only source of any configured decision event.
func NewJSONLObserverWithMode(path, evaluationMode, ruleEvaluation string) (*JSONLObserver, error) {
	if path == "" {
		return nil, fmt.Errorf("event log path is required")
	}
	if evaluationMode == "" || ruleEvaluation == "" {
		return nil, fmt.Errorf("event evaluation mode is required")
	}
	if !filepath.IsAbs(path) {
		return nil, fmt.Errorf("event log path must be absolute")
	}
	if filepath.Clean(path) != path {
		return nil, fmt.Errorf("event log path must be normalized")
	}
	parent := filepath.Dir(path)
	leaf := filepath.Base(path)
	if leaf == "" || leaf == "." || leaf == string(filepath.Separator) {
		return nil, fmt.Errorf("event log path must name a regular file")
	}
	parentFD, err := openPrivateEventParent(parent)
	if err != nil {
		return nil, err
	}
	defer func() { _ = unix.Close(parentFD) }()
	file, err := openPrivateEventLog(parentFD, leaf, path)
	if err != nil {
		return nil, fmt.Errorf("open event log: %w", err)
	}
	return &JSONLObserver{
		file:           file,
		evaluationMode: evaluationMode,
		ruleEvaluation: ruleEvaluation,
	}, nil
}

// openPrivateEventParent walks every absolute directory component with
// openat(O_NOFOLLOW), creating only missing components with mkdirat. It
// returns the validated final descriptor so callers can keep the directory
// object anchored through their final openat operation.
func openPrivateEventParent(parent string) (int, error) {
	fd, err := unix.Open("/", unix.O_RDONLY|unix.O_DIRECTORY|unix.O_CLOEXEC|unix.O_NOFOLLOW, 0)
	if err != nil {
		return -1, fmt.Errorf("open event log root: %w", err)
	}
	relative := strings.TrimPrefix(parent, string(filepath.Separator))
	if relative == "" {
		if err := ensurePrivateEventDirectory(fd); err != nil {
			_ = unix.Close(fd)
			return -1, err
		}
		return fd, nil
	}
	for _, component := range strings.Split(relative, string(filepath.Separator)) {
		if component == "" || component == "." || component == ".." {
			_ = unix.Close(fd)
			return -1, fmt.Errorf("event log parent contains unsafe component")
		}
		next, openErr := unix.Openat(fd, component, unix.O_RDONLY|unix.O_DIRECTORY|unix.O_CLOEXEC|unix.O_NOFOLLOW, 0)
		if openErr != nil && errors.Is(openErr, unix.ENOENT) {
			if mkdirErr := unix.Mkdirat(fd, component, 0o750); mkdirErr != nil && !errors.Is(mkdirErr, unix.EEXIST) {
				_ = unix.Close(fd)
				return -1, fmt.Errorf("create event log directory: %w", mkdirErr)
			}
			next, openErr = unix.Openat(fd, component, unix.O_RDONLY|unix.O_DIRECTORY|unix.O_CLOEXEC|unix.O_NOFOLLOW, 0)
		}
		if openErr != nil {
			_ = unix.Close(fd)
			return -1, fmt.Errorf("open event log directory: %w", openErr)
		}
		if err := unix.Close(fd); err != nil {
			_ = unix.Close(next)
			return -1, fmt.Errorf("close event log directory: %w", err)
		}
		fd = next
	}
	if err := ensurePrivateEventDirectory(fd); err != nil {
		_ = unix.Close(fd)
		return -1, err
	}
	return fd, nil
}

func ensurePrivateEventDirectory(fd int) error {
	var stat unix.Stat_t
	if err := unix.Fstat(fd, &stat); err != nil {
		return fmt.Errorf("inspect event log directory: %w", err)
	}
	if stat.Mode&unix.S_IFMT != unix.S_IFDIR || stat.Mode&0o022 != 0 || stat.Uid != uint32(unix.Geteuid()) {
		return fmt.Errorf("event log parent must be an owner-private directory")
	}
	return nil
}

// openPrivateEventLog uses a retained parent descriptor and basename-only
// openat calls, so an ancestor replacement cannot redirect event creation.
// Existing files with unsafe permissions are rejected without mutation;
// newly-created files are normalized to 0600 and verified. The ext_proc
// module is supported on Unix targets; unsupported targets fail closed at
// build time rather than silently falling back to a symlink-following open.
func openPrivateEventLog(parentFD int, leaf, displayPath string) (*os.File, error) {
	if parentFD < 0 || leaf == "" || leaf == "." || leaf == ".." || strings.ContainsRune(leaf, filepath.Separator) {
		return nil, fmt.Errorf("event log final component is unsafe")
	}
	flags := unix.O_WRONLY | unix.O_APPEND | unix.O_CLOEXEC | unix.O_NOFOLLOW | unix.O_NONBLOCK
	fd, err := unix.Openat(parentFD, leaf, flags|unix.O_CREAT|unix.O_EXCL, 0o600)
	existed := err != nil
	if errors.Is(err, unix.EEXIST) {
		fd, err = unix.Openat(parentFD, leaf, flags, 0)
	}
	if err != nil {
		return nil, err
	}
	var stat unix.Stat_t
	if err := unix.Fstat(fd, &stat); err != nil {
		_ = unix.Close(fd)
		return nil, err
	}
	if stat.Mode&unix.S_IFMT != unix.S_IFREG || stat.Uid != uint32(unix.Geteuid()) {
		_ = unix.Close(fd)
		return nil, fmt.Errorf("event log must be an owner-owned regular file")
	}
	if existed && stat.Mode&0o777 != 0o600 {
		_ = unix.Close(fd)
		return nil, fmt.Errorf("existing event log must have mode 0600")
	}
	if !existed {
		if err := unix.Fchmod(fd, 0o600); err != nil {
			_ = unix.Close(fd)
			return nil, err
		}
		if err := unix.Fstat(fd, &stat); err != nil || stat.Mode&0o777 != 0o600 {
			_ = unix.Close(fd)
			if err != nil {
				return nil, err
			}
			return nil, fmt.Errorf("event log permissions could not be restricted")
		}
	}
	return os.NewFile(uintptr(fd), displayPath), nil
}

func (observer *JSONLObserver) Record(summary Summary) error {
	if observer == nil {
		return fmt.Errorf("event observer is closed")
	}
	record := jsonlCompletionRecord{
		Event:               "ext_proc_stream_complete",
		IntegrationMode:     "ext_proc",
		EvaluationMode:      observer.evaluationMode,
		RuleEvaluation:      observer.ruleEvaluation,
		TransactionID:       summary.TransactionID,
		RequestHeaderCount:  summary.RequestHeaderCount,
		ResponseHeaderCount: summary.ResponseHeaderCount,
		RequestBodyChunks:   summary.RequestBodyChunks,
		ResponseBodyChunks:  summary.ResponseBodyChunks,
		RequestBodyBytes:    summary.RequestBodyBytes,
		ResponseBodyBytes:   summary.ResponseBodyBytes,
		LateAction:          summary.LateAction,
		CloseReason:         summary.CloseReason,
	}
	encoded, err := json.Marshal(record)
	if err != nil {
		return fmt.Errorf("encode event: %w", err)
	}
	observer.mu.Lock()
	defer observer.mu.Unlock()
	if observer.file == nil {
		return fmt.Errorf("event observer is closed")
	}
	if _, err := observer.file.Write(append(encoded, '\n')); err != nil {
		return fmt.Errorf("write event: %w", err)
	}
	return nil
}

func (observer *JSONLObserver) Close() error {
	if observer == nil {
		return nil
	}
	observer.mu.Lock()
	defer observer.mu.Unlock()
	if observer.file == nil {
		return nil
	}
	err := observer.file.Close()
	observer.file = nil
	return err
}
