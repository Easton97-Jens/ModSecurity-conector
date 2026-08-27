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
	contexts       []context.Context
	closed         []Summary
	headerDecision func(Direction, []Header, bool) Decision
	bodyDecision   func(Direction, []byte, bool) Decision
	bodyError      func(Direction, []byte, bool) error
}

func (transaction *recordingTransaction) ProcessHeaders(value context.Context, direction Direction, headers []Header, end bool) (Decision, error) {
	transaction.contexts = append(transaction.contexts, value)
	transaction.headerCalls = append(transaction.headerCalls, headerCall{direction: direction, end: end, count: len(headers)})
	transaction.headerValues = append(transaction.headerValues, append([]Header(nil), headers...))
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
	if transaction.bodyDecision != nil {
		return transaction.bodyDecision(direction, body, end), nil
	}
	if transaction.bodyError != nil {
		return allowDecision(), transaction.bodyError(direction, body, end)
	}
	return allowDecision(), nil
}

func (transaction *recordingTransaction) Close(value context.Context, summary Summary) {
	transaction.contexts = append(transaction.contexts, value)
	transaction.closed = append(transaction.closed, summary)
}

type recordingEngine struct {
	transaction Transaction
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
	return newTestMiddlewareWithTransaction(t, next, transaction)
}

func newTestMiddlewareWithTransaction(t *testing.T, next http.Handler, transaction Transaction) *Middleware {
	t.Helper()
	config := CreateConfig()
	config.MaxRequestChunkBytes = 3
	config.MaxResponseChunkBytes = 2
	middleware, err := NewWithEngine(next, config, "test", recordingEngine{transaction: transaction})
	if err != nil {
		t.Fatalf("NewWithEngine() error = %v", err)
	}
	return middleware
}

type commitErrorTransaction struct {
	*recordingTransaction
	err error
}

func (transaction *commitErrorTransaction) SetResponseCommit(context.Context, bool, bool) error {
	return transaction.err
}

type acknowledgementErrorTransaction struct {
	*recordingTransaction
	appliedErr error
	lateErr    error
}

func (transaction *acknowledgementErrorTransaction) AcknowledgeApplied(context.Context, Decision) error {
	return transaction.appliedErr
}

func (transaction *acknowledgementErrorTransaction) AcknowledgeLateLogOnly(context.Context, int) error {
	return transaction.lateErr
}

func TestMiddlewareStreamsRequestAndResponseInBoundedChunks(t *testing.T) {
	transaction := &recordingTransaction{}
	middleware := newTestMiddleware(t, http.HandlerFunc(func(writer http.ResponseWriter, request *http.Request) {
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
	}), transaction)

	request := httptest.NewRequest(http.MethodPost, "http://example.test/stream", strings.NewReader("request"))
	request.Header.Set("X-Request-Id", "transaction-1")
	response := httptest.NewRecorder()
	middleware.ServeHTTP(response, request)

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

func TestReadFromEngineEOSErrorAfterHostCommitDoesNotWriteFailure(t *testing.T) {
	engineErr := errors.New("response eos engine unavailable")
	transaction := &recordingTransaction{
		bodyError: func(direction Direction, _ []byte, end bool) error {
			if direction == DirectionResponse && end {
				return engineErr
			}
			return nil
		},
	}
	var readFromErr error
	middleware := newTestMiddleware(t, http.HandlerFunc(func(writer http.ResponseWriter, _ *http.Request) {
		readerFrom, ok := writer.(io.ReaderFrom)
		if !ok {
			t.Fatal("wrapped ResponseWriter does not implement io.ReaderFrom")
		}
		_, readFromErr = readerFrom.ReadFrom(&plainReader{reader: strings.NewReader("body")})
	}), transaction)
	response := &readerFromResponseWriter{header: make(http.Header)}

	middleware.ServeHTTP(response, httptest.NewRequest(http.MethodGet, "http://example.test/read-from-eos-error", nil))

	if !errors.Is(readFromErr, engineErr) {
		t.Fatalf("ReadFrom() error = %v, want %v", readFromErr, engineErr)
	}
	if got, want := response.body.String(), "body"; got != want {
		t.Fatalf("response body = %q, want %q", got, want)
	}
	if strings.Contains(response.body.String(), "response rejected") {
		t.Fatalf("post-commit EOS error appended a synthetic failure body: %q", response.body.String())
	}
	if len(transaction.closed) != 1 || transaction.closed[0].ResponseEOS {
		t.Fatalf("post-commit EOS error fabricated response EOS: %#v", transaction.closed)
	}
	responseEOSCalls := 0
	for _, call := range transaction.bodyCalls {
		if call.direction == DirectionResponse && call.end {
			responseEOSCalls++
		}
	}
	if responseEOSCalls != 1 {
		t.Fatalf("response EOS callbacks = %d, want 1 attempted callback", responseEOSCalls)
	}
}

func TestReadFromInitialZeroProgressPreservesPreCommitResponseDeny(t *testing.T) {
	const upstreamBody = "sensitive upstream body"
	transaction := &recordingTransaction{
		bodyDecision: func(direction Direction, _ []byte, end bool) Decision {
			if direction == DirectionResponse && !end {
				return Decision{Action: ActionDeny, Status: http.StatusForbidden}
			}
			return allowDecision()
		},
	}
	var readFromCount int64
	var readFromErr error
	middleware := newTestMiddleware(t, http.HandlerFunc(func(writer http.ResponseWriter, _ *http.Request) {
		readerFrom, ok := writer.(io.ReaderFrom)
		if !ok {
			t.Fatal("wrapped ResponseWriter does not implement io.ReaderFrom")
		}
		readFromCount, readFromErr = readerFrom.ReadFrom(&zeroThenReader{reader: strings.NewReader(upstreamBody)})
	}), transaction)
	response := &readerFromResponseWriter{header: make(http.Header)}

	middleware.ServeHTTP(response, httptest.NewRequest(http.MethodGet, "http://example.test/read-from-zero-deny", nil))

	if readFromErr != nil {
		t.Fatalf("ReadFrom() error = %v", readFromErr)
	}
	if got, want := readFromCount, int64(len(upstreamBody)); got != want {
		t.Fatalf("ReadFrom() count = %d, want %d", got, want)
	}
	if response.readFromCalled {
		t.Fatal("zero-progress pre-commit ReadFrom delegated around response controls")
	}
	if got, want := response.status, http.StatusForbidden; got != want {
		t.Fatalf("response status = %d, want %d", got, want)
	}
	if got, want := response.body.String(), "request rejected\n"; got != want {
		t.Fatalf("response body = %q, want %q", got, want)
	}
	if len(transaction.closed) != 1 || transaction.closed[0].ResponseEOS {
		t.Fatalf("rejected zero-progress ReadFrom fabricated response EOS: %#v", transaction.closed)
	}
}

func TestReadFromInitialSourceErrorDoesNotInventResponseEOS(t *testing.T) {
	sourceErr := errors.New("upstream response source failed")
	for _, test := range []struct {
		name string
		data string
	}{
		{name: "before_body", data: ""},
		{name: "after_body", data: "ok"},
	} {
		t.Run(test.name, func(t *testing.T) {
			assertInitialSourceErrorDoesNotInventResponseEOS(t, test.data, sourceErr)
		})
	}
}

func assertInitialSourceErrorDoesNotInventResponseEOS(t *testing.T, data string, sourceErr error) {
	t.Helper()

	transaction := &recordingTransaction{}
	var readFromErr error
	middleware := newTestMiddleware(t, http.HandlerFunc(func(writer http.ResponseWriter, _ *http.Request) {
		readerFrom, ok := writer.(io.ReaderFrom)
		if !ok {
			t.Fatal("wrapped ResponseWriter does not implement io.ReaderFrom")
		}
		_, readFromErr = readerFrom.ReadFrom(&errorReader{data: []byte(data), err: sourceErr})
	}), transaction)
	response := &readerFromResponseWriter{header: make(http.Header)}

	middleware.ServeHTTP(response, httptest.NewRequest(http.MethodGet, "http://example.test/read-from-source-error", nil))

	if !errors.Is(readFromErr, sourceErr) {
		t.Fatalf("ReadFrom() error = %v, want %v", readFromErr, sourceErr)
	}
	if got, want := response.body.String(), data; got != want {
		t.Fatalf("response body = %q, want %q", got, want)
	}
	if len(transaction.closed) != 1 || transaction.closed[0].ResponseEOS {
		t.Fatalf("initial source error fabricated response EOS: %#v", transaction.closed)
	}
	for _, call := range transaction.bodyCalls {
		if call.direction == DirectionResponse && call.end {
			t.Fatalf("initial source error invoked a response EOS callback: %#v", transaction.bodyCalls)
		}
	}
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

func TestEmptyHostWriteDoesNotInventResponseEOS(t *testing.T) {
	transaction := &recordingTransaction{}
	var writeErr error
	middleware := newTestMiddleware(t, http.HandlerFunc(func(writer http.ResponseWriter, _ *http.Request) {
		_, writeErr = writer.Write(nil)
	}), transaction)
	response := &failingResponseWriter{header: make(http.Header)}

	middleware.ServeHTTP(response, httptest.NewRequest(http.MethodGet, "http://example.test/empty-disconnect", nil))

	if !errors.Is(writeErr, io.ErrClosedPipe) {
		t.Fatalf("Write() error = %v, want %v", writeErr, io.ErrClosedPipe)
	}
	if len(transaction.closed) != 1 || transaction.closed[0].ResponseEOS {
		t.Fatalf("empty host write fabricated response EOS: %#v", transaction.closed)
	}
	for _, call := range transaction.bodyCalls {
		if call.direction == DirectionResponse && call.end {
			t.Fatalf("empty host write invoked a response EOS callback: %#v", transaction.bodyCalls)
		}
	}
}

func TestResponseCommitErrorDoesNotInventResponseEOS(t *testing.T) {
	commitErr := errors.New("response commit acknowledgement failed")
	recording := &recordingTransaction{}
	transaction := &commitErrorTransaction{recordingTransaction: recording, err: commitErr}
	var writeErr error
	middleware := newTestMiddlewareWithTransaction(t, http.HandlerFunc(func(writer http.ResponseWriter, _ *http.Request) {
		_, writeErr = writer.Write([]byte("body that cannot be committed to the engine"))
	}), transaction)
	response := httptest.NewRecorder()

	middleware.ServeHTTP(response, httptest.NewRequest(http.MethodGet, "http://example.test/commit-error", nil))

	if !errors.Is(writeErr, commitErr) {
		t.Fatalf("Write() error = %v, want %v", writeErr, commitErr)
	}
	if got := response.Body.String(); got != "" {
		t.Fatalf("response body after commit acknowledgement failure = %q, want empty", got)
	}
	if len(recording.closed) != 1 || recording.closed[0].ResponseEOS {
		t.Fatalf("commit acknowledgement failure fabricated response EOS: %#v", recording.closed)
	}
	for _, call := range recording.bodyCalls {
		if call.direction == DirectionResponse && call.end {
			t.Fatalf("commit acknowledgement failure invoked a response EOS callback: %#v", recording.bodyCalls)
		}
	}
}

func TestNoBodyResponseCommitErrorDoesNotInventResponseEOS(t *testing.T) {
	commitErr := errors.New("empty response commit acknowledgement failed")
	recording := &recordingTransaction{}
	transaction := &commitErrorTransaction{recordingTransaction: recording, err: commitErr}
	middleware := newTestMiddlewareWithTransaction(t, http.HandlerFunc(func(http.ResponseWriter, *http.Request) {}), transaction)
	response := httptest.NewRecorder()

	middleware.ServeHTTP(response, httptest.NewRequest(http.MethodGet, "http://example.test/empty-commit-error", nil))

	if got, want := response.Code, http.StatusOK; got != want {
		t.Fatalf("response status = %d, want %d", got, want)
	}
	if len(recording.closed) != 1 || recording.closed[0].ResponseEOS {
		t.Fatalf("empty response commit acknowledgement fabricated response EOS: %#v", recording.closed)
	}
}

func TestDirectResponseEOSErrorAtFinishMarksResponseIncomplete(t *testing.T) {
	engineErr := errors.New("response EOS engine unavailable")
	transaction := &recordingTransaction{
		bodyError: func(direction Direction, _ []byte, end bool) error {
			if direction == DirectionResponse && end {
				return engineErr
			}
			return nil
		},
	}
	middleware := newTestMiddleware(t, http.HandlerFunc(func(writer http.ResponseWriter, _ *http.Request) {
		_, _ = writer.Write([]byte("body"))
	}), transaction)
	response := httptest.NewRecorder()

	middleware.ServeHTTP(response, httptest.NewRequest(http.MethodGet, "http://example.test/direct-eos-error", nil))

	if len(transaction.closed) != 1 || !transaction.closed[0].ResponseIncomplete || transaction.closed[0].ResponseEOS {
		t.Fatalf("direct response EOS error did not close incomplete: %#v", transaction.closed)
	}
}

func TestPreCommitDenialWriteFailureMarksResponseIncomplete(t *testing.T) {
	transaction := &recordingTransaction{
		bodyDecision: func(direction Direction, _ []byte, _ bool) Decision {
			if direction == DirectionResponse {
				return Decision{Action: ActionDeny, Status: http.StatusForbidden}
			}
			return allowDecision()
		},
	}
	middleware := newTestMiddleware(t, http.HandlerFunc(func(writer http.ResponseWriter, _ *http.Request) {
		_, _ = writer.Write([]byte("blocked response"))
	}), transaction)
	response := &failingResponseWriter{header: make(http.Header)}

	middleware.ServeHTTP(response, httptest.NewRequest(http.MethodGet, "http://example.test/denial-write-error", nil))

	if len(transaction.closed) != 1 || !transaction.closed[0].ResponseIncomplete || transaction.closed[0].ResponseEOS {
		t.Fatalf("denial write failure did not close incomplete: %#v", transaction.closed)
	}
}

func TestPreCommitDenialCommitErrorMarksResponseIncomplete(t *testing.T) {
	recording := &recordingTransaction{
		bodyDecision: func(direction Direction, _ []byte, _ bool) Decision {
			if direction == DirectionResponse {
				return Decision{Action: ActionDeny, Status: http.StatusForbidden}
			}
			return allowDecision()
		},
	}
	transaction := &commitErrorTransaction{
		recordingTransaction: recording,
		err:                  errors.New("denial response commit failed"),
	}
	middleware := newTestMiddlewareWithTransaction(t, http.HandlerFunc(func(writer http.ResponseWriter, _ *http.Request) {
		_, _ = writer.Write([]byte("blocked response"))
	}), transaction)
	response := httptest.NewRecorder()

	middleware.ServeHTTP(response, httptest.NewRequest(http.MethodGet, "http://example.test/denial-commit-error", nil))

	if len(recording.closed) != 1 || !recording.closed[0].ResponseIncomplete || recording.closed[0].ResponseEOS {
		t.Fatalf("denial commit error did not close incomplete: %#v", recording.closed)
	}
}

func TestEvaluationFailureCommitErrorMarksResponseIncomplete(t *testing.T) {
	recording := &recordingTransaction{
		bodyError: func(direction Direction, _ []byte, end bool) error {
			if direction == DirectionResponse && !end {
				return errors.New("response evaluation failed")
			}
			return nil
		},
	}
	transaction := &commitErrorTransaction{
		recordingTransaction: recording,
		err:                  errors.New("failure response commit failed"),
	}
	middleware := newTestMiddlewareWithTransaction(t, http.HandlerFunc(func(writer http.ResponseWriter, _ *http.Request) {
		_, _ = writer.Write([]byte("body"))
	}), transaction)
	response := httptest.NewRecorder()

	middleware.ServeHTTP(response, httptest.NewRequest(http.MethodGet, "http://example.test/failure-commit-error", nil))

	if len(recording.closed) != 1 || !recording.closed[0].ResponseIncomplete || recording.closed[0].ResponseEOS {
		t.Fatalf("failure commit error did not close incomplete: %#v", recording.closed)
	}
}

func TestPreCommitResponseEOSErrorFallbackMarksResponseIncomplete(t *testing.T) {
	transaction := &recordingTransaction{
		bodyError: func(direction Direction, _ []byte, end bool) error {
			if direction == DirectionResponse && end {
				return errors.New("pre-commit response EOS failed")
			}
			return nil
		},
	}
	middleware := newTestMiddleware(t, http.HandlerFunc(func(http.ResponseWriter, *http.Request) {}), transaction)
	response := httptest.NewRecorder()

	middleware.ServeHTTP(response, httptest.NewRequest(http.MethodGet, "http://example.test/precommit-eos-error", nil))

	if got, want := response.Code, http.StatusInternalServerError; got != want {
		t.Fatalf("fallback status = %d, want %d", got, want)
	}
	if len(transaction.closed) != 1 || !transaction.closed[0].ResponseIncomplete || transaction.closed[0].ResponseEOS {
		t.Fatalf("pre-commit response EOS fallback did not close incomplete: %#v", transaction.closed)
	}
}

func TestPreCommitDenialAcknowledgementErrorMarksResponseIncomplete(t *testing.T) {
	recording := &recordingTransaction{
		bodyDecision: func(direction Direction, _ []byte, _ bool) Decision {
			if direction == DirectionResponse {
				return Decision{Action: ActionDeny, Status: http.StatusForbidden}
			}
			return allowDecision()
		},
	}
	transaction := &acknowledgementErrorTransaction{
		recordingTransaction: recording,
		appliedErr:           errors.New("outcome acknowledgement failed"),
	}
	middleware := newTestMiddlewareWithTransaction(t, http.HandlerFunc(func(writer http.ResponseWriter, _ *http.Request) {
		_, _ = writer.Write([]byte("blocked response"))
	}), transaction)
	response := httptest.NewRecorder()

	middleware.ServeHTTP(response, httptest.NewRequest(http.MethodGet, "http://example.test/denial-ack-error", nil))

	if len(recording.closed) != 1 || !recording.closed[0].ResponseIncomplete || recording.closed[0].ResponseEOS {
		t.Fatalf("denial acknowledgement error did not close incomplete: %#v", recording.closed)
	}
}

func TestLateDecisionAcknowledgementErrorMarksResponseIncomplete(t *testing.T) {
	responseCalls := 0
	recording := &recordingTransaction{
		bodyDecision: func(direction Direction, _ []byte, end bool) Decision {
			if direction == DirectionResponse && !end {
				responseCalls++
				if responseCalls == 2 {
					return Decision{Action: ActionDeny, Status: http.StatusForbidden}
				}
			}
			return allowDecision()
		},
	}
	transaction := &acknowledgementErrorTransaction{
		recordingTransaction: recording,
		lateErr:              errors.New("late outcome acknowledgement failed"),
	}
	middleware := newTestMiddlewareWithTransaction(t, http.HandlerFunc(func(writer http.ResponseWriter, _ *http.Request) {
		_, _ = writer.Write([]byte("one"))
		_, _ = writer.Write([]byte("two"))
	}), transaction)
	response := httptest.NewRecorder()

	middleware.ServeHTTP(response, httptest.NewRequest(http.MethodGet, "http://example.test/late-ack-error", nil))

	if len(recording.closed) != 1 || !recording.closed[0].ResponseIncomplete || recording.closed[0].ResponseEOS {
		t.Fatalf("late acknowledgement error did not close incomplete: %#v", recording.closed)
	}
	if got, want := recording.closed[0].LateAction, "log_only"; got != want {
		t.Fatalf("late action = %q, want %q", got, want)
	}
	for _, call := range recording.bodyCalls {
		if call.direction == DirectionResponse && call.end {
			t.Fatalf("late acknowledgement error invoked a response EOS callback: %#v", recording.bodyCalls)
		}
	}
}

func TestReadFromLateDecisionAcknowledgementErrorDoesNotInventResponseEOS(t *testing.T) {
	responseCalls := 0
	recording := &recordingTransaction{
		bodyDecision: func(direction Direction, _ []byte, end bool) Decision {
			if direction == DirectionResponse && !end {
				responseCalls++
				if responseCalls == 2 {
					return Decision{Action: ActionDeny, Status: http.StatusForbidden}
				}
			}
			return allowDecision()
		},
	}
	transaction := &acknowledgementErrorTransaction{
		recordingTransaction: recording,
		lateErr:              errors.New("late ReadFrom acknowledgement failed"),
	}
	middleware := newTestMiddlewareWithTransaction(t, http.HandlerFunc(func(writer http.ResponseWriter, _ *http.Request) {
		readerFrom, ok := writer.(io.ReaderFrom)
		if !ok {
			t.Fatal("wrapped ResponseWriter does not implement io.ReaderFrom")
		}
		_, _ = readerFrom.ReadFrom(&plainReader{reader: strings.NewReader("one-two")})
	}), transaction)
	response := &readerFromResponseWriter{header: make(http.Header)}

	middleware.ServeHTTP(response, httptest.NewRequest(http.MethodGet, "http://example.test/read-from-late-ack-error", nil))

	if !response.readFromCalled {
		t.Fatal("ReaderFrom late-ack path did not delegate after the pre-commit chunk")
	}
	if len(recording.closed) != 1 || !recording.closed[0].ResponseIncomplete || recording.closed[0].ResponseEOS {
		t.Fatalf("ReaderFrom late acknowledgement error did not close incomplete: %#v", recording.closed)
	}
	for _, call := range recording.bodyCalls {
		if call.direction == DirectionResponse && call.end {
			t.Fatalf("ReaderFrom late acknowledgement error invoked a response EOS callback: %#v", recording.bodyCalls)
		}
	}
}

func TestEngineErrorAfterCommittedResponseDoesNotInventResponseEOS(t *testing.T) {
	engineErr := errors.New("response engine unavailable")
	responseChunks := 0
	transaction := &recordingTransaction{
		bodyError: func(direction Direction, _ []byte, end bool) error {
			if direction != DirectionResponse || end {
				return nil
			}
			responseChunks++
			if responseChunks == 2 {
				return engineErr
			}
			return nil
		},
	}
	var writeErr error
	middleware := newTestMiddleware(t, http.HandlerFunc(func(writer http.ResponseWriter, _ *http.Request) {
		if _, err := writer.Write([]byte("ok")); err != nil {
			t.Fatalf("first Write() error = %v", err)
		}
		_, writeErr = writer.Write([]byte("later"))
	}), transaction)
	response := httptest.NewRecorder()

	middleware.ServeHTTP(response, httptest.NewRequest(http.MethodGet, "http://example.test/engine-error", nil))

	if !errors.Is(writeErr, engineErr) {
		t.Fatalf("second Write() error = %v, want %v", writeErr, engineErr)
	}
	if got, want := response.Body.String(), "ok"; got != want {
		t.Fatalf("response body = %q, want %q", got, want)
	}
	if len(transaction.closed) != 1 {
		t.Fatalf("Close calls = %d, want 1", len(transaction.closed))
	}
	if transaction.closed[0].ResponseEOS {
		t.Fatalf("post-commit engine error fabricated response EOS: %#v", transaction.closed[0])
	}
	for _, call := range transaction.bodyCalls {
		if call.direction == DirectionResponse && call.end {
			t.Fatalf("post-commit engine error invoked a response EOS callback: %#v", transaction.bodyCalls)
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

type zeroThenReader struct {
	reader io.Reader
	zero   bool
}

func (reader *zeroThenReader) Read(buffer []byte) (int, error) {
	if !reader.zero {
		reader.zero = true
		return 0, nil
	}
	return reader.reader.Read(buffer)
}

type errorReader struct {
	data []byte
	err  error
	read bool
}

func (reader *errorReader) Read(buffer []byte) (int, error) {
	if reader.read {
		return 0, reader.err
	}
	reader.read = true
	count := copy(buffer, reader.data)
	return count, reader.err
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
