package response_observer

import (
	"bufio"
	"bytes"
	"context"
	"encoding/binary"
	"fmt"
	"io"
	"net"
	"net/http"
	"net/http/httptest"
	"os"
	"path/filepath"
	"strings"
	"sync"
	"testing"
)

const testHandle = "0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef"

type informationalRecorder struct {
	*httptest.ResponseRecorder
	informational []int
}

func (r *informationalRecorder) WriteHeader(status int) {
	if status >= 100 && status < 200 {
		r.informational = append(r.informational, status)
		return
	}
	r.ResponseRecorder.WriteHeader(status)
}

func TestReadResultRejectsInvalidCanonicalFields(t *testing.T) {
	cases := []struct {
		name   string
		mutate func([]byte)
	}{
		{"reserved", func(payload []byte) { payload[3] = 1 }},
		{"result code", func(payload []byte) { payload[1] = resultError + 1 }},
		{"decision kind", func(payload []byte) { payload[2] = 8 }},
		{"error consistency", func(payload []byte) { binary.BigEndian.PutUint16(payload[6:], 1) }},
		{"status", func(payload []byte) { binary.BigEndian.PutUint16(payload[4:], 99) }},
		{"non HTTP status", func(payload []byte) { binary.BigEndian.PutUint16(payload[4:], 600) }},
		{"redirect", func(payload []byte) { payload[2] = decisionRedirect }},
		{"statusless deny", func(payload []byte) {
			payload[2] = decisionDeny
			binary.BigEndian.PutUint16(payload[4:], 0)
		}},
		{"statusless error", func(payload []byte) {
			payload[2] = decisionError
			binary.BigEndian.PutUint16(payload[4:], 0)
		}},
	}
	for _, test := range cases {
		t.Run(test.name, func(t *testing.T) {
			payload := make([]byte, 12)
			payload[0] = opClaim
			payload[1] = resultOK
			payload[2] = decisionAllow
			binary.BigEndian.PutUint16(payload[4:], 200)
			test.mutate(payload)
			if _, err := readResult(bufio.NewReader(bytes.NewReader(testResultFrame(payload)))); err == nil {
				t.Fatal("invalid result accepted")
			}
		})
	}
}

func TestReadResultAcceptsCanonicalStatuslessSuccess(t *testing.T) {
	for _, decision := range []byte{
		decisionAllow,
		decisionLogOnly,
		decisionDrop,
		decisionAbort,
	} {
		payload := make([]byte, 12)
		payload[0], payload[1], payload[2] = opClaim, resultOK, decision
		if got, err := readResult(bufio.NewReader(bytes.NewReader(testResultFrame(payload)))); err != nil || got.status != 0 {
			t.Fatalf("statusless decision %d was rejected: result=%+v err=%v", decision, got, err)
		}
	}
}

func TestReadResultAcceptsStatuslessCleanupAcknowledgement(t *testing.T) {
	for _, operation := range []byte{opCancel, opRelease} {
		payload := make([]byte, 12)
		payload[0], payload[1], payload[2] = operation, resultOK, decisionError
		if got, err := readResult(bufio.NewReader(bytes.NewReader(testResultFrame(payload)))); err != nil || got.status != 0 {
			t.Fatalf("statusless cleanup acknowledgement for op %d was rejected: result=%+v err=%v", operation, got, err)
		}
	}
}

func TestReadResultRejectsHeaderControlResultText(t *testing.T) {
	cases := []struct {
		name     string
		decision byte
		status   int
		redirect []byte
		rule     []byte
	}{
		{"redirect C0", decisionRedirect, http.StatusFound, []byte("/safe\x00path"), nil},
		{"redirect DEL", decisionRedirect, http.StatusFound, []byte("/safe\x7fpath"), nil},
		{"rule C0", decisionAllow, http.StatusOK, nil, []byte("rule\x1fname")},
		{"rule DEL", decisionAllow, http.StatusOK, nil, []byte("rule\x7fname")},
	}
	for _, test := range cases {
		t.Run(test.name, func(t *testing.T) {
			payload := make([]byte, 12+len(test.redirect)+len(test.rule))
			payload[0], payload[1], payload[2] = opClaim, resultOK, test.decision
			binary.BigEndian.PutUint16(payload[4:], uint16(test.status))
			binary.BigEndian.PutUint16(payload[8:], uint16(len(test.redirect)))
			binary.BigEndian.PutUint16(payload[10:], uint16(len(test.rule)))
			copy(payload[12:], test.redirect)
			copy(payload[12+len(test.redirect):], test.rule)
			if _, err := readResult(bufio.NewReader(bytes.NewReader(testResultFrame(payload)))); err == nil {
				t.Fatal("result text with a header control byte was accepted")
			}
		})
	}
}

func testResultFrame(payload []byte) []byte {
	frame := make([]byte, frameHeaderSize+len(payload))
	copy(frame[:4], []byte("MRC1"))
	frame[4], frame[5] = protocolVersion, opResult
	binary.BigEndian.PutUint32(frame[8:], uint32(len(payload)))
	copy(frame[frameHeaderSize:], payload)
	return frame
}

func TestResponseHeaderEncodingUsesLengthThenBytesOrder(t *testing.T) {
	payload := encodeResponseHeaders(http.StatusOK, http.Header{"X-Test": {"value"}})
	if payload == nil || binary.BigEndian.Uint16(payload[0:2]) != http.StatusOK {
		t.Fatalf("invalid header payload: %v", payload)
	}
	versionLen := int(binary.BigEndian.Uint16(payload[2:4]))
	offset := 4 + versionLen
	if string(payload[4:offset]) != "HTTP/1.1" {
		t.Fatalf("version=%q", payload[4:offset])
	}
	if binary.BigEndian.Uint16(payload[offset:]) != 1 {
		t.Fatalf("header count missing")
	}
	offset += 2
	nameLen := int(binary.BigEndian.Uint16(payload[offset:]))
	offset += 2
	if string(payload[offset:offset+nameLen]) != "X-Test" {
		t.Fatalf("name order malformed: %q", payload[offset:offset+nameLen])
	}
	offset += nameLen
	valueLen := int(binary.BigEndian.Uint16(payload[offset:]))
	offset += 2
	if string(payload[offset:offset+valueLen]) != "value" {
		t.Fatalf("value order malformed: %q", payload[offset:offset+valueLen])
	}
}

func TestResponseHeaderEncodingFitsIndependentMRC1WireCapacity(t *testing.T) {
	const (
		independentFrameLimit = 65536
		independentFixedBytes = 2 + 2 + len("HTTP/1.1") + 2
		fieldCount            = 128
		fieldLengthWords      = 4
		fieldName             = "X-000"
	)
	maxHeaderContent := independentFrameLimit - independentFixedBytes -
		fieldCount*fieldLengthWords
	values := make(http.Header, fieldCount)
	remaining := maxHeaderContent - fieldCount*len(fieldName)
	for index := 0; index < fieldCount; index++ {
		name := fmt.Sprintf("X-%03d", index)
		length := remaining / (fieldCount - index)
		remaining -= length
		values[name] = []string{strings.Repeat("v", length)}
	}
	if payload := encodeResponseHeaders(http.StatusOK, values); len(payload) != independentFrameLimit {
		t.Fatalf("wire-boundary payload length=%d, want %d", len(payload), independentFrameLimit)
	}
	values["X-000"][0] += "v"
	if payload := encodeResponseHeaders(http.StatusOK, values); payload != nil {
		t.Fatalf("over-capacity P3 payload was accepted with length %d", len(payload))
	}

	const (
		sparseFieldCount    = 10
		sparseValueSize     = 6510
		sparseContentBytes  = sparseFieldCount * (len(fieldName) + sparseValueSize)
		sparsePayloadLength = independentFixedBytes +
			sparseFieldCount*fieldLengthWords + sparseContentBytes
	)
	sparse := make(http.Header, sparseFieldCount)
	for index := 0; index < sparseFieldCount; index++ {
		name := fmt.Sprintf("X-%03d", index)
		sparse[name] = []string{strings.Repeat("v", sparseValueSize)}
	}
	if payload := encodeResponseHeaders(http.StatusOK, sparse); len(payload) != sparsePayloadLength {
		t.Fatalf("encodeResponseHeaders(sparse) length = %d, want %d", len(payload), sparsePayloadLength)
	}
}

func TestResponseHeaderEncodingAllowsCommonHeaderCountLimit(t *testing.T) {
	const acceptedFieldCount = 256
	headers := make(http.Header, acceptedFieldCount)
	for index := 0; index < acceptedFieldCount; index++ {
		headers[fmt.Sprintf("X-%03d", index)] = []string{"v"}
	}
	if payload := encodeResponseHeaders(http.StatusOK, headers); payload == nil {
		t.Fatal("encodeResponseHeaders(256 headers) = nil, want payload")
	}
	headers["X-256"] = []string{"v"}
	if encodeResponseHeaders(http.StatusOK, headers) != nil {
		t.Fatal("encodeResponseHeaders(257 headers) accepted, want nil")
	}
}

func TestOutcomeActionMappingSeparatesDecisionKind(t *testing.T) {
	for kind, want := range map[byte]byte{decisionAllow: outcomeAllow, decisionDeny: outcomeDeny, decisionRedirect: outcomeRedirect, decisionDrop: outcomeDrop, decisionAbort: outcomeAbort, decisionError: outcomeError, decisionUnsupported: outcomeUnsupported} {
		if got := outcomeAction(kind, true); got != want {
			t.Fatalf("kind %d action=%d want %d", kind, got, want)
		}
	}
	if got := outcomeAction(decisionDeny, false); got != outcomeLogOnly {
		t.Fatalf("late deny action=%d", got)
	}
}

func TestDisruptiveIncludesFailClosedEngineOutcomes(t *testing.T) {
	for _, kind := range []byte{decisionDeny, decisionRedirect, decisionDrop, decisionAbort, decisionError, decisionUnsupported} {
		if !disruptive(kind) {
			t.Fatalf("decision kind %d must be disruptive", kind)
		}
	}
	if disruptive(decisionAllow) || disruptive(decisionLogOnly) {
		t.Fatal("allow and log-only must remain non-disruptive")
	}
}

func TestP3DenyOutcomeDoesNotSetConnectionAbortedFlag(t *testing.T) {
	deny := encodeOutcome(decisionDeny, false, false, http.StatusForbidden)
	if deny[0] != outcomeDeny || deny[1] != 0 {
		t.Fatalf("deny outcome=%v, want action deny and connection_aborted=0", deny)
	}
	abort := encodeOutcome(decisionAbort, false, true, http.StatusServiceUnavailable)
	if abort[0] != outcomeAbort || abort[1] != 1 {
		t.Fatalf("abort outcome=%v, want action abort and connection_aborted=1", abort)
	}
}

func TestMiddlewareStreamsHeaderOnlyResponseAndStripsHandle(t *testing.T) {
	path, stop, operations := startFakeObserver(t, func(byte) (byte, byte) { return decisionAllow, resultOK })
	defer stop()
	handler := newObserverHandler(t, path, http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		if r.Header.Get("X-Msconnector-Response-Handle") != "" {
			t.Error("handle leaked upstream")
		}
		if _, bypass := w.(interface{ Unwrap() http.ResponseWriter }); bypass {
			t.Error("observer exposes ResponseWriter.Unwrap")
		}
		w.Header().Set("X-Test", "yes")
		w.WriteHeader(http.StatusNoContent)
	}))
	req := newObserverRequest()
	recorder := httptest.NewRecorder()
	handler.ServeHTTP(recorder, req)
	if recorder.Code != http.StatusNoContent {
		t.Fatalf("status=%d, want 204", recorder.Code)
	}
	want := []byte{opClaim, opResponseHeaders, opCommit, opResponseEOS, opRelease}
	if got := operations.snapshot(); !sameBytes(got, want) {
		t.Fatalf("operations=%v, want %v", got, want)
	}
}

func TestMiddlewareCancelsEscapingPanicWithoutSuccessfulFinalization(t *testing.T) {
	recorder, recovered, operations := runPanicMiddleware(t, "downstream panic", false)
	if recovered != "downstream panic" {
		t.Fatalf("recovered panic = %#v, want original value", recovered)
	}
	if recorder.Body.Len() != 0 {
		t.Fatalf("panic path synthesized response body %q", recorder.Body.String())
	}
	if got, want := operations.snapshot(), []byte{opClaim, opCancel}; !sameBytes(got, want) {
		t.Fatalf("operations=%v, want typed cancellation without finalization %v", got, want)
	}
	if got := operations.payloadFor(opCancel); len(got) != 1 || got[0] != cancelConnectorError {
		t.Fatalf("cancel payload=%v, want connector-error value %d", got, cancelConnectorError)
	}
}

func TestMiddlewareCancelsEscapingPanicAfterCommitWithoutEOSOrRelease(t *testing.T) {
	recorder, recovered, operations := runPanicMiddleware(t, "downstream panic after commit", true)
	if recovered != "downstream panic after commit" {
		t.Fatalf("recovered panic = %#v, want original value", recovered)
	}
	if recorder.Code != http.StatusNoContent {
		t.Fatalf("status=%d, want committed upstream status 204", recorder.Code)
	}
	if got, want := operations.snapshot(), []byte{opClaim, opResponseHeaders, opCommit, opCancel}; !sameBytes(got, want) {
		t.Fatalf("operations=%v, want cancellation without EOS/release %v", got, want)
	}
}

func runPanicMiddleware(t *testing.T, panicValue string, commitResponse bool) (*httptest.ResponseRecorder, any, *opLog) {
	t.Helper()
	path, stop, operations := startFakeObserver(t, func(byte) (byte, byte) { return decisionAllow, resultOK })
	t.Cleanup(stop)
	handler := newObserverHandler(t, path, http.HandlerFunc(func(w http.ResponseWriter, _ *http.Request) {
		if commitResponse {
			w.WriteHeader(http.StatusNoContent)
		}
		panic(panicValue)
	}))
	req := newObserverRequest()
	recorder := httptest.NewRecorder()
	var recovered any
	func() {
		defer func() { recovered = recover() }()
		handler.ServeHTTP(recorder, req)
	}()
	return recorder, recovered, operations
}

func newObserverHandler(t *testing.T, path string, next http.Handler) http.Handler {
	t.Helper()
	handler, err := New(nil, next, &Config{SocketPath: path, TimeoutMillis: 1000}, "")
	if err != nil {
		t.Fatal(err)
	}
	return handler
}

func newObserverRequest() *http.Request {
	req := httptest.NewRequest(http.MethodGet, "http://example.test/", nil)
	req.Header.Set("X-Msconnector-Response-Handle", testHandle)
	return req
}

func TestMiddlewareFailsClosedForMissingOrMalformedHandle(t *testing.T) {
	called := false
	handler, err := New(nil, http.HandlerFunc(func(http.ResponseWriter, *http.Request) { called = true }), &Config{SocketPath: "/run/no-such-observer.sock", TimeoutMillis: 10}, "")
	if err != nil {
		t.Fatal(err)
	}
	for _, value := range []string{"", "ABC", "0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdeg"} {
		req := httptest.NewRequest(http.MethodGet, "http://example.test/", nil)
		if value != "" {
			req.Header.Set("X-Msconnector-Response-Handle", value)
		}
		recorder := httptest.NewRecorder()
		handler.ServeHTTP(recorder, req)
		if recorder.Code != http.StatusServiceUnavailable {
			t.Fatalf("handle %q status=%d", value, recorder.Code)
		}
	}
	if called {
		t.Fatal("upstream called after invalid handle")
	}
}

func TestMiddlewareFailsClosedForRejectedReplay(t *testing.T) {
	path, stop, _ := startFakeObserver(t, func(op byte) (byte, byte) {
		if op == opClaim {
			return decisionAllow, 1
		}
		return decisionAllow, resultOK
	})
	defer stop()
	called := false
	handler := newObserverHandler(t, path, http.HandlerFunc(func(http.ResponseWriter, *http.Request) { called = true }))
	req := newObserverRequest()
	recorder := httptest.NewRecorder()
	handler.ServeHTTP(recorder, req)
	if recorder.Code != http.StatusServiceUnavailable || called {
		t.Fatalf("replayed handle status=%d upstreamCalled=%v", recorder.Code, called)
	}
}

func TestMiddlewareAppliesPrecommitBlockAndCancel(t *testing.T) {
	path, stop, operations := startFakeObserver(t, func(op byte) (byte, byte) {
		if op == opResponseHeaders {
			return decisionDeny, resultOK
		}
		return decisionAllow, resultOK
	})
	defer stop()
	handler := newObserverHandler(t, path, http.HandlerFunc(func(w http.ResponseWriter, _ *http.Request) {
		w.Header().Set("Content-Length", "21")
		w.Header().Set("Set-Cookie", "session=upstream")
		w.Header().Set("Location", "https://upstream.invalid/private")
		w.Header().Set("WWW-Authenticate", "Basic realm=upstream")
		w.Header().Set("X-Msconnector-Response-Handle", "opaque-upstream-handle")
		w.WriteHeader(http.StatusOK)
		if written, err := w.Write([]byte("must-not-reach-client")); err != nil || written != len("must-not-reach-client") {
			t.Errorf("terminal upstream body write=%d err=%v", written, err)
		}
	}))
	req := newObserverRequest()
	recorder := httptest.NewRecorder()
	handler.ServeHTTP(recorder, req)
	if recorder.Code != http.StatusForbidden {
		t.Fatalf("status=%d, want 403", recorder.Code)
	}
	if recorder.Body.Len() != 0 {
		t.Fatalf("terminal upstream body reached client: %q", recorder.Body.String())
	}
	if got := recorder.Header().Get("Content-Length"); got != "" {
		t.Fatalf("terminal response retained upstream content length %q", got)
	}
	for _, header := range []string{"Set-Cookie", "Location", "WWW-Authenticate", "X-Msconnector-Response-Handle"} {
		if got := recorder.Header().Get(header); got != "" {
			t.Fatalf("terminal response retained upstream %s=%q", header, got)
		}
	}
	got := operations.snapshot()
	want := []byte{opClaim, opResponseHeaders, opOutcome, opCancel}
	if !sameBytes(got, want) {
		t.Fatalf("operations=%v, want %v", got, want)
	}
}

func TestMiddlewareConsumesImplicitWriteAfterPrecommitBlock(t *testing.T) {
	path, stop, _ := startFakeObserver(t, func(op byte) (byte, byte) {
		if op == opResponseHeaders {
			return decisionDeny, resultOK
		}
		return decisionAllow, resultOK
	})
	defer stop()
	var written int
	var writeErr error
	handler := newObserverHandler(t, path, http.HandlerFunc(func(w http.ResponseWriter, _ *http.Request) {
		written, writeErr = w.Write([]byte("discarded"))
	}))
	req := newObserverRequest()
	recorder := httptest.NewRecorder()
	handler.ServeHTTP(recorder, req)
	if written != len("discarded") || writeErr != nil {
		t.Fatalf("implicit write=%d err=%v, want consumed body without error", written, writeErr)
	}
	if recorder.Code != http.StatusForbidden {
		t.Fatalf("status=%d, want 403", recorder.Code)
	}
}

func TestMiddlewareDefersP3UntilTheFinalResponse(t *testing.T) {
	responseHeaderCount := 0
	path, stop, operations := startFakeObserver(t, func(op byte) (byte, byte) {
		if op == opResponseHeaders {
			responseHeaderCount++
			if responseHeaderCount > 1 {
				return decisionError, resultError
			}
		}
		return decisionAllow, resultOK
	})
	defer stop()
	handler, err := New(nil, http.HandlerFunc(func(w http.ResponseWriter, _ *http.Request) {
		w.WriteHeader(http.StatusEarlyHints)
		w.WriteHeader(http.StatusProcessing)
		w.WriteHeader(http.StatusNoContent)
	}), &Config{SocketPath: path, TimeoutMillis: 1000}, "")
	if err != nil {
		t.Fatal(err)
	}
	req := httptest.NewRequest(http.MethodGet, "http://example.test/", nil)
	req.Header.Set("X-Msconnector-Response-Handle", testHandle)
	recorder := &informationalRecorder{ResponseRecorder: httptest.NewRecorder()}
	handler.ServeHTTP(recorder, req)
	if recorder.Code != http.StatusNoContent {
		t.Fatalf("status=%d, want 204", recorder.Code)
	}
	if got, want := recorder.informational, []int{http.StatusEarlyHints, http.StatusProcessing}; !sameStatusCodes(got, want) {
		t.Fatalf("informational statuses=%v, want %v", got, want)
	}
	want := []byte{opClaim, opResponseHeaders, opCommit, opResponseEOS, opRelease}
	if got := operations.snapshot(); !sameBytes(got, want) {
		t.Fatalf("operations=%v, want %v", got, want)
	}
}

func TestMiddlewareRejectsProtocolSwitchBeforeCommit(t *testing.T) {
	path, stop, operations := startFakeObserver(t, func(byte) (byte, byte) {
		return decisionAllow, resultOK
	})
	defer stop()
	handler, err := New(nil, http.HandlerFunc(func(w http.ResponseWriter, _ *http.Request) {
		w.WriteHeader(http.StatusSwitchingProtocols)
	}), &Config{SocketPath: path, TimeoutMillis: 1000}, "")
	if err != nil {
		t.Fatal(err)
	}
	req := httptest.NewRequest(http.MethodGet, "http://example.test/", nil)
	req.Header.Set("X-Msconnector-Response-Handle", testHandle)
	recorder := httptest.NewRecorder()
	handler.ServeHTTP(recorder, req)
	if recorder.Code != http.StatusServiceUnavailable {
		t.Fatalf("status=%d, want 503", recorder.Code)
	}
	if got, want := operations.snapshot(), []byte{opClaim, opCancel}; !sameBytes(got, want) {
		t.Fatalf("operations=%v, want precommit cleanup %v", got, want)
	}
}

func TestMiddlewareCancellationAfterClaimSendsBoundedCancel(t *testing.T) {
	path, stop, operations := startFakeObserver(t, func(op byte) (byte, byte) {
		return decisionAllow, resultOK
	})
	defer stop()
	requestContext, cancelRequest := context.WithCancel(context.Background())
	defer cancelRequest()
	handler, err := New(nil, http.HandlerFunc(func(w http.ResponseWriter, _ *http.Request) {
		cancelRequest()
		w.WriteHeader(http.StatusOK)
	}), &Config{SocketPath: path, TimeoutMillis: 1000}, "")
	if err != nil {
		t.Fatal(err)
	}
	req := httptest.NewRequest(http.MethodGet, "http://example.test/", nil).WithContext(requestContext)
	req.Header.Set("X-Msconnector-Response-Handle", testHandle)
	recorder := httptest.NewRecorder()
	handler.ServeHTTP(recorder, req)
	if recorder.Code != http.StatusServiceUnavailable {
		t.Fatalf("status=%d, want cancellation fail-closed 503", recorder.Code)
	}
	if got, want := operations.snapshot(), []byte{opClaim, opCancel}; !sameBytes(got, want) {
		t.Fatalf("operations=%v, want bounded cleanup %v", got, want)
	}
}

func TestMiddlewareUsesClientCancelForDownstreamWriteFailure(t *testing.T) {
	path, stop, operations := startFakeObserver(t, func(byte) (byte, byte) { return decisionAllow, resultOK })
	defer stop()
	handler, err := New(nil, http.HandlerFunc(func(w http.ResponseWriter, _ *http.Request) {
		_, _ = w.Write([]byte("downstream failure"))
	}), &Config{SocketPath: path, TimeoutMillis: 1000}, "")
	if err != nil {
		t.Fatal(err)
	}
	req := httptest.NewRequest(http.MethodGet, "http://example.test/", nil)
	req.Header.Set("X-Msconnector-Response-Handle", testHandle)
	handler.ServeHTTP(failingResponseWriter{}, req)
	if got, want := operations.snapshot(), []byte{opClaim, opResponseHeaders, opCommit, opResponseBody, opCancel}; !sameBytes(got, want) {
		t.Fatalf("operations=%v, want client cleanup %v", got, want)
	}
	if got := operations.payloadFor(opCancel); len(got) != 1 || got[0] != 0 {
		t.Fatalf("cancel payload=%v, want client-cancel value 0", got)
	}
}

func TestMiddlewareSendsBoundedResponseBodyChunks(t *testing.T) {
	path, stop, operations := startFakeObserver(t, func(byte) (byte, byte) { return decisionAllow, resultOK })
	defer stop()
	handler := newObserverHandler(t, path, http.HandlerFunc(func(w http.ResponseWriter, _ *http.Request) {
		_, _ = w.Write(make([]byte, maxBodyChunk+7))
	}))
	req := newObserverRequest()
	recorder := httptest.NewRecorder()
	handler.ServeHTTP(recorder, req)
	if recorder.Code != http.StatusOK || recorder.Body.Len() != maxBodyChunk+7 {
		t.Fatalf("response status/body=%d/%d", recorder.Code, recorder.Body.Len())
	}
	want := []byte{opClaim, opResponseHeaders, opCommit, opResponseBody, opResponseBody, opResponseEOS, opRelease}
	if got := operations.snapshot(); !sameBytes(got, want) {
		t.Fatalf("operations=%v, want %v", got, want)
	}
}

func TestMiddlewareStopsBodyOnCanonicalResultFailure(t *testing.T) {
	path, stop, operations := startFakeObserver(t, func(op byte) (byte, byte) {
		if op == opResponseBody {
			return decisionError, resultError
		}
		return decisionAllow, resultOK
	})
	defer stop()
	handler := newObserverHandler(t, path, http.HandlerFunc(func(w http.ResponseWriter, _ *http.Request) {
		if _, err := w.Write([]byte("must-not-be-forwarded")); err == nil {
			t.Error("body write succeeded after response-companion failure")
		}
	}))
	req := newObserverRequest()
	recorder := httptest.NewRecorder()
	handler.ServeHTTP(recorder, req)
	if recorder.Body.Len() != 0 {
		t.Fatalf("body was forwarded after response-companion failure: %q", recorder.Body.String())
	}
	want := []byte{opClaim, opResponseHeaders, opCommit, opResponseBody, opCancel}
	if got := operations.snapshot(); !sameBytes(got, want) {
		t.Fatalf("operations=%v, want %v", got, want)
	}
	if got := operations.payloadFor(opCancel); len(got) != 1 || got[0] != cancelInvalidEngine {
		t.Fatalf("cancel payload=%v, want invalid-engine value %d", got, cancelInvalidEngine)
	}
}

func TestNormalizeConfigRejectsNonCanonicalSocketPath(t *testing.T) {
	for _, socketPath := range []string{"relative.sock", "/run/modsecurity/../observer.sock", "/run//modsecurity/observer.sock"} {
		if _, err := normalizeConfig(&Config{SocketPath: socketPath, TimeoutMillis: 1000}); err == nil {
			t.Fatalf("accepted non-canonical socket path %q", socketPath)
		}
	}
}

func TestConcurrentRequestsUseIndependentSessions(t *testing.T) {
	path, stop, _ := startFakeObserver(t, func(byte) (byte, byte) { return decisionAllow, resultOK })
	defer stop()
	handler, err := New(nil, http.HandlerFunc(func(w http.ResponseWriter, _ *http.Request) { _, _ = w.Write([]byte("ok")) }), &Config{SocketPath: path, TimeoutMillis: 1000}, "")
	if err != nil {
		t.Fatal(err)
	}
	var wait sync.WaitGroup
	for i := 0; i < 8; i++ {
		wait.Add(1)
		go func() {
			defer wait.Done()
			req := httptest.NewRequest(http.MethodGet, "http://example.test/", nil)
			req.Header.Set("X-Msconnector-Response-Handle", testHandle)
			handler.ServeHTTP(httptest.NewRecorder(), req)
		}()
	}
	wait.Wait()
}

func TestReleaseFailureTriggersDeterministicCleanup(t *testing.T) {
	path, stop, operations := startFakeObserver(t, func(op byte) (byte, byte) {
		if op == opRelease {
			return decisionAllow, 1
		}
		return decisionAllow, resultOK
	})
	defer stop()
	handler := newObserverHandler(t, path, http.HandlerFunc(func(w http.ResponseWriter, _ *http.Request) { w.WriteHeader(http.StatusNoContent) }))
	req := newObserverRequest()
	recorder := httptest.NewRecorder()
	handler.ServeHTTP(recorder, req)
	if recorder.Code != http.StatusNoContent {
		t.Fatalf("status=%d", recorder.Code)
	}
	got := operations.snapshot()
	if len(got) < 6 || got[len(got)-2] != opRelease || got[len(got)-1] != opCancel {
		t.Fatalf("cleanup operations=%v", got)
	}
	if got := operations.payloadFor(opCancel); len(got) != 1 || got[0] != cancelInvalidEngine {
		t.Fatalf("cancel payload=%v, want invalid-engine value %d", got, cancelInvalidEngine)
	}
}

func TestLateOutcomeFailureCancelsWithoutRelease(t *testing.T) {
	path, stop, operations := startFakeObserver(t, func(op byte) (byte, byte) {
		if op == opResponseEOS {
			return decisionError, resultOK
		}
		if op == opOutcome {
			return decisionError, resultError
		}
		return decisionAllow, resultOK
	})
	defer stop()
	handler := newObserverHandler(t, path, http.HandlerFunc(func(w http.ResponseWriter, _ *http.Request) { w.WriteHeader(http.StatusNoContent) }))
	req := newObserverRequest()
	recorder := httptest.NewRecorder()
	handler.ServeHTTP(recorder, req)
	if recorder.Code != http.StatusNoContent {
		t.Fatalf("status=%d", recorder.Code)
	}
	want := []byte{opClaim, opResponseHeaders, opCommit, opResponseEOS, opOutcome, opCancel}
	if got := operations.snapshot(); !sameBytes(got, want) {
		t.Fatalf("operations=%v, want %v", got, want)
	}
	if got := operations.payloadFor(opCancel); len(got) != 1 || got[0] != cancelProtocolError {
		t.Fatalf("cancel payload=%v, want protocol-error value %d", got, cancelProtocolError)
	}
}

type opLog struct {
	mu       sync.Mutex
	values   []byte
	payloads map[byte][][]byte
}

func (l *opLog) add(value byte, payload []byte) {
	l.mu.Lock()
	defer l.mu.Unlock()
	l.values = append(l.values, value)
	if l.payloads == nil {
		l.payloads = make(map[byte][][]byte)
	}
	l.payloads[value] = append(l.payloads[value], append([]byte(nil), payload...))
}
func (l *opLog) snapshot() []byte {
	l.mu.Lock()
	defer l.mu.Unlock()
	return append([]byte(nil), l.values...)
}
func (l *opLog) payloadFor(value byte) []byte {
	l.mu.Lock()
	defer l.mu.Unlock()
	values := l.payloads[value]
	if len(values) == 0 {
		return nil
	}
	return append([]byte(nil), values[len(values)-1]...)
}
func sameBytes(a, b []byte) bool {
	if len(a) != len(b) {
		return false
	}
	for i := range a {
		if a[i] != b[i] {
			return false
		}
	}
	return true
}

func sameStatusCodes(actual, expected []int) bool {
	if len(actual) != len(expected) {
		return false
	}
	for index := range actual {
		if actual[index] != expected[index] {
			return false
		}
	}
	return true
}

type failingResponseWriter struct{}

func (failingResponseWriter) Header() http.Header { return make(http.Header) }
func (failingResponseWriter) WriteHeader(int)     {}
func (failingResponseWriter) Write([]byte) (int, error) {
	return 0, io.ErrClosedPipe
}

func startFakeObserver(t *testing.T, decide func(byte) (byte, byte)) (string, func(), *opLog) {
	t.Helper()
	path := os.Getenv("MSCONNECTOR_TEST_SOCKET_PATH")
	if path == "" {
		socketDir, err := os.MkdirTemp("", "msco")
		if err != nil {
			t.Fatal(err)
		}
		t.Cleanup(func() { _ = os.RemoveAll(socketDir) })
		path = filepath.Join(socketDir, "observer.sock")
	}
	_ = os.Remove(path)
	listener, err := net.Listen("unix", path)
	if err != nil {
		t.Fatal(err)
	}
	log := &opLog{}
	done := make(chan struct{})
	var workers sync.WaitGroup
	go func() {
		for {
			conn, err := listener.Accept()
			if err != nil {
				select {
				case <-done:
					return
				default:
					continue
				}
			}
			workers.Add(1)
			go func() { defer workers.Done(); serveFake(conn, log, decide) }()
		}
	}()
	return path, func() { close(done); _ = listener.Close(); workers.Wait(); _ = os.Remove(path) }, log
}

func serveFake(conn net.Conn, log *opLog, decide func(byte) (byte, byte)) {
	defer conn.Close()
	reader := bufio.NewReader(conn)
	for {
		opcode, payload, err := readTestFrame(reader)
		if err != nil {
			return
		}
		log.add(opcode, payload)
		action, code := decide(opcode)
		if err := writeTestResult(conn, opcode, action, code); err != nil {
			return
		}
		if opcode == opRelease && code == resultOK {
			return
		}
	}
}

func readTestFrame(reader *bufio.Reader) (byte, []byte, error) {
	header := make([]byte, frameHeaderSize)
	if _, err := io.ReadFull(reader, header); err != nil {
		return 0, nil, err
	}
	if string(header[:4]) != "MRC1" || header[4] != protocolVersion {
		return 0, nil, errProtocol
	}
	length := binary.BigEndian.Uint32(header[8:])
	if length > maxPayload {
		return 0, nil, errProtocol
	}
	payload := make([]byte, length)
	_, err := io.ReadFull(reader, payload)
	return header[5], payload, err
}

func writeTestResult(conn net.Conn, requestOpcode, action, code byte) error {
	payload := make([]byte, 12)
	payload[0], payload[1], payload[2] = requestOpcode, code, action
	if !(code == resultOK && (action == decisionAllow || action == decisionLogOnly ||
		action == decisionDrop || action == decisionAbort)) {
		binary.BigEndian.PutUint16(payload[4:], 200)
	}
	if code != resultOK {
		binary.BigEndian.PutUint16(payload[6:], 1)
	}
	header := make([]byte, frameHeaderSize)
	copy(header[:4], []byte("MRC1"))
	header[4], header[5] = protocolVersion, opResult
	binary.BigEndian.PutUint32(header[8:], uint32(len(payload)))
	if _, err := conn.Write(header); err != nil {
		return err
	}
	_, err := conn.Write(payload)
	return err
}
