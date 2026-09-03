package responseobserver

import (
	"context"
	"errors"
	"fmt"
	"io"
	"net"
	"os"
	"strings"
	"time"

	corev3 "github.com/envoyproxy/go-control-plane/envoy/config/core/v3"
	extprocv3 "github.com/envoyproxy/go-control-plane/envoy/service/ext_proc/v3"
	typev3 "github.com/envoyproxy/go-control-plane/envoy/type/v3"
)

const (
	DefaultHandleHeader       = "x-msconnector-response-handle"
	terminalAuthzMarkerHeader = "x-msconnector-terminal-authz"
	terminalAuthzMarkerValue  = "1"
	failClosedStatus          = 503
)

type Config struct {
	SocketPath           string
	HandleHeader         string
	Timeout              time.Duration
	MaxHeaderCount       int
	MaxHeaderBytes       int
	MaxResponseBodyBytes int64
}

type Service struct {
	extprocv3.UnimplementedExternalProcessorServer
	config Config
}

type stream struct {
	c                             *client
	committed, requestHeadersSeen bool
	responseHeaders, responseDone bool
	responseBytes                 int64
	responseStatus                int
	terminal, released            bool
	terminalAuthorizationResponse bool
	pendingAction                 byte
	pendingStatus                 int
	pendingOutcome                bool
}

func New(config Config) (*Service, error) {
	if strings.TrimSpace(config.SocketPath) == "" {
		return nil, fmt.Errorf("response observer: socket_path is required")
	}
	if config.HandleHeader == "" {
		config.HandleHeader = DefaultHandleHeader
	}
	if config.Timeout <= 0 {
		config.Timeout = timeoutOrDefault(config.Timeout)
	}
	if config.MaxHeaderCount <= 0 {
		config.MaxHeaderCount = 128
	}
	if config.MaxHeaderBytes <= 0 {
		config.MaxHeaderBytes = 32768
	}
	if config.MaxResponseBodyBytes <= 0 {
		config.MaxResponseBodyBytes = 1 << 20
	}
	return &Service{config: config}, nil
}

func (s *Service) Process(server extprocv3.ExternalProcessor_ProcessServer) error {
	state := &stream{}
	defer func() {
		if state.c != nil && !state.terminal && !state.released {
			_, _ = state.c.cancel(terminationClientCancel)
			_, _ = state.c.release()
			_ = state.c.close()
		}
	}()
	for {
		req, err := server.Recv()
		if err != nil {
			return err
		}
		if done, err := s.processRequest(server, state, req); err != nil {
			return err
		} else if done {
			return nil
		}
	}
}

func (s *Service) processRequest(server extprocv3.ExternalProcessor_ProcessServer, state *stream, req *extprocv3.ProcessingRequest) (bool, error) {
	response, done, err := s.handle(server.Context(), state, req)
	if err != nil {
		// This reports only a fixed protocol/error classification.  The
		// opaque MRC1 handle and all HTTP payloads remain out of logs.
		fmt.Fprintf(os.Stderr, "response observer stream error: %v\n", err)
		if !state.committed {
			return true, server.Send(immediate(503))
		}
		return false, err
	}
	if err := server.Send(response); err != nil {
		if state.pendingOutcome {
			state.failClosed(causeForTransport(err))
		}
		return false, err
	}
	if done && state.pendingOutcome {
		if err := s.finalizePrecommit(state); err != nil {
			return false, err
		}
	}
	return done, nil
}

func (s *Service) handle(ctx context.Context, state *stream, req *extprocv3.ProcessingRequest) (*extprocv3.ProcessingResponse, bool, error) {
	if req == nil {
		return nil, false, fmt.Errorf("response observer: nil processing request")
	}
	switch {
	case req.GetRequestHeaders() != nil:
		return s.requestHeaders(state, req.GetRequestHeaders())
	case req.GetResponseHeaders() != nil:
		return s.responseHeaders(state, req.GetResponseHeaders())
	case req.GetResponseBody() != nil:
		return s.responseBody(state, req.GetResponseBody())
	case req.GetResponseTrailers() != nil:
		return s.responseEOS(state)
	default:
		return nil, false, fmt.Errorf("response observer: unsupported phase")
	}
}

func (s *Service) requestHeaders(state *stream, message *extprocv3.HttpHeaders) (*extprocv3.ProcessingResponse, bool, error) {
	if state.requestHeadersSeen || state.c != nil {
		return nil, false, fmt.Errorf("response observer: duplicate request headers")
	}
	/* Record the observed phase before decoding the handle.  A following
	 * response without a claimed session is then a real protocol failure, not
	 * eligible for the narrowly attested terminal-authz response path. */
	state.requestHeadersSeen = true
	handle, err := responseHandle(message.GetHeaders(), s.config.HandleHeader)
	if err != nil {
		return nil, false, err
	}
	c, err := dial(s.config.SocketPath, s.config.Timeout)
	if err != nil {
		return nil, false, err
	}
	state.c = c
	r, err := c.claim(handle)
	if err != nil {
		return nil, false, claimTransportFailure(err)
	}
	if r.code != resultOK {
		return nil, false, claimFailure(r.errorCode)
	}
	return continueHeaders(s.config.HandleHeader), false, nil
}

func claimTransportFailure(err error) error {
	var networkErr net.Error
	switch {
	case errors.Is(err, os.ErrDeadlineExceeded), errors.As(err, &networkErr) && networkErr.Timeout():
		return fmt.Errorf("response observer: response companion transport timed out")
	case errors.Is(err, io.EOF), errors.Is(err, io.ErrUnexpectedEOF), errors.Is(err, net.ErrClosed):
		return fmt.Errorf("response observer: response companion transport closed")
	default:
		return fmt.Errorf("response observer: response companion transport failure")
	}
}

func claimFailure(errorCode int) error {
	switch errorCode {
	case 4: // MSCONNECTOR_ERROR_RUNTIME_UNAVAILABLE
		return fmt.Errorf("response observer: response companion is unavailable")
	case 13: // MSCONNECTOR_ERROR_TIMEOUT
		return fmt.Errorf("response observer: response companion timed out")
	case 15: // MSCONNECTOR_ERROR_PROTOCOL
		return fmt.Errorf("response observer: response companion protocol error")
	case 16: // MSCONNECTOR_ERROR_PHASE_SEQUENCE
		return fmt.Errorf("response observer: response companion phase sequence error")
	case 17, 18, 19: // MSCONNECTOR_ERROR_CORRELATION_*
		return fmt.Errorf("response observer: response companion correlation failure")
	default:
		return fmt.Errorf("response observer: response companion rejected handle")
	}
}

func responseHandle(headers *corev3.HeaderMap, handleHeader string) (string, error) {
	var handle string
	for _, value := range headers.GetHeaders() {
		if strings.EqualFold(value.GetKey(), handleHeader) {
			candidate, err := headerValueText(value)
			if err != nil {
				return "", err
			}
			if !validHandle(candidate) {
				return "", fmt.Errorf("response observer: empty or malformed response handle")
			}
			if handle != "" && candidate != handle {
				return "", fmt.Errorf("response observer: mismatched duplicate response handles")
			}
			/* Envoy may expose the same allowed authorization-response header
			 * more than once at the ext_proc boundary.  It is safe to collapse
			 * only byte-identical, already-valid opaque handles: a distinct,
			 * empty, or malformed value remains a fail-closed protocol error.
			 * continueHeaders removes this internal header before upstream use. */
			handle = candidate
		}
	}
	if !validHandle(handle) {
		return "", fmt.Errorf("response observer: missing or malformed response handle")
	}
	return handle, nil
}

/* Envoy's HeaderValue may carry an ASCII HTTP field value as either `value`
 * or `raw_value`.  The protocol says the forms are exclusive; reject an
 * ambiguous value rather than preferring one silently.  The caller validates
 * the returned text as exactly one lowercase hexadecimal capability. */
func headerValueText(value *corev3.HeaderValue) (string, error) {
	if value == nil {
		return "", fmt.Errorf("response observer: missing response handle value")
	}
	text := value.GetValue()
	raw := value.GetRawValue()
	if text != "" && len(raw) != 0 {
		return "", fmt.Errorf("response observer: ambiguous response handle encoding")
	}
	if len(raw) != 0 {
		return string(raw), nil
	}
	return text, nil
}

/* terminalAuthzResponseMarker is an explicit deployment attestation, emitted
 * only by the local ext_authz service for a terminal P1/P2 reply.  It is not
 * inferred from a missing response handle: that would turn a skipped observer
 * request phase into an unsafe pass-through. */
func terminalAuthzResponseMarker(headers *corev3.HeaderMap) (bool, error) {
	found := false
	if headers == nil {
		return false, nil
	}
	for _, value := range headers.GetHeaders() {
		if !strings.EqualFold(value.GetKey(), terminalAuthzMarkerHeader) {
			continue
		}
		text, err := headerValueText(value)
		if err != nil {
			return false, fmt.Errorf("response observer: invalid terminal authorization marker")
		}
		if found || text != terminalAuthzMarkerValue {
			return false, fmt.Errorf("response observer: malformed terminal authorization marker")
		}
		found = true
	}
	return found, nil
}

func (s *Service) responseHeaders(state *stream, message *extprocv3.HttpHeaders) (*extprocv3.ProcessingResponse, bool, error) {
	if state.responseHeaders {
		return nil, false, fmt.Errorf("response observer: response headers out of order")
	}
	if state.c == nil {
		return s.terminalAuthorizationResponse(state, message)
	}
	return s.observedResponseHeaders(state, message)
}

func (s *Service) observedResponseHeaders(state *stream, message *extprocv3.HttpHeaders) (*extprocv3.ProcessingResponse, bool, error) {
	headers, err := decodeResponseHeaders(message.GetHeaders(), s.config)
	if err != nil {
		return nil, false, err
	}
	state.responseStatus = statusFromHeaders(headers)
	r, err := state.c.responseHeaders(state.responseStatus, headers)
	if err != nil {
		return nil, false, err
	}
	if r.code != 0 {
		r.decision, r.status = decisionError, 503
	}
	if disruptive(r.decision) {
		response, err := s.precommit(state, r)
		return response, true, err
	}
	r, err = state.c.commit(true, false)
	if err != nil {
		return nil, false, err
	}
	if r.code != 0 {
		r.decision, r.status = decisionError, 503
	}
	if disruptive(r.decision) {
		response, err := s.precommit(state, r)
		return response, true, err
	}
	state.committed, state.responseHeaders = true, true
	if !message.GetEndOfStream() {
		return continueResponse(false), false, nil
	}
	return s.finishHeaderOnlyResponse(state)
}

func (s *Service) finishHeaderOnlyResponse(state *stream) (*extprocv3.ProcessingResponse, bool, error) {
	return s.finalizeResponseEOS(state, continueResponse)
}

// finalizeResponseEOS applies the common response EOS transaction semantics
// for header-only and body-streamed responses. The continuation is the only
// host-specific part; the EOS result, late fail-closed outcome, and cleanup
// ordering remain identical for both response shapes.
func (s *Service) finalizeResponseEOS(state *stream, continuation func(bool) *extprocv3.ProcessingResponse) (*extprocv3.ProcessingResponse, bool, error) {
	eos, err := state.c.eos()
	if err != nil {
		return nil, false, err
	}
	if eos.code != 0 {
		state.failClosed(causeForErrorCode(eos.errorCode))
		return nil, false, fmt.Errorf("response observer: EOS failed (%d)", eos.errorCode)
	}
	if disruptive(eos.decision) {
		if err := state.sendLateOutcome(); err != nil {
			return nil, false, err
		}
	}
	state.responseDone = true
	if err := state.releaseAndClose(); err != nil {
		return nil, false, err
	}
	return continuation(true), true, nil
}

func (s *Service) terminalAuthorizationResponse(state *stream,
	message *extprocv3.HttpHeaders) (*extprocv3.ProcessingResponse, bool, error) {
	/* A terminal ext_authz reply does not claim a companion transaction, but it
	 * still crosses this ext_proc boundary. Apply the same bounded header
	 * decoding as an observed upstream response before accepting its marker. */
	if _, err := decodeResponseHeaders(message.GetHeaders(), s.config); err != nil {
		return nil, false, err
	}
	marked, err := terminalAuthzResponseMarker(message.GetHeaders())
	if err != nil {
		return nil, false, err
	}
	if state.requestHeadersSeen || !marked {
		return nil, false, fmt.Errorf("response observer: response headers out of order")
	}
	/* An ext_authz terminal reply does not enter the upstream path, hence
	 * Envoy emits response callbacks without a preceding ext_proc request
	 * callback.  The profile-owned marker is stripped before the client and
	 * is the only condition that permits this response-only continuation. */
	state.terminalAuthorizationResponse = true
	state.responseHeaders = true
	state.responseDone = message.GetEndOfStream()
	return continueResponse(message.GetEndOfStream()), state.responseDone, nil
}

func decodeResponseHeaders(headers *corev3.HeaderMap, config Config) ([]header, error) {
	values := headers.GetHeaders()
	if len(values) > config.MaxHeaderCount {
		return nil, fmt.Errorf("response observer: response header count exceeds limit")
	}
	decoded := make([]header, 0, len(values))
	total := 0
	for _, value := range values {
		text, err := headerValueText(value)
		if err != nil {
			return nil, fmt.Errorf("response observer: invalid response header value")
		}
		total += len(value.GetKey()) + len(text)
		if total > config.MaxHeaderBytes {
			return nil, fmt.Errorf("response observer: response headers exceed limit")
		}
		if !strings.EqualFold(value.GetKey(), terminalAuthzMarkerHeader) {
			decoded = append(decoded, header{name: value.GetKey(), value: text})
		}
	}
	return decoded, nil
}

func (s *Service) responseBody(state *stream, message *extprocv3.HttpBody) (*extprocv3.ProcessingResponse, bool, error) {
	if state.terminalAuthorizationResponse {
		return s.terminalResponseBody(state, message)
	}
	if state.c == nil || !state.responseHeaders || state.responseDone {
		return nil, false, fmt.Errorf("response observer: response body out of order")
	}
	if err := s.observeResponseBody(state, message.GetBody()); err != nil {
		return nil, false, err
	}
	if message.GetEndOfStream() {
		return s.finishResponseBody(state)
	}
	return continueBody(false), false, nil
}

func (s *Service) terminalResponseBody(state *stream, message *extprocv3.HttpBody) (*extprocv3.ProcessingResponse, bool, error) {
	if !state.responseHeaders || state.responseDone {
		return nil, false, fmt.Errorf("response observer: terminal authorization response body out of order")
	}
	bodyBytes := int64(len(message.GetBody()))
	if bodyBytes > s.config.MaxResponseBodyBytes-state.responseBytes {
		return nil, false, fmt.Errorf("response observer: terminal authorization response body limit exceeded")
	}
	state.responseBytes += bodyBytes
	state.responseDone = message.GetEndOfStream()
	return continueBody(message.GetEndOfStream()), state.responseDone, nil
}

func (s *Service) observeResponseBody(state *stream, body []byte) error {
	/* Envoy may legitimately deliver a STREAMED callback larger than one
	 * MRC1 frame.  Validate its complete logical contribution before forwarding
	 * any prefix, then preserve the MRC1 per-frame bound below. */
	if int64(len(body)) > s.config.MaxResponseBodyBytes-state.responseBytes {
		return fmt.Errorf("response observer: response body limit exceeded")
	}
	for len(body) > 0 {
		chunk := body
		if len(chunk) > maxBody {
			chunk = chunk[:maxBody]
		}
		if err := s.observeResponseChunk(state, chunk); err != nil {
			return err
		}
		body = body[len(chunk):]
	}
	return nil
}

func (s *Service) observeResponseChunk(state *stream, chunk []byte) error {
	r, err := state.c.body(chunk)
	if err != nil {
		return err
	}
	if r.code != 0 {
		state.failClosed(causeForErrorCode(r.errorCode))
		return fmt.Errorf("response observer: body failed (%d)", r.errorCode)
	}
	if state.committed && disruptive(r.decision) {
		if err := state.sendLateOutcome(); err != nil {
			return err
		}
	}
	state.responseBytes += int64(len(chunk))
	return nil
}

func (s *Service) finishResponseBody(state *stream) (*extprocv3.ProcessingResponse, bool, error) {
	return s.finalizeResponseEOS(state, continueBody)
}

func (s *Service) responseEOS(state *stream) (*extprocv3.ProcessingResponse, bool, error) {
	if state.terminalAuthorizationResponse {
		if !state.responseHeaders || state.responseDone {
			return nil, false, fmt.Errorf("response observer: terminal authorization response trailers out of order")
		}
		state.responseDone = true
		return continueTrailers(), true, nil
	}
	if state.c == nil || !state.responseHeaders || state.responseDone {
		return nil, false, fmt.Errorf("response observer: response trailers out of order")
	}
	r, err := state.c.eos()
	if err != nil {
		return nil, false, err
	}
	if r.code != 0 {
		state.failClosed(causeForErrorCode(r.errorCode))
		return nil, false, fmt.Errorf("response observer: trailer EOS failed (%d)", r.errorCode)
	}
	state.responseDone = true
	if state.committed && disruptive(r.decision) {
		if err := state.sendLateOutcome(); err != nil {
			return nil, false, err
		}
	}
	if err := state.releaseAndClose(); err != nil {
		return nil, false, err
	}
	return continueTrailers(), true, nil
}

/* precommitHostAction preserves the canonical requested decision while
 * recording the actual Envoy action.  The ext_proc response API exposes no
 * demonstrated connection-reset primitive here, so statusless DROP and
 * CONNECTION_ABORT cannot be claimed as a socket abort.  Before commitment
 * they are translated to an explicit fail-closed HTTP denial (503), never an
 * accidental status-200 response. */
func precommitHostAction(r result) (byte, int, *extprocv3.ProcessingResponse) {
	if r.decision == decisionDrop || r.decision == decisionConnectionAbort {
		return actionDeny, failClosedStatus, immediate(failClosedStatus)
	}
	return outcomeAction(r.decision), stateStatus(r), immediateResult(r)
}

func (s *Service) precommit(state *stream, r result) (*extprocv3.ProcessingResponse, error) {
	action, status, response := precommitHostAction(r)
	state.pendingAction, state.pendingStatus, state.pendingOutcome = action, status, true
	return response, nil
}

// finalizePrecommit records the host action only after Envoy accepted the
// ext_proc response.  A failed Send must never leave a claimed outcome.
func (s *Service) finalizePrecommit(state *stream) error {
	if state == nil || !state.pendingOutcome {
		return nil
	}
	outcome, err := state.c.outcome(state.pendingAction, state.pendingStatus)
	if err != nil || outcome.code != resultOK {
		state.failClosed(terminationConnectorError)
		if err != nil {
			return err
		}
		return fmt.Errorf("response observer: outcome failed (%d)", outcome.errorCode)
	}
	cancelled, err := state.c.cancel(terminationClientCancel)
	if err != nil || cancelled.code != resultOK {
		state.failClosed(causeForErrorCode(cancelled.errorCode))
		if err != nil {
			return err
		}
		return fmt.Errorf("response observer: pre-commit cancellation failed (%d)", cancelled.errorCode)
	}
	state.terminal = true
	if err := state.c.close(); err != nil {
		return err
	}
	state.pendingOutcome = false
	return nil
}

func (state *stream) failClosed(cause byte) {
	if state == nil || state.c == nil {
		return
	}
	if !state.terminal {
		_, _ = state.c.cancel(cause)
	}
	state.terminal = true
	_ = state.c.close()
}

func (state *stream) releaseAndClose() error {
	if state == nil || state.c == nil {
		return fmt.Errorf("response observer: missing companion session")
	}
	released, err := state.c.release()
	if err != nil {
		state.failClosed(causeForTransport(err))
		return err
	}
	if released.code != resultOK {
		state.failClosed(causeForErrorCode(released.errorCode))
		return fmt.Errorf("response observer: release failed (%d)", released.errorCode)
	}
	state.released, state.terminal = true, true
	return state.c.close()
}

func causeForTransport(err error) byte {
	if err == nil {
		return terminationConnectorError
	}
	var networkErr net.Error
	if errors.Is(err, os.ErrDeadlineExceeded) || (errors.As(err, &networkErr) && networkErr.Timeout()) {
		return terminationEngineTimeout
	}
	if strings.Contains(err.Error(), "invalid result") || strings.Contains(err.Error(), "malformed") {
		return terminationProtocolError
	}
	return terminationConnectorError
}

func causeForErrorCode(code int) byte {
	switch code {
	case 4: // MSCONNECTOR_ERROR_RUNTIME_UNAVAILABLE
		return terminationEngineUnavailable
	case 13: // MSCONNECTOR_ERROR_TIMEOUT
		return terminationEngineTimeout
	case 15, 16, 17, 18, 19: // protocol, phase, and correlation failures
		return terminationProtocolError
	default:
		return terminationInvalidEngineResponse
	}
}

func (state *stream) sendLateOutcome() error {
	outcome, err := state.c.outcome(actionLogOnly, state.visibleResponseStatus())
	if err != nil {
		return err
	}
	if outcome.code != 0 {
		return fmt.Errorf("response observer: outcome failed (%d)", outcome.errorCode)
	}
	return nil
}

func (state *stream) visibleResponseStatus() int {
	if state != nil && state.responseStatus >= 100 && state.responseStatus <= 599 {
		return state.responseStatus
	}
	return 200
}

func disruptive(decision byte) bool {
	return decision == decisionDeny || decision == decisionRedirect || decision == decisionDrop || decision == decisionConnectionAbort || decision == decisionError || decision == decisionUnsupported
}
func outcomeAction(decision byte) byte {
	switch decision {
	case decisionDeny:
		return actionDeny
	case decisionRedirect:
		return actionRedirect
	case decisionDrop:
		return actionDrop
	case decisionConnectionAbort:
		return actionAbortConnection
	case decisionError:
		return actionError
	case decisionUnsupported:
		return actionUnsupported
	default:
		return actionError
	}
}
func stateStatus(r result) int {
	if r.status >= 100 && r.status <= 599 {
		return r.status
	}
	return 200
}
func statusFromHeaders(headers []header) int {
	for _, h := range headers {
		if strings.EqualFold(h.name, ":status") {
			var status int
			_, _ = fmt.Sscanf(h.value, "%d", &status)
			return status
		}
	}
	return 200
}
func continueResponse(eos bool) *extprocv3.ProcessingResponse {
	return &extprocv3.ProcessingResponse{Response: &extprocv3.ProcessingResponse_ResponseHeaders{ResponseHeaders: &extprocv3.HeadersResponse{Response: &extprocv3.CommonResponse{Status: extprocv3.CommonResponse_CONTINUE, ClearRouteCache: false, HeaderMutation: &extprocv3.HeaderMutation{RemoveHeaders: []string{terminalAuthzMarkerHeader}}}}}}
}
func continueHeaders(handleHeader string) *extprocv3.ProcessingResponse {
	mutation := &extprocv3.HeaderMutation{}
	if handleHeader != "" {
		mutation.RemoveHeaders = []string{handleHeader}
	}
	return &extprocv3.ProcessingResponse{Response: &extprocv3.ProcessingResponse_RequestHeaders{RequestHeaders: &extprocv3.HeadersResponse{Response: &extprocv3.CommonResponse{Status: extprocv3.CommonResponse_CONTINUE, HeaderMutation: mutation}}}}
}
func continueBody(eos bool) *extprocv3.ProcessingResponse {
	return &extprocv3.ProcessingResponse{Response: &extprocv3.ProcessingResponse_ResponseBody{ResponseBody: &extprocv3.BodyResponse{Response: &extprocv3.CommonResponse{Status: extprocv3.CommonResponse_CONTINUE}}}}
}
func continueTrailers() *extprocv3.ProcessingResponse {
	return &extprocv3.ProcessingResponse{Response: &extprocv3.ProcessingResponse_ResponseTrailers{ResponseTrailers: &extprocv3.TrailersResponse{}}}
}
func immediate(status int) *extprocv3.ProcessingResponse {
	return &extprocv3.ProcessingResponse{Response: &extprocv3.ProcessingResponse_ImmediateResponse{ImmediateResponse: &extprocv3.ImmediateResponse{Status: &typev3.HttpStatus{Code: typev3.StatusCode(status)}}}}
}
func immediateResult(r result) *extprocv3.ProcessingResponse {
	response := immediate(stateStatus(r))
	if r.decision == decisionRedirect && r.redirect != "" {
		response.GetImmediateResponse().Headers = &extprocv3.HeaderMutation{SetHeaders: []*corev3.HeaderValueOption{{
			Header:       &corev3.HeaderValue{Key: "location", RawValue: []byte(r.redirect)},
			AppendAction: corev3.HeaderValueOption_OVERWRITE_IF_EXISTS_OR_ADD,
		}}}
	}
	return response
}
