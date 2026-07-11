package processor

import (
	"context"
	"io"
	"testing"

	corev3 "github.com/envoyproxy/go-control-plane/envoy/config/core/v3"
	extprocv3 "github.com/envoyproxy/go-control-plane/envoy/service/ext_proc/v3"
	"google.golang.org/grpc/metadata"
)

func TestProcessStreamsChunksAndCleansUpAtResponseEOS(t *testing.T) {
	transaction := &recordingTransaction{}
	service := newTestService(t, transaction, LateActionSafe)
	stream := &fakeProcessStream{context: context.Background(), receive: []receiveResult{
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
	stream := &fakeProcessStream{context: context.Background(), receive: []receiveResult{{request: requestHeaders(false)}}}

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
	stream := &fakeProcessStream{context: context.Background(), receive: []receiveResult{
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
}

func TestCancellationCleansUpWithoutAttributingTheHTTPReset(t *testing.T) {
	transaction := &recordingTransaction{}
	service := newTestService(t, transaction, LateActionSafe)
	contextValue, cancel := context.WithCancel(context.Background())
	stream := &fakeProcessStream{context: contextValue, cancel: cancel, receive: []receiveResult{
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

func newTestService(t *testing.T, transaction *recordingTransaction, policy LateActionPolicy) *Service {
	t.Helper()
	config := Config{
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
	service, err := NewService(config, recordingEngine{transaction: transaction})
	if err != nil {
		t.Fatalf("NewService() error = %v", err)
	}
	return service
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

type receiveResult struct {
	request *extprocv3.ProcessingRequest
	err     error
	cancel  bool
}

type fakeProcessStream struct {
	context context.Context
	cancel  context.CancelFunc
	receive []receiveResult
	sent    []*extprocv3.ProcessingResponse
	index   int
}

func (stream *fakeProcessStream) Send(response *extprocv3.ProcessingResponse) error {
	stream.sent = append(stream.sent, response)
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
func (stream *fakeProcessStream) Context() context.Context     { return stream.context }
func (stream *fakeProcessStream) SendMsg(any) error            { return nil }
func (stream *fakeProcessStream) RecvMsg(any) error            { return nil }

func requestHeaders(eos bool) *extprocv3.ProcessingRequest {
	return &extprocv3.ProcessingRequest{Request: &extprocv3.ProcessingRequest_RequestHeaders{RequestHeaders: &extprocv3.HttpHeaders{
		Headers: &corev3.HeaderMap{Headers: []*corev3.HeaderValue{
			{Key: ":method", Value: "POST"},
			{Key: "x-request-id", Value: "test-id"},
		}},
		EndOfStream: eos,
	}}}
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
