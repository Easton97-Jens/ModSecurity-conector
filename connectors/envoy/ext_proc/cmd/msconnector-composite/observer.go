package main

import (
	"bytes"
	"encoding/json"
	"errors"
	"fmt"
	"io"
	"os"
	"path/filepath"
	"sort"
	"strings"
	"sync"
	"syscall"
	"time"

	"github.com/Easton97-Jens/ModSecurity-conector/connectors/envoy/ext_proc/internal/composite"
)

const (
	maxCompositeEventRecordBytes      int64 = 2048
	maxCompositeEventLineBytes        int64 = maxCompositeEventRecordBytes + 1
	maxCompositeEventLogBytes         int64 = 1 << 20
	maxCompositeEventLogOverflowBytes int64 = 7 << 20
	maxCompositeActiveDecisions             = 128
)

// compositeObserver is deliberately narrower than the legacy stream observer:
// it records only lifecycle/action metadata, never headers, bodies, leases, or
// caller identifiers. Writes are serialized and each record is bounded. The
// log rotates only before the next lifecycle, so it never discards a partial
// active transaction; a fixed overflow ceiling bounds that short deferral.
type compositeObserver struct {
	mu              sync.Mutex
	file            eventLogFile
	maxSize         int64
	maxOverflow     int64
	size            int64
	active          map[string]eventLifecycle
	rotationPending bool
	lastErr         error
}

// eventLogFile is deliberately the small subset used by the observer. Keeping
// it narrow lets the write rollback path be exercised with a short-writing
// test double; production always supplies an *os.File opened with O_NOFOLLOW.
type eventLogFile interface {
	io.ReaderAt
	io.Writer
	Stat() (os.FileInfo, error)
	Truncate(int64) error
	Seek(int64, int) (int64, error)
	Close() error
}

type eventLifecycle struct {
	Connector    string
	RuleID       string
	RequestPath  string
	ResponsePath string
	Transport    string
}

type compositeEventRecord struct {
	DecisionID       string `json:"decision_id"`
	Connector        string `json:"connector"`
	RuleID           string `json:"rule_id,omitempty"`
	Phase            string `json:"phase"`
	Outcome          string `json:"outcome"`
	Reason           string `json:"reason,omitempty"`
	RequestedAction  string `json:"requested_action,omitempty"`
	ActualHostAction string `json:"actual_host_action,omitempty"`
	VisibleStatus    int    `json:"visible_status,omitempty"`
	CleanupOutcome   string `json:"cleanup_outcome,omitempty"`
	EventTime        string `json:"event_time"`
	RequestPath      string `json:"request_path"`
	ResponsePath     string `json:"response_path"`
	Transport        string `json:"transport"`
}

func newCompositeObserver(path string) (*compositeObserver, *compositeObserver, error) {
	return newCompositeObserverWithLimit(path, maxCompositeEventLogBytes)
}

func newCompositeObserverWithLimit(path string, maxSize int64) (*compositeObserver, *compositeObserver, error) {
	return newCompositeObserverWithBounds(path, maxSize, maxCompositeEventLogOverflowBytes)
}

func newCompositeObserverWithBounds(path string, maxSize, maxOverflow int64) (*compositeObserver, *compositeObserver, error) {
	if path == "" {
		return nil, nil, errors.New("event log path is required")
	}
	if !filepath.IsAbs(path) {
		return nil, nil, errors.New("event log path must be absolute")
	}
	if maxSize < maxCompositeEventRecordBytes+1 {
		return nil, nil, errors.New("event log retention bound is too small")
	}
	if maxOverflow < 0 {
		return nil, nil, errors.New("event log overflow bound is invalid")
	}
	if maxSize > (1<<63-1)-maxOverflow {
		return nil, nil, errors.New("event log retention bounds overflow")
	}
	if _, err := secureParent(filepath.Dir(path)); err != nil {
		return nil, nil, err
	}
	file, err := os.OpenFile(path, os.O_CREATE|os.O_APPEND|os.O_RDWR|syscall.O_NOFOLLOW, 0o600)
	if err != nil {
		return nil, nil, fmt.Errorf("open event log: %w", err)
	}
	stat, err := file.Stat()
	if err != nil {
		_ = file.Close()
		return nil, nil, fmt.Errorf("stat event log: %w", err)
	}
	owner, ok := stat.Sys().(*syscall.Stat_t)
	if !stat.Mode().IsRegular() || stat.Mode().Perm()&0077 != 0 || !ok || owner.Uid != uint32(os.Getuid()) {
		_ = file.Close()
		return nil, nil, errors.New("event log must be an owner-only regular file")
	}
	size := stat.Size()
	if size > eventLogHardLimit(maxSize, maxOverflow) {
		if err := resetEventLog(file); err != nil {
			_ = file.Close()
			return nil, nil, fmt.Errorf("reset oversized event log: %w", err)
		}
		size = 0
	} else if size > 0 {
		size, err = repairEventLogTail(file, size)
		if err != nil {
			_ = file.Close()
			return nil, nil, fmt.Errorf("repair event log tail: %w", err)
		}
	}
	active, err := recoverEventLifecycles(file, size)
	if err != nil {
		_ = file.Close()
		return nil, nil, fmt.Errorf("recover event log lifecycle state: %w", err)
	}
	recoveryEvents := recoveryTerminalEvents(active)
	if !eventLogHasRecoveryReservation(size, len(recoveryEvents), maxSize, maxOverflow) {
		// A prior version could reach the hard cap without reserving space for
		// crash-recovery terminals. A restarted coordinator cannot resume those
		// transactions, so reset this owner-only legacy window rather than make
		// the connector unavailable. Current writes reserve that space up front.
		if err := resetEventLog(file); err != nil {
			_ = file.Close()
			return nil, nil, fmt.Errorf("reset unrecoverable event log: %w", err)
		}
		size = 0
		active = make(map[string]eventLifecycle)
		recoveryEvents = nil
	}
	observer := &compositeObserver{file: file, maxSize: maxSize, maxOverflow: maxOverflow, size: size, active: active}
	for _, event := range recoveryEvents {
		if err := observer.Observe(event); err != nil {
			_ = file.Close()
			return nil, nil, fmt.Errorf("close recovered event lifecycle: %w", err)
		}
	}
	return observer, observer, nil
}

func eventLogHardLimit(maxSize, maxOverflow int64) int64 {
	return maxSize + maxOverflow
}

func eventLogHasRecoveryReservation(size int64, activeCount int, maxSize, maxOverflow int64) bool {
	if size < 0 || activeCount < 0 {
		return false
	}
	reserved := int64(activeCount) * maxCompositeEventLineBytes
	hardLimit := eventLogHardLimit(maxSize, maxOverflow)
	return reserved <= hardLimit && size <= hardLimit-reserved
}

func eventLogWriteFits(size, next int64, activeAfter int, maxSize, maxOverflow int64) bool {
	if size < 0 || next < 0 || activeAfter < 0 {
		return false
	}
	reserved := int64(activeAfter) * maxCompositeEventLineBytes
	hardLimit := eventLogHardLimit(maxSize, maxOverflow)
	if reserved > hardLimit || next > hardLimit-reserved {
		return false
	}
	return size <= hardLimit-reserved-next
}

func secureParent(path string) (string, error) {
	info, err := os.Lstat(path)
	if err != nil {
		return "", fmt.Errorf("event log parent: %w", err)
	}
	stat, ok := info.Sys().(*syscall.Stat_t)
	if !ok || !info.IsDir() || info.Mode()&os.ModeSymlink != 0 || info.Mode().Perm()&0022 != 0 || stat.Uid != uint32(os.Getuid()) {
		return "", errors.New("event log parent must be an owner-controlled non-writable directory")
	}
	return path, nil
}

func resetEventLog(file eventLogFile) error {
	if err := file.Truncate(0); err != nil {
		return err
	}
	_, err := file.Seek(0, io.SeekStart)
	return err
}

func repairEventLogTail(file eventLogFile, size int64) (int64, error) {
	contents := make([]byte, size)
	n, err := file.ReadAt(contents, 0)
	if err != nil && !errors.Is(err, io.EOF) {
		return 0, err
	}
	if n != len(contents) {
		return 0, io.ErrUnexpectedEOF
	}
	lastGood := 0
	remaining := contents
	for len(remaining) > 0 {
		lineEnd := bytes.IndexByte(remaining, '\n')
		if lineEnd < 0 || !json.Valid(remaining[:lineEnd]) {
			break
		}
		lastGood += lineEnd + 1
		remaining = remaining[lineEnd+1:]
	}
	if int64(lastGood) == size {
		return size, nil
	}
	if err := file.Truncate(int64(lastGood)); err != nil {
		return 0, err
	}
	if _, err := file.Seek(0, io.SeekStart); err != nil {
		return 0, err
	}
	return int64(lastGood), nil
}

// recoverEventLifecycles derives the bounded set of decision IDs whose last
// valid retained record is non-terminal. Constructor recovery immediately
// appends a restart terminal for each such ID, preserving an intelligible
// lifecycle before the next retention rotation. Records that are not from the
// bounded composite schema are ignored rather than treated as lifecycle state.
func recoverEventLifecycles(file eventLogFile, size int64) (map[string]eventLifecycle, error) {
	active := make(map[string]eventLifecycle)
	if size == 0 {
		return active, nil
	}
	contents := make([]byte, size)
	n, err := file.ReadAt(contents, 0)
	if err != nil && !errors.Is(err, io.EOF) {
		return nil, err
	}
	if n != len(contents) {
		return nil, io.ErrUnexpectedEOF
	}
	for _, line := range bytes.Split(contents, []byte{'\n'}) {
		if len(line) == 0 {
			continue
		}
		var record compositeEventRecord
		if err := json.Unmarshal(line, &record); err != nil || !recoverableLifecycleRecord(record) {
			continue
		}
		if record.Phase == "terminal" {
			delete(active, record.DecisionID)
			continue
		}
		if _, exists := active[record.DecisionID]; !exists && len(active) >= maxCompositeActiveDecisions {
			return nil, errors.New("recovered event lifecycle capacity exceeded")
		}
		active[record.DecisionID] = eventLifecycle{
			Connector:    record.Connector,
			RuleID:       record.RuleID,
			RequestPath:  record.RequestPath,
			ResponsePath: record.ResponsePath,
			Transport:    record.Transport,
		}
	}
	return active, nil
}

func recoverableLifecycleRecord(record compositeEventRecord) bool {
	if record.DecisionID == "" || record.Connector == "" || record.Phase == "" || record.RequestPath == "" || record.ResponsePath == "" || record.Transport == "" {
		return false
	}
	if len(record.RuleID) > 128 {
		return false
	}
	for _, value := range []string{record.DecisionID, record.Connector, record.RuleID, record.Phase, record.RequestPath, record.ResponsePath, record.Transport} {
		if len(value) > 256 || strings.ContainsAny(value, "\r\n") {
			return false
		}
	}
	return true
}

func recoveryTerminalEvents(active map[string]eventLifecycle) []composite.Event {
	ids := make([]string, 0, len(active))
	for id := range active {
		ids = append(ids, id)
	}
	sort.Strings(ids)
	now := time.Now()
	events := make([]composite.Event, 0, len(ids))
	for _, id := range ids {
		metadata := active[id]
		events = append(events, composite.Event{
			DecisionID:     id,
			Connector:      metadata.Connector,
			RuleID:         metadata.RuleID,
			Phase:          "terminal",
			Outcome:        "closed",
			Reason:         "restart_recovery",
			CleanupOutcome: "restart_recovery",
			RequestPath:    metadata.RequestPath,
			ResponsePath:   metadata.ResponsePath,
			Transport:      metadata.Transport,
			EventTime:      now,
		})
	}
	return events
}

func (o *compositeObserver) prepareEventWriteLocked(event composite.Event, next int64) error {
	stat, err := o.file.Stat()
	if err != nil {
		return fmt.Errorf("stat event log before write: %w", err)
	}
	o.size = stat.Size()
	if o.size >= o.maxSize {
		o.rotationPending = true
	}
	if o.rotationPending && len(o.active) == 0 {
		if err := resetEventLog(o.file); err != nil {
			return fmt.Errorf("reset event log retention window: %w", err)
		}
		o.size = 0
		o.rotationPending = false
	}
	if event.Phase == "terminal" {
		if _, ok := o.active[event.DecisionID]; !ok {
			return errors.New("terminal event has no active lifecycle")
		}
		if !eventLogWriteFits(o.size, next, len(o.active)-1, o.maxSize, o.maxOverflow) {
			return errors.New("event log hard retention bound exceeded")
		}
		return nil
	}
	activeAfter := len(o.active)
	_, active := o.active[event.DecisionID]
	if !active {
		if len(o.active) >= maxCompositeActiveDecisions {
			return errors.New("active event lifecycle capacity exceeded")
		}
		activeAfter++
	}
	if !eventLogWriteFits(o.size, next, activeAfter, o.maxSize, o.maxOverflow) {
		return errors.New("event log hard retention bound exceeded")
	}
	if !active {
		o.active[event.DecisionID] = eventLifecycle{
			Connector:    event.Connector,
			RuleID:       event.RuleID,
			RequestPath:  event.RequestPath,
			ResponsePath: event.ResponsePath,
			Transport:    event.Transport,
		}
	}
	return nil
}

func (o *compositeObserver) completeEventWriteLocked(event composite.Event) {
	if event.Phase == "terminal" {
		delete(o.active, event.DecisionID)
	}
	if o.size >= o.maxSize {
		o.rotationPending = true
	}
}

func (o *compositeObserver) restoreFailedWriteLocked(size int64) error {
	if err := o.file.Truncate(size); err != nil {
		return err
	}
	if _, err := o.file.Seek(0, io.SeekStart); err != nil {
		return err
	}
	o.size = size
	return nil
}

func validateCompositeEvent(event composite.Event) error {
	for _, value := range []string{event.DecisionID, event.Connector, event.RuleID, event.Phase, event.Outcome, event.Reason, event.RequestedAction, event.ActualHostAction, event.CleanupOutcome, event.RequestPath, event.ResponsePath, event.Transport} {
		if len(value) > 256 || strings.ContainsAny(value, "\r\n") {
			return errors.New("event metadata exceeds bounds")
		}
	}
	if len(event.RuleID) > 128 {
		return errors.New("rule identifier exceeds bounds")
	}
	if event.DecisionID == "" || event.RequestPath == "" || event.ResponsePath == "" || event.Transport == "" {
		return errors.New("event pipeline metadata is required")
	}
	return nil
}

func compositeEventRecordFor(event composite.Event) ([]byte, error) {
	record := compositeEventRecord{
		DecisionID: event.DecisionID, Connector: event.Connector, RuleID: event.RuleID,
		Phase: event.Phase, Outcome: event.Outcome, Reason: event.Reason,
		RequestedAction: event.RequestedAction, ActualHostAction: event.ActualHostAction,
		VisibleStatus: event.VisibleStatus, CleanupOutcome: event.CleanupOutcome,
		EventTime:   event.EventTime.UTC().Format("2006-01-02T15:04:05.999999999Z07:00"),
		RequestPath: event.RequestPath, ResponsePath: event.ResponsePath, Transport: event.Transport,
	}
	line, err := json.Marshal(record)
	if err != nil || len(line) > int(maxCompositeEventRecordBytes) {
		return nil, errors.New("event record exceeds bounds")
	}
	return line, nil
}

func (o *compositeObserver) Observe(event composite.Event) error {
	if o == nil || o.file == nil {
		return o.fail(errors.New("event observer is closed"))
	}
	if err := validateCompositeEvent(event); err != nil {
		return o.fail(err)
	}
	line, err := compositeEventRecordFor(event)
	if err != nil {
		return o.fail(err)
	}
	o.mu.Lock()
	defer o.mu.Unlock()
	if o.file == nil {
		o.lastErr = errors.New("event observer is closed")
		return o.lastErr
	}
	line = append(line, '\n')
	if err := o.prepareEventWriteLocked(event, int64(len(line))); err != nil {
		o.lastErr = err
		return err
	}
	startSize := o.size
	written := 0
	for written < len(line) {
		n, writeErr := o.file.Write(line[written:])
		if n < 0 || n > len(line)-written {
			writeErr = errors.New("event log write returned an invalid byte count")
			n = 0
		}
		written += n
		o.size += int64(n)
		if writeErr != nil {
			if restoreErr := o.restoreFailedWriteLocked(startSize); restoreErr != nil {
				o.lastErr = fmt.Errorf("event log write failed: %w; restore failed: %v", writeErr, restoreErr)
				return o.lastErr
			}
			o.lastErr = writeErr
			return writeErr
		}
		if n == 0 {
			noProgressErr := errors.New("event log made no progress")
			if restoreErr := o.restoreFailedWriteLocked(startSize); restoreErr != nil {
				o.lastErr = fmt.Errorf("%w; restore failed: %v", noProgressErr, restoreErr)
				return o.lastErr
			}
			o.lastErr = noProgressErr
			return noProgressErr
		}
	}
	o.completeEventWriteLocked(event)
	return nil
}

func (o *compositeObserver) fail(err error) error {
	if o == nil {
		return err
	}
	o.mu.Lock()
	if o.lastErr == nil {
		o.lastErr = err
	}
	o.mu.Unlock()
	return err
}

func (o *compositeObserver) Err() error {
	if o == nil {
		return errors.New("event observer is unavailable")
	}
	o.mu.Lock()
	defer o.mu.Unlock()
	return o.lastErr
}

func (o *compositeObserver) Close() error {
	if o == nil {
		return nil
	}
	o.mu.Lock()
	defer o.mu.Unlock()
	if o.file == nil {
		return nil
	}
	err := o.file.Close()
	o.file = nil
	return err
}
