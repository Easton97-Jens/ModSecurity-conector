// Package response_observer is a response-only Traefik middleware. It
// consumes the opaque handle emitted by the preceding forwardAuth middleware
// and talks to the canonical C runtime over one private UDS session.
package response_observer

import (
	"bufio"
	"context"
	"encoding/binary"
	"encoding/hex"
	"errors"
	"io"
	"net"
	"net/http"
	"path/filepath"
	"strings"
	"sync"
	"time"
)

const (
	// MRC1 magic family, protocol version 2.  No v1 fallback is allowed
	// because v1 cannot represent typed terminal causes safely.
	protocolVersion          = byte(2)
	frameHeaderSize          = 12
	maxPayload               = 65536
	maxBodyChunk             = 32768
	maxHeaderCount           = 256
	maxHeaderName            = 256
	maxHeaderValue           = 8192
	maxResponseHeaderPayload = maxPayload + 2 + 2 + len("HTTP/1.1") + 2 +
		4*maxHeaderCount
	defaultTimeout    = 5 * time.Second
	opClaim           = byte(1)
	opResponseHeaders = byte(2)
	opResponseBody    = byte(3)
	opResponseEOS     = byte(4)
	opCommit          = byte(5)
	opCancel          = byte(6)
	opRelease         = byte(7)
	opOutcome         = byte(8)
	// CANCEL payload values are canonical cleanup causes. The common runtime
	// consumes these values; they are deliberately not a boolean because a
	// peer close is otherwise indistinguishable from an upstream disconnect.
	cancelClientCancel       = byte(0)
	cancelUpstreamDisconnect = byte(1)
	cancelConnectorError     = byte(2)
	cancelProtocolError      = byte(3)
	cancelEngineTimeout      = byte(4)
	cancelEngineUnavailable  = byte(5)
	cancelInvalidEngine      = byte(6)
	opResult                 = byte(128)
	decisionAllow            = byte(0)
	decisionLogOnly          = byte(1)
	decisionDeny             = byte(2)
	decisionRedirect         = byte(3)
	decisionDrop             = byte(4)
	decisionAbort            = byte(5)
	decisionError            = byte(6)
	decisionUnsupported      = byte(7)
	outcomeAllow             = byte(0)
	outcomeDeny              = byte(1)
	outcomeRedirect          = byte(2)
	outcomeDrop              = byte(3)
	outcomeLogOnly           = byte(4)
	outcomeAbort             = byte(5)
	outcomeStreamReset       = byte(6)
	outcomeError             = byte(7)
	outcomeUnsupported       = byte(8)
	outcomeRateLimit         = byte(9)
	resultOK                 = byte(0)
	resultError              = byte(1)
)

var (
	errProtocol = errors.New("modsecurity response observer: invalid private UDS protocol")
	errClosed   = errors.New("modsecurity response observer: session closed")
)

// Config is the host-facing configuration. SocketPath is deliberately UDS
// only; no TCP or implicit fallback is supported.
type Config struct {
	SocketPath    string `json:"socketPath,omitempty"`
	TimeoutMillis int    `json:"timeoutMillis,omitempty"`
}

func CreateConfig() *Config {
	return &Config{SocketPath: "/run/modsecurity/traefik-forwardauth-companion.sock", TimeoutMillis: 5000}
}

func normalizeConfig(input *Config) (Config, error) {
	if input == nil {
		return Config{}, errors.New("modsecurity response observer: config is required")
	}
	c := *input
	if c.SocketPath == "" {
		c.SocketPath = CreateConfig().SocketPath
	}
	if c.TimeoutMillis == 0 {
		c.TimeoutMillis = 5000
	}
	if !safeSocketPath(c.SocketPath) || c.TimeoutMillis < 1 || c.TimeoutMillis > 60000 {
		return Config{}, errors.New("modsecurity response observer: invalid private socket or timeout")
	}
	return c, nil
}

func safeSocketPath(path string) bool {
	return filepath.IsAbs(path) && filepath.Clean(path) == path &&
		strings.ContainsRune(path, 0) == false
}

// New constructs the Traefik middleware handler.
func New(_ context.Context, next http.Handler, config *Config, _ string) (http.Handler, error) {
	if next == nil {
		return nil, errors.New("modsecurity response observer: next handler is required")
	}
	c, err := normalizeConfig(config)
	if err != nil {
		return nil, err
	}
	return &middleware{next: next, config: c}, nil
}

type middleware struct {
	next   http.Handler
	config Config
}

func (m *middleware) ServeHTTP(writer http.ResponseWriter, request *http.Request) {
	handles := request.Header.Values("X-Msconnector-Response-Handle")
	if len(handles) != 1 || !validHandle(handles[0]) {
		http.Error(writer, "response observer handle required", http.StatusServiceUnavailable)
		return
	}
	request.Header.Del("X-Msconnector-Response-Handle")
	session, err := openSession(request.Context(), m.config, handles[0])
	if err != nil {
		http.Error(writer, "response observer unavailable", http.StatusServiceUnavailable)
		return
	}
	defer session.close()
	state := &responseState{session: session, target: writer, request: request}
	completed := false
	defer func() {
		if !completed {
			/* An escaping handler panic or Goexit leaves the upstream response
			 * incomplete.  Do not synthesize P3/COMMIT/EOS/release; preserve the
			 * abnormal control flow after bounded typed cleanup instead. */
			if !state.finished && !state.precommitFail {
				_ = state.cancelWithClass(cancelConnectorError)
			}
			state.finished = true
			return
		}
		state.finish()
	}()
	m.next.ServeHTTP(state, request)
	completed = true
}

func validHandle(handle string) bool {
	if len(handle) != 64 {
		return false
	}
	for _, c := range handle {
		if !((c >= '0' && c <= '9') || (c >= 'a' && c <= 'f')) {
			return false
		}
	}
	_, err := hex.DecodeString(handle)
	return err == nil
}

type session struct {
	mu      sync.Mutex
	conn    net.Conn
	reader  *bufio.Reader
	timeout time.Duration
	closed  bool
}

func maxPayloadForOpcode(opcode byte) int {
	if opcode == opResponseHeaders {
		return maxResponseHeaderPayload
	}
	return maxPayload
}

func openSession(ctx context.Context, config Config, handle string) (*session, error) {
	dialer := net.Dialer{Timeout: time.Duration(config.TimeoutMillis) * time.Millisecond}
	conn, err := dialer.DialContext(ctx, "unix", config.SocketPath)
	if err != nil {
		return nil, err
	}
	s := &session{conn: conn, reader: bufio.NewReader(conn), timeout: time.Duration(config.TimeoutMillis) * time.Millisecond}
	claim, err := s.exchange(ctx, opClaim, []byte(handle))
	if err != nil {
		_ = conn.Close()
		return nil, err
	}
	if claim.requestOpcode != opClaim || claim.code != resultOK {
		_ = conn.Close()
		return nil, errors.New("modsecurity response observer: handle claim rejected")
	}
	return s, nil
}

func (s *session) exchange(ctx context.Context, opcode byte, payload []byte) (result, error) {
	s.mu.Lock()
	defer s.mu.Unlock()
	if s.closed || len(payload) > maxPayloadForOpcode(opcode) {
		return result{}, errProtocol
	}
	if err := ctx.Err(); err != nil {
		return result{}, err
	}
	watchDone := make(chan struct{})
	if ctx.Done() != nil {
		go func() {
			select {
			case <-ctx.Done():
				// Interrupt a blocked read/write promptly. The caller will use
				// the bounded cleanup context to send CANCEL.
				_ = s.conn.SetDeadline(time.Now())
			case <-watchDone:
			}
		}()
		defer close(watchDone)
	}
	deadline := time.Now().Add(s.timeout)
	if contextDeadline, ok := ctx.Deadline(); ok && contextDeadline.Before(deadline) {
		deadline = contextDeadline
	}
	if err := s.conn.SetDeadline(deadline); err != nil {
		return result{}, err
	}
	if err := writeFrame(s.conn, opcode, payload); err != nil {
		return result{}, err
	}
	value, err := readResult(s.reader)
	if err != nil {
		return result{}, err
	}
	if value.requestOpcode != opcode {
		return result{}, errProtocol
	}
	return value, nil
}

func writeFrame(writer io.Writer, opcode byte, payload []byte) error {
	if len(payload) > maxPayloadForOpcode(opcode) {
		return errProtocol
	}
	header := make([]byte, frameHeaderSize)
	copy(header[:4], []byte("MRC1"))
	header[4] = protocolVersion
	header[5] = opcode
	binary.BigEndian.PutUint32(header[8:], uint32(len(payload)))
	if err := writeFull(writer, header); err != nil {
		return err
	}
	return writeFull(writer, payload)
}

func writeFull(writer io.Writer, payload []byte) error {
	for len(payload) > 0 {
		written, err := writer.Write(payload)
		if written > 0 {
			payload = payload[written:]
		}
		if err != nil {
			return err
		}
		if written == 0 {
			return io.ErrShortWrite
		}
	}
	return nil
}

type result struct {
	requestOpcode byte
	code          byte
	decision      byte
	errorCode     uint16
	status        int
	redirect      string
	rule          string
}

func readResult(reader *bufio.Reader) (result, error) {
	header := make([]byte, frameHeaderSize)
	if _, err := io.ReadFull(reader, header); err != nil {
		return result{}, err
	}
	if !validResultHeader(header) {
		return result{}, errProtocol
	}
	length := binary.BigEndian.Uint32(header[8:])
	if length > maxPayload || length < 12 {
		return result{}, errProtocol
	}
	payload := make([]byte, length)
	if _, err := io.ReadFull(reader, payload); err != nil {
		return result{}, err
	}
	if !validResultPayload(payload) {
		return result{}, errProtocol
	}
	errorCode := binary.BigEndian.Uint16(payload[6:])
	status := int(binary.BigEndian.Uint16(payload[4:]))
	redirectLen := int(binary.BigEndian.Uint16(payload[8:]))
	return result{requestOpcode: payload[0], code: payload[1], decision: payload[2], errorCode: errorCode, status: status, redirect: string(payload[12 : 12+redirectLen]), rule: string(payload[12+redirectLen:])}, nil
}

func validResultHeader(header []byte) bool {
	return len(header) == frameHeaderSize && string(header[:4]) == "MRC1" &&
		header[4] == protocolVersion && header[5] == opResult &&
		header[6] == 0 && header[7] == 0
}

func validResultPayload(payload []byte) bool {
	if len(payload) < 12 || payload[3] != 0 || payload[1] > resultError ||
		payload[2] > decisionUnsupported {
		return false
	}
	errorCode := binary.BigEndian.Uint16(payload[6:])
	if (payload[1] == resultOK && errorCode != 0) ||
		(payload[1] != resultOK && errorCode == 0) {
		return false
	}
	status := int(binary.BigEndian.Uint16(payload[4:]))
	if payload[1] == resultOK && !validSuccessfulResultStatus(payload[0],
		payload[2], status) {
		return false
	}
	redirectLen := int(binary.BigEndian.Uint16(payload[8:]))
	ruleLen := int(binary.BigEndian.Uint16(payload[10:]))
	if 12+redirectLen+ruleLen != len(payload) ||
		redirectLen > maxHeaderValue || ruleLen > maxHeaderValue {
		return false
	}
	return validRedirectResult(payload[2], status, redirectLen) &&
		validResultText(payload[12:12+redirectLen]) &&
		validResultText(payload[12+redirectLen:])
}

func validResultText(value []byte) bool {
	for _, character := range value {
		if character < 0x20 || character == 0x7f {
			return false
		}
	}
	return true
}

func validRedirectResult(decision byte, status, redirectLen int) bool {
	if decision == decisionRedirect {
		return status >= 300 && status <= 399 && redirectLen != 0
	}
	return redirectLen == 0
}

func validSuccessfulResultStatus(operation, decision byte, status int) bool {
	if status >= 100 && status <= 599 {
		return true
	}
	/* MRC1 uses a statusless ERROR decision for successful cleanup ACKs that
	 * deliberately carry no engine decision.  Accept it only for CANCEL and
	 * RELEASE; accepting it for P1--P4 would turn an invalid engine response
	 * into a local success.  This matches the Envoy observer's MRC1 parser. */
	if (operation == opCancel || operation == opRelease) && decision == decisionError {
		return status == 0
	}
	return status == 0 && (decision == decisionAllow ||
		decision == decisionLogOnly || decision == decisionDrop ||
		decision == decisionAbort)
}

func (s *session) close() {
	s.mu.Lock()
	defer s.mu.Unlock()
	if !s.closed {
		s.closed = true
		_ = s.conn.Close()
	}
}

type responseState struct {
	session                                          *session
	target                                           http.ResponseWriter
	request                                          *http.Request
	status                                           int
	headerSent, bodyStarted, finished, precommitFail bool
}

func (s *responseState) Header() http.Header { return s.target.Header() }

func (s *responseState) WriteHeader(status int) {
	if s.headerSent || s.finished {
		return
	}
	payload := encodeResponseHeaders(status, s.target.Header())
	if payload == nil || status < 100 || status > 999 {
		s.failBeforeCommit()
		return
	}
	if status == http.StatusSwitchingProtocols {
		// The observer has no safe upgrade handoff and cannot provide P4 once
		// the protocol switches.  Reject it before any upstream bytes commit.
		s.failBeforeCommit()
		return
	}
	if status >= 100 && status < 200 {
		// The canonical contract has exactly one P3 for the final response.
		// Preserve bounded header validation above, but let informational
		// responses pass through without consuming P3 or COMMIT state.
		s.target.WriteHeader(status)
		return
	}
	decision, err := s.session.exchange(s.request.Context(), opResponseHeaders, payload)
	if err != nil || decision.code != resultOK {
		s.failBeforeCommit()
		return
	}
	if disruptive(decision.decision) {
		s.applyImmediate(decision)
		return
	}
	commit, err := s.session.exchange(s.request.Context(), opCommit, []byte{1, 0})
	if err != nil {
		s.failBeforeCommit()
		return
	}
	if commit.code != resultOK {
		s.failBeforeCommit()
		return
	}
	if disruptive(commit.decision) {
		s.applyImmediate(commit)
		return
	}
	s.target.WriteHeader(status)
	s.status = status
	s.headerSent = true
}

func (s *responseState) Write(payload []byte) (int, error) {
	totalWritten := 0
	if s.finished {
		return 0, errClosed
	}
	/* A pre-commit P3 decision already produced the terminal client response.
	 * ReverseProxy may still write the upstream body after its WriteHeader call;
	 * consume that body without forwarding it so an ordinary policy denial does
	 * not become a transport reset. */
	if s.precommitFail {
		return len(payload), nil
	}
	if !s.headerSent {
		s.WriteHeader(http.StatusOK)
	}
	if s.precommitFail {
		// WriteHeader may have materialized a terminal P3 decision for an
		// implicit Write(200, body). The downstream body is already consumed
		// by the terminal response and must not be reported as a write failure.
		return len(payload), nil
	}
	for len(payload) > 0 {
		chunk := payload
		if len(chunk) > maxBodyChunk {
			chunk = chunk[:maxBodyChunk]
		}
		decision, err := s.session.exchange(s.request.Context(), opResponseBody, chunk)
		if err != nil {
			_ = s.cancelFailure(err)
			s.finished = true
			return totalWritten, err
		}
		if decision.code != resultOK {
			_ = s.cancelWithClass(cancelInvalidEngine)
			s.finished = true
			return totalWritten, errProtocol
		}
		if disruptive(decision.decision) {
			if err := s.sendLateOutcome(s.status); err != nil {
				_ = s.cancelFailure(err)
				s.finished = true
				return totalWritten, err
			}
		}
		written, writeErr := s.target.Write(chunk)
		s.bodyStarted = s.bodyStarted || written > 0
		totalWritten += written
		if writeErr != nil {
			_ = s.cancel(false)
			s.finished = true
			return totalWritten, writeErr
		}
		if written != len(chunk) {
			_ = s.cancel(false)
			s.finished = true
			return totalWritten, io.ErrShortWrite
		}
		payload = payload[len(chunk):]
	}
	return totalWritten, nil
}

func (s *responseState) Flush() {
	if !s.headerSent {
		s.WriteHeader(http.StatusOK)
	}
	if flusher, ok := s.target.(http.Flusher); ok {
		flusher.Flush()
	}
}

func (s *responseState) finish() {
	if s.finished {
		return
	}
	if s.precommitFail {
		s.finished = true
		return
	}
	if !s.headerSent {
		s.WriteHeader(http.StatusOK)
		if s.precommitFail {
			s.finished = true
			return
		}
	}
	eos, err := s.session.exchange(s.request.Context(), opResponseEOS, nil)
	if err != nil {
		_ = s.cancelFailure(err)
		s.finished = true
		return
	}
	if eos.code != resultOK {
		_ = s.cancelWithClass(cancelInvalidEngine)
		s.finished = true
		return
	}
	if disruptive(eos.decision) {
		if err := s.sendLateOutcome(s.status); err != nil {
			_ = s.cancelFailure(err)
			s.finished = true
			return
		}
	}
	release, err := s.session.exchange(s.request.Context(), opRelease, nil)
	if err != nil || release.code != resultOK {
		if err != nil {
			_ = s.cancelFailure(err)
		} else {
			_ = s.cancelWithClass(cancelInvalidEngine)
		}
	}
	s.finished = true
}

func (s *responseState) failBeforeCommit() {
	if s.headerSent || s.precommitFail {
		return
	}
	s.precommitFail = true
	if s.request != nil && s.request.Context().Err() != nil {
		// The request context is the authoritative client-cancel signal.
		_ = s.cancel(false)
	} else {
		_ = s.cancelWithClass(cancelConnectorError)
	}
	s.writeTerminalStatus(http.StatusServiceUnavailable)
}

/* writeTerminalStatus replaces the upstream response before its headers have
 * committed. In particular, a copied upstream Content-Length must not survive
 * after Write discards the upstream body, or net/http will turn the intended
 * deterministic denial into an incomplete downstream response. */
func (s *responseState) writeTerminalStatus(status int) {
	location := ""
	if status >= 300 && status <= 399 {
		candidate := s.target.Header().Get("Location")
		if validRedirect(candidate) {
			location = candidate
		}
	}
	// The upstream response is no longer being forwarded. Clear every
	// precommit header so cookies, auth challenges, internal handles, and
	// other upstream metadata cannot escape on a terminal observer response.
	for name := range s.target.Header() {
		s.target.Header().Del(name)
	}
	if location != "" {
		s.target.Header().Set("Location", location)
	}
	s.target.WriteHeader(status)
}

func (s *responseState) applyImmediate(value result) {
	status := value.status
	actualDecision := value.decision
	if value.decision == decisionRedirect {
		if status < 300 || status > 399 || !validRedirect(value.redirect) {
			s.failBeforeCommit()
			return
		}
	} else if value.decision == decisionDeny {
		if status < 400 || status > 499 {
			status = http.StatusForbidden
		}
	} else if value.decision == decisionDrop || value.decision == decisionAbort {
		/* net/http's ResponseWriter offers no demonstrated connection-abort
		 * primitive. Record the actual pre-commit action as an explicit HTTP
		 * deny rather than claiming an abort while returning a status response. */
		actualDecision = decisionDeny
		status = http.StatusServiceUnavailable
	} else {
		s.failBeforeCommit()
		return
	}
	s.precommitFail = true
	if value.decision == decisionRedirect && value.redirect != "" {
		s.target.Header().Set("Location", value.redirect)
	}
	if err := s.sendOutcome(actualDecision, false, false, status); err != nil {
		_ = s.cancelFailure(err)
		s.writeTerminalStatus(http.StatusServiceUnavailable)
		return
	}
	if err := s.cancel(false); err != nil {
		// The outcome was already recorded. A failed cleanup acknowledgement
		// is a connector/engine failure, never a fresh client cancellation.
		_ = s.cancelFailure(err)
		s.writeTerminalStatus(http.StatusServiceUnavailable)
		return
	}
	s.writeTerminalStatus(status)
}

func validRedirect(value string) bool {
	return value != "" && len(value) <= maxHeaderValue && validResultText([]byte(value))
}

func (s *responseState) sendLateOutcome(status int) error {
	return s.sendOutcome(decisionLogOnly, true, false, status)
}
func (s *responseState) sendOutcome(decisionKind byte, late bool, connectionAborted bool, status int) error {
	payload := encodeOutcome(decisionKind, late, connectionAborted, status)
	result, err := s.session.exchange(s.request.Context(), opOutcome, payload)
	if err != nil {
		return err
	}
	if result.code != resultOK {
		return errProtocol
	}
	return nil
}

func encodeOutcome(decisionKind byte, late bool, connectionAborted bool, status int) []byte {
	flags := byte(0)
	if connectionAborted {
		flags = 1
	}
	payload := []byte{outcomeAction(decisionKind, !late), flags, 0, 0}
	binary.BigEndian.PutUint16(payload[2:], uint16(status))
	return payload
}
func (s *responseState) cancel(upstreamDisconnect bool) error {
	value := cancelClientCancel
	if upstreamDisconnect {
		value = cancelUpstreamDisconnect
	}
	return s.cancelWithClass(value)
}

func (s *responseState) cancelFailure(err error) error {
	if errors.Is(err, context.Canceled) {
		return s.cancelWithClass(cancelClientCancel)
	}
	if errors.Is(err, context.DeadlineExceeded) {
		return s.cancelWithClass(cancelEngineTimeout)
	}
	var networkError net.Error
	if errors.As(err, &networkError) && networkError.Timeout() {
		return s.cancelWithClass(cancelEngineTimeout)
	}
	if errors.Is(err, errProtocol) {
		return s.cancelWithClass(cancelProtocolError)
	}
	return s.cancelWithClass(cancelConnectorError)
}

func (s *responseState) cancelWithClass(value byte) error {
	cleanupContext, cleanupCancel := context.WithTimeout(context.Background(), s.session.timeout)
	defer cleanupCancel()
	result, err := s.session.exchange(cleanupContext, opCancel, []byte{value})
	if err != nil {
		return err
	}
	if result.code != resultOK {
		return errProtocol
	}
	return nil
}
func outcomeAction(kind byte, applied bool) byte {
	if !applied {
		return outcomeLogOnly
	}
	switch kind {
	case decisionAllow:
		return outcomeAllow
	case decisionRedirect:
		return outcomeRedirect
	case decisionDrop:
		return outcomeDrop
	case decisionAbort:
		return outcomeAbort
	case decisionError:
		return outcomeError
	case decisionUnsupported:
		return outcomeUnsupported
	case decisionLogOnly:
		return outcomeLogOnly
	default:
		return outcomeDeny
	}
}

func disruptive(action byte) bool {
	return action == decisionDeny || action == decisionRedirect || action == decisionDrop ||
		action == decisionAbort || action == decisionError || action == decisionUnsupported
}

func encodeResponseHeaders(status int, headers http.Header) []byte {
	version := "HTTP/1.1"
	count, headerBytes, total := 0, 0, 6+len(version)
	for name, values := range headers {
		for _, value := range values {
			if count >= maxHeaderCount || len(name) > maxHeaderName || len(value) > maxHeaderValue {
				return nil
			}
			count++
			headerBytes += len(name) + len(value)
			total += 4 + len(name) + len(value)
		}
	}
	if headerBytes > maxPayload || total > maxResponseHeaderPayload {
		return nil
	}
	payload := make([]byte, total)
	offset := 0
	binary.BigEndian.PutUint16(payload[offset:], uint16(status))
	offset += 2
	binary.BigEndian.PutUint16(payload[offset:], uint16(len(version)))
	offset += 2
	copy(payload[offset:], version)
	offset += len(version)
	binary.BigEndian.PutUint16(payload[offset:], uint16(count))
	offset += 2
	for name, values := range headers {
		for _, value := range values {
			binary.BigEndian.PutUint16(payload[offset:], uint16(len(name)))
			offset += 2
			copy(payload[offset:], name)
			offset += len(name)
			binary.BigEndian.PutUint16(payload[offset:], uint16(len(value)))
			offset += 2
			copy(payload[offset:], value)
			offset += len(value)
		}
	}
	return payload
}

var _ http.ResponseWriter = (*responseState)(nil)
var _ http.Flusher = (*responseState)(nil)
