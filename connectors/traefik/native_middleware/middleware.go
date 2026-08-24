// Package native_middleware provides a repository-owned Traefik middleware
// entry point with a deliberately narrow, streaming engine seam.
//
// The public CreateConfig and New functions use Traefik's Go middleware
// shape: Traefik supplies an http.Handler and calls ServeHTTP for each
// request.  The package imports no Traefik internals, Common runtime code, or
// libmodsecurity. That keeps the source buildable as a local plugin package;
// the selected host probe reaches Common/libmodsecurity through a private
// persistent Unix-domain socket service instead. Source compilation alone is
// still not rule-evaluation or runtime evidence.
//
// Traefik's local-plugin loader resolves the exported constructor through the
// final module-path component. Keep this package name aligned with the
// “native_middleware“ directory/module suffix so the pinned host can load
// the plugin instead of treating it as an unregistered alternate source.
package native_middleware

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
	"strconv"
	"strings"
	"sync"
	"unicode"
)

const (
	defaultMaxHeaderCount        = 128
	defaultMaxHeaderBytes        = 64 << 10
	defaultMaxRequestChunkBytes  = 32 << 10
	defaultMaxResponseChunkBytes = 32 << 10
	// Keep the native middleware's aggregate request-body ceiling aligned with
	// the Common Runtime default hard body-buffer bound. A lower deployment
	// value is supported; a higher one would make the pre-engine guard weaker
	// than the repository-wide resource contract.
	defaultMaxRequestBodyBytes int64 = 1 << 20
	maximumMaxRequestBodyBytes int64 = 1 << 20
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
// EngineMode is either "passthrough" or "uds". The latter speaks only to the
// separately built persistent local engine service; it does not itself promote
// host-action or capability claims.
type Config struct {
	MaxHeaderCount        int    `json:"maxHeaderCount,omitempty"`
	MaxHeaderBytes        int    `json:"maxHeaderBytes,omitempty"`
	MaxRequestChunkBytes  int    `json:"maxRequestChunkBytes,omitempty"`
	MaxRequestBodyBytes   int64  `json:"maxRequestBodyBytes,omitempty"`
	MaxResponseChunkBytes int    `json:"maxResponseChunkBytes,omitempty"`
	TransactionIDHeader   string `json:"transactionIDHeader,omitempty"`
	EngineMode            string `json:"engineMode,omitempty"`
	EngineSocketPath      string `json:"engineSocketPath,omitempty"`
}

// CreateConfig returns safe bounded defaults. It is the standard Traefik Go
// plugin configuration entry point.
func CreateConfig() *Config {
	return &Config{
		MaxHeaderCount:        defaultMaxHeaderCount,
		MaxHeaderBytes:        defaultMaxHeaderBytes,
		MaxRequestChunkBytes:  defaultMaxRequestChunkBytes,
		MaxRequestBodyBytes:   defaultMaxRequestBodyBytes,
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
	applyConfigDefaults(&value)
	if err := validateConfigLimits(value); err != nil {
		return Config{}, err
	}
	if err := validateEngineConfig(value); err != nil {
		return Config{}, err
	}
	return value, nil
}

func applyConfigDefaults(value *Config) {
	if value == nil {
		return
	}
	if value.MaxHeaderCount == 0 {
		value.MaxHeaderCount = defaultMaxHeaderCount
	}
	if value.MaxHeaderBytes == 0 {
		value.MaxHeaderBytes = defaultMaxHeaderBytes
	}
	if value.MaxRequestChunkBytes == 0 {
		value.MaxRequestChunkBytes = defaultMaxRequestChunkBytes
	}
	if value.MaxRequestBodyBytes == 0 {
		value.MaxRequestBodyBytes = defaultMaxRequestBodyBytes
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

}

func validateConfigLimits(value Config) error {
	if value.MaxHeaderCount <= 0 || value.MaxHeaderBytes <= 0 ||
		value.MaxRequestChunkBytes <= 0 || value.MaxRequestBodyBytes <= 0 ||
		value.MaxResponseChunkBytes <= 0 {
		return errors.New("modsecurity native middleware: all limits must be positive")
	}
	if value.MaxRequestBodyBytes > maximumMaxRequestBodyBytes {
		return fmt.Errorf("modsecurity native middleware: maxRequestBodyBytes must not exceed %d", maximumMaxRequestBodyBytes)
	}
	if int64(value.MaxRequestChunkBytes) > value.MaxRequestBodyBytes {
		return errors.New("modsecurity native middleware: maxRequestChunkBytes must not exceed maxRequestBodyBytes")
	}
	if strings.TrimSpace(value.TransactionIDHeader) == "" {
		return errors.New("modsecurity native middleware: transactionIDHeader is required")
	}
	return nil
}

func validateEngineConfig(value Config) error {
	if value.EngineMode != "passthrough" && value.EngineMode != "uds" {
		return fmt.Errorf("modsecurity native middleware: unsupported engineMode %q", value.EngineMode)
	}
	if value.EngineMode == "uds" && !safeUnixSocketPath(value.EngineSocketPath) {
		return errors.New("modsecurity native middleware: engineSocketPath must be an absolute private path without parent segments")
	}
	if value.EngineMode == "uds" &&
		(value.MaxHeaderCount > udsMaxHeaders ||
			value.MaxHeaderBytes > udsMaxPayload ||
			value.MaxRequestChunkBytes > udsMaxChunk ||
			value.MaxResponseChunkBytes > udsMaxChunk) {
		return errors.New("modsecurity native middleware: uds limits exceed the local engine wire contract")
	}
	return nil
}

func safeUnixSocketPath(path string) bool {
	if !strings.HasPrefix(path, "/") || strings.ContainsRune(path, '\x00') {
		return false
	}
	for _, component := range strings.Split(path, "/") {
		if component == ".." {
			return false
		}
	}
	return true
}

// Direction keeps the engine seam independent of Traefik and HTTP plumbing.
type Direction string

const (
	DirectionRequest  Direction = "request"
	DirectionResponse Direction = "response"
)

// Header is a bounded borrowed view passed to a TransactionOpener callback. Implementers
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
	HTTPVersion   string
	Hostname      string
	ClientAddress string
	ClientPort    int
	ServerAddress string
	ServerPort    int
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

// TransactionOpener is the explicit bridge seam to Common/libmodsecurity.
// `uds` selects the persistent local service; PassthroughEngine remains the
// intentional source-only default. An opener receives bounded, incremental
// callbacks only and must never retain borrowed body slices.
type TransactionOpener interface {
	Open(context.Context, Metadata) (Transaction, error)
}

// Engine remains a source-compatible name for existing plugin consumers.
type Engine = TransactionOpener

// Transaction consumes the request/response lifecycle for one HTTP request.
// Body slices are borrowed and valid only for the duration of the callback.
type Transaction interface {
	ProcessHeaders(context.Context, Direction, []Header, bool) (Decision, error)
	ProcessBody(context.Context, Direction, []byte, bool) (Decision, error)
	Close(context.Context, Summary)
}

// responseHeaderProcessor carries the real host response status/version to
// engines that need Common Phase 3 input. Older test engines continue through
// Transaction.ProcessHeaders without an adapter-visible status.
type responseHeaderProcessor interface {
	ProcessResponseHeaders(context.Context, int, string, []Header) (Decision, error)
}

// responseCommitter receives host commit metadata immediately after
// the underlying ResponseWriter has accepted headers or body bytes.
type responseCommitter interface {
	SetResponseCommit(context.Context, bool, bool) error
}

// outcomeAcknowledger is deliberately a coordination seam only. It is called
// after a concrete host decision is written, or when a committed Phase-4
// decision is downgraded to log-only. It is not an evidence claim by itself.
type outcomeAcknowledger interface {
	AcknowledgeApplied(context.Context, Decision) error
	AcknowledgeLateLogOnly(context.Context, int) error
}

// PassthroughEngine is the intentional source-only default. It proves no
// Common/libmodsecurity integration and always allows traffic.
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

func (passthroughTransaction) Close(_ context.Context, _ Summary) {
	// Intentional no-op: this source-only engine owns no request resources.
}

// Middleware is an http.Handler suitable for Traefik's Go middleware API.
// New creates either PassthroughEngine or the configured UDS bridge. Tests may
// use NewWithEngine to supply an explicit engine implementation.
type Middleware struct {
	next   http.Handler
	config Config
	engine TransactionOpener
	name   string
}

// New is Traefik's Go plugin entry point. Its http.Handler return signature is
// intentionally the one expected by Traefik's Yaegi middleware contract. The
// full-lifecycle host probe selects this local plugin independently from the
// existing forwardAuth compatibility connector. `uds` selects a separately
// started persistent local engine-service; that selection alone is not a
// promoted capability or host-outcome claim.
func New(_ context.Context, next http.Handler, config *Config, name string) (http.Handler, error) {
	normalized, err := normalizedConfig(config)
	if err != nil {
		return nil, err
	}
	var engine TransactionOpener = PassthroughEngine{}
	if normalized.EngineMode == "uds" {
		engine = newUnixSocketEngine(normalized.EngineSocketPath)
	}
	return newMiddleware(next, normalized, name, engine)
}

// NewWithEngine is an explicit test/future-bridge seam. A nil TransactionOpener is never
// silently replaced because doing so would hide a missing security integration.
func NewWithEngine(next http.Handler, config *Config, name string, engine TransactionOpener) (*Middleware, error) {
	normalized, err := normalizedConfig(config)
	if err != nil {
		return nil, err
	}
	return newMiddleware(next, normalized, name, engine)
}

func newMiddleware(next http.Handler, config Config, name string, engine TransactionOpener) (*Middleware, error) {
	if next == nil {
		return nil, errors.New("modsecurity native middleware: next handler is required")
	}
	if engine == nil {
		return nil, errors.New("modsecurity native middleware: engine is required")
	}
	return &Middleware{next: next, config: config, engine: engine, name: name}, nil
}

// ServeHTTP evaluates headers and body chunks incrementally. It never collects
// a complete request or response body: request reads are capped, response
// writes are sliced for callbacks, and ReadFrom uses at most one bounded first
// chunk before delegating the remaining stream.
func (middleware *Middleware) ServeHTTP(writer http.ResponseWriter, request *http.Request) {
	requestContext := request.Context()
	metadata := Metadata{
		TransactionID: request.Header.Get(middleware.config.TransactionIDHeader),
		Method:        request.Method,
		RequestURI:    request.URL.RequestURI(),
		HTTPVersion:   request.Proto,
		Hostname:      request.Host,
	}
	metadata.ClientAddress, metadata.ClientPort = endpointFromAddress(request.RemoteAddr, 0)
	defaultServerPort := 80
	if request.TLS != nil {
		defaultServerPort = 443
	}
	metadata.ServerAddress, metadata.ServerPort = endpointFromAddress(request.Host, defaultServerPort)
	if metadata.ServerAddress == "" {
		metadata.ServerAddress = request.Host
	} else {
		metadata.Hostname = metadata.ServerAddress
	}
	transaction, err := middleware.engine.Open(requestContext, metadata)
	if err != nil {
		http.Error(writer, "modsecurity middleware engine unavailable", http.StatusInternalServerError)
		return
	}

	state := &streamState{
		config:   middleware.config,
		metadata: metadata,
		engine:   transaction,
	}
	defer state.close(requestContext)

	requestHeaders, err := boundedRequestHeaders(request.Header, request.Host, middleware.config)
	if err != nil {
		http.Error(writer, "request headers exceed middleware limits", http.StatusRequestHeaderFieldsTooLarge)
		return
	}
	// A zero Content-Length is not by itself proof that Body cannot yield
	// bytes: test adapters and nonstandard middleware can still provide a
	// readable body. Only nil or the canonical NoBody sentinel can skip the
	// bounded P2 reader without leaving a body-bearing bypass.
	requestEnd := request.Body == nil || request.Body == http.NoBody
	decision, err := state.processHeaders(requestContext, DirectionRequest, requestHeaders, requestEnd)
	if err != nil {
		http.Error(writer, "modsecurity middleware request-header evaluation failed", http.StatusInternalServerError)
		return
	}
	if decision.disruptive() {
		state.writeDecision(requestContext, writer, decision)
		return
	}
	if requestEnd {
		state.markRequestEOS()
	}

	response := newResponseWriter(request, writer, state)
	originalBody := request.Body
	if originalBody != nil {
		inspectingBody := &inspectingRequestBody{request: request, source: originalBody, state: state}
		state.requestBody = inspectingBody
		request.Body = inspectingBody
		defer func() { request.Body = originalBody }()
	}

	middleware.next.ServeHTTP(response, request)
	response.finish()
}

func endpointFromAddress(value string, fallbackPort int) (string, int) {
	if value == "" {
		return "", fallbackPort
	}
	host, portText, err := net.SplitHostPort(value)
	if err == nil {
		port := fallbackPort
		if parsed, parseErr := strconv.Atoi(portText); parseErr == nil && parsed >= 0 && parsed <= 65535 {
			port = parsed
		}
		return host, port
	}
	return strings.Trim(value, "[]"), fallbackPort
}

type streamState struct {
	mu       sync.Mutex
	config   Config
	metadata Metadata
	engine   Transaction

	requestHeaderCount  uint64
	responseHeaderCount uint64
	requestBodyChunks   uint64
	responseBodyChunks  uint64
	requestBodyBytes    int64
	responseBodyBytes   int64
	requestBody         *inspectingRequestBody
	requestEOS          bool
	responseEOS         bool
	responseCommitted   bool
	responseStatus      int
	lateAction          string

	pendingRequestDecision Decision
	pendingRequestError    error
	closed                 bool
}

func (state *streamState) processHeaders(contextValue context.Context, direction Direction, headers []Header, end bool) (Decision, error) {
	state.mu.Lock()
	defer state.mu.Unlock()
	if direction == DirectionRequest {
		state.requestHeaderCount += uint64(len(headers))
	} else {
		state.responseHeaderCount += uint64(len(headers))
	}
	return state.engine.ProcessHeaders(contextValue, direction, headers, end)
}

func (state *streamState) processResponseHeaders(contextValue context.Context, status int, headers []Header) (Decision, error) {
	state.mu.Lock()
	defer state.mu.Unlock()
	state.responseHeaderCount += uint64(len(headers))
	if processor, ok := state.engine.(responseHeaderProcessor); ok {
		return processor.ProcessResponseHeaders(contextValue, status, state.metadata.HTTPVersion, headers)
	}
	return state.engine.ProcessHeaders(contextValue, DirectionResponse, headers, false)
}

// processRequestBody returns an error only for a request-side rejection or an
// engine failure. The pending result is also retained so a handler that tries
// to write after Read returns can still be blocked before commitment.
func (state *streamState) processRequestBody(contextValue context.Context, chunk []byte, end bool) error {
	state.mu.Lock()
	defer state.mu.Unlock()
	if end && state.requestEOS {
		return nil
	}
	state.requestBodyChunks++
	state.requestBodyBytes += int64(len(chunk))
	// The aggregate body guard is intentionally applied before the engine
	// callback. Passing an over-limit chunk to the engine would let a P2 body
	// bypass the repository's reject-before-engine resource policy.
	if state.requestBodyBytes > state.config.MaxRequestBodyBytes {
		state.pendingRequestDecision = Decision{Action: ActionDeny, Status: http.StatusRequestEntityTooLarge}
		return ErrRequestRejected
	}
	decision, err := state.engine.ProcessBody(contextValue, DirectionRequest, chunk, end)
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
func (state *streamState) processResponseBody(contextValue context.Context, chunk []byte, end bool, beforeCommit bool) (Decision, error) {
	state.mu.Lock()
	defer state.mu.Unlock()
	if end && state.responseEOS {
		return allowDecision(), nil
	}
	state.responseBodyChunks++
	state.responseBodyBytes += int64(len(chunk))
	decision, err := state.engine.ProcessBody(contextValue, DirectionResponse, chunk, end)
	if end {
		state.responseEOS = true
	}
	if err != nil {
		return allowDecision(), err
	}
	if decision.disruptive() && !beforeCommit {
		state.lateAction = "log_only"
		if reporter, ok := state.engine.(outcomeAcknowledger); ok {
			_ = reporter.AcknowledgeLateLogOnly(contextValue, state.responseStatus)
		}
		return allowDecision(), nil
	}
	return decision, nil
}

func (state *streamState) pendingRequestResult() (Decision, error) {
	state.mu.Lock()
	defer state.mu.Unlock()
	return state.pendingRequestDecision, state.pendingRequestError
}

// ensureRequestEOS drains a body that the downstream handler did not consume.
// It is called immediately before response-header evaluation, so P3 and host
// response commitment cannot run ahead of the request-body phase. The drain
// uses the same bounded inspecting reader as normal handler reads and fails
// closed on source errors or a source that makes no progress.
func (state *streamState) ensureRequestEOS() error {
	state.mu.Lock()
	if state.requestEOS {
		state.mu.Unlock()
		return nil
	}
	body := state.requestBody
	state.mu.Unlock()
	if err := state.pendingRequestBlocker(); err != nil {
		return err
	}
	if body == nil {
		state.markRequestEOS()
		return nil
	}

	buffer := make([]byte, state.config.MaxRequestChunkBytes)
	for {
		count, readErr := body.Read(buffer)
		if readErr != nil && !errors.Is(readErr, io.EOF) {
			state.recordRequestError(readErr)
			return readErr
		}
		if errors.Is(readErr, io.EOF) {
			return nil
		}
		if count == 0 {
			err := errors.New("modsecurity native middleware: request body made no progress")
			state.recordRequestError(err)
			return err
		}
	}
}

// pendingRequestBlocker stops all further source reads after a disruptive P2
// result or request inspection error. In particular, a request that exceeds
// MaxRequestBodyBytes is not subsequently drained merely because its handler
// tries to send a response.
func (state *streamState) pendingRequestBlocker() error {
	state.mu.Lock()
	defer state.mu.Unlock()
	if state.pendingRequestDecision.disruptive() {
		return ErrRequestRejected
	}
	return state.pendingRequestError
}

func (state *streamState) recordRequestError(err error) {
	state.mu.Lock()
	state.pendingRequestError = err
	state.mu.Unlock()
}

func (state *streamState) markResponseCommit(contextValue context.Context, status int, headersSent bool, bodyStarted bool) {
	state.mu.Lock()
	if headersSent || bodyStarted {
		state.responseCommitted = true
	}
	if status >= 100 && status <= 999 {
		state.responseStatus = status
	}
	transaction := state.engine
	state.mu.Unlock()
	if committer, ok := transaction.(responseCommitter); ok {
		_ = committer.SetResponseCommit(contextValue, headersSent, bodyStarted)
	}
}

func (state *streamState) acknowledgeApplied(contextValue context.Context, decision Decision) {
	state.mu.Lock()
	transaction := state.engine
	state.mu.Unlock()
	if reporter, ok := transaction.(outcomeAcknowledger); ok {
		_ = reporter.AcknowledgeApplied(contextValue, decision)
	}
}

// writeDecision sends the selected pre-commit action to the actual
// ResponseWriter before reporting it to the engine. WriteHeader has no error
// result in net/http, so a complete successful body write is the strongest
// ResponseWriter confirmation available here. The engine receives the outcome
// while its Common commit state is still pre-action; only then do we publish
// the actual host commit. A failed or short body write still records only
// commit metadata and deliberately emits no host outcome.
func (state *streamState) writeDecision(contextValue context.Context, target http.ResponseWriter, decision Decision) {
	count, writeErr := writeDecision(target, decision)
	status, _ := normalizeDecision(decision)
	if writeErr == nil {
		state.acknowledgeApplied(contextValue, decision)
	}
	state.markResponseCommit(contextValue, status, true, count > 0)
}

func (state *streamState) markRequestEOS() {
	state.mu.Lock()
	state.requestEOS = true
	state.mu.Unlock()
}

func (state *streamState) close(contextValue context.Context) {
	state.mu.Lock()
	defer state.mu.Unlock()
	if state.closed {
		return
	}
	state.closed = true
	state.engine.Close(contextValue, Summary{
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
	request *http.Request
	source  io.ReadCloser
	state   *streamState
}

func (body *inspectingRequestBody) Read(buffer []byte) (int, error) {
	if err := body.state.pendingRequestBlocker(); err != nil {
		return 0, err
	}
	if len(buffer) > body.state.config.MaxRequestChunkBytes {
		buffer = buffer[:body.state.config.MaxRequestChunkBytes]
	}
	count, readErr := body.source.Read(buffer)
	if count > 0 {
		end := errors.Is(readErr, io.EOF)
		if err := body.state.processRequestBody(body.request.Context(), buffer[:count], end); err != nil {
			return 0, err
		}
	}
	if errors.Is(readErr, io.EOF) && count == 0 {
		if err := body.state.processRequestBody(body.request.Context(), nil, true); err != nil {
			return 0, err
		}
	}
	if readErr != nil && !errors.Is(readErr, io.EOF) {
		body.state.recordRequestError(readErr)
	}
	return count, readErr
}

func (body *inspectingRequestBody) Close() error {
	return body.source.Close()
}

type responseWriter struct {
	request *http.Request
	target  http.ResponseWriter
	state   *streamState

	responseHeadersEvaluated bool
	committed                bool
	finished                 bool
	rejected                 bool
	hijacked                 bool
	// responseIncomplete is set only when the wrapped host writer or a source
	// stream reports that it could not complete the response.  In particular,
	// it keeps a downstream disconnect, short write, or upstream ReadFrom error
	// from being converted into a synthetic response EOS.  The transaction is
	// still closed exactly once by ServeHTTP's defer, but the engine never gets
	// a false end-of-stream callback for an incomplete host response.
	responseIncomplete bool
}

func newResponseWriter(request *http.Request, target http.ResponseWriter, state *streamState) *responseWriter {
	return &responseWriter{request: request, target: target, state: state}
}

func (writer *responseWriter) requestContext() context.Context {
	return writer.request.Context()
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
		// A pre-commit decision is already visible to the downstream client.
		// Consume the proxy's attempted response stream without forwarding it so
		// its upstream handler does not replace the selected denial with a 5xx.
		return len(payload), nil
	}
	if len(payload) == 0 {
		return writer.writeEmptyResponse()
	}
	written, rejected, err := writer.writeResponseChunks(payload)
	if rejected {
		return len(payload), nil
	}
	return written, err
}

func (writer *responseWriter) writeEmptyResponse() (int, error) {
	writer.WriteHeader(http.StatusOK)
	if writer.rejected {
		return 0, ErrResponseRejected
	}
	return writer.target.Write(nil)
}

func (writer *responseWriter) writeResponseChunks(payload []byte) (int, bool, error) {
	if !writer.committed && !writer.prepareResponseHeaders(http.StatusOK) {
		return 0, writer.rejected, ErrResponseRejected
	}
	written := 0
	for len(payload) > 0 {
		chunkLength := len(payload)
		if chunkLength > writer.state.config.MaxResponseChunkBytes {
			chunkLength = writer.state.config.MaxResponseChunkBytes
		}
		count, rejected, err := writer.writeResponseChunk(payload[:chunkLength])
		written += count
		if err != nil || rejected {
			return written, rejected, err
		}
		payload = payload[chunkLength:]
	}
	return written, false, nil
}

func (writer *responseWriter) writeResponseChunk(chunk []byte) (int, bool, error) {
	decision, err := writer.state.processResponseBody(writer.requestContext(), chunk, false, !writer.committed)
	if err != nil {
		if !writer.committed {
			writer.writeFailure()
		}
		return 0, false, err
	}
	if decision.disruptive() {
		writer.writeDecision(decision)
		return 0, true, nil
	}
	if !writer.committed {
		writer.commit(http.StatusOK)
	}
	count, writeErr := writer.target.Write(chunk)
	if count > 0 {
		writer.state.markResponseCommit(writer.requestContext(), 0, true, true)
		// Traefik's native forwarding path may otherwise retain a small response
		// chunk until upstream EOS. Flush only bytes the host accepted so a
		// committed streaming response remains observable before upstream EOF.
		if flusher, ok := writer.target.(http.Flusher); ok {
			flusher.Flush()
		}
	}
	if writeErr != nil {
		writer.responseIncomplete = true
		return count, false, writeErr
	}
	if count != len(chunk) {
		writer.responseIncomplete = true
		return count, false, io.ErrShortWrite
	}
	return count, false, nil
}

func (writer *responseWriter) prepareResponseHeaders(status int) bool {
	if writer.committed || writer.rejected || writer.responseHeadersEvaluated {
		return !writer.rejected
	}
	if err := writer.state.ensureRequestEOS(); err != nil {
		if decision, _ := writer.state.pendingRequestResult(); decision.disruptive() {
			writer.writeDecision(decision)
		} else {
			writer.writeFailure()
		}
		return false
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
	decision, err := writer.state.processResponseHeaders(writer.requestContext(), status, headers)
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
	writer.state.markResponseCommit(writer.requestContext(), status, true, false)
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
	count, _ := writer.target.Write([]byte("modsecurity middleware evaluation failed\n"))
	writer.state.markResponseCommit(writer.requestContext(), http.StatusInternalServerError, true, count > 0)
}

func (writer *responseWriter) writeDecision(decision Decision) {
	if writer.committed || writer.rejected {
		return
	}
	writer.committed = true
	writer.rejected = true
	writer.state.writeDecision(writer.requestContext(), writer.target, decision)
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

func writeDecision(target http.ResponseWriter, decision Decision) (int, error) {
	status, location := normalizeDecision(decision)
	for name := range target.Header() {
		target.Header().Del(name)
	}
	if location != "" {
		target.Header().Set("Location", location)
	}
	target.Header().Set("Content-Type", "text/plain; charset=utf-8")
	target.WriteHeader(status)
	count, err := target.Write([]byte("request rejected\n"))
	if err == nil && count != len("request rejected\n") {
		err = io.ErrShortWrite
	}
	return count, err
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
func (writer *responseWriter) consumeInitialReadFromChunk(source io.Reader) (int64, bool, error) {
	if writer.committed {
		return 0, false, nil
	}
	first := make([]byte, writer.state.config.MaxResponseChunkBytes)
	count, readErr := source.Read(first)
	total, writeErr := writer.writeInitialReadFromBytes(first[:count], count)
	if writeErr != nil {
		return total, true, writeErr
	}
	if errors.Is(readErr, io.EOF) {
		return total, true, nil
	}
	if readErr != nil {
		return total, true, readErr
	}
	if writer.rejected {
		count, err := io.Copy(io.Discard, source)
		return total + count, true, err
	}
	return total, false, nil
}

func (writer *responseWriter) writeInitialReadFromBytes(first []byte, count int) (int64, error) {
	if count == 0 {
		return 0, nil
	}
	written, err := writer.Write(first)
	if err != nil {
		return int64(written), err
	}
	if written != count {
		return int64(written), io.ErrShortWrite
	}
	return int64(written), nil
}

func (writer *responseWriter) ReadFrom(source io.Reader) (int64, error) {
	if writer.rejected {
		return io.Copy(io.Discard, source)
	}
	total, complete, err := writer.consumeInitialReadFromChunk(source)
	if complete {
		return total, err
	}

	if readerFrom, ok := writer.target.(io.ReaderFrom); ok {
		inspected := &responseInspectionReader{source: source, writer: writer}
		count, err := readerFrom.ReadFrom(inspected)
		if count > 0 {
			writer.state.markResponseCommit(writer.requestContext(), 0, true, true)
		}
		if err != nil {
			// ReaderFrom may surface either an upstream read failure or a
			// downstream write failure.  Neither is evidence that the response
			// reached EOS, so do not send a later synthetic EOS callback.
			writer.responseIncomplete = true
		}
		return total + count, err
	}
	count, err := copyIntoWriter(writer, source)
	if err != nil {
		writer.responseIncomplete = true
	}
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
		_, err := reader.writer.state.processResponseBody(reader.writer.requestContext(), buffer[:count], false, false)
		if err != nil {
			return 0, err
		}
	}
	if errors.Is(readErr, io.EOF) && count == 0 {
		_, err := reader.writer.state.processResponseBody(reader.writer.requestContext(), nil, true, false)
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
	if writer.responseIncomplete {
		// A real host-side read/write failure is not normal completion.  Do not
		// claim EOS or turn it into a late intervention result; Close will
		// release the per-request engine session through its normal idempotent
		// cleanup path.
		return
	}
	if writer.rejected {
		return
	}
	if !writer.committed {
		if !writer.prepareResponseHeaders(http.StatusOK) {
			return
		}
		decision, err := writer.state.processResponseBody(writer.requestContext(), nil, true, true)
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

	_, err := writer.state.processResponseBody(writer.requestContext(), nil, true, false)
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

// boundedRequestHeaders includes the authority from net/http's separate Host
// field when the incoming Header map does not contain an ordinary Host entry.
// Server requests normally omit Host from Header, but ModSecurity evaluates
// it as REQUEST_HEADERS:Host. The authority is copied only after validating
// it as a bounded header value; an existing Host entry always wins and is
// never duplicated.
func boundedRequestHeaders(header http.Header, authority string, config Config) ([]Header, error) {
	hostEntries := 0
	for name, values := range header {
		if !strings.EqualFold(name, "Host") {
			continue
		}
		hostEntries += len(values)
	}
	if hostEntries > 1 {
		return nil, errors.New("ambiguous Host header")
	}
	if hostEntries == 1 || authority == "" {
		return boundedHeaders(header, config)
	}
	if invalidHostAuthority(authority) {
		return nil, errors.New("invalid Host authority")
	}
	withHost := make(http.Header, len(header)+1)
	for name, values := range header {
		withHost[name] = append([]string(nil), values...)
	}
	withHost["Host"] = []string{authority}
	return boundedHeaders(withHost, config)
}

func invalidHostAuthority(value string) bool {
	if strings.TrimSpace(value) != value {
		return true
	}
	return strings.IndexFunc(value, func(r rune) bool {
		return r < 0x20 || r == 0x7f || unicode.IsSpace(r)
	}) >= 0
}

var (
	_ http.ResponseWriter = (*responseWriter)(nil)
	_ http.Flusher        = (*responseWriter)(nil)
	_ http.Hijacker       = (*responseWriter)(nil)
	_ http.Pusher         = (*responseWriter)(nil)
	_ io.ReaderFrom       = (*responseWriter)(nil)
)
