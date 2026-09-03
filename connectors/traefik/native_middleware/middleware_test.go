package native_middleware

import (
	"bufio"
	"bytes"
	"context"
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
	opens          int
	headerCalls    []headerCall
	headerValues   [][]Header
	bodyCalls      []bodyCall
	contexts       []context.Context
	closed         []Summary
	headerDecision func(Direction, []Header, bool) Decision
	bodyDecision   func(Direction, []byte, bool) Decision
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

func serveNoContentRequest(t *testing.T, request *http.Request) (*recordingTransaction, *httptest.ResponseRecorder) {
	t.Helper()
	transaction := &recordingTransaction{}
	middleware := newTestMiddleware(t, http.HandlerFunc(func(writer http.ResponseWriter, _ *http.Request) {
		writer.WriteHeader(http.StatusNoContent)
	}), transaction)
	response := httptest.NewRecorder()
	middleware.ServeHTTP(response, request)
	return transaction, response
}

func serveRejectedRequest(t *testing.T, request *http.Request) *recordingTransaction {
	t.Helper()
	transaction := &recordingTransaction{}
	nextCalled := false
	middleware := newTestMiddleware(t, http.HandlerFunc(func(http.ResponseWriter, *http.Request) {
		nextCalled = true
	}), transaction)
	response := httptest.NewRecorder()
	middleware.ServeHTTP(response, request)
	if nextCalled {
		t.Fatal("next handler ran for rejected request")
	}
	if got, want := response.Code, http.StatusRequestHeaderFieldsTooLarge; got != want {
		t.Fatalf("status = %d, want %d", got, want)
	}
	return transaction
}

func metadataForRequest(t *testing.T, request *http.Request) []Metadata {
	t.Helper()
	transaction := &recordingTransaction{}
	engine := &recordingEngine{transaction: transaction}
	config := CreateConfig()
	config.EngineSocketPath = "/run/msconnector-test.sock"
	middleware, err := newWithEngine(http.HandlerFunc(func(writer http.ResponseWriter, _ *http.Request) {
		writer.WriteHeader(http.StatusNoContent)
	}), config, "test", engine)
	if err != nil {
		t.Fatalf("newWithEngine() error = %v", err)
	}
	middleware.ServeHTTP(httptest.NewRecorder(), request)
	return engine.metadata
}

func TestMiddlewareForwardsRequestAuthorityAsHostHeader(t *testing.T) {
	request := httptest.NewRequest(http.MethodGet, "http://authority.example:8443/resource", nil)
	if request.Header.Get("Host") != "" {
		t.Fatal("httptest request unexpectedly stored authority in Header")
	}

	transaction, response := serveNoContentRequest(t, request)

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

func TestMiddlewareRejectsConflictingHostHeaderBeforeEngine(t *testing.T) {
	request := httptest.NewRequest(http.MethodGet, "http://authority.example/resource", nil)
	request.Host = "authority.example"
	request.Header.Set("Host", "header.example")
	transaction := serveRejectedRequest(t, request)
	if got := transaction.opens; got != 0 {
		t.Fatalf("engine opens = %d, want 0", got)
	}
}

func TestMiddlewareRejectsInvalidHostHeaderBeforeEngine(t *testing.T) {
	request := httptest.NewRequest(http.MethodGet, "http://authority.example/resource", nil)
	request.Host = "authority.example"
	request.Header.Set("Host", "authority.example\r\nInjected: yes")
	transaction := serveRejectedRequest(t, request)
	if got := transaction.opens; got != 0 {
		t.Fatalf("engine opens = %d, want 0", got)
	}
}

func TestMiddlewareAcceptsMatchingHostHeaderWithoutAuthorityDuplicate(t *testing.T) {
	request := httptest.NewRequest(http.MethodGet, "http://authority.example/resource", nil)
	request.Host = "authority.example"
	request.Header.Set("Host", "authority.example")
	transaction, response := serveNoContentRequest(t, request)

	if got, want := response.Code, http.StatusNoContent; got != want {
		t.Fatalf("status = %d, want %d", got, want)
	}
	var hosts []string
	for _, header := range requestHeaderValues(transaction) {
		if strings.EqualFold(header.Name, "Host") {
			hosts = append(hosts, header.Value)
		}
	}
	if got, want := hosts, []string{"authority.example"}; !reflect.DeepEqual(got, want) {
		t.Fatalf("forwarded Host values = %#v, want %#v", got, want)
	}
}

func TestMiddlewareRejectsInvalidAuthorityBeforeEngineHeaders(t *testing.T) {
	request := httptest.NewRequest(http.MethodGet, "http://authority.example/resource", nil)
	request.Host = "authority.example\r\nInjected: yes"
	transaction := serveRejectedRequest(t, request)
	if got := transaction.opens; got != 0 {
		t.Fatalf("engine opens = %d, want 0", got)
	}
}

func TestMiddlewareRejectsMissingAuthorityBeforeEngineOpen(t *testing.T) {
	request := httptest.NewRequest(http.MethodGet, "http://authority.example/resource", nil)
	request.Host = ""
	transaction := serveRejectedRequest(t, request)
	if got := transaction.opens; got != 0 {
		t.Fatalf("engine opens = %d, want 0", got)
	}
}

func (transaction *recordingTransaction) ProcessBody(value context.Context, direction Direction, body []byte, end bool) (Decision, error) {
	transaction.contexts = append(transaction.contexts, value)
	transaction.bodyCalls = append(transaction.bodyCalls, bodyCall{direction: direction, end: end, length: len(body)})
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
	metadata    []Metadata
}

func (engine *recordingEngine) Open(_ context.Context, metadata Metadata) (Transaction, error) {
	engine.transaction.opens++
	engine.metadata = append(engine.metadata, metadata)
	return engine.transaction, nil
}

func TestMiddlewarePreservesRawAuthorityInMetadata(t *testing.T) {
	request := httptest.NewRequest(http.MethodGet, "http://authority.example:8443/resource", nil)
	metadata := metadataForRequest(t, request)
	if got, want := len(metadata), 1; got != want {
		t.Fatalf("metadata records = %d, want %d", got, want)
	}
	value := metadata[0]
	if got, want := value.Hostname, "authority.example:8443"; got != want {
		t.Fatalf("metadata Hostname = %q, want raw authority %q", got, want)
	}
	if got, want := value.ServerAddress, "authority.example"; got != want {
		t.Fatalf("metadata ServerAddress = %q, want parsed host %q", got, want)
	}
	if got, want := value.ServerPort, 8443; got != want {
		t.Fatalf("metadata ServerPort = %d, want %d", got, want)
	}
}

func TestMiddlewarePreservesBracketedIPv6AuthorityInMetadata(t *testing.T) {
	request := httptest.NewRequest(http.MethodGet, "http://[2001:db8::1]:8443/resource", nil)
	metadata := metadataForRequest(t, request)
	if got, want := len(metadata), 1; got != want {
		t.Fatalf("metadata records = %d, want %d", got, want)
	}
	value := metadata[0]
	if got, want := value.ServerAddress, "2001:db8::1"; got != want {
		t.Fatalf("metadata ServerAddress = %q, want parsed IPv6 address %q", got, want)
	}
	if got, want := value.ServerPort, 8443; got != want {
		t.Fatalf("metadata ServerPort = %d, want %d", got, want)
	}
}

func TestMiddlewareRejectsInvalidAuthorityPortBeforeEngineOpen(t *testing.T) {
	tests := []struct {
		name      string
		authority string
	}{
		{name: "non-numeric port", authority: "authority.example:not-a-port"},
		{name: "out-of-range port", authority: "authority.example:65536"},
		{name: "invalid IPv6 port", authority: "[2001:db8::1]:not-a-port"},
	}
	for _, test := range tests {
		t.Run(test.name, func(t *testing.T) {
			request := httptest.NewRequest(http.MethodGet, "http://authority.example/resource", nil)
			request.Host = test.authority
			transaction := serveRejectedRequest(t, request)
			if got := transaction.opens; got != 0 {
				t.Fatalf("engine opens = %d, want 0", got)
			}
		})
	}
}

func TestMiddlewareForwardsMixedCaseHostMapKeyExactlyOnce(t *testing.T) {
	transaction := &recordingTransaction{}
	middleware := newTestMiddleware(t, http.HandlerFunc(func(writer http.ResponseWriter, _ *http.Request) {
		writer.WriteHeader(http.StatusNoContent)
	}), transaction)
	request := httptest.NewRequest(http.MethodGet, "http://authority.example/resource", nil)
	request.Host = "authority.example"
	request.Header["hOsT"] = []string{"authority.example"}

	middleware.ServeHTTP(httptest.NewRecorder(), request)

	var hosts []Header
	for _, header := range requestHeaderValues(transaction) {
		if strings.EqualFold(header.Name, "Host") {
			hosts = append(hosts, header)
		}
	}
	if got, want := len(hosts), 1; got != want {
		t.Fatalf("forwarded Host headers = %d, want %d", got, want)
	}
	if got, want := hosts[0], (Header{Name: "hOsT", Value: "authority.example"}); got != want {
		t.Fatalf("forwarded mixed-case Host header = %#v, want %#v", got, want)
	}
}

func TestMiddlewareRejectsMalformedHeaderBeforeEngineOpen(t *testing.T) {
	tests := []struct {
		name   string
		header string
		value  string
	}{
		{name: "invalid name", header: "Bad Name", value: "value"},
		{name: "nul value", header: "X-Test", value: "bad\x00value"},
		{name: "invalid utf8 value", header: "X-Test", value: string([]byte{'b', 0xff})},
	}
	for _, test := range tests {
		t.Run(test.name, func(t *testing.T) {
			request := httptest.NewRequest(http.MethodGet, "http://authority.example/resource", nil)
			request.Header[test.header] = []string{test.value}
			transaction := serveRejectedRequest(t, request)
			if got := transaction.opens; got != 0 {
				t.Fatalf("engine opens = %d, want 0", got)
			}
		})
	}
}

func TestTraefikMiddlewareEntryPointSignature(t *testing.T) {
	var entryPoint func(context.Context, http.Handler, *Config, string) (http.Handler, error) = New
	if entryPoint == nil {
		t.Fatal("Traefik middleware New entry point is nil")
	}
}

func newTestMiddleware(t *testing.T, next http.Handler, transaction *recordingTransaction) *Middleware {
	t.Helper()
	config := CreateConfig()
	config.EngineSocketPath = "/run/msconnector-test.sock"
	config.MaxRequestChunkBytes = 3
	config.MaxResponseChunkBytes = 2
	middleware, err := newWithEngine(next, config, "test", &recordingEngine{transaction: transaction})
	if err != nil {
		t.Fatalf("newWithEngine() error = %v", err)
	}
	return middleware
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
	config := CreateConfig()
	config.EngineSocketPath = "/run/msconnector-test.sock"
	normalized, err := normalizedConfig(config)
	if err != nil {
		t.Fatalf("normalizedConfig() error = %v", err)
	}
	return normalized
}

func TestCreateConfigFailsClosedUntilUDSEngineIsConfigured(t *testing.T) {
	config := CreateConfig()
	if config.EngineMode != "uds" {
		t.Fatalf("CreateConfig() EngineMode = %q, want secure uds default", config.EngineMode)
	}
	if _, err := New(context.Background(), http.NotFoundHandler(), config, "missing-uds"); err == nil {
		t.Fatal("New() accepted the secure default without an engineSocketPath")
	}

	config.EngineMode = "passthrough"
	if _, err := New(context.Background(), http.NotFoundHandler(), config, "explicit-passthrough"); err == nil {
		t.Fatal("New() accepted an always-allow passthrough mode")
	}

	config.EngineMode = "uds"
	config.EngineSocketPath = "/run/msconnector-test.sock"
	handler, err := New(context.Background(), http.NotFoundHandler(), config, "configured-uds")
	if handler == nil {
		t.Fatal("New() returned a nil handler for configured UDS mode")
	}
	if err != nil {
		t.Fatalf("New() rejected configured UDS mode: %v", err)
	}
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
