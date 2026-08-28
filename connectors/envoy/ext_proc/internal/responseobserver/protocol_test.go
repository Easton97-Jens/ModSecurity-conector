package responseobserver

import (
	"encoding/binary"
	"fmt"
	"io"
	"net"
	"net/http"
	"os"
	"path/filepath"
	"reflect"
	"strings"
	"testing"
	"time"

	corev3 "github.com/envoyproxy/go-control-plane/envoy/config/core/v3"
	extprocv3 "github.com/envoyproxy/go-control-plane/envoy/service/ext_proc/v3"
)

func testSocketDir(t *testing.T) string {
	t.Helper()
	dir, err := os.MkdirTemp("", "mso-")
	if err != nil {
		t.Fatal(err)
	}
	t.Cleanup(func() { _ = os.RemoveAll(dir) })
	return dir
}

func TestValidHandleRejectsCallerIdentifiers(t *testing.T) {
	if !validHandle("0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef") {
		t.Fatal("expected valid opaque handle")
	}
	for _, value := range []string{"", "x-request-id", "0123456789ABCDEF0123456789abcdef0123456789abcdef0123456789abcdef", "0123456789abcdef"} {
		if validHandle(value) {
			t.Fatalf("accepted invalid handle %q", value)
		}
	}
}

func TestClientFramesBoundedOrderedOperations(t *testing.T) {
	dir := testSocketDir(t)
	path := filepath.Join(dir, "observer.sock")
	listener, err := net.Listen("unix", path)
	if err != nil {
		t.Fatal(err)
	}
	defer listener.Close()
	seen := make(chan byte, 8)
	versionSeen := make(chan bool, 1)
	go func() {
		conn, err := listener.Accept()
		if err != nil {
			return
		}
		defer conn.Close()
		for {
			var h [frameSize]byte
			if _, err := io.ReadFull(conn, h[:]); err != nil {
				return
			}
			length := int(binary.BigEndian.Uint32(h[8:]))
			payload := make([]byte, length)
			if _, err := io.ReadFull(conn, payload); err != nil {
				return
			}
			if h[5] == opResponseHeaders {
				versionSeen <- string(payload[4:12]) == "HTTP/1.1"
			}
			seen <- h[5]
			resultPayload := make([]byte, 12)
			resultPayload[0], resultPayload[1], resultPayload[2] = h[5], 0, decisionAllow
			/* Common encodes a successful ALLOW without an HTTP response status.
			 * This is the real MRC1 claim/commit/body/EOS interoperability case,
			 * not a synthetic 200 acknowledgement. */
			binary.BigEndian.PutUint16(resultPayload[4:], 0)
			var out [frameSize]byte
			copy(out[:4], []byte("MRC1"))
			out[4], out[5] = protocolVersion, resultOpcode
			binary.BigEndian.PutUint32(out[8:], uint32(len(resultPayload)))
			if _, err := conn.Write(out[:]); err != nil {
				return
			}
			if _, err := conn.Write(resultPayload); err != nil {
				return
			}
		}
	}()
	c, err := dial(path, time.Second)
	if err != nil {
		t.Fatal(err)
	}
	defer c.close()
	handle := "0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef"
	if _, err = c.claim(handle); err != nil {
		t.Fatal(err)
	}
	if _, err = c.responseHeaders(200, []header{{name: ":status", value: "200"}}); err != nil {
		t.Fatal(err)
	}
	if _, err = c.commit(true, false); err != nil {
		t.Fatal(err)
	}
	if _, err = c.body([]byte("body")); err != nil {
		t.Fatal(err)
	}
	if _, err = c.eos(); err != nil {
		t.Fatal(err)
	}
	if _, err = c.release(); err != nil {
		t.Fatal(err)
	}
	close(seen)
	var got []byte
	for op := range seen {
		got = append(got, op)
	}
	want := []byte{opClaim, opResponseHeaders, opCommit, opResponseBody, opResponseEOS, opRelease}
	if !reflect.DeepEqual(got, want) {
		t.Fatalf("operations = %v, want %v", got, want)
	}
	if !<-versionSeen {
		t.Fatal("P3 did not carry HTTP/1.1")
	}
}

func TestCancelCarriesTypedTerminationCause(t *testing.T) {
	causes := []byte{
		terminationClientCancel,
		terminationUpstreamDisconnect,
		terminationConnectorError,
		terminationProtocolError,
		terminationEngineTimeout,
		terminationEngineUnavailable,
		terminationInvalidEngineResponse,
	}
	for _, wantCause := range causes {
		t.Run(fmt.Sprintf("cause-%d", wantCause), func(t *testing.T) {
			left, right := net.Pipe()
			defer left.Close()
			defer right.Close()
			seen := make(chan []byte, 1)
			go func() {
				var h [frameSize]byte
				if _, err := io.ReadFull(right, h[:]); err != nil {
					return
				}
				payload := make([]byte, binary.BigEndian.Uint32(h[8:]))
				if _, err := io.ReadFull(right, payload); err != nil {
					return
				}
				seen <- append([]byte{h[4], h[5]}, payload...)
				resultPayload := make([]byte, 12)
				resultPayload[0], resultPayload[1], resultPayload[2] = opCancel, resultOK, decisionError
				var out [frameSize]byte
				copy(out[:4], []byte("MRC1"))
				out[4], out[5] = protocolVersion, resultOpcode
				binary.BigEndian.PutUint32(out[8:], uint32(len(resultPayload)))
				_, _ = right.Write(out[:])
				_, _ = right.Write(resultPayload)
			}()
			c := &client{conn: left, timeout: time.Second}
			if _, err := c.cancel(wantCause); err != nil {
				t.Fatal(err)
			}
			frame := <-seen
			if frame[0] != protocolVersion || frame[1] != opCancel || !reflect.DeepEqual(frame[2:], []byte{wantCause}) {
				t.Fatalf("cancel frame = %v, want version/op/cause [%d %d %d]", frame, protocolVersion, opCancel, wantCause)
			}
		})
	}
}

func TestFailureCauseMappingDoesNotAliasUpstreamDisconnect(t *testing.T) {
	for _, test := range []struct {
		name string
		got  byte
		want byte
	}{
		{name: "connector", got: causeForTransport(io.ErrUnexpectedEOF), want: terminationConnectorError},
		{name: "timeout", got: causeForTransport(os.ErrDeadlineExceeded), want: terminationEngineTimeout},
		{name: "protocol", got: causeForTransport(fmt.Errorf("invalid result frame")), want: terminationProtocolError},
		{name: "engine-timeout", got: causeForErrorCode(13), want: terminationEngineTimeout},
		{name: "engine-unavailable", got: causeForErrorCode(4), want: terminationEngineUnavailable},
		{name: "invalid-engine-response", got: causeForErrorCode(99), want: terminationInvalidEngineResponse},
	} {
		t.Run(test.name, func(t *testing.T) {
			if test.got == terminationUpstreamDisconnect || test.got != test.want {
				t.Fatalf("cause = %d, want %d and never upstream disconnect", test.got, test.want)
			}
		})
	}
}

func TestDecisionKindAndOutcomeActionAreDistinct(t *testing.T) {
	if decisionDeny == actionDeny {
		t.Fatal("decision kind and outcome action must remain distinct enums")
	}
	if outcomeAction(decisionDeny) != actionDeny || outcomeAction(decisionRedirect) != actionRedirect || outcomeAction(decisionConnectionAbort) != actionAbortConnection {
		t.Fatal("decision-to-outcome mapping is incorrect")
	}
	if !disruptive(decisionDrop) || disruptive(decisionLogOnly) {
		t.Fatal("canonical decision disruption mapping is incorrect")
	}
}

func TestImmediateResultRedirectUsesRawLocationOverwrite(t *testing.T) {
	const location = "https://redirect.example.test/next"
	response := immediateResult(result{decision: decisionRedirect, status: 307, redirect: location})
	headers := response.GetImmediateResponse().GetHeaders().GetSetHeaders()
	if len(headers) != 1 || headers[0].GetHeader().GetKey() != "location" || string(headers[0].GetHeader().GetRawValue()) != location || headers[0].GetHeader().GetValue() != "" || headers[0].GetAppendAction() != corev3.HeaderValueOption_OVERWRITE_IF_EXISTS_OR_ADD {
		t.Fatalf("redirect headers=%v, want one raw overwrite Location", headers)
	}
}

func TestPrecommitHostActionNeverTurnsStatuslessAbortIntoHTTP200(t *testing.T) {
	for name, r := range map[string]result{
		"drop":  {decision: decisionDrop},
		"abort": {decision: decisionConnectionAbort},
	} {
		action, status, response := precommitHostAction(r)
		if action != actionDeny || status != failClosedStatus ||
			int(response.GetImmediateResponse().GetStatus().GetCode()) != failClosedStatus {
			t.Fatalf("%s precommit translation = action=%d status=%d response=%#v, want fail-closed 503 deny", name, action, status, response)
		}
	}
	/* The ordinary HTTP decision remains an ordinary HTTP decision; the
	 * fallback is limited to statusless actions that ext_proc cannot prove it
	 * reset or aborted. */
	action, status, response := precommitHostAction(result{decision: decisionDeny, status: 403})
	if action != actionDeny || status != 403 ||
		int(response.GetImmediateResponse().GetStatus().GetCode()) != 403 {
		t.Fatalf("deny precommit translation changed: action=%d status=%d response=%#v", action, status, response)
	}
}

func TestPrecommitRecordsFailClosedFallbackOutcome(t *testing.T) {
	dir := testSocketDir(t)
	path := filepath.Join(dir, "observer.sock")
	listener, err := net.Listen("unix", path)
	if err != nil {
		t.Fatal(err)
	}
	defer listener.Close()
	type frame struct {
		op      byte
		payload []byte
	}
	seen := make(chan frame, 2)
	go func() {
		conn, err := listener.Accept()
		if err != nil {
			return
		}
		defer conn.Close()
		for range 2 {
			var header [frameSize]byte
			if _, err := io.ReadFull(conn, header[:]); err != nil {
				return
			}
			payload := make([]byte, binary.BigEndian.Uint32(header[8:]))
			if _, err := io.ReadFull(conn, payload); err != nil {
				return
			}
			seen <- frame{op: header[5], payload: payload}
			resultPayload := make([]byte, 12)
			resultPayload[0], resultPayload[1], resultPayload[2] = header[5], resultOK, decisionAllow
			var out [frameSize]byte
			copy(out[:4], []byte("MRC1"))
			out[4], out[5] = protocolVersion, resultOpcode
			binary.BigEndian.PutUint32(out[8:], uint32(len(resultPayload)))
			if _, err := conn.Write(out[:]); err != nil {
				return
			}
			if _, err := conn.Write(resultPayload); err != nil {
				return
			}
		}
	}()
	c, err := dial(path, time.Second)
	if err != nil {
		t.Fatal(err)
	}
	service, err := New(Config{SocketPath: path})
	if err != nil {
		t.Fatal(err)
	}
	response, err := service.precommit(&stream{c: c}, result{decision: decisionDrop})
	if err != nil {
		t.Fatal(err)
	}
	if int(response.GetImmediateResponse().GetStatus().GetCode()) != failClosedStatus {
		t.Fatalf("drop response status = %d, want %d", response.GetImmediateResponse().GetStatus().GetCode(), failClosedStatus)
	}
	outcome := <-seen
	if outcome.op != opOutcome || len(outcome.payload) != 4 || outcome.payload[0] != actionDeny || outcome.payload[1] != 0 || binary.BigEndian.Uint16(outcome.payload[2:]) != failClosedStatus {
		t.Fatalf("drop fallback outcome = %#v, want deny/http-503 without abort claim", outcome)
	}
	cancel := <-seen
	if cancel.op != opCancel || !reflect.DeepEqual(cancel.payload, []byte{0}) {
		t.Fatalf("precommit cleanup = %#v, want non-disconnect cancel", cancel)
	}
}

func TestTerminalAuthzResponseRequiresAttestationAndStripsIt(t *testing.T) {
	service, err := New(Config{SocketPath: "/unused"})
	if err != nil {
		t.Fatal(err)
	}
	markerHeaders := &corev3.HeaderMap{Headers: []*corev3.HeaderValue{{
		Key: terminalAuthzMarkerHeader, Value: terminalAuthzMarkerValue,
	}}}
	state := &stream{}
	response, done, err := service.responseHeaders(state, &extprocv3.HttpHeaders{Headers: markerHeaders})
	if err != nil || done || !state.terminalAuthorizationResponse || !state.responseHeaders {
		t.Fatalf("attested terminal response = response=%#v done=%t state=%#v err=%v", response, done, state, err)
	}
	mutation := response.GetResponseHeaders().GetResponse().GetHeaderMutation()
	if mutation == nil || !reflect.DeepEqual(mutation.GetRemoveHeaders(), []string{terminalAuthzMarkerHeader}) {
		t.Fatalf("terminal marker was not stripped: %#v", mutation)
	}
	response, done, err = service.responseBody(state, &extprocv3.HttpBody{Body: []byte("blocked"), EndOfStream: true})
	if err != nil || !done || !state.responseDone || response.GetResponseBody() == nil {
		t.Fatalf("attested terminal response body = response=%#v done=%t state=%#v err=%v", response, done, state, err)
	}

	/* A response without both the profile-owned marker and the absence of a
	 * request observation stays fail-closed.  A normal request missing a
	 * handle cannot borrow the terminal path by adding the marker. */
	if _, _, err := service.responseHeaders(&stream{}, &extprocv3.HttpHeaders{Headers: &corev3.HeaderMap{}}); err == nil {
		t.Fatal("unattested response without a request phase was accepted")
	}
	if _, _, err := service.responseHeaders(&stream{requestHeadersSeen: true}, &extprocv3.HttpHeaders{Headers: markerHeaders}); err == nil {
		t.Fatal("attested response after a request phase was accepted without a session")
	}
}

func TestTerminalAuthzResponseHonorsHeaderLimits(t *testing.T) {
	service, err := New(Config{
		SocketPath:     "/unused",
		MaxHeaderCount: 1,
	})
	if err != nil {
		t.Fatal(err)
	}
	markerAndExtra := &corev3.HeaderMap{Headers: []*corev3.HeaderValue{
		{Key: terminalAuthzMarkerHeader, Value: terminalAuthzMarkerValue},
		{Key: "x-terminal-extra", Value: "value"},
	}}
	if _, _, err := service.responseHeaders(&stream{}, &extprocv3.HttpHeaders{Headers: markerAndExtra}); err == nil {
		t.Fatal("terminal authorization response accepted headers above configured limit")
	}
}

func TestTerminalAuthzResponseHonorsAggregateBodyLimit(t *testing.T) {
	service, err := New(Config{
		SocketPath:           "/unused",
		MaxResponseBodyBytes: 4,
	})
	if err != nil {
		t.Fatal(err)
	}
	markerHeaders := &corev3.HeaderMap{Headers: []*corev3.HeaderValue{{
		Key: terminalAuthzMarkerHeader, Value: terminalAuthzMarkerValue,
	}}}
	state := &stream{}
	if _, _, err := service.responseHeaders(state, &extprocv3.HttpHeaders{Headers: markerHeaders}); err != nil {
		t.Fatal(err)
	}
	response, done, err := service.responseBody(state, &extprocv3.HttpBody{Body: []byte("1234")})
	if err != nil || done || response.GetResponseBody() == nil || state.responseBytes != 4 {
		t.Fatalf("bounded terminal body = response=%#v done=%t bytes=%d err=%v", response, done, state.responseBytes, err)
	}
	if _, _, err := service.responseBody(state, &extprocv3.HttpBody{Body: []byte("5"), EndOfStream: true}); err == nil {
		t.Fatal("terminal authorization response accepted aggregate body above configured limit")
	}
	if state.responseBytes != 4 {
		t.Fatalf("terminal overflow changed accepted body count: %d", state.responseBytes)
	}
}

func TestLateOutcomeUsesVisibleResponseStatus(t *testing.T) {
	state := &stream{responseStatus: 204}
	if got := state.visibleResponseStatus(); got != 204 {
		t.Fatalf("visible status = %d, want 204", got)
	}
	state.responseStatus = 99
	if got := state.visibleResponseStatus(); got != 200 {
		t.Fatalf("invalid visible status = %d, want 200", got)
	}
}

func TestClientRejectsOversizedBody(t *testing.T) {
	c := &client{timeout: time.Second}
	if _, err := c.body(make([]byte, maxBody+1)); err == nil {
		t.Fatal("expected body limit error")
	}
}

func TestServiceSplitsStreamedResponseBodyBeforeMRC1Limit(t *testing.T) {
	left, right := net.Pipe()
	defer left.Close()
	frames := make(chan struct {
		op      byte
		payload []byte
	}, 4)
	serverDone := make(chan struct{})
	go func() {
		defer close(serverDone)
		defer right.Close()
		for {
			var header [frameSize]byte
			if _, err := io.ReadFull(right, header[:]); err != nil {
				return
			}
			payload := make([]byte, binary.BigEndian.Uint32(header[8:]))
			if _, err := io.ReadFull(right, payload); err != nil {
				return
			}
			frames <- struct {
				op      byte
				payload []byte
			}{op: header[5], payload: payload}
			resultPayload := make([]byte, 12)
			resultPayload[0], resultPayload[1], resultPayload[2] = header[5], resultOK, decisionAllow
			var resultHeader [frameSize]byte
			copy(resultHeader[:4], []byte("MRC1"))
			resultHeader[4], resultHeader[5] = protocolVersion, resultOpcode
			binary.BigEndian.PutUint32(resultHeader[8:], uint32(len(resultPayload)))
			if _, err := right.Write(resultHeader[:]); err != nil {
				return
			}
			if _, err := right.Write(resultPayload); err != nil || header[5] == opRelease {
				return
			}
		}
	}()

	service := &Service{config: Config{MaxResponseBodyBytes: int64(maxBody + 7)}}
	state := &stream{
		c:               &client{conn: left, timeout: time.Second},
		committed:       true,
		responseHeaders: true,
		responseStatus:  http.StatusOK,
	}
	response, done, err := service.responseBody(state, &extprocv3.HttpBody{
		Body:        make([]byte, maxBody+7),
		EndOfStream: true,
	})
	if err != nil || !done || !state.responseDone || !state.released || response.GetResponseBody() == nil {
		t.Fatalf("split streamed body = response=%#v done=%t state=%#v err=%v", response, done, state, err)
	}
	if state.responseBytes != int64(maxBody+7) {
		t.Fatalf("response bytes = %d, want %d", state.responseBytes, maxBody+7)
	}
	<-serverDone
	close(frames)
	var operations []byte
	var bodyLengths []int
	for frame := range frames {
		operations = append(operations, frame.op)
		if frame.op == opResponseBody {
			bodyLengths = append(bodyLengths, len(frame.payload))
		}
	}
	if want := []byte{opResponseBody, opResponseBody, opResponseEOS, opRelease}; !reflect.DeepEqual(operations, want) {
		t.Fatalf("operations = %v, want %v", operations, want)
	}
	if want := []int{maxBody, 7}; !reflect.DeepEqual(bodyLengths, want) {
		t.Fatalf("body lengths = %v, want %v", bodyLengths, want)
	}
}

func TestServiceRejectsOversizedStreamedCallbackBeforeForwardingAPrefix(t *testing.T) {
	left, right := net.Pipe()
	defer left.Close()
	defer right.Close()
	service := &Service{config: Config{MaxResponseBodyBytes: int64(maxBody)}}
	state := &stream{c: &client{conn: left, timeout: time.Second}, responseHeaders: true}
	if _, _, err := service.responseBody(state, &extprocv3.HttpBody{Body: make([]byte, maxBody+1)}); err == nil {
		t.Fatal("oversized logical response body was accepted")
	}
	if state.responseBytes != 0 {
		t.Fatalf("response bytes = %d, want no forwarded prefix", state.responseBytes)
	}
	if err := right.SetReadDeadline(time.Now().Add(100 * time.Millisecond)); err != nil {
		t.Fatal(err)
	}
	var header [frameSize]byte
	if _, err := io.ReadFull(right, header[:]); err == nil {
		t.Fatalf("forwarded an MRC1 frame before rejecting oversized body: %v", header)
	}
}

func TestReplayResultIsNotAccepted(t *testing.T) {
	dir := testSocketDir(t)
	path := filepath.Join(dir, "observer.sock")
	listener, err := net.Listen("unix", path)
	if err != nil {
		t.Fatal(err)
	}
	defer listener.Close()
	go func() {
		conn, _ := listener.Accept()
		if conn == nil {
			return
		}
		defer conn.Close()
		var h [frameSize]byte
		_, _ = io.ReadFull(conn, h[:])
		payload := make([]byte, binary.BigEndian.Uint32(h[8:]))
		_, _ = io.ReadFull(conn, payload)
		out := make([]byte, 12)
		out[0], out[1], out[2] = opClaim, 1, decisionError
		binary.BigEndian.PutUint16(out[4:], 503)
		binary.BigEndian.PutUint16(out[6:], 1)
		var oh [frameSize]byte
		copy(oh[:4], []byte("MRC1"))
		oh[4], oh[5] = protocolVersion, resultOpcode
		binary.BigEndian.PutUint32(oh[8:], uint32(len(out)))
		_, _ = conn.Write(oh[:])
		_, _ = conn.Write(out)
	}()
	c, err := dial(path, time.Second)
	if err != nil {
		t.Fatal(err)
	}
	defer c.close()
	if r, err := c.claim("0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef"); err != nil || r.code == 0 {
		t.Fatalf("replayed handle was accepted: result=%+v err=%v", r, err)
	}
}

func TestParseResultRejectsInvalidCanonicalCombinations(t *testing.T) {
	valid := func(code, decision byte, status, errorCode int, redirect, rule string) []byte {
		payload := make([]byte, 12+len(redirect)+len(rule))
		payload[0], payload[1], payload[2] = opClaim, code, decision
		binary.BigEndian.PutUint16(payload[4:], uint16(status))
		binary.BigEndian.PutUint16(payload[6:], uint16(errorCode))
		binary.BigEndian.PutUint16(payload[8:], uint16(len(redirect)))
		binary.BigEndian.PutUint16(payload[10:], uint16(len(rule)))
		copy(payload[12:], redirect)
		copy(payload[12+len(redirect):], rule)
		return payload
	}
	for name, payload := range map[string][]byte{
		"unknown code":            valid(2, decisionAllow, 200, 1, "", ""),
		"unknown decision":        valid(resultOK, 8, 200, 0, "", ""),
		"success error":           valid(resultOK, decisionAllow, 200, 1, "", ""),
		"failure no error":        valid(1, decisionError, 503, 0, "", ""),
		"success bad status":      valid(resultOK, decisionAllow, 99, 0, "", ""),
		"success non-http status": valid(resultOK, decisionAllow, 600, 0, "", ""),
		"redirect missing URL":    valid(resultOK, decisionRedirect, 302, 0, "", ""),
		"redirect bad status":     valid(resultOK, decisionRedirect, 200, 0, "/next", ""),
		"non redirect URL":        valid(resultOK, decisionAllow, 200, 0, "/next", ""),
		"oversized rule":          valid(resultOK, decisionAllow, 200, 0, "", strings.Repeat("r", maxResultText+1)),
		"statusless deny":         valid(resultOK, decisionDeny, 0, 0, "", ""),
		"statusless error":        valid(resultOK, decisionError, 0, 0, "", ""),
		"statusless unsupported":  valid(resultOK, decisionUnsupported, 0, 0, "", ""),
	} {
		if _, err := parseResult(opClaim, payload); err == nil {
			t.Fatalf("%s was accepted", name)
		}
	}
}

func TestParseResultRejectsRedirectHeaderControlCharacters(t *testing.T) {
	valid := func(redirect, rule string) []byte {
		payload := make([]byte, 12+len(redirect)+len(rule))
		payload[0], payload[1], payload[2] = opResponseHeaders, resultOK, decisionRedirect
		binary.BigEndian.PutUint16(payload[4:], 302)
		binary.BigEndian.PutUint16(payload[8:], uint16(len(redirect)))
		binary.BigEndian.PutUint16(payload[10:], uint16(len(rule)))
		copy(payload[12:], redirect)
		copy(payload[12+len(redirect):], rule)
		return payload
	}
	for _, control := range []string{"\r", "\n", "\x00", "\x1f", "\x7f"} {
		redirect := "https://safe.example/" + control + "next"
		if _, err := parseResult(opResponseHeaders, valid(redirect, "rule-id")); err == nil {
			t.Fatalf("redirect with header control was accepted: %q", redirect)
		}
		if _, err := parseResult(opResponseHeaders,
			valid("https://safe.example/next", "rule"+control+"id")); err == nil {
			t.Fatalf("result metadata with control was accepted: %q", control)
		}
	}
	const safeRedirect = "https://safe.example/next"
	if got, err := parseResult(opResponseHeaders, valid(safeRedirect, "rule-id")); err != nil ||
		got.redirect != safeRedirect {
		t.Fatalf("safe redirect = %+v, %v", got, err)
	}
}

func TestParseResultAcceptsCanonicalStatuslessSuccess(t *testing.T) {
	valid := func(decision byte) []byte {
		payload := make([]byte, 12)
		payload[0], payload[1], payload[2] = opClaim, resultOK, decision
		return payload
	}
	for _, decision := range []byte{
		decisionAllow,
		decisionLogOnly,
		decisionDrop,
		decisionConnectionAbort,
	} {
		if got, err := parseResult(opClaim, valid(decision)); err != nil || got.status != 0 {
			t.Fatalf("statusless decision %d was rejected: result=%+v err=%v", decision, got, err)
		}
	}
}

func TestParseResultAcceptsStatuslessReleaseAcknowledgement(t *testing.T) {
	payload := make([]byte, 12)
	payload[0], payload[1], payload[2] = opRelease, resultOK, decisionError
	if got, err := parseResult(opRelease, payload); err != nil || got.status != 0 {
		t.Fatalf("statusless release acknowledgement was rejected: result=%+v err=%v", got, err)
	}
	if _, err := parseResult(opClaim, payload); err == nil {
		t.Fatal("accepted statusless error decision for claim")
	}
}

func TestRequestHandleMutationStripsOpaqueHeader(t *testing.T) {
	service, err := New(Config{SocketPath: "/unused"})
	if err != nil {
		t.Fatal(err)
	}
	response := continueHeaders(service.config.HandleHeader)
	mutation := response.GetRequestHeaders().GetResponse().GetHeaderMutation()
	if mutation == nil || len(mutation.GetRemoveHeaders()) != 1 || mutation.GetRemoveHeaders()[0] != DefaultHandleHeader {
		t.Fatalf("handle mutation = %#v", mutation)
	}
}

func TestResponseHandleOnlyCollapsesByteIdenticalDuplicates(t *testing.T) {
	handle := "0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef"
	mapFor := func(values ...string) *corev3.HeaderMap {
		headers := make([]*corev3.HeaderValue, 0, len(values))
		for _, value := range values {
			headers = append(headers, &corev3.HeaderValue{
				Key: DefaultHandleHeader, Value: value,
			})
		}
		return &corev3.HeaderMap{Headers: headers}
	}
	got, err := responseHandle(mapFor(handle, handle), DefaultHandleHeader)
	if err != nil || got != handle {
		t.Fatalf("identical duplicates were not collapsed safely: handle=%q err=%v", got, err)
	}
	rawMap := &corev3.HeaderMap{Headers: []*corev3.HeaderValue{{
		Key: DefaultHandleHeader, RawValue: []byte(handle),
	}}}
	if got, err := responseHandle(rawMap, DefaultHandleHeader); err != nil || got != handle {
		t.Fatalf("raw opaque handle was not accepted: handle=%q err=%v", got, err)
	}
	if _, err := headerValueText(&corev3.HeaderValue{
		Value: handle, RawValue: []byte(handle),
	}); err == nil {
		t.Fatal("ambiguous value/raw_value handle encoding was accepted")
	}
	if _, err := responseHandle(mapFor(handle,
		"fedcba9876543210fedcba9876543210fedcba9876543210fedcba9876543210"),
		DefaultHandleHeader); err == nil {
		t.Fatal("mismatched duplicate handles were accepted")
	}
	if _, err := responseHandle(mapFor(""), DefaultHandleHeader); err == nil {
		t.Fatal("empty handle was accepted")
	}
}

func TestHeaderValueTextAcceptsRawValueForResponseHeaders(t *testing.T) {
	value := &corev3.HeaderValue{Key: ":status", RawValue: []byte("204")}
	text, err := headerValueText(value)
	if err != nil || text != "204" {
		t.Fatalf("raw response header value = %q, err=%v", text, err)
	}
	if _, err := headerValueText(&corev3.HeaderValue{
		Key:      ":status",
		Value:    "204",
		RawValue: []byte("204"),
	}); err == nil {
		t.Fatal("accepted ambiguous text and raw response header values")
	}
}

func TestClaimFailureClassifiesOnlySharedContractErrors(t *testing.T) {
	for code, want := range map[int]string{
		4:  "unavailable",
		13: "timed out",
		15: "protocol error",
		16: "phase sequence error",
		17: "correlation failure",
		18: "correlation failure",
		19: "correlation failure",
		99: "rejected handle",
	} {
		if got := claimFailure(code).Error(); !strings.Contains(got, want) {
			t.Fatalf("claimFailure(%d) = %q, want %q", code, got, want)
		}
	}
}

func TestClaimTransportFailureDoesNotExposeTransportDetails(t *testing.T) {
	for input, want := range map[error]string{
		os.ErrDeadlineExceeded: "timed out",
		io.EOF:                 "closed",
		fmt.Errorf("private socket path must stay private"): "transport failure",
	} {
		if got := claimTransportFailure(input).Error(); !strings.Contains(got, want) {
			t.Fatalf("claimTransportFailure(%v) = %q, want %q", input, got, want)
		}
		if strings.Contains(claimTransportFailure(input).Error(), "private socket") {
			t.Fatal("transport classification exposed an underlying error detail")
		}
	}
}
