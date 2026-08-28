package main

import (
	"context"
	"net"
	"testing"
	"time"

	extprocv3 "github.com/envoyproxy/go-control-plane/envoy/service/ext_proc/v3"
	"google.golang.org/grpc"
	"google.golang.org/grpc/credentials/insecure"
	"google.golang.org/grpc/test/bufconn"
	"google.golang.org/protobuf/proto"
)

type responseObserverReceiveProbe struct {
	extprocv3.UnimplementedExternalProcessorServer
	received chan int
}

func (probe *responseObserverReceiveProbe) Process(stream extprocv3.ExternalProcessor_ProcessServer) error {
	request, err := stream.Recv()
	if err != nil {
		return err
	}
	probe.received <- len(request.GetResponseBody().GetBody())
	return stream.Send(&extprocv3.ProcessingResponse{
		Response: &extprocv3.ProcessingResponse_ResponseBody{
			ResponseBody: &extprocv3.BodyResponse{
				Response: &extprocv3.CommonResponse{Status: extprocv3.CommonResponse_CONTINUE},
			},
		},
	})
}

func TestResponseObserverGRPCReceiveLimitAdmitsBoundedResponseBody(t *testing.T) {
	body := make([]byte, 1<<20)
	request := &extprocv3.ProcessingRequest{
		Request: &extprocv3.ProcessingRequest_ResponseBody{
			ResponseBody: &extprocv3.HttpBody{Body: body, EndOfStream: true},
		},
	}
	if size := proto.Size(request); size > responseObserverMaxRecvMessageBytes {
		t.Fatalf("bounded response body serializes to %d bytes, receive bound is only %d", size, responseObserverMaxRecvMessageBytes)
	}

	listener := bufconn.Listen(responseObserverMaxRecvMessageBytes + 1024)
	probe := &responseObserverReceiveProbe{received: make(chan int, 1)}
	server := newResponseObserverGRPCServer(probe)
	defer server.Stop()
	go func() { _ = server.Serve(listener) }()
	defer listener.Close()

	contextValue, cancel := context.WithTimeout(context.Background(), 5*time.Second)
	defer cancel()
	connection, err := grpc.DialContext(
		contextValue,
		"bufnet",
		grpc.WithContextDialer(func(context.Context, string) (net.Conn, error) {
			return listener.Dial()
		}),
		grpc.WithTransportCredentials(insecure.NewCredentials()),
	)
	if err != nil {
		t.Fatalf("dial response observer: %v", err)
	}
	defer connection.Close()

	stream, err := extprocv3.NewExternalProcessorClient(connection).Process(contextValue)
	if err != nil {
		t.Fatalf("open response observer stream: %v", err)
	}
	if err := stream.Send(request); err != nil {
		t.Fatalf("send bounded response body: %v", err)
	}
	if _, err := stream.Recv(); err != nil {
		t.Fatalf("receive response observer acknowledgement: %v", err)
	}
	select {
	case received := <-probe.received:
		if received != len(body) {
			t.Fatalf("response observer received %d bytes, want %d", received, len(body))
		}
	case <-contextValue.Done():
		t.Fatal("response observer did not receive the bounded body")
	}
}
