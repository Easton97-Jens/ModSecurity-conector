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
	CloseProcessorError    CloseReason = "processor_error"
)

// Engine receives only incremental data. The production libmodsecurity build
// installs CommonRuntimeEngine; PassthroughEngine remains for protobuf/unit
// development without CGo linkage.
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

func (passthroughTransaction) Close(context.Context, Summary) {}

// Service implements Envoy's official ext_proc ExternalProcessor gRPC service.
type Service struct {
	extprocv3.UnimplementedExternalProcessorServer

	config   Config
	engine   Engine
	observer Observer
	active   sync.WaitGroup
}

func NewService(config Config, engine Engine) (*Service, error) {
	return NewServiceWithObserver(config, engine, discardObserver{})
}

// NewServiceWithObserver constructs a service with an optional completion
// observer. A nil observer is equivalent to a discard observer, which keeps
// the existing unit-test and library API safe for callers that do not need
// runtime evidence.
func NewServiceWithObserver(config Config, engine Engine, observer Observer) (*Service, error) {
	if err := config.Validate(); err != nil {
		return nil, err
	}
	if engine == nil {
		return nil, fmt.Errorf("ext_proc engine is required")
	}
	if observer == nil {
		observer = discardObserver{}
	}
	return &Service{config: config, engine: engine, observer: observer}, nil
}

// Process owns one Envoy ext_proc gRPC stream and therefore one independent
// transaction state. No state is shared across parallel streams.
func (service *Service) Process(stream extprocv3.ExternalProcessor_ProcessServer) (processErr error) {
	service.active.Add(1)
	defer service.active.Done()

	state := newStreamState(service.config, service.engine, service.observer)
	closeReason := ClosePeerEOF
	defer func() {
		if err := state.close(closeReason); err != nil && processErr == nil {
			processErr = status.Errorf(codes.Internal, "ext_proc metadata evidence: %v", err)
		}
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
			if err := state.markResponseCommittedAfterSuccessfulContinue(stream.Context(), request, response); err != nil {
				closeReason = CloseProcessorError
				return status.Errorf(codes.Internal, "ext_proc response commit bookkeeping failed: %v", err)
			}
			if err := state.recordHostActionAfterSuccessfulResponse(stream.Context()); err != nil {
				closeReason = CloseProcessorError
				return status.Errorf(codes.Internal, "ext_proc host action evidence failed: %v", err)
			}
		}
		if terminal && !request.GetObservabilityMode() {
			closeReason = state.completionReason()
			return nil
		}
	}
}

type streamState struct {
	config   Config
	engine   Engine
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

func newStreamState(config Config, engine Engine, observer Observer) *streamState {
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
		// The arrival of upstream response headers is only an ordering boundary.
		// A response becomes committed for this adapter only after Process sends
		// the matching CONTINUE response successfully.
		state.responseHeadersSeen = true
	}

	headers, transactionID, limitDecision, err := state.decodeHeaders(message.GetHeaders())
	if err != nil {
		return nil, false, err
	}
	if direction == DirectionRequest && transactionID != "" {
		state.transactionID = transactionID
	}
	if direction == DirectionRequest {
		metadata, err := requestMetadataFromEnvoy(headers, attributes)
		if err != nil {
			return nil, false, err
		}
		state.request = metadata
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
		state.responseStatus = responseStatusFromHeaders(headers)
		state.summary.ResponseHeaderCount += uint64(len(headers))
		state.responseDone = message.GetEndOfStream()
	}
	return state.responseForDecision(headerPhase(direction), decision, state.responseDone)
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
	return state.responseForDecision(bodyPhase(direction), decision, state.responseDone)
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
			metadata.Hostname = value
		case "host":
			if metadata.Hostname == "" {
				metadata.Hostname = value
			}
		}
	}
	if value, found, err := envoyAttributeText(attributes, "request.protocol"); err != nil {
		return RequestMetadata{}, err
	} else if found {
		metadata.Protocol = value
	}
	if value, found, err := envoyAttributeText(attributes, "source.address"); err != nil {
		return RequestMetadata{}, err
	} else if found {
		metadata.ClientAddress = envoyEndpointAddress(value)
	}
	if value, found, err := envoyAttributePort(attributes, "source.port"); err != nil {
		return RequestMetadata{}, err
	} else if found {
		metadata.ClientPort = value
	}
	if value, found, err := envoyAttributeText(attributes, "destination.address"); err != nil {
		return RequestMetadata{}, err
	} else if found {
		metadata.ServerAddress = envoyEndpointAddress(value)
	}
	if value, found, err := envoyAttributePort(attributes, "destination.port"); err != nil {
		return RequestMetadata{}, err
	} else if found {
		metadata.ServerPort = value
	}
	return metadata, nil
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
	state.summary.TransactionID = state.transactionID
	state.summary.CloseReason = reason
	if state.transaction != nil {
		cleanupContext, cancel := context.WithTimeout(context.Background(), state.config.cleanupTimeout())
		defer cancel()
		state.transaction.Close(cleanupContext, state.summary)
	}
	return state.observer.Record(state.summary)
}
