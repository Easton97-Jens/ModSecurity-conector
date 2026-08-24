package processor

import (
	"context"
	"io"
	"net"
	"sync"
	"testing"
	"time"

	corev3 "github.com/envoyproxy/go-control-plane/envoy/config/core/v3"
	extprocv3 "github.com/envoyproxy/go-control-plane/envoy/service/ext_proc/v3"
	"google.golang.org/grpc"
	"google.golang.org/grpc/codes"
	"google.golang.org/grpc/credentials/insecure"
	"google.golang.org/grpc/metadata"
	"google.golang.org/grpc/status"
	"google.golang.org/grpc/test/bufconn"
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

func TestLateStrictDecisionDoesNotClaimOrSendAbort(t *testing.T) {
	transaction := &recordingTransaction{
		bodyDecision: func(direction Direction) Decision {
			if direction == DirectionResponse {
				return Decision{Action: ActionDeny, Status: 403}
			}
			return allowDecision()
		},
	}
	service := newTestService(t, transaction, LateActionStrict)
	stream := &fakeProcessStream{contextFactory: testStreamContext(context.Background()), receive: []receiveResult{
		{request: requestHeaders(true)},
		{request: responseHeaders(false)},
		{request: responseBody([]byte("late"), true)},
	}}

	if err := service.Process(stream); err != nil {
		t.Fatalf("Process() error = %v", err)
	}
	last := stream.sent[len(stream.sent)-1]
	if last.GetResponseBody() == nil || last.GetImmediateResponse() != nil {
		t.Fatalf("late decision must continue the response body, got %#v", last)
	}
	summary := transaction.closed[0]
	if summary.LateAction != LateActionStrictNotAttempted {
		t.Fatalf("late action = %q, want %q", summary.LateAction, LateActionStrictNotAttempted)
	}
	if len(transaction.hostActions) != 0 {
		t.Fatalf("strict late decision recorded a fabricated host action: %#v", transaction.hostActions)
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

func TestConfigRequiresNumericLoopbackListener(t *testing.T) {
	for _, address := range []string{"0.0.0.0:18083", "192.0.2.1:18083", "localhost:18083", "[::]:18083"} {
		config := testConfig(LateActionSafe)
		config.ListenAddress = address
		if err := config.Validate(); err == nil {
			t.Errorf("Validate(%q) accepted a non-loopback or non-numeric listener", address)
		}
	}
	for _, address := range []string{"127.0.0.1:18083", "127.42.0.7:18083", "[::1]:18083"} {
		config := testConfig(LateActionSafe)
		config.ListenAddress = address
		if err := config.Validate(); err != nil {
			t.Errorf("Validate(%q) rejected numeric loopback listener: %v", address, err)
		}
	}
}

func TestConfigRequiresBoundedIdleAndConcurrentStreamLimits(t *testing.T) {
	for name, mutate := range map[string]func(*Config){
		"zero idle timeout": func(config *Config) { config.StreamIdleTimeoutMS = 0 },
		"zero stream limit": func(config *Config) { config.MaxConcurrentStreams = 0 },
		"oversized stream limit": func(config *Config) {
			config.MaxConcurrentStreams = MaximumConcurrentStreams + 1
		},
	} {
		config := testConfig(LateActionSafe)
		mutate(&config)
		if err := config.Validate(); err == nil {
			t.Errorf("Validate() accepted %s", name)
		}
	}
}

func TestProcessRejectsWhenProcessWideStreamAdmissionIsFull(t *testing.T) {
	service := newTestService(t, &recordingTransaction{}, LateActionSafe)
	for index := 0; index < service.config.MaxConcurrentStreams; index++ {
		service.admission <- struct{}{}
	}

	stream := &fakeProcessStream{receive: []receiveResult{{request: requestHeaders(true)}}}
	err := service.Process(stream)
	if status.Code(err) != codes.ResourceExhausted {
		t.Fatalf("Process() error code = %v, want %v (err=%v)", status.Code(err), codes.ResourceExhausted, err)
	}
	if stream.index != 0 || len(stream.sent) != 0 {
		t.Fatalf("overload rejection touched stream: index=%d sent=%d", stream.index, len(stream.sent))
	}
}

func TestStreamIdleTimeoutCleansUpAndAllowsFollowUpStream(t *testing.T) {
	transaction := &recordingTransaction{}
	config := testConfig(LateActionSafe)
	config.StreamIdleTimeoutMS = 20
	service, err := NewService(config, recordingEngine{transaction: transaction})
	if err != nil {
		t.Fatalf("NewService() error = %v", err)
	}
	contextValue, cancel := context.WithCancel(context.Background())
	defer cancel()
	stream := &fakeProcessStream{
		contextFactory: testStreamContext(contextValue),
		receive:        []receiveResult{{request: requestHeaders(false)}},
		receiveBlock:   make(chan struct{}),
		recvStarted:    make(chan struct{}),
		recvBlocking:   make(chan struct{}),
		recvDone:       make(chan struct{}),
	}

	result := make(chan error, 1)
	go func() { result <- service.Process(stream) }()
	select {
	case <-stream.recvStarted:
	case <-time.After(time.Second):
		t.Fatal("idle stream never entered Recv")
	}
	select {
	case <-stream.recvBlocking:
	case <-time.After(time.Second):
		t.Fatal("idle stream never waited for its next message")
	}
	if err := <-result; status.Code(err) != codes.DeadlineExceeded {
		t.Fatalf("Process() idle result = %v, want DeadlineExceeded", err)
	}
	if len(transaction.closed) != 1 || transaction.closed[0].CloseReason != CloseStreamIdleTimeout {
		t.Fatalf("idle cleanup = %#v, want one stream_idle_timeout", transaction.closed)
	}
	if got := service.pendingReceives.Load(); got != 1 {
		t.Fatalf("pending Recv count after fake idle return = %d, want one blocked receive", got)
	}

	// A returning gRPC handler cancels the real transport context. The fake
	// stream needs the same explicit cancellation to release its blocked Recv
	// goroutine before the follow-up control stream is asserted.
	cancel()
	select {
	case <-stream.recvDone:
	case <-time.After(time.Second):
		t.Fatal("idle Recv goroutine did not observe cancellation")
	}
	deadline := time.Now().Add(time.Second)
	for service.pendingReceives.Load() != 0 && time.Now().Before(deadline) {
		time.Sleep(time.Millisecond)
	}
	if got := service.pendingReceives.Load(); got != 0 {
		t.Fatalf("pending Recv count after cancellation = %d, want zero", got)
	}
	control := &fakeProcessStream{contextFactory: testStreamContext(context.Background()), receive: []receiveResult{{request: requestHeaders(true)}}}
	if err := service.Process(control); err != nil {
		t.Fatalf("follow-up Process() error = %v", err)
	}
	if len(transaction.closed) != 2 {
		t.Fatalf("follow-up cleanup count = %d, want 2", len(transaction.closed))
	}
}

func TestGRPCServerIdleTimeoutReleasesAdmissionForFollowUpStream(t *testing.T) {
	transaction := &recordingTransaction{}
	config := testConfig(LateActionSafe)
	config.StreamIdleTimeoutMS = 20
	config.MaxConcurrentStreams = 1
	service, err := NewService(config, recordingEngine{transaction: transaction})
	if err != nil {
		t.Fatalf("NewService() error = %v", err)
	}
	listener := bufconn.Listen(1024 * 1024)
	server := grpc.NewServer(grpc.MaxConcurrentStreams(uint32(config.MaxConcurrentStreams)))
	extprocv3.RegisterExternalProcessorServer(server, service)
	defer server.Stop()
	go func() { _ = server.Serve(listener) }()

	connection, err := grpc.DialContext(context.Background(), "bufnet",
		grpc.WithContextDialer(func(context.Context, string) (net.Conn, error) {
			return listener.Dial()
		}),
		grpc.WithTransportCredentials(insecure.NewCredentials()))
	if err != nil {
		t.Fatalf("DialContext() error = %v", err)
	}
	defer connection.Close()
	client := extprocv3.NewExternalProcessorClient(connection)
	idle, err := client.Process(context.Background())
	if err != nil {
		t.Fatalf("idle Process() open error = %v", err)
	}
	if _, err := idle.Recv(); status.Code(err) != codes.DeadlineExceeded {
		t.Fatalf("idle stream Recv() error = %v, want DeadlineExceeded", err)
	}
	deadline := time.Now().Add(time.Second)
	for service.pendingReceives.Load() != 0 && time.Now().Before(deadline) {
		time.Sleep(time.Millisecond)
	}
	if got := service.pendingReceives.Load(); got != 0 {
		t.Fatalf("bufconn idle stream retained %d Recv goroutines", got)
	}

	control, err := client.Process(context.Background())
	if err != nil {
		t.Fatalf("follow-up Process() open error = %v", err)
	}
	if err := control.Send(requestHeaders(true)); err != nil {
		t.Fatalf("follow-up Send() error = %v", err)
	}
	if response, err := control.Recv(); err != nil || response.GetRequestHeaders() == nil {
		t.Fatalf("follow-up Recv() = %#v, %v; want request headers response", response, err)
	}
	if err := control.CloseSend(); err != nil {
		t.Fatalf("follow-up CloseSend() error = %v", err)
	}
	if _, err := control.Recv(); err != io.EOF {
		t.Fatalf("follow-up final Recv() error = %v, want EOF", err)
	}
}

func TestGRPCServerStopCancelsIdleStreamAndReleasesAdmission(t *testing.T) {
	transaction := &recordingTransaction{closedDone: make(chan struct{})}
	config := testConfig(LateActionSafe)
	config.StreamIdleTimeoutMS = 1000
	config.MaxConcurrentStreams = 1
	service, err := NewService(config, recordingEngine{transaction: transaction})
	if err != nil {
		t.Fatalf("NewService() error = %v", err)
	}
	listener := bufconn.Listen(1024 * 1024)
	server := grpc.NewServer(grpc.MaxConcurrentStreams(uint32(config.MaxConcurrentStreams)))
	extprocv3.RegisterExternalProcessorServer(server, service)
	go func() { _ = server.Serve(listener) }()

	connection, err := grpc.DialContext(context.Background(), "bufnet",
		grpc.WithContextDialer(func(context.Context, string) (net.Conn, error) {
			return listener.Dial()
		}),
		grpc.WithTransportCredentials(insecure.NewCredentials()))
	if err != nil {
		t.Fatalf("DialContext() error = %v", err)
	}
	defer connection.Close()
	client := extprocv3.NewExternalProcessorClient(connection)
	stream, err := client.Process(context.Background())
	if err != nil {
		t.Fatalf("Process() open error = %v", err)
	}
	if err := stream.Send(requestHeaders(false)); err != nil {
		t.Fatalf("Send() error = %v", err)
	}
	if response, err := stream.Recv(); err != nil || response.GetRequestHeaders() == nil {
		t.Fatalf("initial Recv() = %#v, %v; want request headers response", response, err)
	}

	// This exercises the forced Stop path used after a bounded graceful
	// shutdown. The idle handler must observe its cancelled stream context,
	// close its transaction, and return its admission slot.
	server.Stop()
	select {
	case <-transaction.closedDone:
	case <-time.After(time.Second):
		t.Fatal("server Stop() did not cancel and clean up the idle stream")
	}
	if len(transaction.closed) != 1 || transaction.closed[0].CloseReason != CloseContextCanceled {
		t.Fatalf("shutdown cleanup = %#v, want one context_canceled close", transaction.closed)
	}
	deadline := time.Now().Add(time.Second)
	for len(service.admission) != 0 && time.Now().Before(deadline) {
		time.Sleep(time.Millisecond)
	}
	if len(service.admission) != 0 {
		t.Fatalf("server shutdown left %d admission slots occupied", len(service.admission))
	}

	control := &fakeProcessStream{contextFactory: testStreamContext(context.Background()), receive: []receiveResult{{request: requestHeaders(true)}}}
	if err := service.Process(control); err != nil {
		t.Fatalf("follow-up Process() after shutdown cleanup error = %v", err)
	}
}

func TestRegularStreamActivityResetsIdleDeadline(t *testing.T) {
	transaction := &recordingTransaction{}
	config := testConfig(LateActionSafe)
	config.StreamIdleTimeoutMS = 30
	service, err := NewService(config, recordingEngine{transaction: transaction})
	if err != nil {
		t.Fatalf("NewService() error = %v", err)
	}
	requests := make(chan receiveResult)
	stream := &fakeProcessStream{
		contextFactory: testStreamContext(context.Background()),
		receiveChannel: requests,
	}
	result := make(chan error, 1)
	go func() { result <- service.Process(stream) }()

	requests <- receiveResult{request: requestHeaders(false)}
	time.Sleep(15 * time.Millisecond)
	requests <- receiveResult{request: requestBody([]byte("one"), false)}
	time.Sleep(15 * time.Millisecond)
	requests <- receiveResult{request: requestBody([]byte("two"), true)}
	time.Sleep(15 * time.Millisecond)
	close(requests)

	if err := <-result; err != nil {
		t.Fatalf("active stream Process() error = %v", err)
	}
	if len(transaction.closed) != 1 || transaction.closed[0].CloseReason != ClosePeerEOF {
		t.Fatalf("active stream cleanup = %#v", transaction.closed)
	}
	if got, want := transaction.requestBodyLengths, []int{3, 3}; !sameInts(got, want) {
		t.Fatalf("active stream body chunks = %v, want %v", got, want)
	}
}

func TestConcurrentStreamLimitReleasesAfterCancellation(t *testing.T) {
	transaction := &recordingTransaction{}
	config := testConfig(LateActionSafe)
	config.MaxConcurrentStreams = 1
	config.StreamIdleTimeoutMS = 1000
	service, err := NewService(config, recordingEngine{transaction: transaction})
	if err != nil {
		t.Fatalf("NewService() error = %v", err)
	}
	contextValue, cancel := context.WithCancel(context.Background())
	first := &fakeProcessStream{
		contextFactory: testStreamContext(contextValue),
		receiveBlock:   make(chan struct{}),
		recvStarted:    make(chan struct{}),
	}
	firstResult := make(chan error, 1)
	go func() { firstResult <- service.Process(first) }()
	select {
	case <-first.recvStarted:
	case <-time.After(time.Second):
		t.Fatal("first stream never entered Recv")
	}

	second := &fakeProcessStream{contextFactory: testStreamContext(context.Background()), receive: []receiveResult{{request: requestHeaders(true)}}}
	if err := service.Process(second); status.Code(err) != codes.ResourceExhausted {
		t.Fatalf("second Process() error = %v, want ResourceExhausted", err)
	}
	cancel()
	if err := <-firstResult; err != nil {
		t.Fatalf("cancelled first Process() error = %v", err)
	}

	third := &fakeProcessStream{contextFactory: testStreamContext(context.Background()), receive: []receiveResult{{request: requestHeaders(true)}}}
	if err := service.Process(third); err != nil {
		t.Fatalf("follow-up after cancellation error = %v", err)
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
		StreamIdleTimeoutMS:  100,
		MaxConcurrentStreams: 8,
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

type recordingTransaction struct {
	headerDecision      func(Direction) Decision
	bodyDecision        func(Direction) Decision
	requestBodyLengths  []int
	responseBodyLengths []int
	closed              []Summary
	hostActions         []HostAction
	closedDone          chan struct{}
	closedOnce          sync.Once
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
	if transaction.closedDone != nil {
		transaction.closedOnce.Do(func() { close(transaction.closedDone) })
	}
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
	contextFactory   func() context.Context
	cancel           context.CancelFunc
	receive          []receiveResult
	receiveChannel   <-chan receiveResult
	receiveBlock     <-chan struct{}
	recvStarted      chan struct{}
	recvBlocking     chan struct{}
	recvDone         chan struct{}
	sent             []*extprocv3.ProcessingResponse
	sendErr          error
	index            int
	recvStartedOnce  sync.Once
	recvBlockingOnce sync.Once
	recvDoneOnce     sync.Once
}

func (stream *fakeProcessStream) Send(response *extprocv3.ProcessingResponse) error {
	stream.sent = append(stream.sent, response)
	if stream.sendErr != nil {
		return stream.sendErr
	}
	return nil
}

func (stream *fakeProcessStream) Recv() (*extprocv3.ProcessingRequest, error) {
	if stream.recvStarted != nil {
		stream.recvStartedOnce.Do(func() { close(stream.recvStarted) })
	}
	if stream.receiveChannel != nil {
		select {
		case result, ok := <-stream.receiveChannel:
			if !ok {
				return nil, io.EOF
			}
			if result.cancel && stream.cancel != nil {
				stream.cancel()
			}
			return result.request, result.err
		case <-stream.Context().Done():
			return nil, stream.Context().Err()
		}
	}
	if stream.index >= len(stream.receive) {
		if stream.receiveBlock != nil {
			if stream.recvBlocking != nil {
				stream.recvBlockingOnce.Do(func() { close(stream.recvBlocking) })
			}
			defer func() {
				if stream.recvDone != nil {
					stream.recvDoneOnce.Do(func() { close(stream.recvDone) })
				}
			}()
			select {
			case <-stream.receiveBlock:
				return nil, io.EOF
			case <-stream.Context().Done():
				return nil, stream.Context().Err()
			}
		}
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
