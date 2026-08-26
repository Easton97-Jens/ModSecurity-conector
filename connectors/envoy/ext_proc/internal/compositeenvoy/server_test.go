package compositeenvoy

import (
	"context"
	"errors"
	"io"
	"net"
	"strconv"
	"strings"
	"testing"
	"time"

	"github.com/Easton97-Jens/ModSecurity-conector/connectors/envoy/ext_proc/internal/composite"
	"github.com/Easton97-Jens/ModSecurity-conector/connectors/envoy/ext_proc/internal/processor"
	corev3 "github.com/envoyproxy/go-control-plane/envoy/config/core/v3"
	authv3 "github.com/envoyproxy/go-control-plane/envoy/service/auth/v3"
	extprocv3 "github.com/envoyproxy/go-control-plane/envoy/service/ext_proc/v3"
	"google.golang.org/grpc"
	"google.golang.org/grpc/codes"
	"google.golang.org/grpc/credentials/insecure"
	"google.golang.org/grpc/metadata"
	"google.golang.org/grpc/status"
	"google.golang.org/grpc/test/bufconn"
	"google.golang.org/protobuf/types/known/structpb"
)

type recordingOpener struct{ opened processor.StreamMetadata }

func (o *recordingOpener) Open(_ context.Context, meta processor.StreamMetadata) (processor.Transaction, error) {
	o.opened = meta
	return recordingTransaction{}, nil
}

type recordingTransaction struct{}

func (recordingTransaction) ProcessHeaders(context.Context, processor.Direction, []processor.Header, bool) (processor.Decision, error) {
	return processor.Decision{Action: processor.ActionAllow}, nil
}
func (recordingTransaction) ProcessBody(context.Context, processor.Direction, []byte, bool) (processor.Decision, error) {
	return processor.Decision{Action: processor.ActionAllow}, nil
}
func (recordingTransaction) Close(context.Context, processor.Summary) {}

func TestCheckUsesServerDecisionIDAndMetadataOnlyLease(t *testing.T) {
	opener := &recordingOpener{}
	coordinator, err := composite.New("envoy", make([]byte, 32), composite.Limits{Capacity: 2}, opener, nil)
	if err != nil {
		t.Fatal(err)
	}
	defer coordinator.Close()
	server, err := NewAuthzServer(coordinator)
	if err != nil {
		t.Fatal(err)
	}
	response, err := server.Check(context.Background(), &authv3.CheckRequest{Attributes: &authv3.AttributeContext{
		Source:      &authv3.AttributeContext_Peer{Address: testAddress("127.0.0.1", 1234)},
		Destination: &authv3.AttributeContext_Peer{Address: testAddress("127.0.0.1", 8080)},
		Request:     &authv3.AttributeContext_Request{Http: &authv3.AttributeContext_HttpRequest{Id: "client-id", Method: "POST", Path: "/", Host: "example.test", Protocol: "HTTP/1.1", Headers: map[string]string{"x-request-id": "client-id"}, RawBody: []byte("body")}},
	}})
	if err != nil {
		t.Fatal(err)
	}
	if response.GetOkResponse() == nil || response.GetDynamicMetadata() == nil {
		t.Fatal("allow response omitted dynamic metadata")
	}
	if response.GetOkResponse().GetHeaders() != nil && len(response.GetOkResponse().GetHeaders()) != 0 {
		t.Fatal("lease was returned as an HTTP header")
	}
	if opener.opened.TransactionID == "" || opener.opened.TransactionID == "client-id" {
		t.Fatalf("decision ID was not server generated: %q", opener.opened.TransactionID)
	}
	if _, ok := response.GetDynamicMetadata().GetFields()["lease"]; !ok {
		t.Fatal("lease missing from dynamic metadata")
	}
	if _, ok := response.GetDynamicMetadata().GetFields()[metadataTerminal]; ok {
		t.Fatal("allow response was marked as a terminal local reply")
	}
}

func TestAuthRequestExcludesClientSuppliedCompositeLeaseHeader(t *testing.T) {
	request := authCheckRequest(nil)
	request.GetAttributes().GetRequest().GetHttp().Headers = map[string]string{
		"X-MsConnector-Composite-Lease": "client-spoof",
		"x-msconnector-composite-lease": "client-spoof-duplicate",
		"X-Request-ID":                  "request-id",
	}
	_, headers, _, err := authRequest(request)
	if err != nil {
		t.Fatal(err)
	}
	for _, header := range headers {
		if header.Name == compositeLeaseHeader {
			t.Fatalf("client-supplied protected header reached Common: %+v", headers)
		}
	}
	if len(headers) != 1 || headers[0].Name != "x-request-id" {
		t.Fatalf("headers=%v, want only non-reserved request header", headers)
	}
}

func TestCheckAcceptsExactly32ByteBodyAndMintsLease(t *testing.T) {
	opener := &recordingOpener{}
	coordinator, err := composite.New("envoy", make([]byte, 32), composite.Limits{Capacity: 2, MaxRequestBody: 32}, opener, nil)
	if err != nil {
		t.Fatal(err)
	}
	defer coordinator.Close()
	server, err := NewAuthzServer(coordinator)
	if err != nil {
		t.Fatal(err)
	}
	response, err := server.Check(context.Background(), authCheckRequest(make([]byte, 32)))
	if err != nil {
		t.Fatal(err)
	}
	if response.GetOkResponse() == nil || response.GetDynamicMetadata().GetFields()["lease"].GetStringValue() == "" {
		t.Fatalf("exactly 32 bytes did not receive allow/lease metadata: %v", response)
	}
}

func TestCheckRejects33ByteBodyWith413(t *testing.T) {
	opener := &recordingOpener{}
	coordinator, err := composite.New("envoy", make([]byte, 32), composite.Limits{Capacity: 2, MaxRequestBody: 32}, opener, nil)
	if err != nil {
		t.Fatal(err)
	}
	defer coordinator.Close()
	server, err := NewAuthzServer(coordinator)
	if err != nil {
		t.Fatal(err)
	}
	response, err := server.Check(context.Background(), authCheckRequest(make([]byte, 33)))
	if err != nil {
		t.Fatal(err)
	}
	if response.GetDeniedResponse() == nil || response.GetDeniedResponse().GetStatus().GetCode() != 413 {
		t.Fatalf("33-byte body response=%v, want fail-closed 413", response)
	}
}

// strictRequestOpener models the Common runtime's transport-result allowlist.
// It prevents the Envoy adapter tests from accepting connector-local labels
// that make a real CGo/Common host fail closed with a 503.
type strictRequestOpener struct {
	headerAction           processor.Action
	bodyAction             processor.Action
	status                 int
	redirectURL            string
	rejectNativeHostAction bool
	tx                     *strictRequestTransaction
}

func (o *strictRequestOpener) Open(_ context.Context, _ processor.StreamMetadata) (processor.Transaction, error) {
	o.tx = &strictRequestTransaction{headerAction: o.headerAction, bodyAction: o.bodyAction, status: o.status, redirectURL: o.redirectURL, rejectNativeHostAction: o.rejectNativeHostAction}
	return o.tx, nil
}

type strictRequestTransaction struct {
	headerAction           processor.Action
	bodyAction             processor.Action
	status                 int
	redirectURL            string
	rejectNativeHostAction bool
	actions                []processor.HostAction
}

func (t *strictRequestTransaction) ProcessHeaders(_ context.Context, _ processor.Direction, _ []processor.Header, _ bool) (processor.Decision, error) {
	return processor.Decision{Action: t.headerAction, Status: t.status, RedirectURL: t.redirectURL}, nil
}
func (t *strictRequestTransaction) ProcessBody(_ context.Context, _ processor.Direction, _ []byte, _ bool) (processor.Decision, error) {
	return processor.Decision{Action: t.bodyAction, Status: t.status, RedirectURL: t.redirectURL}, nil
}
func (t *strictRequestTransaction) Close(context.Context, processor.Summary) {}
func (t *strictRequestTransaction) RecordHostAction(_ context.Context, action processor.HostAction) error {
	if t.rejectNativeHostAction {
		return errors.New("synthetic request body limit invoked native Common host action")
	}
	if action.TransportResult != commonTransportHTTPStatus {
		return errors.New("noncanonical Common transport result")
	}
	t.actions = append(t.actions, action)
	return nil
}

type canonicalTransportCase struct {
	name             string
	headerAction     processor.Action
	bodyAction       processor.Action
	body             []byte
	wantStatus       int32
	wantNativeAction bool
}

func TestCheckUsesCanonicalCommonTransportForDenyAndBodyLimit(t *testing.T) {
	tests := []canonicalTransportCase{
		{name: "p1 deny", headerAction: processor.ActionDeny, bodyAction: processor.ActionAllow, wantStatus: 403, wantNativeAction: true},
		{name: "p2 deny", headerAction: processor.ActionAllow, bodyAction: processor.ActionDeny, body: []byte("p2"), wantStatus: 403, wantNativeAction: true},
		{name: "p2 body limit", headerAction: processor.ActionAllow, bodyAction: processor.ActionAllow, body: make([]byte, 33), wantStatus: 413},
	}
	for _, test := range tests {
		t.Run(test.name, func(t *testing.T) { runCanonicalTransportCase(t, test) })
	}
}

func runCanonicalTransportCase(t *testing.T, test canonicalTransportCase) {
	t.Helper()
	opener := &strictRequestOpener{headerAction: test.headerAction, bodyAction: test.bodyAction, status: 403, rejectNativeHostAction: !test.wantNativeAction}
	coordinator, err := composite.New("envoy", make([]byte, 32), composite.Limits{Capacity: 2, MaxRequestBody: 32}, opener, nil)
	if err != nil {
		t.Fatal(err)
	}
	t.Cleanup(coordinator.Close)
	server, err := NewAuthzServer(coordinator)
	if err != nil {
		t.Fatal(err)
	}
	response, err := server.Check(context.Background(), authCheckRequest(test.body))
	if err != nil {
		t.Fatal(err)
	}
	if response.GetDeniedResponse() == nil || int32(response.GetDeniedResponse().GetStatus().GetCode()) != test.wantStatus {
		t.Fatalf("response=%v, want denied status %d", response, test.wantStatus)
	}
	if response.GetDynamicMetadata().GetFields()[metadataTerminal].GetStringValue() != metadataTerminalBlock || response.GetDynamicMetadata().GetFields()[metadataLease] != nil {
		t.Fatalf("denied response did not carry only the protected terminal marker: %v", response.GetDynamicMetadata())
	}
	if opener.tx == nil {
		t.Fatal("missing request transaction")
	}
	if test.wantNativeAction && (len(opener.tx.actions) != 1 || opener.tx.actions[0].TransportResult != commonTransportHTTPStatus) {
		t.Fatalf("actions=%v, want one canonical %q action", opener.tx.actions, commonTransportHTTPStatus)
	}
	if !test.wantNativeAction && len(opener.tx.actions) != 0 {
		t.Fatalf("synthetic P2 limit invoked native Common action: %v", opener.tx.actions)
	}
}

func TestCheckNormalizesMalformedRequestDenyStatus(t *testing.T) {
	for _, malformedStatus := range []int{103, 200, 600} {
		t.Run(strconv.Itoa(malformedStatus), func(t *testing.T) {
			opener := &strictRequestOpener{headerAction: processor.ActionDeny, bodyAction: processor.ActionAllow, status: malformedStatus}
			response := runStrictCheck(t, opener)
			if got := int(response.GetDeniedResponse().GetStatus().GetCode()); got != 403 {
				t.Fatalf("visible status=%d, want 403", got)
			}
			if opener.tx == nil || len(opener.tx.actions) != 1 || opener.tx.actions[0].VisibleStatus != 403 || opener.tx.actions[0].Action != processor.AppliedActionDeny {
				t.Fatalf("host actions=%v, want one deny status 403", opener.tx.actions)
			}
		})
	}
}

func TestCheckPreservesValidatedRedirect(t *testing.T) {
	const location = "https://redirect.example.test/next"
	opener := &strictRequestOpener{headerAction: processor.ActionRedirect, bodyAction: processor.ActionAllow, status: 307, redirectURL: location}
	response := runStrictCheck(t, opener)
	denied := response.GetDeniedResponse()
	if denied == nil || int(denied.GetStatus().GetCode()) != 307 {
		t.Fatalf("response=%v, want redirect status 307", response)
	}
	foundLocation := false
	for _, header := range denied.GetHeaders() {
		if header.GetHeader().GetKey() == "location" && header.GetHeader().GetValue() == location {
			foundLocation = true
		}
	}
	if !foundLocation {
		t.Fatalf("redirect response omitted location %q: %v", location, denied)
	}
	if opener.tx == nil || len(opener.tx.actions) != 1 || opener.tx.actions[0].Action != processor.AppliedActionRedirect || opener.tx.actions[0].VisibleStatus != 307 {
		t.Fatalf("host actions=%v, want one redirect status 307", opener.tx.actions)
	}
}

func runStrictCheck(t *testing.T, opener *strictRequestOpener) *authv3.CheckResponse {
	t.Helper()
	coordinator, err := composite.New("envoy", make([]byte, 32), composite.Limits{Capacity: 2}, opener, nil)
	if err != nil {
		t.Fatal(err)
	}
	t.Cleanup(coordinator.Close)
	server, err := NewAuthzServer(coordinator)
	if err != nil {
		t.Fatal(err)
	}
	response, err := server.Check(context.Background(), authCheckRequest(nil))
	if err != nil {
		t.Fatal(err)
	}
	return response
}

func TestNormalizePolicyDecisionRejectsInvalidRedirect(t *testing.T) {
	got := normalizePolicyDecision(processor.Decision{Action: processor.ActionRedirect, Status: 307, RedirectURL: " \t"}, nil)
	if got.Action != processor.ActionDeny || got.Status != 403 || got.RedirectURL != "" {
		t.Fatalf("normalized invalid redirect=%#v, want deny 403", got)
	}
}

func TestNormalizePolicyDecisionRejectsUnsafeRedirectTarget(t *testing.T) {
	for _, target := range []string{"https://redirect.example.test/next\r\nX-Injected: true", strings.Repeat("a", 2049)} {
		got := normalizePolicyDecision(processor.Decision{Action: processor.ActionRedirect, Status: 307, RedirectURL: target}, nil)
		if got.Action != processor.ActionDeny || got.Status != 403 || got.RedirectURL != "" {
			t.Fatalf("normalized unsafe redirect=%#v, want deny 403", got)
		}
	}
}

func authCheckRequest(body []byte) *authv3.CheckRequest {
	return &authv3.CheckRequest{Attributes: &authv3.AttributeContext{
		Source:      &authv3.AttributeContext_Peer{Address: testAddress("127.0.0.1", 1234)},
		Destination: &authv3.AttributeContext_Peer{Address: testAddress("127.0.0.1", 8080)},
		Request: &authv3.AttributeContext_Request{Http: &authv3.AttributeContext_HttpRequest{
			Method: "POST", Path: "/", Host: "example.test", Protocol: "HTTP/1.1", RawBody: body,
		}},
	}}
}

func TestLeaseMetadataRequiresExactNamespaceAndVersion(t *testing.T) {
	lease := "server-lease"
	good, err := structpb.NewStruct(map[string]interface{}{"lease": lease, "version": float64(1)})
	if err != nil {
		t.Fatal(err)
	}
	metadata := &coreMetadata{filter: map[string]*structpb.Struct{metadataNamespace: good}}
	if got, ok := leaseFromMetadata(metadata.toProto()); !ok || got != lease {
		t.Fatalf("valid metadata rejected: %q %v", got, ok)
	}
	wrong, _ := structpb.NewStruct(map[string]interface{}{"lease": lease, "version": float64(2)})
	metadata.filter[metadataNamespace] = wrong
	if _, ok := leaseFromMetadata(metadata.toProto()); ok {
		t.Fatal("wrong metadata version accepted")
	}
	metadata.filter = map[string]*structpb.Struct{"other.namespace": good}
	if _, ok := leaseFromMetadata(metadata.toProto()); ok {
		t.Fatal("lease from unexpected namespace accepted")
	}
}

// coreMetadata keeps this test's construction readable without leaking Envoy
// metadata details into the coordinator package.
type coreMetadata struct{ filter map[string]*structpb.Struct }

func (m *coreMetadata) toProto() *corev3.Metadata { return &corev3.Metadata{FilterMetadata: m.filter} }

func testAddress(host string, port uint32) *corev3.Address {
	return &corev3.Address{Address: &corev3.Address_SocketAddress{SocketAddress: &corev3.SocketAddress{Address: host, PortSpecifier: &corev3.SocketAddress_PortValue{PortValue: port}}}}
}

type processStream struct {
	requests  []*extprocv3.ProcessingRequest
	responses []*extprocv3.ProcessingResponse
}

func (s *processStream) SetHeader(metadata.MD) error  { return nil }
func (s *processStream) SendHeader(metadata.MD) error { return nil }
func (s *processStream) SetTrailer(metadata.MD)       {}
func (s *processStream) Context() context.Context     { return context.Background() }
func (s *processStream) SendMsg(interface{}) error    { return nil }
func (s *processStream) RecvMsg(interface{}) error    { return nil }
func (s *processStream) Send(response *extprocv3.ProcessingResponse) error {
	s.responses = append(s.responses, response)
	return nil
}
func (s *processStream) Recv() (*extprocv3.ProcessingRequest, error) {
	if len(s.requests) == 0 {
		return nil, io.EOF
	}
	request := s.requests[0]
	s.requests = s.requests[1:]
	return request, nil
}

type blockingProcessStream struct {
	ctx         context.Context
	requests    chan *extprocv3.ProcessingRequest
	responses   []*extprocv3.ProcessingResponse
	recvEntered chan struct{}
	recvExited  chan struct{}
}

func newBlockingProcessStream(ctx context.Context) *blockingProcessStream {
	return &blockingProcessStream{
		ctx:         ctx,
		requests:    make(chan *extprocv3.ProcessingRequest, 4),
		recvEntered: make(chan struct{}, 4),
		recvExited:  make(chan struct{}, 4),
	}
}

func (s *blockingProcessStream) SetHeader(metadata.MD) error  { return nil }
func (s *blockingProcessStream) SendHeader(metadata.MD) error { return nil }
func (s *blockingProcessStream) SetTrailer(metadata.MD)       {}
func (s *blockingProcessStream) Context() context.Context     { return s.ctx }
func (s *blockingProcessStream) SendMsg(interface{}) error    { return nil }
func (s *blockingProcessStream) RecvMsg(interface{}) error    { return nil }
func (s *blockingProcessStream) Send(response *extprocv3.ProcessingResponse) error {
	s.responses = append(s.responses, response)
	return nil
}
func (s *blockingProcessStream) Recv() (*extprocv3.ProcessingRequest, error) {
	s.recvEntered <- struct{}{}
	defer func() { s.recvExited <- struct{}{} }()
	select {
	case request := <-s.requests:
		return request, nil
	case <-s.ctx.Done():
		return nil, s.ctx.Err()
	}
}

func waitForStreamSignal(t *testing.T, signal <-chan struct{}, name string) {
	t.Helper()
	select {
	case <-signal:
	case <-time.After(time.Second):
		t.Fatalf("timed out waiting for %s", name)
	}
}

func waitForProcessResult(t *testing.T, done <-chan error) error {
	t.Helper()
	select {
	case err := <-done:
		return err
	case <-time.After(time.Second):
		t.Fatal("Process did not return by its deadline")
		return nil
	}
}

func TestProcessIdleDeadlineBeforeInitialRequest(t *testing.T) {
	opener := &recordingOpener{}
	coordinator, err := composite.New("envoy", make([]byte, 32), composite.Limits{Capacity: 1}, opener, nil)
	if err != nil {
		t.Fatal(err)
	}
	t.Cleanup(coordinator.Close)
	server, err := newExtProcServerWithLimits(coordinator, 20*time.Millisecond, 1)
	if err != nil {
		t.Fatal(err)
	}
	ctx, cancel := context.WithCancel(context.Background())
	stream := newBlockingProcessStream(ctx)
	done := make(chan error, 1)
	go func() { done <- server.Process(stream) }()
	waitForStreamSignal(t, stream.recvEntered, "initial Recv entry")
	if code := status.Code(waitForProcessResult(t, done)); code != codes.DeadlineExceeded {
		t.Fatalf("Process status=%s, want DeadlineExceeded", code)
	}
	if opener.opened.TransactionID != "" {
		t.Fatalf("idle pre-request stream opened a transaction: %+v", opener.opened)
	}
	if len(stream.responses) != 0 {
		t.Fatalf("idle pre-request responses=%v, want none", stream.responses)
	}
	cancel()
	waitForStreamSignal(t, stream.recvExited, "initial Recv exit after stream cancellation")
	if err := server.Process(&processStream{}); err != nil {
		t.Fatalf("capacity was not released after idle stream: %v", err)
	}
}

func TestProcessMarkedTerminalIdleDeadlineReleasesCapacity(t *testing.T) {
	opener := &recordingOpener{}
	coordinator, err := composite.New("envoy", make([]byte, 32), composite.Limits{Capacity: 1}, opener, nil)
	if err != nil {
		t.Fatal(err)
	}
	t.Cleanup(coordinator.Close)
	server, err := newExtProcServerWithLimits(coordinator, 20*time.Millisecond, 1)
	if err != nil {
		t.Fatal(err)
	}
	ctx, cancel := context.WithCancel(context.Background())
	stream := newBlockingProcessStream(ctx)
	stream.requests <- terminalResponseHeaders("403", false)
	done := make(chan error, 1)
	go func() { done <- server.Process(stream) }()
	waitForStreamSignal(t, stream.recvEntered, "marked-terminal initial Recv entry")
	waitForStreamSignal(t, stream.recvExited, "marked-terminal initial Recv exit")
	waitForStreamSignal(t, stream.recvEntered, "marked-terminal continuation Recv entry")
	if code := status.Code(waitForProcessResult(t, done)); code != codes.DeadlineExceeded {
		t.Fatalf("marked-terminal Process status=%s, want DeadlineExceeded", code)
	}
	if len(stream.responses) != 1 || stream.responses[0].GetResponseHeaders() == nil || stream.responses[0].GetImmediateResponse() != nil {
		t.Fatalf("responses=%v, want only marked response-header CONTINUE", stream.responses)
	}
	if opener.opened.TransactionID != "" {
		t.Fatalf("marked terminal idle stream opened a transaction: %+v", opener.opened)
	}
	cancel()
	waitForStreamSignal(t, stream.recvExited, "marked-terminal continuation Recv exit after stream cancellation")
	if err := server.Process(&processStream{}); err != nil {
		t.Fatalf("capacity was not released after marked-terminal idle stream: %v", err)
	}
}

func TestProcessIdleDeadlineAfterClaimClosesResponseAndReleasesCapacity(t *testing.T) {
	closed := make(chan processor.Summary, 1)
	opener := &responseOpener{action: processor.ActionAllow, bodyAction: processor.ActionAllow, status: 200, closeSummary: closed}
	observer := &eventObserver{notify: make(chan composite.Event, 8)}
	coordinator, err := composite.New("envoy", make([]byte, 32), composite.Limits{Capacity: 1}, opener, observer)
	if err != nil {
		t.Fatal(err)
	}
	t.Cleanup(coordinator.Close)
	authz, err := NewAuthzServer(coordinator)
	if err != nil {
		t.Fatal(err)
	}
	check, err := authz.Check(context.Background(), authCheckRequest(nil))
	if err != nil {
		t.Fatal(err)
	}
	lease := check.GetDynamicMetadata().GetFields()[metadataLease].GetStringValue()
	if lease == "" {
		t.Fatal("fixture did not receive a lease")
	}
	server, err := newExtProcServerWithLimits(coordinator, 20*time.Millisecond, 1)
	if err != nil {
		t.Fatal(err)
	}
	ctx, cancel := context.WithCancel(context.Background())
	stream := newBlockingProcessStream(ctx)
	stream.requests <- initialRequest(lease)
	done := make(chan error, 1)
	go func() { done <- server.Process(stream) }()
	waitForStreamSignal(t, stream.recvEntered, "claimed initial Recv entry")
	waitForStreamSignal(t, stream.recvExited, "claimed initial Recv exit")
	waitForStreamSignal(t, stream.recvEntered, "claimed response-loop Recv entry")
	if code := status.Code(waitForProcessResult(t, done)); code != codes.DeadlineExceeded {
		t.Fatalf("Process status=%s, want DeadlineExceeded", code)
	}
	if len(stream.responses) != 1 || stream.responses[0].GetRequestHeaders() == nil || stream.responses[0].GetImmediateResponse() != nil {
		t.Fatalf("responses=%v, want only request-header CONTINUE", stream.responses)
	}
	select {
	case summary := <-closed:
		if summary.CloseReason != processor.CloseReason("grpc_stream_idle_timeout") {
			t.Fatalf("close reason=%q, want grpc_stream_idle_timeout", summary.CloseReason)
		}
	case <-time.After(time.Second):
		t.Fatal("claimed idle stream did not close its transaction")
	}
	for {
		select {
		case event := <-observer.notify:
			if event.Phase == "terminal" {
				if event.Reason != "grpc_stream_idle_timeout" || event.CleanupOutcome != "closed" {
					t.Fatalf("terminal event=%+v, want idle timeout cleanup", event)
				}
				goto terminalObserved
			}
		case <-time.After(time.Second):
			t.Fatal("claimed idle stream did not emit a terminal event")
		}
	}

terminalObserved:
	next, err := authz.Check(context.Background(), authCheckRequest(nil))
	if err != nil || next.GetOkResponse() == nil {
		t.Fatalf("capacity was not released for a legitimate follow-up: response=%v err=%v", next, err)
	}
	cancel()
	waitForStreamSignal(t, stream.recvExited, "claimed response-loop Recv exit after stream cancellation")
}

func TestProcessIdleDeadlineResetsAfterEachMessage(t *testing.T) {
	opener := &responseOpener{action: processor.ActionAllow, bodyAction: processor.ActionAllow, status: 200}
	coordinator, err := composite.New("envoy", make([]byte, 32), composite.Limits{Capacity: 1}, opener, nil)
	if err != nil {
		t.Fatal(err)
	}
	t.Cleanup(coordinator.Close)
	authz, err := NewAuthzServer(coordinator)
	if err != nil {
		t.Fatal(err)
	}
	check, err := authz.Check(context.Background(), authCheckRequest(nil))
	if err != nil {
		t.Fatal(err)
	}
	lease := check.GetDynamicMetadata().GetFields()[metadataLease].GetStringValue()
	if lease == "" {
		t.Fatal("fixture did not receive a lease")
	}
	server, err := newExtProcServerWithLimits(coordinator, 100*time.Millisecond, 1)
	if err != nil {
		t.Fatal(err)
	}
	stream := newBlockingProcessStream(context.Background())
	stream.requests <- initialResponseHeaders(lease, "200", false)
	done := make(chan error, 1)
	go func() { done <- server.Process(stream) }()
	waitForStreamSignal(t, stream.recvEntered, "initial response-header Recv entry")
	waitForStreamSignal(t, stream.recvExited, "initial response-header Recv exit")
	waitForStreamSignal(t, stream.recvEntered, "first response-body Recv entry")
	time.Sleep(60 * time.Millisecond)
	stream.requests <- &extprocv3.ProcessingRequest{Request: &extprocv3.ProcessingRequest_ResponseBody{ResponseBody: &extprocv3.HttpBody{Body: []byte("first"), EndOfStream: false}}}
	waitForStreamSignal(t, stream.recvExited, "first response-body Recv exit")
	waitForStreamSignal(t, stream.recvEntered, "second response-body Recv entry")
	time.Sleep(60 * time.Millisecond)
	stream.requests <- &extprocv3.ProcessingRequest{Request: &extprocv3.ProcessingRequest_ResponseBody{ResponseBody: &extprocv3.HttpBody{EndOfStream: true}}}
	if err := waitForProcessResult(t, done); err != nil {
		t.Fatalf("active streamed response did not complete: %v", err)
	}
	if len(stream.responses) != 3 || stream.responses[0].GetResponseHeaders() == nil || stream.responses[1].GetResponseBody() == nil || stream.responses[2].GetResponseBody() == nil {
		t.Fatalf("responses=%v, want response-header and two response-body CONTINUE messages", stream.responses)
	}
}

func TestProcessRejectsStreamsBeyondProcessWideCapacity(t *testing.T) {
	coordinator, err := composite.New("envoy", make([]byte, 32), composite.Limits{Capacity: 1}, &recordingOpener{}, nil)
	if err != nil {
		t.Fatal(err)
	}
	t.Cleanup(coordinator.Close)
	server, err := newExtProcServerWithLimits(coordinator, time.Second, 1)
	if err != nil {
		t.Fatal(err)
	}
	ctx, cancel := context.WithCancel(context.Background())
	stream := newBlockingProcessStream(ctx)
	done := make(chan error, 1)
	go func() { done <- server.Process(stream) }()
	waitForStreamSignal(t, stream.recvEntered, "capacity-held Recv entry")
	if code := status.Code(server.Process(&processStream{})); code != codes.ResourceExhausted {
		t.Fatalf("overflow Process status=%s, want ResourceExhausted", code)
	}
	cancel()
	if err := waitForProcessResult(t, done); err != nil {
		t.Fatalf("cancelled Process err=%v, want nil", err)
	}
	waitForStreamSignal(t, stream.recvExited, "capacity-held Recv exit")
	if err := server.Process(&processStream{}); err != nil {
		t.Fatalf("capacity was not released after cancellation: %v", err)
	}
}

func TestProcessIdleDeadlineClosesARealGRPCStream(t *testing.T) {
	coordinator, err := composite.New("envoy", make([]byte, 32), composite.Limits{Capacity: 1}, &recordingOpener{}, nil)
	if err != nil {
		t.Fatal(err)
	}
	t.Cleanup(coordinator.Close)
	server, err := newExtProcServerWithLimits(coordinator, 20*time.Millisecond, 1)
	if err != nil {
		t.Fatal(err)
	}
	listener := bufconn.Listen(1 << 20)
	grpcServer := grpc.NewServer()
	extprocv3.RegisterExternalProcessorServer(grpcServer, server)
	go func() { _ = grpcServer.Serve(listener) }()
	t.Cleanup(func() {
		grpcServer.Stop()
		_ = listener.Close()
	})
	dialCtx, cancelDial := context.WithTimeout(context.Background(), time.Second)
	defer cancelDial()
	connection, err := grpc.DialContext(dialCtx, "bufnet", grpc.WithContextDialer(func(context.Context, string) (net.Conn, error) {
		return listener.Dial()
	}), grpc.WithTransportCredentials(insecure.NewCredentials()), grpc.WithBlock())
	if err != nil {
		t.Fatal(err)
	}
	t.Cleanup(func() { _ = connection.Close() })
	client := extprocv3.NewExternalProcessorClient(connection)
	ctx, cancel := context.WithTimeout(context.Background(), time.Second)
	defer cancel()
	started := time.Now()
	stream, err := client.Process(ctx)
	if err != nil {
		t.Fatal(err)
	}
	_, err = stream.Recv()
	if code := status.Code(err); code != codes.DeadlineExceeded {
		t.Fatalf("real gRPC idle stream status=%s err=%v, want DeadlineExceeded", code, err)
	}
	if elapsed := time.Since(started); elapsed > 500*time.Millisecond {
		t.Fatalf("real gRPC idle deadline took %s, want bounded server-side timeout", elapsed)
	}
}

type eventObserver struct {
	events []composite.Event
	notify chan composite.Event
}

func (o *eventObserver) Observe(event composite.Event) error {
	o.events = append(o.events, event)
	if o.notify != nil {
		select {
		case o.notify <- event:
		default:
		}
	}
	return nil
}

type responseOpener struct {
	action        processor.Action
	bodyAction    processor.Action
	status        int
	commitErr     error
	hostActionErr error
	bodyErr       error
	closeSummary  chan processor.Summary
	tx            *responseTransaction
}

func (o *responseOpener) Open(_ context.Context, _ processor.StreamMetadata) (processor.Transaction, error) {
	o.tx = &responseTransaction{action: o.action, bodyAction: o.bodyAction, status: o.status, commitErr: o.commitErr, hostActionErr: o.hostActionErr, bodyErr: o.bodyErr, closeSummary: o.closeSummary}
	return o.tx, nil
}

type responseTransaction struct {
	action            processor.Action
	bodyAction        processor.Action
	bodyActions       []processor.Action
	status            int
	actions           []processor.HostAction
	commits           int
	commitErr         error
	hostActionErr     error
	bodyErr           error
	expectedTransport string
	closeSummary      chan processor.Summary
}

func (t *responseTransaction) ProcessHeaders(_ context.Context, direction processor.Direction, _ []processor.Header, _ bool) (processor.Decision, error) {
	if direction == processor.DirectionResponse {
		return processor.Decision{Action: t.action, Status: t.status}, nil
	}
	return processor.Decision{Action: processor.ActionAllow}, nil
}
func (t *responseTransaction) ProcessBody(_ context.Context, direction processor.Direction, _ []byte, _ bool) (processor.Decision, error) {
	if direction == processor.DirectionResponse {
		if t.bodyErr != nil {
			return processor.Decision{}, t.bodyErr
		}
		action := t.bodyAction
		if len(t.bodyActions) != 0 {
			action = t.bodyActions[0]
			t.bodyActions = t.bodyActions[1:]
		}
		return processor.Decision{Action: action, Status: t.status}, nil
	}
	return processor.Decision{Action: processor.ActionAllow}, nil
}

func TestProcessP4ProcessingErrorDoesNotSendSecondImmediateResponse(t *testing.T) {
	server, opener, _, lease := newProcessFixture(t, processor.ActionAllow, 200)
	// Configure the transaction before ext_proc claims it; the fixture opener
	// copies this fault into the transaction at Open time.
	opener.tx.bodyErr = errors.New("body inspection failed")
	stream := &processStream{requests: []*extprocv3.ProcessingRequest{
		initialRequest(lease),
		{Request: &extprocv3.ProcessingRequest_ResponseHeaders{ResponseHeaders: &extprocv3.HttpHeaders{Headers: &corev3.HeaderMap{Headers: []*corev3.HeaderValue{{Key: ":status", Value: "200"}}}}}},
		{Request: &extprocv3.ProcessingRequest_ResponseBody{ResponseBody: &extprocv3.HttpBody{Body: []byte("body"), EndOfStream: true}}},
	}}
	if err := server.Process(stream); err == nil {
		t.Fatal("post-commit body error unexpectedly succeeded")
	}
	if len(stream.responses) != 2 || stream.responses[1].GetResponseHeaders() == nil {
		t.Fatalf("responses=%v, want only the committed P3 CONTINUE", stream.responses)
	}
}
func (t *responseTransaction) Close(_ context.Context, summary processor.Summary) {
	if t.closeSummary != nil {
		t.closeSummary <- summary
	}
}
func (t *responseTransaction) RecordHostAction(_ context.Context, action processor.HostAction) error {
	if t.hostActionErr != nil {
		return t.hostActionErr
	}
	if t.expectedTransport != "" && action.TransportResult != t.expectedTransport {
		return errors.New("noncanonical Common transport result")
	}
	t.actions = append(t.actions, action)
	return nil
}
func (t *responseTransaction) MarkResponseCommitted(context.Context) error {
	t.commits++
	return t.commitErr
}

func newProcessFixture(t *testing.T, action processor.Action, statusCode int) (*ExtProcServer, *responseOpener, *eventObserver, string) {
	return newProcessFixtureWithActions(t, action, action, statusCode)
}

func newProcessFixtureWithActions(t *testing.T, headerAction, bodyAction processor.Action, statusCode int) (*ExtProcServer, *responseOpener, *eventObserver, string) {
	return newProcessFixtureWithFailures(t, headerAction, bodyAction, statusCode, nil, nil)
}

func newProcessFixtureWithFailures(t *testing.T, headerAction, bodyAction processor.Action, statusCode int, commitErr, hostActionErr error) (*ExtProcServer, *responseOpener, *eventObserver, string) {
	t.Helper()
	opener := &responseOpener{action: headerAction, bodyAction: bodyAction, status: statusCode, commitErr: commitErr, hostActionErr: hostActionErr}
	observer := &eventObserver{notify: make(chan composite.Event, 64)}
	coordinator, err := composite.New("envoy", make([]byte, 32), composite.Limits{Capacity: 2}, opener, observer)
	if err != nil {
		t.Fatal(err)
	}
	t.Cleanup(coordinator.Close)
	authz, err := NewAuthzServer(coordinator)
	if err != nil {
		t.Fatal(err)
	}
	check, err := authz.Check(context.Background(), &authv3.CheckRequest{Attributes: &authv3.AttributeContext{Source: &authv3.AttributeContext_Peer{Address: testAddress("127.0.0.1", 1234)}, Destination: &authv3.AttributeContext_Peer{Address: testAddress("127.0.0.1", 8080)}, Request: &authv3.AttributeContext_Request{Http: &authv3.AttributeContext_HttpRequest{Method: "GET", Path: "/", Host: "example.test", Protocol: "HTTP/1.1"}}}})
	if err != nil {
		t.Fatal(err)
	}
	lease, ok := check.GetDynamicMetadata().GetFields()["lease"]
	if !ok {
		t.Fatal("fixture did not receive lease")
	}
	returnServer, err := NewExtProcServer(coordinator)
	if err != nil {
		t.Fatal(err)
	}
	return returnServer, opener, observer, lease.GetStringValue()
}

func processRequest(lease string, request *extprocv3.ProcessingRequest) *extprocv3.ProcessingRequest {
	request.MetadataContext = &corev3.Metadata{FilterMetadata: map[string]*structpb.Struct{metadataNamespace: {Fields: map[string]*structpb.Value{"lease": structpb.NewStringValue(lease), "version": structpb.NewNumberValue(1)}}}}
	return request
}

func initialRequest(lease string) *extprocv3.ProcessingRequest {
	return processRequest(lease, &extprocv3.ProcessingRequest{Request: &extprocv3.ProcessingRequest_RequestHeaders{RequestHeaders: &extprocv3.HttpHeaders{}}})
}

func initialResponseHeaders(lease string, status string, endOfStream bool) *extprocv3.ProcessingRequest {
	return processRequest(lease, &extprocv3.ProcessingRequest{Request: &extprocv3.ProcessingRequest_ResponseHeaders{ResponseHeaders: &extprocv3.HttpHeaders{EndOfStream: endOfStream, Headers: &corev3.HeaderMap{Headers: []*corev3.HeaderValue{{Key: ":status", Value: status}}}}}})
}

func terminalResponseHeaders(status string, endOfStream bool) *extprocv3.ProcessingRequest {
	return &extprocv3.ProcessingRequest{MetadataContext: &corev3.Metadata{FilterMetadata: map[string]*structpb.Struct{metadataNamespace: terminalBlockMetadata()}}, Request: &extprocv3.ProcessingRequest_ResponseHeaders{ResponseHeaders: &extprocv3.HttpHeaders{EndOfStream: endOfStream, Headers: &corev3.HeaderMap{Headers: []*corev3.HeaderValue{{Key: ":status", Value: status}}}}}}
}

func TestProcessMissingMetadataFailsClosed503(t *testing.T) {
	server, _, _, _ := newProcessFixture(t, processor.ActionAllow, 200)
	stream := &processStream{requests: []*extprocv3.ProcessingRequest{{Request: &extprocv3.ProcessingRequest_ResponseHeaders{ResponseHeaders: &extprocv3.HttpHeaders{EndOfStream: true, Headers: &corev3.HeaderMap{Headers: []*corev3.HeaderValue{{Key: ":status", Value: "403"}}}}}}}}
	if err := server.Process(stream); err != nil {
		t.Fatal(err)
	}
	if len(stream.responses) != 1 || stream.responses[0].GetImmediateResponse().GetStatus().GetCode() != 503 {
		t.Fatalf("responses=%v, want one 503 immediate response", stream.responses)
	}
}

func TestProcessMarkedTerminalLocalReplyContinuesWithoutClaim(t *testing.T) {
	opener := &responseOpener{}
	coordinator, err := composite.New("envoy", make([]byte, 32), composite.Limits{Capacity: 2}, opener, nil)
	if err != nil {
		t.Fatal(err)
	}
	t.Cleanup(coordinator.Close)
	server, err := NewExtProcServer(coordinator)
	if err != nil {
		t.Fatal(err)
	}
	stream := &processStream{requests: []*extprocv3.ProcessingRequest{terminalResponseHeaders("413", true)}}
	if err := server.Process(stream); err != nil {
		t.Fatal(err)
	}
	if len(stream.responses) != 1 || stream.responses[0].GetResponseHeaders() == nil {
		t.Fatalf("responses=%v, want one terminal response-header CONTINUE", stream.responses)
	}
	if opener.tx != nil {
		t.Fatal("marked terminal local reply opened or claimed a Common transaction")
	}
}

func TestProcessP3DenyImmediateAndAction(t *testing.T) {
	server, opener, _, lease := newProcessFixture(t, processor.ActionDeny, 451)
	opener.tx.expectedTransport = commonTransportHTTPStatus
	stream := &processStream{requests: []*extprocv3.ProcessingRequest{initialRequest(lease), {Request: &extprocv3.ProcessingRequest_ResponseHeaders{ResponseHeaders: &extprocv3.HttpHeaders{Headers: &corev3.HeaderMap{Headers: []*corev3.HeaderValue{{Key: ":status", Value: "200"}}}}}}}}
	if err := server.Process(stream); err != nil {
		t.Fatal(err)
	}
	if len(stream.responses) != 2 || stream.responses[1].GetImmediateResponse() == nil {
		t.Fatalf("responses=%v, want P3 immediate response", stream.responses)
	}
	if got := int(stream.responses[1].GetImmediateResponse().GetStatus().GetCode()); got != 451 {
		t.Fatalf("P3 visible status=%d, want 451", got)
	}
	if len(opener.tx.actions) != 1 || opener.tx.actions[0].Action != processor.AppliedActionDeny || opener.tx.actions[0].VisibleStatus != 451 || opener.tx.actions[0].TransportResult != commonTransportHTTPStatus {
		t.Fatalf("actions=%v, want deny", opener.tx.actions)
	}
}

func TestProcessMarkedTerminalRedirectPassesThrough(t *testing.T) {
	const location = "https://redirect.example.test/next"
	opener := &strictRequestOpener{headerAction: processor.ActionRedirect, bodyAction: processor.ActionAllow, status: 307, redirectURL: location}
	coordinator, err := composite.New("envoy", make([]byte, 32), composite.Limits{Capacity: 2}, opener, nil)
	if err != nil {
		t.Fatal(err)
	}
	t.Cleanup(coordinator.Close)
	authz, err := NewAuthzServer(coordinator)
	if err != nil {
		t.Fatal(err)
	}
	terminal, err := authz.Check(context.Background(), authCheckRequest(nil))
	if err != nil {
		t.Fatal(err)
	}
	if terminal.GetDeniedResponse() == nil || int(terminal.GetDeniedResponse().GetStatus().GetCode()) != 307 {
		t.Fatalf("terminal response=%v, want redirect 307", terminal)
	}
	requestTransaction := opener.tx
	server, err := NewExtProcServer(coordinator)
	if err != nil {
		t.Fatal(err)
	}
	stream := &processStream{requests: []*extprocv3.ProcessingRequest{{
		MetadataContext: &corev3.Metadata{FilterMetadata: map[string]*structpb.Struct{metadataNamespace: terminal.GetDynamicMetadata()}},
		Request: &extprocv3.ProcessingRequest_ResponseHeaders{ResponseHeaders: &extprocv3.HttpHeaders{
			EndOfStream: true,
			Headers:     &corev3.HeaderMap{Headers: []*corev3.HeaderValue{{Key: ":status", Value: "307"}, {Key: "location", Value: location}}},
		}},
	}}}
	if err := server.Process(stream); err != nil {
		t.Fatal(err)
	}
	if len(stream.responses) != 1 || stream.responses[0].GetResponseHeaders() == nil || stream.responses[0].GetImmediateResponse() != nil {
		t.Fatalf("responses=%v, want terminal redirect continuation", stream.responses)
	}
	if opener.tx != requestTransaction {
		t.Fatal("marked terminal redirect opened a second transaction")
	}
}

func TestProcessMarkedTerminalServerErrorPassesThrough(t *testing.T) {
	server, opener, _, _ := newProcessFixture(t, processor.ActionAllow, 200)
	requestTransaction := opener.tx
	stream := &processStream{requests: []*extprocv3.ProcessingRequest{terminalResponseHeaders("500", true)}}
	if err := server.Process(stream); err != nil {
		t.Fatal(err)
	}
	if len(stream.responses) != 1 || stream.responses[0].GetResponseHeaders() == nil || stream.responses[0].GetImmediateResponse() != nil {
		t.Fatalf("responses=%v, want terminal 500 continuation", stream.responses)
	}
	if opener.tx != requestTransaction {
		t.Fatal("marked terminal 500 opened a second Common transaction")
	}
}

func TestProcessMarkedTerminalInvalidRedirectFailsClosed(t *testing.T) {
	tests := []struct {
		name    string
		headers []*corev3.HeaderValue
	}{
		{name: "missing location", headers: []*corev3.HeaderValue{{Key: ":status", Value: "307"}}},
		{name: "duplicate location", headers: []*corev3.HeaderValue{{Key: ":status", Value: "307"}, {Key: "location", Value: "https://redirect.example.test/a"}, {Key: "location", Value: "https://redirect.example.test/b"}}},
		{name: "newline location", headers: []*corev3.HeaderValue{{Key: ":status", Value: "307"}, {Key: "location", Value: "https://redirect.example.test/next\r\nX-Injected: true"}}},
	}
	for _, test := range tests {
		t.Run(test.name, func(t *testing.T) {
			opener := &responseOpener{}
			coordinator, err := composite.New("envoy", make([]byte, 32), composite.Limits{Capacity: 2}, opener, nil)
			if err != nil {
				t.Fatal(err)
			}
			t.Cleanup(coordinator.Close)
			server, err := NewExtProcServer(coordinator)
			if err != nil {
				t.Fatal(err)
			}
			stream := &processStream{requests: []*extprocv3.ProcessingRequest{{
				MetadataContext: &corev3.Metadata{FilterMetadata: map[string]*structpb.Struct{metadataNamespace: terminalBlockMetadata()}},
				Request:         &extprocv3.ProcessingRequest_ResponseHeaders{ResponseHeaders: &extprocv3.HttpHeaders{EndOfStream: true, Headers: &corev3.HeaderMap{Headers: test.headers}}},
			}}}
			if err := server.Process(stream); err != nil {
				t.Fatal(err)
			}
			if len(stream.responses) != 1 || stream.responses[0].GetImmediateResponse() == nil || int(stream.responses[0].GetImmediateResponse().GetStatus().GetCode()) != 503 {
				t.Fatalf("responses=%v, want one fail-closed 503", stream.responses)
			}
			if opener.tx != nil {
				t.Fatal("invalid marked redirect opened a Common transaction")
			}
		})
	}
}

func TestProcessNormalizesMalformedP3DenyStatus(t *testing.T) {
	for _, malformedStatus := range []int{103, 200, 600} {
		t.Run(strconv.Itoa(malformedStatus), func(t *testing.T) {
			server, opener, _, lease := newProcessFixture(t, processor.ActionDeny, malformedStatus)
			opener.tx.expectedTransport = commonTransportHTTPStatus
			stream := &processStream{requests: []*extprocv3.ProcessingRequest{
				initialRequest(lease),
				{Request: &extprocv3.ProcessingRequest_ResponseHeaders{ResponseHeaders: &extprocv3.HttpHeaders{Headers: &corev3.HeaderMap{Headers: []*corev3.HeaderValue{{Key: ":status", Value: "200"}}}}}},
			}}
			if err := server.Process(stream); err != nil {
				t.Fatal(err)
			}
			if len(stream.responses) != 2 || stream.responses[1].GetImmediateResponse() == nil || int(stream.responses[1].GetImmediateResponse().GetStatus().GetCode()) != 403 {
				t.Fatalf("responses=%v, want P3 immediate status 403", stream.responses)
			}
			if len(opener.tx.actions) != 1 || opener.tx.actions[0].Action != processor.AppliedActionDeny || opener.tx.actions[0].VisibleStatus != 403 || opener.tx.actions[0].TransportResult != commonTransportHTTPStatus {
				t.Fatalf("host actions=%v, want one deny status 403", opener.tx.actions)
			}
		})
	}
}

func TestSendImmediatePreservesValidatedRedirect(t *testing.T) {
	stream := &processStream{}
	if err := sendImmediate(stream, processor.Decision{Action: processor.ActionRedirect, Status: 307, RedirectURL: "https://redirect.example.test/next"}); err != nil {
		t.Fatal(err)
	}
	if len(stream.responses) != 1 || stream.responses[0].GetImmediateResponse() == nil {
		t.Fatalf("responses=%v, want one redirect immediate response", stream.responses)
	}
	immediate := stream.responses[0].GetImmediateResponse()
	if got := int(immediate.GetStatus().GetCode()); got != 307 {
		t.Fatalf("redirect status=%d, want 307", got)
	}
	headers := immediate.GetHeaders().GetSetHeaders()
	if len(headers) != 1 || headers[0].GetHeader().GetKey() != "location" || headers[0].GetHeader().GetValue() != "https://redirect.example.test/next" {
		t.Fatalf("redirect headers=%v, want one location", headers)
	}
}

func TestProcessP4DisruptiveContinuesLogOnly(t *testing.T) {
	server, opener, _, lease := newProcessFixtureWithActions(t, processor.ActionAllow, processor.ActionDeny, 451)
	opener.tx.expectedTransport = commonTransportLogOnly
	stream := &processStream{requests: []*extprocv3.ProcessingRequest{initialRequest(lease), {Request: &extprocv3.ProcessingRequest_ResponseHeaders{ResponseHeaders: &extprocv3.HttpHeaders{Headers: &corev3.HeaderMap{Headers: []*corev3.HeaderValue{{Key: ":status", Value: "204"}}}}}}, {Request: &extprocv3.ProcessingRequest_ResponseBody{ResponseBody: &extprocv3.HttpBody{Body: []byte("body"), EndOfStream: true}}}}}
	if err := server.Process(stream); err != nil {
		t.Fatal(err)
	}
	if len(stream.responses) != 3 || stream.responses[2].GetImmediateResponse() != nil {
		t.Fatalf("responses=%v, want P4 CONTINUE", stream.responses)
	}
	if len(opener.tx.actions) != 1 || opener.tx.actions[0].Action != processor.AppliedActionLogOnly || opener.tx.actions[0].VisibleStatus != 204 || opener.tx.actions[0].TransportResult != commonTransportLogOnly {
		t.Fatalf("actions=%v, want status 204 log_only", opener.tx.actions)
	}
}

func TestProcessStreamedP4DenyEmitsOnceAndSuppressesNeutralAllow(t *testing.T) {
	server, opener, observer, lease := newProcessFixtureWithActions(t, processor.ActionAllow, processor.ActionAllow, 451)
	opener.tx.bodyActions = []processor.Action{processor.ActionDeny, processor.ActionAllow}
	opener.tx.expectedTransport = commonTransportLogOnly
	stream := &processStream{requests: []*extprocv3.ProcessingRequest{
		initialRequest(lease),
		{Request: &extprocv3.ProcessingRequest_ResponseHeaders{ResponseHeaders: &extprocv3.HttpHeaders{Headers: &corev3.HeaderMap{Headers: []*corev3.HeaderValue{{Key: ":status", Value: "200"}}}}}},
		{Request: &extprocv3.ProcessingRequest_ResponseBody{ResponseBody: &extprocv3.HttpBody{Body: []byte("first"), EndOfStream: false}}},
		{Request: &extprocv3.ProcessingRequest_ResponseBody{ResponseBody: &extprocv3.HttpBody{EndOfStream: true}}},
	}}
	if err := server.Process(stream); err != nil {
		t.Fatal(err)
	}
	if len(opener.tx.actions) != 1 || opener.tx.actions[0].Action != processor.AppliedActionLogOnly {
		t.Fatalf("actions=%v, want one P4 log_only action", opener.tx.actions)
	}
	p4, neutral := eventCountsUntilTerminal(t, observer)
	if p4 != 1 || neutral != 0 {
		t.Fatalf("P4=%d neutral=%d, want one P4 and no neutral allow after log_only", p4, neutral)
	}
}

func TestProcessStreamedP4AllowEmitsAtEOSAndRecordsNeutralAllow(t *testing.T) {
	server, _, observer, lease := newProcessFixtureWithActions(t, processor.ActionAllow, processor.ActionAllow, 200)
	stream := &processStream{requests: []*extprocv3.ProcessingRequest{
		initialRequest(lease),
		{Request: &extprocv3.ProcessingRequest_ResponseHeaders{ResponseHeaders: &extprocv3.HttpHeaders{Headers: &corev3.HeaderMap{Headers: []*corev3.HeaderValue{{Key: ":status", Value: "200"}}}}}},
		{Request: &extprocv3.ProcessingRequest_ResponseBody{ResponseBody: &extprocv3.HttpBody{Body: []byte("first"), EndOfStream: false}}},
		{Request: &extprocv3.ProcessingRequest_ResponseBody{ResponseBody: &extprocv3.HttpBody{EndOfStream: true}}},
	}}
	if err := server.Process(stream); err != nil {
		t.Fatal(err)
	}
	p4, neutral := eventCountsUntilTerminal(t, observer)
	if p4 != 1 || neutral != 1 {
		t.Fatalf("P4=%d neutral=%d, want one P4 and one neutral allow", p4, neutral)
	}
}

func eventCountsUntilTerminal(t *testing.T, observer *eventObserver) (int, int) {
	t.Helper()
	p4, neutral := 0, 0
	deadline := time.NewTimer(time.Second)
	defer deadline.Stop()
	for {
		select {
		case event := <-observer.notify:
			switch event.Phase {
			case "P4":
				p4++
			case "neutral_outcome":
				if event.ActualHostAction == "allow" {
					neutral++
				}
			case "terminal":
				return p4, neutral
			}
		case <-deadline.C:
			t.Fatal("timed out waiting for terminal composite event")
		}
	}
}

func TestProcessHeaderOnlyAllowNeutralOutcome(t *testing.T) {
	server, opener, observer, lease := newProcessFixture(t, processor.ActionAllow, 200)
	stream := &processStream{requests: []*extprocv3.ProcessingRequest{initialResponseHeaders(lease, "201", true)}}
	if err := server.Process(stream); err != nil {
		t.Fatal(err)
	}
	if len(stream.responses) != 1 || stream.responses[0].GetResponseHeaders() == nil {
		t.Fatalf("responses=%v, want header CONTINUE", stream.responses)
	}
	found := false
	deadline := time.NewTimer(time.Second)
	defer deadline.Stop()
	for !found {
		select {
		case event := <-observer.notify:
			if event.Phase == "neutral_outcome" && event.ActualHostAction == "allow" {
				found = true
			}
		case <-deadline.C:
			t.Fatalf("events=%v, want neutral allow", observer.events)
		}
	}
	if !found {
		t.Fatalf("events=%v, want neutral allow", observer.events)
	}
	if opener.tx == nil {
		t.Fatal("transaction missing")
	}
}

func TestProcessHeaderOnlyDenyEmitsFinalP4BeforeTerminalization(t *testing.T) {
	server, _, observer, lease := newProcessFixture(t, processor.ActionDeny, 451)
	stream := &processStream{requests: []*extprocv3.ProcessingRequest{initialRequest(lease), initialResponseHeaders(lease, "200", true)}}
	if err := server.Process(stream); err != nil {
		t.Fatal(err)
	}
	p4, neutral := eventCountsUntilTerminal(t, observer)
	if p4 != 1 || neutral != 0 {
		t.Fatalf("P4=%d neutral=%d, want final disruptive P4 and no neutral allow", p4, neutral)
	}
}

func TestProcessOutOfOrderResponseFailsClosed(t *testing.T) {
	server, _, _, lease := newProcessFixture(t, processor.ActionAllow, 200)
	stream := &processStream{requests: []*extprocv3.ProcessingRequest{initialRequest(lease), {Request: &extprocv3.ProcessingRequest_ResponseBody{ResponseBody: &extprocv3.HttpBody{EndOfStream: true}}}}}
	if err := server.Process(stream); err != nil {
		t.Fatal(err)
	}
	if len(stream.responses) != 2 || stream.responses[1].GetImmediateResponse().GetStatus().GetCode() != 503 {
		t.Fatalf("responses=%v, want out-of-order 503", stream.responses)
	}
}

func TestProcessP3ImmediateRecorderFailureLeavesOutcomeUnknown(t *testing.T) {
	server, opener, _, lease := newProcessFixtureWithFailures(t, processor.ActionDeny, processor.ActionDeny, 451, nil, errors.New("recorder failed"))
	stream := &processStream{requests: []*extprocv3.ProcessingRequest{
		initialRequest(lease),
		{Request: &extprocv3.ProcessingRequest_ResponseHeaders{ResponseHeaders: &extprocv3.HttpHeaders{Headers: &corev3.HeaderMap{Headers: []*corev3.HeaderValue{{Key: ":status", Value: "200"}}}}}},
	}}
	if err := server.Process(stream); err == nil {
		t.Fatal("P3 recorder failure unexpectedly succeeded")
	}
	if len(stream.responses) != 2 || stream.responses[1].GetImmediateResponse() == nil {
		t.Fatalf("responses=%v, want only the already-sent P3 ImmediateResponse", stream.responses)
	}
	if len(opener.tx.actions) != 0 {
		t.Fatalf("actions=%v, must not claim an action after recorder failure", opener.tx.actions)
	}
}

func TestProcessP3AllowCommitFailureDoesNotSendSecondDecision(t *testing.T) {
	server, opener, _, lease := newProcessFixtureWithFailures(t, processor.ActionAllow, processor.ActionAllow, 200, errors.New("commit recorder failed"), nil)
	stream := &processStream{requests: []*extprocv3.ProcessingRequest{
		initialRequest(lease),
		{Request: &extprocv3.ProcessingRequest_ResponseHeaders{ResponseHeaders: &extprocv3.HttpHeaders{Headers: &corev3.HeaderMap{Headers: []*corev3.HeaderValue{{Key: ":status", Value: "204"}}}}}},
	}}
	if err := server.Process(stream); err == nil {
		t.Fatal("P3 commit failure unexpectedly succeeded")
	}
	if len(stream.responses) != 2 || stream.responses[1].GetResponseHeaders() == nil || stream.responses[1].GetImmediateResponse() != nil {
		t.Fatalf("responses=%v, want only the already-sent P3 CONTINUE", stream.responses)
	}
	if opener.tx.commits != 1 {
		t.Fatalf("commit attempts=%d, want 1", opener.tx.commits)
	}
}
