package native_middleware

import (
	"bufio"
	"bytes"
	"context"
	"errors"
	"io"
	"net"
	"net/http"
	"net/http/httptest"
	"reflect"
	"strings"
	"testing"
)

type headerCall struct {
	direction Direction
	end       bool
	count     int
}

type bodyCall struct {
	direction Direction
	end       bool
	length    int
}

type recordingTransaction struct {
	headerCalls    []headerCall
	headerValues   [][]Header
	bodyCalls      []bodyCall
	events         []string
	contexts       []context.Context
	closed         []Summary
	headerDecision func(Direction, []Header, bool) Decision
	bodyDecision   func(Direction, []byte, bool) Decision
}

func (transaction *recordingTransaction) ProcessHeaders(value context.Context, direction Direction, headers []Header, end bool) (Decision, error) {
	transaction.contexts = append(transaction.contexts, value)
	transaction.headerCalls = append(transaction.headerCalls, headerCall{direction: direction, end: end, count: len(headers)})
	transaction.headerValues = append(transaction.headerValues, append([]Header(nil), headers...))
	transaction.events = append(transaction.events, string(direction)+"-headers")
	if transaction.headerDecision != nil {
		return transaction.headerDecision(direction, headers, end), nil
	}
	return allowDecision(), nil
}

func requestHeaderValues(transaction *recordingTransaction) []Header {
	for index, call := range transaction.headerCalls {
		if call.direction == DirectionRequest {
			return transaction.headerValues[index]
		}
	}
	return nil
}

func TestMiddlewareForwardsRequestAuthorityAsHostHeader(t *testing.T) {
	transaction := &recordingTransaction{}
	middleware := newTestMiddleware(t, http.HandlerFunc(func(writer http.ResponseWriter, _ *http.Request) {
		writer.WriteHeader(http.StatusNoContent)
	}), transaction)
	request := httptest.NewRequest(http.MethodGet, "http://authority.example:8443/resource", nil)
	if request.Header.Get("Host") != "" {
		t.Fatal("httptest request unexpectedly stored authority in Header")
	}

	response := httptest.NewRecorder()
	middleware.ServeHTTP(response, request)

	if got, want := response.Code, http.StatusNoContent; got != want {
		t.Fatalf("status = %d, want %d", got, want)
	}
	var hosts []string
	for _, header := range requestHeaderValues(transaction) {
		if strings.EqualFold(header.Name, "Host") {
			hosts = append(hosts, header.Value)
		}
	}
	if got, want := hosts, []string{"authority.example:8443"}; !reflect.DeepEqual(got, want) {
		t.Fatalf("forwarded Host values = %#v, want %#v", got, want)
	}
}

func TestMiddlewarePreservesExistingHostHeaderWithoutAuthorityDuplicate(t *testing.T) {
	transaction := &recordingTransaction{}
	middleware := newTestMiddleware(t, http.HandlerFunc(func(writer http.ResponseWriter, _ *http.Request) {
		writer.WriteHeader(http.StatusNoContent)
	}), transaction)
	request := httptest.NewRequest(http.MethodGet, "http://authority.example/resource", nil)
	request.Host = "authority.example"
	request.Header.Set("Host", "header.example")

	middleware.ServeHTTP(httptest.NewRecorder(), request)

	var hosts []string
	for _, header := range requestHeaderValues(transaction) {
		if strings.EqualFold(header.Name, "Host") {
			hosts = append(hosts, header.Value)
		}
	}
	if got, want := hosts, []string{"header.example"}; !reflect.DeepEqual(got, want) {
		t.Fatalf("preserved Host values = %#v, want %#v", got, want)
	}
}

func TestMiddlewareRejectsInvalidAuthorityBeforeEngineHeaders(t *testing.T) {
	transaction := &recordingTransaction{}
	nextCalled := false
	middleware := newTestMiddleware(t, http.HandlerFunc(func(http.ResponseWriter, *http.Request) {
		nextCalled = true
	}), transaction)
	request := httptest.NewRequest(http.MethodGet, "http://authority.example/resource", nil)
	request.Host = "authority.example\r\nInjected: yes"
	response := httptest.NewRecorder()

	middleware.ServeHTTP(response, request)

	if nextCalled {
		t.Fatal("next handler ran for invalid authority")
	}
	if got, want := response.Code, http.StatusRequestHeaderFieldsTooLarge; got != want {
		t.Fatalf("status = %d, want %d", got, want)
	}
}

func (transaction *recordingTransaction) ProcessBody(value context.Context, direction Direction, body []byte, end bool) (Decision, error) {
	transaction.contexts = append(transaction.contexts, value)
	transaction.bodyCalls = append(transaction.bodyCalls, bodyCall{direction: direction, end: end, length: len(body)})
	transaction.events = append(transaction.events, string(direction)+"-body")
	if transaction.bodyDecision != nil {
		return transaction.bodyDecision(direction, body, end), nil
	}
	return allowDecision(), nil
}

func (transaction *recordingTransaction) Close(value context.Context, summary Summary) {
	transaction.contexts = append(transaction.contexts, value)
	transaction.closed = append(transaction.closed, summary)
}

type recordingEngine struct {
	transaction *recordingTransaction
}

func (engine recordingEngine) Open(_ context.Context, _ Metadata) (Transaction, error) {
	return engine.transaction, nil
}

func TestTraefikMiddlewareEntryPointSignature(t *testing.T) {
	var entryPoint func(context.Context, http.Handler, *Config, string) (http.Handler, error) = New
	if entryPoint == nil {
		t.Fatal("Traefik middleware New entry point is nil")
	}
}

func newTestMiddleware(t *testing.T, next http.Handler, transaction *recordingTransaction) *Middleware {
	return newTestMiddlewareWithRequestBodyLimit(t, next, transaction, defaultMaxRequestBodyBytes)
}

func newTestMiddlewareWithRequestBodyLimit(t *testing.T, next http.Handler, transaction *recordingTransaction, requestBodyLimit int64) *Middleware {
	t.Helper()
	config := CreateConfig()
	config.MaxRequestChunkBytes = 3
	config.MaxRequestBodyBytes = requestBodyLimit
	config.MaxResponseChunkBytes = 2
	middleware, err := NewWithEngine(next, config, "test", recordingEngine{transaction: transaction})
	if err != nil {
		t.Fatalf("NewWithEngine() error = %v", err)
	}
	return middleware
}

type trackingRequestBody struct {
	reader    *strings.Reader
	readBytes int
}

func newTrackingRequestBody(payload string) *trackingRequestBody {
	return &trackingRequestBody{reader: strings.NewReader(payload)}
}

func (body *trackingRequestBody) Read(buffer []byte) (int, error) {
	count, err := body.reader.Read(buffer)
	body.readBytes += count
	return count, err
}

func (*trackingRequestBody) Close() error { return nil }

func TestMiddlewareStreamsRequestAndResponseInBoundedChunks(t *testing.T) {
	transaction := &recordingTransaction{}
	middleware := newTestMiddleware(t, boundedChunksHandler(t), transaction)

	request := httptest.NewRequest(http.MethodPost, "http://example.test/stream", strings.NewReader("request"))
	request.Header.Set("X-Request-Id", "transaction-1")
	response := httptest.NewRecorder()
	middleware.ServeHTTP(response, request)

	assertBoundedChunkResponse(t, response, transaction)
}

func boundedChunksHandler(t *testing.T) http.Handler {
	t.Helper()
	return http.HandlerFunc(func(writer http.ResponseWriter, request *http.Request) {
		body, err := io.ReadAll(request.Body)
		if err != nil {
			t.Errorf("ReadAll(request.Body) error = %v", err)
			return
		}
		if got, want := string(body), "request"; got != want {
			t.Errorf("request body = %q, want %q", got, want)
		}
		if _, err := writer.Write([]byte("result")); err != nil {
			t.Errorf("Write() error = %v", err)
		}
	})
}

func assertBoundedChunkResponse(t *testing.T, response *httptest.ResponseRecorder, transaction *recordingTransaction) {
	t.Helper()
	if got, want := response.Code, http.StatusOK; got != want {
		t.Fatalf("status = %d, want %d", got, want)
	}
	if got, want := response.Body.String(), "result"; got != want {
		t.Fatalf("response body = %q, want %q", got, want)
	}
	assertBoundedBodies(t, transaction.bodyCalls, DirectionRequest, 3, len("request"))
	assertBoundedBodies(t, transaction.bodyCalls, DirectionResponse, 2, len("result"))
	if len(transaction.closed) != 1 {
		t.Fatalf("Close calls = %d, want 1", len(transaction.closed))
	}
	summary := transaction.closed[0]
	if summary.RequestBodyBytes != int64(len("request")) || summary.ResponseBodyBytes != int64(len("result")) {
		t.Fatalf("unexpected body counters: %#v", summary)
	}
	if !summary.RequestEOS || !summary.ResponseEOS || !summary.ResponseCommitted {
		t.Fatalf("expected complete committed summary, got %#v", summary)
	}
	assertRequestBodyCallbacks(t, transaction)
}

func assertRequestBodyCallbacks(t *testing.T, transaction *recordingTransaction) {
	t.Helper()
	requestBodyEvents := 0
	requestBodyEndEvents := 0
	requestBodyBytes := 0
	for _, event := range transaction.events {
		if event == "request-body" {
			requestBodyEvents++
		}
	}
	for _, call := range transaction.bodyCalls {
		if call.direction != DirectionRequest {
			continue
		}
		requestBodyBytes += call.length
		if call.end {
			requestBodyEndEvents++
		}
	}
	if requestBodyEvents == 0 || requestBodyBytes != len("request") || requestBodyEndEvents != 1 {
		t.Fatalf("request body callbacks did not reach one EOS without duplication: events=%d bytes=%d eos=%d", requestBodyEvents, requestBodyBytes, requestBodyEndEvents)
	}
}

func TestMiddlewareDrainsRequestBeforeResponseHeadersWhenHandlerSkipsBody(t *testing.T) {
	transaction := &recordingTransaction{}
	middleware := newTestMiddleware(t, http.HandlerFunc(func(writer http.ResponseWriter, _ *http.Request) {
		writer.WriteHeader(http.StatusNoContent)
	}), transaction)
	request := httptest.NewRequest(http.MethodPost, "http://example.test/ordering", strings.NewReader("request"))
	middleware.ServeHTTP(httptest.NewRecorder(), request)

	lastRequestBody := -1
	firstResponseHeaders := -1
	for index, event := range transaction.events {
		if event == "request-body" {
			lastRequestBody = index
		}
		if event == "response-headers" && firstResponseHeaders < 0 {
			firstResponseHeaders = index
		}
	}
	if lastRequestBody < 0 || firstResponseHeaders < 0 || lastRequestBody >= firstResponseHeaders {
		t.Fatalf("request body was not drained before response headers: events=%v", transaction.events)
	}
	if len(transaction.closed) != 1 || !transaction.closed[0].RequestEOS {
		t.Fatalf("request EOS was not recorded after pre-commit drain: %#v", transaction.closed)
	}
}

func TestMiddlewareAllowsInLimitRequestBodyBeforeResponseHeaders(t *testing.T) {
	transaction := &recordingTransaction{}
	middleware := newTestMiddlewareWithRequestBodyLimit(t, http.HandlerFunc(func(writer http.ResponseWriter, request *http.Request) {
		if _, err := io.ReadAll(request.Body); err != nil {
			t.Errorf("ReadAll(request.Body) error = %v", err)
			return
		}
		writer.WriteHeader(http.StatusNoContent)
	}), transaction, int64(len("request")))
	source := newTrackingRequestBody("request")
	request := httptest.NewRequest(http.MethodPost, "http://example.test/in-limit", nil)
	request.ContentLength = int64(len("request"))
	request.Body = source
	response := httptest.NewRecorder()
	middleware.ServeHTTP(response, request)

	if got, want := response.Code, http.StatusNoContent; got != want {
		t.Fatalf("status = %d, want %d", got, want)
	}
	if got, want := source.readBytes, len("request"); got != want {
		t.Fatalf("source bytes = %d, want %d", got, want)
	}
	if len(transaction.closed) != 1 || !transaction.closed[0].RequestEOS {
		t.Fatalf("in-limit request did not complete at EOS: %#v", transaction.closed)
	}
}

func TestMiddlewareRejectsOverLimitBodyDuringSkippedHandlerDrain(t *testing.T) {
	transaction := &recordingTransaction{}
	middleware := newTestMiddlewareWithRequestBodyLimit(t, http.HandlerFunc(func(writer http.ResponseWriter, _ *http.Request) {
		writer.WriteHeader(http.StatusNoContent)
	}), transaction, 5)
	source := newTrackingRequestBody("request")
	request := httptest.NewRequest(http.MethodPost, "http://example.test/over-limit-drain", nil)
	request.ContentLength = int64(len("request"))
	request.Body = source
	response := httptest.NewRecorder()
	middleware.ServeHTTP(response, request)

	assertOverLimitRequestRejectedBeforeP3(t, transaction, response, source, len("request"))
}

func TestMiddlewareRejectsOverLimitBodyReadByHandlerWithoutFurtherDrain(t *testing.T) {
	transaction := &recordingTransaction{}
	middleware := newTestMiddlewareWithRequestBodyLimit(t, http.HandlerFunc(func(writer http.ResponseWriter, request *http.Request) {
		if _, err := io.ReadAll(request.Body); !errors.Is(err, ErrRequestRejected) {
			t.Errorf("ReadAll(request.Body) error = %v, want ErrRequestRejected", err)
		}
		writer.WriteHeader(http.StatusNoContent)
	}), transaction, 5)
	source := newTrackingRequestBody("request")
	request := httptest.NewRequest(http.MethodPost, "http://example.test/over-limit-handler", nil)
	request.ContentLength = int64(len("request"))
	request.Body = source
	response := httptest.NewRecorder()
	middleware.ServeHTTP(response, request)

	assertOverLimitRequestRejectedBeforeP3(t, transaction, response, source, len("request"))
}

func assertOverLimitRequestRejectedBeforeP3(t *testing.T, transaction *recordingTransaction, response *httptest.ResponseRecorder, source *trackingRequestBody, inputBytes int) {
	t.Helper()
	if got, want := response.Code, http.StatusRequestEntityTooLarge; got != want {
		t.Fatalf("status = %d, want body-limit status %d", got, want)
	}
	if source.readBytes >= inputBytes {
		t.Fatalf("over-limit source was fully drained: read=%d input=%d", source.readBytes, inputBytes)
	}
	for _, event := range transaction.events {
		if event == "response-headers" {
			t.Fatalf("P3 ran after request body limit rejection: events=%v", transaction.events)
		}
	}
	if len(transaction.closed) != 1 || transaction.closed[0].RequestEOS {
		t.Fatalf("over-limit request incorrectly reached EOS: %#v", transaction.closed)
	}
	engineRequestBytes := 0
	for _, call := range transaction.bodyCalls {
		if call.direction == DirectionRequest {
			engineRequestBytes += call.length
		}
	}
	if got, want := engineRequestBytes, 3; got != want {
		t.Fatalf("over-limit chunk reached engine: engine request bytes=%d, want only first bounded chunk=%d", got, want)
	}
}

func TestMiddlewareConfigRejectsOutOfRangeRequestBodyLimit(t *testing.T) {
	config := CreateConfig()
	if config.MaxRequestBodyBytes != defaultMaxRequestBodyBytes {
		t.Fatalf("default max request body bytes = %d, want %d", config.MaxRequestBodyBytes, defaultMaxRequestBodyBytes)
	}
	config.MaxRequestBodyBytes = maximumMaxRequestBodyBytes + 1
	if _, err := normalizedConfig(config); err == nil {
		t.Fatal("normalizedConfig accepted a request body limit above the finite cap")
	}
	config = CreateConfig()
	config.MaxRequestBodyBytes = -1
	if _, err := normalizedConfig(config); err == nil {
		t.Fatal("normalizedConfig accepted a non-positive request body limit")
	}
	config = CreateConfig()
	config.MaxRequestBodyBytes = 2
	if _, err := normalizedConfig(config); err == nil {
		t.Fatal("normalizedConfig accepted a request chunk larger than the aggregate request body limit")
	}
}

type failingRequestBody struct{}

func (failingRequestBody) Read([]byte) (int, error) {
	return 0, errors.New("synthetic request-body read failure")
}

func (failingRequestBody) Close() error { return nil }

func TestMiddlewareFailsClosedWhenPreCommitRequestDrainFails(t *testing.T) {
	transaction := &recordingTransaction{}
	nextCalled := false
	middleware := newTestMiddleware(t, http.HandlerFunc(func(writer http.ResponseWriter, _ *http.Request) {
		nextCalled = true
		writer.WriteHeader(http.StatusNoContent)
	}), transaction)
	request := httptest.NewRequest(http.MethodPost, "http://example.test/drain-error", nil)
	request.ContentLength = -1
	request.Body = failingRequestBody{}
	response := httptest.NewRecorder()
	middleware.ServeHTTP(response, request)

	if !nextCalled {
		t.Fatal("next handler was not reached before its response triggered the drain")
	}
	if got, want := response.Code, http.StatusInternalServerError; got != want {
		t.Fatalf("status = %d, want fail-closed status %d", got, want)
	}
	for _, event := range transaction.events {
		if event == "response-headers" {
			t.Fatalf("response headers evaluated after request drain failure: events=%v", transaction.events)
		}
	}
}

func TestMiddlewareKeepsBodyDecisionWhenPreCommitDrainFindsP2Deny(t *testing.T) {
	transaction := &recordingTransaction{
		bodyDecision: func(direction Direction, _ []byte, _ bool) Decision {
			if direction == DirectionRequest {
				return Decision{Action: ActionDeny, Status: http.StatusForbidden}
			}
			return allowDecision()
		},
	}
	middleware := newTestMiddleware(t, http.HandlerFunc(func(writer http.ResponseWriter, _ *http.Request) {
		writer.WriteHeader(http.StatusNoContent)
	}), transaction)
	response := httptest.NewRecorder()
	request := httptest.NewRequest(http.MethodPost, "http://example.test/p2-deny", strings.NewReader("request"))
	middleware.ServeHTTP(response, request)

	if got, want := response.Code, http.StatusForbidden; got != want {
		t.Fatalf("status = %d, want preserved P2 denial %d", got, want)
	}
	if len(transaction.events) == 0 {
		t.Fatal("body decision produced no engine event")
	}
	for _, event := range transaction.events {
		if event == "response-headers" {
			t.Fatalf("response headers evaluated after P2 denial: events=%v", transaction.events)
		}
	}
}

func TestMiddlewareMarksEmptyRequestEOSWithoutBodyCallback(t *testing.T) {
	transaction := &recordingTransaction{}
	middleware := newTestMiddleware(t, http.HandlerFunc(func(writer http.ResponseWriter, _ *http.Request) {
		writer.WriteHeader(http.StatusNoContent)
	}), transaction)
	middleware.ServeHTTP(httptest.NewRecorder(), httptest.NewRequest(http.MethodGet, "http://example.test/empty", nil))

	if len(transaction.closed) != 1 || !transaction.closed[0].RequestEOS {
		t.Fatalf("empty request was not closed at request EOS: %#v", transaction.closed)
	}
	for _, call := range transaction.bodyCalls {
		if call.direction == DirectionRequest {
			t.Fatalf("empty request unexpectedly produced request-body callback: %#v", transaction.bodyCalls)
		}
	}
}

func TestMiddlewareInspectsReadableZeroLengthBodyBeforeP3(t *testing.T) {
	transaction := &recordingTransaction{}
	middleware := newTestMiddleware(t, http.HandlerFunc(func(writer http.ResponseWriter, _ *http.Request) {
		writer.WriteHeader(http.StatusNoContent)
	}), transaction)
	request := httptest.NewRequest(http.MethodPost, "http://example.test/zero-length-body", nil)
	request.ContentLength = 0
	request.Body = io.NopCloser(strings.NewReader(""))
	middleware.ServeHTTP(httptest.NewRecorder(), request)

	if len(transaction.closed) != 1 || !transaction.closed[0].RequestEOS {
		t.Fatalf("readable zero-length body did not reach request EOS: %#v", transaction.closed)
	}
	lastRequestBody := -1
	firstResponseHeaders := -1
	for index, event := range transaction.events {
		if event == "request-body" {
			lastRequestBody = index
		}
		if event == "response-headers" && firstResponseHeaders < 0 {
			firstResponseHeaders = index
		}
	}
	if lastRequestBody < 0 || firstResponseHeaders < 0 || lastRequestBody >= firstResponseHeaders {
		t.Fatalf("readable zero-length body bypassed P2 before P3: events=%v", transaction.events)
	}
}

func TestMiddlewarePreservesRequestContextForEveryEngineCallback(t *testing.T) {
	type requestContextKey struct{}
	key := requestContextKey{}
	requestContext := context.WithValue(context.Background(), key, "request-scope")
	transaction := &recordingTransaction{}
	middleware := newTestMiddleware(t, http.HandlerFunc(func(writer http.ResponseWriter, _ *http.Request) {
		_, _ = writer.Write([]byte("response"))
	}), transaction)
	request := httptest.NewRequest(http.MethodGet, "http://example.test/context", nil).WithContext(requestContext)

	middleware.ServeHTTP(httptest.NewRecorder(), request)

	if len(transaction.contexts) == 0 {
		t.Fatal("engine did not receive a request context")
	}
	for _, value := range transaction.contexts {
		if got, want := value.Value(key), "request-scope"; got != want {
			t.Fatalf("engine callback context value = %q, want %q", got, want)
		}
	}
}

func TestInspectingRequestBodyUsesDirectContext(t *testing.T) {
	type requestContextKey struct{}
	key := requestContextKey{}
	requestContext := context.WithValue(context.Background(), key, "request-body-scope")
	transaction := &recordingTransaction{}
	request := httptest.NewRequest(http.MethodPost, "http://example.test/request-body", nil).WithContext(requestContext)
	body := &inspectingRequestBody{
		request: request,
		source:  io.NopCloser(strings.NewReader("body")),
		state: &streamState{
			config: mustTestConfig(t),
			engine: transaction,
		},
	}

	if _, err := io.ReadAll(body); err != nil {
		t.Fatalf("ReadAll(body) error = %v", err)
	}
	if len(transaction.contexts) == 0 {
		t.Fatal("request-body processor did not receive a context")
	}
	for _, value := range transaction.contexts {
		if got, want := value.Value(key), "request-body-scope"; got != want {
			t.Fatalf("request-body context value = %q, want %q", got, want)
		}
	}
}

func TestRequestHeaderRejectionNeverReflectsHeaderValue(t *testing.T) {
	maliciousHeader := "<script>alert('request-header')</script>"
	nextCalled := false
	transaction := &recordingTransaction{
		headerDecision: func(direction Direction, _ []Header, _ bool) Decision {
			if direction == DirectionRequest {
				return Decision{Action: ActionDeny, Status: http.StatusForbidden}
			}
			return allowDecision()
		},
	}
	middleware := newTestMiddleware(t, http.HandlerFunc(func(http.ResponseWriter, *http.Request) {
		nextCalled = true
	}), transaction)
	request := httptest.NewRequest(http.MethodGet, "http://example.test/reject", nil)
	request.Header.Set("X-Attacker-Input", maliciousHeader)
	response := httptest.NewRecorder()

	middleware.ServeHTTP(response, request)

	if nextCalled {
		t.Fatal("next handler ran after request-header rejection")
	}
	if got, want := response.Code, http.StatusForbidden; got != want {
		t.Fatalf("status = %d, want %d", got, want)
	}
	if got, want := response.Body.String(), "request rejected\n"; got != want {
		t.Fatalf("rejection body = %q, want %q", got, want)
	}
	if strings.Contains(response.Body.String(), maliciousHeader) {
		t.Fatalf("rejection reflected a request header: %q", response.Body.String())
	}
}

func TestReadFromUsesUnderlyingReaderFromAndKeepsChunksBounded(t *testing.T) {
	transaction := &recordingTransaction{}
	middleware := newTestMiddleware(t, http.HandlerFunc(func(writer http.ResponseWriter, _ *http.Request) {
		readerFrom, ok := writer.(io.ReaderFrom)
		if !ok {
			t.Error("wrapped ResponseWriter does not implement io.ReaderFrom")
			return
		}
		count, err := readerFrom.ReadFrom(&plainReader{reader: strings.NewReader("read-from")})
		if err != nil {
			t.Errorf("ReadFrom() error = %v", err)
		}
		if want := int64(len("read-from")); count != want {
			t.Errorf("ReadFrom() count = %d, want %d", count, want)
		}
	}), transaction)

	response := &readerFromResponseWriter{header: make(http.Header)}
	request := httptest.NewRequest(http.MethodGet, "http://example.test/read-from", nil)
	middleware.ServeHTTP(response, request)

	if !response.readFromCalled {
		t.Fatal("underlying io.ReaderFrom fast path was not used")
	}
	if got, want := response.body.String(), "read-from"; got != want {
		t.Fatalf("response body = %q, want %q", got, want)
	}
	assertBoundedBodies(t, transaction.bodyCalls, DirectionResponse, 2, len("read-from"))
}

func TestOptionalResponseWriterInterfacesArePreserved(t *testing.T) {
	transaction := &recordingTransaction{}
	state := &streamState{
		config: mustTestConfig(t),
		engine: transaction,
	}
	underlying := newAdvancedResponseWriter(t)
	request := httptest.NewRequest(http.MethodGet, "http://example.test/interfaces", nil)
	writer := newResponseWriter(request, underlying, state)

	if _, ok := interface{}(writer).(http.Flusher); !ok {
		t.Fatal("wrapped ResponseWriter does not implement http.Flusher")
	}
	if _, ok := interface{}(writer).(http.Hijacker); !ok {
		t.Fatal("wrapped ResponseWriter does not implement http.Hijacker")
	}
	if _, ok := interface{}(writer).(http.Pusher); !ok {
		t.Fatal("wrapped ResponseWriter does not implement http.Pusher")
	}
	if _, ok := interface{}(writer).(io.ReaderFrom); !ok {
		t.Fatal("wrapped ResponseWriter does not implement io.ReaderFrom")
	}

	writer.Flush()
	if !underlying.flushed {
		t.Fatal("Flush was not forwarded")
	}
	if err := writer.Push("/asset.js", nil); err != nil {
		t.Fatalf("Push() error = %v", err)
	}
	if got, want := underlying.pushed, "/asset.js"; got != want {
		t.Fatalf("Push target = %q, want %q", got, want)
	}
	connection, _, err := writer.Hijack()
	if err != nil {
		t.Fatalf("Hijack() error = %v", err)
	}
	if connection != underlying.connection {
		t.Fatal("Hijack did not preserve the underlying connection")
	}
	_ = connection.Close()
}

func TestResponseWriteFlushesForwardedChunk(t *testing.T) {
	transaction := &recordingTransaction{}
	underlying := newAdvancedResponseWriter(t)
	defer underlying.connection.Close()
	middleware := newTestMiddleware(t, http.HandlerFunc(func(writer http.ResponseWriter, _ *http.Request) {
		if _, err := writer.Write([]byte("forwarded response")); err != nil {
			t.Errorf("Write() error = %v", err)
		}
	}), transaction)

	middleware.ServeHTTP(underlying, httptest.NewRequest(http.MethodGet, "http://example.test/flush", nil))

	if !underlying.flushed {
		t.Fatal("forwarded response bytes were not flushed to the underlying host writer")
	}
	if got, want := underlying.body.String(), "forwarded response"; got != want {
		t.Fatalf("response body = %q, want %q", got, want)
	}
}

func TestPreCommitResponseDecisionDoesNotBufferOrForwardBody(t *testing.T) {
	transaction := &recordingTransaction{
		bodyDecision: func(direction Direction, _ []byte, _ bool) Decision {
			if direction == DirectionResponse {
				return Decision{Action: ActionDeny, Status: http.StatusUnavailableForLegalReasons}
			}
			return allowDecision()
		},
	}
	middleware := newTestMiddleware(t, http.HandlerFunc(func(writer http.ResponseWriter, _ *http.Request) {
		_, _ = writer.Write([]byte("sensitive response body"))
	}), transaction)

	response := httptest.NewRecorder()
	middleware.ServeHTTP(response, httptest.NewRequest(http.MethodGet, "http://example.test/deny", nil))

	if got, want := response.Code, http.StatusUnavailableForLegalReasons; got != want {
		t.Fatalf("status = %d, want %d", got, want)
	}
	if strings.Contains(response.Body.String(), "sensitive") {
		t.Fatalf("response unexpectedly contains upstream body: %q", response.Body.String())
	}
	if len(transaction.closed) != 1 || transaction.closed[0].ResponseEOS {
		t.Fatalf("rejected response should not invent EOS evidence: %#v", transaction.closed)
	}
}

func TestLateResponseDecisionDoesNotReplaceCommittedResponse(t *testing.T) {
	transaction := &recordingTransaction{
		bodyDecision: func(direction Direction, _ []byte, _ bool) Decision {
			if direction == DirectionResponse {
				return Decision{Action: ActionDeny, Status: http.StatusForbidden}
			}
			return allowDecision()
		},
	}
	middleware := newTestMiddleware(t, http.HandlerFunc(func(writer http.ResponseWriter, _ *http.Request) {
		writer.WriteHeader(http.StatusOK)
		if _, err := writer.Write([]byte("already committed")); err != nil {
			t.Errorf("Write() error = %v", err)
		}
	}), transaction)

	response := httptest.NewRecorder()
	middleware.ServeHTTP(response, httptest.NewRequest(http.MethodGet, "http://example.test/late", nil))

	if got, want := response.Code, http.StatusOK; got != want {
		t.Fatalf("status = %d, want %d", got, want)
	}
	if got, want := response.Body.String(), "already committed"; got != want {
		t.Fatalf("response body = %q, want %q", got, want)
	}
	if len(transaction.closed) != 1 || transaction.closed[0].LateAction != "log_only" {
		t.Fatalf("late decision did not remain log-only: %#v", transaction.closed)
	}
}

func TestLateResponseDecisionDoesNotHijackTheHostConnection(t *testing.T) {
	transaction := &recordingTransaction{
		bodyDecision: func(direction Direction, _ []byte, _ bool) Decision {
			if direction == DirectionResponse {
				return Decision{Action: ActionDeny, Status: http.StatusForbidden}
			}
			return allowDecision()
		},
	}
	underlying := newAdvancedResponseWriter(t)
	middleware := newTestMiddleware(t, http.HandlerFunc(func(writer http.ResponseWriter, _ *http.Request) {
		writer.WriteHeader(http.StatusOK)
		if _, err := writer.Write([]byte("already committed")); err != nil {
			t.Errorf("Write() error = %v", err)
		}
	}), transaction)

	middleware.ServeHTTP(underlying, httptest.NewRequest(http.MethodGet, "http://example.test/late", nil))

	if got, want := underlying.body.String(), "already committed"; got != want {
		t.Fatalf("response body = %q, want %q", got, want)
	}
	if underlying.hijackCalls != 0 {
		t.Fatalf("late decision unexpectedly hijacked the host connection %d times", underlying.hijackCalls)
	}
	if len(transaction.closed) != 1 || transaction.closed[0].LateAction != "log_only" {
		t.Fatalf("late decision did not remain log-only: %#v", transaction.closed)
	}
}

func TestIncompleteHostWriteDoesNotInventResponseEOS(t *testing.T) {
	transaction := &recordingTransaction{}
	middleware := newTestMiddleware(t, http.HandlerFunc(func(writer http.ResponseWriter, _ *http.Request) {
		_, _ = writer.Write([]byte("response that the client did not receive"))
	}), transaction)
	response := &failingResponseWriter{header: make(http.Header)}

	middleware.ServeHTTP(response, httptest.NewRequest(http.MethodGet, "http://example.test/disconnect", nil))

	if len(transaction.closed) != 1 {
		t.Fatalf("Close calls = %d, want 1", len(transaction.closed))
	}
	if transaction.closed[0].ResponseEOS {
		t.Fatalf("incomplete host write fabricated response EOS: %#v", transaction.closed[0])
	}
	for _, call := range transaction.bodyCalls {
		if call.direction == DirectionResponse && call.end {
			t.Fatalf("incomplete host write invoked a response EOS callback: %#v", transaction.bodyCalls)
		}
	}
}

func assertBoundedBodies(t *testing.T, calls []bodyCall, direction Direction, maximum, wantBytes int) {
	t.Helper()
	bytesSeen := 0
	endSeen := false
	chunks := 0
	for _, call := range calls {
		if call.direction != direction {
			continue
		}
		chunks++
		if call.length > maximum {
			t.Fatalf("%s chunk length = %d, maximum = %d", direction, call.length, maximum)
		}
		bytesSeen += call.length
		endSeen = endSeen || call.end
	}
	if chunks == 0 {
		t.Fatalf("no %s body callbacks", direction)
	}
	if bytesSeen != wantBytes {
		t.Fatalf("%s body bytes = %d, want %d", direction, bytesSeen, wantBytes)
	}
	if !endSeen {
		t.Fatalf("no %s end-of-stream callback", direction)
	}
}

func mustTestConfig(t *testing.T) Config {
	t.Helper()
	config, err := normalizedConfig(CreateConfig())
	if err != nil {
		t.Fatalf("normalizedConfig() error = %v", err)
	}
	return config
}

type plainReader struct {
	reader io.Reader
}

func (reader *plainReader) Read(buffer []byte) (int, error) {
	return reader.reader.Read(buffer)
}

type readerFromResponseWriter struct {
	header         http.Header
	status         int
	body           bytes.Buffer
	readFromCalled bool
}

func (writer *readerFromResponseWriter) Header() http.Header {
	return writer.header
}

func (writer *readerFromResponseWriter) WriteHeader(status int) {
	if writer.status == 0 {
		writer.status = status
	}
}

func (writer *readerFromResponseWriter) Write(payload []byte) (int, error) {
	if writer.status == 0 {
		writer.status = http.StatusOK
	}
	return writer.body.Write(payload)
}

func (writer *readerFromResponseWriter) ReadFrom(source io.Reader) (int64, error) {
	writer.readFromCalled = true
	if writer.status == 0 {
		writer.status = http.StatusOK
	}
	return writer.body.ReadFrom(source)
}

type advancedResponseWriter struct {
	readerFromResponseWriter
	flushed     bool
	pushed      string
	connection  net.Conn
	hijackCalls int
}

func newAdvancedResponseWriter(t *testing.T) *advancedResponseWriter {
	t.Helper()
	connection, peer := net.Pipe()
	_ = peer.Close()
	return &advancedResponseWriter{
		readerFromResponseWriter: readerFromResponseWriter{header: make(http.Header)},
		connection:               connection,
	}
}

func (writer *advancedResponseWriter) Flush() {
	writer.flushed = true
}

func (writer *advancedResponseWriter) Push(target string, _ *http.PushOptions) error {
	writer.pushed = target
	return nil
}

func (writer *advancedResponseWriter) Hijack() (net.Conn, *bufio.ReadWriter, error) {
	writer.hijackCalls++
	return writer.connection, bufio.NewReadWriter(bufio.NewReader(writer.connection), bufio.NewWriter(writer.connection)), nil
}

type failingResponseWriter struct {
	header http.Header
	status int
}

func (writer *failingResponseWriter) Header() http.Header {
	return writer.header
}

func (writer *failingResponseWriter) WriteHeader(status int) {
	if writer.status == 0 {
		writer.status = status
	}
}

func (writer *failingResponseWriter) Write(_ []byte) (int, error) {
	if writer.status == 0 {
		writer.status = http.StatusOK
	}
	return 0, io.ErrClosedPipe
}
