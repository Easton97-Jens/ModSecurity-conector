// Package modsecuritynative provides a repository-owned Traefik middleware
// entry point with a deliberately narrow, streaming engine seam.
//
// The public CreateConfig and New functions use Traefik's Go middleware
// shape: Traefik supplies an http.Handler and calls ServeHTTP for each
// request.  The package imports no Traefik internals, Common runtime code, or
// libmodsecurity.  That keeps the source buildable as a local plugin package
// while making the missing Common/libmodsecurity bridge explicit.  New
// installs PassthroughEngine, so this source alone is not rule-evaluation or
// runtime evidence.
package modsecuritynative

import (
	"bufio"
	"context"
	"errors"
	"fmt"
	"io"
	"net"
	"net/http"
	"net/url"
	"sort"
	"strings"
	"sync"
)

const (
	defaultMaxHeaderCount        = 128
	defaultMaxHeaderBytes        = 64 << 10
	defaultMaxRequestChunkBytes  = 32 << 10
	defaultMaxResponseChunkBytes = 32 << 10
)

var (
	// ErrRequestRejected is returned to the downstream handler's request-body
	// reader after a prospective engine decision rejects a request-body chunk.
	// The middleware writes the decision only if response headers have not
	// already committed.
	ErrRequestRejected = errors.New("modsecurity native middleware: request rejected")

	// ErrResponseRejected is returned from Write/ReadFrom when a prospective
	// decision is made before response commitment. It is intentionally not used
	// to claim a late connection abort after bytes have been sent.
	ErrResponseRejected = errors.New("modsecurity native middleware: response rejected")
)

// Config is intentionally limited to bounded streaming controls. It is the
// config object Traefik supplies to CreateConfig/New when this package is used
// as a Go middleware plugin.
//
// EngineMode is currently restricted to "passthrough". A Common or
// libmodsecurity bridge must be added as a separately reviewed Engine rather
// than turning this source-only path into an implicit security claim.
type Config struct {
	MaxHeaderCount        int    `json:"maxHeaderCount,omitempty"`
	MaxHeaderBytes        int    `json:"maxHeaderBytes,omitempty"`
	MaxRequestChunkBytes  int    `json:"maxRequestChunkBytes,omitempty"`
	MaxResponseChunkBytes int    `json:"maxResponseChunkBytes,omitempty"`
	TransactionIDHeader   string `json:"transactionIDHeader,omitempty"`
	EngineMode            string `json:"engineMode,omitempty"`
}

// CreateConfig returns safe bounded defaults. It is the standard Traefik Go
// plugin configuration entry point.
func CreateConfig() *Config {
	return &Config{
		MaxHeaderCount:        defaultMaxHeaderCount,
		MaxHeaderBytes:        defaultMaxHeaderBytes,
		MaxRequestChunkBytes:  defaultMaxRequestChunkBytes,
		MaxResponseChunkBytes: defaultMaxResponseChunkBytes,
		TransactionIDHeader:   "X-Request-Id",
		EngineMode:            "passthrough",
	}
}

func normalizedConfig(config *Config) (Config, error) {
	if config == nil {
		return Config{}, errors.New("modsecurity native middleware: config is required")
	}
	value := *config
	if value.MaxHeaderCount == 0 {
		value.MaxHeaderCount = defaultMaxHeaderCount
	}
	if value.MaxHeaderBytes == 0 {
		value.MaxHeaderBytes = defaultMaxHeaderBytes
	}
	if value.MaxRequestChunkBytes == 0 {
		value.MaxRequestChunkBytes = defaultMaxRequestChunkBytes
	}
	if value.MaxResponseChunkBytes == 0 {
		value.MaxResponseChunkBytes = defaultMaxResponseChunkBytes
	}
	if value.TransactionIDHeader == "" {
		value.TransactionIDHeader = "X-Request-Id"
	}
	if value.EngineMode == "" {
		value.EngineMode = "passthrough"
	}
	if value.MaxHeaderCount <= 0 || value.MaxHeaderBytes <= 0 ||
		value.MaxRequestChunkBytes <= 0 || value.MaxResponseChunkBytes <= 0 {
		return Config{}, errors.New("modsecurity native middleware: all limits must be positive")
	}
	if strings.TrimSpace(value.TransactionIDHeader) == "" {
		return Config{}, errors.New("modsecurity native middleware: transactionIDHeader is required")
	}
	if value.EngineMode != "passthrough" {
		return Config{}, fmt.Errorf("modsecurity native middleware: unsupported engineMode %q", value.EngineMode)
	}
	return value, nil
}

// Direction keeps the engine seam independent of Traefik and HTTP plumbing.
type Direction string

const (
	DirectionRequest  Direction = "request"
	DirectionResponse Direction = "response"
)

// Header is a bounded borrowed view passed to an Engine callback. Implementers
// must consume it synchronously and must not retain header values.
type Header struct {
	Name  string
	Value string
}

// Metadata intentionally contains only routing/request identifiers, never a
// request or response body payload.
type Metadata struct {
	TransactionID string
	Method        string
	RequestURI    string
}

// Action is a prospective engine result. Only a decision discovered before
// response commitment can change the HTTP response. A late disruptive result
// is recorded in Summary as log-only and never claimed as an abort.
type Action string

const (
	ActionAllow    Action = "allow"
	ActionDeny     Action = "deny"
	ActionRedirect Action = "redirect"
)

// Decision is supplied by the future engine bridge. Status and Location are
// normalized before being written to a client response.
type Decision struct {
	Action   Action
	Status   int
	Location string
}

func allowDecision() Decision {
	return Decision{Action: ActionAllow}
}

func (decision Decision) disruptive() bool {
	return decision.Action == ActionDeny || decision.Action == ActionRedirect
}

// Summary is the metadata-only lifecycle record passed to Transaction.Close.
// It deliberately keeps counters and outcomes, never body content.
type Summary struct {
	TransactionID       string
	RequestHeaderCount  uint64
	ResponseHeaderCount uint64
	RequestBodyChunks   uint64
	ResponseBodyChunks  uint64
	RequestBodyBytes    int64
	ResponseBodyBytes   int64
	RequestEOS          bool
	ResponseEOS         bool
	ResponseCommitted   bool
	LateAction          string
}

// Engine is the explicit future bridge to Common/libmodsecurity. The checked-in
// Traefik entry point installs PassthroughEngine. An Engine receives bounded,
// incremental callbacks only and must never retain borrowed body slices.
type Engine interface {
	Open(context.Context, Metadata) (Transaction, error)
}

// Transaction consumes the request/response lifecycle for one HTTP request.
// Body slices are borrowed and valid only for the duration of the callback.
type Transaction interface {
	ProcessHeaders(context.Context, Direction, []Header, bool) (Decision, error)
	ProcessBody(context.Context, Direction, []byte, bool) (Decision, error)
	Close(context.Context, Summary)
}

// PassthroughEngine is intentionally the only engine New can construct. It
// proves no Common/libmodsecurity integration and always allows traffic.
type PassthroughEngine struct{}

func (PassthroughEngine) Open(_ context.Context, _ Metadata) (Transaction, error) {
	return passthroughTransaction{}, nil
}

type passthroughTransaction struct{}

func (passthroughTransaction) ProcessHeaders(_ context.Context, _ Direction, _ []Header, _ bool) (Decision, error) {
	return allowDecision(), nil
}

func (passthroughTransaction) ProcessBody(_ context.Context, _ Direction, _ []byte, _ bool) (Decision, error) {
	return allowDecision(), nil
}

func (passthroughTransaction) Close(_ context.Context, _ Summary) {}

// Middleware is an http.Handler suitable for Traefik's Go middleware API.
// New creates it with PassthroughEngine. Tests and a future reviewed bridge may
// use NewWithEngine to supply an explicit engine implementation.
type Middleware struct {
	next   http.Handler
	config Config
	engine Engine
	name   string
}

// New is Traefik's Go plugin entry point. Its http.Handler return signature is
// intentionally the one expected by Traefik's Yaegi middleware contract. It
// preserves the existing forwardAuth connector by being an unselected alternate
// source/build path; selecting it in a real Traefik deployment requires
// independent config-load and runtime evidence.
func New(_ context.Context, next http.Handler, config *Config, name string) (http.Handler, error) {
	return NewWithEngine(next, config, name, PassthroughEngine{})
}

// NewWithEngine is an explicit test/future-bridge seam. A nil Engine is never
// silently replaced because doing so would hide a missing security integration.
func NewWithEngine(next http.Handler, config *Config, name string, engine Engine) (*Middleware, error) {
	if next == nil {
		return nil, errors.New("modsecurity native middleware: next handler is required")
	}
	if engine == nil {
		return nil, errors.New("modsecurity native middleware: engine is required")
	}
	normalized, err := normalizedConfig(config)
	if err != nil {
		return nil, err
	}
	return &Middleware{next: next, config: normalized, engine: engine, name: name}, nil
}

// ServeHTTP evaluates headers and body chunks incrementally. It never collects
// a complete request or response body: request reads are capped, response
// writes are sliced for callbacks, and ReadFrom uses at most one bounded first
// chunk before delegating the remaining stream.
func (middleware *Middleware) ServeHTTP(writer http.ResponseWriter, request *http.Request) {
	contextValue := request.Context()
	metadata := Metadata{
		TransactionID: request.Header.Get(middleware.config.TransactionIDHeader),
		Method:        request.Method,
		RequestURI:    request.URL.RequestURI(),
	}
	transaction, err := middleware.engine.Open(contextValue, metadata)
	if err != nil {
		http.Error(writer, "modsecurity middleware engine unavailable", http.StatusInternalServerError)
		return
	}

	state := &streamState{
		context:  contextValue,
		config:   middleware.config,
		metadata: metadata,
		engine:   transaction,
	}
	defer state.close()

	requestHeaders, err := boundedHeaders(request.Header, middleware.config)
	if err != nil {
		http.Error(writer, "request headers exceed middleware limits", http.StatusRequestHeaderFieldsTooLarge)
		return
	}
	requestEnd := request.Body == nil || request.ContentLength == 0
	decision, err := state.processHeaders(DirectionRequest, requestHeaders, requestEnd)
	if err != nil {
		http.Error(writer, "modsecurity middleware request-header evaluation failed", http.StatusInternalServerError)
		return
	}
	if decision.disruptive() {
		writeDecision(writer, decision)
		state.markCommitted()
		return
	}
	if requestEnd {
		state.markRequestEOS()
	}

	response := newResponseWriter(writer, state)
	originalBody := request.Body
	if originalBody != nil {
		request.Body = &inspectingRequestBody{source: originalBody, state: state}
		defer func() { request.Body = originalBody }()
	}

	middleware.next.ServeHTTP(response, request)
	response.finish()
}

type streamState struct {
	mu       sync.Mutex
	context  context.Context
	config   Config
	metadata Metadata
	engine   Transaction

	requestHeaderCount  uint64
	responseHeaderCount uint64
	requestBodyChunks   uint64
	responseBodyChunks  uint64
	requestBodyBytes    int64
	responseBodyBytes   int64
	requestEOS          bool
	responseEOS         bool
	responseCommitted   bool
	lateAction          string

	pendingRequestDecision Decision
	pendingRequestError    error
	closed                 bool
}

func (state *streamState) processHeaders(direction Direction, headers []Header, end bool) (Decision, error) {
	state.mu.Lock()
	defer state.mu.Unlock()
	if direction == DirectionRequest {
		state.requestHeaderCount += uint64(len(headers))
	} else {
		state.responseHeaderCount += uint64(len(headers))
	}
	return state.engine.ProcessHeaders(state.context, direction, headers, end)
}

// processRequestBody returns an error only for a request-side rejection or an
// engine failure. The pending result is also retained so a handler that tries
// to write after Read returns can still be blocked before commitment.
func (state *streamState) processRequestBody(chunk []byte, end bool) error {
	state.mu.Lock()
	defer state.mu.Unlock()
	if end && state.requestEOS {
		return nil
	}
	state.requestBodyChunks++
	state.requestBodyBytes += int64(len(chunk))
	decision, err := state.engine.ProcessBody(state.context, DirectionRequest, chunk, end)
	if end {
		state.requestEOS = true
	}
	if err != nil {
		state.pendingRequestError = err
		return err
	}
	if decision.disruptive() {
		state.pendingRequestDecision = decision
		return ErrRequestRejected
	}
	return nil
}

// processResponseBody invokes the engine before a bounded slice is forwarded.
// A disruptive decision found after commitment is intentionally a log-only
// outcome: no synthetic abort or changed visible HTTP status is claimed.
func (state *streamState) processResponseBody(chunk []byte, end bool, beforeCommit bool) (Decision, error) {
	state.mu.Lock()
	defer state.mu.Unlock()
	if end && state.responseEOS {
		return allowDecision(), nil
	}
	state.responseBodyChunks++
	state.responseBodyBytes += int64(len(chunk))
	decision, err := state.engine.ProcessBody(state.context, DirectionResponse, chunk, end)
	if end {
		state.responseEOS = true
	}
	if err != nil {
		return allowDecision(), err
	}
	if decision.disruptive() && !beforeCommit {
		state.lateAction = "log_only"
		return allowDecision(), nil
	}
	return decision, nil
}

func (state *streamState) pendingRequestResult() (Decision, error) {
	state.mu.Lock()
	defer state.mu.Unlock()
	return state.pendingRequestDecision, state.pendingRequestError
}

func (state *streamState) markCommitted() {
	state.mu.Lock()
	state.responseCommitted = true
	state.mu.Unlock()
}

func (state *streamState) markRequestEOS() {
	state.mu.Lock()
	state.requestEOS = true
	state.mu.Unlock()
}

func (state *streamState) close() {
	state.mu.Lock()
	defer state.mu.Unlock()
	if state.closed {
		return
	}
	state.closed = true
	state.engine.Close(state.context, Summary{
		TransactionID:       state.metadata.TransactionID,
		RequestHeaderCount:  state.requestHeaderCount,
		ResponseHeaderCount: state.responseHeaderCount,
		RequestBodyChunks:   state.requestBodyChunks,
		ResponseBodyChunks:  state.responseBodyChunks,
		RequestBodyBytes:    state.requestBodyBytes,
		ResponseBodyBytes:   state.responseBodyBytes,
		RequestEOS:          state.requestEOS,
		ResponseEOS:         state.responseEOS,
		ResponseCommitted:   state.responseCommitted,
		LateAction:          state.lateAction,
	})
}

type inspectingRequestBody struct {
	source io.ReadCloser
	state  *streamState
}

func (body *inspectingRequestBody) Read(buffer []byte) (int, error) {
	if len(buffer) > body.state.config.MaxRequestChunkBytes {
		buffer = buffer[:body.state.config.MaxRequestChunkBytes]
	}
	count, readErr := body.source.Read(buffer)
	if count > 0 {
		end := errors.Is(readErr, io.EOF)
		if err := body.state.processRequestBody(buffer[:count], end); err != nil {
			return 0, err
		}
	}
	if errors.Is(readErr, io.EOF) && count == 0 {
		if err := body.state.processRequestBody(nil, true); err != nil {
			return 0, err
		}
	}
	return count, readErr
}

func (body *inspectingRequestBody) Close() error {
	return body.source.Close()
}

type responseWriter struct {
	target http.ResponseWriter
	state  *streamState

	responseHeadersEvaluated bool
	committed                bool
	finished                 bool
	rejected                 bool
	hijacked                 bool
}

func newResponseWriter(target http.ResponseWriter, state *streamState) *responseWriter {
	return &responseWriter{target: target, state: state}
}

func (writer *responseWriter) Header() http.Header {
	return writer.target.Header()
}

func (writer *responseWriter) Unwrap() http.ResponseWriter {
	return writer.target
}

func (writer *responseWriter) WriteHeader(status int) {
	if writer.committed || writer.rejected {
		return
	}
	if !writer.prepareResponseHeaders(status) {
		return
	}
	writer.commit(status)
}

func (writer *responseWriter) Write(payload []byte) (int, error) {
	if writer.rejected {
		return 0, ErrResponseRejected
	}
	if len(payload) == 0 {
		writer.WriteHeader(http.StatusOK)
		if writer.rejected {
			return 0, ErrResponseRejected
		}
		return writer.target.Write(payload)
	}

	firstChunk := !writer.committed
	if firstChunk && !writer.prepareResponseHeaders(http.StatusOK) {
		return 0, ErrResponseRejected
	}

	written := 0
	for len(payload) > 0 {
		chunkLength := writer.state.config.MaxResponseChunkBytes
		if chunkLength > len(payload) {
			chunkLength = len(payload)
		}
		chunk := payload[:chunkLength]
		decision, err := writer.state.processResponseBody(chunk, false, !writer.committed)
		if err != nil {
			if !writer.committed {
				writer.writeFailure()
			}
			return written, err
		}
		if decision.disruptive() {
			writer.writeDecision(decision)
			return written, ErrResponseRejected
		}
		if !writer.committed {
			writer.commit(http.StatusOK)
		}
		count, writeErr := writer.target.Write(chunk)
		written += count
		if writeErr != nil {
			return written, writeErr
		}
		if count != len(chunk) {
			return written, io.ErrShortWrite
		}
		payload = payload[chunkLength:]
	}
	return written, nil
}

func (writer *responseWriter) prepareResponseHeaders(status int) bool {
	if writer.committed || writer.rejected || writer.responseHeadersEvaluated {
		return !writer.rejected
	}
	if decision, err := writer.state.pendingRequestResult(); err != nil {
		writer.writeFailure()
		return false
	} else if decision.disruptive() {
		writer.writeDecision(decision)
		return false
	}
	headers, err := boundedHeaders(writer.target.Header(), writer.state.config)
	if err != nil {
		writer.writeFailure()
		return false
	}
	decision, err := writer.state.processHeaders(DirectionResponse, headers, false)
	if err != nil {
		writer.writeFailure()
		return false
	}
	writer.responseHeadersEvaluated = true
	if decision.disruptive() {
		writer.writeDecision(decision)
		return false
	}
	return status >= 100 && status <= 999
}

func (writer *responseWriter) commit(status int) {
	if writer.committed || writer.rejected {
		return
	}
	writer.target.WriteHeader(status)
	writer.committed = true
	writer.state.markCommitted()
}

func (writer *responseWriter) writeFailure() {
	if writer.committed || writer.rejected {
		return
	}
	writer.clearHeaders()
	writer.target.Header().Set("Content-Type", "text/plain; charset=utf-8")
	writer.target.WriteHeader(http.StatusInternalServerError)
	writer.committed = true
	writer.rejected = true
	writer.state.markCommitted()
	_, _ = writer.target.Write([]byte("modsecurity middleware evaluation failed\n"))
}

func (writer *responseWriter) writeDecision(decision Decision) {
	if writer.committed || writer.rejected {
		return
	}
	writeDecision(writer.target, decision)
	writer.committed = true
	writer.rejected = true
	writer.state.markCommitted()
}

func (writer *responseWriter) clearHeaders() {
	for name := range writer.target.Header() {
		writer.target.Header().Del(name)
	}
}

func normalizeDecision(decision Decision) (int, string) {
	if decision.Action == ActionRedirect {
		location, err := url.Parse(decision.Location)
		if err == nil && location.String() != "" && !strings.ContainsAny(decision.Location, "\r\n") {
			status := decision.Status
			if status < 300 || status > 399 {
				status = http.StatusFound
			}
			return status, location.String()
		}
	}
	status := decision.Status
	if status < 400 || status > 599 {
		status = http.StatusForbidden
	}
	return status, ""
}

func writeDecision(target http.ResponseWriter, decision Decision) {
	status, location := normalizeDecision(decision)
	for name := range target.Header() {
		target.Header().Del(name)
	}
	if location != "" {
		target.Header().Set("Location", location)
	}
	target.Header().Set("Content-Type", "text/plain; charset=utf-8")
	target.WriteHeader(status)
	_, _ = target.Write([]byte("request rejected\n"))
}

// Flush preserves the http.Flusher surface. If the wrapped writer does not
// implement it, Flush is intentionally a no-op because http.Flusher cannot
// return ErrNotSupported. Unwrap lets http.ResponseController reach the
// underlying writer when it needs richer semantics.
func (writer *responseWriter) Flush() {
	if !writer.committed && !writer.rejected {
		writer.WriteHeader(http.StatusOK)
	}
	if flusher, ok := writer.target.(http.Flusher); ok {
		flusher.Flush()
	}
}

// Hijack preserves http.Hijacker. A hijacked connection has no inspectable
// HTTP response stream after takeover, so finish intentionally does not invent
// an end-of-stream event or a transport outcome.
func (writer *responseWriter) Hijack() (net.Conn, *bufio.ReadWriter, error) {
	hijacker, ok := writer.target.(http.Hijacker)
	if !ok {
		return nil, nil, http.ErrNotSupported
	}
	connection, buffer, err := hijacker.Hijack()
	if err == nil {
		writer.hijacked = true
	}
	return connection, buffer, err
}

// Push preserves http.Pusher without changing push semantics.
func (writer *responseWriter) Push(target string, options *http.PushOptions) error {
	pusher, ok := writer.target.(http.Pusher)
	if !ok {
		return http.ErrNotSupported
	}
	return pusher.Push(target, options)
}

// ReadFrom preserves io.ReaderFrom while retaining bounded inspection. Before
// commitment it reads exactly one bounded chunk, evaluates it, and then uses
// the wrapped writer's ReaderFrom for the remaining stream when available.
// That avoids full-response buffering and retains the underlying fast path for
// all but the bounded first chunk.
func (writer *responseWriter) ReadFrom(source io.Reader) (int64, error) {
	if writer.rejected {
		return 0, ErrResponseRejected
	}

	var total int64
	if !writer.committed {
		first := make([]byte, writer.state.config.MaxResponseChunkBytes)
		count, readErr := source.Read(first)
		if count > 0 {
			written, writeErr := writer.Write(first[:count])
			total += int64(written)
			if writeErr != nil {
				return total, writeErr
			}
			if written != count {
				return total, io.ErrShortWrite
			}
		}
		if errors.Is(readErr, io.EOF) {
			return total, nil
		}
		if readErr != nil {
			return total, readErr
		}
	}

	if readerFrom, ok := writer.target.(io.ReaderFrom); ok {
		inspected := &responseInspectionReader{source: source, writer: writer}
		count, err := readerFrom.ReadFrom(inspected)
		return total + count, err
	}
	count, err := copyIntoWriter(writer, source)
	return total + count, err
}

type responseInspectionReader struct {
	source io.Reader
	writer *responseWriter
}

func (reader *responseInspectionReader) Read(buffer []byte) (int, error) {
	if len(buffer) > reader.writer.state.config.MaxResponseChunkBytes {
		buffer = buffer[:reader.writer.state.config.MaxResponseChunkBytes]
	}
	count, readErr := reader.source.Read(buffer)
	if count > 0 {
		_, err := reader.writer.state.processResponseBody(buffer[:count], false, false)
		if err != nil {
			return 0, err
		}
	}
	if errors.Is(readErr, io.EOF) && count == 0 {
		_, err := reader.writer.state.processResponseBody(nil, true, false)
		if err != nil {
			return 0, err
		}
	}
	return count, readErr
}

func copyIntoWriter(writer *responseWriter, source io.Reader) (int64, error) {
	buffer := make([]byte, writer.state.config.MaxResponseChunkBytes)
	var total int64
	for {
		count, readErr := source.Read(buffer)
		if count > 0 {
			written, writeErr := writer.Write(buffer[:count])
			total += int64(written)
			if writeErr != nil {
				return total, writeErr
			}
			if written != count {
				return total, io.ErrShortWrite
			}
		}
		if errors.Is(readErr, io.EOF) {
			return total, nil
		}
		if readErr != nil {
			return total, readErr
		}
	}
}

func (writer *responseWriter) finish() {
	if writer.finished || writer.hijacked {
		return
	}
	writer.finished = true
	if writer.rejected {
		return
	}
	if !writer.committed {
		if !writer.prepareResponseHeaders(http.StatusOK) {
			return
		}
		decision, err := writer.state.processResponseBody(nil, true, true)
		if err != nil {
			writer.writeFailure()
			return
		}
		if decision.disruptive() {
			writer.writeDecision(decision)
			return
		}
		writer.commit(http.StatusOK)
		return
	}

	_, err := writer.state.processResponseBody(nil, true, false)
	if err != nil {
		// Response headers may already be committed. There is no safe replacement
		// status or claimed abort path here; Close records counters only.
		return
	}
}

func boundedHeaders(header http.Header, config Config) ([]Header, error) {
	names := make([]string, 0, len(header))
	for name := range header {
		names = append(names, name)
	}
	sort.Strings(names)
	values := make([]Header, 0, len(header))
	totalBytes := 0
	for _, name := range names {
		for _, value := range header.Values(name) {
			if len(values) >= config.MaxHeaderCount {
				return nil, errors.New("header count exceeds middleware limit")
			}
			totalBytes += len(name) + len(value)
			if totalBytes > config.MaxHeaderBytes {
				return nil, errors.New("header bytes exceed middleware limit")
			}
			values = append(values, Header{Name: name, Value: value})
		}
	}
	return values, nil
}

var (
	_ http.ResponseWriter = (*responseWriter)(nil)
	_ http.Flusher        = (*responseWriter)(nil)
	_ http.Hijacker       = (*responseWriter)(nil)
	_ http.Pusher         = (*responseWriter)(nil)
	_ io.ReaderFrom       = (*responseWriter)(nil)
)
