package processor

import (
	"context"
	"errors"
	"fmt"
	"io"
	"strings"
	"sync"

	corev3 "github.com/envoyproxy/go-control-plane/envoy/config/core/v3"
	extprocv3 "github.com/envoyproxy/go-control-plane/envoy/service/ext_proc/v3"
	typev3 "github.com/envoyproxy/go-control-plane/envoy/type/v3"
	"google.golang.org/grpc/codes"
	"google.golang.org/grpc/status"
)

// Direction distinguishes request and response data while keeping the engine
// seam free from Envoy protobuf types.
type Direction string

const (
	DirectionRequest  Direction = "request"
	DirectionResponse Direction = "response"
)

// Header is a bounded, temporary view over one header. Values are never held
// in stream state. Engines must consume the value during the callback and must
// not retain it.
type Header struct {
	Name  string
	Value []byte
}

// StreamMetadata is deliberately small and contains no body/header payload.
type StreamMetadata struct {
	TransactionID string
}

// Summary is provided to the future Common/libmodsecurity adapter at cleanup.
// It records only counters and action metadata, never request or response body
// content.
type Summary struct {
	TransactionID       string
	RequestHeaderCount  uint64
	ResponseHeaderCount uint64
	RequestBodyChunks   uint64
	ResponseBodyChunks  uint64
	RequestBodyBytes    int64
	ResponseBodyBytes   int64
	LateAction          LateActionOutcome
	CloseReason         CloseReason
}

// Action is a prospective engine decision. Only decisions found before the
// response-header boundary can use ext_proc ImmediateResponse in this source
// groundwork.
type Action string

const (
	ActionAllow    Action = "allow"
	ActionDeny     Action = "deny"
	ActionRedirect Action = "redirect"
)

// Decision is supplied by the connector-local evaluation seam. The checked-in
// service uses PassthroughEngine, which only returns ActionAllow.
type Decision struct {
	Action      Action
	Status      int
	RedirectURL string
}

func allowDecision() Decision {
	return Decision{Action: ActionAllow}
}

func (decision Decision) disruptive() bool {
	return decision.Action == ActionDeny || decision.Action == ActionRedirect
}

// LateActionOutcome never claims a downstream reset. In particular, strict is
// intentionally not implemented through a gRPC error: that is a processor
// failure signal, not evidence of a client-visible abort.
type LateActionOutcome string

const (
	LateActionNone               LateActionOutcome = "none"
	LateActionLogged             LateActionOutcome = "log_only"
	LateActionStrictNotAttempted LateActionOutcome = "strict_abort_not_attempted"
)

// CloseReason describes the ext_proc stream lifecycle, not a proven underlying
// HTTP reset cause. Envoy does not identify client versus upstream resets to
// this service on gRPC context cancellation alone.
type CloseReason string

const (
	CloseResponseEOS       CloseReason = "response_end_of_stream"
	CloseImmediateResponse CloseReason = "request_immediate_response"
	ClosePeerEOF           CloseReason = "grpc_peer_eof"
	CloseContextCanceled   CloseReason = "grpc_context_canceled_unattributed"
	CloseProcessorError    CloseReason = "processor_error"
)

// Engine is the narrow future bridge to Common/libmodsecurity. It receives
// incremental data only. The current source/build service installs a
// PassthroughEngine so it makes no claim that Common/libmodsecurity is wired.
type Engine interface {
	Open(context.Context, StreamMetadata) (Transaction, error)
}

// Transaction consumes each bounded header/body callback synchronously.
// Body slices are borrowed from the protobuf message and must not be retained.
type Transaction interface {
	ProcessHeaders(context.Context, Direction, []Header, bool) (Decision, error)
	ProcessBody(context.Context, Direction, []byte, bool) (Decision, error)
	Close(context.Context, Summary)
}

// PassthroughEngine is intentionally the production default until the separate
// Common/libmodsecurity adapter is implemented and independently verified.
type PassthroughEngine struct{}

func (PassthroughEngine) Open(context.Context, StreamMetadata) (Transaction, error) {
	return passthroughTransaction{}, nil
}

type passthroughTransaction struct{}

func (passthroughTransaction) ProcessHeaders(context.Context, Direction, []Header, bool) (Decision, error) {
	return allowDecision(), nil
}

func (passthroughTransaction) ProcessBody(context.Context, Direction, []byte, bool) (Decision, error) {
	return allowDecision(), nil
}

func (passthroughTransaction) Close(context.Context, Summary) {}

// Service implements Envoy's official ext_proc ExternalProcessor gRPC service.
type Service struct {
	extprocv3.UnimplementedExternalProcessorServer

	config Config
	engine Engine
	active sync.WaitGroup
}

func NewService(config Config, engine Engine) (*Service, error) {
	if err := config.Validate(); err != nil {
		return nil, err
	}
	if engine == nil {
		return nil, fmt.Errorf("ext_proc engine is required")
	}
	return &Service{config: config, engine: engine}, nil
}

// Process owns one Envoy ext_proc gRPC stream and therefore one independent
// transaction state. No state is shared across parallel streams.
func (service *Service) Process(stream extprocv3.ExternalProcessor_ProcessServer) error {
	service.active.Add(1)
	defer service.active.Done()

	state := newStreamState(service.config, service.engine)
	closeReason := ClosePeerEOF
	defer func() {
		state.close(closeReason)
	}()

	for {
		request, err := stream.Recv()
		if err != nil {
			if errors.Is(err, io.EOF) {
				closeReason = ClosePeerEOF
				return nil
			}
			if stream.Context().Err() != nil {
				closeReason = CloseContextCanceled
				return nil
			}
			closeReason = CloseProcessorError
			return status.Errorf(codes.Unknown, "ext_proc receive failed: %v", err)
		}

		response, terminal, err := state.handle(stream.Context(), request)
		if err != nil {
			closeReason = CloseProcessorError
			return status.Errorf(codes.InvalidArgument, "ext_proc request rejected: %v", err)
		}
		if !request.GetObservabilityMode() {
			if err := stream.Send(response); err != nil {
				if stream.Context().Err() != nil {
					closeReason = CloseContextCanceled
					return nil
				}
				closeReason = CloseProcessorError
				return status.Errorf(codes.Unavailable, "ext_proc response send failed: %v", err)
			}
		}
		if terminal && !request.GetObservabilityMode() {
			closeReason = state.completionReason()
			return nil
		}
	}
}

type streamState struct {
	config Config
	engine Engine

	transaction   Transaction
	transactionID string

	requestHeadersSeen  bool
	responseHeadersSeen bool
	requestDone         bool
	responseDone        bool
	immediateResponse   bool
	closed              bool

	summary Summary
}

func newStreamState(config Config, engine Engine) *streamState {
	return &streamState{config: config, engine: engine, summary: Summary{LateAction: LateActionNone}}
}

func (state *streamState) handle(ctx context.Context, request *extprocv3.ProcessingRequest) (*extprocv3.ProcessingResponse, bool, error) {
	if request == nil || request.GetRequest() == nil {
		return nil, false, fmt.Errorf("empty processing request")
	}
	switch message := request.GetRequest().(type) {
	case *extprocv3.ProcessingRequest_RequestHeaders:
		return state.handleHeaders(ctx, DirectionRequest, message.RequestHeaders)
	case *extprocv3.ProcessingRequest_ResponseHeaders:
		return state.handleHeaders(ctx, DirectionResponse, message.ResponseHeaders)
	case *extprocv3.ProcessingRequest_RequestBody:
		return state.handleBody(ctx, DirectionRequest, message.RequestBody)
	case *extprocv3.ProcessingRequest_ResponseBody:
		return state.handleBody(ctx, DirectionResponse, message.ResponseBody)
	case *extprocv3.ProcessingRequest_RequestTrailers:
		return state.handleTrailers(DirectionRequest, message.RequestTrailers)
	case *extprocv3.ProcessingRequest_ResponseTrailers:
		return state.handleTrailers(DirectionResponse, message.ResponseTrailers)
	default:
		return nil, false, fmt.Errorf("unsupported processing request type %T", message)
	}
}

func (state *streamState) handleHeaders(ctx context.Context, direction Direction, message *extprocv3.HttpHeaders) (*extprocv3.ProcessingResponse, bool, error) {
	if message == nil {
		return nil, false, fmt.Errorf("%s headers are missing", direction)
	}
	if direction == DirectionRequest {
		if state.requestHeadersSeen {
			return nil, false, fmt.Errorf("duplicate request headers")
		}
		state.requestHeadersSeen = true
	} else {
		if !state.requestHeadersSeen {
			return nil, false, fmt.Errorf("response headers arrived before request headers")
		}
		if state.responseHeadersSeen {
			return nil, false, fmt.Errorf("duplicate response headers")
		}
		// This is a conservative commitment boundary. A normal headers response
		// allows Envoy to release the downstream response, so later data is
		// treated as late without claiming that a specific client byte was sent.
		state.responseHeadersSeen = true
	}

	headers, transactionID, limitDecision, err := state.decodeHeaders(message.GetHeaders())
	if err != nil {
		return nil, false, err
	}
	if direction == DirectionRequest && transactionID != "" {
		state.transactionID = transactionID
	}
	if err := state.ensureTransaction(ctx); err != nil {
		return nil, false, err
	}

	decision := limitDecision
	if decision.Action == ActionAllow {
		decision, err = state.processHeaders(ctx, direction, headers, message.GetEndOfStream())
		if err != nil {
			return nil, false, err
		}
	}
	if direction == DirectionRequest {
		state.summary.RequestHeaderCount += uint64(len(headers))
		state.requestDone = message.GetEndOfStream()
	} else {
		state.summary.ResponseHeaderCount += uint64(len(headers))
		state.responseDone = message.GetEndOfStream()
	}
	return state.responseForDecision(direction, headerPhase(direction), decision, state.responseDone)
}

func (state *streamState) handleBody(ctx context.Context, direction Direction, message *extprocv3.HttpBody) (*extprocv3.ProcessingResponse, bool, error) {
	if message == nil {
		return nil, false, fmt.Errorf("%s body is missing", direction)
	}
	if direction == DirectionRequest {
		if !state.requestHeadersSeen || state.requestDone {
			return nil, false, fmt.Errorf("request body violates stream order")
		}
	} else if !state.responseHeadersSeen || state.responseDone {
		return nil, false, fmt.Errorf("response body violates stream order")
	}
	if err := state.ensureTransaction(ctx); err != nil {
		return nil, false, err
	}

	body := message.GetBody()
	decision := allowDecision()
	if len(body) > state.config.MaxBodyChunkBytes {
		decision = Decision{Action: ActionDeny, Status: int(typev3.StatusCode_PayloadTooLarge)}
	} else if direction == DirectionRequest && state.summary.RequestBodyBytes+int64(len(body)) > state.config.MaxRequestBodyBytes {
		decision = Decision{Action: ActionDeny, Status: int(typev3.StatusCode_PayloadTooLarge)}
	} else if direction == DirectionResponse && state.summary.ResponseBodyBytes+int64(len(body)) > state.config.MaxResponseBodyBytes {
		decision = Decision{Action: ActionDeny, Status: int(typev3.StatusCode_PayloadTooLarge)}
	}
	if decision.Action == ActionAllow {
		processedDecision, err := state.processBody(ctx, direction, body, message.GetEndOfStream())
		if err != nil {
			return nil, false, err
		}
		decision = processedDecision
	}

	if direction == DirectionRequest {
		state.summary.RequestBodyChunks++
		state.summary.RequestBodyBytes += int64(len(body))
		state.requestDone = message.GetEndOfStream()
	} else {
		state.summary.ResponseBodyChunks++
		state.summary.ResponseBodyBytes += int64(len(body))
		state.responseDone = message.GetEndOfStream()
	}
	return state.responseForDecision(direction, bodyPhase(direction), decision, state.responseDone)
}

func (state *streamState) handleTrailers(direction Direction, message *extprocv3.HttpTrailers) (*extprocv3.ProcessingResponse, bool, error) {
	if message == nil {
		return nil, false, fmt.Errorf("%s trailers are missing", direction)
	}
	if direction == DirectionRequest {
		if !state.requestHeadersSeen || state.requestDone {
			return nil, false, fmt.Errorf("request trailers violate stream order")
		}
		state.requestDone = true
	} else {
		if !state.responseHeadersSeen || state.responseDone {
			return nil, false, fmt.Errorf("response trailers violate stream order")
		}
		state.responseDone = true
	}
	// The checked-in Envoy template skips trailers. If a caller enables them,
	// acknowledge them for stream hygiene but do not treat them as a body phase.
	return trailerResponse(direction), state.responseDone, nil
}

func (state *streamState) ensureTransaction(ctx context.Context) error {
	if state.transaction != nil {
		return nil
	}
	engineContext, cancel := context.WithTimeout(ctx, state.config.engineTimeout())
	defer cancel()
	transaction, err := state.engine.Open(engineContext, StreamMetadata{TransactionID: state.transactionID})
	if err != nil {
		return fmt.Errorf("open transaction: %w", err)
	}
	if transaction == nil {
		return fmt.Errorf("open transaction returned nil")
	}
	state.transaction = transaction
	return nil
}

func (state *streamState) processHeaders(ctx context.Context, direction Direction, headers []Header, eos bool) (Decision, error) {
	engineContext, cancel := context.WithTimeout(ctx, state.config.engineTimeout())
	defer cancel()
	decision, err := state.transaction.ProcessHeaders(engineContext, direction, headers, eos)
	if err != nil {
		return Decision{}, fmt.Errorf("process %s headers: %w", direction, err)
	}
	return normalizeDecision(decision), nil
}

func (state *streamState) processBody(ctx context.Context, direction Direction, body []byte, eos bool) (Decision, error) {
	engineContext, cancel := context.WithTimeout(ctx, state.config.engineTimeout())
	defer cancel()
	decision, err := state.transaction.ProcessBody(engineContext, direction, body, eos)
	if err != nil {
		return Decision{}, fmt.Errorf("process %s body: %w", direction, err)
	}
	return normalizeDecision(decision), nil
}

func (state *streamState) decodeHeaders(headerMap *corev3.HeaderMap) ([]Header, string, Decision, error) {
	if headerMap == nil {
		return nil, "", Decision{Action: ActionDeny, Status: int(typev3.StatusCode_RequestHeaderFieldsTooLarge)}, nil
	}
	values := headerMap.GetHeaders()
	if len(values) > state.config.MaxHeaderCount {
		return nil, "", Decision{Action: ActionDeny, Status: int(typev3.StatusCode_RequestHeaderFieldsTooLarge)}, nil
	}
	headers := make([]Header, 0, len(values))
	total := 0
	transactionID := ""
	for _, value := range values {
		if value == nil {
			return nil, "", Decision{}, fmt.Errorf("nil header")
		}
		name := value.GetKey()
		body := headerValueBytes(value)
		if len(name) > state.config.MaxHeaderNameBytes || len(body) > state.config.MaxHeaderValueBytes {
			return nil, "", Decision{Action: ActionDeny, Status: int(typev3.StatusCode_RequestHeaderFieldsTooLarge)}, nil
		}
		total += len(name) + len(body)
		if total > state.config.MaxTotalHeaderBytes {
			return nil, "", Decision{Action: ActionDeny, Status: int(typev3.StatusCode_RequestHeaderFieldsTooLarge)}, nil
		}
		if transactionID == "" && strings.EqualFold(name, state.config.TransactionIDHeader) {
			transactionID = boundedTransactionID(body)
		}
		headers = append(headers, Header{Name: name, Value: body})
	}
	return headers, transactionID, allowDecision(), nil
}

func headerValueBytes(value *corev3.HeaderValue) []byte {
	if raw := value.GetRawValue(); raw != nil {
		return raw
	}
	// Envoy's string field is UTF-8. This bounded conversion is necessary only
	// when raw_value was not used; stream state still never retains it.
	return []byte(value.GetValue())
}

func boundedTransactionID(value []byte) string {
	const maximumTransactionIDBytes = 128
	if len(value) == 0 || len(value) > maximumTransactionIDBytes {
		return ""
	}
	for _, byteValue := range value {
		if byteValue < 0x21 || byteValue > 0x7e {
			return ""
		}
	}
	return string(value)
}

func normalizeDecision(decision Decision) Decision {
	switch decision.Action {
	case ActionAllow:
		return allowDecision()
	case ActionDeny:
		if decision.Status < 400 || decision.Status > 599 {
			decision.Status = int(typev3.StatusCode_Forbidden)
		}
		return decision
	case ActionRedirect:
		if strings.TrimSpace(decision.RedirectURL) == "" {
			return Decision{Action: ActionDeny, Status: int(typev3.StatusCode_Forbidden)}
		}
		if decision.Status < 300 || decision.Status > 399 {
			decision.Status = int(typev3.StatusCode_TemporaryRedirect)
		}
		return decision
	default:
		return Decision{Action: ActionDeny, Status: int(typev3.StatusCode_Forbidden)}
	}
}

func (state *streamState) responseForDecision(direction Direction, phase processingPhase, decision Decision, responseDone bool) (*extprocv3.ProcessingResponse, bool, error) {
	if decision.disruptive() {
		if direction == DirectionRequest && !state.responseHeadersSeen {
			state.immediateResponse = true
			return immediateResponse(decision), true, nil
		}
		state.resolveLateAction()
	}
	return continueResponse(phase), responseDone, nil
}

func (state *streamState) resolveLateAction() {
	switch state.config.LateActionPolicy {
	case LateActionMinimal, LateActionSafe:
		state.summary.LateAction = LateActionLogged
	case LateActionStrict:
		// Do not send an ImmediateResponse or a gRPC error here. Envoy's API
		// does not make either a proven deterministic downstream stream reset;
		// presenting either as abort evidence would be dishonest.
		state.summary.LateAction = LateActionStrictNotAttempted
	}
}

type processingPhase uint8

const (
	phaseRequestHeaders processingPhase = iota
	phaseResponseHeaders
	phaseRequestBody
	phaseResponseBody
	phaseRequestTrailers
	phaseResponseTrailers
)

func headerPhase(direction Direction) processingPhase {
	if direction == DirectionRequest {
		return phaseRequestHeaders
	}
	return phaseResponseHeaders
}

func bodyPhase(direction Direction) processingPhase {
	if direction == DirectionRequest {
		return phaseRequestBody
	}
	return phaseResponseBody
}

func continueResponse(phase processingPhase) *extprocv3.ProcessingResponse {
	common := &extprocv3.CommonResponse{Status: extprocv3.CommonResponse_CONTINUE}
	switch phase {
	case phaseRequestHeaders:
		return &extprocv3.ProcessingResponse{Response: &extprocv3.ProcessingResponse_RequestHeaders{RequestHeaders: &extprocv3.HeadersResponse{Response: common}}}
	case phaseResponseHeaders:
		return &extprocv3.ProcessingResponse{Response: &extprocv3.ProcessingResponse_ResponseHeaders{ResponseHeaders: &extprocv3.HeadersResponse{Response: common}}}
	case phaseRequestBody:
		return &extprocv3.ProcessingResponse{Response: &extprocv3.ProcessingResponse_RequestBody{RequestBody: &extprocv3.BodyResponse{Response: common}}}
	case phaseResponseBody:
		return &extprocv3.ProcessingResponse{Response: &extprocv3.ProcessingResponse_ResponseBody{ResponseBody: &extprocv3.BodyResponse{Response: common}}}
	case phaseRequestTrailers:
		return &extprocv3.ProcessingResponse{Response: &extprocv3.ProcessingResponse_RequestTrailers{RequestTrailers: &extprocv3.TrailersResponse{}}}
	default:
		return &extprocv3.ProcessingResponse{Response: &extprocv3.ProcessingResponse_ResponseTrailers{ResponseTrailers: &extprocv3.TrailersResponse{}}}
	}
}

func trailerResponse(direction Direction) *extprocv3.ProcessingResponse {
	if direction == DirectionRequest {
		return continueResponse(phaseRequestTrailers)
	}
	return continueResponse(phaseResponseTrailers)
}

func immediateResponse(decision Decision) *extprocv3.ProcessingResponse {
	statusCode := typev3.StatusCode(decision.Status)
	response := &extprocv3.ImmediateResponse{
		Status:  &typev3.HttpStatus{Code: statusCode},
		Details: "msconnector-ext-proc-request-decision",
	}
	if decision.Action == ActionRedirect {
		response.Headers = &extprocv3.HeaderMutation{SetHeaders: []*corev3.HeaderValueOption{{
			Header: &corev3.HeaderValue{Key: "location", Value: decision.RedirectURL},
		}}}
	}
	return &extprocv3.ProcessingResponse{Response: &extprocv3.ProcessingResponse_ImmediateResponse{ImmediateResponse: response}}
}

func (state *streamState) completionReason() CloseReason {
	if state.immediateResponse {
		return CloseImmediateResponse
	}
	if state.responseDone {
		return CloseResponseEOS
	}
	return ClosePeerEOF
}

func (state *streamState) close(reason CloseReason) {
	if state.closed {
		return
	}
	state.closed = true
	if state.transaction == nil {
		return
	}
	state.summary.TransactionID = state.transactionID
	state.summary.CloseReason = reason
	cleanupContext, cancel := context.WithTimeout(context.Background(), state.config.cleanupTimeout())
	defer cancel()
	state.transaction.Close(cleanupContext, state.summary)
}
