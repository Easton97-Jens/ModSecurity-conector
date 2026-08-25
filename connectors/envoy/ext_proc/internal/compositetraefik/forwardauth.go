// Package compositetraefik contains the private service side of the Traefik
// composite connector. The local plugin and this loopback service share only
// an opaque, UDS-reserved lease; no lease is ever emitted in an HTTP response.
package compositetraefik

import (
	"errors"
	"io"
	"net"
	"net/http"
	"strconv"
	"strings"

	"github.com/Easton97-Jens/ModSecurity-conector/connectors/envoy/ext_proc/internal/composite"
	"github.com/Easton97-Jens/ModSecurity-conector/connectors/envoy/ext_proc/internal/processor"
)

// LeaseHeader is private hop-by-hop metadata. The outer plugin replaces any
// client copy before it reaches this loopback service, the service omits it
// from Common headers, and the next Traefik middleware removes it before the
// real upstream request. It is never written to an HTTP response.
const LeaseHeader = "X-Msconnector-Composite-Lease"

const (
	commonTransportHTTPStatus = "http_status"
	commonTransportLogOnly    = "log_only"
	authorizationUnavailable  = "authorization unavailable"
)

var (
	ErrInvalidRequest = errors.New("invalid forwardAuth request")
	ErrBodyLimit      = errors.New("forwardAuth request body limit exceeded")
)

// ForwardAuthConfig bounds all data retained by one authorization call.
type ForwardAuthConfig struct {
	MaxBodyBytes int64
}

func (c ForwardAuthConfig) withDefaults() (ForwardAuthConfig, error) {
	if c.MaxBodyBytes <= 0 {
		if c.MaxBodyBytes < 0 {
			return ForwardAuthConfig{}, ErrBodyLimit
		}
		c.MaxBodyBytes = 32
	}
	if c.MaxBodyBytes > maxFrame {
		return ForwardAuthConfig{}, ErrBodyLimit
	}
	return c, nil
}

// ForwardAuth handles the private loopback authorization call. The lease was
// reserved by the outer UDS companion and is activated here to create exactly
// one retained Common transaction for P1/P2 and the later P3/P4 response.
type ForwardAuth struct {
	Coordinator *composite.Coordinator
	Config      ForwardAuthConfig
}

func (h *ForwardAuth) ServeHTTP(w http.ResponseWriter, r *http.Request) {
	if h == nil || h.Coordinator == nil {
		writeUnavailable(w)
		return
	}
	cfg, err := h.Config.withDefaults()
	if err != nil {
		writeUnavailable(w)
		return
	}
	lease, ok := exactHeader(r.Header, LeaseHeader)
	if !ok {
		writeUnavailable(w)
		return
	}
	metaRequest, err := forwardedMetadata(r)
	if err != nil {
		writeUnavailable(w)
		return
	}
	meta := processor.StreamMetadata{Request: metaRequest}
	admission, decision, err := h.Coordinator.Activate(
		r.Context(), lease, metaRequest.Method, metaRequest.URI, meta, false,
	)
	if err != nil {
		writeUnavailable(w)
		return
	}
	if decision.Action != processor.ActionAllow {
		h.writeRequestDecision(w, r, admission, decision)
		return
	}
	// Preserve Common request ordering: P1 is evaluated from the canonical
	// ForwardAuth metadata before the bounded body read is turned into P2.
	body, tooLarge, err := readBounded(r.Body, cfg.MaxBodyBytes)
	if err != nil {
		admission.Cancel(r.Context())
		writeUnavailable(w)
		return
	}
	decision, err = admission.ProcessBody(r.Context(), body, true)
	if tooLarge {
		if err != nil && !errors.Is(err, composite.ErrLimit) {
			admission.Cancel(r.Context())
			writeUnavailable(w)
			return
		}
		if admission.RecordRequestBodyLimitHostAction() != nil {
			admission.Cancel(r.Context())
			writeUnavailable(w)
			return
		}
		http.Error(w, "request body too large", http.StatusRequestEntityTooLarge)
		return
	}
	if err != nil {
		admission.Cancel(r.Context())
		writeUnavailable(w)
		return
	}
	if decision.Action != processor.ActionAllow {
		h.writeRequestDecision(w, r, admission, decision)
		return
	}
	// Neither the lease nor a derived binding is ever copied to this response.
	w.WriteHeader(http.StatusOK)
}

func (h *ForwardAuth) writeRequestDecision(w http.ResponseWriter, r *http.Request, admission *composite.Admission, decision processor.Decision) {
	status := decision.Status
	action := processor.AppliedActionDeny
	if decision.Action == processor.ActionRedirect {
		action = processor.AppliedActionRedirect
		if status < http.StatusMultipleChoices || status > 399 {
			status = http.StatusFound
		}
	} else if status < http.StatusBadRequest || status > 599 {
		status = http.StatusForbidden
	}
	// The outer response wrapper must know that this is a request-terminal
	// decision before WriteHeader reaches it; otherwise its P3 Claim would
	// correctly fail closed because no host action had been recorded yet.
	// net/http exposes no write acknowledgement, so this is the closest native
	// host seam: record the exact status immediately before forwarding it.
	if admission.RecordHostAction(r.Context(), processor.HostAction{Action: action, VisibleStatus: status, TransportResult: commonTransportHTTPStatus}) != nil {
		admission.Cancel(r.Context())
		writeUnavailable(w)
		return
	}
	// Write the same normalized final status that was recorded as the host
	// action. Otherwise a malformed deny/redirect decision (for example 103 or
	// 200 for a deny) could send an informational/success response even though
	// the coordinator correctly recorded a request-terminal rejection.
	decision.Status = status
	writeDecision(w, decision, status)
}

func readBounded(r io.Reader, max int64) ([]byte, bool, error) {
	if r == nil {
		return nil, false, nil
	}
	if max < 0 {
		return nil, false, ErrBodyLimit
	}
	b, err := io.ReadAll(io.LimitReader(r, max+1))
	if err != nil {
		return nil, false, err
	}
	if int64(len(b)) > max {
		return b, true, nil
	}
	return b, false, nil
}

func writeUnavailable(w http.ResponseWriter) {
	http.Error(w, authorizationUnavailable, http.StatusServiceUnavailable)
}

func exactHeader(h http.Header, name string) (string, bool) {
	values := h.Values(name)
	if len(values) != 1 {
		return "", false
	}
	value := strings.TrimSpace(values[0])
	if value == "" || len(value) > maxTokenSize || strings.ContainsAny(value, "\r\n") || strings.Contains(value, ",") {
		return "", false
	}
	return value, true
}

func forwardedMetadata(r *http.Request) (processor.RequestMetadata, error) {
	method, ok := exactHeader(r.Header, "X-Forwarded-Method")
	if !ok || !validMethod(method) {
		return processor.RequestMetadata{}, ErrInvalidRequest
	}
	uri, ok := exactHeader(r.Header, "X-Forwarded-Uri")
	if !ok || !strings.HasPrefix(uri, "/") || strings.ContainsAny(uri, "\r\n") {
		return processor.RequestMetadata{}, ErrInvalidRequest
	}
	proto, ok := exactHeader(r.Header, "X-Forwarded-Proto")
	if !ok || (proto != "http" && proto != "https") {
		return processor.RequestMetadata{}, ErrInvalidRequest
	}
	host, ok := exactHeader(r.Header, "X-Forwarded-Host")
	if !ok || strings.ContainsAny(host, "\r\n") {
		return processor.RequestMetadata{}, ErrInvalidRequest
	}
	client, ok := exactHeader(r.Header, "X-Forwarded-For")
	if !ok || strings.ContainsAny(client, "\r\n") {
		return processor.RequestMetadata{}, ErrInvalidRequest
	}
	address, port, err := parseForwardedClient(client)
	if err != nil {
		return processor.RequestMetadata{}, ErrInvalidRequest
	}
	if !validHTTPProtocol(r.Proto) {
		return processor.RequestMetadata{}, ErrInvalidRequest
	}
	local, ok := r.Context().Value(http.LocalAddrContextKey).(net.Addr)
	if !ok || local == nil {
		return processor.RequestMetadata{}, ErrInvalidRequest
	}
	serverAddress, serverPort, err := parseServerAddr(local.String())
	if err != nil {
		return processor.RequestMetadata{}, ErrInvalidRequest
	}
	return processor.RequestMetadata{
		Method: method, URI: uri, Protocol: r.Proto, Hostname: host,
		ClientAddress: address, ClientPort: port, ServerAddress: serverAddress, ServerPort: serverPort,
	}, nil
}

func parseForwardedClient(value string) (string, int, error) {
	if ip := net.ParseIP(value); ip != nil {
		return ip.String(), 0, nil
	}
	host, port, err := netSplitHostPort(value)
	if err != nil || net.ParseIP(host) == nil || port < 1 || port > 65535 {
		return "", 0, ErrInvalidRequest
	}
	return host, port, nil
}

func validHTTPProtocol(s string) bool {
	return strings.HasPrefix(s, "HTTP/") && len(s) <= 16 && !strings.ContainsAny(s, "\r\n")
}

func parseServerAddr(s string) (string, int, error) {
	h, p, err := netSplitHostPort(s)
	if err != nil || h == "" || p < 1 || p > 65535 {
		return "", 0, ErrInvalidRequest
	}
	return h, p, nil
}

func validMethod(s string) bool {
	if s == "" {
		return false
	}
	for _, c := range s {
		if c <= ' ' || c >= 127 {
			return false
		}
	}
	return true
}

var netSplitHostPort = func(s string) (string, int, error) {
	h, p, err := net.SplitHostPort(s)
	if err != nil {
		return "", 0, err
	}
	n, err := strconv.Atoi(p)
	return h, n, err
}

func writeDecision(w http.ResponseWriter, d processor.Decision, fallback int) {
	status := d.Status
	if status < 100 || status > 599 {
		status = fallback
	}
	if d.Action == processor.ActionRedirect && d.RedirectURL != "" {
		w.Header().Set("Location", d.RedirectURL)
	}
	w.WriteHeader(status)
}

var _ http.Handler = (*ForwardAuth)(nil)
