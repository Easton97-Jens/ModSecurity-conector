package native_middleware

import (
	"context"
	"encoding/binary"
	"errors"
	"io"
	"net"
	"net/http"
	"net/http/httptest"
	"os"
	"path/filepath"
	"strings"
	"testing"
	"time"
)

type udsTestResult struct {
	action byte
	status int
}

type udsTestCall struct {
	opcode  byte
	payload []byte
}

type udsTestServer struct {
	listener net.Listener
	results  map[byte]udsTestResult
	done     chan struct{}
	calls    []udsTestCall
	err      error
}

func newUDSTestSocketPath(t *testing.T) string {
	t.Helper()
	directory, err := os.MkdirTemp("", "uds-")
	if err != nil {
		t.Fatalf("create short UDS test directory: %v", err)
	}
	t.Cleanup(func() {
		if err := os.RemoveAll(directory); err != nil {
			t.Errorf("remove UDS test directory: %v", err)
		}
	})
	return filepath.Join(directory, "engine.sock")
}

func startUDSTestServer(t *testing.T, results map[byte]udsTestResult) (string, *udsTestServer) {
	t.Helper()
	socketPath := newUDSTestSocketPath(t)
	listener, err := net.Listen("unix", socketPath)
	if err != nil {
		t.Fatalf("listen Unix socket: %v", err)
	}
	server := &udsTestServer{listener: listener, results: results, done: make(chan struct{})}
	go func() {
		defer close(server.done)
		defer server.listener.Close()
		connection, err := server.listener.Accept()
		if err != nil {
			server.err = err
			return
		}
		defer connection.Close()
		for {
			opcode, payload, err := readUDSFrame(connection)
			if err != nil {
				if !errors.Is(err, io.EOF) {
					server.err = err
				}
				return
			}
			copyPayload := append([]byte(nil), payload...)
			server.calls = append(server.calls, udsTestCall{opcode: opcode, payload: copyPayload})
			result := udsTestResult{action: udsActionAllow}
			if configured, ok := server.results[opcode]; ok {
				result = configured
			}
			if err := writeUDSTestResult(connection, opcode, result); err != nil {
				server.err = err
				return
			}
			if opcode == udsOpcodeDestroy {
				return
			}
		}
	}()
	return socketPath, server
}

func writeUDSTestResult(writer io.Writer, command byte, result udsTestResult) error {
	payload := make([]byte, 14)
	payload[0] = command
	payload[1] = udsResultOK
	payload[2] = result.action
	binary.BigEndian.PutUint16(payload[4:6], uint16(result.status))
	return writeUDSFrame(writer, udsOpcodeResult, payload)
}

func (server *udsTestServer) wait(t *testing.T) []udsTestCall {
	t.Helper()
	select {
	case <-server.done:
	case <-time.After(3 * time.Second):
		_ = server.listener.Close()
		t.Fatal("Unix engine test server did not finish")
	}
	if server.err != nil {
		t.Fatalf("Unix engine test server: %v", server.err)
	}
	return server.calls
}

func newUDSTestMiddleware(t *testing.T, socketPath string, next http.Handler) *Middleware {
	t.Helper()
	config := CreateConfig()
	config.EngineMode = "uds"
	config.EngineSocketPath = socketPath
	config.MaxRequestChunkBytes = 3
	config.MaxResponseChunkBytes = 2
	handler, err := New(context.Background(), next, config, "uds-test")
	if err != nil {
		t.Fatalf("New() error = %v", err)
	}
	middleware, ok := handler.(*Middleware)
	if !ok {
		t.Fatalf("New() handler type = %T, want *Middleware", handler)
	}
	return middleware
}

func TestUDSConfigRejectsValuesOutsideTheWireContract(t *testing.T) {
	tests := []struct {
		name   string
		mutate func(*Config)
	}{
		{
			name: "header-count",
			mutate: func(config *Config) {
				config.MaxHeaderCount = udsMaxHeaders + 1
			},
		},
		{
			name: "header-bytes",
			mutate: func(config *Config) {
				config.MaxHeaderBytes = udsMaxPayload + 1
			},
		},
		{
			name: "request-chunk",
			mutate: func(config *Config) {
				config.MaxRequestChunkBytes = udsMaxChunk + 1
			},
		},
		{
			name: "response-chunk",
			mutate: func(config *Config) {
				config.MaxResponseChunkBytes = udsMaxChunk + 1
			},
		},
	}
	for _, test := range tests {
		t.Run(test.name, func(t *testing.T) {
			config := CreateConfig()
			config.EngineMode = "uds"
			config.EngineSocketPath = "/private/engine.sock"
			test.mutate(config)
			if _, err := New(context.Background(), http.NotFoundHandler(), config, "uds-limit-test"); err == nil {
				t.Fatal("New() unexpectedly accepted an out-of-contract UDS limit")
			}
		})
	}
}

func TestUDSEngineUsesOneSessionForFullLifecycle(t *testing.T) {
	socketPath, server := startUDSTestServer(t, nil)
	middleware := newUDSTestMiddleware(t, socketPath, http.HandlerFunc(func(writer http.ResponseWriter, request *http.Request) {
		if _, err := io.ReadAll(request.Body); err != nil {
			t.Errorf("ReadAll(request.Body) error = %v", err)
			return
		}
		_, _ = writer.Write([]byte("result"))
	}))

	request := httptest.NewRequest(http.MethodPost, "http://example.test/uds", strings.NewReader("request"))
	request.Header.Set("X-Request-Id", "uds-full-lifecycle")
	response := httptest.NewRecorder()
	middleware.ServeHTTP(response, request)
	if got, want := response.Code, http.StatusOK; got != want {
		t.Fatalf("status = %d, want %d", got, want)
	}
	calls := server.wait(t)
	assertUDSOrder(t, calls, []byte{
		udsOpcodeBegin,
		udsOpcodeRequestChunk,
		udsOpcodeRequestEOS,
		udsOpcodeResponseHead,
		udsOpcodeResponseCommit,
		udsOpcodeResponseBody,
		udsOpcodeResponseEOS,
		udsOpcodeFinish,
		udsOpcodeDestroy,
	})
	if countUDSCalls(calls, udsOpcodeBegin) != 1 || countUDSCalls(calls, udsOpcodeDestroy) != 1 {
		t.Fatalf("expected exactly one UDS session, calls=%#v", calls)
	}
}

func TestUDSEngineAcknowledgesP1AndP2HostDenies(t *testing.T) {
	tests := []struct {
		name       string
		results    map[byte]udsTestResult
		request    *http.Request
		readBody   bool
		denyOpcode byte
	}{
		{
			name:       "phase1",
			results:    map[byte]udsTestResult{udsOpcodeBegin: {action: udsActionDeny, status: http.StatusForbidden}},
			request:    httptest.NewRequest(http.MethodGet, "http://example.test/p1", nil),
			denyOpcode: udsOpcodeBegin,
		},
		{
			name:       "phase2",
			results:    map[byte]udsTestResult{udsOpcodeRequestEOS: {action: udsActionDeny, status: http.StatusForbidden}},
			request:    httptest.NewRequest(http.MethodPost, "http://example.test/p2", strings.NewReader("request")),
			readBody:   true,
			denyOpcode: udsOpcodeRequestEOS,
		},
	}
	for _, test := range tests {
		t.Run(test.name, func(t *testing.T) {
			socketPath, server := startUDSTestServer(t, test.results)
			called := false
			middleware := newUDSTestMiddleware(t, socketPath, http.HandlerFunc(func(_ http.ResponseWriter, request *http.Request) {
				called = true
				if test.readBody {
					_, _ = io.ReadAll(request.Body)
				}
			}))
			response := httptest.NewRecorder()
			middleware.ServeHTTP(response, test.request)
			if got, want := response.Code, http.StatusForbidden; got != want {
				t.Fatalf("status = %d, want %d", got, want)
			}
			if test.name == "phase1" && called {
				t.Fatal("P1 deny unexpectedly invoked downstream handler")
			}
			calls := server.wait(t)
			if countUDSCalls(calls, test.denyOpcode) != 1 {
				t.Fatalf("missing deny opcode %d: %#v", test.denyOpcode, calls)
			}
			outcome := findUDSCall(calls, udsOpcodeOutcome)
			if outcome == nil || len(outcome.payload) != 4 || outcome.payload[1] != udsOutcomeApplied {
				t.Fatalf("missing applied host outcome: %#v", calls)
			}
		})
	}
}

func TestUDSEngineDoesNotAcknowledgeAnUnconfirmedHostWrite(t *testing.T) {
	socketPath, server := startUDSTestServer(t, map[byte]udsTestResult{
		udsOpcodeBegin: {action: udsActionDeny, status: http.StatusForbidden},
	})
	middleware := newUDSTestMiddleware(t, socketPath, http.NotFoundHandler())
	response := &failingDecisionResponseWriter{header: make(http.Header)}
	middleware.ServeHTTP(response, httptest.NewRequest(http.MethodGet, "http://example.test/p1", nil))
	if got, want := response.status, http.StatusForbidden; got != want {
		t.Fatalf("status = %d, want %d", got, want)
	}
	calls := server.wait(t)
	if outcome := findUDSCall(calls, udsOpcodeOutcome); outcome != nil {
		t.Fatalf("host outcome was recorded after failed ResponseWriter.Write: %#v", outcome)
	}
	if countUDSCalls(calls, udsOpcodeResponseCommit) != 1 {
		t.Fatalf("expected commit metadata after WriteHeader, calls=%#v", calls)
	}
}

func TestUDSEngineAppliesP3BeforeCommitAndDowngradesP4AfterCommit(t *testing.T) {
	tests := []struct {
		name        string
		results     map[byte]udsTestResult
		wantStatus  int
		wantBody    string
		lateLogOnly bool
	}{
		{
			name:       "phase3-precommit",
			results:    map[byte]udsTestResult{udsOpcodeResponseHead: {action: udsActionDeny, status: http.StatusForbidden}},
			wantStatus: http.StatusForbidden,
			wantBody:   "request rejected\n",
		},
		{
			name:        "phase4-postcommit-log-only",
			results:     map[byte]udsTestResult{udsOpcodeResponseEOS: {action: udsActionDeny, status: http.StatusForbidden}},
			wantStatus:  http.StatusOK,
			wantBody:    "firstsecond",
			lateLogOnly: true,
		},
	}
	for _, test := range tests {
		t.Run(test.name, func(t *testing.T) {
			socketPath, server := startUDSTestServer(t, test.results)
			middleware := newUDSTestMiddleware(t, socketPath, http.HandlerFunc(func(writer http.ResponseWriter, _ *http.Request) {
				writer.Header().Set("Content-Type", "text/plain")
				_, _ = writer.Write([]byte("first"))
				_, _ = writer.Write([]byte("second"))
			}))
			response := httptest.NewRecorder()
			middleware.ServeHTTP(response, httptest.NewRequest(http.MethodGet, "http://example.test/response", nil))
			if got := response.Code; got != test.wantStatus {
				t.Fatalf("status = %d, want %d", got, test.wantStatus)
			}
			if got := response.Body.String(); got != test.wantBody {
				t.Fatalf("body = %q, want %q", got, test.wantBody)
			}
			calls := server.wait(t)
			outcome := findUDSCall(calls, udsOpcodeOutcome)
			if outcome == nil || len(outcome.payload) != 4 {
				t.Fatalf("missing outcome: %#v", calls)
			}
			if test.lateLogOnly {
				if outcome.payload[0] != udsActionLogOnly || outcome.payload[1] != 0 ||
					binary.BigEndian.Uint16(outcome.payload[2:]) != http.StatusOK {
					t.Fatalf("P4 outcome is not log-only: %#v", outcome.payload)
				}
			} else if outcome.payload[1] != udsOutcomeApplied {
				t.Fatalf("P3 outcome is not applied: %#v", outcome.payload)
			}
		})
	}
}

func assertUDSOrder(t *testing.T, calls []udsTestCall, required []byte) {
	t.Helper()
	position := 0
	for _, call := range calls {
		if position < len(required) && call.opcode == required[position] {
			position++
		}
	}
	if position != len(required) {
		t.Fatalf("required UDS lifecycle %v not found in calls %#v", required, calls)
	}
}

func countUDSCalls(calls []udsTestCall, opcode byte) int {
	count := 0
	for _, call := range calls {
		if call.opcode == opcode {
			count++
		}
	}
	return count
}

func findUDSCall(calls []udsTestCall, opcode byte) *udsTestCall {
	for index := range calls {
		if calls[index].opcode == opcode {
			return &calls[index]
		}
	}
	return nil
}

type failingDecisionResponseWriter struct {
	header http.Header
	status int
}

func (writer *failingDecisionResponseWriter) Header() http.Header {
	return writer.header
}

func (writer *failingDecisionResponseWriter) WriteHeader(status int) {
	if writer.status == 0 {
		writer.status = status
	}
}

func (writer *failingDecisionResponseWriter) Write(_ []byte) (int, error) {
	if writer.status == 0 {
		writer.status = http.StatusOK
	}
	return 0, errors.New("injected response writer failure")
}
