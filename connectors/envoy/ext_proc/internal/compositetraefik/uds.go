package compositetraefik

import (
	"bytes"
	"context"
	"crypto/rand"
	"encoding/base64"
	"encoding/binary"
	"errors"
	"fmt"
	"io"
	"net"
	"os"
	"path/filepath"
	"strconv"
	"strings"
	"syscall"
	"time"
	"unicode/utf8"

	"github.com/Easton97-Jens/ModSecurity-conector/connectors/envoy/ext_proc/internal/composite"
	"github.com/Easton97-Jens/ModSecurity-conector/connectors/envoy/ext_proc/internal/processor"
)

const (
	frameSize         = 12
	maxFrame          = 64 << 10
	maxChunk          = 32 << 10
	maxTokenSize      = 256
	maxRedirect       = 4096
	maxHeaderCount    = 256
	maxHeaderBytes    = 64 << 10
	maxHeaderName     = 256
	maxHeaderValue    = 8192
	envoyStatusHeader = ":status"

	opClaim           byte = 1
	opReserve         byte = 8
	opResponseHeaders byte = 2
	opResponseChunk   byte = 3
	opResponseEOS     byte = 4
	opResponseCommit  byte = 5
	opOutcome         byte = 6
	opFinish          byte = 7
	opResult          byte = 128

	decisionAllow    byte = 0
	decisionDeny     byte = 1
	decisionRedirect byte = 2

	// resultFlagRequestTerminal means ForwardAuth recorded a P1/P2 host
	// action. The outer plugin must preserve that exact host response, emit no
	// P3/P4 frames, and finish the retained reservation over this UDS session.
	resultFlagRequestTerminal byte = 1
)

var errMSC2 = errors.New("invalid MSC2 frame")

func newSession() (string, error) {
	b := make([]byte, 32)
	if _, err := rand.Read(b); err != nil {
		return "", err
	}
	return base64.RawURLEncoding.EncodeToString(b), nil
}

// ListenPrivate creates a Unix socket only below an existing operator-owned
// private directory. It never removes or replaces an existing path.
func ListenPrivate(path string) (net.Listener, error) {
	if path == "" || !filepath.IsAbs(path) || filepath.Clean(path) != path || strings.Contains(path, "..") || len(path) > 108 {
		return nil, errors.New("invalid private socket path")
	}
	parent := filepath.Dir(path)
	info, err := os.Lstat(parent)
	if err != nil {
		return nil, errors.New("socket parent is not private")
	}
	st, ok := info.Sys().(*syscall.Stat_t)
	if !ok || info.Mode()&os.ModeSymlink != 0 || !info.IsDir() || info.Mode().Perm()&0077 != 0 || st.Uid != uint32(os.Getuid()) {
		return nil, errors.New("socket parent is not private")
	}
	if _, err := os.Lstat(path); err == nil {
		return nil, errors.New("socket path already exists")
	} else if !os.IsNotExist(err) {
		return nil, err
	}
	l, err := net.Listen("unix", path)
	if err != nil {
		return nil, err
	}
	if err := os.Chmod(path, 0600); err != nil {
		_ = l.Close()
		return nil, err
	}
	return l, nil
}

// UDS serves one bounded MSC2 session per connection. A connection may claim
// exactly one retained coordinator response and cannot be reused for another
// lease, which makes duplicate and cross-request claims deterministic.
type UDS struct {
	Coordinator    *composite.Coordinator
	Timeout        time.Duration
	MaxConnections int
}

func (s *UDS) Serve(l net.Listener) error {
	if s == nil || s.Coordinator == nil || l == nil {
		return errors.New("composite UDS is not configured")
	}
	maxConnections := s.MaxConnections
	if maxConnections <= 0 {
		maxConnections = 128
	}
	if maxConnections > 1024 {
		return errors.New("composite UDS connection limit is too high")
	}
	admission := make(chan struct{}, maxConnections)
	for {
		conn, err := l.Accept()
		if err != nil {
			return err
		}
		select {
		case admission <- struct{}{}:
			go func() { defer func() { <-admission }(); s.handle(conn) }()
		default:
			_ = conn.Close()
		}
	}
}

type udsSession struct {
	svc                   *UDS
	conn                  net.Conn
	response              *composite.Response
	claimed               bool
	requestTerminal       bool
	finished              bool
	session               string
	leaseToken            string
	responseHeaders       bool
	responseCommitted     bool
	responseEOS           bool
	responseChunk         bool
	sawDisruptive         bool
	p3Action              processor.Action
	p4Disruptive          bool
	upstreamStatus        int
	expectedOutcomeStatus int
}

func (s *UDS) handle(conn net.Conn) {
	session, err := newSession()
	if err != nil {
		_ = conn.Close()
		return
	}
	st := &udsSession{svc: s, conn: conn, session: session}
	cleanupReason := "disconnect"
	defer conn.Close()
	defer func() { st.cleanup(context.Background(), cleanupReason) }()
	for {
		if err := st.deadline(context.Background()); err != nil {
			return
		}
		op, payload, err := readFrame(conn)
		if err != nil {
			if isTimeout(err) {
				cleanupReason = "timeout"
			}
			return
		}
		result, terminal := st.dispatch(context.Background(), op, payload)
		clear(payload)
		if err := st.writeResult(context.Background(), op, result); err != nil {
			if isTimeout(err) {
				cleanupReason = "timeout"
			}
			return
		}
		if terminal {
			return
		}
	}
}

func isTimeout(err error) bool {
	var netErr net.Error
	return errors.As(err, &netErr) && netErr.Timeout()
}

func (s *udsSession) deadline(ctx context.Context) error {
	d := time.Now().Add(s.svc.Timeout)
	if s.svc.Timeout <= 0 {
		d = time.Now().Add(5 * time.Second)
	}
	if x, ok := ctx.Deadline(); ok && x.Before(d) {
		d = x
	}
	return s.conn.SetDeadline(d)
}

type wireResult struct {
	decision byte
	status   uint16
	redirect string
	token    string
	flags    byte
}

func (s *udsSession) dispatch(ctx context.Context, op byte, p []byte) (wireResult, bool) {
	result, terminal, handled := s.dispatchControl(ctx, op, p)
	if handled {
		return result, terminal
	}
	result, terminal, d, err := s.dispatchResponse(ctx, op, p)
	if terminal {
		return result, true
	}
	if err != nil {
		return wireResult{decision: decisionDeny, status: 503}, true
	}
	s.applyResponseDecision(op, d)
	return decisionResult(d), false
}

func (s *udsSession) dispatchControl(ctx context.Context, op byte, p []byte) (wireResult, bool, bool) {
	if op == opReserve {
		result, terminal := s.dispatchReserve(p)
		return result, terminal, true
	}
	if op == opClaim {
		result, terminal := s.dispatchClaim(p)
		return result, terminal, true
	}
	if s.requestTerminal {
		if op == opFinish {
			s.cleanup(ctx, "finish")
			return wireResult{}, true, true
		}
		return wireResult{decision: decisionDeny, status: 503}, true, true
	}
	if !s.claimed || s.response == nil || s.finished {
		return wireResult{decision: decisionDeny, status: 503}, true, true
	}
	if op == opOutcome {
		result, terminal := s.dispatchOutcome(ctx, p)
		return result, terminal, true
	}
	if op == opFinish {
		s.cleanup(ctx, "finish")
		return wireResult{}, true, true
	}
	return wireResult{}, false, false
}

func (s *udsSession) applyResponseDecision(op byte, d processor.Decision) {
	if d.Action != processor.ActionAllow {
		s.sawDisruptive = true
		if op == opResponseHeaders {
			s.p3Action = d.Action
		}
		if op == opResponseChunk || op == opResponseEOS {
			s.p4Disruptive = true
		}
	} else if op == opResponseHeaders {
		s.p3Action = processor.ActionAllow
	}
	if op == opResponseHeaders {
		s.responseHeaders = true
		// For a normal response or a late P4 result the host-visible status is
		// the already validated upstream P3 status. For a P3 replacement it is
		// the status the host was instructed to emit in decisionResult(d), never
		// an arbitrary plugin-supplied value.
		if d.Action == processor.ActionAllow {
			s.expectedOutcomeStatus = s.upstreamStatus
		} else {
			s.expectedOutcomeStatus = int(decisionResult(d).status)
		}
	}
}

func (s *udsSession) dispatchResponse(ctx context.Context, op byte, p []byte) (wireResult, bool, processor.Decision, error) {
	var d processor.Decision
	var err error
	switch op {
	case opResponseHeaders:
		if s.responseHeaders || s.responseCommitted || s.responseEOS {
			return wireResult{decision: decisionDeny, status: 409}, true, d, nil
		}
		h, parseErr := parseResponseHeaders(p)
		if parseErr != nil {
			return wireResult{decision: decisionDeny, status: 503}, true, d, nil
		}
		d, err = s.response.Headers(ctx, h, false)
		s.upstreamStatus = headerStatus(h)
	case opResponseChunk:
		if !s.responseHeaders || !s.responseCommitted || s.responseEOS {
			return wireResult{decision: decisionDeny, status: 409}, true, d, nil
		}
		if len(p) > maxChunk {
			return wireResult{decision: decisionDeny, status: 503}, true, d, nil
		}
		d, err = s.response.Body(ctx, p, false)
		s.responseChunk = true
	case opResponseEOS:
		if !s.responseHeaders || !s.responseCommitted || s.responseEOS {
			return wireResult{decision: decisionDeny, status: 409}, true, d, nil
		}
		d, err = s.response.Body(ctx, nil, true)
		s.responseEOS = true
	case opResponseCommit:
		if !s.responseHeaders || s.responseCommitted || s.responseEOS {
			return wireResult{decision: decisionDeny, status: 409}, true, d, nil
		}
		if len(p) != 2 || p[0] != 1 || p[1] != 0 {
			return wireResult{decision: decisionDeny, status: 400}, true, d, nil
		}
		committer, ok := any(s.response).(interface{ MarkResponseCommitted(context.Context) error })
		if !ok {
			return wireResult{decision: decisionDeny, status: 503}, true, d, nil
		}
		err = committer.MarkResponseCommitted(ctx)
		s.responseCommitted = err == nil
		d = processor.Decision{Action: processor.ActionAllow}
	default:
		return wireResult{decision: decisionDeny, status: 400}, true, d, nil
	}
	return wireResult{}, false, d, err
}

func (s *udsSession) dispatchOutcome(ctx context.Context, p []byte) (wireResult, bool) {
	if !s.validOutcomeShape(p) || !s.outcomeStatusMatches(p[0], int(binary.BigEndian.Uint16(p[1:]))) {
		return wireResult{decision: decisionDeny, status: 409}, true
	}
	if err := s.recordOutcome(ctx, p); err != nil {
		return wireResult{decision: decisionDeny, status: 503}, true
	}
	return wireResult{}, false
}

func (s *udsSession) validOutcomeShape(p []byte) bool {
	if len(p) != 3 || (s.responseCommitted && !s.responseEOS) || (!s.responseCommitted && p[0] != 1 && p[0] != 2) || (s.responseCommitted && (p[0] == 1 || p[0] == 2)) {
		return false
	}
	if p[0] == 0 && (s.p3Action != processor.ActionAllow || s.p4Disruptive) {
		return false
	}
	if (p[0] == 1 || p[0] == 2) && (s.responseCommitted || s.p3Action == processor.ActionAllow || (p[0] == 1 && s.p3Action != processor.ActionDeny) || (p[0] == 2 && s.p3Action != processor.ActionRedirect)) {
		return false
	}
	return p[0] != 3 || s.p4Disruptive
}

func (s *udsSession) dispatchReserve(p []byte) (wireResult, bool) {
	if s.leaseToken != "" {
		return wireResult{decision: decisionDeny, status: 409}, true
	}
	snapshot, err := parseReservationSnapshot(p)
	if err != nil {
		return wireResult{decision: decisionDeny, status: 503}, true
	}
	defer wipeParsedHeaders(snapshot.Headers)
	token, err := s.svc.Coordinator.Reserve(s.session, snapshot)
	if err != nil {
		return wireResult{decision: decisionDeny, status: 503}, true
	}
	s.leaseToken = token
	return wireResult{token: token}, false
}

func (s *udsSession) dispatchClaim(p []byte) (wireResult, bool) {
	if s.claimed {
		return wireResult{decision: decisionDeny, status: 409}, true
	}
	token, err := parseToken(p)
	if err != nil || s.leaseToken == "" || token != s.leaseToken {
		return wireResult{decision: decisionDeny, status: 503}, true
	}
	resp, err := s.svc.Coordinator.Claim(token, s.session)
	if err == nil {
		s.response, s.claimed = resp, true
		return wireResult{}, false
	}
	if errors.Is(err, composite.ErrNotAllowed) {
		s.requestTerminal = true
		return wireResult{flags: resultFlagRequestTerminal}, false
	}
	return wireResult{decision: decisionDeny, status: 503}, true
}

func (s *udsSession) recordOutcome(ctx context.Context, p []byte) error {
	if len(p) != 3 {
		return errMSC2
	}
	status := int(binary.BigEndian.Uint16(p[1:]))
	if status < 200 || status > 599 {
		return errMSC2
	}
	if p[0] == 0 {
		neutral, ok := any(s.response).(interface {
			RecordNeutralOutcome(context.Context, int, string) error
		})
		if !ok {
			return errors.New("neutral outcome recorder unavailable")
		}
		return neutral.RecordNeutralOutcome(ctx, status, "response_completed")
	}
	action := processor.AppliedActionLogOnly
	switch p[0] {
	case 1:
		action = processor.AppliedActionDeny
	case 2:
		action = processor.AppliedActionRedirect
	case 3:
		action = processor.AppliedActionLogOnly
	default:
		return errMSC2
	}
	recorder, ok := any(s.response).(interface {
		RecordHostAction(context.Context, processor.HostAction) error
	})
	if !ok {
		return errors.New("host action recorder unavailable")
	}
	transport := commonTransportHTTPStatus
	if action == processor.AppliedActionLogOnly {
		transport = commonTransportLogOnly
	}
	return recorder.RecordHostAction(ctx, processor.HostAction{Action: action, VisibleStatus: status, TransportResult: transport})
}

func (s *udsSession) outcomeStatusMatches(action byte, status int) bool {
	if status < 200 || status > 599 || s.expectedOutcomeStatus < 200 || s.expectedOutcomeStatus > 599 {
		return false
	}
	// action 0 (ordinary completion) and action 3 (late log-only) retain the
	// upstream response status. Actions 1/2 confirm the replacement response
	// selected from the P3 Common decision, which may intentionally differ.
	switch action {
	case 0, 1, 2, 3:
		return status == s.expectedOutcomeStatus
	default:
		return false
	}
}

func headerStatus(headers []processor.Header) int {
	for _, h := range headers {
		if h.Name != ":status" {
			continue
		}
		status, err := strconv.Atoi(string(h.Value))
		if err == nil && status >= 200 && status <= 599 {
			return status
		}
		return 0
	}
	return 0
}

func (s *udsSession) cleanup(ctx context.Context, reason string) {
	if s.finished {
		return
	}
	s.finished = true
	if s.response != nil {
		s.response.Finish(ctx, reason)
	} else if s.leaseToken != "" {
		_ = s.svc.Coordinator.AbortWithReason(s.leaseToken, s.session, reason)
	}
}

func (s *udsSession) writeResult(ctx context.Context, op byte, r wireResult) error {
	_ = ctx
	if r.flags != 0 && (op != opClaim || r.flags != resultFlagRequestTerminal || r.decision != decisionAllow || r.status != 0 || r.redirect != "") {
		return errMSC2
	}
	value := r.redirect
	limit := maxRedirect
	if op == opReserve {
		value = r.token
		limit = maxTokenSize
	}
	if len(value) > limit || !utf8.ValidString(value) || strings.ContainsAny(value, "\r\n") {
		return errMSC2
	}
	p := make([]byte, 8+len(value))
	p[0], p[1], p[2], p[3] = op, 0, r.decision, r.flags
	binary.BigEndian.PutUint16(p[4:6], r.status)
	binary.BigEndian.PutUint16(p[6:8], uint16(len(value)))
	copy(p[8:], value)
	return writeFrame(s.conn, opResult, p)
}

func decisionResult(d processor.Decision) wireResult {
	r := wireResult{}
	if d.Action == processor.ActionAllow {
		return r
	}
	r.status = uint16(d.Status)
	if d.Action == processor.ActionRedirect {
		if r.status < 300 || r.status > 399 {
			r.status = 302
		}
		r.decision, r.redirect = decisionRedirect, d.RedirectURL
	} else {
		if r.status < 400 || r.status > 599 {
			r.status = 403
		}
		r.decision = decisionDeny
	}
	return r
}

func readFrame(r io.Reader) (byte, []byte, error) {
	h := make([]byte, frameSize)
	if _, err := io.ReadFull(r, h); err != nil {
		return 0, nil, err
	}
	if string(h[:4]) != "MSC2" || h[4] != 1 || h[6] != 0 || h[7] != 0 || h[5] == opResult {
		return 0, nil, errMSC2
	}
	n := binary.BigEndian.Uint32(h[8:12])
	if n > maxFrame {
		return 0, nil, errMSC2
	}
	p := make([]byte, n)
	if _, err := io.ReadFull(r, p); err != nil {
		return 0, nil, err
	}
	return h[5], p, nil
}

func writeFrame(w io.Writer, op byte, p []byte) error {
	if len(p) > maxFrame {
		return errMSC2
	}
	h := make([]byte, frameSize)
	copy(h[:4], "MSC2")
	h[4] = 1
	h[5] = op
	binary.BigEndian.PutUint32(h[8:12], uint32(len(p)))
	if err := writeFull(w, h); err != nil {
		return err
	}
	return writeFull(w, p)
}

func writeFull(w io.Writer, p []byte) error {
	for len(p) > 0 {
		n, err := w.Write(p)
		if err != nil {
			return err
		}
		if n <= 0 || n > len(p) {
			return io.ErrShortWrite
		}
		p = p[n:]
	}
	return nil
}

func parseToken(p []byte) (string, error) {
	if len(p) < 2 {
		return "", errMSC2
	}
	n := int(binary.BigEndian.Uint16(p[:2]))
	if n == 0 || n > maxTokenSize || len(p) != n+2 || !utf8.Valid(p[2:]) {
		return "", errMSC2
	}
	return string(p[2:]), nil
}

// parseReservationSnapshot decodes the private opReserve payload. The wire
// format is versioned and length-delimited:
//
//	version(1), methodLen(2), method, uriLen(2), uri, headerGroups(2),
//	repeated nameLen(2), lower-case-name, valueCount(2), repeated
//	valueLen(2), value.
//
// Header groups are strictly sorted by canonical lower-case name. Values are
// retained as individual fields, never comma-joined. Every length and count
// is checked before allocation so malformed private-peer input cannot retain
// unbounded memory or create an ambiguous P1 snapshot.
func parseReservationSnapshot(p []byte) (composite.ReservationSnapshot, error) {
	if len(p) < 7 || len(p) > maxFrame || p[0] != composite.ReservationSnapshotVersion {
		return composite.ReservationSnapshot{}, errMSC2
	}
	i := 1
	method, next, err := reservationText(p, i, 256)
	if err != nil || !validHeaderName(method) {
		return composite.ReservationSnapshot{}, errMSC2
	}
	i = next
	uri, next, err := reservationText(p, i, maxHeaderBytes)
	if err != nil || !validReservationURI(uri) {
		return composite.ReservationSnapshot{}, errMSC2
	}
	i = next
	if i+2 > len(p) {
		return composite.ReservationSnapshot{}, errMSC2
	}
	groups := int(binary.BigEndian.Uint16(p[i : i+2]))
	i += 2
	if groups > maxHeaderCount {
		return composite.ReservationSnapshot{}, errMSC2
	}
	headers, next, hostValues, err := parseReservationGroups(p, i, groups)
	if err != nil {
		return composite.ReservationSnapshot{}, errMSC2
	}
	i = next
	if i != len(p) || hostValues != 1 {
		wipeParsedHeaders(headers)
		return composite.ReservationSnapshot{}, errMSC2
	}
	return composite.ReservationSnapshot{Version: composite.ReservationSnapshotVersion, Method: method, URI: uri, Headers: headers}, nil
}

func parseReservationGroups(p []byte, offset, groups int) ([]processor.Header, int, int, error) {
	headers := make([]processor.Header, 0, groups)
	lastName := ""
	hostValues := 0
	total := 0
	for group := 0; group < groups; group++ {
		name, next, values, nextTotal, nextHeaders, err := parseReservationGroup(p, offset, lastName, total, headers)
		if err != nil {
			wipeParsedHeaders(nextHeaders)
			return nil, 0, 0, errMSC2
		}
		offset, total, headers = next, nextTotal, nextHeaders
		if name == "host" {
			hostValues += values
		}
		lastName = name
	}
	return headers, offset, hostValues, nil
}

func parseReservationGroup(p []byte, offset int, lastName string, total int, headers []processor.Header) (string, int, int, int, []processor.Header, error) {
	name, next, err := reservationText(p, offset, maxHeaderName)
	if err != nil || name != strings.ToLower(name) || !validHeaderName(name) ||
		(lastName != "" && name <= lastName) || internalSnapshotHeader(name) {
		return "", 0, 0, total, headers, errMSC2
	}
	if next+2 > len(p) {
		return "", 0, 0, total, headers, errMSC2
	}
	values := int(binary.BigEndian.Uint16(p[next : next+2]))
	next += 2
	if values == 0 || values > maxHeaderCount-len(headers) {
		return "", 0, 0, total, headers, errMSC2
	}
	for valueIndex := 0; valueIndex < values; valueIndex++ {
		value, valueNext, valueErr := reservationBytes(p, next, maxHeaderValue)
		if valueErr != nil || invalidReservationValue(value) {
			return "", 0, 0, total, headers, errMSC2
		}
		next = valueNext
		total += len(name) + len(value)
		if total > maxHeaderBytes {
			return "", 0, 0, total, headers, errMSC2
		}
		headers = append(headers, processor.Header{Name: name, Value: append([]byte(nil), value...)})
	}
	return name, next, values, total, headers, nil
}

func reservationText(p []byte, offset, max int) (string, int, error) {
	value, next, err := reservationBytes(p, offset, max)
	if err != nil || !utf8.Valid(value) || bytes.IndexByte(value, '\r') >= 0 || bytes.IndexByte(value, '\n') >= 0 || bytes.IndexByte(value, 0) >= 0 {
		return "", 0, errMSC2
	}
	return string(value), next, nil
}

func reservationBytes(p []byte, offset, max int) ([]byte, int, error) {
	if offset+2 > len(p) {
		return nil, 0, errMSC2
	}
	n := int(binary.BigEndian.Uint16(p[offset : offset+2]))
	next := offset + 2 + n
	if n == 0 || n > max || next > len(p) {
		return nil, 0, errMSC2
	}
	return p[offset+2 : next], next, nil
}

func validReservationURI(uri string) bool {
	return len(uri) <= maxHeaderBytes && strings.HasPrefix(uri, "/") && !strings.ContainsAny(uri, "\r\n\x00")
}

func invalidReservationValue(value []byte) bool {
	return bytes.IndexByte(value, '\r') >= 0 || bytes.IndexByte(value, '\n') >= 0 || bytes.IndexByte(value, 0) >= 0
}

func internalSnapshotHeader(name string) bool {
	return strings.EqualFold(name, LeaseHeader) || strings.EqualFold(name, "X-Msconnector-Composite-Request-Context")
}

func wipeParsedHeaders(headers []processor.Header) {
	for i := range headers {
		clear(headers[i].Value)
		headers[i].Value = nil
		headers[i].Name = ""
	}
}

func parseResponseHeaders(p []byte) ([]processor.Header, error) {
	if len(p) < 6 {
		return nil, errMSC2
	}
	status := int(binary.BigEndian.Uint16(p[:2]))
	if status < 200 || status > 599 {
		return nil, errMSC2
	}
	protoLen := int(binary.BigEndian.Uint16(p[2:4]))
	i := 4 + protoLen
	if protoLen == 0 || i+2 > len(p) || !utf8.Valid(p[4:i]) {
		return nil, errMSC2
	}
	n := int(binary.BigEndian.Uint16(p[i : i+2]))
	i += 2
	if n > maxHeaderCount {
		return nil, errMSC2
	}
	h := make([]processor.Header, 0, n+1)
	statusValue := []byte(strconv.Itoa(status))
	h = append(h, processor.Header{Name: envoyStatusHeader, Value: statusValue})
	total := len(envoyStatusHeader) + len(statusValue) + 4
	var err error
	h, i, err = parseResponseHeaderList(p, i, n, h, total)
	if err != nil {
		return nil, errMSC2
	}
	if i != len(p) {
		return nil, fmt.Errorf("%w: trailing header data", errMSC2)
	}
	return h, nil
}

func parseResponseHeaderList(p []byte, offset, count int, headers []processor.Header, total int) ([]processor.Header, int, error) {
	for i := 0; i < count; i++ {
		header, next, headerSize, err := parseResponseHeader(p, offset)
		if err != nil {
			return nil, 0, errMSC2
		}
		offset = next
		total += headerSize
		if total > maxHeaderBytes {
			return nil, 0, errMSC2
		}
		headers = append(headers, header)
	}
	return headers, offset, nil
}

func parseResponseHeader(p []byte, offset int) (processor.Header, int, int, error) {
	if offset+2 > len(p) {
		return processor.Header{}, 0, 0, errMSC2
	}
	nameLen := int(binary.BigEndian.Uint16(p[offset : offset+2]))
	i := offset + 2
	if nameLen == 0 || i+nameLen+2 > len(p) {
		return processor.Header{}, 0, 0, errMSC2
	}
	name := p[i : i+nameLen]
	i += nameLen
	valueLen := int(binary.BigEndian.Uint16(p[i : i+2]))
	i += 2
	if i+valueLen > len(p) || !utf8.Valid(name) || !utf8.Valid(p[i:i+valueLen]) {
		return processor.Header{}, 0, 0, errMSC2
	}
	value := p[i : i+valueLen]
	if !validHeaderName(string(name)) || bytes.IndexByte(value, '\r') >= 0 || bytes.IndexByte(value, '\n') >= 0 {
		return processor.Header{}, 0, 0, errMSC2
	}
	return processor.Header{Name: string(name), Value: append([]byte(nil), value...)}, i + valueLen, nameLen + valueLen + 4, nil
}

func validHeaderName(s string) bool {
	if s == "" {
		return false
	}
	for i := 0; i < len(s); i++ {
		c := s[i]
		if (c >= 'a' && c <= 'z') || (c >= 'A' && c <= 'Z') || (c >= '0' && c <= '9') {
			continue
		}
		if !strings.ContainsRune("!#$%&'*+-.^_`|~", rune(c)) {
			return false
		}
	}
	return true
}
