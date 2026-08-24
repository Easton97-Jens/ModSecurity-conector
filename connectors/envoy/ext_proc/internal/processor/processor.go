package processor

import (
	"context"
	"errors"
	"fmt"
	"io"
	"net"
	"strconv"
	"strings"
	"sync"
	"sync/atomic"
	"time"

	corev3 "github.com/envoyproxy/go-control-plane/envoy/config/core/v3"
	extprocv3 "github.com/envoyproxy/go-control-plane/envoy/service/ext_proc/v3"
	typev3 "github.com/envoyproxy/go-control-plane/envoy/type/v3"
	"google.golang.org/grpc/codes"
	"google.golang.org/grpc/status"
	"google.golang.org/protobuf/types/known/structpb"
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

// RequestMetadata is the connection and pseudo-header metadata Envoy supplied
// for the downstream request. It deliberately contains no ordinary header or
// body payload. A Common/libmodsecurity bridge must reject missing required
// fields instead of substituting the Envoy-to-service gRPC peer address.
type RequestMetadata struct {
	Method        string
	URI           string
	Protocol      string
	Hostname      string
	ClientAddress string
	ClientPort    int
	ServerAddress string
	ServerPort    int
}

// StreamMetadata is deliberately small and contains no body/header payload.
type StreamMetadata struct {
	TransactionID string
	Request       RequestMetadata
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

// Decision is supplied by the connector-local evaluation seam. The production
// CGo build maps a real Common/libmodsecurity decision into this small form.
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
	CloseStreamIdleTimeout CloseReason = "grpc_stream_idle_timeout"
	CloseProcessorError    CloseReason = "processor_error"
)

// TransactionOpener receives only incremental data. The production
// libmodsecurity build installs CommonRuntimeEngine; PassthroughEngine remains
// for protobuf/unit development without CGo linkage.
type TransactionOpener interface {
	Open(context.Context, StreamMetadata) (Transaction, error)
}

// Transaction consumes each bounded header/body callback synchronously.
// Body slices are borrowed from the protobuf message and must not be retained.
type Transaction interface {
	ProcessHeaders(context.Context, Direction, []Header, bool) (Decision, error)
	ProcessBody(context.Context, Direction, []byte, bool) (Decision, error)
	Close(context.Context, Summary)
}

// CleanupFailureReporter is an optional transaction capability. Native
// cleanup cannot safely free a transaction while another native call owns the
// engine mutex; implementations report that bounded cleanup failure so the
// stream handler can return a controlled error and the supervisor can restart
// the process.
type CleanupFailureReporter interface {
	CleanupFailure() error
}

// ResponseCommitter is an optional transaction capability implemented by the
// Common/libmodsecurity bridge. It records the real adapter boundary only
// after ext_proc successfully sends a response-header CONTINUE to Envoy.
// Passthrough and test engines intentionally do not need to implement it.
type ResponseCommitter interface {
	MarkResponseCommitted(context.Context) error
}

// TransactionIDProvider is an optional capability for engines whose native
// transaction ID is resolved after the adapter opens its transaction.
type TransactionIDProvider interface {
	TransactionID() string
}

// AppliedAction records the host action that was actually accepted after a
// disruptive Common decision. It is deliberately separate from Decision:
// after a response commit the only truthful Envoy outcome is log-only, even
// if the rule engine requested a deny.
type AppliedAction string

const (
	AppliedActionDeny     AppliedAction = "deny"
	AppliedActionRedirect AppliedAction = "redirect"
	AppliedActionLogOnly  AppliedAction = "log_only"
)

// HostAction is payload-free confirmation that the ext_proc response was
// successfully written to Envoy. visible_status is the client-visible status
// that the adapter requested; it never stands in for an observed client byte.
type HostAction struct {
	Action          AppliedAction
	VisibleStatus   int
	TransportResult string
}

// HostActionRecorder is optional because the transport-only test engine has no
// native Common transaction. The real bridge records only successful actions,
// never a prospective decision or a failed gRPC send.
type HostActionRecorder interface {
	RecordHostAction(context.Context, HostAction) error
}

// Observer receives metadata-only stream completion records. It must never
// receive headers or body content: those values are intentionally borrowed by
// the stream adapter and are not retained in Summary.
type Observer interface {
	Record(Summary) error
}

type discardObserver struct{}

func (discardObserver) Record(Summary) error { return nil }

// PassthroughEngine is deliberately source-test-only. A binary built without
// the libmodsecurity tag refuses a Common runtime config rather than claiming
// that rule evaluation is wired.
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

func (passthroughTransaction) Close(context.Context, Summary) {
	// The source-only passthrough engine owns no per-stream resources.
}

// Service implements Envoy's official ext_proc ExternalProcessor gRPC service.
type Service struct {
	extprocv3.UnimplementedExternalProcessorServer

	config   Config
	engine   TransactionOpener
	observer Observer
	active   sync.WaitGroup
	// admission is process-wide rather than connection-local. gRPC's stream
	// limit protects each HTTP/2 connection; this second gate also bounds
	// transaction state when a peer opens streams over many connections.
	admission chan struct{}
	// pendingReceives counts the one Recv goroutine owned by each active stream.
	// It is evidence for deterministic cleanup tests, not a second admission
	// control: the gRPC stream context remains the cancellation mechanism.
	pendingReceives atomic.Int64
}

func NewService(config Config, engine TransactionOpener) (*Service, error) {
	return NewServiceWithObserver(config, engine, discardObserver{})
}

// NewServiceWithObserver constructs a service with an optional completion
// observer. A nil observer is equivalent to a discard observer, which keeps
// the existing unit-test and library API safe for callers that do not need
// runtime evidence.
func NewServiceWithObserver(config Config, engine TransactionOpener, observer Observer) (*Service, error) {
	if err := config.Validate(); err != nil {
		return nil, err
	}
	if engine == nil {
		return nil, fmt.Errorf("ext_proc engine is required")
	}
	if observer == nil {
		observer = discardObserver{}
	}
	return &Service{
		config:    config,
		engine:    engine,
		observer:  observer,
		admission: make(chan struct{}, config.MaxConcurrentStreams),
	}, nil
}

// Process owns one Envoy ext_proc gRPC stream and therefore one independent
// transaction state. No state is shared across parallel streams.
func (service *Service) Process(stream extprocv3.ExternalProcessor_ProcessServer) (processErr error) {
	select {
	case service.admission <- struct{}{}:
		defer func() { <-service.admission }()
	default:
		// Reject before allocating stream state or opening a Common
		// transaction. This makes overload a clean gRPC admission failure and
		// leaves no transaction/WaitGroup state to clean up.
		return status.Error(codes.ResourceExhausted, "ext_proc concurrent stream limit reached")
	}
	service.active.Add(1)
	defer service.active.Done()

	state := newStreamState(service.config, service.engine, service.observer)
	closeReason := ClosePeerEOF
	defer func() {
		if err := state.close(closeReason); err != nil && processErr == nil {
			processErr = status.Errorf(codes.Internal, "ext_proc metadata evidence: %v", err)
		}
	}()
	return service.processStream(stream, state, &closeReason)
}

func (service *Service) processStream(stream extprocv3.ExternalProcessor_ProcessServer, state *streamState, closeReason *CloseReason) error {
	for {
		request, receivedCloseReason, done, err := receiveProcessingRequest(
			stream, service.config.streamIdleTimeout(), &service.pendingReceives)
		if err != nil {
			*closeReason = receivedCloseReason
			return err
		}
		if done {
			*closeReason = receivedCloseReason
			return nil
		}
		terminal, requestCloseReason, err := service.processRequest(stream, state, request)
		if err != nil {
			*closeReason = requestCloseReason
			return err
		}
		if terminal {
			*closeReason = requestCloseReason
			return nil
		}
	}
}

type processingReceiveResult struct {
	request *extprocv3.ProcessingRequest
	err     error
}

// receiveProcessingRequest bounds inactivity, not evaluation. Activity means
// one complete ProcessingRequest arrived from Envoy; after every arrival the
// next interval begins only after the response/engine work for that message
// has completed. The gRPC server cancels stream.Context when Process returns,
// so the single buffered receive result cannot strand a sender after an idle
// deadline or a server shutdown.
func receiveProcessingRequest(
	stream extprocv3.ExternalProcessor_ProcessServer,
	idleTimeout time.Duration,
	pendingReceives *atomic.Int64,
) (*extprocv3.ProcessingRequest, CloseReason, bool, error) {
	resultChannel := make(chan processingReceiveResult, 1)
	if pendingReceives != nil {
		pendingReceives.Add(1)
	}
	go func() {
		if pendingReceives != nil {
			defer pendingReceives.Add(-1)
		}
		request, err := stream.Recv()
		resultChannel <- processingReceiveResult{request: request, err: err}
	}()

	timer := time.NewTimer(idleTimeout)
	defer timer.Stop()
	select {
	case result := <-resultChannel:
		return classifyProcessingReceiveResult(stream, result.request, result.err)
	case <-stream.Context().Done():
		return nil, CloseContextCanceled, true, nil
	case <-timer.C:
		return nil, CloseStreamIdleTimeout, false,
			status.Errorf(codes.DeadlineExceeded,
				"ext_proc stream idle timeout after %s", idleTimeout)
	}
}

func classifyProcessingReceiveResult(
	stream extprocv3.ExternalProcessor_ProcessServer,
	request *extprocv3.ProcessingRequest,
	err error,
) (*extprocv3.ProcessingRequest, CloseReason, bool, error) {
	if err == nil {
		return request, ClosePeerEOF, false, nil
	}
	if errors.Is(err, io.EOF) {
		return nil, ClosePeerEOF, true, nil
	}
	if stream.Context().Err() != nil {
		return nil, CloseContextCanceled, true, nil
	}
	return nil, CloseProcessorError, false, status.Errorf(codes.Unknown, "ext_proc receive failed: %v", err)
}

func (service *Service) processRequest(stream extprocv3.ExternalProcessor_ProcessServer, state *streamState, request *extprocv3.ProcessingRequest) (bool, CloseReason, error) {
	response, terminal, err := state.handle(stream.Context(), request)
	if err != nil {
		return false, CloseProcessorError, status.Errorf(codes.InvalidArgument, "ext_proc request rejected: %v", err)
	}
	if request.GetObservabilityMode() {
		return false, ClosePeerEOF, nil
	}
	if closeReason, sent, err := sendProcessingResponse(stream, response); err != nil {
		return false, closeReason, err
	} else if !sent {
		return true, closeReason, nil
	}
	if err := state.markResponseCommittedAfterSuccessfulContinue(stream.Context(), request, response); err != nil {
		return false, CloseProcessorError, status.Errorf(codes.Internal, "ext_proc response commit bookkeeping failed: %v", err)
	}
	if err := state.recordHostActionAfterSuccessfulResponse(stream.Context()); err != nil {
		return false, CloseProcessorError, status.Errorf(codes.Internal, "ext_proc host action evidence failed: %v", err)
	}
	if terminal {
		return true, state.completionReason(), nil
	}
	return false, ClosePeerEOF, nil
}

func sendProcessingResponse(stream extprocv3.ExternalProcessor_ProcessServer, response *extprocv3.ProcessingResponse) (CloseReason, bool, error) {
	if err := stream.Send(response); err != nil {
		if stream.Context().Err() != nil {
			return CloseContextCanceled, false, nil
		}
		return CloseProcessorError, false, status.Errorf(codes.Unavailable, "ext_proc response send failed: %v", err)
	}
	return ClosePeerEOF, true, nil
}

type streamState struct {
	config   Config
	engine   TransactionOpener
	observer Observer

	transaction   Transaction
	transactionID string
	request       RequestMetadata

	requestHeadersSeen  bool
	responseHeadersSeen bool
	requestDone         bool
	responseDone        bool
	responseStatus      int
	// responseHeadersSeen means Envoy delivered upstream response headers to
	// this service. It is an ordering boundary, not proof that Envoy released
	// anything downstream. responseCommitted changes only after this service
	// successfully sends the matching CONTINUE response to Envoy. It still does
	// not claim that a client byte has been observed.
	responseCommitted bool
	immediateResponse bool
	closed            bool
	pendingHostAction *HostAction

	summary Summary
}

func newStreamState(config Config, engine TransactionOpener, observer Observer) *streamState {
	return &streamState{config: config, engine: engine, observer: observer, summary: Summary{LateAction: LateActionNone}}
}

func (state *streamState) handle(ctx context.Context, request *extprocv3.ProcessingRequest) (*extprocv3.ProcessingResponse, bool, error) {
	if request == nil || request.GetRequest() == nil {
		return nil, false, fmt.Errorf("empty processing request")
	}
	switch message := request.GetRequest().(type) {
	case *extprocv3.ProcessingRequest_RequestHeaders:
		return state.handleHeaders(ctx, DirectionRequest, message.RequestHeaders, request.GetAttributes())
	case *extprocv3.ProcessingRequest_ResponseHeaders:
		return state.handleHeaders(ctx, DirectionResponse, message.ResponseHeaders, nil)
	case *extprocv3.ProcessingRequest_RequestBody:
		return state.handleBody(ctx, DirectionRequest, message.RequestBody)
	case *extprocv3.ProcessingRequest_ResponseBody:
		return state.handleBody(ctx, DirectionResponse, message.ResponseBody)
	case *extprocv3.ProcessingRequest_RequestTrailers:
		return state.handleTrailers(ctx, DirectionRequest, message.RequestTrailers)
	case *extprocv3.ProcessingRequest_ResponseTrailers:
		return state.handleTrailers(ctx, DirectionResponse, message.ResponseTrailers)
	default:
		return nil, false, fmt.Errorf("unsupported processing request type %T", message)
	}
}

func (state *streamState) handleHeaders(ctx context.Context, direction Direction, message *extprocv3.HttpHeaders, attributes map[string]*structpb.Struct) (*extprocv3.ProcessingResponse, bool, error) {
	if message == nil {
		return nil, false, fmt.Errorf("%s headers are missing", direction)
	}
	if err := state.recordHeaderArrival(direction); err != nil {
		return nil, false, err
	}
	headers, transactionID, limitDecision, err := state.decodeHeaders(message.GetHeaders())
	if err != nil {
		return nil, false, err
	}
	if err := state.recordRequestHeaders(direction, headers, transactionID, attributes); err != nil {
		return nil, false, err
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
	state.recordHeaderProgress(direction, headers, message.GetEndOfStream())
	return state.responseForDecision(headerPhase(direction), decision, state.responseDone)
}

func (state *streamState) recordHeaderArrival(direction Direction) error {
	if direction == DirectionRequest {
		if state.requestHeadersSeen {
			return fmt.Errorf("duplicate request headers")
		}
		state.requestHeadersSeen = true
		return nil
	}
	if !state.requestHeadersSeen {
		return fmt.Errorf("response headers arrived before request headers")
	}
	if state.responseHeadersSeen {
		return fmt.Errorf("duplicate response headers")
	}
	// The arrival of upstream response headers is only an ordering boundary.
	// A response becomes committed for this adapter only after Process sends
	// the matching CONTINUE response successfully.
	state.responseHeadersSeen = true
	return nil
}

func (state *streamState) recordRequestHeaders(direction Direction, headers []Header, transactionID string, attributes map[string]*structpb.Struct) error {
	if direction != DirectionRequest {
		return nil
	}
	if transactionID != "" {
		state.transactionID = transactionID
	}
	metadata, err := requestMetadataFromEnvoy(headers, attributes)
	if err != nil {
		return err
	}
	state.request = metadata
	return nil
}

func (state *streamState) recordHeaderProgress(direction Direction, headers []Header, endOfStream bool) {
	if direction == DirectionRequest {
		state.summary.RequestHeaderCount += uint64(len(headers))
		state.requestDone = endOfStream
		return
	}
	state.responseStatus = responseStatusFromHeaders(headers)
	state.summary.ResponseHeaderCount += uint64(len(headers))
	state.responseDone = endOfStream
}

func (state *streamState) handleBody(ctx context.Context, direction Direction, message *extprocv3.HttpBody) (*extprocv3.ProcessingResponse, bool, error) {
	if message == nil {
		return nil, false, fmt.Errorf("%s body is missing", direction)
	}
	if err := state.validateBodyOrder(direction); err != nil {
		return nil, false, err
	}
	if err := state.ensureTransaction(ctx); err != nil {
		return nil, false, err
	}

	body := message.GetBody()
	decision := state.bodyLimitDecision(direction, len(body))
	if decision.Action == ActionAllow {
		processedDecision, err := state.processBody(ctx, direction, body, message.GetEndOfStream())
		if err != nil {
			return nil, false, err
		}
		decision = processedDecision
	}

	state.recordBodyProgress(direction, len(body), message.GetEndOfStream())
	return state.responseForDecision(bodyPhase(direction), decision, state.responseDone)
}

func (state *streamState) validateBodyOrder(direction Direction) error {
	if direction == DirectionRequest {
		if !state.requestHeadersSeen || state.requestDone {
			return fmt.Errorf("request body violates stream order")
		}
		return nil
	}
	if !state.responseHeadersSeen || state.responseDone {
		return fmt.Errorf("response body violates stream order")
	}
	return nil
}

func (state *streamState) bodyLimitDecision(direction Direction, bodyLength int) Decision {
	if bodyLength > state.config.MaxBodyChunkBytes {
		return payloadTooLargeDecision()
	}
	if direction == DirectionRequest && state.summary.RequestBodyBytes+int64(bodyLength) > state.config.MaxRequestBodyBytes {
		return payloadTooLargeDecision()
	}
	if direction == DirectionResponse && state.summary.ResponseBodyBytes+int64(bodyLength) > state.config.MaxResponseBodyBytes {
		return payloadTooLargeDecision()
	}
	return allowDecision()
}

func payloadTooLargeDecision() Decision {
	return Decision{Action: ActionDeny, Status: int(typev3.StatusCode_PayloadTooLarge)}
}

func (state *streamState) recordBodyProgress(direction Direction, bodyLength int, endOfStream bool) {
	if direction == DirectionRequest {
		state.summary.RequestBodyChunks++
		state.summary.RequestBodyBytes += int64(bodyLength)
		state.requestDone = endOfStream
		return
	}
	state.summary.ResponseBodyChunks++
	state.summary.ResponseBodyBytes += int64(bodyLength)
	state.responseDone = endOfStream
}

func (state *streamState) handleTrailers(ctx context.Context, direction Direction, message *extprocv3.HttpTrailers) (*extprocv3.ProcessingResponse, bool, error) {
	if message == nil {
		return nil, false, fmt.Errorf("%s trailers are missing", direction)
	}
	if direction == DirectionRequest {
		if !state.requestHeadersSeen || state.requestDone {
			return nil, false, fmt.Errorf("request trailers violate stream order")
		}
	} else if !state.responseHeadersSeen || state.responseDone {
		return nil, false, fmt.Errorf("response trailers violate stream order")
	}
	if err := state.ensureTransaction(ctx); err != nil {
		return nil, false, err
	}
	// Trailers are the body end-of-stream signal when the preceding streamed
	// body chunks did not carry end_of_stream. The Common runtime has no
	// separate trailer API, so finish the corresponding incremental body
	// lifecycle with an empty final chunk. Trailer fields themselves are never
	// retained or converted into synthetic body content.
	decision, err := state.processBody(ctx, direction, nil, true)
	if err != nil {
		return nil, false, err
	}
	if direction == DirectionRequest {
		state.requestDone = true
	} else {
		state.responseDone = true
	}
	return state.responseForDecision(trailerPhase(direction), decision, state.responseDone)
}

func (state *streamState) ensureTransaction(ctx context.Context) error {
	if state.transaction != nil {
		return nil
	}
	engineContext, cancel := context.WithTimeout(ctx, state.config.engineTimeout())
	defer cancel()
	transaction, err := state.engine.Open(engineContext, StreamMetadata{
		TransactionID: state.transactionID,
		Request:       state.request,
	})
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
	if provider, ok := state.transaction.(TransactionIDProvider); ok {
		if transactionID := provider.TransactionID(); transactionID != "" {
			state.transactionID = transactionID
		}
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
		return nil, "", requestHeadersTooLargeDecision(), nil
	}
	values := headerMap.GetHeaders()
	if len(values) > state.config.MaxHeaderCount {
		return nil, "", requestHeadersTooLargeDecision(), nil
	}
	return state.decodeHeaderValues(values)
}

func requestHeadersTooLargeDecision() Decision {
	return Decision{Action: ActionDeny, Status: int(typev3.StatusCode_RequestHeaderFieldsTooLarge)}
}

func (state *streamState) decodeHeaderValues(values []*corev3.HeaderValue) ([]Header, string, Decision, error) {
	headers := make([]Header, 0, len(values))
	total := 0
	transactionID := ""
	for _, value := range values {
		header, updatedTotal, updatedTransactionID, decision, err := state.decodeHeader(value, total, transactionID)
		if err != nil {
			return nil, "", Decision{}, err
		}
		if decision.Action != ActionAllow {
			return nil, "", decision, nil
		}
		total = updatedTotal
		transactionID = updatedTransactionID
		headers = append(headers, header)
	}
	return headers, transactionID, allowDecision(), nil
}

func (state *streamState) decodeHeader(value *corev3.HeaderValue, total int, transactionID string) (Header, int, string, Decision, error) {
	if value == nil {
		return Header{}, 0, "", Decision{}, fmt.Errorf("nil header")
	}
	name := value.GetKey()
	body := headerValueBytes(value)
	if len(name) > state.config.MaxHeaderNameBytes || len(body) > state.config.MaxHeaderValueBytes {
		return Header{}, 0, "", requestHeadersTooLargeDecision(), nil
	}
	updatedTotal := total + len(name) + len(body)
	if updatedTotal > state.config.MaxTotalHeaderBytes {
		return Header{}, 0, "", requestHeadersTooLargeDecision(), nil
	}
	if transactionID == "" && strings.EqualFold(name, state.config.TransactionIDHeader) {
		transactionID = boundedTransactionID(body)
	}
	return Header{Name: name, Value: body}, updatedTotal, transactionID, allowDecision(), nil
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

func responseStatusFromHeaders(headers []Header) int {
	for _, header := range headers {
		if header.Name != ":status" {
			continue
		}
		status, err := strconv.Atoi(string(header.Value))
		if err == nil && status >= 100 && status <= 599 {
			return status
		}
		return 0
	}
	return 0
}

// requestMetadataFromEnvoy maps only Envoy-provided pseudo headers and the
// explicit request_attributes requested in the checked-in filter config. It
// accepts absent fields so the transport-only engine remains testable; the
// Common bridge validates that its required metadata is actually present and
// never silently substitutes the gRPC peer endpoint.
func requestMetadataFromEnvoy(headers []Header, attributes map[string]*structpb.Struct) (RequestMetadata, error) {
	metadata := RequestMetadata{}
	authority := ""
	host := ""
	authoritySeen := false
	hostSeen := false
	for _, header := range headers {
		name := strings.ToLower(header.Name)
		value, err := boundedMetadataText(header.Value, name)
		if err != nil {
			return RequestMetadata{}, err
		}
		switch name {
		case ":method":
			metadata.Method = value
		case ":path":
			metadata.URI = value
		case ":authority":
			if authoritySeen {
				return RequestMetadata{}, fmt.Errorf("Envoy request contains multiple :authority headers")
			}
			authority = value
			authoritySeen = true
		case "host":
			if hostSeen {
				return RequestMetadata{}, fmt.Errorf("Envoy request contains multiple Host headers")
			}
			host = value
			hostSeen = true
		}
	}
	if authoritySeen && hostSeen && !strings.EqualFold(authority, host) {
		return RequestMetadata{}, fmt.Errorf("Envoy :authority and Host headers disagree")
	}
	if authoritySeen {
		metadata.Hostname = authority
	} else if hostSeen {
		metadata.Hostname = host
	}
	textAssignments := []struct {
		attribute string
		assign    func(string)
	}{
		{"request.protocol", func(value string) { metadata.Protocol = value }},
		{"source.address", func(value string) { metadata.ClientAddress = envoyEndpointAddress(value) }},
		{"destination.address", func(value string) { metadata.ServerAddress = envoyEndpointAddress(value) }},
	}
	for _, assignment := range textAssignments {
		if err := assignEnvoyTextAttribute(attributes, assignment.attribute, assignment.assign); err != nil {
			return RequestMetadata{}, err
		}
	}

	portAssignments := []struct {
		attribute string
		assign    func(int)
	}{
		{"source.port", func(value int) { metadata.ClientPort = value }},
		{"destination.port", func(value int) { metadata.ServerPort = value }},
	}
	for _, assignment := range portAssignments {
		if err := assignEnvoyPortAttribute(attributes, assignment.attribute, assignment.assign); err != nil {
			return RequestMetadata{}, err
		}
	}
	return metadata, nil
}

func assignEnvoyTextAttribute(
	attributes map[string]*structpb.Struct,
	attribute string,
	assign func(string),
) error {
	value, found, err := envoyAttributeText(attributes, attribute)
	if err != nil {
		return err
	}
	if found {
		assign(value)
	}
	return nil
}

func assignEnvoyPortAttribute(
	attributes map[string]*structpb.Struct,
	attribute string,
	assign func(int),
) error {
	value, found, err := envoyAttributePort(attributes, attribute)
	if err != nil {
		return err
	}
	if found {
		assign(value)
	}
	return nil
}

// Envoy's standard address attributes may be rendered as host:port. The port
// is requested separately and remains authoritative, so strip only a valid
// socket-address wrapper before passing the host string to libmodsecurity.
// A bare IPv6 address or an unparseable host is retained exactly as Envoy sent
// it rather than guessed at.
func envoyEndpointAddress(value string) string {
	if host, _, err := net.SplitHostPort(value); err == nil {
		return host
	}
	return value
}

func boundedMetadataText(value []byte, field string) (string, error) {
	if len(value) > 4096 {
		return "", fmt.Errorf("%s exceeds metadata limit", field)
	}
	text := string(value)
	if strings.IndexByte(text, 0) >= 0 {
		return "", fmt.Errorf("%s contains a NUL byte", field)
	}
	return text, nil
}

func envoyAttributeText(attributes map[string]*structpb.Struct, name string) (string, bool, error) {
	value, found := envoyAttributeValue(attributes, name)
	if !found {
		return "", false, nil
	}
	if value == nil {
		return "", true, fmt.Errorf("Envoy attribute %s is empty", name)
	}
	kind, ok := value.GetKind().(*structpb.Value_StringValue)
	if !ok {
		return "", true, fmt.Errorf("Envoy attribute %s is not a string", name)
	}
	if len(kind.StringValue) > 4096 || strings.IndexByte(kind.StringValue, 0) >= 0 {
		return "", true, fmt.Errorf("Envoy attribute %s is invalid", name)
	}
	return kind.StringValue, true, nil
}

func envoyAttributePort(attributes map[string]*structpb.Struct, name string) (int, bool, error) {
	value, found := envoyAttributeValue(attributes, name)
	if !found {
		return 0, false, nil
	}
	if value == nil {
		return 0, true, fmt.Errorf("Envoy attribute %s is empty", name)
	}
	var parsed int64
	switch kind := value.GetKind().(type) {
	case *structpb.Value_NumberValue:
		if kind.NumberValue != float64(int64(kind.NumberValue)) {
			return 0, true, fmt.Errorf("Envoy attribute %s is not an integer", name)
		}
		parsed = int64(kind.NumberValue)
	case *structpb.Value_StringValue:
		var err error
		parsed, err = strconv.ParseInt(kind.StringValue, 10, 32)
		if err != nil {
			return 0, true, fmt.Errorf("Envoy attribute %s is not a port: %w", name, err)
		}
	default:
		return 0, true, fmt.Errorf("Envoy attribute %s is not a number", name)
	}
	if parsed < 0 || parsed > 65535 {
		return 0, true, fmt.Errorf("Envoy attribute %s is outside the port range", name)
	}
	return int(parsed), true, nil
}

// envoyAttributeValue supports the standard ext_proc namespace and the direct
// form used by small protobuf fixtures. The actual Envoy representation groups
// selected attributes under envoy.filters.http.ext_proc.
func envoyAttributeValue(attributes map[string]*structpb.Struct, name string) (*structpb.Value, bool) {
	for _, attributeSet := range attributes {
		if attributeSet == nil {
			continue
		}
		if value, found := attributeSet.GetFields()[name]; found {
			return value, true
		}
	}
	if direct, found := attributes[name]; found && direct != nil {
		if value, found := direct.GetFields()["value"]; found {
			return value, true
		}
	}
	return nil, false
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

func (state *streamState) responseForDecision(phase processingPhase, decision Decision, responseDone bool) (*extprocv3.ProcessingResponse, bool, error) {
	if decision.disruptive() {
		if !state.responseCommitted {
			state.immediateResponse = true
			state.pendingHostAction = immediateHostAction(decision)
			return immediateResponse(decision), true, nil
		}
		state.resolveLateAction()
		if state.summary.LateAction == LateActionLogged && state.responseStatus >= 100 && state.responseStatus <= 599 {
			state.pendingHostAction = &HostAction{
				Action:          AppliedActionLogOnly,
				VisibleStatus:   state.responseStatus,
				TransportResult: "log_only",
			}
		}
	}
	return continueResponse(phase), responseDone, nil
}

func immediateHostAction(decision Decision) *HostAction {
	action := AppliedActionDeny
	if decision.Action == ActionRedirect {
		action = AppliedActionRedirect
	}
	return &HostAction{
		Action:          action,
		VisibleStatus:   decision.Status,
		TransportResult: "http_status",
	}
}

// markResponseCommittedAfterSuccessfulContinue records the earliest point at
// which this service has permitted Envoy to continue a response downstream.
// It deliberately runs after stream.Send succeeds: a locally constructed
// HeadersResponse or a failed gRPC send cannot establish this boundary.
func (state *streamState) markResponseCommittedAfterSuccessfulContinue(ctx context.Context, request *extprocv3.ProcessingRequest, response *extprocv3.ProcessingResponse) error {
	if state == nil || state.responseCommitted || request == nil || response == nil {
		return nil
	}
	if request.GetResponseHeaders() == nil {
		return nil
	}
	headers := response.GetResponseHeaders()
	if headers == nil || headers.GetResponse() == nil || headers.GetResponse().GetStatus() != extprocv3.CommonResponse_CONTINUE {
		return nil
	}
	if committer, ok := state.transaction.(ResponseCommitter); ok {
		engineContext, cancel := context.WithTimeout(ctx, state.config.engineTimeout())
		defer cancel()
		if err := committer.MarkResponseCommitted(engineContext); err != nil {
			return fmt.Errorf("mark Common response commit: %w", err)
		}
	}
	state.responseCommitted = true
	return nil
}

func (state *streamState) recordHostActionAfterSuccessfulResponse(ctx context.Context) error {
	if state == nil || state.pendingHostAction == nil {
		return nil
	}
	recorder, ok := state.transaction.(HostActionRecorder)
	if !ok {
		state.pendingHostAction = nil
		return nil
	}
	engineContext, cancel := context.WithTimeout(ctx, state.config.engineTimeout())
	defer cancel()
	if err := recorder.RecordHostAction(engineContext, *state.pendingHostAction); err != nil {
		return fmt.Errorf("record Common host action: %w", err)
	}
	state.pendingHostAction = nil
	return nil
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

func trailerPhase(direction Direction) processingPhase {
	if direction == DirectionRequest {
		return phaseRequestTrailers
	}
	return phaseResponseTrailers
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

func (state *streamState) close(reason CloseReason) error {
	if state.closed {
		return nil
	}
	state.closed = true
	var cleanupErr error
	state.summary.TransactionID = state.transactionID
	state.summary.CloseReason = reason
	if state.transaction != nil {
		cleanupContext, cancel := context.WithTimeout(context.Background(), state.config.cleanupTimeout())
		defer cancel()
		state.transaction.Close(cleanupContext, state.summary)
		if reporter, ok := state.transaction.(CleanupFailureReporter); ok {
			if err := reporter.CleanupFailure(); err != nil {
				cleanupErr = err
			}
		}
	}
	observerErr := state.observer.Record(state.summary)
	if cleanupErr != nil {
		if observerErr != nil {
			return fmt.Errorf("transaction cleanup: %w; metadata evidence: %v", cleanupErr, observerErr)
		}
		return cleanupErr
	}
	return observerErr
}
