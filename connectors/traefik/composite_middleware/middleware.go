// Package composite_middleware is the outer, response-capable half of the
// Traefik composite connector. It reserves a random lease only over a private
// UDS connection, injects it for the immediately following ForwardAuth call,
// and keeps that same UDS session for P3/P4 observation. The lease is never
// accepted from a client and is never written to an HTTP response.
package composite_middleware

import (
	"context"
	"encoding/base64"
	"encoding/binary"
	"errors"
	"io"
	"net"
	"net/http"
	"net/url"
	"sort"
	"strconv"
	"strings"
	"time"
	"unicode/utf8"
)

const (
	frameHeaderSize      = 12
	maxPayload           = 64 << 10
	maxToken             = 256
	maxChunk             = 32 << 10
	maxHeaders           = 256
	maxHeaderName        = 256
	maxHeaderValue       = 8192
	maxRedirect          = 4096
	defaultTimeout       = 5 * time.Second
	companionUnavailable = "composite companion unavailable"
	contentLengthHeader  = "content-length"
	trailerHeader        = "Trailer"
	commitPayload        = "\x01\x00"
	rejectedBody         = "request rejected\n"
	textContentType      = "text/plain; charset=utf-8"
	forbiddenHeaderChars = "\r\n\x00"

	reservationSnapshotVersion byte = 1
	requestContextHeader            = "X-Msconnector-Composite-Request-Context"

	opClaim           byte = 1
	opResponseHeaders byte = 2
	opResponseChunk   byte = 3
	opResponseEOS     byte = 4
	opResponseCommit  byte = 5
	opOutcome         byte = 6
	opFinish          byte = 7
	opReserve         byte = 8
	opResult          byte = 128

	resultOK       byte = 0
	decisionAllow  byte = 0
	decisionDeny   byte = 1
	decisionRedir  byte = 2
	actualDeny     byte = 1
	actualRedirect byte = 2
	actualLogOnly  byte = 3

	// resultFlagRequestTerminal preserves an actual P1/P2 ForwardAuth block.
	// The writer must forward that response unchanged and must not send P3/P4.
	resultFlagRequestTerminal byte = 1
)

var (
	errInvalidConfig = errors.New("modsecurity composite middleware: invalid configuration")
	errProtocol      = errors.New("modsecurity composite middleware: invalid MSC2 protocol frame")
)

// Config is the bounded local-plugin configuration.
type Config struct {
	SocketPath             string `json:"socketPath,omitempty"`
	LeaseHeader            string `json:"leaseHeader,omitempty"`
	MaxResponseChunkBytes  int    `json:"maxResponseChunkBytes,omitempty"`
	MaxResponseHeaderCount int    `json:"maxResponseHeaderCount,omitempty"`
	MaxResponseHeaderBytes int    `json:"maxResponseHeaderBytes,omitempty"`
	TimeoutMillis          int    `json:"timeoutMillis,omitempty"`
}

func CreateConfig() *Config {
	return &Config{
		SocketPath:             "/var/run/modsecurity/composite.sock",
		LeaseHeader:            "X-Msconnector-Composite-Lease",
		MaxResponseChunkBytes:  maxChunk,
		MaxResponseHeaderCount: maxHeaders,
		MaxResponseHeaderBytes: maxPayload,
		TimeoutMillis:          int(defaultTimeout / time.Millisecond),
	}
}

func New(_ context.Context, next http.Handler, config *Config, _ string) (http.Handler, error) {
	if next == nil || config == nil {
		return nil, errInvalidConfig
	}
	c := *config
	defaults := CreateConfig()
	if c.SocketPath == "" {
		c.SocketPath = defaults.SocketPath
	}
	if c.LeaseHeader == "" {
		c.LeaseHeader = defaults.LeaseHeader
	}
	if c.MaxResponseChunkBytes == 0 {
		c.MaxResponseChunkBytes = defaults.MaxResponseChunkBytes
	}
	if c.MaxResponseHeaderCount == 0 {
		c.MaxResponseHeaderCount = defaults.MaxResponseHeaderCount
	}
	if c.MaxResponseHeaderBytes == 0 {
		c.MaxResponseHeaderBytes = defaults.MaxResponseHeaderBytes
	}
	if c.TimeoutMillis == 0 {
		c.TimeoutMillis = defaults.TimeoutMillis
	}
	if !safeSocketPath(c.SocketPath) || !validHeaderToken(c.LeaseHeader) || c.MaxResponseChunkBytes <= 0 || c.MaxResponseChunkBytes > maxChunk || c.MaxResponseHeaderCount <= 0 || c.MaxResponseHeaderCount > maxHeaders || c.MaxResponseHeaderBytes <= 0 || c.MaxResponseHeaderBytes > maxPayload || c.TimeoutMillis <= 0 || c.TimeoutMillis > 60000 {
		return nil, errInvalidConfig
	}
	return &Middleware{next: next, config: c}, nil
}

type Middleware struct {
	next   http.Handler
	config Config
}

func (m *Middleware) ServeHTTP(w http.ResponseWriter, r *http.Request) {
	// Do not make the reservation conditional on, or reusable from, a client
	// header. Original P1 headers are snapshotted only into the private UDS
	// Reserve frame; the immediate ForwardAuth HTTP call carries only the lease
	// and Traefik-generated metadata from its explicit allow-list.
	stripInternalHeaders(r.Header, m.config.LeaseHeader, requestContextHeader)
	stripInternalHeaders(r.Trailer, m.config.LeaseHeader, requestContextHeader)
	reservePayload, err := reservationPayload(r.Method, requestURI(r), r.Header, r.Host, r.ContentLength)
	if err != nil {
		http.Error(w, companionUnavailable, http.StatusServiceUnavailable)
		return
	}
	defer wipeBytes(reservePayload)
	conn, err := dial(r.Context(), m.config.SocketPath, time.Duration(m.config.TimeoutMillis)*time.Millisecond)
	if err != nil {
		http.Error(w, companionUnavailable, http.StatusServiceUnavailable)
		return
	}
	p := &protocolConn{conn: conn, timeout: time.Duration(m.config.TimeoutMillis) * time.Millisecond}
	defer conn.Close()

	reservation, err := p.exchange(r.Context(), opReserve, reservePayload)
	if err != nil || reservation.token == "" {
		http.Error(w, companionUnavailable, http.StatusServiceUnavailable)
		return
	}
	lease := reservation.token
	r.Header.Set(m.config.LeaseHeader, lease)
	defer stripInternalHeaders(r.Header, m.config.LeaseHeader, requestContextHeader)
	defer stripInternalHeaders(r.Trailer, m.config.LeaseHeader, requestContextHeader)

	rw := &responseWriter{
		parent:   m,
		writer:   w,
		proto:    p,
		exchange: func(opcode byte, payload []byte) (result, error) { return p.exchange(r.Context(), opcode, payload) },
		lease:    lease,
	}
	m.next.ServeHTTP(rw, r)
	if rw.transportErr != nil && !rw.committed {
		for name := range w.Header() {
			w.Header().Del(name)
		}
		stripInternalHeaders(w.Header(), m.config.LeaseHeader, requestContextHeader)
		w.Header().Set("Connection", "close")
		w.WriteHeader(http.StatusServiceUnavailable)
		rw.status = http.StatusServiceUnavailable
		rw.wroteHeader = true
		rw.committed = true
	}
	if !rw.finished {
		rw.finish(r.Context())
	}
}

func safeSocketPath(path string) bool {
	if !strings.HasPrefix(path, "/") || strings.ContainsRune(path, 0) || len(path) > 108 {
		return false
	}
	for _, part := range strings.Split(path, "/") {
		if part == ".." {
			return false
		}
		if part == "" {
			continue
		}
		if strings.ContainsRune(part, '\\') {
			return false
		}
	}
	return true
}

func dial(ctx context.Context, path string, timeout time.Duration) (net.Conn, error) {
	d := net.Dialer{Timeout: timeout}
	return d.DialContext(ctx, "unix", path)
}

func requestURI(r *http.Request) string {
	if r == nil || r.URL == nil {
		return ""
	}
	if target := r.URL.RequestURI(); target != "" {
		return target
	}
	return (&url.URL{Path: r.URL.Path, RawQuery: r.URL.RawQuery}).RequestURI()
}

type reservationHeaderGroup struct {
	name   string
	values []string
}

// reservationPayload is the private UDS opReserve snapshot. It is deliberately
// versioned and length-delimited: no raw request header crosses the loopback
// ForwardAuth HTTP hop, no field is comma-joined, and no unbounded allocation
// is possible at the UDS peer. The paired parser accepts only this canonical
// lower-case, sorted representation.
func reservationPayload(method, target string, headers http.Header, authority string, contentLength int64) ([]byte, error) {
	if !validHeaderToken(method) || !validReservationTarget(target) {
		return nil, errProtocol
	}
	groups, err := reservationHeaderGroups(headers, authority, contentLength)
	if err != nil {
		return nil, err
	}
	p := make([]byte, 0, 256)
	p = append(p, reservationSnapshotVersion)
	p, err = appendReservationText(p, method, maxHeaderName)
	if err != nil {
		return nil, err
	}
	p, err = appendReservationText(p, target, maxPayload)
	if err != nil {
		return nil, err
	}
	if len(groups) > maxHeaders {
		return nil, errProtocol
	}
	var size [2]byte
	binary.BigEndian.PutUint16(size[:], uint16(len(groups)))
	p = append(p, size[:]...)
	for _, group := range groups {
		p, err = appendReservationText(p, group.name, maxHeaderName)
		if err != nil || len(group.values) == 0 || len(group.values) > maxHeaders {
			return nil, errProtocol
		}
		binary.BigEndian.PutUint16(size[:], uint16(len(group.values)))
		p = append(p, size[:]...)
		for _, value := range group.values {
			p, err = appendReservationValue(p, value)
			if err != nil {
				return nil, err
			}
		}
		if len(p) > maxPayload {
			return nil, errProtocol
		}
	}
	if len(p) > maxPayload {
		return nil, errProtocol
	}
	return p, nil
}

func reservationHeaderGroups(headers http.Header, authority string, contentLength int64) ([]reservationHeaderGroup, error) {
	if len(headers) > maxHeaders {
		return nil, errProtocol
	}
	groupsByName, valuesSeen, total, err := copyReservationHeaders(headers)
	if err != nil {
		return nil, err
	}
	valuesSeen, total, err = addReservationDefaults(groupsByName, authority, contentLength, valuesSeen, total)
	if err != nil {
		return nil, err
	}
	return sortedReservationGroups(groupsByName)
}

func addReservationDefaults(groupsByName map[string][]string, authority string, contentLength int64, valuesSeen, total int) (int, int, error) {
	if _, hasHost := groupsByName["host"]; !hasHost {
		if authority == "" || invalidHostAuthority(authority) {
			return 0, 0, errProtocol
		}
		groupsByName["host"] = []string{authority}
	}
	if _, hasContentLength := groupsByName[contentLengthHeader]; !hasContentLength && contentLength >= 0 {
		value := strconv.FormatInt(contentLength, 10)
		if valuesSeen == maxHeaders || total+len(contentLengthHeader)+len(value) > maxPayload {
			return 0, 0, errProtocol
		}
		groupsByName[contentLengthHeader] = []string{value}
		valuesSeen++
		total += len(contentLengthHeader) + len(value)
	}
	if len(groupsByName) > maxHeaders {
		return 0, 0, errProtocol
	}
	return valuesSeen, total, nil
}

func sortedReservationGroups(groupsByName map[string][]string) ([]reservationHeaderGroup, error) {
	names := make([]string, 0, len(groupsByName))
	for name := range groupsByName {
		names = append(names, name)
	}
	sort.Strings(names)
	groups := make([]reservationHeaderGroup, 0, len(names))
	valuesSeen, total := 0, 0
	for _, name := range names {
		values := groupsByName[name]
		if !validHeaderToken(name) || len(values) == 0 || len(values) > maxHeaders {
			return nil, errProtocol
		}
		var err error
		valuesSeen, total, err = accountHeaderValues(name, values, valuesSeen, total)
		if err != nil {
			return nil, err
		}
		groups = append(groups, reservationHeaderGroup{name: name, values: values})
	}
	return groups, nil
}

func copyReservationHeaders(headers http.Header) (map[string][]string, int, int, error) {
	groupsByName := make(map[string][]string, len(headers)+1)
	valuesSeen, total := 0, 0
	for name, values := range headers {
		if len(values) == 0 {
			continue
		}
		if len(values) > maxHeaders-valuesSeen {
			return nil, 0, 0, errProtocol
		}
		canonical := strings.ToLower(name)
		if !validHeaderToken(name) || internalReservationHeader(canonical) {
			return nil, 0, 0, errProtocol
		}
		if _, duplicate := groupsByName[canonical]; duplicate {
			// A normal net/http request cannot produce map keys that differ only
			// by case. Reject hand-built ambiguity rather than choosing one.
			return nil, 0, 0, errProtocol
		}
		if canonical == "host" && (len(values) != 1 || values[0] == "") {
			return nil, 0, 0, errProtocol
		}
		var err error
		valuesSeen, total, err = accountHeaderValues(canonical, values, valuesSeen, total)
		if err != nil {
			return nil, 0, 0, err
		}
		groupsByName[canonical] = append([]string(nil), values...)
	}
	return groupsByName, valuesSeen, total, nil
}

func accountHeaderValues(name string, values []string, seen, total int) (int, int, error) {
	for _, value := range values {
		if len(value) > maxHeaderValue || strings.ContainsAny(value, forbiddenHeaderChars) {
			return 0, 0, errProtocol
		}
		seen++
		total += len(name) + len(value)
		if seen > maxHeaders || total > maxPayload {
			return 0, 0, errProtocol
		}
	}
	return seen, total, nil
}

func appendReservationText(payload []byte, value string, max int) ([]byte, error) {
	if len(value) == 0 || len(value) > max || len(value) > int(^uint16(0)) || strings.ContainsAny(value, forbiddenHeaderChars) {
		return nil, errProtocol
	}
	return appendReservationField(payload, value)
}

func appendReservationValue(payload []byte, value string) ([]byte, error) {
	if len(value) > maxHeaderValue || len(value) > int(^uint16(0)) || strings.ContainsAny(value, forbiddenHeaderChars) {
		return nil, errProtocol
	}
	return appendReservationField(payload, value)
}

func appendReservationField(payload []byte, value string) ([]byte, error) {
	if len(payload)+2+len(value) > maxPayload {
		return nil, errProtocol
	}
	var size [2]byte
	binary.BigEndian.PutUint16(size[:], uint16(len(value)))
	payload = append(payload, size[:]...)
	payload = append(payload, value...)
	return payload, nil
}

func validReservationTarget(target string) bool {
	return strings.HasPrefix(target, "/") && len(target) <= maxPayload && !strings.ContainsAny(target, forbiddenHeaderChars)
}

func internalReservationHeader(name string) bool {
	return strings.EqualFold(name, "x-msconnector-composite-lease") ||
		strings.EqualFold(name, strings.ToLower(requestContextHeader))
}

func invalidHostAuthority(value string) bool {
	if strings.TrimSpace(value) != value {
		return true
	}
	for _, r := range value {
		if r < 0x20 || r == 0x7f || r == ' ' || r == '\t' || r == '\r' || r == '\n' || r == 0 {
			return true
		}
	}
	return false
}

type protocolConn struct {
	conn    net.Conn
	timeout time.Duration
}

func (p *protocolConn) exchange(ctx context.Context, opcode byte, payload []byte) (result, error) {
	if len(payload) > maxPayload || !knownOpcode(opcode) {
		return result{}, errProtocol
	}
	if err := p.setDeadline(ctx); err != nil {
		return result{}, err
	}
	frame := make([]byte, frameHeaderSize+len(payload))
	defer wipeBytes(frame)
	copy(frame[:4], "MSC2")
	frame[4] = 1
	frame[5] = opcode
	binary.BigEndian.PutUint32(frame[8:12], uint32(len(payload)))
	copy(frame[12:], payload)
	if err := writeFull(p.conn, frame); err != nil {
		return result{}, err
	}
	header := make([]byte, frameHeaderSize)
	if _, err := io.ReadFull(p.conn, header); err != nil {
		return result{}, err
	}
	if string(header[:4]) != "MSC2" || header[4] != 1 || header[5] != opResult || header[6] != 0 || header[7] != 0 || binary.BigEndian.Uint32(header[8:12]) > maxPayload {
		return result{}, errProtocol
	}
	data := make([]byte, binary.BigEndian.Uint32(header[8:12]))
	defer wipeBytes(data)
	if _, err := io.ReadFull(p.conn, data); err != nil {
		return result{}, err
	}
	res, err := parseResult(data)
	if err != nil || res.requestOpcode != opcode {
		return result{}, errProtocol
	}
	return res, nil
}

func (p *protocolConn) setDeadline(ctx context.Context) error {
	deadline := time.Now().Add(p.timeout)
	if d, ok := ctx.Deadline(); ok && d.Before(deadline) {
		deadline = d
	}
	return p.conn.SetDeadline(deadline)
}

type result struct {
	requestOpcode, code, decision, flags byte
	status                               uint16
	redirect                             string
	token                                string
}

func knownOpcode(op byte) bool {
	switch op {
	case opClaim, opResponseHeaders, opResponseChunk, opResponseEOS, opResponseCommit, opOutcome, opFinish, opReserve:
		return true
	default:
		return false
	}
}

func parseResult(b []byte) (result, error) {
	if len(b) < 8 || !knownOpcode(b[0]) || b[1] != resultOK || b[2] > decisionRedir {
		return result{}, errProtocol
	}
	r := result{requestOpcode: b[0], code: b[1], decision: b[2], flags: b[3], status: binary.BigEndian.Uint16(b[4:6])}
	value, err := resultValue(b, r.requestOpcode)
	if err != nil {
		return result{}, errProtocol
	}
	if r.requestOpcode == opReserve {
		if r.flags != 0 || r.decision != decisionAllow || r.status != 0 || !validOpaqueToken(value) {
			return result{}, errProtocol
		}
		r.token = value
		return r, nil
	}
	if r.flags != 0 {
		if r.requestOpcode != opClaim || r.flags != resultFlagRequestTerminal || r.decision != decisionAllow || r.status != 0 || value != "" {
			return result{}, errProtocol
		}
		return r, nil
	}
	r.redirect = value
	if !validDecisionResult(r) {
		return result{}, errProtocol
	}
	return r, nil
}

func resultValue(b []byte, opcode byte) (string, error) {
	n := int(binary.BigEndian.Uint16(b[6:8]))
	limit := maxRedirect
	if opcode == opReserve {
		limit = maxToken
	}
	if n > limit || len(b) != 8+n {
		return "", errProtocol
	}
	value := string(b[8:])
	if !utf8.ValidString(value) || strings.ContainsAny(value, "\r\n") {
		return "", errProtocol
	}
	return value, nil
}

func validDecisionResult(r result) bool {
	switch r.decision {
	case decisionAllow:
		return r.status == 0 && r.redirect == ""
	case decisionDeny:
		return r.status >= http.StatusBadRequest && r.status <= 599 && r.redirect == ""
	case decisionRedir:
		return r.status >= http.StatusMultipleChoices && r.status <= 399 && r.redirect != ""
	default:
		return false
	}
}

func validOpaqueToken(token string) bool {
	if token == "" || len(token) > maxToken || strings.Contains(token, ",") {
		return false
	}
	decoded, err := base64.RawURLEncoding.DecodeString(token)
	return err == nil && len(decoded) >= 32
}

func claimPayload(token string) []byte {
	b := make([]byte, 2+len(token))
	binary.BigEndian.PutUint16(b, uint16(len(token)))
	copy(b[2:], token)
	return b
}

type responseWriter struct {
	parent                                             *Middleware
	writer                                             http.ResponseWriter
	proto                                              *protocolConn
	exchange                                           func(byte, []byte) (result, error)
	lease                                              string
	status                                             int
	wroteHeader, committed, blocked, finished, claimed bool
	requestTerminal                                    bool
	late                                               bool
	outcomeAction                                      byte
	transportErr                                       error
}

func (rw *responseWriter) Header() http.Header { return rw.writer.Header() }

func (rw *responseWriter) ensureClaim() bool {
	if rw.claimed || rw.requestTerminal {
		return true
	}
	res, err := rw.exchange(opClaim, claimPayload(rw.lease))
	if err != nil || res.decision != decisionAllow {
		if err == nil {
			err = errProtocol
		}
		rw.transportErr = err
		return false
	}
	if res.flags == resultFlagRequestTerminal {
		rw.requestTerminal = true
		return true
	}
	rw.claimed = true
	return true
}

func (rw *responseWriter) WriteHeader(status int) {
	if rw.wroteHeader || rw.transportErr != nil {
		return
	}
	if status < 100 || status > 599 {
		rw.transportErr = errProtocol
		return
	}
	if status < http.StatusOK {
		// 100/102/103 are interim HTTP responses, not P3. Forward them without
		// touching the retained transaction, then wait for a 2xx--5xx final
		// response.  101 changes the protocol and cannot be correlated safely
		// by this HTTP response wrapper, so fail before anything is committed.
		if status == http.StatusSwitchingProtocols {
			rw.transportErr = errProtocol
			return
		}
		stripInternalHeaders(rw.writer.Header(), rw.parent.config.LeaseHeader, requestContextHeader)
		rw.writer.WriteHeader(status)
		return
	}
	if !rw.ensureClaim() {
		return
	}
	rw.status = status
	stripInternalHeaders(rw.writer.Header(), rw.parent.config.LeaseHeader, requestContextHeader)
	if rw.requestTerminal {
		rw.writer.WriteHeader(status)
		rw.wroteHeader = true
		rw.committed = true
		return
	}
	headers, err := responseHeaders(status, "HTTP/1.1", rw.writer.Header(), rw.parent.config.MaxResponseHeaderCount, rw.parent.config.MaxResponseHeaderBytes)
	if err != nil {
		rw.transportErr = err
		return
	}
	res, err := rw.exchange(opResponseHeaders, headers)
	if err != nil {
		rw.transportErr = err
		return
	}
	if res.decision != decisionAllow {
		rw.writeDecision(res)
		rw.blocked = true
		rw.wroteHeader = true
		return
	}
	res, err = rw.exchange(opResponseCommit, []byte(commitPayload))
	if err != nil {
		rw.transportErr = err
		return
	}
	if res.decision != decisionAllow {
		rw.writeDecision(res)
		rw.blocked = true
		rw.wroteHeader = true
		return
	}
	rw.writer.WriteHeader(status)
	rw.wroteHeader = true
	rw.committed = true
}

func (rw *responseWriter) Write(body []byte) (int, error) {
	if rw.blocked {
		return len(body), nil
	}
	if rw.transportErr != nil {
		// The response has not been committed, so swallow the current upstream
		// bytes and let the outer middleware replace them with a fail-closed
		// 503. Returning the UDS error here makes ReverseProxy abort the client
		// connection before that replacement response can be written.
		if !rw.committed {
			return len(body), nil
		}
		return 0, rw.transportErr
	}
	if !rw.wroteHeader {
		rw.WriteHeader(http.StatusOK)
	}
	if rw.transportErr != nil {
		if !rw.committed {
			return len(body), nil
		}
		return 0, rw.transportErr
	}
	if rw.blocked {
		return len(body), nil
	}
	if rw.requestTerminal {
		return rw.writer.Write(body)
	}
	return rw.writeChunks(body)
}

func (rw *responseWriter) writeChunks(body []byte) (int, error) {
	written := 0
	for written < len(body) {
		end := written + rw.parent.config.MaxResponseChunkBytes
		if end > len(body) {
			end = len(body)
		}
		chunk := body[written:end]
		res, err := rw.exchange(opResponseChunk, chunk)
		if err != nil {
			rw.transportErr = err
			return written, err
		}
		if res.decision != decisionAllow {
			rw.late = true
		}
		n, err := rw.writer.Write(chunk)
		written += n
		if err != nil {
			rw.transportErr = err
			return written, err
		}
		if n != len(chunk) {
			rw.transportErr = io.ErrShortWrite
			return written, rw.transportErr
		}
	}
	return written, nil
}

func (rw *responseWriter) Flush() {
	if !rw.wroteHeader {
		rw.WriteHeader(http.StatusOK)
	}
	if rw.transportErr == nil {
		if f, ok := rw.writer.(http.Flusher); ok {
			f.Flush()
		}
	}
}

func (rw *responseWriter) Push(target string, options *http.PushOptions) error {
	pusher, ok := rw.writer.(http.Pusher)
	if !ok {
		return http.ErrNotSupported
	}
	return pusher.Push(target, options)
}

func (rw *responseWriter) writeDecision(res result) {
	for name := range rw.writer.Header() {
		delete(rw.writer.Header(), name)
	}
	if res.decision == decisionRedir && res.redirect != "" {
		rw.writer.Header().Set("Location", res.redirect)
	}
	rw.writer.Header().Set("Content-Type", textContentType)
	status := int(res.status)
	if status < 100 || status > 599 {
		status = http.StatusForbidden
	}
	rw.status = status
	rw.writer.WriteHeader(status)
	if res.decision == decisionRedir {
		rw.outcomeAction = actualRedirect
		_, _ = io.WriteString(rw.writer, res.redirect)
	} else {
		rw.outcomeAction = actualDeny
		_, _ = io.WriteString(rw.writer, rejectedBody)
	}
	rw.committed = true
}

func stripHeader(headers http.Header, name string) {
	stripInternalHeaders(headers, name)
}

func wipeBytes(value []byte) {
	for i := range value {
		value[i] = 0
	}
}

// stripInternalHeaders removes private metadata from regular headers,
// explicitly declared trailers, and net/http trailer-prefix entries. This is
// defense in depth around the configured inner header middleware: neither a
// downstream handler nor a forged client trailer can make private connector
// metadata visible to an upstream or a client response.
func stripInternalHeaders(headers http.Header, names ...string) {
	if headers == nil || len(names) == 0 {
		return
	}
	for key, values := range headers {
		if isInternalHeader(key, names) {
			delete(headers, key)
			continue
		}
		if isInternalTrailerKey(key, names) {
			delete(headers, key)
			continue
		}
		if !strings.EqualFold(key, trailerHeader) {
			continue
		}
		filtered := filterTrailerValues(values, names)
		if len(filtered) == 0 {
			delete(headers, key)
		} else {
			headers[key] = filtered
		}
	}
}

func isInternalHeader(value string, names []string) bool {
	for _, name := range names {
		if strings.EqualFold(value, name) {
			return true
		}
	}
	return false
}

func isInternalTrailerKey(key string, names []string) bool {
	if len(key) < len(http.TrailerPrefix) || !strings.EqualFold(key[:len(http.TrailerPrefix)], http.TrailerPrefix) {
		return false
	}
	return isInternalHeader(key[len(http.TrailerPrefix):], names)
}

func filterTrailerValues(values, names []string) []string {
	filtered := make([]string, 0, len(values))
	for _, value := range values {
		kept := make([]string, 0)
		for _, part := range strings.Split(value, ",") {
			part = strings.TrimSpace(part)
			if part != "" && !isInternalHeader(part, names) {
				kept = append(kept, part)
			}
		}
		if len(kept) > 0 {
			filtered = append(filtered, strings.Join(kept, ", "))
		}
	}
	return filtered
}

func (rw *responseWriter) finish(ctx context.Context) {
	if rw.finished {
		return
	}
	rw.finished = true
	if rw.proto == nil {
		return
	}
	if rw.requestTerminal {
		_, _ = rw.proto.exchange(ctx, opFinish, nil)
		return
	}
	if rw.transportErr != nil {
		return
	}
	if !rw.blocked {
		if !rw.wroteHeader {
			rw.WriteHeader(http.StatusOK)
		}
		if rw.transportErr != nil {
			return
		}
		if res, err := rw.proto.exchange(ctx, opResponseEOS, nil); err != nil {
			rw.transportErr = err
			return
		} else if res.decision != decisionAllow {
			rw.late = true
		}
	}
	action := rw.outcomeAction
	if rw.late {
		action = actualLogOnly
	}
	payload := []byte{action, byte(rw.status >> 8), byte(rw.status)}
	if _, err := rw.proto.exchange(ctx, opOutcome, payload); err != nil {
		rw.transportErr = err
		return
	}
	_, _ = rw.proto.exchange(ctx, opFinish, nil)
}

func responseHeaders(status int, protocol string, h http.Header, maxCount, maxBytes int) ([]byte, error) {
	if len(h) > maxCount {
		return nil, errProtocol
	}
	p := make([]byte, 0, 256)
	count := 0
	total := 0
	if status < http.StatusOK || status > 599 || len(protocol) > maxHeaderValue || !utf8.ValidString(protocol) {
		return nil, errProtocol
	}
	var b [2]byte
	binary.BigEndian.PutUint16(b[:], uint16(status))
	p = append(p, b[:]...)
	binary.BigEndian.PutUint16(b[:], uint16(len(protocol)))
	p = append(p, b[:]...)
	p = append(p, protocol...)
	countOffset := len(p)
	p = append(p, 0, 0)
	for name, values := range h {
		if !validHeaderToken(name) {
			return nil, errProtocol
		}
		for _, value := range values {
			var err error
			p, count, total, err = appendResponseHeader(p, name, value, count, total, maxCount, maxBytes)
			if err != nil {
				return nil, errProtocol
			}
		}
	}
	binary.BigEndian.PutUint16(p[countOffset:countOffset+2], uint16(count))
	if len(p) > maxPayload {
		return nil, errProtocol
	}
	return p, nil
}

func appendResponseHeader(payload []byte, name, value string, count, total, maxCount, maxBytes int) ([]byte, int, int, error) {
	if len(name) > maxHeaderName || len(value) > maxHeaderValue || strings.ContainsAny(value, "\r\n") {
		return nil, 0, 0, errProtocol
	}
	count++
	if count > maxCount {
		return nil, 0, 0, errProtocol
	}
	total += len(name) + len(value) + 4
	if total > maxBytes || len(payload)+4+len(name)+len(value) > maxPayload {
		return nil, 0, 0, errProtocol
	}
	var b [2]byte
	binary.BigEndian.PutUint16(b[:], uint16(len(name)))
	payload = append(payload, b[:]...)
	payload = append(payload, name...)
	binary.BigEndian.PutUint16(b[:], uint16(len(value)))
	payload = append(payload, b[:]...)
	payload = append(payload, value...)
	return payload, count, total, nil
}

func validHeaderToken(s string) bool {
	if s == "" || !utf8.ValidString(s) {
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

var _ http.ResponseWriter = (*responseWriter)(nil)
var _ http.Flusher = (*responseWriter)(nil)
var _ io.ReaderFrom = (*responseWriter)(nil)

func (rw *responseWriter) ReadFrom(src io.Reader) (int64, error) {
	return io.Copy(struct{ io.Writer }{rw}, src)
}
