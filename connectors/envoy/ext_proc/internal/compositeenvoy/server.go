// Package compositeenvoy contains the Envoy transport adapters for the
// retained composite transaction.  ext_authz performs P1/P2 admission and
// ext_proc performs only the later response phases.  The lease is carried in
// Envoy dynamic metadata; it is never copied into an HTTP header.
package compositeenvoy

import (
	"context"
	"crypto/rand"
	"encoding/base64"
	"errors"
	"io"
	"sort"
	"strconv"
	"strings"

	"github.com/Easton97-Jens/ModSecurity-conector/connectors/envoy/ext_proc/internal/composite"
	"github.com/Easton97-Jens/ModSecurity-conector/connectors/envoy/ext_proc/internal/processor"
	corev3 "github.com/envoyproxy/go-control-plane/envoy/config/core/v3"
	authv3 "github.com/envoyproxy/go-control-plane/envoy/service/auth/v3"
	extprocv3 "github.com/envoyproxy/go-control-plane/envoy/service/ext_proc/v3"
	typev3 "github.com/envoyproxy/go-control-plane/envoy/type/v3"
	"google.golang.org/grpc/codes"
	"google.golang.org/grpc/status"
	"google.golang.org/protobuf/types/known/structpb"
)

const (
	metadataNamespace         = "envoy.filters.http.ext_authz"
	compositeLeaseHeader      = "x-msconnector-composite-lease"
	metadataLease             = "lease"
	metadataVersion           = "version"
	metadataTerminal          = "terminal"
	metadataTerminalBlock     = "request_block"
	commonTransportHTTPStatus = "http_status"
	commonTransportLogOnly    = "log_only"
	envoyStatusHeader         = ":status"
	statusUnavailable         = 503
	defaultUpstreamStatus     = 200
	maxRedirectURLBytes       = 2048
)

// postTransportError marks a failure discovered only after the adapter has
// successfully sent an irreversible response to Envoy.  Its caller must not
// manufacture a second ImmediateResponse: doing so would make the recorded
// host outcome false.
type postTransportError struct {
	reason string
	err    error
}

func (e *postTransportError) Error() string { return e.reason + ": " + e.err.Error() }
func (e *postTransportError) Unwrap() error { return e.err }

// AuthzServer is the P1/P2 side of a composite Envoy integration.
type AuthzServer struct {
	authv3.UnimplementedAuthorizationServer
	coordinator *composite.Coordinator
}

func NewAuthzServer(coordinator *composite.Coordinator) (*AuthzServer, error) {
	if coordinator == nil {
		return nil, errors.New("composite coordinator is required")
	}
	return &AuthzServer{coordinator: coordinator}, nil
}

// Check deliberately does not use HttpRequest.Id as an identifier.  Envoy's
// request id is input data and is therefore unsuitable for lease correlation.
func (s *AuthzServer) Check(ctx context.Context, req *authv3.CheckRequest) (*authv3.CheckResponse, error) {
	cleanupCtx := context.WithoutCancel(ctx)
	meta, headers, body, err := authRequest(req)
	if err != nil {
		return nil, status.Error(codes.InvalidArgument, err.Error())
	}
	admission, decision, err := s.coordinator.BeginRequest(ctx, meta, headers, false)
	if err != nil {
		return handleAdmissionError(ctx, cleanupCtx, admission, decision, err, false)
	}
	if decision.Action != processor.ActionAllow {
		decision = normalizePolicyDecision(decision, nil)
		if recordErr := admission.RecordHostAction(ctx, processor.HostAction{Action: appliedAction(decision), VisibleStatus: decision.Status, TransportResult: commonTransportHTTPStatus}); recordErr != nil {
			return nil, authFailure(recordErr)
		}
		admission.Finish(cleanupCtx, "request_block")
		return denied(decision), nil
	}
	leased := false
	defer func() {
		if admission != nil && !leased {
			admission.Finish(cleanupCtx, "request_block")
		}
	}()
	decision, err = admission.ProcessBody(ctx, body, true)
	if err != nil {
		return handleAdmissionError(ctx, cleanupCtx, admission, decision, err, true)
	}
	if decision.Action != processor.ActionAllow {
		decision = normalizePolicyDecision(decision, nil)
		if recordErr := admission.RecordHostAction(ctx, processor.HostAction{Action: appliedAction(decision), VisibleStatus: decision.Status, TransportResult: commonTransportHTTPStatus}); recordErr != nil {
			return nil, authFailure(recordErr)
		}
		admission.Finish(cleanupCtx, "request_block")
		return denied(decision), nil
	}
	lease, err := admission.Lease()
	if err != nil {
		return nil, authFailure(err)
	}
	leased = true
	// DynamicMetadata is emitted by ext_authz in the namespace of this filter;
	// the companion ext_proc filter is configured to forward only this namespace.
	dynamic, err := structpb.NewStruct(map[string]interface{}{"lease": lease, "version": float64(1)})
	if err != nil {
		return nil, authFailure(err)
	}
	return &authv3.CheckResponse{
		Status:          status.New(codes.OK, "").Proto(),
		HttpResponse:    &authv3.CheckResponse_OkResponse{OkResponse: &authv3.OkHttpResponse{}},
		DynamicMetadata: dynamic,
	}, nil
}

func handleAdmissionError(ctx, cleanupCtx context.Context, admission *composite.Admission, decision processor.Decision, err error, recordDeny bool) (*authv3.CheckResponse, error) {
	if errors.Is(err, composite.ErrNotAllowed) {
		decision = normalizePolicyDecision(decision, err)
		if recordDeny {
			if recordErr := admission.RecordHostAction(ctx, processor.HostAction{Action: appliedAction(decision), VisibleStatus: decision.Status, TransportResult: commonTransportHTTPStatus}); recordErr != nil {
				return nil, authFailure(recordErr)
			}
		}
		return denied(decision), nil
	}
	if errors.Is(err, composite.ErrLimit) {
		decision = normalizePolicyDecision(decision, err)
		if admission != nil {
			if recordErr := admission.RecordRequestBodyLimitHostAction(); recordErr != nil {
				return nil, authFailure(recordErr)
			}
			admission.Finish(cleanupCtx, "request_body_limit")
		}
		return denied(decision), nil
	}
	return nil, authFailure(err)
}

// ExtProcServer binds one Envoy ext_proc stream to the lease minted by
// AuthzServer.  It never opens a second Common transaction.
type ExtProcServer struct {
	extprocv3.UnimplementedExternalProcessorServer
	coordinator *composite.Coordinator
}

func NewExtProcServer(coordinator *composite.Coordinator) (*ExtProcServer, error) {
	if coordinator == nil {
		return nil, errors.New("composite coordinator is required")
	}
	return &ExtProcServer{coordinator: coordinator}, nil
}

func (s *ExtProcServer) Process(stream extprocv3.ExternalProcessor_ProcessServer) error {
	ctx := stream.Context()
	first, err := stream.Recv()
	if err != nil {
		return classifyRecv(err)
	}
	firstIsRequestHeaders := first.GetRequestHeaders() != nil
	firstIsResponseHeaders := first.GetResponseHeaders() != nil
	if terminalBlockFromMetadata(first.GetMetadataContext()) {
		// ext_authz has already sent a server-owned P1/P2 local denial. It is
		// not a companion transaction and must not be allowed to claim a lease,
		// but ext_proc must continue the marked local reply without replacing
		// its client-visible 4xx status.
		if !firstIsResponseHeaders {
			return sendImmediate(stream, processor.Decision{Action: processor.ActionDeny, Status: statusUnavailable})
		}
		return continueMarkedTerminalReply(stream, first)
	}
	lease, ok := leaseFromMetadata(first.GetMetadataContext())
	if !ok || (!firstIsRequestHeaders && !firstIsResponseHeaders) {
		return sendImmediate(stream, processor.Decision{Action: processor.ActionDeny, Status: statusUnavailable})
	}
	session, err := serverSession()
	if err != nil {
		return status.Error(codes.Internal, "cannot create server session")
	}
	response, err := s.coordinator.Claim(lease, session)
	if err != nil {
		return sendImmediate(stream, processor.Decision{Action: processor.ActionDeny, Status: statusUnavailable})
	}
	finished := false
	cleanupCtx := context.WithoutCancel(ctx)
	finish := func(reason string) {
		if !finished {
			finished = true
			response.Finish(cleanupCtx, reason)
		}
	}
	defer finish("grpc_peer_eof")
	state := &responseStreamState{stream: stream, response: response}
	return s.runResponseStream(ctx, state, first, firstIsRequestHeaders, finish)
}

func (s *ExtProcServer) runResponseStream(ctx context.Context, state *responseStreamState, first *extprocv3.ProcessingRequest, firstIsRequestHeaders bool, finish func(string)) error {
	handleProcessError := func(err error) error {
		var post *postTransportError
		if errors.As(err, &post) {
			finish(post.reason)
			return status.Errorf(codes.Internal, "composite outcome evidence unavailable after Envoy response: %v", post.err)
		}
		finish("processor_error")
		if sendErr := sendImmediate(state.stream, processor.Decision{Action: processor.ActionDeny, Status: statusUnavailable}); sendErr != nil {
			return sendErr
		}
		return nil
	}
	if firstIsRequestHeaders {
		return s.runRequestHeadersPhase(ctx, state, finish, handleProcessError)
	}
	if err := s.processStreamRequest(ctx, state, first, finish, handleProcessError); err != nil {
		return err
	}
	return s.runResponseLoop(ctx, state, finish, handleProcessError)
}

func (s *ExtProcServer) runRequestHeadersPhase(ctx context.Context, state *responseStreamState, finish func(string), handleProcessError func(error) error) error {
	// Kept as a fail-closed compatibility path for a pinned host that still
	// sends the protected request phase. The composite template skips it.
	if err := sendContinue(state.stream, requestHeadersResponse()); err != nil {
		finish("processor_error")
		return err
	}
	return s.runResponseLoop(ctx, state, finish, handleProcessError)
}

func (s *ExtProcServer) processStreamRequest(ctx context.Context, state *responseStreamState, request *extprocv3.ProcessingRequest, finish func(string), handleProcessError func(error) error) error {
	terminal, err := s.processResponse(ctx, state, request)
	if err != nil {
		return handleProcessError(err)
	}
	if terminal {
		state.responseDone = true
		finish("response_end_of_stream")
		return nil
	}
	return nil
}

func (s *ExtProcServer) runResponseLoop(ctx context.Context, state *responseStreamState, finish func(string), handleProcessError func(error) error) error {
	for {
		request, err := state.stream.Recv()
		if err != nil {
			if errors.Is(err, io.EOF) {
				return nil
			}
			finish("grpc_context_canceled_unattributed")
			return classifyRecv(err)
		}
		terminal, err := s.processResponse(ctx, state, request)
		if err != nil {
			return handleProcessError(err)
		}
		if terminal {
			state.responseDone = true
			finish("response_end_of_stream")
			return nil
		}
	}
}

type responseStreamState struct {
	stream               extprocv3.ExternalProcessor_ProcessServer
	response             *composite.Response
	responseHeadersSeen  bool
	responseTrailersSeen bool
	responseDone         bool
	upstreamStatus       int
	lateActionRecorded   bool
}

func (s *ExtProcServer) processResponse(ctx context.Context, state *responseStreamState, request *extprocv3.ProcessingRequest) (bool, error) {
	if request == nil {
		return false, errors.New("empty ext_proc request")
	}
	switch {
	case request.GetResponseHeaders() != nil:
		if state.responseHeadersSeen || state.responseDone {
			return false, errors.New("duplicate response headers")
		}
		state.responseHeadersSeen = true
		return s.responseHeaders(ctx, state.stream, state.response, request.GetResponseHeaders(), &state.upstreamStatus)
	case request.GetResponseBody() != nil:
		if !state.responseHeadersSeen || state.responseDone || state.responseTrailersSeen {
			return false, errors.New("response body violates stream order")
		}
		return s.responseBody(ctx, state.stream, state.response, request.GetResponseBody(), state.upstreamStatus, &state.lateActionRecorded)
	case request.GetResponseTrailers() != nil:
		if !state.responseHeadersSeen || state.responseDone || state.responseTrailersSeen {
			return false, errors.New("duplicate or out-of-order response trailers")
		}
		state.responseTrailersSeen = true
		return s.responseTrailers(ctx, state.stream, state.response, request.GetResponseTrailers(), state.upstreamStatus, &state.lateActionRecorded)
	default:
		return false, errors.New("unexpected ext_proc phase; composite stream accepts response phases only")
	}
}

func (s *ExtProcServer) responseHeaders(ctx context.Context, stream extprocv3.ExternalProcessor_ProcessServer, response *composite.Response, msg *extprocv3.HttpHeaders, upstreamStatus *int) (bool, error) {
	headers, err := decodeHeaders(msg.GetHeaders())
	if err != nil {
		return false, err
	}
	visibleStatus := responseStatus(headers)
	*upstreamStatus = visibleStatus
	decision, err := response.Headers(ctx, headers, msg.GetEndOfStream())
	if err != nil {
		return false, err
	}
	if decision.Action != processor.ActionAllow {
		decision = normalizePolicyDecision(decision, nil)
		if err := sendImmediate(stream, decision); err != nil {
			return false, err
		}
		if err := response.RecordHostAction(ctx, processor.HostAction{Action: appliedAction(decision), VisibleStatus: decision.Status, TransportResult: commonTransportHTTPStatus}); err != nil {
			return false, &postTransportError{reason: "host_action_unknown_after_immediate", err: err}
		}
		response.Finish(context.WithoutCancel(ctx), "response_block")
		return true, nil
	}
	if err := sendContinue(stream, responseHeadersResponse()); err != nil {
		return false, err
	}
	if err := response.MarkResponseCommitted(ctx); err != nil {
		return false, &postTransportError{reason: "response_commit_unknown_after_continue", err: err}
	}
	if msg.GetEndOfStream() {
		if err := response.RecordNeutralOutcome(ctx, visibleStatus, "response_allow"); err != nil {
			return false, &postTransportError{reason: "neutral_outcome_unknown_after_continue", err: err}
		}
	}
	return msg.GetEndOfStream(), nil
}

func (s *ExtProcServer) responseBody(ctx context.Context, stream extprocv3.ExternalProcessor_ProcessServer, response *composite.Response, msg *extprocv3.HttpBody, upstreamStatus int, lateActionRecorded *bool) (bool, error) {
	decision, err := response.Body(ctx, msg.GetBody(), msg.GetEndOfStream())
	if err != nil {
		return false, err
	}
	// The response has already crossed the commit boundary. Disruptive P4
	// decisions are therefore recorded as log-only and never reset the stream.
	if err := sendContinue(stream, bodyResponse()); err != nil {
		return false, err
	}
	if decision.Action != processor.ActionAllow {
		if err := response.RecordHostAction(ctx, processor.HostAction{Action: processor.AppliedActionLogOnly, VisibleStatus: upstreamStatus, TransportResult: commonTransportLogOnly}); err != nil {
			return false, &postTransportError{reason: "late_host_action_unknown_after_continue", err: err}
		}
		*lateActionRecorded = true
	} else if msg.GetEndOfStream() && !*lateActionRecorded {
		if err := response.RecordNeutralOutcome(ctx, upstreamStatus, "response_allow"); err != nil {
			return false, &postTransportError{reason: "neutral_outcome_unknown_after_continue", err: err}
		}
	}
	return msg.GetEndOfStream(), nil
}

func (s *ExtProcServer) responseTrailers(ctx context.Context, stream extprocv3.ExternalProcessor_ProcessServer, response *composite.Response, msg *extprocv3.HttpTrailers, upstreamStatus int, lateActionRecorded *bool) (bool, error) {
	if msg == nil {
		return false, errors.New("missing response trailers")
	}
	decision, err := response.Body(ctx, nil, true)
	if err != nil {
		return false, err
	}
	if err := sendContinue(stream, trailersResponse()); err != nil {
		return false, err
	}
	if decision.Action != processor.ActionAllow {
		if err := response.RecordHostAction(ctx, processor.HostAction{Action: processor.AppliedActionLogOnly, VisibleStatus: upstreamStatus, TransportResult: commonTransportLogOnly}); err != nil {
			return false, &postTransportError{reason: "late_host_action_unknown_after_continue", err: err}
		}
		*lateActionRecorded = true
	} else if !*lateActionRecorded {
		if err := response.RecordNeutralOutcome(ctx, upstreamStatus, "response_allow"); err != nil {
			return false, &postTransportError{reason: "neutral_outcome_unknown_after_continue", err: err}
		}
	}
	return true, nil
}

func responseStatus(headers []processor.Header) int {
	for _, header := range headers {
		if header.Name == envoyStatusHeader {
			if statusCode, err := strconv.Atoi(string(header.Value)); err == nil && statusCode >= 100 && statusCode <= 599 {
				return statusCode
			}
		}
	}
	return 200
}

func authRequest(req *authv3.CheckRequest) (processor.StreamMetadata, []processor.Header, []byte, error) {
	if req == nil || req.GetAttributes() == nil || req.GetAttributes().GetRequest() == nil || req.GetAttributes().GetRequest().GetHttp() == nil {
		return processor.StreamMetadata{}, nil, nil, errors.New("missing Envoy HTTP attributes")
	}
	h := req.GetAttributes().GetRequest().GetHttp()
	if h.GetMethod() == "" {
		return processor.StreamMetadata{}, nil, nil, errors.New("missing HTTP method")
	}
	values := make(map[string]string, len(h.GetHeaders()))
	keys := make([]string, 0, len(h.GetHeaders()))
	for k, v := range h.GetHeaders() {
		k = strings.ToLower(k)
		// The lease is host-generated metadata, never request input. Envoy's
		// header_mutation filter removes it before this callback, but keep the
		// boundary defensive if a direct caller or alternate filter chain sends
		// the protected name anyway.
		if k == compositeLeaseHeader {
			continue
		}
		if _, exists := values[k]; exists {
			return processor.StreamMetadata{}, nil, nil, errors.New("duplicate HTTP header names")
		}
		values[k] = v
		keys = append(keys, k)
	}
	sort.Strings(keys)
	headers := make([]processor.Header, 0, len(keys))
	for _, k := range keys {
		headers = append(headers, processor.Header{Name: k, Value: []byte(values[k])})
	}
	body := h.GetRawBody()
	if len(body) == 0 && h.GetBody() != "" {
		body = []byte(h.GetBody())
	}
	clientAddress, clientPort, err := peerMetadata(req.GetAttributes().GetSource())
	if err != nil {
		return processor.StreamMetadata{}, nil, nil, err
	}
	serverAddress, serverPort, err := peerMetadata(req.GetAttributes().GetDestination())
	if err != nil {
		return processor.StreamMetadata{}, nil, nil, err
	}
	if h.GetHost() == "" || h.GetProtocol() == "" || h.GetPath() == "" {
		return processor.StreamMetadata{}, nil, nil, errors.New("missing required HTTP metadata")
	}
	return processor.StreamMetadata{Request: processor.RequestMetadata{Method: h.GetMethod(), URI: h.GetPath(), Protocol: h.GetProtocol(), Hostname: h.GetHost(), ClientAddress: clientAddress, ClientPort: clientPort, ServerAddress: serverAddress, ServerPort: serverPort}}, headers, body, nil
}

func peerMetadata(peer *authv3.AttributeContext_Peer) (string, int, error) {
	if peer == nil || peer.GetAddress() == nil || peer.GetAddress().GetSocketAddress() == nil {
		return "", 0, errors.New("missing Envoy peer address")
	}
	socket := peer.GetAddress().GetSocketAddress()
	if socket.GetAddress() == "" || socket.GetPortValue() == 0 || socket.GetPortValue() > 65535 {
		return "", 0, errors.New("ambiguous Envoy peer address")
	}
	return socket.GetAddress(), int(socket.GetPortValue()), nil
}

func leaseFromMetadata(metadata *corev3.Metadata) (string, bool) {
	if metadata == nil {
		return "", false
	}
	value := metadata.GetFilterMetadata()[metadataNamespace]
	if value == nil {
		return "", false
	}
	field := value.GetFields()[metadataLease]
	if field == nil || field.GetStringValue() == "" || len(field.GetStringValue()) > 512 {
		return "", false
	}
	version := value.GetFields()[metadataVersion]
	if version == nil || version.GetNumberValue() != 1 {
		return "", false
	}
	return field.GetStringValue(), true
}

// terminalBlockMetadata marks only the ext_authz-generated local response for
// a P1/P2 block. It is not a lease and can never authorize a companion claim.
// Envoy owns the ext_authz dynamic-metadata namespace, so request headers and
// other client input cannot create this marker.
func terminalBlockMetadata() *structpb.Struct {
	return &structpb.Struct{Fields: map[string]*structpb.Value{
		metadataTerminal: structpb.NewStringValue(metadataTerminalBlock),
		metadataVersion:  structpb.NewNumberValue(1),
	}}
}

func terminalBlockFromMetadata(metadata *corev3.Metadata) bool {
	if metadata == nil {
		return false
	}
	value := metadata.GetFilterMetadata()[metadataNamespace]
	if value == nil || value.GetFields()[metadataLease] != nil {
		return false
	}
	terminal := value.GetFields()[metadataTerminal]
	version := value.GetFields()[metadataVersion]
	return terminal != nil && terminal.GetStringValue() == metadataTerminalBlock && version != nil && version.GetNumberValue() == 1
}

// continueMarkedTerminalReply forwards an ext_authz-created P1/P2 local reply
// after validating its protected marker. It retains no payload and never
// opens, claims, or records a Common transaction; any unmarked lease-less
// response remains fail-closed in Process.
func continueMarkedTerminalReply(stream extprocv3.ExternalProcessor_ProcessServer, first *extprocv3.ProcessingRequest) error {
	responseHeadersSeen := false
	request := first
	for {
		done, nextHeadersSeen, err := continueMarkedRequest(stream, request, responseHeadersSeen)
		if err != nil || done {
			return err
		}
		responseHeadersSeen = nextHeadersSeen
		next, err := stream.Recv()
		if err != nil {
			return classifyRecv(err)
		}
		request = next
	}
}

func continueMarkedRequest(stream extprocv3.ExternalProcessor_ProcessServer, request *extprocv3.ProcessingRequest, responseHeadersSeen bool) (bool, bool, error) {
	deny := func() (bool, bool, error) {
		return true, responseHeadersSeen, sendImmediate(stream, processor.Decision{Action: processor.ActionDeny, Status: statusUnavailable})
	}
	if request == nil {
		return deny()
	}
	switch {
	case request.GetResponseHeaders() != nil:
		if responseHeadersSeen {
			return deny()
		}
		headers, err := decodeHeaders(request.GetResponseHeaders().GetHeaders())
		if err != nil || !validMarkedTerminalReply(headers) {
			return deny()
		}
		if err := sendContinue(stream, responseHeadersResponse()); err != nil {
			return true, responseHeadersSeen, err
		}
		return request.GetResponseHeaders().GetEndOfStream(), true, nil
	case request.GetResponseBody() != nil:
		if !responseHeadersSeen {
			return deny()
		}
		if err := sendContinue(stream, bodyResponse()); err != nil {
			return true, responseHeadersSeen, err
		}
		return request.GetResponseBody().GetEndOfStream(), responseHeadersSeen, nil
	case request.GetResponseTrailers() != nil:
		if !responseHeadersSeen {
			return deny()
		}
		return true, responseHeadersSeen, sendContinue(stream, trailersResponse())
	default:
		return deny()
	}
}

func decodeHeaders(headerMap *corev3.HeaderMap) ([]processor.Header, error) {
	if headerMap == nil {
		return nil, errors.New("missing Envoy header map")
	}
	headers := make([]processor.Header, 0, len(headerMap.GetHeaders()))
	for _, h := range headerMap.GetHeaders() {
		if h == nil || h.GetKey() == "" {
			return nil, errors.New("malformed Envoy header")
		}
		value := h.GetRawValue()
		if len(value) == 0 {
			value = []byte(h.GetValue())
		}
		headers = append(headers, processor.Header{Name: strings.ToLower(h.GetKey()), Value: value})
	}
	return headers, nil
}

func serverSession() (string, error) {
	b := make([]byte, 32)
	if _, err := rand.Read(b); err != nil {
		return "", err
	}
	return base64.RawURLEncoding.EncodeToString(b), nil
}

func denied(d processor.Decision) *authv3.CheckResponse {
	d = normalizePolicyDecision(d, nil)
	denied := &authv3.DeniedHttpResponse{Status: &typev3.HttpStatus{Code: typev3.StatusCode(d.Status)}}
	if d.Action == processor.ActionRedirect {
		denied.Headers = []*corev3.HeaderValueOption{{Header: &corev3.HeaderValue{Key: "location", Value: d.RedirectURL}}}
	}
	return &authv3.CheckResponse{Status: status.New(codes.PermissionDenied, "request denied").Proto(), HttpResponse: &authv3.CheckResponse_DeniedResponse{DeniedResponse: denied}, DynamicMetadata: terminalBlockMetadata()}
}

func normalizePolicyDecision(d processor.Decision, err error) processor.Decision {
	if errors.Is(err, composite.ErrLimit) {
		d.Action = processor.ActionDeny
		d.Status = 413
		d.RedirectURL = ""
		return d
	}
	switch d.Action {
	case processor.ActionDeny:
		if d.Status < 400 || d.Status > 599 {
			d.Status = 403
		}
		return d
	case processor.ActionRedirect:
		if !validRedirectURL(d.RedirectURL) {
			return processor.Decision{Action: processor.ActionDeny, Status: 403}
		}
		if d.Status < 300 || d.Status > 399 {
			d.Status = 307
		}
		return d
	default:
		d.Action = processor.ActionDeny
		d.Status = 403
		d.RedirectURL = ""
		return d
	}
}

func validRedirectURL(value string) bool {
	if value == "" || len(value) > maxRedirectURLBytes || value != strings.TrimSpace(value) {
		return false
	}
	for i := 0; i < len(value); i++ {
		if value[i] < 0x20 || value[i] == 0x7f {
			return false
		}
	}
	return true
}

func validMarkedTerminalReply(headers []processor.Header) bool {
	status, statusSeen, locationSeen, valid := scanMarkedTerminalReply(headers)
	if !valid || !statusSeen {
		return false
	}
	if status >= 400 && status <= 599 {
		return !locationSeen
	}
	return status >= 300 && status <= 399 && locationSeen
}

func scanMarkedTerminalReply(headers []processor.Header) (int, bool, bool, bool) {
	status := 0
	statusSeen := false
	locationSeen := false
	for _, header := range headers {
		switch header.Name {
		case envoyStatusHeader:
			if statusSeen {
				return 0, false, false, false
			}
			parsed, ok := markedTerminalStatus(header.Value)
			if !ok {
				return 0, false, false, false
			}
			status = parsed
			statusSeen = true
		case "location":
			if locationSeen || !validRedirectURL(string(header.Value)) {
				return 0, false, false, false
			}
			locationSeen = true
		}
	}
	return status, statusSeen, locationSeen, true
}

func markedTerminalStatus(value []byte) (int, bool) {
	status, err := strconv.Atoi(string(value))
	return status, err == nil && status >= 100 && status <= 599
}

func appliedAction(d processor.Decision) processor.AppliedAction {
	if d.Action == processor.ActionRedirect {
		return processor.AppliedActionRedirect
	}
	return processor.AppliedActionDeny
}

func authFailure(err error) error {
	return status.Errorf(codes.Unavailable, "composite authorization unavailable: %v", err)
}
func classifyRecv(err error) error {
	if errors.Is(err, io.EOF) {
		return nil
	}
	if errors.Is(err, context.Canceled) {
		return nil
	}
	return status.Errorf(codes.Unavailable, "ext_proc receive failed: %v", err)
}
func requestHeadersResponse() *extprocv3.ProcessingResponse {
	return &extprocv3.ProcessingResponse{Response: &extprocv3.ProcessingResponse_RequestHeaders{RequestHeaders: &extprocv3.HeadersResponse{Response: &extprocv3.CommonResponse{Status: extprocv3.CommonResponse_CONTINUE}}}}
}
func responseHeadersResponse() *extprocv3.ProcessingResponse {
	return &extprocv3.ProcessingResponse{Response: &extprocv3.ProcessingResponse_ResponseHeaders{ResponseHeaders: &extprocv3.HeadersResponse{Response: &extprocv3.CommonResponse{Status: extprocv3.CommonResponse_CONTINUE}}}}
}
func bodyResponse() *extprocv3.ProcessingResponse {
	return &extprocv3.ProcessingResponse{Response: &extprocv3.ProcessingResponse_ResponseBody{ResponseBody: &extprocv3.BodyResponse{Response: &extprocv3.CommonResponse{Status: extprocv3.CommonResponse_CONTINUE}}}}
}
func trailersResponse() *extprocv3.ProcessingResponse {
	return &extprocv3.ProcessingResponse{Response: &extprocv3.ProcessingResponse_ResponseTrailers{ResponseTrailers: &extprocv3.TrailersResponse{}}}
}
func sendContinue(stream extprocv3.ExternalProcessor_ProcessServer, response *extprocv3.ProcessingResponse) error {
	return stream.Send(response)
}
func sendImmediate(stream extprocv3.ExternalProcessor_ProcessServer, decision processor.Decision) error {
	decision = normalizePolicyDecision(decision, nil)
	immediate := &extprocv3.ImmediateResponse{Status: &typev3.HttpStatus{Code: typev3.StatusCode(decision.Status)}, Details: "msconnector-composite-fail-closed"}
	if decision.Action == processor.ActionRedirect {
		immediate.Headers = &extprocv3.HeaderMutation{SetHeaders: []*corev3.HeaderValueOption{{Header: &corev3.HeaderValue{Key: "location", Value: decision.RedirectURL}}}}
	}
	return stream.Send(&extprocv3.ProcessingResponse{Response: &extprocv3.ProcessingResponse_ImmediateResponse{ImmediateResponse: immediate}})
}

var _ authv3.AuthorizationServer = (*AuthzServer)(nil)
var _ extprocv3.ExternalProcessorServer = (*ExtProcServer)(nil)
