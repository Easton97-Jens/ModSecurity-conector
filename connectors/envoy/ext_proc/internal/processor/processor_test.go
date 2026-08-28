package processor

import (
	"context"
	"errors"
	"io"
	"strings"
	"testing"

	corev3 "github.com/envoyproxy/go-control-plane/envoy/config/core/v3"
	extprocv3 "github.com/envoyproxy/go-control-plane/envoy/service/ext_proc/v3"
	typev3 "github.com/envoyproxy/go-control-plane/envoy/type/v3"
	"google.golang.org/grpc/metadata"
	"google.golang.org/protobuf/types/known/structpb"
)

func TestProcessStreamsChunksAndCleansUpAtResponseEOS(t *testing.T) {
	transaction := &recordingTransaction{}
	service := newTestService(t, transaction, LateActionSafe)
	stream := &fakeProcessStream{contextFactory: testStreamContext(context.Background()), receive: []receiveResult{
		{request: requestHeaders(false)},
		{request: requestBody([]byte("one"), false)},
		{request: requestBody([]byte("two"), true)},
		{request: responseHeaders(false)},
		{request: responseBody([]byte("result"), true)},
	}}

	if err := service.Process(stream); err != nil {
		t.Fatalf("Process() error = %v", err)
	}
	if got, want := len(stream.sent), 5; got != want {
		t.Fatalf("sent responses = %d, want %d", got, want)
	}
	if stream.sent[0].GetRequestHeaders() == nil || stream.sent[1].GetRequestBody() == nil || stream.sent[3].GetResponseHeaders() == nil || stream.sent[4].GetResponseBody() == nil {
		t.Fatalf("responses did not match streamed request phases")
	}
	if got, want := transaction.requestBodyLengths, []int{3, 3}; !sameInts(got, want) {
		t.Fatalf("request chunk lengths = %v, want %v", got, want)
	}
	if got, want := transaction.responseBodyLengths, []int{6}; !sameInts(got, want) {
		t.Fatalf("response chunk lengths = %v, want %v", got, want)
	}
	if len(transaction.closed) != 1 {
		t.Fatalf("close calls = %d, want 1", len(transaction.closed))
	}
	summary := transaction.closed[0]
	if summary.CloseReason != CloseResponseEOS || summary.RequestBodyBytes != 6 || summary.ResponseBodyBytes != 6 {
		t.Fatalf("unexpected cleanup summary: %#v", summary)
	}
}

func TestRequestDenyUsesImmediateResponseBeforeResponseHeaders(t *testing.T) {
	transaction := &recordingTransaction{
		headerDecision: func(direction Direction) Decision {
			if direction == DirectionRequest {
				return Decision{Action: ActionDeny, Status: 403}
			}
			return allowDecision()
		},
	}
	service := newTestService(t, transaction, LateActionSafe)
	stream := &fakeProcessStream{contextFactory: testStreamContext(context.Background()), receive: []receiveResult{{request: requestHeaders(false)}}}

	if err := service.Process(stream); err != nil {
		t.Fatalf("Process() error = %v", err)
	}
	if got, want := len(stream.sent), 1; got != want {
		t.Fatalf("sent responses = %d, want %d", got, want)
	}
	if response := stream.sent[0].GetImmediateResponse(); response == nil || int(response.GetStatus().GetCode()) != 403 {
		t.Fatalf("expected a request immediate 403 response, got %#v", stream.sent[0])
	}
	if transaction.closed[0].CloseReason != CloseImmediateResponse {
		t.Fatalf("close reason = %q, want %q", transaction.closed[0].CloseReason, CloseImmediateResponse)
	}
	if got, want := transaction.hostActions, []HostAction{{
		Action: AppliedActionDeny, VisibleStatus: 403, TransportResult: "http_status",
	}}; !sameHostActions(got, want) {
		t.Fatalf("host actions = %#v, want %#v", got, want)
	}
}

func TestRequestBodyLimitUses413WithoutEngineBodyDispatch(t *testing.T) {
	transaction := &recordingTransaction{}
	config := testConfig(LateActionSafe)
	config.MaxRequestBodyBytes = 4
	service, err := NewService(config, recordingEngine{transaction: transaction})
	if err != nil {
		t.Fatalf("NewService() error = %v", err)
	}
	stream := &fakeProcessStream{contextFactory: testStreamContext(context.Background()), receive: []receiveResult{
		{request: requestHeaders(false)},
		{request: requestBody([]byte("12345"), true)},
	}}

	if err := service.Process(stream); err != nil {
		t.Fatalf("Process() error = %v", err)
	}
	if got, want := len(stream.sent), 2; got != want {
		t.Fatalf("sent responses = %d, want %d", got, want)
	}
	if response := stream.sent[1].GetImmediateResponse(); response == nil || int(response.GetStatus().GetCode()) != 413 {
		t.Fatalf("expected a request-body immediate 413 response, got %#v", stream.sent[1])
	}
	if got := transaction.requestBodyLengths; len(got) != 0 {
		t.Fatalf("over-limit request body reached engine dispatch: %v", got)
	}
	if len(transaction.closed) != 1 {
		t.Fatalf("close calls = %d, want 1", len(transaction.closed))
	}
	summary := transaction.closed[0]
	if summary.CloseReason != CloseImmediateResponse || summary.RequestBodyChunks != 1 || summary.RequestBodyBytes != 5 {
		t.Fatalf("unexpected body-limit cleanup summary: %#v", summary)
	}
	if got, want := transaction.hostActions, []HostAction{{
		Action: AppliedActionDeny, VisibleStatus: 413, TransportResult: "http_status",
	}}; !sameHostActions(got, want) {
		t.Fatalf("host actions = %#v, want %#v", got, want)
	}
}

func TestRedirectDecisionRejectsUnsafeHeaderTargets(t *testing.T) {
	for _, target := range []string{
		"https://example.test/next\r\nX-Injected: yes",
		"https://example.test/next\x1f",
		"https://example.test/next\x7f",
		strings.Repeat("a", maxRedirectURLBytes+1),
	} {
		decision := normalizeDecision(Decision{Action: ActionRedirect, Status: 302, RedirectURL: target})
		if decision.Action != ActionDeny || decision.Status != int(typev3.StatusCode_Forbidden) {
			t.Fatalf("unsafe redirect %q normalized to %#v, want deny/403", target, decision)
		}
		if response := immediateResponse(decision); response.GetImmediateResponse().GetHeaders() != nil {
			t.Fatalf("rejected redirect retained a Location mutation: %#v", response)
		}
	}
}

func TestResponseHeaderDenyUsesImmediateResponseBeforeCommit(t *testing.T) {
	transaction := &recordingTransaction{
		headerDecision: func(direction Direction) Decision {
			if direction == DirectionResponse {
				return Decision{Action: ActionDeny, Status: 403}
			}
			return allowDecision()
		},
	}
	service := newTestService(t, transaction, LateActionSafe)
	stream := &fakeProcessStream{contextFactory: testStreamContext(context.Background()), receive: []receiveResult{
		{request: requestHeaders(true)},
		{request: responseHeaders(false)},
	}}

	if err := service.Process(stream); err != nil {
		t.Fatalf("Process() error = %v", err)
	}
	if got, want := len(stream.sent), 2; got != want {
		t.Fatalf("sent responses = %d, want %d", got, want)
	}
	if stream.sent[0].GetRequestHeaders() == nil {
		t.Fatalf("request headers did not receive a continue response: %#v", stream.sent[0])
	}
	if response := stream.sent[1].GetImmediateResponse(); response == nil || int(response.GetStatus().GetCode()) != 403 {
		t.Fatalf("expected a response-header immediate 403 response, got %#v", stream.sent[1])
	}
	if len(transaction.closed) != 1 || transaction.closed[0].CloseReason != CloseImmediateResponse {
		t.Fatalf("unexpected cleanup after response-header denial: %#v", transaction.closed)
	}
	if len(transaction.hostActions) != 1 || transaction.hostActions[0].Action != AppliedActionDeny {
		t.Fatalf("response-header host action = %#v", transaction.hostActions)
	}
}

func TestResponseHeaderRedirectUsesImmediateResponseBeforeCommit(t *testing.T) {
	transaction := &recordingTransaction{
		headerDecision: func(direction Direction) Decision {
			if direction == DirectionResponse {
				return Decision{Action: ActionRedirect, Status: 302, RedirectURL: "/msconnector-p3-redirect-target"}
			}
			return allowDecision()
		},
	}
	service := newTestService(t, transaction, LateActionSafe)
	stream := &fakeProcessStream{contextFactory: testStreamContext(context.Background()), receive: []receiveResult{
		{request: requestHeaders(true)},
		{request: responseHeaders(false)},
	}}

	if err := service.Process(stream); err != nil {
		t.Fatalf("Process() error = %v", err)
	}
	if got, want := len(stream.sent), 2; got != want {
		t.Fatalf("sent responses = %d, want %d", got, want)
	}
	response := stream.sent[1].GetImmediateResponse()
	if response == nil || int(response.GetStatus().GetCode()) != 302 {
		t.Fatalf("expected a response-header immediate 302 response, got %#v", stream.sent[1])
	}
	headers := response.GetHeaders().GetSetHeaders()
	if len(headers) != 1 || headers[0].GetHeader().GetKey() != "location" || string(headers[0].GetHeader().GetRawValue()) != "/msconnector-p3-redirect-target" || headers[0].GetHeader().GetValue() != "" || headers[0].GetAppendAction() != corev3.HeaderValueOption_OVERWRITE_IF_EXISTS_OR_ADD {
		t.Fatalf("response-header redirect location = %#v", headers)
	}
	if len(transaction.closed) != 1 || transaction.closed[0].CloseReason != CloseImmediateResponse {
		t.Fatalf("unexpected cleanup after response-header redirect: %#v", transaction.closed)
	}
	if got, want := transaction.hostActions, []HostAction{{
		Action: AppliedActionRedirect, VisibleStatus: 302, TransportResult: "http_status",
	}}; !sameHostActions(got, want) {
		t.Fatalf("response-header redirect host action = %#v", got)
	}
}

func TestExplicitEmptyRequestDoesNotSynthesizeBody(t *testing.T) {
	transaction := &recordingTransaction{}
	service := newTestService(t, transaction, LateActionSafe)
	stream := &fakeProcessStream{contextFactory: testStreamContext(context.Background()), receive: []receiveResult{
		{request: requestHeadersWithExplicitEmptyBody()},
		{request: responseHeaders(false)},
	}}

	if err := service.Process(stream); err != nil {
		t.Fatalf("Process() error = %v", err)
	}
	if got, want := len(stream.sent), 2; got != want {
		t.Fatalf("sent responses = %d, want %d", got, want)
	}
	if stream.sent[0].GetRequestHeaders() == nil {
		t.Fatalf("request headers did not receive a continue response: %#v", stream.sent[0])
	}
	if stream.sent[1].GetResponseHeaders() == nil {
		t.Fatalf("response headers unexpectedly became an immediate response: %#v", stream.sent[1])
	}
	if got := transaction.requestBodyLengths; len(got) != 0 {
		t.Fatalf("explicitly empty request synthesized body chunks = %v", got)
	}
	if len(transaction.closed) != 1 || transaction.closed[0].CloseReason != ClosePeerEOF {
		t.Fatalf("unexpected cleanup after explicit empty request: %#v", transaction.closed)
	}
	if len(transaction.hostActions) != 0 {
		t.Fatalf("explicitly empty request recorded host actions: %#v", transaction.hostActions)
	}
}

func TestFailedImmediateResponseDoesNotRecordHostAction(t *testing.T) {
	transaction := &recordingTransaction{
		headerDecision: func(direction Direction) Decision {
			if direction == DirectionRequest {
				return Decision{Action: ActionDeny, Status: 403}
			}
			return allowDecision()
		},
	}
	service := newTestService(t, transaction, LateActionSafe)
	stream := &fakeProcessStream{
		contextFactory: testStreamContext(context.Background()),
		sendErr:        io.ErrClosedPipe,
		receive:        []receiveResult{{request: requestHeaders(false)}},
	}
	if err := service.Process(stream); err == nil {
		t.Fatal("Process() accepted a failed ImmediateResponse send")
	}
	if len(transaction.hostActions) != 0 {
		t.Fatalf("failed send recorded host action: %#v", transaction.hostActions)
	}
}

func TestResponseCommitRequiresSuccessfulResponseHeaderContinue(t *testing.T) {
	transaction := &recordingTransaction{}
	state := newStreamState(testConfig(LateActionSafe), recordingEngine{transaction: transaction}, discardObserver{})

	requestHeaderResponse, terminal, err := state.handle(context.Background(), requestHeaders(true))
	if err != nil || terminal || requestHeaderResponse.GetRequestHeaders() == nil {
		t.Fatalf("request header handling = response=%#v terminal=%t err=%v", requestHeaderResponse, terminal, err)
	}
	if err := state.markResponseCommittedAfterSuccessfulContinue(context.Background(), requestHeaders(true), requestHeaderResponse); err != nil {
		t.Fatalf("mark request response committed: %v", err)
	}
	if state.responseCommitted {
		t.Fatal("request-header continue must not commit the response")
	}

	upstreamHeaders := responseHeaders(false)
	responseHeaderResponse, terminal, err := state.handle(context.Background(), upstreamHeaders)
	if err != nil || terminal || responseHeaderResponse.GetResponseHeaders() == nil {
		t.Fatalf("response header handling = response=%#v terminal=%t err=%v", responseHeaderResponse, terminal, err)
	}
	if state.responseCommitted {
		t.Fatal("constructing a response-header continue must not commit the response")
	}
	if err := state.markResponseCommittedAfterSuccessfulContinue(context.Background(), upstreamHeaders, responseHeaderResponse); err != nil {
		t.Fatalf("mark response response committed: %v", err)
	}
	if !state.responseCommitted {
		t.Fatal("successful response-header continue must commit the response boundary")
	}
}

func TestStrictPolicyIsRejectedBeforeStreamAdmission(t *testing.T) {
	_, err := NewService(testConfig(LateActionStrict), recordingEngine{transaction: &recordingTransaction{}})
	if err == nil || !strings.Contains(err.Error(), "proven strict post-commit host action") {
		t.Fatalf("NewService() error = %v, want strict admission rejection", err)
	}
}

func TestLatePolicyAdmissionDelegatesToRuleEvaluatingEngine(t *testing.T) {
	engine := &policyValidationEngine{
		recordingEngine: recordingEngine{transaction: &recordingTransaction{}},
		rejection:       errors.New("phase4_mode=safe cannot prove strict"),
	}
	_, err := NewService(testConfig(LateActionStrict), engine)
	if err == nil || !strings.Contains(err.Error(), "phase4_mode=safe") {
		t.Fatalf("NewService() error = %v, want runtime policy rejection", err)
	}
	if got, want := engine.policies, []LateActionPolicy{LateActionStrict}; !sameLateActionPolicies(got, want) {
		t.Fatalf("validated policies = %v, want %v", got, want)
	}

	engine.rejection = nil
	if _, err := NewService(testConfig(LateActionSafe), engine); err != nil {
		t.Fatalf("NewService() safe policy error = %v", err)
	}
	if got, want := engine.policies, []LateActionPolicy{LateActionStrict, LateActionSafe}; !sameLateActionPolicies(got, want) {
		t.Fatalf("validated policies = %v, want %v", got, want)
	}
}

func TestCancellationCleansUpWithoutAttributingTheHTTPReset(t *testing.T) {
	transaction := &recordingTransaction{}
	service := newTestService(t, transaction, LateActionSafe)
	contextValue, cancel := context.WithCancel(context.Background())
	stream := &fakeProcessStream{contextFactory: testStreamContext(contextValue), cancel: cancel, receive: []receiveResult{
		{request: requestHeaders(false)},
		{cancel: true, err: context.Canceled},
	}}

	if err := service.Process(stream); err != nil {
		t.Fatalf("Process() error = %v", err)
	}
	if len(transaction.closed) != 1 {
		t.Fatalf("close calls = %d, want 1", len(transaction.closed))
	}
	if got, want := transaction.closed[0].CloseReason, CloseContextCanceled; got != want {
		t.Fatalf("close reason = %q, want %q", got, want)
	}
}

func TestPeerEOFCleansUpWithoutAttributingTheHTTPReset(t *testing.T) {
	transaction := &recordingTransaction{}
	service := newTestService(t, transaction, LateActionSafe)
	stream := &fakeProcessStream{contextFactory: testStreamContext(context.Background()), receive: []receiveResult{
		{request: requestHeaders(false)},
		{err: io.EOF},
	}}

	if err := service.Process(stream); err != nil {
		t.Fatalf("Process() error = %v", err)
	}
	if len(transaction.closed) != 1 {
		t.Fatalf("close calls = %d, want 1", len(transaction.closed))
	}
	if got, want := transaction.closed[0].CloseReason, ClosePeerEOF; got != want {
		t.Fatalf("close reason = %q, want %q", got, want)
	}
}

func TestTrailersFinalizeIncrementalBodiesAtEOS(t *testing.T) {
	transaction := &recordingTransaction{}
	service := newTestService(t, transaction, LateActionSafe)
	stream := &fakeProcessStream{contextFactory: testStreamContext(context.Background()), receive: []receiveResult{
		{request: requestHeaders(false)},
		{request: requestTrailers()},
		{request: responseHeaders(false)},
		{request: responseTrailers()},
	}}

	if err := service.Process(stream); err != nil {
		t.Fatalf("Process() error = %v", err)
	}
	if !sameInts(transaction.requestBodyLengths, []int{0}) {
		t.Fatalf("request trailer EOS body lengths = %v, want %v", transaction.requestBodyLengths, []int{0})
	}
	if !sameInts(transaction.responseBodyLengths, []int{0}) {
		t.Fatalf("response trailer EOS body lengths = %v, want %v", transaction.responseBodyLengths, []int{0})
	}
	if stream.sent[1].GetRequestTrailers() == nil {
		t.Fatalf("request trailer did not receive trailer response: %#v", stream.sent[1])
	}
	if stream.sent[3].GetResponseTrailers() == nil {
		t.Fatalf("response trailer did not receive trailer response: %#v", stream.sent[3])
	}
	if len(transaction.closed) != 1 || transaction.closed[0].CloseReason != CloseResponseEOS {
		t.Fatalf("trailer cleanup = %#v", transaction.closed)
	}
}

func TestRequestMetadataUsesEnvoyAttributesWithoutPeerInference(t *testing.T) {
	attributes, err := structpb.NewStruct(map[string]any{
		"request.protocol":    "HTTP/1.1",
		"source.address":      "192.0.2.10",
		"source.port":         45678,
		"destination.address": "198.51.100.7",
		"destination.port":    443,
	})
	if err != nil {
		t.Fatalf("NewStruct() error = %v", err)
	}
	metadata, err := requestMetadataFromEnvoy([]Header{
		{Name: ":method", Value: []byte("POST")},
		{Name: ":path", Value: []byte("/metadata")},
		{Name: ":authority", Value: []byte("example.test")},
	}, map[string]*structpb.Struct{"envoy.filters.http.ext_proc": attributes})
	if err != nil {
		t.Fatalf("requestMetadataFromEnvoy() error = %v", err)
	}
	if got, want := metadata, (RequestMetadata{
		Method: "POST", URI: "/metadata", Protocol: "HTTP/1.1", Hostname: "example.test",
		ClientAddress: "192.0.2.10", ClientPort: 45678,
		ServerAddress: "198.51.100.7", ServerPort: 443,
	}); got != want {
		t.Fatalf("metadata = %#v, want %#v", got, want)
	}
}

func TestRequestMetadataRejectsMismatchedAuthorityAndHost(t *testing.T) {
	authorityAndHost := func(authorityFirst bool) []Header {
		authority := Header{Name: ":authority", Value: []byte("trusted.example")}
		host := Header{Name: "Host", Value: []byte("attacker.example")}
		if authorityFirst {
			return []Header{authority, host}
		}
		return []Header{host, authority}
	}

	for name, headers := range map[string][]Header{
		"authority before Host": authorityAndHost(true),
		"Host before authority": authorityAndHost(false),
		"duplicate Host after matching Host": {
			{Name: ":authority", Value: []byte("trusted.example")},
			{Name: "Host", Value: []byte("trusted.example")},
			{Name: "Host", Value: []byte("attacker.example")},
		},
		"duplicate authority after matching authority": {
			{Name: ":authority", Value: []byte("trusted.example")},
			{Name: ":authority", Value: []byte("attacker.example")},
			{Name: "Host", Value: []byte("trusted.example")},
		},
	} {
		t.Run(name, func(t *testing.T) {
			if _, err := requestMetadataFromEnvoy(headers, map[string]*structpb.Struct{}); err == nil {
				t.Fatal("requestMetadataFromEnvoy() accepted mismatched :authority and Host")
			}
		})
	}
}

func TestRequestMetadataAcceptsCaseInsensitiveMatchingAuthorityAndHost(t *testing.T) {
	metadata, err := requestMetadataFromEnvoy([]Header{
		{Name: ":authority", Value: []byte("Example.TEST:8443")},
		{Name: "Host", Value: []byte("example.test:8443")},
	}, map[string]*structpb.Struct{})
	if err != nil {
		t.Fatalf("requestMetadataFromEnvoy() error = %v", err)
	}
	if got, want := metadata.Hostname, "Example.TEST:8443"; got != want {
		t.Fatalf("Hostname = %q, want authority %q", got, want)
	}
}

func TestEnvoyEndpointAddressKeepsOnlyTheHostComponentOfSocketAttributes(t *testing.T) {
	for input, want := range map[string]string{
		"192.0.2.10:45678":  "192.0.2.10",
		"[2001:db8::1]:443": "2001:db8::1",
		"2001:db8::1":       "2001:db8::1",
		"example.test":      "example.test",
	} {
		if got := envoyEndpointAddress(input); got != want {
			t.Errorf("envoyEndpointAddress(%q) = %q, want %q", input, got, want)
		}
	}
}

func newTestService(t *testing.T, transaction *recordingTransaction, policy LateActionPolicy) *Service {
	t.Helper()
	service, err := NewService(testConfig(policy), recordingEngine{transaction: transaction})
	if err != nil {
		t.Fatalf("NewService() error = %v", err)
	}
	return service
}

func testConfig(policy LateActionPolicy) Config {
	return Config{
		ListenAddress:        "127.0.0.1:18083",
		TransactionIDHeader:  "x-request-id",
		MaxHeaderCount:       128,
		MaxHeaderNameBytes:   256,
		MaxHeaderValueBytes:  8192,
		MaxTotalHeaderBytes:  32768,
		MaxBodyChunkBytes:    1024,
		MaxRequestBodyBytes:  4096,
		MaxResponseBodyBytes: 4096,
		MaxGRPCMessageBytes:  2048,
		EngineTimeoutMS:      100,
		CleanupTimeoutMS:     100,
		ShutdownTimeoutMS:    100,
		LateActionPolicy:     policy,
	}
}

type recordingEngine struct {
	transaction *recordingTransaction
}

func (engine recordingEngine) Open(context.Context, StreamMetadata) (Transaction, error) {
	return engine.transaction, nil
}

type policyValidationEngine struct {
	recordingEngine
	rejection error
	policies  []LateActionPolicy
}

func (engine *policyValidationEngine) ValidateLateActionPolicy(policy LateActionPolicy) error {
	engine.policies = append(engine.policies, policy)
	return engine.rejection
}

type recordingTransaction struct {
	headerDecision      func(Direction) Decision
	bodyDecision        func(Direction) Decision
	requestBodyLengths  []int
	responseBodyLengths []int
	closed              []Summary
	hostActions         []HostAction
}

func (transaction *recordingTransaction) ProcessHeaders(_ context.Context, direction Direction, _ []Header, _ bool) (Decision, error) {
	if transaction.headerDecision != nil {
		return transaction.headerDecision(direction), nil
	}
	return allowDecision(), nil
}

func (transaction *recordingTransaction) ProcessBody(_ context.Context, direction Direction, body []byte, _ bool) (Decision, error) {
	// Intentionally keep only length metadata: the test exercises that the
	// stream adapter gives the transaction one chunk at a time.
	if direction == DirectionRequest {
		transaction.requestBodyLengths = append(transaction.requestBodyLengths, len(body))
	} else {
		transaction.responseBodyLengths = append(transaction.responseBodyLengths, len(body))
	}
	if transaction.bodyDecision != nil {
		return transaction.bodyDecision(direction), nil
	}
	return allowDecision(), nil
}

func (transaction *recordingTransaction) Close(_ context.Context, summary Summary) {
	transaction.closed = append(transaction.closed, summary)
}

func (transaction *recordingTransaction) RecordHostAction(_ context.Context, action HostAction) error {
	transaction.hostActions = append(transaction.hostActions, action)
	return nil
}

type receiveResult struct {
	request *extprocv3.ProcessingRequest
	err     error
	cancel  bool
}

type fakeProcessStream struct {
	contextFactory func() context.Context
	cancel         context.CancelFunc
	receive        []receiveResult
	sent           []*extprocv3.ProcessingResponse
	sendErr        error
	index          int
}

func (stream *fakeProcessStream) Send(response *extprocv3.ProcessingResponse) error {
	stream.sent = append(stream.sent, response)
	if stream.sendErr != nil {
		return stream.sendErr
	}
	return nil
}

func (stream *fakeProcessStream) Recv() (*extprocv3.ProcessingRequest, error) {
	if stream.index >= len(stream.receive) {
		return nil, io.EOF
	}
	result := stream.receive[stream.index]
	stream.index++
	if result.cancel && stream.cancel != nil {
		stream.cancel()
	}
	return result.request, result.err
}

func (stream *fakeProcessStream) SetHeader(metadata.MD) error  { return nil }
func (stream *fakeProcessStream) SendHeader(metadata.MD) error { return nil }
func (stream *fakeProcessStream) SetTrailer(metadata.MD)       {}
func (stream *fakeProcessStream) Context() context.Context {
	if stream.contextFactory == nil {
		return context.Background()
	}
	return stream.contextFactory()
}
func (stream *fakeProcessStream) SendMsg(any) error { return nil }
func (stream *fakeProcessStream) RecvMsg(any) error { return nil }

func testStreamContext(contextValue context.Context) func() context.Context {
	return func() context.Context {
		return contextValue
	}
}

func requestHeaders(eos bool) *extprocv3.ProcessingRequest {
	return &extprocv3.ProcessingRequest{Request: &extprocv3.ProcessingRequest_RequestHeaders{RequestHeaders: &extprocv3.HttpHeaders{
		Headers: &corev3.HeaderMap{Headers: []*corev3.HeaderValue{
			{Key: ":method", Value: "POST"},
			{Key: ":path", Value: "/test"},
			{Key: ":authority", Value: "example.test"},
			{Key: "x-request-id", Value: "test-id"},
		}},
		EndOfStream: eos,
	}}}
}

func requestHeadersWithExplicitEmptyBody() *extprocv3.ProcessingRequest {
	request := requestHeaders(false)
	request.GetRequestHeaders().Headers.Headers = append(
		request.GetRequestHeaders().Headers.Headers,
		&corev3.HeaderValue{Key: "content-length", Value: "0"},
	)
	return request
}

func responseHeaders(eos bool) *extprocv3.ProcessingRequest {
	return &extprocv3.ProcessingRequest{Request: &extprocv3.ProcessingRequest_ResponseHeaders{ResponseHeaders: &extprocv3.HttpHeaders{
		Headers:     &corev3.HeaderMap{Headers: []*corev3.HeaderValue{{Key: ":status", Value: "200"}}},
		EndOfStream: eos,
	}}}
}

func requestBody(body []byte, eos bool) *extprocv3.ProcessingRequest {
	return &extprocv3.ProcessingRequest{Request: &extprocv3.ProcessingRequest_RequestBody{RequestBody: &extprocv3.HttpBody{Body: body, EndOfStream: eos}}}
}

func responseBody(body []byte, eos bool) *extprocv3.ProcessingRequest {
	return &extprocv3.ProcessingRequest{Request: &extprocv3.ProcessingRequest_ResponseBody{ResponseBody: &extprocv3.HttpBody{Body: body, EndOfStream: eos}}}
}

func requestTrailers() *extprocv3.ProcessingRequest {
	return &extprocv3.ProcessingRequest{Request: &extprocv3.ProcessingRequest_RequestTrailers{RequestTrailers: &extprocv3.HttpTrailers{
		Trailers: &corev3.HeaderMap{Headers: []*corev3.HeaderValue{{Key: "x-request-trailer", Value: "done"}}},
	}}}
}

func responseTrailers() *extprocv3.ProcessingRequest {
	return &extprocv3.ProcessingRequest{Request: &extprocv3.ProcessingRequest_ResponseTrailers{ResponseTrailers: &extprocv3.HttpTrailers{
		Trailers: &corev3.HeaderMap{Headers: []*corev3.HeaderValue{{Key: "x-response-trailer", Value: "done"}}},
	}}}
}

func sameInts(left, right []int) bool {
	if len(left) != len(right) {
		return false
	}
	for index := range left {
		if left[index] != right[index] {
			return false
		}
	}
	return true
}

func sameLateActionPolicies(left, right []LateActionPolicy) bool {
	if len(left) != len(right) {
		return false
	}
	for index := range left {
		if left[index] != right[index] {
			return false
		}
	}
	return true
}

func sameHostActions(left, right []HostAction) bool {
	if len(left) != len(right) {
		return false
	}
	for index := range left {
		if left[index] != right[index] {
			return false
		}
	}
	return true
}
