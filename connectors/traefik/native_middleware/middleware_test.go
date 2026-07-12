package native_middleware

import (
	"bufio"
	"bytes"
	"context"
	"io"
	"net"
	"net/http"
	"net/http/httptest"
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
	headerCalls  []headerCall
	bodyCalls    []bodyCall
	closed       []Summary
	bodyDecision func(Direction, []byte, bool) Decision
}

func (transaction *recordingTransaction) ProcessHeaders(_ context.Context, direction Direction, headers []Header, end bool) (Decision, error) {
	transaction.headerCalls = append(transaction.headerCalls, headerCall{direction: direction, end: end, count: len(headers)})
	return allowDecision(), nil
}

func (transaction *recordingTransaction) ProcessBody(_ context.Context, direction Direction, body []byte, end bool) (Decision, error) {
	transaction.bodyCalls = append(transaction.bodyCalls, bodyCall{direction: direction, end: end, length: len(body)})
	if transaction.bodyDecision != nil {
		return transaction.bodyDecision(direction, body, end), nil
	}
	return allowDecision(), nil
}

func (transaction *recordingTransaction) Close(_ context.Context, summary Summary) {
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
		context: context.Background(),
		config:  mustTestConfig(t),
		engine:  transaction,
	}
	underlying := newAdvancedResponseWriter(t)
	writer := newResponseWriter(underlying, state)

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
	flushed    bool
	pushed     string
	connection net.Conn
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
	return writer.connection, bufio.NewReadWriter(bufio.NewReader(writer.connection), bufio.NewWriter(writer.connection)), nil
}
