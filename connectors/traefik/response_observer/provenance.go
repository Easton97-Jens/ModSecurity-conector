package response_observer

import (
	"context"
	"crypto/hmac"
	"crypto/rand"
	"crypto/sha256"
	"encoding/binary"
	"encoding/hex"
	"errors"
	"io"
	"log"
	"net"
	"net/http"
	"strconv"
	"strings"
	"sync"
	"time"
)

const provenanceHeader = "X-Msconnector-Trusted-Reservation"
const responseHandleHeader = "X-Msconnector-Response-Handle"

func validProvenanceText(value string) bool {
	if len(value) == 0 || len(value) > 128 {
		return false
	}
	for i := range value {
		c := value[i]
		if !((c >= 'a' && c <= 'z') || (c >= 'A' && c <= 'Z') ||
			(c >= '0' && c <= '9') || c == '_' || c == '-' || c == '.' || c == ':') {
			return false
		}
	}
	return true
}

func validateProvenanceConfig(c Config) error {
	if c.ConfirmProvenance && (c.ProvenanceSocketPath != "" || c.RunID != "" || c.TransportCaseID != "") {
		return errProtocol
	}
	if c.ProvenanceSocketPath == "" {
		if c.RunID != "" || c.TransportCaseID != "" {
			return errProtocol
		}
		return nil
	}
	if !safeSocketPath(c.ProvenanceSocketPath) || len(c.ProvenanceSocketPath) > 107 ||
		c.ProvenanceSocketPath == c.SocketPath || !validProvenanceText(c.RunID) ||
		!validProvenanceText(c.TransportCaseID) {
		return errProtocol
	}
	return nil
}

func (m *middleware) initializeCorrelationSecret() error {
	_, err := io.ReadFull(rand.Reader, m.correlationSecret[:])
	return err
}

// This is an opaque, instance-local physical-tuple correlation token. A tuple
// may be recycled, so it deliberately never asserts connection_reused=true.
// Independent host socket evidence is required to prove same-live reuse.
func (m *middleware) connectionCorrelation(r *http.Request) (string, error) {
	remoteHost, remotePort, err := net.SplitHostPort(r.RemoteAddr)
	if err != nil || net.ParseIP(remoteHost) == nil {
		return "", errProtocol
	}
	port, err := strconv.Atoi(remotePort)
	if err != nil || port < 1 || port > 65535 {
		return "", errProtocol
	}
	local, ok := r.Context().Value(http.LocalAddrContextKey).(net.Addr)
	if !ok || local == nil {
		return "", errProtocol
	}
	localHost, localPort, err := net.SplitHostPort(local.String())
	if err != nil || net.ParseIP(localHost) == nil {
		return "", errProtocol
	}
	port, err = strconv.Atoi(localPort)
	if err != nil || port < 1 || port > 65535 {
		return "", errProtocol
	}
	digest := hmac.New(sha256.New, m.correlationSecret[:])
	_, _ = io.WriteString(digest, local.String()+"\x00"+r.RemoteAddr)
	return hex.EncodeToString(digest.Sum(nil)), nil
}

func stripProvenanceHeaders(headers http.Header) {
	stripPrivateHeaders(headers, provenanceHeader)
}

func privateHeaderName(name string, names []string) bool {
	for _, private := range names {
		if strings.EqualFold(name, private) {
			return true
		}
	}
	return false
}

func privateHeaderKey(key string, names []string) bool {
	if privateHeaderName(key, names) {
		return true
	}
	return len(key) >= len(http.TrailerPrefix) &&
		strings.EqualFold(key[:len(http.TrailerPrefix)], http.TrailerPrefix) &&
		privateHeaderName(key[len(http.TrailerPrefix):], names)
}

func publicTrailerNames(values []string, private []string) []string {
	kept := []string{}
	for _, value := range values {
		for _, name := range strings.Split(value, ",") {
			name = strings.TrimSpace(name)
			if name != "" && !privateHeaderName(name, private) {
				kept = append(kept, name)
			}
		}
	}
	return kept
}

func stripPrivateHeaders(headers http.Header, names ...string) {
	for key, values := range headers {
		if privateHeaderKey(key, names) {
			delete(headers, key)
			continue
		}
		if !strings.EqualFold(key, "Trailer") {
			continue
		}
		kept := publicTrailerNames(values, names)
		if len(kept) == 0 {
			delete(headers, key)
		} else {
			headers[key] = []string{strings.Join(kept, ", ")}
		}
	}
}

type provenanceReservation struct {
	conn    net.Conn
	timeout time.Duration
	token   string
}

type provenanceBindingKey struct{}
type provenanceBinding struct {
	mu          sync.Mutex
	reservation *provenanceReservation
	reply       []byte
	confirmed   bool
	failed      bool
}

func (binding *provenanceBinding) confirm(ctx context.Context) error {
	binding.mu.Lock()
	defer binding.mu.Unlock()
	if binding.confirmed {
		binding.failed = true
		return errProtocol
	}
	reply, err := binding.reservation.exchange(ctx, 2, nil, 67)
	if err != nil {
		binding.failed = true
		return err
	}
	status := int(binary.BigEndian.Uint16(reply[:2]))
	if status < 200 || status >= 300 || !validHandle(string(reply[2:])) {
		binding.failed = true
		return errProtocol
	}
	binding.reply = reply
	binding.confirmed = true
	return nil
}

func (m *middleware) confirmProvenance(w http.ResponseWriter, r *http.Request) {
	stripPrivateHeaders(r.Header, provenanceHeader, responseHandleHeader)
	stripPrivateHeaders(r.Trailer, provenanceHeader, responseHandleHeader)
	binding, ok := r.Context().Value(provenanceBindingKey{}).(*provenanceBinding)
	if !ok || binding == nil || binding.confirm(r.Context()) != nil {
		http.Error(w, "trusted authorization confirmation required", http.StatusServiceUnavailable)
		return
	}
	m.next.ServeHTTP(w, r)
}

func provenanceFrame(op byte, payload []byte) []byte {
	frame := make([]byte, 12+len(payload))
	copy(frame, "MTP1")
	frame[4], frame[5] = 1, op
	binary.BigEndian.PutUint32(frame[8:12], uint32(len(payload)))
	copy(frame[12:], payload)
	return frame
}

func (p *provenanceReservation) exchange(ctx context.Context, op byte, payload []byte, size int) ([]byte, error) {
	deadline := time.Now().Add(p.timeout)
	if expires, ok := ctx.Deadline(); ok && expires.Before(deadline) {
		deadline = expires
	}
	if err := p.conn.SetDeadline(deadline); err != nil {
		return nil, err
	}
	if err := ctx.Err(); err != nil {
		return nil, err
	}
	// A canceled request must release its lease while blocked in private I/O.
	stopped := make(chan struct{})
	exited := make(chan struct{})
	go func() {
		defer close(exited)
		select {
		case <-ctx.Done():
			_ = p.conn.Close()
		case <-stopped:
		}
	}()
	defer func() { close(stopped); <-exited }()
	frame := provenanceFrame(op, payload)
	for len(frame) > 0 {
		n, err := p.conn.Write(frame)
		if err != nil {
			return nil, err
		}
		if n <= 0 {
			return nil, io.ErrShortWrite
		}
		frame = frame[n:]
	}
	header := make([]byte, 12)
	if _, err := io.ReadFull(p.conn, header); err != nil {
		return nil, err
	}
	if string(header[:4]) != "MTP1" || header[4] != 1 || header[5] != 128 ||
		header[6] != 0 || header[7] != 0 || int(binary.BigEndian.Uint32(header[8:])) != size {
		return nil, errProtocol
	}
	result := make([]byte, size)
	if _, err := io.ReadFull(p.conn, result); err != nil {
		return nil, err
	}
	if len(result) == 0 || result[0] != 0 {
		return nil, errProtocol
	}
	return result[1:], nil
}

func (m *middleware) reserveProvenance(r *http.Request) (*provenanceReservation, error) {
	correlation, err := m.connectionCorrelation(r)
	if err != nil {
		return nil, err
	}
	dialer := net.Dialer{Timeout: time.Duration(m.config.TimeoutMillis) * time.Millisecond}
	conn, err := dialer.DialContext(r.Context(), "unix", m.config.ProvenanceSocketPath)
	if err != nil {
		return nil, err
	}
	if err := verifyResponseCompanionPeer(conn, *m.config.ExpectedPeerUID, *m.config.ExpectedPeerGID); err != nil {
		_ = conn.Close()
		return nil, err
	}
	reservation := &provenanceReservation{conn: conn, timeout: time.Duration(m.config.TimeoutMillis) * time.Millisecond}
	payload := make([]byte, 0, 391)
	for _, value := range []string{m.config.RunID, m.config.TransportCaseID, correlation} {
		payload = append(payload, byte(len(value)>>8), byte(len(value)))
		payload = append(payload, value...)
	}
	payload = append(payload, 0) // conservative reuse; never derive it from tuple cache
	token, err := reservation.exchange(r.Context(), 1, payload, 65)
	if err != nil || !validHandle(string(token)) {
		_ = conn.Close()
		return nil, errProtocol
	}
	reservation.token = string(token)
	return reservation, nil
}

func (m *middleware) serveWithProvenance(w http.ResponseWriter, r *http.Request) {
	// This mode is outermost: discard client handles before built-in
	// ForwardAuth. Its binding is obtained only through this private lease.
	for key := range r.Header {
		if strings.EqualFold(key, responseHandleHeader) {
			delete(r.Header, key)
		}
	}
	reservation, err := m.reserveProvenance(r)
	if err != nil {
		http.Error(w, "trusted reservation unavailable", http.StatusServiceUnavailable)
		return
	}
	defer reservation.conn.Close()
	r.Header.Set(provenanceHeader, reservation.token)
	defer stripProvenanceHeaders(r.Header)
	defer stripProvenanceHeaders(r.Trailer)
	binding := &provenanceBinding{reservation: reservation}
	r = r.WithContext(context.WithValue(r.Context(), provenanceBindingKey{}, binding))
	writer := &provenanceWriter{target: w, request: r, parent: m, binding: binding}
	completed := false
	defer func() { writer.cleanup(completed) }()
	m.next.ServeHTTP(writer, r)
	completed = true
}

type provenanceWriter struct {
	target                  http.ResponseWriter
	request                 *http.Request
	parent                  *middleware
	binding                 *provenanceBinding
	state                   *responseState
	cleanupError            error
	wrote, terminal, failed bool
}

func (w *provenanceWriter) cleanupCause(completed bool) byte {
	if errors.Is(w.request.Context().Err(), context.DeadlineExceeded) {
		return cancelEngineTimeout
	}
	if w.request.Context().Err() != nil {
		return cancelClientCancel
	}
	if completed && w.failed {
		return cancelProtocolError
	}
	return cancelConnectorError
}

func (w *provenanceWriter) cleanupBeforeHeaders(completed bool) {
	if err := w.cancelBeforeHeaders(w.cleanupCause(completed)); err != nil {
		w.cleanupError = err
		// Keep a physical, payload-free failure signal; never log the
		// capability, handle, metadata or request/response bytes.
		log.Print("modsecurity response observer: trusted reservation cleanup failed")
	}
	if completed && !w.wrote {
		w.wrote = true
		w.fail()
	}
}

func (w *provenanceWriter) cleanup(completed bool) {
	if w.state == nil {
		w.cleanupBeforeHeaders(completed)
		return
	}
	defer w.state.session.close()
	if !completed {
		if !w.state.finished && !w.state.precommitFail {
			_ = w.state.cancelWithClass(cancelConnectorError)
		}
		w.state.finished = true
		return
	}
	w.finish()
}

func (w *provenanceWriter) Header() http.Header { return w.target.Header() }
func (w *provenanceWriter) WriteHeader(status int) {
	if w.wrote {
		return
	}
	if status >= 100 && status < 200 && status != http.StatusSwitchingProtocols {
		stripPrivateHeaders(w.target.Header(), provenanceHeader, responseHandleHeader)
		w.target.WriteHeader(status)
		return
	}
	w.wrote = true
	w.binding.mu.Lock()
	reply := w.binding.reply
	confirmed := w.binding.confirmed
	failed := w.binding.failed
	var err error
	if !confirmed && !failed {
		reply, err = w.binding.reservation.exchange(w.request.Context(), 2, nil, 67)
		if err == nil {
			w.binding.reply = reply
		}
	}
	w.binding.mu.Unlock()
	if err != nil || failed {
		w.fail()
		return
	}
	attestedStatus := int(binary.BigEndian.Uint16(reply[:2]))
	handle := string(reply[2:])
	if handle == strings.Repeat("\x00", 64) {
		if attestedStatus < 300 || attestedStatus > 599 || attestedStatus != status {
			w.fail()
			return
		}
		w.terminal = true
		stripPrivateHeaders(w.target.Header(), provenanceHeader, responseHandleHeader)
		w.target.WriteHeader(status)
		return
	}
	if !confirmed || attestedStatus < 200 || attestedStatus >= 300 || !validHandle(handle) {
		w.fail()
		return
	}
	session, err := openSession(w.request.Context(), w.parent.config, handle)
	if err != nil {
		w.fail()
		return
	}
	w.request.Header.Del(responseHandleHeader)
	stripPrivateHeaders(w.target.Header(), provenanceHeader, responseHandleHeader)
	w.state = &responseState{session: session, target: w.target, request: w.request}
	w.state.WriteHeader(status)
}

func (w *provenanceWriter) fail() {
	for key := range w.target.Header() {
		delete(w.target.Header(), key)
	}
	w.failed = true
	w.target.WriteHeader(http.StatusServiceUnavailable)
}

// No MRC1 claim exists during normal backend waiting. If that wait exits
// without a response header, claim the privately attested handle solely for
// bounded typed cancellation using a detached cleanup context.
func (w *provenanceWriter) cancelBeforeHeaders(cause byte) error {
	w.binding.mu.Lock()
	reply := append([]byte(nil), w.binding.reply...)
	w.binding.mu.Unlock()
	ctx, cancel := context.WithTimeout(context.Background(), time.Duration(w.parent.config.TimeoutMillis)*time.Millisecond)
	defer cancel()
	if len(reply) == 0 {
		var err error
		reply, err = w.binding.reservation.exchange(ctx, 2, nil, 67)
		if err != nil {
			return err
		}
	}
	if len(reply) != 66 {
		return errProtocol
	}
	status := int(binary.BigEndian.Uint16(reply[:2]))
	if status >= 300 && status <= 599 && string(reply[2:]) == strings.Repeat("\x00", 64) {
		return nil
	}
	if status < 200 || status >= 300 || !validHandle(string(reply[2:])) {
		return errProtocol
	}
	session, err := openSession(ctx, w.parent.config, string(reply[2:]))
	if err != nil {
		return err
	}
	defer session.close()
	state := &responseState{session: session, target: w.target, request: w.request}
	err = state.cancelWithClass(cause)
	state.finished = true
	return err
}
func (w *provenanceWriter) Write(payload []byte) (int, error) {
	if !w.wrote {
		w.WriteHeader(http.StatusOK)
	}
	if w.failed {
		return len(payload), nil
	}
	if w.terminal {
		return w.target.Write(payload)
	}
	if w.state == nil {
		return 0, errors.New("missing private companion binding")
	}
	return w.state.Write(payload)
}
func (w *provenanceWriter) Flush() {
	if !w.wrote {
		w.WriteHeader(http.StatusOK)
	}
	if w.state != nil {
		w.state.Flush()
		return
	}
	if f, ok := w.target.(http.Flusher); ok {
		f.Flush()
	}
}
func (w *provenanceWriter) ReadFrom(reader io.Reader) (int64, error) {
	return io.Copy(struct{ io.Writer }{w}, reader)
}
func (w *provenanceWriter) finish() {
	if !w.wrote {
		w.WriteHeader(http.StatusOK)
	}
	if w.state != nil {
		w.state.finish()
	}
}
